"""
tests/test_clo_bloom_alignment.py — Đối chiếu CLO với độ phủ nhận thức thực tế (C3).

Bộ kiểm CLO sẵn có chỉ kiểm ĐỘ PHỦ TỪ KHOÁ: thuật ngữ trong chuẩn đầu ra có xuất
hiện đâu đó trong chương trình không. Nó bỏ lọt loại lệch chuẩn nghiêm trọng hơn:

    CLO tuyên bố "Phân tích và đánh giá hiệu năng truy vấn", nhưng toàn bộ bài tập
    phủ CLO đó chỉ dừng ở mức Vận dụng (viết được câu truy vấn chạy đúng).

Từ khoá khớp hoàn hảo nên bộ kiểm cũ cho qua, nhưng chuẩn đầu ra đã hứa với người
học và hội đồng kiểm định một mức nhận thức mà chương trình không đưa họ tới.
"""

import pytest

from core.pedagogy.bloom import (
    audit_clo_alignment,
    classify_clo,
    covered_levels_from_tiers,
    find_ambiguous_verbs,
    find_non_measurable_verbs,
    get_level,
)
from core.pm_validators import validate_clo_bloom_alignment

# Bộ tầng của một môn nhập môn: chỉ đưa người học tới mức Vận dụng.
INTRO_TIERS = [
    {"label": "Mức độ 1: Cơ bản - Debug lỗi", "pdf_level": "co_ban"},
    {"label": "Mức độ 3: Nâng cao - Xây dựng tính năng mới", "pdf_level": "chuyen_sau"},
]


class TestCloVerbClassification:
    @pytest.mark.parametrize(
        "clo,expected_key",
        [
            ("Liệt kê được các kiểu dữ liệu nguyên thuỷ", "remember"),
            ("Trình bày được cơ chế hoạt động của vòng lặp", "understand"),
            ("Vận dụng được câu lệnh điều kiện vào bài toán tính phí", "apply"),
            ("Phân tích được độ phức tạp thuật toán sắp xếp", "analyze"),
            ("Đánh giá được ưu nhược điểm của từng giải pháp lưu trữ", "evaluate"),
            ("Thiết kế được lược đồ cơ sở dữ liệu cho hệ thống bán hàng", "create"),
        ],
    )
    def test_nhan_dien_cap_bloom_tu_dong_tu(self, clo, expected_key):
        assert classify_clo(clo) is get_level(expected_key)

    def test_nhieu_dong_tu_thi_lay_cap_cao_nhat(self):
        """
        Chuẩn đầu ra chỉ coi là đạt khi người học làm được phần khó nhất trong đó.
        """
        clo = "Phân tích yêu cầu và thiết kế được kiến trúc module"
        assert classify_clo(clo) is get_level("create")

    def test_khong_nhan_ra_dong_tu_thi_tra_none(self):
        """Đoán bừa một cấp còn tệ hơn để không phân loại được."""
        assert classify_clo("Sinh viên tiếp cận môn học") is None
        assert classify_clo("") is None


class TestAmbiguousVerbsAreNotGuessed:
    def test_so_sanh_khong_bi_gan_bua_mot_cap(self):
        """
        Anderson & Krathwohl xếp "comparing" vào cấp HIỂU, nhưng "so sánh giải pháp
        và trade-off" trong repo này được coi là PHÂN TÍCH. Cùng một động từ, hai cấp
        khác nhau tuỳ ngữ cảnh — nên không gán cấp nào cả.
        """
        assert classify_clo("So sánh các kiểu dữ liệu") is None
        assert "so sánh" in find_ambiguous_verbs("So sánh các kiểu dữ liệu")

    @pytest.mark.parametrize("verb", ["xây dựng", "giải quyết"])
    def test_cac_dong_tu_da_nghia_khac(self, verb):
        assert verb in find_ambiguous_verbs(f"{verb.capitalize()} được chương trình")


class TestNonMeasurableVerbs:
    """
    Kho kinh nghiệm của chính hệ thống (skills/lessons_learned/SKILL.md) đã ghi lại
    nhiều lần rằng chuẩn đầu ra dùng những từ này bị reviewer trả về. C3 biến bài
    học lặp đi lặp lại đó thành ràng buộc kiểm được bằng code.
    """

    @pytest.mark.parametrize(
        "clo", ["Hiểu được nguyên lý OOP", "Nắm vững cú pháp Python", "Ghi nhớ các toán tử"]
    )
    def test_phat_hien_dong_tu_khong_do_duoc(self, clo):
        assert find_non_measurable_verbs(clo)

    def test_dong_tu_do_duoc_khong_bi_bao_nham(self):
        assert find_non_measurable_verbs("Trình bày được nguyên lý OOP") == []


