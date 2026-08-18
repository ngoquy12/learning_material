"""
agents/knowledge_memory_agent.py

Agent 1 — Knowledge Memory Agent (KMA)
=======================================
Cải tiến từ lessons_learned_agent.py với kiến trúc:
- Kho lưu trữ có cấu trúc (SQLite) thay vì flat Markdown list
- Phân loại lỗi theo error_category, severity, tech_stack, scope
- Creator Agent có thể TRUY VẤN kho này trước khi sinh nội dung
- Tự động loại bỏ các rule trùng lặp & hợp nhất rule tương đồng

Triết lý thiết kế:
- "Đừng để Agent mắc 2 lần cùng 1 lỗi"
- "Rule phải cụ thể, đo lường được, áp dụng được ngay"
"""

import os
import sqlite3
import json
import hashlib
import re
import math
from collections import Counter
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.state import AgentState
from pathlib import Path

# ─────────────────────────────────────────────
# TF-IDF + Cosine Similarity Engine (Semantic Fallback)
# ─────────────────────────────────────────────
class TFIDFMatcher:
    def __init__(self, documents: List[str]):
        self.documents = documents
        self.num_docs = len(documents)
        
        # Tokenize all documents
        self.tokenized_docs = [self._tokenize(doc) for doc in documents]
        
        # Compute IDF
        self.vocab = set()
        for doc in self.tokenized_docs:
            self.vocab.update(doc)
            
        self.idf = {}
        for term in self.vocab:
            # Number of documents containing term
            df = sum(1 for doc in self.tokenized_docs if term in doc)
            self.idf[term] = math.log((1 + self.num_docs) / (1 + df)) + 1
            
        # Compute TF-IDF vectors for documents
        self.doc_vectors = []
        for doc in self.tokenized_docs:
            vector = self._compute_vector(doc)
            self.doc_vectors.append(vector)
            
    def _tokenize(self, text: str) -> List[str]:
        # Simple lowercase tokenizer
        text = text.lower()
        # Keep only alphanumeric words
        words = re.findall(r'\w+', text)
        return words
        
    def _compute_vector(self, words: List[str]) -> Dict[str, float]:
        tf = Counter(words)
        vector = {}
        for term, count in tf.items():
            if term in self.idf:
                vector[term] = count * self.idf[term]
        # Normalize vector (make it unit length)
        sq_sum = sum(v ** 2 for v in vector.values())
        norm = math.sqrt(sq_sum)
        if norm > 0:
            for term in vector:
                vector[term] /= norm
        return vector

    def get_similarity(self, query: str) -> List[float]:
        if not self.vocab or not query:
            return [0.0] * self.num_docs
        query_words = self._tokenize(query)
        query_vector = self._compute_vector(query_words)
        
        scores = []
        for doc_vector in self.doc_vectors:
            # Cosine similarity is the dot product since vectors are normalized
            dot_product = sum(query_vector.get(term, 0.0) * doc_vector.get(term, 0.0) for term in query_vector)
            scores.append(dot_product)
        return scores


# ─────────────────────────────────────────────
# Schema của 1 Memory Entry
# ─────────────────────────────────────────────
"""
TABLE: agent_memory
  id              TEXT PRIMARY KEY     -- sha256 của (tech_stack + rule_text[:80])
  tech_stack      TEXT NOT NULL        -- 'python/core', 'typescript/nestjs', '*'
  error_category  TEXT NOT NULL        -- xem ERROR_CATEGORIES bên dưới
  severity        TEXT NOT NULL        -- 'CRITICAL' | 'MAJOR' | 'MINOR'
  scope           TEXT                 -- 'mindmap' | 'html' | 'quiz' | 'homework' | 'pm' | 'all'
  rule_text       TEXT NOT NULL        -- Quy tắc cụ thể, ngắn gọn
  example_bad     TEXT                 -- Ví dụ code/nội dung SAI
  example_good    TEXT                 -- Ví dụ code/nội dung ĐÚNG
  source_lesson   TEXT                 -- 'Session 03 - Lesson 02 - ...'
  source_agent    TEXT                 -- Reviewer nào phát hiện
  created_at      TEXT
  hit_count       INTEGER DEFAULT 0    -- Số lần rule này được tra cứu
"""

