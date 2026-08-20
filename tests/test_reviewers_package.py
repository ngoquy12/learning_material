"""
tests/test_reviewers_package.py
Verifies the Modular Reviewers Package (agents.reviewers):
- Reading UX/UI reviewer module.
- Lecture UI reviewer module.
- Prerequisite guard reviewer module.
- Academic and Sandbox reviewer modules.
"""

import unittest
from agents.reviewers import (
    html_ux_reviewer,
    reading_ui_reviewer,
    HTMLReadingUIReviewerAgent,
    lecture_ui_reviewer_agent,
    ClassroomLectureUIReviewerAgent,
    prerequisite_guard_agent,
    run_prerequisite_check_for_pm,
    objective_reviewer_agent,
    pm_reviewer_agent,
    sandbox_testing_agent,
    check_forbidden_emojis,
    check_unaccented_vietnamese
)

class TestReviewersPackage(unittest.TestCase):

    def test_check_forbidden_emojis(self):
        """Tests that text emoji validator detects forbidden emojis."""
        clean_text = "Nội dung kỹ thuật chuẩn không chứa biểu tượng."
        dirty_text = "Bài học này có emoji 🚀🔥."
        self.assertEqual(check_forbidden_emojis(clean_text), "")
        self.assertIn("TUYỆT ĐỐI CẤM", check_forbidden_emojis(dirty_text))

    def test_check_unaccented_vietnamese(self):
        """Tests that unaccented Vietnamese is flagged."""
        dirty = "ky su phan mem lam viec tai doanh nghiep nhan ban thu vien tren mot he thong khong tim thay duong dan phu hop cho nguoi dung"
        msg = check_unaccented_vietnamese(dirty)
        self.assertIn("KHÔNG DẤU", msg)

    def test_prerequisite_guard_exports(self):
        """Tests prerequisite guard reviewer functions are callable."""
        self.assertTrue(callable(prerequisite_guard_agent))
        self.assertTrue(callable(run_prerequisite_check_for_pm))

    def test_reviewer_classes_instantiable(self):
        """Tests reviewer agent classes instantiation."""
        reading_agent = HTMLReadingUIReviewerAgent()
        self.assertIsNotNone(reading_agent)
        lecture_agent = ClassroomLectureUIReviewerAgent()
        self.assertIsNotNone(lecture_agent)

if __name__ == "__main__":
    unittest.main()
