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

from core.paths import get_cache_db_path

CACHE_DB_PATH = get_cache_db_path()
SIMILARITY_THRESHOLD = float(os.getenv("CACHE_SIMILARITY_THRESHOLD", "0.88"))
MAX_CACHE_AGE_DAYS = int(os.getenv("CACHE_MAX_AGE_DAYS", "30"))
CACHE_ENABLED = os.getenv("SEMANTIC_CACHE_ENABLED", "true").lower() in ("true", "1", "yes")


# ─────────────────────────────────────────────────────
# DB Setup
# ─────────────────────────────────────────────────────

from core.persistence import get_db_pool
from contextlib import contextmanager

_cache_db_initialized = False

def _init_cache_db(conn: sqlite3.Connection):
    global _cache_db_initialized
    if _cache_db_initialized:
        return
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS semantic_cache (
            id          TEXT PRIMARY KEY,      -- sha256(namespace+system+user prompt)
            agent_name  TEXT NOT NULL DEFAULT '',
            namespace   TEXT NOT NULL DEFAULT '',  -- phạm vi cô lập: khoá học/buổi/bài/agent
            prompt_hash TEXT NOT NULL,         -- dùng để exact match
            prompt_text TEXT NOT NULL,         -- lưu để fuzzy match
            response    TEXT NOT NULL,
            hit_count   INTEGER DEFAULT 0,
            created_at  REAL NOT NULL,
            last_used   REAL NOT NULL
        )
    """)
    # Di trú DB đã tồn tại từ trước khi có cột namespace. Các entry cũ nhận
    # namespace rỗng, nghĩa là chúng KHÔNG bao giờ khớp với truy vấn mới (vốn luôn
    # có namespace thật). Đây là hành vi cố ý: entry cũ được sinh ra khi cache còn
    # dùng chung cho mọi bài học, nên không thể tin là đúng phạm vi kiến thức nào.
    existing_columns = {row[1] for row in conn.execute("PRAGMA table_info(semantic_cache)")}
    if "namespace" not in existing_columns:
        conn.execute("ALTER TABLE semantic_cache ADD COLUMN namespace TEXT NOT NULL DEFAULT ''")
        print("  [SemanticCache] Đã bổ sung cột namespace; entry cũ không còn được tái sử dụng.")
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_created ON semantic_cache(created_at)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_namespace ON semantic_cache(namespace, created_at)
    """)
    conn.commit()
    _cache_db_initialized = True

@contextmanager
def get_cache_db():
    """Retrieves a thread-pooled connection for semantic_cache.db."""
    pool = get_db_pool(str(CACHE_DB_PATH))
    with pool.get_connection() as conn:
        conn.row_factory = sqlite3.Row
        _init_cache_db(conn)
        yield conn


# Tiền tố phạm vi cho cả lượt chạy — thường là mã/khoá thư mục khoá học. Đặt MỘT LẦN
# lúc khởi động CLI, trước khi bất kỳ luồng nào chạy, rồi chỉ đọc.
_NAMESPACE_PREFIX = ""


def set_cache_namespace_prefix(prefix: str) -> None:
    """
    Khai báo phạm vi bao ngoài của cache cho lượt chạy hiện tại (thường là khoá học).

    Cần thiết vì hai khoá học khác nhau đều có "Session 01 / Lesson 01": nếu không
    tách, bài mở đầu của khoá Python có thể ăn cache của bài mở đầu khoá Java.
    """
    global _NAMESPACE_PREFIX
    _NAMESPACE_PREFIX = (prefix or "").strip()


def get_cache_namespace_prefix() -> str:
    return _NAMESPACE_PREFIX


def build_namespace(agent_name: str = "", session_id: str = "", lesson_id: str = "") -> str:
    """
    Dựng khoá phạm vi cô lập cache.

    Vì sao phải có: `cache_lookup` đối sánh mờ bằng TF-IDF với ngưỡng 0.88 trên
    TOÀN BỘ bảng cache. Hai bài học liền kề cùng chủ đề (Lesson 02 và Lesson 03 về
    List chẳng hạn) có prompt gần như trùng nhau về từ vựng, nên hoàn toàn có thể
    vượt ngưỡng và ăn cache của nhau. Khi đó bài sau nhận lại nội dung của bài
    trước — nội dung ĐÚNG NGỮ PHÁP nhưng SAI PHẠM VI KIẾN THỨC, và không có gì báo
    lỗi vì kết quả trông vẫn hợp lệ.

    Thành phần agent_name cũng bắt buộc: prompt của Reading Creator và Quiz Creator
    cho cùng một bài chia sẻ rất nhiều từ vựng chung, không được phép khớp chéo.
    """
    parts = [_NAMESPACE_PREFIX, str(agent_name or ""), str(session_id or ""), str(lesson_id or "")]
    return "|".join(p.strip() for p in parts)


def _make_hash(system_prompt: str, user_prompt: str, namespace: str = "") -> str:
    # Namespace nằm TRONG hash vì id của entry lấy từ hash này làm khoá chính.
    # Không đưa vào thì hai bài học có prompt trùng nhau sẽ đụng khoá chính và
    # `INSERT OR IGNORE` lặng lẽ vứt bản ghi thứ hai.
    combined = (
        f"NS::{namespace}|SYS::{system_prompt.strip()[:500]}|USR::{user_prompt.strip()[:1000]}"
    )
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

