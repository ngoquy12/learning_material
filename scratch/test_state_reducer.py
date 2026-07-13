"""
Test suite for the State Reducer engine upgrade in antigravity.py.
Validates all 3 built-in reducers, the registry, extension API, and full parallel merge.
"""
import sys
sys.path.insert(0, ".")

from antigravity import (
    override, append_unique, merge_dict,
    get_reducer, register_reducer,
    CompiledWorkflow, Workflow, parallel, component
)


def test_override_reducer():
    """override: last-write-wins with empty/None protection."""
    assert override("old", "new") == "new"
    assert override("old", "") == "old"       # empty string → keep old
    assert override("old", None) == "old"     # None → keep old
    assert override("old", {}) == "old"       # empty dict → keep old
    assert override("", "new") == "new"
    assert override(None, "new") == "new"
    assert override(42, 99) == 99             # works for non-str too
    print("[PASS] test_override_reducer")


def test_append_unique_reducer():
    """append_unique: deduplication append for lists."""
    assert append_unique([1, 2], [2, 3]) == [1, 2, 3]
    assert append_unique([], [1]) == [1]
    assert append_unique(None, [1]) == [1]
    assert append_unique([1], None) == [1]

    # Dict deduplication
    logs = [{"source": "A", "msg": "1"}]
    new_logs = [{"source": "A", "msg": "1"}, {"source": "B", "msg": "2"}]
    merged = append_unique(logs, new_logs)
    assert len(merged) == 2
    print("[PASS] test_append_unique_reducer")


def test_merge_dict_reducer():
    """merge_dict: shallow dict merge."""
    assert merge_dict({"a": 1}, {"b": 2}) == {"a": 1, "b": 2}
    assert merge_dict({"a": 1}, {"a": 2}) == {"a": 2}
    assert merge_dict(None, {"a": 1}) == {"a": 1}
    assert merge_dict({"a": 1}, None) == {"a": 1}
    print("[PASS] test_merge_dict_reducer")


def test_registry_lookup():
    """get_reducer: returns correct reducer per field, falls back to override."""
    assert get_reducer("html_content") is override
    assert get_reducer("slide_markdown") is override
    assert get_reducer("quiz_json") is override
    assert get_reducer("video_script_markdown") is override
    assert get_reducer("mindmap_markdown") is override
    assert get_reducer("review_logs") is append_unique
    assert get_reducer("artifacts_status") is merge_dict
    assert get_reducer("core_ssot") is merge_dict
    assert get_reducer("time_reference") is merge_dict
    # Unknown fields fallback
    assert get_reducer("totally_unknown_field") is override
    print("[PASS] test_registry_lookup")


def test_register_custom_reducer():
    """register_reducer: downstream code can extend without touching engine."""
    def sum_reducer(old, new):
        return (old or 0) + (new or 0)

    register_reducer("token_count", sum_reducer)
    assert get_reducer("token_count") is sum_reducer
    assert sum_reducer(10, 5) == 15
    assert sum_reducer(None, 5) == 5
    print("[PASS] test_register_custom_reducer")