ERROR_CATEGORIES = [
    "scope_violation",       # Nội dung vượt phạm vi bài học
    "syntax_error",          # Cú pháp sai với công nghệ
    "format_violation",      # Vi phạm định dạng Markdown/HTML/JSON
    "prerequisite_leak",     # Dùng khái niệm chưa được dạy
    "pedagogical_error",     # Sai phương pháp sư phạm (Bloom's)
    "image_prompt_error",    # Prompt ảnh không đúng style
    "structure_error",       # Cấu trúc file/thư mục sai
    "terminology_error",     # Sai thuật ngữ chuyên môn
    "ai_mention_violation",  # Đề cập AI trong nội dung học liệu
    "other",
]

DB_PATH = Path("knowledge_store.db")


def _get_connection() -> sqlite3.Connection:
    """Trả về connection đến Knowledge Store DB."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging cho performance
    conn.execute("""
        CREATE TABLE IF NOT EXISTS agent_memory (
            id              TEXT PRIMARY KEY,
            tech_stack      TEXT NOT NULL DEFAULT '*',
            error_category  TEXT NOT NULL DEFAULT 'other',
            severity        TEXT NOT NULL DEFAULT 'MAJOR',
            scope           TEXT DEFAULT 'all',
            rule_text       TEXT NOT NULL,
            example_bad     TEXT DEFAULT '',
            example_good    TEXT DEFAULT '',
            source_lesson   TEXT DEFAULT '',
            source_agent    TEXT DEFAULT '',
            created_at      TEXT NOT NULL,
            hit_count       INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


def _make_id(tech_stack: str, rule_text: str) -> str:
    """Tạo ID ổn định từ hash để tránh trùng lặp."""
    fingerprint = f"{tech_stack.lower()}::{rule_text[:120].strip().lower()}"
    return "mem_" + hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:16]


# ─────────────────────────────────────────────
# Public API — LƯU TRỮ
# ─────────────────────────────────────────────

