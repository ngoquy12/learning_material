import tempfile
import unittest
from pathlib import Path

from core.renderers.lecture.outline_deck_compiler import compile_outline_to_html, parse_outline_markdown

OUTLINE = """# Outline Bài Giảng: Buổi thử

### Slide 1: [cover] Mở đầu
*Phụ đề ngắn*
🎙️ **Speaker Notes:** Chào lớp. [~2 phút]

### Slide 2: [content] Nội dung chính
- Ý một
- Ý hai
"""


class TestOutlineDeckCompiler(unittest.TestCase):
    def test_parse(self):
        data = parse_outline_markdown(OUTLINE)
        self.assertEqual(data["session_title"], "Buổi thử")
        self.assertEqual([s["num"] for s in data["slides"]], [1, 2])
        self.assertEqual(data["slides"][0]["type"], "cover")
        self.assertEqual(data["slides"][0]["subtitle"], "Phụ đề ngắn")
        self.assertEqual(data["slides"][0]["timing"], "~2 phút")

    def test_compile_ra_html_khong_gan_cung_ten_mon(self):
        with tempfile.TemporaryDirectory() as tmp:
            md = Path(tmp) / "outline_bai_giang.md"
            md.write_text(OUTLINE, encoding="utf-8")
            out = Path(tmp) / "slides.html"
            compile_outline_to_html(md, out, module_name="Môn thử")
            html = out.read_text(encoding="utf-8")
        self.assertIn("Môn thử", html)
        self.assertIn("Mở đầu", html)
        self.assertNotIn("IT103", html)


if __name__ == "__main__":
    unittest.main()
