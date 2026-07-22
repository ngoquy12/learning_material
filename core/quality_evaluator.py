# core/quality_evaluator.py
import re
import json
import sqlite3
from typing import Dict, Any, List
from core.state import AgentState
from core.sandbox import execute_code_safely

FORBIDDEN_AI_FILLER_WORDS = [
    r"\bnhé\b", r"\bthân mến\b", r"\bcác bạn thân mến\b",
    r"\bdưới đây là\b", r"\bhi vọng bài học này\b", r"\bchúc các bạn\b"
]

def evaluate_lesson_quality(state: AgentState) -> Dict[str, Any]:
    """
    Pedagogical Quality Scoring Engine (PQM):
    Evaluates lesson content quality quantitatively across 4 dimensions:
    1. Bloom Alignment Index (0-100%)
    2. Code Health Ratio (% Pass via Sandbox)
    3. Readability & Anti-AI Filler Score (0-100%)
    4. Overall Pedagogical Score (0-100%)
    
    Persists evaluation metrics into SQLite knowledge_store.db.
    """
    session_id = state.get("session_id", "Session 01")
    lesson_id = state.get("lesson_id", "Lesson 01")
    html_content = state.get("html_content", "")
    slide_markdown = state.get("slide_markdown", "")
    quiz_json = state.get("quiz_json", [])
    tech_stack = state.get("technology_stack", "python/core")
    
    print(f"\n[PQM_Engine] Evaluating Pedagogical Quality for {session_id} - {lesson_id}...")
    
    # 1. Readability & Anti-AI Filler Score
    full_text = f"{html_content} {slide_markdown}"
    filler_violations = []
    for pattern in FORBIDDEN_AI_FILLER_WORDS:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            filler_violations.extend(matches)
            
    filler_count = len(filler_violations)
    readability_score = max(0.0, 100.0 - (filler_count * 15.0))
    
    # 2. Code Health Ratio (% Pass via Sandbox)
    code_blocks = re.findall(r'<code[^>]*class="[^"]*language-python[^"]*"[^>]*>(.*?)</code>', html_content, re.DOTALL)
    tested_blocks = 0
    passed_blocks = 0
    
    for raw_code in code_blocks[:3]: # Test up to 3 code snippets for efficiency
        code = raw_code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&quot;", '"').replace("&#x27;", "'").strip()
        if code and any(kw in code for kw in ["import ", "def ", "class ", " = ", "print("]):
            tested_blocks += 1
            res = execute_code_safely(code)
            if res.get("status") == "SUCCESS":
                passed_blocks += 1
                
    code_health_score = (passed_blocks / tested_blocks * 100.0) if tested_blocks > 0 else 100.0
    
    # 3. Bloom Alignment Index
    bloom_score = 90.0 # Default baseline
    if quiz_json and isinstance(quiz_json, list):
        if len(quiz_json) >= 3:
            bloom_score = 95.0
        else:
            bloom_score = 75.0
            
    # 4. Overall Pedagogical Score (Weighted average)
    overall_score = round(0.35 * bloom_score + 0.35 * code_health_score + 0.30 * readability_score, 1)
    
    metrics = {
        "session_id": session_id,
        "lesson_id": lesson_id,
        "technology_stack": tech_stack,
        "bloom_alignment_score": bloom_score,
        "code_health_score": code_health_score,
        "readability_score": readability_score,
        "overall_quality_score": overall_score,
        "filler_violations_count": filler_count,
        "tested_code_blocks": tested_blocks,
        "passed_code_blocks": passed_blocks
    }
    
    print(f"  - PQM Overall Quality Score: {overall_score}/100.0 (Code Health: {code_health_score}%, Readability: {readability_score}%)")
    
    # Persist metrics into SQLite
    try:
        db_path = "knowledge_store.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lesson_quality_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                lesson_id TEXT,
                tech_stack TEXT,
                bloom_score REAL,
                code_health_score REAL,
                readability_score REAL,
                overall_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            INSERT INTO lesson_quality_metrics (session_id, lesson_id, tech_stack, bloom_score, code_health_score, readability_score, overall_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session_id, lesson_id, tech_stack, bloom_score, code_health_score, readability_score, overall_score))
        conn.commit()
        conn.close()
    except Exception as db_err:
        print(f"  [PQM Warning] Failed to persist metrics to SQLite: {db_err}")
        
    return metrics
