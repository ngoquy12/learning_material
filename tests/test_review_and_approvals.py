"""
tests/test_review_and_approvals.py — Trang rà soát (E1) và hồ sơ duyệt (E2).

Pipeline gắn nhãn rất cẩn thận — APPROVED, APPROVED_WITH_SCOPE_WARNINGS,
PENDING_HUMAN_REVIEW, FAILED, SKIPPED kèm lý do — nhưng toàn bộ nhãn đó chỉ tồn tại
trong console và trong checkpoint nhị phân. Sau một lượt chạy 20 buổi học, không ai
dựng lại được câu hỏi đơn giản nhất: "bài nào cần tôi rà lại trước khi phát cho
sinh viên?".

Và ngay cả khi đã rà xong, không có chỗ nào ghi lại. Hai hệ quả: chạy lại pipeline
ghi đè thẳng lên bản giảng viên đã sửa tay, và không xuất được hồ sơ "ai duyệt cái
gì, khi nào" — thứ mà kiểm định chất lượng đào tạo bắt buộc phải có.
"""

import pytest

from core import paths
from core.artifact_status import ArtifactStatus, skipped
from core.review_dashboard import (
    build_dashboard_data,
    categorize,
    render_dashboard_html,
    write_dashboard,
)


@pytest.fixture
def store(tmp_path, monkeypatch):
    """Kho tri thức sạch trong thư mục tạm."""
    monkeypatch.setenv("STORAGE_DIR", str(tmp_path / "storage"))
    paths.reset_path_cache()
    yield tmp_path
    paths.reset_path_cache()


def _state(**overrides):
    base = {
        "session_id": "Session 02",
        "lesson_id": "Lesson 01",
        "core_ssot": {"session_title": "Biến và phép gán"},
        "artifacts_status": {
            "html": ArtifactStatus.APPROVED,
            "quiz": ArtifactStatus.PENDING_HUMAN_REVIEW,
            "practical_lab": ArtifactStatus.FAILED,
            "reading_questions": skipped("ORIENTATION session"),
            "video_script": ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS,
        },
        "review_logs": [
            {"source": "UX_Reviewer", "artifact": "quiz", "feedback": "Thiếu phương án nhiễu hợp lý."},
        ],
        "scope_audits": {"video_script": {"violations": ["dictionary"], "domain_drift": False}},
    }
    base.update(overrides)
    return base


class TestCategorization:
    @pytest.mark.parametrize(
        "status,expected",
        [
            (ArtifactStatus.FAILED, "failed"),
            (ArtifactStatus.PENDING_HUMAN_REVIEW, "needs_review"),
            (ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS, "needs_review"),
            (ArtifactStatus.APPROVED, "approved"),
            (ArtifactStatus.APPROVED_WITH_WARNINGS, "approved"),
            (ArtifactStatus.PUBLISHED, "approved"),
            (ArtifactStatus.PENDING, "pending"),
            (ArtifactStatus.SKIPPED, "skipped"),
        ],
    )
    def test_xep_nhom_dung(self, status, expected):
        assert categorize(status) == expected

    def test_vi_pham_pham_vi_xep_vao_nhom_can_ra_lai(self):
        """
        Đây là điểm dễ sai nhất: "Approved with Scope Warnings" bắt đầu bằng
        "Approved" nhưng là lỗi NỘI DUNG. Gộp nó vào nhóm đã duyệt là giấu mất
        artifact nghiêm trọng nhất khỏi mắt người rà soát.
        """
        assert categorize(ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS) == "needs_review"

    def test_moi_bien_the_skipped_deu_vao_nhom_khong_ap_dung(self):
        assert categorize(skipped("ORIENTATION session")) == "skipped"
        assert categorize(skipped("Exam Session")) == "skipped"


