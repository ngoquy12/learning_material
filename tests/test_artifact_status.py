"""
tests/test_artifact_status.py — Khoá bộ từ vựng trạng thái artifact.

Ba nhóm bảo đảm, tương ứng ba vấn đề mà core/artifact_status.py sinh ra để sửa:

  1. Tách được LÝ DO khỏi TRẠNG THÁI ("Skipped (Exam Session)" vẫn là "bị bỏ qua").
  2. Phân biệt được ba mức "Approved", trong đó bản vi phạm phạm vi kiến thức phải
     bị xếp vào nhóm CẦN NGƯỜI RÀ LẠI chứ không lẫn vào nhóm đã duyệt sạch.
  3. Tương thích ngược tuyệt đối với chuỗi thô: checkpoint đã ghi trên đĩa từ trước
     phải đọc lại và phân loại đúng, nếu không là mất toàn bộ tiến độ đã chạy.
"""

import json

import pytest

from core.artifact_status import (
    ArtifactStatus,
    base_status,
    is_approved,
    is_failed,
    is_skipped,
    is_terminal,
    needs_human_review,
    normalize,
    reason_of,
    skipped,
)


class TestBackwardCompatibility:
    """Enum phải thay thế được chuỗi cũ ở mọi vị trí, không cần migrate dữ liệu."""

    @pytest.mark.parametrize(
        "member,literal",
        [
            (ArtifactStatus.APPROVED, "Approved"),
            (ArtifactStatus.PENDING, "Pending"),
            (ArtifactStatus.SKIPPED, "Skipped"),
            (ArtifactStatus.PUBLISHED, "PUBLISHED"),
            (ArtifactStatus.PENDING_HUMAN_REVIEW, "Pending Human Review"),
            (ArtifactStatus.APPROVED_WITH_WARNINGS, "Approved with Warnings"),
            (ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS, "Approved with Scope Warnings"),
        ],
    )
    def test_so_sanh_bang_voi_chuoi_cu(self, member, literal):
        assert member == literal

    def test_json_ghi_ra_dung_chuoi_cu(self):
        """
        Checkpoint được tuần tự hoá bằng json. Nếu enum ghi ra 'ArtifactStatus.APPROVED'
        thì mọi file checkpoint mới sẽ không đọc được bằng code cũ.
        """
        payload = {"html": ArtifactStatus.APPROVED, "quiz": skipped("Exam Session")}
        assert json.loads(json.dumps(payload)) == {
            "html": "Approved",
            "quiz": "Skipped (Exam Session)",
        }

    def test_f_string_va_str_giu_nguyen_dien_mao(self):
        """Enum có mixin str mặc định in ra 'ArtifactStatus.APPROVED' — phải chặn."""
        assert str(ArtifactStatus.APPROVED) == "Approved"
        assert f"{ArtifactStatus.PUBLISHED}" == "PUBLISHED"
        assert f"{ArtifactStatus.PENDING!s}" == "Pending"

    def test_doc_lai_duoc_chuoi_tho_tu_checkpoint_cu(self):
        for legacy in ("Approved", "Pending", "Skipped", "PUBLISHED", "FAILED"):
            assert normalize(legacy) is not None, legacy


class TestReasonSeparation:
    """Lý do là dữ liệu tự do, KHÔNG được hàn vào giá trị trạng thái."""

    @pytest.mark.parametrize(
        "reason",
        ["Session 01 Orientation", "Exam Session", "Project/Practice", "Moved to Session Level"],
    )
    def test_moi_bien_the_skipped_van_la_bi_bo_qua(self, reason):
        value = skipped(reason)
        assert is_skipped(value), f"{value} phải được nhận là bị bỏ qua"
        assert base_status(value) == "Skipped"
        assert reason_of(value) == reason

    def test_skipped_khong_ly_do_tra_ve_chuoi_tran(self):
        assert skipped() == "Skipped"
        assert skipped("   ") == "Skipped"
        assert reason_of("Skipped") == ""

    def test_bien_the_cu_viet_tay_van_nhan_dien_duoc(self):
        """Chuỗi do code cũ ghi ra phải phân loại đúng mà không cần sửa dữ liệu."""
        assert is_skipped("Skipped (Temporarily Commented Out)")
        assert not is_approved("Skipped (Exam Session)")


