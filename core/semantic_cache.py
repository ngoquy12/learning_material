"""
core/semantic_cache.py

Semantic Response Cache — Lớp cache ngữ nghĩa cho LLM
=======================================================
Mục tiêu:
- Tránh gọi LLM khi cùng 1 prompt đã được xử lý trước đó
- Tiết kiệm token cost khi nhiều giáo viên tạo bài học tương tự
- Không thay đổi interface của call_llm — chỉ hoạt động như middleware

Chiến lược:
1. Hash-based exact match (nhanh nhất, ưu tiên đầu)
2. TF-IDF keyword similarity cho fuzzy match (fallback không cần embedding)
3. Lưu trữ SQLite để persist giữa các lần chạy

Cách tích hợp: Bọc xung quanh call_llm bằng decorator @with_semantic_cache,
KHÔNG sửa code call_llm gốc.
"""

import os
import sqlite3
import hashlib
import json
import math
import time
from typing import Optional, List, Dict
from pathlib import Path
from functools import wraps

CACHE_DB_PATH = Path("semantic_cache.db")
SIMILARITY_THRESHOLD = float(os.getenv("CACHE_SIMILARITY_THRESHOLD", "0.88"))
MAX_CACHE_AGE_DAYS = int(os.getenv("CACHE_MAX_AGE_DAYS", "30"))
CACHE_ENABLED = os.getenv("SEMANTIC_CACHE_ENABLED", "true").lower() in ("true", "1", "yes")


# ─────────────────────────────────────────────────────
# DB Setup
# ─────────────────────────────────────────────────────

