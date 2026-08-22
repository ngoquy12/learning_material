"""
tests/test_agent_state_schema.py — Kiểm định runtime cho AgentState.

AgentState là TypedDict(total=False): chú thích kiểu chỉ có tác dụng ở type-checker,
không có gì kiểm tra lúc chạy thật. validate_state() lấp khoảng trống đó ở ranh giới
node. Test quan trọng nhất trong file này KHÔNG PHẢI test bắt lỗi — mà là test xác
nhận validator không chặn nhầm state hợp lệ: một validator quá gắt sẽ làm gián đoạn
pipeline sản xuất thật, tệ hơn cả việc không có validator.
"""

import pytest

from core.dag_engine import CompiledWorkflow, Workflow, component
from core.schemas.agent_state_schema import StateValidationError, validate_state


def _realistic_state(**overrides):
    """State với đúng hình dạng dữ liệu thật mà pipeline sản xuất ra."""
    state = {
        "session_id": "Session 03",
        "lesson_id": "Lesson 02",
        "technology_stack": "javascript/web",
        "core_ssot": {"session_title": "DOM Interaction"},
        "artifacts_status": {"html": "Approved"},
        "review_logs": [{"source": "UX_Reviewer", "feedback": "OK"}],
        "requested_parts": ["html", "quiz"],
        "force_rebuild": False,
        "pm_approved": True,
        # Các key ad-hoc chưa lên AgentState chính thức — không được bị chặn.
        "allowed_scope": ["biến", "toán tử"],
        "forbidden_scope": ["vòng lặp"],
        "chosen_domain": "Hotel Booking",
        "lesson_blueprint": {"key_concepts": ["a", "b"]},
    }
    state.update(overrides)
    return state


class TestValidStatesPassThrough:
    def test_realistic_pipeline_state_is_valid(self):
        validate_state(_realistic_state(), caller="test")  # không raise

    def test_empty_state_is_valid(self):
        validate_state({}, caller="test")

    def test_none_state_is_valid(self):
        """Một số node nhận state None/rỗng trước khi field đầu tiên được set."""
        validate_state(None, caller="test")

    def test_minimal_state_with_only_session_id(self):
        validate_state({"session_id": "Session 01"}, caller="test")

    def test_unknown_adhoc_keys_are_never_rejected(self):
        """
        State thật có nhiều key ad-hoc chưa lên AgentState chính thức (images_dir,
        lessons_learned_prompt, lesson_content, session_domain...). Validator này bắt
        SAI KIỂU trên field đã biết, không phải whitelist field được phép tồn tại.
        """
        validate_state(
            {"images_dir": "/tmp/x", "lessons_learned_prompt": "...", "brand_new_field_xyz": 123},
            caller="test",
        )


class TestTypeMismatchesAreCaught:
    def test_core_ssot_must_be_a_dict_not_a_string(self):
        with pytest.raises(StateValidationError, match="core_ssot"):
            validate_state({"core_ssot": "không phải dict"}, caller="test")

    def test_review_logs_must_be_a_list_not_a_dict(self):
        with pytest.raises(StateValidationError):
            validate_state({"review_logs": {"source": "X"}}, caller="test")

    def test_artifacts_status_must_be_a_dict_not_a_list(self):
        with pytest.raises(StateValidationError):
            validate_state({"artifacts_status": ["Approved"]}, caller="test")

    def test_error_message_names_the_caller(self):
        with pytest.raises(StateValidationError, match="node_generate_master_content"):
            validate_state({"core_ssot": 123}, caller="node_generate_master_content")


class TestWiredIntoWorkflowEntry:
    """CompiledWorkflow.run() phải kiểm định state đầu vào trước khi chạy node đầu tiên."""

    def _trivial_workflow(self):
        wf = Workflow()

        @component
        def noop(state):
            state["ran"] = True
            return state

        wf.add_node("noop", noop)
        wf.set_entry_point("noop")
        return wf.compile()

    def test_valid_initial_state_runs_normally(self):
        result = self._trivial_workflow().run(_realistic_state())
        assert result["ran"] is True

    def test_malformed_initial_state_fails_at_entry_not_deep_inside_a_node(self):
        with pytest.raises(StateValidationError):
            self._trivial_workflow().run({"core_ssot": "sai kiểu ngay từ đầu"})
