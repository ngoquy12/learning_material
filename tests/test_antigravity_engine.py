"""
tests/test_antigravity_engine.py
Unit tests for antigravity.py asynchronous DAG workflow engine & state reducers.
"""

import pytest
from antigravity import override, append_unique, merge_dict, get_reducer

def test_override_reducer():
    assert override("old_value", "new_value") == "new_value"
    assert override("old_value", None) == "old_value"
    assert override("old_value", "") == "old_value"
    assert override("old_value", {}) == "old_value"
    assert override({"a": 1}, {"b": 2}) == {"b": 2}

def test_append_unique_reducer():
    assert append_unique(["log1", "log2"], ["log2", "log3"]) == ["log1", "log2", "log3"]
    assert append_unique(None, ["log1"]) == ["log1"]
    assert append_unique(["log1"], None) == ["log1"]

def test_merge_dict_reducer():
    old_dict = {"status_a": "Done", "status_b": "Pending"}
    new_dict = {"status_b": "Approved", "status_c": "Draft"}
    merged = merge_dict(old_dict, new_dict)
    assert merged == {"status_a": "Done", "status_b": "Approved", "status_c": "Draft"}
    assert merge_dict(None, {"key": "val"}) == {"key": "val"}

def test_get_reducer_lookup():
    assert get_reducer("html_content") == override
    assert get_reducer("review_logs") == append_unique
    assert get_reducer("artifacts_status") == merge_dict
    assert get_reducer("unregistered_field") == override
