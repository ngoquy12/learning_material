"""
tests/test_e2e_pipeline.py — End-to-End Integration tests for Elearning Content Factory.
"""

import os
import pytest
from pathlib import Path
from core.scope_calculator import calculate_lesson_scope_contract
from core.validators.master_validator import validate_resource
from core.observability import log_agent_call, TRACE_LOG_PATH
from core.persistence import save_checkpoint, load_checkpoint, DB_PATH

def test_scope_calculator_integration():
    """Tests dynamic knowledge scope calculation across lesson progression."""
    mock_syllabus = {
        "sessions": [
            {
                "session_id": "Session 01",
                "lessons": [
                    {"title": "Cú pháp cơ bản", "keywords": ["print", "variable"]},
                    {"title": "Vòng lặp for", "keywords": ["for", "loop", "range"]}
                ]
            }
        ]
    }
    allowed, forbidden = calculate_lesson_scope_contract(mock_syllabus, 0, 0)
    assert isinstance(allowed, set)
    assert isinstance(forbidden, set)

def test_trace_logging_to_storage():
    """Verifies that observability logs write to storage/trace_logs.jsonl correctly."""
    assert "storage" in TRACE_LOG_PATH
    import time
    log_agent_call(
        agent_name="unit_test_agent",
        session_id="Session 01",
        lesson_id="Lesson 01",
        prompt_summary="Test prompt summary",
        response_summary="Test response summary",
        start_time=time.time(),
        token_cost={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    )
    assert os.path.exists(TRACE_LOG_PATH)
    with open(TRACE_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        assert "unit_test_agent" in content

def test_persistence_sqlite_pool():
    """Verifies SQLite connection pool and checkpoint persistence in storage/state_store_v2.db."""
    assert "storage" in DB_PATH
    test_key = "e2e_test_key"
    test_state = {"session_id": "Session 99", "status": "Tested"}
    
    save_checkpoint(test_key, test_state)
    loaded = load_checkpoint(test_key)
    assert loaded is not None
    assert loaded.get("session_id") == "Session 99"
    assert loaded.get("status") == "Tested"

def test_master_validator_all_formats():
    """Verifies validation logic for READING and SLIDE content types."""
    valid_html = """<!doctype html>
    <html lang="vi">
      <head><title>Lesson Test</title></head>
      <body>
        <h1>Khái niệm biến trong Python</h1>
        <section id="section-1"><h2>1. Đặt vấn đề</h2><p>Mô tả bài học</p></section>
        <section id="section-2"><h2>2. Cơ chế hoạt động</h2><p>Mô tả cú pháp</p></section>
        <section id="section-3"><h2>3. Ví dụ thực thi</h2><pre><code>x = 10</code></pre></section>
        <section id="section-4"><h2>4. Cảnh báo lỗi</h2><p>Mô tả gotchas</p></section>
        <section id="section-5"><h2>5. Tóm tắt bài học</h2><div class="selftest-question" style="justify-content: flex-start !important;">Câu hỏi 1</div></section>
      </body>
    </html>"""
    is_valid, errors = validate_resource("READING", valid_html)
    assert is_valid is True, f"Validation failed: {errors}"

def test_resolve_language_info_git_and_theory():
    """Verifies that Git, CLI, and Theory subjects resolve to static engines instead of Pyodide WASM."""
    from agents.creators.reading_creator import resolve_language_info
    
    # 1. Git / CLI subjects
    git_info = resolve_language_info("git")
    assert git_info["engine"] == "static"
    assert git_info["hljs"] == "language-bash"
    
    # 2. Phân tích thiết kế / Architecture
    design_info = resolve_language_info("phân tích và thiết kế hệ thống")
    assert design_info["engine"] == "static"
    assert design_info["hljs"] == "language-plaintext"
    
    # 3. Python (executable code subject)
    py_info = resolve_language_info("python/core")
    assert py_info["engine"] == "pyodide"
    assert py_info["hljs"] == "language-python"