class TestDashboardData:
    def test_gom_du_moi_artifact(self, store):
        data = build_dashboard_data("Lap_trinh_Python", [_state()])
        assert len(data.rows) == 5

    def test_muc_can_can_thiep_xep_len_dau(self, store):
        """Người rà soát mở trang này để tìm việc phải làm, không phải để ngắm thứ đã xong."""
        data = build_dashboard_data("Lap_trinh_Python", [_state()])
        categories = [r.category for r in data.rows]

        assert categories[0] == "failed"
        assert categories.index("failed") < categories.index("needs_review")
        assert categories.index("needs_review") < categories.index("approved")
        assert categories.index("approved") < categories.index("skipped")

    def test_dem_dung_so_can_xu_ly(self, store):
        data = build_dashboard_data("Lap_trinh_Python", [_state()])
        # 1 failed + 2 needs_review (quiz, video_script) + 0 pending
        assert data.needs_attention == 3

    def test_kem_phan_hoi_kiem_dinh_cho_muc_can_xu_ly(self, store):
        data = build_dashboard_data("Lap_trinh_Python", [_state()])
        quiz = next(r for r in data.rows if r.artifact == "quiz")
        assert "phương án nhiễu" in quiz.feedback

    def test_neu_ro_khai_niem_vi_pham_pham_vi(self, store):
        """Nói "cần rà lại" mà không nói vì sao thì người rà phải tự đi tìm."""
        data = build_dashboard_data("Lap_trinh_Python", [_state()])
        vs = next(r for r in data.rows if r.artifact == "video_script")
        assert "dictionary" in vs.feedback

    def test_giu_lai_ly_do_bo_qua(self, store):
        data = build_dashboard_data("Lap_trinh_Python", [_state()])
        rq = next(r for r in data.rows if r.artifact == "reading_questions")
        assert rq.reason == "ORIENTATION session"

    def test_state_hong_khong_lam_chet_trang(self, store):
        data = build_dashboard_data("X", [None, "khong phai dict", {}, _state()])
        assert len(data.rows) == 5


class TestDashboardHtml:
    def test_ket_xuat_html_hop_le_va_tu_chua(self, store, tmp_path):
        data = build_dashboard_data("Lap_trinh_Python", [_state()])
        html_out = render_dashboard_html(data)

        assert html_out.startswith("<!DOCTYPE html>")
        assert "Lap_trinh_Python" in html_out
        assert "http://" not in html_out and "https://" not in html_out, (
            "Trang rà soát phải tự chứa, không phụ thuộc mạng"
        )

    def test_thoat_ky_tu_dac_biet(self, store):
        state = _state(core_ssot={"session_title": '<script>alert("x")</script>'})
        html_out = render_dashboard_html(build_dashboard_data("C", [state]))
        assert "<script>alert" not in html_out
        assert "&lt;script&gt;" in html_out

    def test_ghi_ra_dia(self, store, tmp_path):
        target = tmp_path / "out" / "review_dashboard.html"
        written = write_dashboard("C", [_state()], target)
        assert written == target
        assert target.exists() and target.stat().st_size > 500

    def test_khong_dung_template_hoc_lieu(self):
        """
        Trang này là công cụ quản trị nội bộ. Nó không được đụng tới bộ template bài
        đọc/bài thực hành — vùng thiết kế đã đóng băng.
        """
        from pathlib import Path

        source = Path("core/review_dashboard.py").read_text(encoding="utf-8")
        assert "reading_master" not in source
        assert "templates/html" not in source


