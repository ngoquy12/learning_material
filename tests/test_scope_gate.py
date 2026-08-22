"""
tests/test_scope_gate.py — Cổng kiểm định phạm vi kiến thức & bối cảnh nghiệp vụ.

Trước đây phần kiểm định này chỉ là lệnh print rải trong từng creator: phát hiện được
vi phạm nhưng không làm gì, cảnh báo trôi qua console rồi học liệu lỗi vẫn xuất bản.
Test dưới đây khoá lại hành vi mới: vi phạm phải hiện ra trong state để pipeline sinh
lại và để người dùng nhìn thấy trong báo cáo.
"""

from core.scope_gate import (
    STATUS_SCOPE_WARNING,
    ScopeAuditResult,
    audit_artifact_scope,
    extract_forbidden_scope,
    record_scope_audit,
)


def _state(**overrides):
    state = {
        "session_id": "Session 03",
        "lesson_id": "Lesson 02",
        "technology_stack": "python/core",
        "forbidden_scope": ["decorator", "metaclass"],
        "chosen_domain": "Hotel Booking",
    }
    state.update(overrides)
    return state


class TestForbiddenScopeExtraction:
    def test_normalises_to_lowercase(self):
        assert extract_forbidden_scope({"forbidden_scope": ["Decorator", " MetaClass "]}) == {
            "decorator",
            "metaclass",
        }

    def test_missing_or_malformed_scope_yields_empty_set(self):
        assert extract_forbidden_scope({}) == set()
        assert extract_forbidden_scope({"forbidden_scope": "decorator"}) == set()


class TestScopeViolationDetection:
    def test_flags_concept_not_yet_taught(self):
        text = "Bài này dùng decorator để bọc hàm trong Hotel Booking."

        result = audit_artifact_scope(text, _state(), "html")

        assert not result.is_clean
        assert "decorator" in result.violations

    def test_clean_content_passes(self):
        text = "Bài này dùng vòng lặp for đơn giản trong Hotel Booking."

        result = audit_artifact_scope(text, _state(), "html")

        assert result.is_clean
        assert result.violations == []

    def test_prohibition_sentence_is_not_a_violation(self):
        """
        'Không dùng decorator ở bài này' là câu DẶN DÒ, không phải vi phạm.

        Nếu bắt nhầm ca này, mọi bài đọc có phần lưu ý phạm vi đều bị sinh lại vô ích.
        """
        text = "Lưu ý: chưa dùng decorator ở bài này. Ta làm Hotel Booking bằng hàm thường."

        result = audit_artifact_scope(text, _state(), "html")

        assert result.violations == []

    def test_empty_text_is_clean(self):
        assert audit_artifact_scope("", _state(), "html").is_clean


class TestDomainDrift:
    def test_flags_content_that_left_the_session_domain(self):
        text = "Ta xây hệ thống quản lý kho hàng bằng vòng lặp for."

        result = audit_artifact_scope(text, _state(), "practical_lab")

        assert result.domain_drift is True
        assert result.expected_domain == "Hotel Booking"

    def test_domain_check_can_be_disabled(self):
        text = "Ta xây hệ thống quản lý kho hàng."

        result = audit_artifact_scope(text, _state(), "video_script", check_domain=False)

        assert result.domain_drift is False

    def test_no_drift_when_no_domain_configured(self):
        text = "Nội dung bất kỳ."

        result = audit_artifact_scope(text, _state(chosen_domain=""), "html")

        assert result.domain_drift is False


class TestFeedbackForRegeneration:
    def test_feedback_names_the_forbidden_concepts(self):
        result = ScopeAuditResult(artifact="html", violations=["decorator"])

        feedback = result.as_feedback()

        assert "decorator" in feedback
        assert feedback.strip()

    def test_feedback_names_the_expected_domain(self):
        result = ScopeAuditResult(
            artifact="practical_lab", domain_drift=True, expected_domain="Hotel Booking"
        )

        assert "Hotel Booking" in result.as_feedback()

    def test_clean_result_needs_no_feedback(self):
        assert ScopeAuditResult(artifact="html").as_feedback() == ""


class TestRecording:
    def test_violation_is_recorded_into_state_not_just_printed(self):
        """
        Vi phạm phải nằm trong state để hiện ra báo cáo cuối.

        Cảnh báo chỉ in ra console thì không ai đọc — đúng lý do các vi phạm trước đây
        trôi lọt tới sản phẩm giao cho học viên.
        """
        state = _state()
        result = audit_artifact_scope("Dùng decorator ở Hotel Booking.", state, "html")

        record_scope_audit(state, result)

        assert state["scope_audits"]["html"]["violations"] == ["decorator"]
        assert any(log["source"] == "Scope_Gate" for log in state["review_logs"])

    def test_clean_result_records_nothing(self):
        state = _state()

        record_scope_audit(state, ScopeAuditResult(artifact="html"))

        assert "scope_audits" not in state
        assert "review_logs" not in state

    def test_status_constant_is_distinguishable_from_approved(self):
        """Artifact còn vi phạm không được mang cùng nhãn với artifact sạch."""
        assert STATUS_SCOPE_WARNING != "Approved"
        assert "Approved" in STATUS_SCOPE_WARNING
