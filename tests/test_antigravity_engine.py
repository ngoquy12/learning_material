"""
tests/test_antigravity_engine.py — Unit tests for Antigravity DAG Workflow Engine & State Reducers.
"""

from antigravity import override, append_unique, merge_dict, Workflow, component, parallel

def test_override_reducer():
    assert override("old", "new") == "new"
    assert override("old", "") == "old"
    assert override("old", None) == "old"
    assert override("old", {}) == "old"

def test_append_unique_reducer():
    old_list = ["a", "b"]
    new_list = ["b", "c", "d"]
    merged = append_unique(old_list, new_list)
    assert merged == ["a", "b", "c", "d"]
    assert append_unique(None, ["x"]) == ["x"]

def test_merge_dict_reducer():
    old_dict = {"a": 1, "b": 2}
    new_dict = {"b": 3, "c": 4}
    merged = merge_dict(old_dict, new_dict)
    assert merged == {"a": 1, "b": 3, "c": 4}
    assert merge_dict(None, {"x": 10}) == {"x": 10}

def test_workflow_execution():
    @component
    def step1(state):
        state["html_content"] = "Step 1 Content"
        return state

    @component
    def step2(state):
        state["slide_markdown"] = "Step 2 Slide"
        return state

    wf = Workflow()
    wf.add_node("step1", step1)
    wf.add_node("step2", step2)
    wf.add_edge("step1", "step2")
    wf.set_entry_point("step1")

    compiled_wf = wf.compile()
    state = {
        "html_content": "",
        "slide_markdown": "",
        "artifacts_status": {},
        "review_logs": []
    }
    result = compiled_wf.run(state)
    assert result["html_content"] == "Step 1 Content"
    assert result["slide_markdown"] == "Step 2 Slide"