def store_memory(
    rule_text: str,
    tech_stack: str = "*",
    error_category: str = "other",
    severity: str = "MAJOR",
    scope: str = "all",
    example_bad: str = "",
    example_good: str = "",
    source_lesson: str = "",
    source_agent: str = "",
) -> bool:
    """
    Lưu một kinh nghiệm vào Knowledge Store.
    Trả về True nếu là rule mới, False nếu đã tồn tại.
    """
    if not rule_text or not rule_text.strip():
        return False

    rule_id = _make_id(tech_stack, rule_text)

    conn = _get_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM agent_memory WHERE id = ?", (rule_id,)
        ).fetchone()

        if existing:
            print(f"  [KMA] Rule đã tồn tại (id={rule_id[:12]}...), bỏ qua.")
            conn.close()
            return False

        conn.execute("""
            INSERT INTO agent_memory 
                (id, tech_stack, error_category, severity, scope, rule_text,
                 example_bad, example_good, source_lesson, source_agent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            rule_id, tech_stack, error_category, severity, scope, rule_text.strip(),
            example_bad, example_good, source_lesson, source_agent,
            datetime.utcnow().isoformat()
        ))
        conn.commit()
        print(f"  [KMA] ✅ Đã lưu rule mới [{severity}/{error_category}]: {rule_text[:80]}...")
        return True
    finally:
        conn.close()


# ─────────────────────────────────────────────
# Public API — TRUY VẤN
# ─────────────────────────────────────────────

def recall_memories(
    tech_stack: str = "*",
    scope: Optional[str] = None,
    error_categories: Optional[List[str]] = None,
    severity_filter: Optional[List[str]] = None,
    limit: int = 15,
    query: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Truy vấn các rule liên quan để inject vào prompt của Creator Agent.
    
    Args:
        tech_stack: Stack cụ thể hoặc '*' để lấy tất cả
        scope: Lọc theo scope ('mindmap', 'html', 'quiz', 'all', ...)
        error_categories: Lọc theo loại lỗi
        severity_filter: ['CRITICAL', 'MAJOR'] để lọc theo mức độ
        limit: Số rule tối đa trả về
        query: Chuỗi văn bản ngữ cảnh để so khớp độ tương đồng ngữ nghĩa TF-IDF
    
    Returns:
        Danh sách dict chứa các rule liên quan
    """
    conn = _get_connection()
    try:
        conditions = []
        params = []

        # Lọc theo tech_stack: khớp chính xác, universal rules, hoặc khớp substring phân cấp
        conditions.append("(tech_stack = ? OR tech_stack = '*' OR ? LIKE '%' || tech_stack || '%' OR tech_stack LIKE '%' || ? || '%')")
        params.extend([tech_stack, tech_stack, tech_stack])

        if scope:
            conditions.append("(scope = ? OR scope = 'all')")
            params.append(scope)

        if error_categories:
            placeholders = ",".join("?" * len(error_categories))
            conditions.append(f"error_category IN ({placeholders})")
            params.extend(error_categories)

        if severity_filter:
            placeholders = ",".join("?" * len(severity_filter))
            conditions.append(f"severity IN ({placeholders})")
            params.extend(severity_filter)

        where = " AND ".join(conditions) if conditions else "1=1"
        
        # Nếu dùng Semantic Search, ta không dùng LIMIT cứng trong SQL để lấy được tập ứng viên rộng hơn trước khi xếp hạng
        sql_limit = limit * 4 if query else limit
        
        sql_query = f"""
            SELECT * FROM agent_memory
            WHERE {where}
            ORDER BY 
                CASE severity 
                    WHEN 'CRITICAL' THEN 1 
                    WHEN 'MAJOR' THEN 2 
                    ELSE 3 
                END,
                hit_count DESC,
                created_at DESC
            LIMIT ?
        """
        params.append(sql_limit)

        rows = conn.execute(sql_query, params).fetchall()
        memories = [dict(r) for r in rows]

        # ── ÁP DỤNG TF-IDF COSINE SIMILARITY ĐỂ XẾP HẠNG NGỮ NGHĨA ──
        if query and memories:
            doc_texts = [f"{m.get('rule_text', '')} {m.get('error_category', '')}" for m in memories]
            try:
                matcher = TFIDFMatcher(doc_texts)
                scores = matcher.get_similarity(query)
                # Ghép điểm số tương đồng vào từng memory
                for idx, score in enumerate(scores):
                    memories[idx]["_sim_score"] = score
                
                # Sắp xếp lại danh sách memories:
                # 1. Độ nghiêm trọng (CRITICAL lên trước)
                # 2. Điểm số tương đồng ngữ nghĩa (giảm dần)
                # 3. Hit count / Ngày tạo
                memories.sort(
                    key=lambda m: (
                        0 if m.get("severity") == "CRITICAL" else (1 if m.get("severity") == "MAJOR" else 2),
                        -m.get("_sim_score", 0.0),
                        -m.get("hit_count", 0)
                    )
                )
            except Exception as e:
                print(f"  [Semantic KMA Warning] Lỗi so khớp TF-IDF: {e}. Fallback về sắp xếp SQL mặc định.")

        # Chỉ lấy số lượng theo limit yêu cầu
        final_memories = memories[:limit]

        # Cập nhật hit_count để ưu tiên rule hay được dùng
        if final_memories:
            ids = [r["id"] for r in final_memories]
            conn.execute(
                f"UPDATE agent_memory SET hit_count = hit_count + 1 WHERE id IN ({','.join('?'*len(ids))})",
                ids
            )
            conn.commit()

        return final_memories
    finally:
        conn.close()


def format_memories_for_prompt(memories: List[Dict[str, Any]]) -> str:
    """
    Format danh sách memory thành đoạn văn bản để inject vào system prompt.
    Creator Agent sẽ thấy đây như là "kinh nghiệm của thế hệ trước".
    """
    if not memories:
        return ""

    lines = [
        "## 📚 KINH NGHIỆM TỪ CÁC LẦN CHẠY TRƯỚC (Phải tuân thủ nghiêm ngặt):",
        ""
    ]
    for i, m in enumerate(memories, 1):
        sev_icon = "🔴" if m["severity"] == "CRITICAL" else ("🟡" if m["severity"] == "MAJOR" else "⚪")
        lines.append(f"{sev_icon} [{m['error_category']}] {m['rule_text']}")
        if m.get("example_bad"):
            lines.append(f"   ❌ ĐỪNG: {m['example_bad'][:100]}")
        if m.get("example_good"):
            lines.append(f"   ✅ NÊN: {m['example_good'][:100]}")
    lines.append("")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# Public API — AGENT NODE (tích hợp vào pipeline)
# ─────────────────────────────────────────────

def knowledge_memory_agent(state: AgentState) -> AgentState:
    """
    Node Agent tích hợp vào graph pipeline.
    Chạy SAU mỗi lần Reviewer reject để lưu kinh nghiệm mới.
    
    Cải tiến so với lessons_learned_agent cũ:
    1. Lưu có cấu trúc vào SQLite (thay vì append Markdown)
    2. Phân loại tự động bằng LLM
    3. Trích xuất example_bad và example_good
    """
    from core.llm import call_llm

    review_logs = state.get("review_logs", [])
    if not review_logs:
        return state

    session_id = state.get("session_id", "")
    lesson_id = state.get("lesson_id", "")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "knowledge_memory_agent")
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "")

    source_lesson = f"{session_id} - {lesson_id} - {lesson_title}".strip(" -")

    print(f"\n[KMA] Phân tích {len(review_logs)} nhật ký lỗi để cập nhật kho tri thức...")

    logs_text = "\n\n".join([
        f"Reviewer: {log.get('source', 'Unknown')}\nFeedback: {log.get('feedback', '')}"
        for log in review_logs
    ])

    system_prompt = (
        "You are a Lead Curriculum Quality & AI Memory Engineer at Rikkei Education.\n"
        "Your task: Analyze review error logs and extract actionable error prevention memory rules.\n"
        "Categorize errors into: scope_violation, syntax_error, format_violation, "
        "prerequisite_leak, pedagogical_error, image_prompt_error, structure_error, "
        "terminology_error, ai_mention_violation, other.\n"
        "Identify target scope: mindmap, html, quiz, homework, pm, all.\n"
        "Severity levels: CRITICAL (causes crash/rejection), MAJOR (significant quality impact), MINOR (small enhancement)."
    )

    user_prompt = f"""Review error log history from curriculum generation pipeline:
Tech Stack: {tech_stack}
Lesson Context: {source_lesson}

--- ERROR LOG HISTORY ---
{logs_text}

Extract up to 3 concise, non-redundant rules in JSON array format:
[
  {{
    "rule_text": "Specific, measurable, directly applicable technical rule in Accented Vietnamese",
    "error_category": "category from above list",
    "severity": "CRITICAL|MAJOR|MINOR",
    "scope": "affected scope",
    "example_bad": "Short anti-pattern example (optional)",
    "example_good": "Short best practice example (optional)"
  }}
]

Return ONLY raw JSON array without markdown wrappers.
"""

    new_rules = []
    try:
        response = call_llm(
            system_prompt, user_prompt,
            json_mode=True,
            agent_name="Knowledge_Memory_Agent",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if response:
            cleaned = response.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            parsed = json.loads(cleaned)
            if isinstance(parsed, list):
                new_rules = parsed
    except Exception as e:
        print(f"  [KMA Warning] LLM phân loại lỗi thất bại: {e}. Dùng fallback.")

    # Fallback: lưu rule thô từ logs
    if not new_rules:
        for log in review_logs:
            feedback = log.get("feedback", "")
            if feedback:
                new_rules.append({
                    "rule_text": f"Lưu ý: {feedback[:200]}",
                    "error_category": "other",
                    "severity": "MAJOR",
                    "scope": "all",
                    "example_bad": "",
                    "example_good": ""
                })

    saved_count = 0
    for rule in new_rules:
        is_new = store_memory(
            rule_text=rule.get("rule_text", ""),
            tech_stack=tech_stack,
            error_category=rule.get("error_category", "other"),
            severity=rule.get("severity", "MAJOR"),
            scope=rule.get("scope", "all"),
            example_bad=rule.get("example_bad", ""),
            example_good=rule.get("example_good", ""),
            source_lesson=source_lesson,
            source_agent=", ".join(set(log.get("source", "") for log in review_logs)),
        )
        if is_new:
            saved_count += 1

    print(f"  [KMA] Đã lưu {saved_count}/{len(new_rules)} rule mới vào Knowledge Store.")
    return state


def get_relevant_memories_for_creator(tech_stack: str, scope: str, limit: int = 10, query: Optional[str] = None) -> str:
    """
    Hàm tiện ích cho Creator Agent gọi để lấy context kinh nghiệm.
    Trả về chuỗi text sẵn sàng inject vào system prompt.
    """
    memories = recall_memories(
        tech_stack=tech_stack,
        scope=scope,
        severity_filter=["CRITICAL", "MAJOR"],
        limit=limit,
        query=query
    )
    return format_memories_for_prompt(memories)


def get_memory_stats() -> Dict[str, Any]:
    """Thống kê kho tri thức để monitor."""
    conn = _get_connection()
    try:
        total = conn.execute("SELECT COUNT(*) FROM agent_memory").fetchone()[0]
        by_category = conn.execute(
            "SELECT error_category, COUNT(*) as cnt FROM agent_memory GROUP BY error_category ORDER BY cnt DESC"
        ).fetchall()
        by_severity = conn.execute(
            "SELECT severity, COUNT(*) as cnt FROM agent_memory GROUP BY severity"
        ).fetchall()
        by_stack = conn.execute(
            "SELECT tech_stack, COUNT(*) as cnt FROM agent_memory GROUP BY tech_stack ORDER BY cnt DESC"
        ).fetchall()
        return {
            "total_rules": total,
            "by_category": {r["error_category"]: r["cnt"] for r in by_category},
            "by_severity": {r["severity"]: r["cnt"] for r in by_severity},
            "by_stack": {r["tech_stack"]: r["cnt"] for r in by_stack},
        }
    finally:
        conn.close()


def extract_anti_patterns(tech_stack: str = "*", limit: int = 3) -> str:
    """
    Trích xuất danh sách các bẫy lỗi lập trình thường gặp (Anti-Pattern Catalog) từ KMA 
    để tự động chèn vào Slide/Bài đọc HTML cho học viên.
    """
    memories = recall_memories(tech_stack=tech_stack, scope="all", limit=limit)
    if not memories:
        return ""
        
    lines = ["### ⚠️ Các cạm bẫy lập trình thường gặp & Cách khắc phục:"]
    for idx, mem in enumerate(memories, start=1):
        rule = mem.get("rule_text", "")
        bad = mem.get("example_bad", "")
        good = mem.get("example_good", "")
        
        entry = f"{idx}. **Lỗi thường gặp:** {rule}"
        if bad:
            entry += f"\n   - ❌ **Cách làm sai:** `{bad}`"
        if good:
            entry += f"\n   - ✅ **Cách sửa đúng:** `{good}`"
        lines.append(entry)
        
    return "\n".join(lines)

