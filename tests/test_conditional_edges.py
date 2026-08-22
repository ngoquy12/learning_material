"""
tests/test_conditional_edges.py — Rẽ nhánh thật trong dag_engine.

Trước đây CompiledWorkflow.run() chỉ đi tuyến tính: `next_nodes[0]` trên danh sách
edges, không có cách nào cấu trúc một rẽ nhánh THẬT ở tầng graph — mọi "rẽ nhánh" của
hệ thống (skip quiz cho Session 01, v.v.) đều phải giả bằng early-return bên trong
từng node. Tên gọi "DAG Engine" khi đó hơi phóng đại so với năng lực thực tế: đồ thị
chỉ có một đường đi duy nhất, không phải một DAG với các nhánh rẽ.

add_conditional_edge() lấp đúng khoảng trống đó: node kế tiếp được quyết định LÚC CHẠY
dựa trên state, và giờ luồng rẽ nhánh nhìn thấy được từ chính cấu trúc workflow thay vì
phải đọc code bên trong từng node mới biết.
"""

import pytest

from core.dag_engine import END, Workflow, component


def _make_node(name, mutate=None):
    @component
    def node(state):
        state.setdefault("visited", []).append(name)
        if mutate:
            mutate(state)
        return state
    return node


class TestConditionalBranching:
    def test_takes_the_branch_the_condition_selects(self):
        wf = Workflow()
        wf.add_node("start", _make_node("start"))
        wf.add_node("branch_a", _make_node("branch_a"))
        wf.add_node("branch_b", _make_node("branch_b"))
        wf.set_entry_point("start")
        wf.add_conditional_edge(
            "start",
            condition=lambda state: "a" if state.get("go_a") else "b",
            path_map={"a": "branch_a", "b": "branch_b"},
        )

        result = wf.compile().run({"go_a": True})
        assert result["visited"] == ["start", "branch_a"]

    def test_switching_the_condition_input_switches_the_branch(self):
        wf = Workflow()
        wf.add_node("start", _make_node("start"))
        wf.add_node("branch_a", _make_node("branch_a"))
        wf.add_node("branch_b", _make_node("branch_b"))
        wf.set_entry_point("start")
        wf.add_conditional_edge(
            "start",
            condition=lambda state: "a" if state.get("go_a") else "b",
            path_map={"a": "branch_a", "b": "branch_b"},
        )

        result = wf.compile().run({"go_a": False})
        assert result["visited"] == ["start", "branch_b"]

    def test_end_sentinel_stops_the_pipeline(self):
        """
        Trước khi có END, dừng sớm một nhánh phải trỏ tới một node "no-op" giả — chỉ
        để không còn việc gì làm. END khai báo thẳng ý định "dừng ở đây".
        """
        wf = Workflow()
        wf.add_node("start", _make_node("start"))
        wf.add_node("continue_here", _make_node("continue_here"))
        wf.set_entry_point("start")
        wf.add_conditional_edge(
            "start",
            condition=lambda state: "stop" if state.get("skip") else "go",
            path_map={"stop": END, "go": "continue_here"},
        )

        result = wf.compile().run({"skip": True})
        assert result["visited"] == ["start"]

    def test_conditional_edge_takes_priority_over_straight_edge(self):
        """Một node có cả 2 loại cạnh: cạnh có điều kiện thắng, cạnh thẳng bị bỏ qua."""
        wf = Workflow()
        wf.add_node("start", _make_node("start"))
        wf.add_node("straight_target", _make_node("straight_target"))
        wf.add_node("conditional_target", _make_node("conditional_target"))
        wf.set_entry_point("start")
        wf.add_edge("start", "straight_target")
        wf.add_conditional_edge(
            "start",
            condition=lambda state: "x",
            path_map={"x": "conditional_target"},
        )

        result = wf.compile().run({})
        assert result["visited"] == ["start", "conditional_target"]

    def test_unmapped_branch_key_raises_loudly(self):
        """
        condition() trả về khoá không nằm trong path_map là lỗi cấu hình — phải fail
        ngay và rõ ràng (kèm danh sách khoá hợp lệ), không được lặng lẽ dừng pipeline
        hay đi nhầm sang một node khác.
        """
        wf = Workflow()
        wf.add_node("start", _make_node("start"))
        wf.add_node("branch_a", _make_node("branch_a"))
        wf.set_entry_point("start")
        wf.add_conditional_edge(
            "start",
            condition=lambda state: "khong_ton_tai",
            path_map={"a": "branch_a"},
        )

        with pytest.raises(ValueError, match="khong_ton_tai"):
            wf.compile().run({})

    def test_multi_hop_branching_downstream_of_the_branch_point(self):
        """Sau khi rẽ nhánh, phần còn lại của đồ thị vẫn chạy tuyến tính bình thường."""
        wf = Workflow()
        wf.add_node("start", _make_node("start"))
        wf.add_node("branch_a", _make_node("branch_a"))
        wf.add_node("after_a", _make_node("after_a"))
        wf.set_entry_point("start")
        wf.add_conditional_edge("start", condition=lambda s: "a", path_map={"a": "branch_a"})
        wf.add_edge("branch_a", "after_a")

        result = wf.compile().run({})
        assert result["visited"] == ["start", "branch_a", "after_a"]


class TestBackwardCompatibility:
    """Workflow không dùng conditional edge phải chạy giống hệt như trước khi có tính năng này."""

    def test_pure_straight_line_workflow_unaffected(self):
        wf = Workflow()
        wf.add_node("a", _make_node("a"))
        wf.add_node("b", _make_node("b"))
        wf.add_node("c", _make_node("c"))
        wf.set_entry_point("a")
        wf.add_edge("a", "b")
        wf.add_edge("b", "c")

        result = wf.compile().run({})
        assert result["visited"] == ["a", "b", "c"]

    def test_node_with_no_outgoing_edge_ends_the_run(self):
        wf = Workflow()
        wf.add_node("a", _make_node("a"))
        wf.set_entry_point("a")

        result = wf.compile().run({})
        assert result["visited"] == ["a"]