class TestApprovalTiers:
    def test_ba_muc_approved_deu_tinh_la_da_duyet(self):
        for value in (
            ArtifactStatus.APPROVED,
            ArtifactStatus.APPROVED_WITH_WARNINGS,
            ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS,
        ):
            assert is_approved(value)

    def test_vi_pham_pham_vi_van_phai_bao_can_nguoi_ra_lai(self):
        """
        Đây là bảo đảm sư phạm quan trọng nhất của module: vi phạm phạm vi kiến thức
        là lỗi NỘI DUNG, không phải cảnh báo trình bày. Nó được xuất bản để không
        chặn cả khoá học, nhưng tuyệt đối không được lẫn vào nhóm đã duyệt sạch.
        """
        assert needs_human_review(ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS)
        assert needs_human_review(ArtifactStatus.PENDING_HUMAN_REVIEW)
        assert not needs_human_review(ArtifactStatus.APPROVED)
        assert not needs_human_review(ArtifactStatus.APPROVED_WITH_WARNINGS)

    def test_scope_gate_dung_chung_dinh_nghia(self):
        """core/scope_gate.py không được giữ bản sao riêng của hằng số này."""
        from core.scope_gate import STATUS_SCOPE_WARNING

        assert STATUS_SCOPE_WARNING is ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS


class TestTerminalAndFailure:
    def test_pending_va_failed_khong_phai_terminal(self):
        assert not is_terminal(ArtifactStatus.PENDING)
        assert not is_terminal(ArtifactStatus.PENDING_HUMAN_REVIEW)
        assert not is_terminal(ArtifactStatus.FAILED)

    def test_duyet_bo_qua_xuat_ban_la_terminal(self):
        assert is_terminal(ArtifactStatus.APPROVED)
        assert is_terminal(skipped("Exam Session"))
        assert is_terminal(ArtifactStatus.PUBLISHED)

    def test_failed_phan_biet_voi_skipped(self):
        """Hỏng do exception khác hẳn bỏ qua có chủ đích — gộp chung là giấu lỗi."""
        assert is_failed(ArtifactStatus.FAILED)
        assert not is_failed(skipped("Exam Session"))
        assert not is_skipped(ArtifactStatus.FAILED)


class TestNormalizeRefusesToGuess:
    @pytest.mark.parametrize("value", ["", None, "Xong rồi", "approved-ish", 42])
    def test_gia_tri_la_tra_ve_none_thay_vi_doan_bua(self, value):
        """Đoán sai một trạng thái nghĩa là xuất bản nhầm học liệu chưa đạt chuẩn."""
        assert normalize(value) is None

    def test_khong_phan_biet_hoa_thuong(self):
        assert normalize("APPROVED") is ArtifactStatus.APPROVED
        assert normalize("published") is ArtifactStatus.PUBLISHED


class TestCheckpointRoundTrip:
    def test_trang_thai_song_sot_qua_luu_va_nap_checkpoint(self, tmp_path, monkeypatch):
        """
        Vòng đời thật: ghi state có enum -> lưu checkpoint -> nạp lại -> phân loại.
        Nếu vòng này đứt, pipeline sẽ sinh lại toàn bộ artifact đã duyệt.
        """
        monkeypatch.setenv("STORAGE_DIR", str(tmp_path / "storage"))
        from core import paths

        paths.reset_path_cache()
        import importlib

        from core import persistence

        importlib.reload(persistence)
        try:
            state = {
                "session_id": "Session 99",
                "artifacts_status": {
                    "html": ArtifactStatus.APPROVED,
                    "quiz": skipped("Exam Session"),
                    "lab": ArtifactStatus.APPROVED_WITH_SCOPE_WARNINGS,
                },
            }
            persistence.save_checkpoint("test_roundtrip_status", state)
            loaded = persistence.load_checkpoint("test_roundtrip_status")

            assert loaded is not None
            status = loaded["artifacts_status"]
            assert is_approved(status["html"])
            assert is_skipped(status["quiz"])
            assert reason_of(status["quiz"]) == "Exam Session"
            assert needs_human_review(status["lab"])
        finally:
            paths.reset_path_cache()
            importlib.reload(persistence)