def _record_cache_hit(agent_name: str) -> None:
    """
    Báo cho sổ đo lượt chạy biết vừa có một lượt KHÔNG tốn tiền.

    Không có con số này thì tỷ lệ cache hit của chính lượt chạy hiện tại không tính
    được: get_cache_stats() cộng dồn hit của mọi lượt chạy trong 30 ngày qua.
    """
    try:
        from core.run_metrics import record_cache_hit
        record_cache_hit(agent_name)
    except Exception:
        pass


def cache_lookup(
    system_prompt: str,
    user_prompt: str,
    agent_name: str = "",
    fuzzy: bool = True,
    namespace: str = "",
) -> Optional[str]:
    """
    Tìm kiếm phản hồi trong cache.
    
    Returns:
        Chuỗi response nếu cache HIT, None nếu MISS.
    """
    if not CACHE_ENABLED:
        return None

    with get_cache_db() as conn:
        prompt_hash = _make_hash(system_prompt, user_prompt, namespace)
        now = time.time()
        cutoff = now - (MAX_CACHE_AGE_DAYS * 86400)

        # 1. Exact hash match (tốc độ O(1))
        row = conn.execute(
            "SELECT id, response FROM semantic_cache "
            "WHERE prompt_hash = ? AND namespace = ? AND created_at > ?",
            (prompt_hash, namespace, cutoff)
        ).fetchone()

        if row:
            resp_text = row["response"]
            import re
            emoji_match = re.search(
                r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF]",
                resp_text, flags=re.UNICODE
            )
            if emoji_match:
                conn.execute("DELETE FROM semantic_cache WHERE id = ?", (row["id"],))
                conn.commit()
            else:
                conn.execute(
                    "UPDATE semantic_cache SET hit_count = hit_count + 1, last_used = ? WHERE id = ?",
                    (now, row["id"])
                )
                conn.commit()
                print(f"  [SemanticCache] [EXACT HIT] for {agent_name}. Skipping LLM call.")
                _record_cache_hit(agent_name)
                return resp_text

        # 2. Fuzzy similarity match
        if fuzzy:
            combined_query = f"{system_prompt[:400]} {user_prompt[:800]}"
            # CHỈ đối sánh mờ trong cùng phạm vi. Bỏ điều kiện namespace ở đây là
            # mở lại đúng lỗ hổng nội dung lệch phạm vi kiến thức mô tả ở build_namespace().
            candidates = conn.execute(
                "SELECT id, prompt_text, response FROM semantic_cache "
                "WHERE namespace = ? AND created_at > ? LIMIT 200",
                (namespace, cutoff)
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
                _record_cache_hit(agent_name)
                return best_row["response"]

        return None


def cache_store(
    system_prompt: str,
    user_prompt: str,
    response: str,
    agent_name: str = "",
    namespace: str = "",
) -> None:
    """
    Lưu một phản hồi mới vào cache.
    Chỉ cache những response có nội dung thực sự (>10 chars).
    """
    if not CACHE_ENABLED:
        return
    if not response or len(response.strip()) < 10:
        return

    try:
        with get_cache_db() as conn:
            prompt_hash = _make_hash(system_prompt, user_prompt, namespace)
            combined_prompt = f"{system_prompt[:400]} {user_prompt[:800]}"
            entry_id = "cache_" + prompt_hash[:16]
            now = time.time()

            # INSERT OR IGNORE (không ghi đè nếu đã tồn tại) + cập nhật response nếu cần
            conn.execute("""
                INSERT OR IGNORE INTO semantic_cache
                    (id, agent_name, namespace, prompt_hash, prompt_text, response, hit_count, created_at, last_used)
                VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?)
            """, (entry_id, agent_name, namespace, prompt_hash, combined_prompt, response, now, now))
            conn.commit()
    except Exception as e:
        print(f"  [SemanticCache Warning] Failed to store cache entry: {e}")



def cache_invalidate_old() -> int:
    """Xóa các entry cache quá hạn. Trả về số lượng đã xóa."""
    with get_cache_db() as conn:
        cutoff = time.time() - (MAX_CACHE_AGE_DAYS * 86400)
        cursor = conn.execute("DELETE FROM semantic_cache WHERE created_at < ?", (cutoff,))
        conn.commit()
        deleted = cursor.rowcount
        if deleted:
            print(f"  [SemanticCache] Cleaned up {deleted} expired cache entries.")
        return deleted


def get_cache_stats() -> Dict:
    """Thống kê cache để monitor."""
    with get_cache_db() as conn:
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

        # Namespace dựng từ chính session_id/lesson_id mà wrapper VỐN ĐÃ NHẬN nhưng
        # trước đây không hề dùng tới — cache vì thế dùng chung cho mọi bài học.
        namespace = build_namespace(agent_name, session_id, lesson_id)

        # 1. Tìm trong cache
        cached = cache_lookup(system_prompt, user_prompt, agent_name=agent_name, namespace=namespace)
        if cached:
            return cached

        # 2. Gọi LLM thật
        result = func(system_prompt, user_prompt, json_mode=json_mode,
                     agent_name=agent_name, session_id=session_id,
                     lesson_id=lesson_id, *args, **kwargs)

        # 3. Lưu vào cache nếu thành công
        if result:
            cache_store(system_prompt, user_prompt, result, agent_name=agent_name, namespace=namespace)

        return result

    return wrapper
