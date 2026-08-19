"""
tests/test_pm_pipeline.py
Verifies the PM Generator and Reviewer Agent Pipeline:
- System prompt Jinja2 template rendering.
- Deterministic PM review quality gates.
- Title sanitization and Session 01 single lesson normalization.
- Scope calculation & boundary checking.
"""

import unittest
from agents.pm_generator_agent import (
    get_pm_system_prompt,
    _sanitize_professional_titles,
    _normalize_session_01_lessons,
    _validate_prerequisite_chain
)
from agents.pm_reviewer_agent import pm_reviewer_agent

class TestPMPipeline(unittest.TestCase):

    def test_pm_system_prompt_rendering(self):
        """Tests that PM system prompt renders cleanly with session budgets."""
        prompt = get_pm_system_prompt(
            course_id="PYTHON_CORE",
            tech_stack="Python 3.12",
            session_budget={"total_sessions": 24, "theory_sessions": 12, "practice_sessions": 9, "mini_projects": 2, "final_exam": 1}
        )
        self.assertIn("PYTHON_CORE", prompt)
        self.assertIn("Python 3.12", prompt)
        self.assertIn("24", prompt)

    def test_title_sanitization(self):
        """Tests that amateur fluff phrases in lesson titles are stripped."""
        sample_pm = [
            {
                "session_num": 2,
                "title": "Session 02 - Vấn đề tính toán dữ liệu và cú pháp cơ bản",
                "lessons": [
                    {"lesson_num": 1, "title": "Tìm hiểu về biến và kiểu dữ liệu"},
                    {"lesson_num": 2, "title": "Cách sử dụng toán tử số học"}
                ]
            }
        ]
        cleaned = _sanitize_professional_titles(sample_pm)
        self.assertEqual(cleaned[0]["title"], "Session 02 - Cú pháp cơ bản")
        self.assertEqual(cleaned[0]["lessons"][0]["title"], "Biến và kiểu dữ liệu")
        self.assertEqual(cleaned[0]["lessons"][1]["title"], "Toán tử số học")

    def test_session_01_single_lesson_normalization(self):
        """Tests that Session 01 is strictly normalized to 1 consolidated orientation lesson."""
        sample_pm = [
            {
                "session_num": 1,
                "title": "Session 01 - Định hướng khóa học",
                "lessons": [
                    {"lesson_num": 1, "title": "Lesson A"},
                    {"lesson_num": 2, "title": "Lesson B"}
                ]
            }
        ]
        normalized = _normalize_session_01_lessons(sample_pm)
        self.assertEqual(len(normalized[0]["lessons"]), 1)
        self.assertEqual(normalized[0]["lessons"][0]["title"], "Tổng quan lộ trình và Demo sản phẩm")

    def test_pm_reviewer_quality_gate(self):
        """Tests PM Reviewer agent quality audit on a valid session curriculum structure."""
        valid_pm = [
            {
                "session_num": 1,
                "hinh_thuc": "Lý thuyết",
                "title": "Session 01 - Định hướng khóa học",
                "lessons": [
                    {
                        "lesson_num": 1,
                        "title": "Tổng quan lộ trình và Demo sản phẩm",
                        "content_scope": "1. Lộ trình môn học | 2. Công cụ AI | 3. Demo sản phẩm",
                        "expected_outcome": "Trình bày được toàn bộ cấu trúc lộ trình môn học.",
                        "forbidden_scope": "CẤM: Gõ code, chạy terminal",
                        "allowed_scope": "ĐÃ HỌC: Bài mở đầu"
                    }
                ]
            },
            {
                "session_num": 2,
                "hinh_thuc": "Lý thuyết",
                "title": "Session 02 - Tổng quan và Cú pháp cơ bản",
                "lessons": [
                    {
                        "lesson_num": 1,
                        "title": "Tổng quan về ngôn ngữ Python",
                        "content_scope": "1. Lịch sử Python | 2. Triết lý Zen of Python | 3. Ứng dụng thực tế",
                        "expected_outcome": "Trình bày được đặc điểm và vị thế của Python trong công nghiệp.",
                        "forbidden_scope": "CẤM: Cú pháp phức tạp, OOP, hàm",
                        "allowed_scope": "ĐÃ HỌC: Bài mở đầu"
                    },
                    {
                        "lesson_num": 2,
                        "title": "Cài đặt môi trường và công cụ lập trình",
                        "content_scope": "1. Cài đặt Python 3.12 | 2. Cấu hình VS Code | 3. Tạo venv",
                        "expected_outcome": "Cài đặt thành công môi trường lập trình chuẩn.",
                        "forbidden_scope": "CẤM: OOP, Function",
                        "allowed_scope": "ĐÃ HỌC: Tổng quan Python"
                    },
                    {
                        "lesson_num": 3,
                        "title": "Khai báo biến và kiểu dữ liệu cơ sở",
                        "content_scope": "1. Cú pháp biến | 2. Kiểu int, float, str, bool | 3. Ép kiểu",
                        "expected_outcome": "Khai báo chính xác và sử dụng các kiểu dữ liệu cơ sở.",
                        "forbidden_scope": "CẤM: Vòng lặp, hàm, OOP",
                        "allowed_scope": "ĐÃ HỌC: Môi trường lập trình"
                    }
                ]
            },
            {
                "session_num": 3,
                "hinh_thuc": "Thi cuối môn",
                "title": "Session 03 - Đánh giá và Thi cuối môn",
                "lessons": []
            }
        ]
        config_dict = {
            "tech_stack": "Python",
            "class_configuration": {},
            "student_profile": {},
            "session_budget": {"total_sessions": 3, "theory_sessions": 2, "practice_sessions": 0, "final_exam": 1}
        }
        course_info = {"course_id": "PY01", "course_name": "Python Basic", "clos": [], "plos": []}
        review = pm_reviewer_agent(valid_pm, config_dict, course_info)
        self.assertGreaterEqual(review["score"], 80)

if __name__ == "__main__":
    unittest.main()
