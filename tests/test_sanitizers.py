import unittest

from core.markdown_sanitizer import ensure_table_blank_lines, sanitize_full_markdown, sanitize_headings_and_structure
from core.reading_html_sanitizer import sanitize_reading_html


class TestMarkdownSanitizer(unittest.TestCase):
    def test_bo_emoji(self):
        self.assertNotIn("🚀", sanitize_full_markdown("# Tiêu đề 🚀\n\nNội dung"))

    def test_sua_tieu_de_thieu_khoang_trang(self):
        self.assertIn("## Tiêu đề", sanitize_headings_and_structure("##Tiêu đề\nNội dung"))

    def test_bang_co_dong_trong_truoc_sau(self):
        out = ensure_table_blank_lines("Đoạn văn\n| a | b |\n| - | - |\n| 1 | 2 |\nĐoạn sau")
        lines = out.splitlines()
        i = lines.index("| a | b |")
        self.assertEqual(lines[i - 1].strip(), "")

    def test_rong_tra_chuoi_rong(self):
        self.assertEqual(sanitize_full_markdown(""), "")

    def test_idempotent(self):
        once = sanitize_full_markdown("##Tiêu đề\nNội dung\n| a | b |\n| - | - |\n| 1 | 2 |\n")
        self.assertEqual(once, sanitize_full_markdown(once))


class TestReadingHtmlSanitizer(unittest.TestCase):
    PLAIN = "<html><head><title>x</title></head><body><p>Không có sơ đồ.</p></body></html>"
    WITH_DIAGRAM = (
        '<html><head><title>x</title></head><body><div class="mermaid text-center">graph TD\nA-->B</div></body></html>'
    )

    def test_trang_khong_co_so_do_khong_bi_chen_thu_vien_mermaid(self):
        out, _changed = sanitize_reading_html(self.PLAIN)
        self.assertNotIn("mermaid", out.lower())
        self.assertEqual(out, self.PLAIN)

    def test_trang_co_so_do_duoc_nap_mermaid(self):
        out, _changed = sanitize_reading_html(self.WITH_DIAGRAM)
        self.assertIn("cdn.jsdelivr.net/npm/mermaid", out)

    def test_khong_nap_hai_lan(self):
        once, _ = sanitize_reading_html(self.WITH_DIAGRAM)
        twice, _ = sanitize_reading_html(once)
        self.assertEqual(once.count("cdn.jsdelivr.net/npm/mermaid"), twice.count("cdn.jsdelivr.net/npm/mermaid"))


if __name__ == "__main__":
    unittest.main()
