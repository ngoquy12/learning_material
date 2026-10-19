import unittest

from core.course_nature import (
    get_non_code_spec_language,
    is_design_subject,
    is_non_code_subject,
    should_render_visualizer,
)


class TestCourseNature(unittest.TestCase):
    def test_mon_khong_viet_ma(self):
        self.assertTrue(is_non_code_subject("Agile Scrum"))
        self.assertTrue(is_non_code_subject("", "Phân tích thiết kế hệ thống"))
        self.assertTrue(is_non_code_subject("UML"))
        self.assertTrue(is_non_code_subject("", "", "Viết User Story theo INVEST và Acceptance Criteria"))

    def test_mon_thiet_ke(self):
        self.assertTrue(is_design_subject("Figma"))
        self.assertTrue(is_non_code_subject("UI/UX Design"))

    def test_bai_lap_trinh_khong_bi_xep_nham(self):
        # "word" trong "keyword", "prototype" của JavaScript, "process" trong tên bài
        self.assertFalse(is_non_code_subject("python/core", "", "Tham số keyword argument"))
        self.assertFalse(is_non_code_subject("javascript", "JavaScript nâng cao", "Prototype và kế thừa"))
        self.assertFalse(is_non_code_subject("python", "", "Xử lý process và thread"))
        self.assertFalse(is_non_code_subject("python", "Lập trình Python", "Đọc mật khẩu password"))

    def test_tu_khoa_yeu_chi_xet_o_cap_mon(self):
        self.assertTrue(is_non_code_subject("Microsoft Excel", "Tin học văn phòng"))
        self.assertFalse(is_non_code_subject("python", "", "Xuất dữ liệu ra Excel"))

    def test_visualizer(self):
        self.assertFalse(should_render_visualizer("Agile Scrum"))
        self.assertTrue(should_render_visualizer("python/core"))

    def test_ngon_ngu_dac_ta(self):
        self.assertEqual(get_non_code_spec_language("UML"), "mermaid")
        self.assertEqual(get_non_code_spec_language("Gherkin BDD"), "gherkin")
        self.assertEqual(get_non_code_spec_language("Figma"), "markdown")


if __name__ == "__main__":
    unittest.main()