def test_parallel_merge_full_simulation():
    """Simulates 5-branch parallel execution and validates merge correctness."""

    # Build a minimal workflow to access the merge method
    class FakeWorkflow:
        nodes = {}
        edges = []
        entry_point = None

    cw = CompiledWorkflow(FakeWorkflow())

    base_state = {
        "session_id": "Session 01",
        "lesson_id": "Lesson 01",
        "html_content": "",
        "slide_markdown": "",
        "quiz_json": {},
        "video_script_markdown": "",
        "mindmap_markdown": "",
        "artifacts_status": {
            "html": "Pending",
            "slide": "Pending",
            "quiz": "Pending",
            "video_script": "Pending",
            "mindmap": "Pending",
        },
        "review_logs": [],
    }

    # Simulate 5 parallel branches — each only touches its own artifact
    branch_results = {
        "html_branch": {
            "html_content": "<h1>Hello World</h1>",
            "slide_markdown": "",         # didn't touch
            "quiz_json": {},              # didn't touch
            "video_script_markdown": "",  # didn't touch
            "mindmap_markdown": "",       # didn't touch
            "artifacts_status": {"html": "Approved"},
            "review_logs": [{"source": "UX_Reviewer", "feedback": "LGTM"}],
        },
        "slide_branch": {
            "html_content": "",
            "slide_markdown": "# Slide 1\n---\n# Slide 2",
            "quiz_json": {},
            "video_script_markdown": "",
            "mindmap_markdown": "",
            "artifacts_status": {"slide": "Approved"},
            "review_logs": [{"source": "Academic_Reviewer", "feedback": "OK"}],
        },
        "quiz_branch": {
            "html_content": "",
            "slide_markdown": "",
            "quiz_json": {"lesson_quiz": [{"q": "What is Python?"}]},
            "video_script_markdown": "",
            "mindmap_markdown": "",
            "artifacts_status": {"quiz": "Approved"},
            "review_logs": [],
        },
        "video_branch": {
            "html_content": "",
            "slide_markdown": "",
            "quiz_json": {},
            "video_script_markdown": "## Scene 1\nGiảng viên nói...",
            "mindmap_markdown": "",
            "artifacts_status": {"video_script": "Approved"},
            "review_logs": [],
        },
        "mindmap_branch": {
            "html_content": "",
            "slide_markdown": "",
            "quiz_json": {},
            "video_script_markdown": "",
            "mindmap_markdown": "# Python Core\n## Variables\n## Loops",
            "artifacts_status": {"mindmap": "Approved"},
            "review_logs": [],
        },
    }

    merged = cw._merge_parallel_branches(base_state, branch_results)

    # Validate content fields (override with empty-protection)
    assert merged["html_content"] == "<h1>Hello World</h1>"
    assert merged["slide_markdown"] == "# Slide 1\n---\n# Slide 2"
    assert merged["quiz_json"] == {"lesson_quiz": [{"q": "What is Python?"}]}
    assert merged["video_script_markdown"] == "## Scene 1\nGiảng viên nói..."
    assert merged["mindmap_markdown"] == "# Python Core\n## Variables\n## Loops"

    # Validate status (merge_dict should combine all sub-statuses)
    expected_status = {
        "html": "Approved",
        "slide": "Approved",
        "quiz": "Approved",
        "video_script": "Approved",
        "mindmap": "Approved",
    }
    assert merged["artifacts_status"] == expected_status

    # Validate logs (append_unique should deduplicate)
    assert len(merged["review_logs"]) == 2
    sources = [log["source"] for log in merged["review_logs"]]
    assert "UX_Reviewer" in sources
    assert "Academic_Reviewer" in sources

    # Validate identity fields preserved
    assert merged["session_id"] == "Session 01"
    assert merged["lesson_id"] == "Lesson 01"

    print("[PASS] test_parallel_merge_full_simulation")


def test_backward_compatibility_api():
    """Ensures Workflow, component, parallel decorators still work as before."""
    wf = Workflow()

    @component
    def node_a(state):
        state["counter"] = state.get("counter", 0) + 1
        return state

    @component
    def node_b(state):
        state["counter"] = state.get("counter", 0) + 10
        return state

    wf.add_node("a", node_a)
    wf.add_node("b", node_b)
    wf.set_entry_point("a")
    wf.add_edge("a", "b")

    compiled = wf.compile()
    result = compiled.run({"counter": 0})
    assert result["counter"] == 11

    # Verify decorators set flags
    assert getattr(node_a, "__is_component__", False) is True
    assert getattr(node_b, "__is_component__", False) is True

    @parallel
    def par_node(state):
        return {}

    assert getattr(par_node, "__is_parallel__", False) is True

    print("[PASS] test_backward_compatibility_api")


if __name__ == "__main__":
    test_override_reducer()
    test_append_unique_reducer()
    test_merge_dict_reducer()
    test_registry_lookup()
    test_register_custom_reducer()
    test_parallel_merge_full_simulation()
    test_backward_compatibility_api()

    print()
    print("=" * 60)
    print("  ALL 7 TESTS PASSED - State Reducer Engine Verified")
    print("=" * 60)
