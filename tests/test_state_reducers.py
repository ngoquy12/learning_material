"""
tests/test_state_reducers.py — Bảo vệ tính toàn vẹn của STATE_REDUCERS registry.

Bối cảnh: các nhánh sản xuất chạy song song rồi gộp state lại qua merge_branch_states(),
và hàm này tra reducer theo TÊN FIELD. Field nào không đăng ký sẽ rơi vào reducer mặc
định 'override' — im lặng, không cảnh báo.

Điều đó từng gây ra lỗi thật: một field được thêm vào AgentState nhưng quên đăng ký,
và không ai phát hiện cho tới khi artifact bị mất trong sản phẩm cuối. Test dưới đây
biến "quên đăng ký reducer" từ lỗi thầm lặng thành test đỏ ngay lập tức.
"""

from core.dag_engine import (
    STATE_REDUCERS,
    append_unique,
    get_reducer,
    merge_dict,
    override,
)
from core.state import AgentState


def _agent_state_fields():
    """Mọi field khai báo trong AgentState, kể cả NotRequired."""
    return set(AgentState.__annotations__.keys())


class TestRegistryCoverage:
    def test_every_agent_state_field_has_explicit_reducer(self):
        """
        MỌI field của AgentState phải đăng ký reducer tường minh.

        Nếu test này đỏ vì bạn vừa thêm field mới vào AgentState: hãy vào
        core/dag_engine.py và khai báo chiến lược merge cho nó —
            - override      : nội dung ghi đè, lần ghi sau thắng (artifact, config)
            - merge_dict    : gộp nông 2 dict (bản đồ trạng thái)
            - append_unique : nối list và khử trùng lặp (log tích luỹ)
        Đừng dựa vào fallback ngầm: chọn sai chiến lược merge sẽ làm mất dữ liệu
        theo cách rất khó truy.
        """
        missing = _agent_state_fields() - set(STATE_REDUCERS)
        assert not missing, (
            "Các field sau có trong AgentState nhưng chưa đăng ký reducer trong "
            f"STATE_REDUCERS: {sorted(missing)}"
        )

    def test_registry_has_no_reducer_for_unknown_field(self):
        """
        Registry không được chứa field đã bị xoá khỏi AgentState.

        Reducer mồ côi là dấu hiệu registry và schema đã trôi khỏi nhau — hoặc field
        bị xoá mà quên dọn, hoặc field được dùng ad-hoc mà chưa khai báo vào AgentState.
        """
        known_adhoc_keys = {
            # Các key dùng thực tế trong pipeline nhưng chưa nâng lên AgentState.
            # Thêm vào đây có chủ đích, không phải để làm test xanh cho tiện.
            "allowed_scope",
            "forbidden_scope",
            "lesson_type",
            "lesson_blueprint",
            "lesson_content",
            "reading_material",
            "lessons_learned_prompt",
            "images_dir",
        }
        orphans = set(STATE_REDUCERS) - _agent_state_fields() - known_adhoc_keys
        assert not orphans, (
            f"Reducer mồ côi (không còn field tương ứng trong AgentState): {sorted(orphans)}"
        )

    def test_all_reducers_are_callable(self):
        for field_name, reducer in STATE_REDUCERS.items():
            assert callable(reducer), f"Reducer của '{field_name}' không gọi được"


class TestReducerStrategyCorrectness:
    """Field tích luỹ phải dùng đúng reducer tích luỹ, không được là override."""

    def test_accumulating_fields_use_accumulating_reducers(self):
        assert STATE_REDUCERS["review_logs"] is append_unique
        assert STATE_REDUCERS["artifacts_status"] is merge_dict
        assert STATE_REDUCERS["core_ssot"] is merge_dict

    def test_artifact_fields_use_override(self):
        for field_name in (
            "html_content",
            "quiz_json",
            "practical_lab_markdown",
            "practical_lab_html",
            "reading_questions_markdown",
            "video_script_markdown",
        ):
            assert STATE_REDUCERS[field_name] is override, (
                f"'{field_name}' là artifact nội dung, phải dùng override"
            )

    def test_unregistered_field_falls_back_to_override(self):
        assert get_reducer("field_khong_ton_tai_abc") is override


class TestReducerBehaviour:
    def test_override_keeps_old_value_when_new_is_empty(self):
        """Nhánh trả rỗng không được xoá mất kết quả nhánh khác đã sinh."""
        assert override("<html>cũ</html>", "") == "<html>cũ</html>"
        assert override({"a": 1}, {}) == {"a": 1}
        assert override("<html>cũ</html>", None) == "<html>cũ</html>"

    def test_override_takes_new_value_when_present(self):
        assert override("cũ", "mới") == "mới"
        assert override(None, "mới") == "mới"

    def test_append_unique_deduplicates(self):
        log = {"source": "Reviewer", "feedback": "OK"}
        assert append_unique([log], [log]) == [log]
        assert len(append_unique([log], [{"source": "Khác"}])) == 2

    def test_merge_dict_combines_both_sides(self):
        assert merge_dict({"html": "Approved"}, {"quiz": "Approved"}) == {
            "html": "Approved",
            "quiz": "Approved",
        }