def _get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(CACHE_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS semantic_cache (
            id          TEXT PRIMARY KEY,      -- sha256(system+user prompt)
            agent_name  TEXT NOT NULL DEFAULT '',
            prompt_hash TEXT NOT NULL,         -- dùng để exact match
            prompt_text TEXT NOT NULL,         -- lưu để fuzzy match
            response    TEXT NOT NULL,
            hit_count   INTEGER DEFAULT 0,
            created_at  REAL NOT NULL,
            last_used   REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_created ON semantic_cache(created_at)
    """)
    conn.commit()
    return conn


def _make_hash(system_prompt: str, user_prompt: str) -> str:
    combined = f"SYS::{system_prompt.strip()[:500]}|USR::{user_prompt.strip()[:1000]}"
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


# ─────────────────────────────────────────────────────
# TF-IDF Keyword Similarity (zero-dependency fuzzy match)
# ─────────────────────────────────────────────────────

def _tokenize(text: str) -> List[str]:
    import re
    text = text.lower()
    return re.findall(r'\b\w+\b', text)


def _tf_idf_similarity(query: str, document: str) -> float:
    """
    Lightweight TF-IDF overlap similarity.
    Không cần embedding API, chạy hoàn toàn offline.
    """
    q_tokens = set(_tokenize(query[:2000]))
    d_tokens = set(_tokenize(document[:2000]))
    if not q_tokens or not d_tokens:
        return 0.0
    intersection = q_tokens & d_tokens
    # Jaccard similarity với bonus cho độ dài phù hợp
    jaccard = len(intersection) / len(q_tokens | d_tokens)
    # Bonus: tỷ lệ query terms xuất hiện trong document
    coverage = len(intersection) / len(q_tokens)
    return (jaccard + coverage) / 2.0


# ─────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────

def cache_lookup(
    system_prompt: str,
    user_prompt: str,
    agent_name: str = "",
    fuzzy: bool = True,
) -> Optional[str]:
    """
    Tìm kiếm phản hồi trong cache.
    
    Returns:
        Chuỗi response nếu cache HIT, None nếu MISS.
    """
    if not CACHE_ENABLED:
        return None

    conn = _get_db()
    try:
        prompt_hash = _make_hash(system_prompt, user_prompt)
        now = time.time()
        cutoff = now - (MAX_CACHE_AGE_DAYS * 86400)

        # 1. Exact hash match (tốc độ O(1))
        row = conn.execute(
            "SELECT id, response FROM semantic_cache WHERE prompt_hash = ? AND created_at > ?",
            (prompt_hash, cutoff)
        ).fetchone()

        if row:
            conn.execute(
                "UPDATE semantic_cache SET hit_count = hit_count + 1, last_used = ? WHERE id = ?",
                (now, row["id"])
            )
            conn.commit()
            print(f"  [SemanticCache] [EXACT HIT] for {agent_name}. Skipping LLM call.")
            return row["response"]

        # 2. Fuzzy similarity match
        if fuzzy:
            combined_query = f"{system_prompt[:400]} {user_prompt[:800]}"
            candidates = conn.execute(
                "SELECT id, prompt_text, response FROM semantic_cache WHERE created_at > ? LIMIT 200",
                (cutoff,)
            ).fetchall()

            best_sim = 0.0
            best_row = None
            for candidate in candidates:
                sim = _tf_idf_similarity(combined_query, candidate["prompt_text"])
                if sim > best_sim:
                    best_sim = sim
                    best_row = candidate

            if best_row and best_sim >= SIMILARITY_THRESHOLD:
                conn.execute(
                    "UPDATE semantic_cache SET hit_count = hit_count + 1, last_used = ? WHERE id = ?",
                    (now, best_row["id"])
                )
                conn.commit()
                print(f"  [SemanticCache] [FUZZY HIT] for {agent_name} (similarity={best_sim:.2f}). Skipping LLM call.")
                return best_row["response"]

        return None
    finally:
        conn.close()


def cache_store(
    system_prompt: str,
    user_prompt: str,
    response: str,
    agent_name: str = "",
) -> None:
    """
    Lưu một phản hồi mới vào cache.
    Chỉ cache những response có nội dung thực sự (>10 chars).
    """
    if not CACHE_ENABLED:
        return
    if not response or len(response.strip()) < 10:
        return

    conn = _get_db()
    try:
        prompt_hash = _make_hash(system_prompt, user_prompt)
        combined_prompt = f"{system_prompt[:400]} {user_prompt[:800]}"
        entry_id = "cache_" + prompt_hash[:16]
        now = time.time()

        # INSERT OR IGNORE (không ghi đè nếu đã tồn tại) + cập nhật response nếu cần
        conn.execute("""
            INSERT OR IGNORE INTO semantic_cache
                (id, agent_name, prompt_hash, prompt_text, response, hit_count, created_at, last_used)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
        """, (entry_id, agent_name, prompt_hash, combined_prompt, response, now, now))
        conn.commit()
    except Exception as e:
        print(f"  [SemanticCache Warning] Failed to store cache entry: {e}")
    finally:
        conn.close()



def cache_invalidate_old() -> int:
    """Xóa các entry cache quá hạn. Trả về số lượng đã xóa."""
    conn = _get_db()
    try:
        cutoff = time.time() - (MAX_CACHE_AGE_DAYS * 86400)
        cursor = conn.execute("DELETE FROM semantic_cache WHERE created_at < ?", (cutoff,))
        conn.commit()
        deleted = cursor.rowcount
        if deleted:
            print(f"  [SemanticCache] Cleaned up {deleted} expired cache entries.")
        return deleted
    finally:
        conn.close()


def get_cache_stats() -> Dict:
    """Thống kê cache để monitor."""
    conn = _get_db()
    try:
        total = conn.execute("SELECT COUNT(*) FROM semantic_cache").fetchone()[0]
        hits = conn.execute("SELECT SUM(hit_count) FROM semantic_cache").fetchone()[0] or 0
        by_agent = conn.execute(
            "SELECT agent_name, COUNT(*) as cnt, SUM(hit_count) as total_hits "
            "FROM semantic_cache GROUP BY agent_name ORDER BY cnt DESC"
        ).fetchall()
        return {
            "total_cached_responses": total,
            "total_cache_hits": hits,
            "estimated_tokens_saved": hits * 800,  # avg 800 tokens per call
            "by_agent": {r["agent_name"]: {"cached": r["cnt"], "hits": r["total_hits"]} for r in by_agent},
        }
    finally:
        conn.close()


# ─────────────────────────────────────────────────────
# Decorator — dùng để bọc call_llm
# ─────────────────────────────────────────────────────

def with_semantic_cache(func):
    """
    Decorator để bọc call_llm với semantic cache.
    Dùng thay vì sửa trực tiếp call_llm.
    
    Cách dùng:
        from core.semantic_cache import with_semantic_cache
        from core.llm import call_llm as _call_llm
        call_llm = with_semantic_cache(_call_llm)
    """
    @wraps(func)
    def wrapper(system_prompt, user_prompt, json_mode=False, agent_name="Unknown Agent",
                session_id="", lesson_id="", *args, **kwargs):
        # Không cache các agent quan trọng cần output mới (Reviewer, PM Guard, các trình sinh tạo)
        no_cache_prefixes = {
            "PM_Reviewer",
            "Objective_Reviewer",
            "PrerequisiteGuard",
            "Homework Creator",
            "Homework Reviewer",
            "Practice Creator",
            "Practice Reviewer",
            "Entry Test Creator",
            "SRS Creator",
            "Mini Project Creator"
        }
        if any(agent_name.startswith(prefix) for prefix in no_cache_prefixes):
            return func(system_prompt, user_prompt, json_mode=json_mode,
                       agent_name=agent_name, session_id=session_id,
                       lesson_id=lesson_id, *args, **kwargs)

        # 1. Tìm trong cache
        cached = cache_lookup(system_prompt, user_prompt, agent_name=agent_name)
        if cached:
            return cached

        # 2. Gọi LLM thật
        result = func(system_prompt, user_prompt, json_mode=json_mode,
                     agent_name=agent_name, session_id=session_id,
                     lesson_id=lesson_id, *args, **kwargs)

        # 3. Lưu vào cache nếu thành công
        if result:
            cache_store(system_prompt, user_prompt, result, agent_name=agent_name)

        return result

    return wrapper