class TestUnderCoverage:
    """Nhóm test cốt lõi của C3."""

    def test_clo_vuot_qua_do_phu_cua_chuong_trinh_bi_bat(self):
        covered = covered_levels_from_tiers(INTRO_TIERS)
        issues = audit_clo_alignment(
            ["Thiết kế được kiến trúc hệ thống quản lý kho"], covered
        )

        assert len(issues) == 1
        assert issues[0].kind == "under_covered"
        assert issues[0].required_level.key == "create"
        assert issues[0].highest_covered.key == "apply"
        assert "Sáng tạo" in issues[0].message()
        assert "Vận dụng" in issues[0].message()

    def test_clo_nam_trong_do_phu_thi_khong_bao(self):
        covered = covered_levels_from_tiers(INTRO_TIERS)
        issues = audit_clo_alignment(
            ["Vận dụng được vòng lặp để duyệt danh sách"], covered
        )
        assert issues == []

    def test_clo_o_cap_thap_hon_van_duoc_chap_nhan(self):
        """Các cấp thấp là tiền đề của cấp cao, nên được coi là đã phủ."""
        covered = covered_levels_from_tiers(INTRO_TIERS)
        issues = audit_clo_alignment(["Liệt kê được các toán tử số học"], covered)
        assert issues == []

    def test_khong_co_bai_tap_nao_thi_moi_clo_deu_bi_bao(self):
        issues = audit_clo_alignment(["Vận dụng được vòng lặp"], [])
        assert len(issues) == 1
        assert issues[0].kind == "under_covered"


class TestValidatorIntegration:
    def test_diem_tru_phan_biet_theo_muc_nghiem_trong(self):
        """Lỗi thiết kế chương trình phải nặng hơn lỗi cách viết câu."""
        d_design, _, _ = validate_clo_bloom_alignment(
            clos=["Thiết kế được kiến trúc hệ thống"], tiers=INTRO_TIERS
        )
        d_wording, _, _ = validate_clo_bloom_alignment(
            clos=["Hiểu được nguyên lý OOP"], tiers=INTRO_TIERS
        )

        assert d_design > d_wording > 0

    def test_clo_khong_phan_loai_duoc_chi_canh_bao_khong_tru_diem(self):
        """
        Có thể do bộ động từ của hệ thống chưa phủ hết cách diễn đạt, không chắc là
        lỗi của người viết chương trình.
        """
        d, v, logs = validate_clo_bloom_alignment(
            clos=["So sánh các kiểu dữ liệu"], tiers=INTRO_TIERS
        )
        assert d == 0
        assert v, "Vẫn phải nêu ra để người viết biết"
        assert all(log["level"] != "ERROR" for log in logs if log["rule"] == "CLO_BLOOM_ALIGNMENT")

    def test_khong_co_clo_thi_khong_lam_gi(self):
        assert validate_clo_bloom_alignment(clos=[]) == (0, [], [])
        assert validate_clo_bloom_alignment(clos=None) == (0, [], [])

    def test_bao_cao_neu_ro_khoang_trong_o_giua(self):
        """
        Con số "4/6 cấp" không nói lên điều gì; khoảng trống Ở GIỮA mới cho biết
        người học nhảy cóc qua một quá trình nhận thức nào.
        """
        _, _, logs = validate_clo_bloom_alignment(clos=["Vận dụng được vòng lặp"])
        info = [log["message"] for log in logs if log["level"] == "INFO"]

        assert info, "Phải có dòng thông tin về độ phủ của hệ bài tập"
        assert "Đánh giá" in info[0], (
            "Hệ bài tập hiện tại có Phân tích và Sáng tạo nhưng KHÔNG có bài nào ở "
            "cấp Đánh giá — khoảng trống này phải hiện ra trong báo cáo"
        )


class TestUsesRealTierSource:
    def test_doc_tang_bai_tap_tu_nguon_that(self):
        """
        Chép tay một bản sao danh sách tầng thì khi homework_creator đổi, bộ kiểm
        này vẫn báo cáo theo bản cũ và không ai biết.
        """
        from pathlib import Path

        source = Path("core/pm_validators/clo_bloom_validator.py").read_text(encoding="utf-8")
        assert "SESSION_HOMEWORK_TIERS" in source

    def test_do_phu_mac_dinh_khop_voi_he_bai_tap_thuc_te(self):
        from agents.creators.homework_creator import SESSION_HOMEWORK_TIERS

        tiers = [{"label": lb, "pdf_level": pl} for lb, pl in SESSION_HOMEWORK_TIERS]
        covered = {lvl.key for lvl in covered_levels_from_tiers(tiers)}

        assert covered == {"understand", "apply", "analyze", "create"}, (
            f"Độ phủ thực tế đã đổi: {covered}. Cập nhật kỳ vọng ở đây và rà lại "
            f"xem chương trình có còn khớp chuẩn đầu ra không."
        )


class TestWiredIntoLinter:
    def test_syllabus_linter_goi_buoc_kiem_moi(self):
        from pathlib import Path

        source = Path("core/pm_validators/syllabus_linter.py").read_text(encoding="utf-8")
        assert "validate_clo_bloom_alignment" in source
