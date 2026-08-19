"""
tests/test_slide_deck_generator.py
Unit and Integration tests for Create_Slide 3-Skill PPTX Slide Deck Generator & Reviewer.
"""

import unittest
import tempfile
import shutil
import zipfile
from pathlib import Path

from core.renderers.pptx.slide_deck_builder import SlideDeckBuilder, slide_deck_builder
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

    def test_slide_deck_builder_e2e(self):
        """Tests that SlideDeckBuilder builds a complete, valid PPTX file from slide data."""
        slides_data = [
            {
                "slide_number": 1,
                "type": "cover",
                "layout": "slideLayout1.xml",
                "title": "Tương tác DOM API trong JavaScript",
                "course_name": "Phát triển ứng dụng Web",
                "speaker_notes": "Chào mừng các bạn đến với bài học hôm nay."
            },
            {
                "slide_number": 2,
                "type": "agenda",
                "layout": "slideLayout2.xml",
                "title": "Nội Dung Bài Giảng",
                "agenda_items": [
                    "Tổng quan về cây DOM",
                    "Truy xuất phần tử qua getElementById & querySelector",
                    "Thay đổi nội dung textContent và innerHTML",
                    "Tổng kết & Lưu ý kỹ thuật"
                ],
                "speaker_notes": "Hôm nay chúng ta sẽ đi qua 4 nội dung trọng tâm."
            },
            {
                "slide_number": 3,
                "type": "code",
                "layout": "slideLayout2.xml",
                "title": "1. Truy Xuất Phần Tử DOM — 1/2",
                "subtitle": "Áp dụng trong hệ thống gọi xe công nghệ",
                "bullets": [
                    "Sử dụng document.getElementById cho ID duy nhất",
                    "Sử dụng querySelector cho CSS Selector linh hoạt",
                    "Kiểm tra phần tử tồn tại trước khi thao tác"
                ],
                "code_title": "DOM Query API",
                "code_snippet": "const bookingBtn = document.getElementById('btn-book');\nif (bookingBtn) {\n  bookingBtn.innerText = 'Đặt chuyến ngay';\n}",
                "speaker_notes": "Hãy cùng nhìn vào đoạn mã mẫu truy xuất nút đặt chuyến..."
            },
            {
                "slide_number": 4,
                "type": "table",
                "layout": "slideLayout2.xml",
                "title": "So Sánh textContent & innerHTML",
                "subtitle": "Lựa chọn phương thức an toàn bảo mật",
                "table_headers": ["Tiêu chí", "textContent", "innerHTML"],
                "table_rows": [
                    ["Bảo mật XSS", "Tuyệt đối an toàn (chỉ nhận text)", "Nguy cơ XSS nếu không sanitize"],
                    ["Hiệu năng", "Nhanh hơn", "Chậm hơn do phải parse HTML"],
                    ["Render HTML tag", "Không render (hiển thị nguyên bản)", "Có render thành phần tử DOM"]
                ],
                "speaker_notes": "Bảng so sánh này rất quan trọng để tránh lỗ hổng bảo mật XSS."
            },
            {
                "slide_number": 5,
                "type": "cards",
                "layout": "slideLayout2.xml",
                "title": "Thuật Ngữ Cần Nhớ",
                "subtitle": "Từ khóa kỹ thuật then chốt",
                "cards": [
                    {"title": "DOM Node", "bullets": ["Nút trong cây cấu trúc tài liệu", "Đại diện cho thẻ HTML, text hoặc attribute"]},
                    {"title": "XSS Attack", "bullets": ["Tấn công chèn mã độc vào trình duyệt", "Xảy ra khi dùng innerHTML bừa bãi"]}
                ],
                "speaker_notes": "Các bạn hãy ghi nhớ 2 thuật ngữ cốt lõi này."
            },
            {
                "slide_number": 6,
                "type": "closing",
                "layout": "slideLayout3.xml",
                "title": "Chúc Các Bạn Học Tốt!",
                "message": "Hẹn gặp lại các bạn trong bài giảng tiếp theo.",
                "speaker_notes": "Cảm ơn các bạn đã lắng nghe!"
            }
        ]

        target_pptx = self.out_dir / "Slide_Bai_Giang_Test.pptx"
        built_path = slide_deck_builder.build_deck_from_slides_data(
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
            self.assertIn("ppt/slides/slide6.xml", names)
            self.assertIn("ppt/notesSlides/notesSlide1.xml", names)

        # Run Validator
        val_res = validate_pptx_file(built_path)
        self.assertTrue(val_res["passed"], f"Validation failed with errors: {val_res.get('errors')}")
        self.assertEqual(val_res["total_slides"], 6)

    def test_slide_deck_creator_and_reviewer_agents(self):
        """Tests end-to-end generation and review of Slide bài giảng."""
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
