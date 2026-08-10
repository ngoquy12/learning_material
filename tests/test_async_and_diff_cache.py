"""
tests/test_async_and_diff_cache.py
Unit tests for SemanticCache integration and async parallel workflow helpers.
"""

import pytest
import asyncio
import time
from core.semantic_cache import cache_store, cache_lookup, cache_invalidate_old, get_cache_stats
from core.graph import _merge_sub_state

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


def test_merge_sub_state_helper():
    main_state = {"artifacts_status": {}}
    sub_state = {
        "slide_markdown": "# Slide 1",
        "quiz_json": [{"q": 1}],
        "artifacts_status": {"slide": "Approved", "quiz": "Approved"},
        "review_logs": [{"source": "QuizReviewer", "feedback": "OK"}]
    }
    
    _merge_sub_state(main_state, "TestBranch", sub_state)
    
    assert main_state.get("slide_markdown") == "# Slide 1"
    assert len(main_state.get("quiz_json")) == 1
    assert main_state["artifacts_status"]["slide"] == "Approved"
    assert len(main_state.get("review_logs")) == 1