class TestApprovals:
    def test_ghi_va_tra_cuu_duoc(self, store):
        from core.approvals import get_latest_approval, record_approval

        record_approval(
            artifact="html", reviewer="Nguyen Van A", course="C",
            session_id="Session 02", lesson_id="Lesson 01", note="Đã sửa tay phần 3",
        )
        latest = get_latest_approval("html", "C", "Session 02", "Lesson 01")

        assert latest is not None
        assert latest.reviewer == "Nguyen Van A"
        assert latest.is_approved
        assert latest.note == "Đã sửa tay phần 3"

    def test_tu_choi_quyet_dinh_vo_danh(self, store):
        """Hồ sơ kiểm định không chấp nhận "ai đó đã duyệt"."""
        from core.approvals import record_approval

        with pytest.raises(ValueError, match="người duyệt"):
            record_approval(artifact="html", reviewer="")

    def test_ghi_them_chu_khong_ghi_de_lich_su(self, store):
        """
        Hồ sơ kiểm định cần thấy được cả lịch sử: bị từ chối, sửa, rồi duyệt lại.
        """
        from core.approvals import DECISION_REJECTED, get_latest_approval, list_approvals, record_approval

        record_approval(artifact="html", reviewer="A", course="C", session_id="S1",
                        decision=DECISION_REJECTED, note="Sai phạm vi")
        record_approval(artifact="html", reviewer="B", course="C", session_id="S1")

        assert len(list_approvals("C")) == 2
        assert get_latest_approval("html", "C", "S1").reviewer == "B"

    def test_khoa_ghi_de_sau_khi_duyet(self, store):
        """Chạy lại pipeline không được xoá công rà soát của giảng viên."""
        from core.approvals import is_locked_by_reviewer, record_approval

        assert is_locked_by_reviewer("html", "C", "S1", "L1") is False
        record_approval(artifact="html", reviewer="A", course="C", session_id="S1", lesson_id="L1")
        assert is_locked_by_reviewer("html", "C", "S1", "L1") is True

    def test_force_rebuild_la_loi_thoat_co_chu_dich(self, store):
        """Không có lối thoát thì một artifact duyệt nhầm sẽ khoá vĩnh viễn."""
        from core.approvals import is_locked_by_reviewer, record_approval

        record_approval(artifact="html", reviewer="A", course="C", session_id="S1")
        assert is_locked_by_reviewer("html", "C", "S1", force_rebuild=True) is False

    def test_ban_bi_tu_choi_khong_khoa_ghi_de(self, store):
        from core.approvals import DECISION_REJECTED, is_locked_by_reviewer, record_approval

        record_approval(artifact="html", reviewer="A", course="C", session_id="S1",
                        decision=DECISION_REJECTED)
        assert is_locked_by_reviewer("html", "C", "S1") is False

    def test_xuat_ho_so_kiem_dinh_csv(self, store, tmp_path):
        from core.approvals import export_approvals_csv, record_approval

        record_approval(artifact="html", reviewer="Nguyen Van A", course="C",
                        session_id="Session 02", lesson_id="Lesson 01")
        target = tmp_path / "ho_so.csv"
        count = export_approvals_csv(str(target), course="C")

        assert count == 1
        content = target.read_text(encoding="utf-8-sig")
        assert "Người duyệt" in content and "Nguyen Van A" in content
        assert "Session 02" in content


class TestDashboardShowsApprovals:
    def test_hien_ten_nguoi_da_duyet(self, store):
        from core.approvals import record_approval

        record_approval(artifact="html", reviewer="Tran Thi B", course="Lap_trinh_Python",
                        session_id="Session 02", lesson_id="Lesson 01")

        data = build_dashboard_data("Lap_trinh_Python", [_state()])
        row = next(r for r in data.rows if r.artifact == "html")
        assert row.approved_by == "Tran Thi B"
        assert row.approved_at


class TestCliWiring:
    def test_co_cac_co_dong_lenh(self):
        from cli.args import parse_cli_arguments
        import sys

        argv = sys.argv
        try:
            sys.argv = ["main.py", "--approve", "S1/L1/html", "--reviewer", "A"]
            args = parse_cli_arguments()
            assert args.approve == "S1/L1/html"
            assert args.reviewer == "A"
        finally:
            sys.argv = argv

    def test_workflow_goi_dashboard_va_ho_so_duyet(self):
        from pathlib import Path

        source = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8")
        assert "handle_approval_command(args)" in source
        assert "write_review_dashboard(" in source

    def test_gom_state_ngay_tai_diem_gan(self):
        """
        final_states.append phải nằm ngay sau mỗi phép gán final_state. Đặt ở nhánh
        khác là NameError khi chạy thật — mà test suite lại không phủ CLI end-to-end.
        """
        from pathlib import Path

        lines = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8").split("\n")
        for i, line in enumerate(lines):
            if "final_states.append(final_state)" in line:
                assert "final_state = " in lines[i - 1], (
                    f"Dòng {i + 1}: gom state không nằm ngay sau phép gán final_state"
                )
