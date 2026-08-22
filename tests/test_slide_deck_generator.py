"""
tests/test_slide_deck_generator.py
Unit and Integration tests for Create_Slide 3-Skill PPTX Slide Deck Generator & Reviewer.
"""

import unittest
import tempfile
import shutil
import zipfile
from pathlib import Path

import pytest

from core.renderers.pptx.deck_engine import build_deck
from core.renderers.pptx.slide_validator import validate_pptx_file, validate_unpacked_deck
from agents.creators.slide_deck_creator import SlideDeckCreatorAgent, generate_session_slide_deck
from agents.reviewers.slide_deck_reviewer import SlideDeckReviewerAgent, review_session_slide_deck

class TestSlideDeckGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.out_dir = Path(self.test_dir) / "Slide bài giảng"
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_deck_engine_build_deck_e2e(self):
        """Tests that build_deck() builds a complete, valid PPTX file from slide data."""
        slides_data = [
            {
                "id": 1,
                "type": "cover",
                "session_tag": "Session 17",
                "title": "Tương tác DOM API trong JavaScript",
                "course_name": "Phát triển ứng dụng Web",
                "notes": "Chào mừng các bạn đến với bài học hôm nay."
            },
            {
                "id": 2,
                "type": "agenda",
                "items": [
                    "1. Tổng quan về cây DOM",
                    "2. Truy xuất phần tử qua getElementById & querySelector",
                    "3. Thay đổi nội dung textContent và innerHTML",
                    "4. Tổng kết & Lưu ý kỹ thuật"
                ],
                "notes": "Hôm nay chúng ta sẽ đi qua 4 nội dung trọng tâm."
            },
            {
                "id": 3,
                "type": "objectives",
                "h1": "Mục tiêu bài học",
                "goals": ["Hiểu cách truy xuất phần tử DOM", "Phân biệt textContent và innerHTML"],
                "notes": "Mục tiêu bài học hôm nay."
            },
            {
                "id": 4,
                "type": "code_right_card",
                "h1": "Truy xuất phần tử DOM",
                "h2": "document.getElementById trả về phần tử duy nhất theo id.",
                "code_title": "DOM Query API",
                "code_snippet": "const bookingBtn = document.getElementById('btn-book');\nif (bookingBtn) {\n  bookingBtn.innerText = 'Đặt chuyến ngay';\n}",
                "lang_tag": "JS",
                "card_title": "Lưu ý",
                "card_items": ["Kiểm tra phần tử tồn tại trước khi thao tác"],
                "notes": "Hãy cùng nhìn vào đoạn mã mẫu truy xuất nút đặt chuyến..."
            },
            {
                "id": 5,
                "type": "comparison_2col",
                "h1": "So sánh textContent & innerHTML",
                "h2": "textContent an toàn hơn innerHTML trước tấn công XSS.",
                "left_title": "textContent",
                "left_items": ["Tuyệt đối an toàn (chỉ nhận text)", "Nhanh hơn"],
                "right_title": "innerHTML",
                "right_items": ["Nguy cơ XSS nếu không sanitize", "Chậm hơn do phải parse HTML"],
                "notes": "Bảng so sánh này rất quan trọng để tránh lỗ hổng bảo mật XSS."
            },
            {
                "id": 6,
                "type": "glossary_table",
                "h1": "Thuật ngữ cần nhớ",
                "headers": ["Thuật ngữ", "Tiếng Anh", "Định nghĩa"],
                "rows": [
                    ["Nút DOM", "DOM Node", "Nút trong cây cấu trúc tài liệu"],
                    ["Tấn công XSS", "XSS Attack", "Tấn công chèn mã độc vào trình duyệt"],
                ],
                "notes": "Các bạn hãy ghi nhớ 2 thuật ngữ cốt lõi này."
            },
            {
                "id": 7,
                "type": "closing",
                "title": "Chúc các bạn học tốt!",
                "subtitle": "Hẹn gặp lại các bạn trong bài giảng tiếp theo.",
                "notes": "Cảm ơn các bạn đã lắng nghe!"
            }
        ]

        target_pptx = self.out_dir / "Slide_Bai_Giang_Test.pptx"
        built_path = build_deck(
            slides_data=slides_data,
            output_pptx_path=target_pptx
        )

        self.assertTrue(built_path.exists())
        self.assertGreater(built_path.stat().st_size, 50000)  # > 50KB

        # Verify PPTX is a valid zip with all slides
        with zipfile.ZipFile(built_path, 'r') as z:
            names = z.namelist()
            self.assertIn("ppt/presentation.xml", names)
            self.assertIn("ppt/slides/slide1.xml", names)
            self.assertIn("ppt/slides/slide7.xml", names)
            self.assertIn("ppt/notesSlides/notesSlide1.xml", names)

        # Run Validator
        val_res = validate_pptx_file(built_path)
        self.assertTrue(val_res["passed"], f"Validation failed with errors: {val_res.get('errors')}")
        self.assertEqual(val_res["total_slides"], 7)

    @pytest.mark.integration
    def test_slide_deck_creator_and_reviewer_agents(self):
        """
        Tests end-to-end generation and review of Slide bài giảng.

        INTEGRATION: test này sinh PPTX thật rồi đòi reviewer chấm 100 điểm và >5 slide —
        chỉ đạt được với nội dung LLM thật, không mock nổi một cách có ý nghĩa.
        Chạy bằng: pytest --run-integration
        """
        res = generate_session_slide_deck(
            session_title="Session 17 - Tương tác DOM API (Document Object Model)- Truy xuất và Thay đổi Nội dung",
            course_name="Phát triển ứng dụng Web",
            tech_stack="JavaScript",
            target_dir=self.out_dir
        )

        self.assertIn(res["status"], ["SUCCESS", "WARNING"])
        self.assertTrue(Path(res["pptx_path"]).exists())
        self.assertTrue(Path(res["outline_path"]).exists())

        # Review
        review_res = review_session_slide_deck(self.out_dir)
        self.assertEqual(review_res["status"], "PASSED")
        self.assertEqual(review_res["score"], 100)
        self.assertGreater(review_res["total_slides"], 5)

if __name__ == "__main__":
    unittest.main()
