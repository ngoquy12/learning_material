"""
tests/test_async_and_diff_cache.py
Unit tests for SemanticCache integration and async parallel workflow helpers.
"""

import pytest
import asyncio
import time
from core.semantic_cache import cache_store, cache_lookup, cache_invalidate_old, get_cache_stats
from core.dag_engine import merge_branch_states

def test_semantic_cache_store_and_lookup():
    sys_p = "System instruction for testing cache."
    user_p = "Explain list vs tuple in Python."
    resp = "List is mutable whereas tuple is immutable in Python."
    
    # Store entry
    cache_store(sys_p, user_p, resp, agent_name="TestAgent")
    
    # Exact lookup
    hit = cache_lookup(sys_p, user_p, agent_name="TestAgent", fuzzy=False)
    assert hit is not None
    assert "List is mutable" in hit


def test_semantic_cache_fuzzy_match():
    sys_p = "System prompt about Python data structures."
    user_p_1 = "Detailed explanation of list vs tuple in Python language."
    user_p_2 = "Detailed explanation of list vs tuple in Python programming."
    resp = "List is mutable, tuple is immutable."
    
    cache_store(sys_p, user_p_1, resp, agent_name="TestFuzzyAgent")
    
    # Fuzzy lookup
    hit = cache_lookup(sys_p, user_p_2, agent_name="TestFuzzyAgent", fuzzy=True)
    assert hit is not None
    assert "mutable" in hit


def test_semantic_cache_stats():
    stats = get_cache_stats()
    assert "total_cached_responses" in stats
    assert "total_cache_hits" in stats


def test_asyncio_gather_pipeline_execution():
    async def dummy_pipeline(name: str, delay: float):
        await asyncio.sleep(delay)
        return name, {"artifacts_status": {name: "Approved"}}

    async def main_test():
        start = time.time()
        tasks = [
            dummy_pipeline("Slide", 0.05),
            dummy_pipeline("Quiz", 0.05),
            dummy_pipeline("Lab", 0.05),
        ]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start
        
        # Parallel execution of 3 x 0.05s tasks should take ~0.05s, not 0.15s
        assert elapsed < 0.12
        assert len(results) == 3
        return results

    res = asyncio.run(main_test())
    assert len(res) == 3


def test_merge_branch_states_basic():
    main_state = {"artifacts_status": {}}
    sub_state = {
        "slide_markdown": "# Slide 1",
        "quiz_json": [{"q": 1}],
        "artifacts_status": {"slide": "Approved", "quiz": "Approved"},
        "review_logs": [{"source": "QuizReviewer", "feedback": "OK"}]
    }

    merged = merge_branch_states(main_state, {"TestBranch": sub_state})

    assert merged.get("slide_markdown") == "# Slide 1"
    assert len(merged.get("quiz_json")) == 1
    assert merged["artifacts_status"]["slide"] == "Approved"
    assert len(merged.get("review_logs")) == 1


def test_merge_branch_states_preserves_every_lesson_artifact():
    """
    Mọi artifact cấp lesson sinh ra ở nhánh song song đều phải sống sót qua merge.

    Regression guard: practical_lab_html từng bị BỎ SÓT trong _merge_sub_state (bản copy
    tay từng tên field, nay đã xoá) dù đã có trong AgentState và STATE_REDUCERS. Hậu quả
    là nhánh PracticalLab gọi LLM sinh HTML xong thì bị vứt bỏ lúc merge, rồi
    write_state_artifacts_to_disk phải render lại từ lab_json — tốn token cho một
    artifact không bao giờ được dùng.
    """
    main_state = {"artifacts_status": {}}
    sub_state = {
        "html_content": "<html>reading</html>",
        "quiz_json": [{"q": 1}],
        "lab_json": {"title": "Lab 1"},
        "practical_lab_markdown": "# Lab",
        "practical_lab_html": "<html>lab</html>",
        "reading_questions_markdown": "# Câu hỏi",
        "reading_questions_json": {"questions": []},
        "video_script_markdown": "# Kịch bản",
        "slide_markdown": "# Slide",
    }

    merged = merge_branch_states(main_state, {"PracticalLab": sub_state})

    for field, expected in sub_state.items():
        assert merged.get(field) == expected, f"Artifact '{field}' bị mất khi merge"


def test_merge_branch_states_combines_multiple_branches():
    """Nhiều nhánh gộp cùng lúc: mỗi nhánh giữ artifact riêng, status/log tích luỹ."""
    base = {"artifacts_status": {}, "review_logs": []}
    branches = {
        "HTML": {
            "html_content": "<html>reading</html>",
            "artifacts_status": {"html": "Approved"},
            "review_logs": [{"source": "HtmlReviewer"}],
        },
        "PracticalLab": {
            "practical_lab_html": "<html>lab</html>",
            "artifacts_status": {"practical_lab": "Approved"},
            "review_logs": [{"source": "LabReviewer"}],
        },
    }

    merged = merge_branch_states(base, branches)

    assert merged["html_content"] == "<html>reading</html>"
    assert merged["practical_lab_html"] == "<html>lab</html>"
    assert merged["artifacts_status"] == {"html": "Approved", "practical_lab": "Approved"}
    assert len(merged["review_logs"]) == 2


def test_merge_branch_states_does_not_mutate_base():
    """Merge phải trả về dict mới, không sửa base tại chỗ."""
    base = {"artifacts_status": {}}
    merged = merge_branch_states(base, {"HTML": {"html_content": "<html/>"}})

    assert "html_content" not in base
    assert merged["html_content"] == "<html/>"


def test_merge_branch_states_skips_invalid_branch():
    """Nhánh lỗi (không phải dict) bị bỏ qua thay vì làm hỏng cả lần merge."""
    base = {"html_content": "<html>cũ</html>"}
    merged = merge_branch_states(base, {"Broken": None, "Quiz": {"quiz_json": [{"q": 1}]}})

    assert merged["html_content"] == "<html>cũ</html>"
    assert merged["quiz_json"] == [{"q": 1}]
