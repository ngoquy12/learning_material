"""
tests/test_session_kind.py — Loại buổi học xác định theo TÊN, không theo số thứ tự (B2).

Lỗi được sửa: `_is_session_01_orientation` nhận diện buổi định hướng bằng chuỗi
"SESSION 01" nằm trong mã buổi, tức coi MỌI môn học đều có buổi định hướng ở buổi
đầu tiên.

Hậu quả hai chiều, cả hai đều im lặng:

  - Môn nào vào thẳng kiến thức ngay buổi 1 (phần lớn các môn) bị mất sạch quiz,
    bài thực hành và câu hỏi đọc hiểu của buổi đó. Không có lỗi nào được báo —
    người biên soạn chỉ phát hiện khi mở thư mục và thấy thiếu file.
  - Môn nào đặt buổi định hướng ở vị trí khác buổi 1 thì không bao giờ được nhận
    ra, và hệ thống sinh quiz cho một buổi chưa dạy kiến thức nào.

Cùng heuristic đó còn tồn tại BẢN SAO thứ hai trong core/validators/reading_validator.py.
"""

import pytest

from core import graph
from core.artifact_status import is_skipped, reason_of
from core.session_types import (
    SessionType,
    allowed_parts_for,
    detect_session_type,
    is_part_allowed,
)


def _session(title: str, session_id: str = "Session 01", session_type: str = "Lý thuyết") -> dict:
    return {
        "session_id": session_id,
        "session_code": session_id,
        "title": title,
        "session_type": session_type,
    }


class TestNotBasedOnSessionNumber:
    """Nhóm test cốt lõi của B2."""

    def test_buoi_1_co_kien_thuc_that_khong_bi_coi_la_dinh_huong(self):
        """
        HỒI QUY CHÍNH. Đây là ca mà bản cũ làm sai, và làm sai trong im lặng: mất
        toàn bộ quiz, bài thực hành, câu hỏi đọc hiểu của buổi học đầu tiên.
        """
        kind = detect_session_type(_session("Biến, kiểu dữ liệu và toán tử cơ bản"))

        assert kind is SessionType.THEORY
        assert allowed_parts_for(kind) is None, "Buổi kiến thức phải sinh đầy đủ tài nguyên"
        for part in ("quiz", "practical_lab", "reading_questions", "video_script", "html"):
            assert is_part_allowed(kind, part)

    def test_buoi_dinh_huong_o_vi_tri_khac_van_duoc_nhan_ra(self):
        """Không phải môn nào cũng đặt buổi định hướng ở buổi 1."""
        kind = detect_session_type(
            _session("Giới thiệu môn học Cơ sở dữ liệu", session_id="Session 03")
        )
        assert kind is SessionType.ORIENTATION

    @pytest.mark.parametrize("session_id", ["Session 01", "Session 05", "Session 12"])
    def test_so_thu_tu_buoi_khong_anh_huong_ket_qua(self, session_id):
        """Cùng một tên buổi phải cho cùng kết quả bất kể nằm ở buổi số mấy."""
        content = detect_session_type(_session("Vòng lặp for và while", session_id))
        orientation = detect_session_type(_session("Định hướng môn học", session_id))

        assert content is SessionType.THEORY
        assert orientation is SessionType.ORIENTATION


class TestOrientationDetection:
    @pytest.mark.parametrize(
        "title",
        [
            "Định hướng môn học và Lộ trình phát triển phần mềm với Python",
            "Tổng quan lộ trình khoá học",
            "Giới thiệu môn học Lập trình Java",
            "Khai giảng và hướng dẫn sử dụng LMS",
            "Course Introduction and Roadmap",
            "Orientation session",
        ],
    )
    def test_nhan_ra_buoi_dinh_huong(self, title):
        assert detect_session_type(_session(title)) is SessionType.ORIENTATION

    def test_khai_bao_tuong_minh_trong_pm_duoc_uu_tien(self):
        """PM khai báo thẳng loại buổi thì không cần đoán theo từ khoá."""
        session = _session("Một tiêu đề bất kỳ", session_type="ORIENTATION")
        assert detect_session_type(session) is SessionType.ORIENTATION


class TestPrecisionOverRecall:
    """
    Bộ từ khoá cố ý thiên về ĐỘ CHÍNH XÁC, vì hai loại sai có hậu quả rất khác nhau:
    nhận nhầm buổi kiến thức thành buổi định hướng thì âm thầm xoá sổ tài nguyên;
    còn bỏ sót buổi định hướng thật thì cùng lắm sinh thừa, nhìn ra ngay.
    """

    @pytest.mark.parametrize(
        "title",
        [
            "Nhập môn Trí tuệ nhân tạo",
            "Nhập môn Lập trình Python",
            "Nhập môn Cơ sở dữ liệu",
        ],
    )
    def test_nhap_mon_la_ten_mon_hoc_khong_phai_buoi_dinh_huong(self, title):
        """Trong học thuật Việt Nam, "Nhập môn X" thường là TÊN MÔN HỌC."""
        assert detect_session_type(_session(title)) is not SessionType.ORIENTATION

    @pytest.mark.parametrize(
        "title,expected",
        [
            ("Thực hành truy vấn SQL nâng cao", SessionType.PRACTICE),
            ("Mini Project: Hệ thống quản lý kho", SessionType.MINI_PROJECT),
            ("Đồ án cuối môn", SessionType.FINAL_PROJECT),
        ],
    )
    def test_khong_bat_nham_cac_loai_buoi_khac(self, title, expected):
        assert detect_session_type(_session(title)) is expected


