"""
tests/test_bloom.py — Nguồn Bloom's Taxonomy tập trung.

Hệ thống có ít nhất 2 bộ tên tầng độ khó không thống nhất (AGENTS.md §2.1 dùng
"BASIC APPLICATION"/"CREATIVE"..., homework_creator.py dùng "Mức độ 1: Cơ bản"...),
nên trước đây không cách nào audit tự động xem một session có phủ đủ các cấp độ
nhận thức mục tiêu hay không. Test này khoá hành vi của bộ ánh xạ, và — quan trọng
hơn — khoá luôn việc bộ tầng THẬT trong homework_creator.py phải phủ đủ 5 cấp Bloom
từ Understand đến Create, để nếu ai đó xoá hoặc đổi tên một tầng theo cách không còn
phân loại được, test sẽ đỏ ngay thay vì âm thầm mất một cấp nhận thức khỏi session.
"""

from core.pedagogy.bloom import (
    BLOOM_LEVELS,
    audit_bloom_coverage,
    classify_tier,
    get_level,
)


class TestCanonicalLevels:
    def test_exactly_six_levels_in_ascending_order(self):
        assert len(BLOOM_LEVELS) == 6
        assert [lvl.order for lvl in BLOOM_LEVELS] == [1, 2, 3, 4, 5, 6]

    def test_keys_are_unique(self):
        keys = [lvl.key for lvl in BLOOM_LEVELS]
        assert len(keys) == len(set(keys))

    def test_get_level_returns_canonical_object(self):
        assert get_level("create").name_vi == "Sáng tạo"

    def test_get_level_raises_on_unknown_key(self):
        import pytest
        with pytest.raises(KeyError):
            get_level("không tồn tại")


class TestClassifyByPdfLevel:
    """pdf_level là khoá ổn định — ưu tiên hơn khớp theo câu chữ hiển thị."""

    def test_co_ban_maps_to_understand(self):
        assert classify_tier("bất kỳ câu chữ nào", pdf_level="co_ban").key == "understand"

    def test_chuyen_sau_maps_to_apply(self):
        assert classify_tier("", pdf_level="chuyen_sau").key == "apply"

    def test_phan_tich_maps_to_analyze(self):
        assert classify_tier("", pdf_level="phan_tich").key == "analyze"

    def test_sang_tao_maps_to_create(self):
        assert classify_tier("", pdf_level="sang_tao").key == "create"

    def test_unknown_pdf_level_falls_back_to_label(self):
        result = classify_tier("Analysis exercise", pdf_level="không_tồn_tại")
        assert result.key == "analyze"


class TestClassifyByLegacyLabel:
    """Chuẩn 6-bài cũ trong AGENTS.md §2.1 dùng tên tiếng Anh, khớp theo từ khoá con."""

    def test_basic_application(self):
        assert classify_tier("I. BASIC APPLICATION (Exercise 1 & 2)").key == "understand"

    def test_advanced_application(self):
        assert classify_tier("II. ADVANCED APPLICATION (Exercise 3 & 4)").key == "apply"

    def test_analysis(self):
        assert classify_tier("III. ANALYSIS (Exercise 5)").key == "analyze"

    def test_creative(self):
        assert classify_tier("IV. CREATIVE (Exercise 6)").key == "create"

    def test_case_insensitive(self):
        assert classify_tier("creative design task").key == "create"


class TestUnrecognizedLabelsAreNotGuessed:
    def test_empty_label_returns_none(self):
        assert classify_tier("") is None
        assert classify_tier(None) is None

    def test_unrelated_label_returns_none(self):
        assert classify_tier("Xuất sắc") is None

    def test_difficulty_scale_is_not_forced_into_bloom(self):
        """
        'Dễ/Trung bình/Khá/Giỏi/Xuất sắc' (agents/practice_agents.py) là thang ĐỘ KHÓ,
        khác trục với quá trình NHẬN THỨC mà Bloom mô tả. Một bài 'Xuất sắc' có thể vẫn
        chỉ yêu cầu ghi nhớ ở mức khó hơn — ép nó thành 'Sáng tạo' là ngụy tạo sư phạm.
        """
        for label in ("Dễ", "Trung bình", "Khá", "Giỏi", "Xuất sắc"):
            assert classify_tier(label) is None, f"'{label}' không nên bị ép vào Bloom"


class TestCoverageAudit:
    def test_full_coverage_reports_clean(self):
        tiers = [{"label": "", "pdf_level": lvl} for lvl in
                 ("co_ban", "chuyen_sau", "phan_tich", "sang_tao")]
        report = audit_bloom_coverage(tiers, expected_levels=["understand", "apply", "analyze", "create"])

        assert report.is_full_coverage
        assert report.missing == []

    def test_missing_level_is_reported(self):
        tiers = [{"label": "", "pdf_level": "co_ban"}]
        report = audit_bloom_coverage(tiers, expected_levels=["understand", "create"])

        assert not report.is_full_coverage
        assert [lvl.key for lvl in report.missing] == ["create"]

    def test_unclassified_tier_does_not_count_as_covered(self):
        tiers = [{"label": "Xuất sắc", "pdf_level": None}]
        report = audit_bloom_coverage(tiers, expected_levels=["create"])

        assert not report.is_full_coverage
        assert "Xuất sắc" in report.unclassified

    def test_default_expected_levels_is_all_six(self):
        report = audit_bloom_coverage([])
        assert len(report.missing) == 6

    def test_summary_mentions_missing_level_names(self):
        tiers = [{"label": "", "pdf_level": "co_ban"}]
        report = audit_bloom_coverage(tiers, expected_levels=["understand", "create"])

        assert "Sáng tạo" in report.summary()


class TestRealHomeworkTiersCoverBloom:
    """
    Regression guard trên NGUỒN THẬT: nếu ai đó sửa SESSION_HOMEWORK_TIERS trong
    homework_creator.py theo cách làm mất một cấp Bloom (đổi pdf_level thành giá trị
    lạ, hoặc xoá hẳn một tầng), test này đỏ ngay — thay vì âm thầm phát hành một
    session thiếu hẳn một cấp độ nhận thức mà không ai để ý.
    """

    def test_session_homework_suite_covers_understand_through_create(self):
        from agents.creators.homework_creator import SESSION_HOMEWORK_TIERS

        tiers = [
            {"label": label, "pdf_level": pdf_level}
            for label, pdf_level in SESSION_HOMEWORK_TIERS
        ]
        report = audit_bloom_coverage(
            tiers, expected_levels=["understand", "apply", "analyze", "create"]
        )

        assert report.is_full_coverage, report.summary()
        assert report.unclassified == []

    def test_session_homework_suite_has_fifteen_tiers(self):
        from agents.creators.homework_creator import SESSION_HOMEWORK_TIERS
        assert len(SESSION_HOMEWORK_TIERS) == 15