class TestConfigurableKeywords:
    def test_mo_rong_tu_khoa_qua_moi_truong(self, monkeypatch):
        """
        Hệ thống phục vụ nhiều môn học; môn đặc thù phải mở rộng được từ vựng mà
        không phải sửa mã nguồn.
        """
        title = "Buổi làm quen lớp học"
        assert detect_session_type(_session(title)) is not SessionType.ORIENTATION

        monkeypatch.setenv("ORIENTATION_SESSION_KEYWORDS", "làm quen lớp học")
        assert detect_session_type(_session(title)) is SessionType.ORIENTATION

    def test_loai_buoi_la_thi_sinh_day_du(self):
        """Không nhận ra thì sinh đầy đủ, còn hơn âm thầm bỏ bớt tài nguyên."""
        assert allowed_parts_for("MOT_LOAI_BUOI_LA") is None
        assert is_part_allowed("MOT_LOAI_BUOI_LA", "quiz")


class TestGraphIntegration:
    def test_da_go_heuristic_theo_so_buoi(self):
        assert not hasattr(graph, "_is_session_01_orientation")

    def test_buoi_dinh_huong_bo_qua_quiz_kem_ly_do(self):
        state = {"session_kind": "ORIENTATION", "artifacts_status": {}}

        assert graph.skip_part_for_session_kind(state, "quiz") is True
        status = state["artifacts_status"]["quiz"]
        assert is_skipped(status)
        assert "ORIENTATION" in reason_of(status), (
            "Lý do bỏ qua phải nói rõ loại buổi, không phải một chuỗi cứng về Session 01"
        )

    def test_buoi_ly_thuyet_khong_bi_bo_qua_gi(self):
        state = {"session_kind": "THEORY", "artifacts_status": {}}
        for part in ("quiz", "practical_lab", "reading_questions", "video_script"):
            assert graph.skip_part_for_session_kind(state, part) is False
        assert state["artifacts_status"] == {}

    def test_uu_tien_khai_bao_san_trong_state(self):
        """CLI đã phân loại thì pipeline không được đoán lại."""
        state = {
            "session_kind": "THEORY",
            "core_ssot": {"session_title": "Định hướng môn học"},
        }
        assert graph.resolve_session_kind(state) is SessionType.THEORY

    def test_suy_ra_tu_ten_buoi_khi_thieu_khai_bao(self):
        """State cũ (checkpoint trước khi có session_kind) vẫn phải hoạt động."""
        state = {"core_ssot": {"session_title": "Định hướng môn học và Lộ trình"}}
        assert graph.resolve_session_kind(state) is SessionType.ORIENTATION

    def test_khai_bao_rac_thi_quay_ve_suy_luan(self):
        state = {
            "session_kind": "KHONG_PHAI_LOAI_HOP_LE",
            "core_ssot": {"session_title": "Vòng lặp for"},
        }
        assert graph.resolve_session_kind(state) is SessionType.THEORY


class TestNoDuplicateHeuristic:
    def test_reading_validator_dung_chung_bo_phan_loai(self):
        """
        Bản sao thứ hai của heuristic từng nằm trong reading_validator. Hai bản sao
        trôi khỏi nhau nghĩa là cùng một bài học được coi là định hướng ở nơi này
        nhưng không phải ở nơi kia.
        """
        from pathlib import Path

        source = Path("core/validators/reading_validator.py").read_text(encoding="utf-8")
        assert "SESSION 01" not in source, "Vẫn còn heuristic theo số thứ tự buổi"
        assert "detect_session_type" in source

    def test_cli_khai_bao_session_kind(self):
        from pathlib import Path

        source = Path("cli/commands/workflow_cmd.py").read_text(encoding="utf-8")
        assert "detect_session_type(session)" in source
        assert '"session_kind": session_kind' in source


class TestParserFamily:
    """`is_orientation_session` phải nhất quán với họ hàm phân loại sẵn có."""

    def test_buoi_dinh_huong_khong_bi_tinh_la_buoi_thuc_hanh(self):
        from cli.curriculum_parser import is_orientation_session, is_practice_session

        session = _session("Định hướng môn học và thực hành cài đặt môi trường")
        assert is_orientation_session(session) is True
        assert is_practice_session(session) is False

    def test_buoi_thi_khong_bi_tinh_la_dinh_huong(self):
        from cli.curriculum_parser import is_orientation_session

        session = _session("Thi cuối kỳ", session_type="Thi cuối kỳ")
        assert is_orientation_session(session) is False
