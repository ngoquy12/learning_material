# tests/test_visual_linter.py
import unittest
from core.validators.visual_linter import validate_html_visual_layout

class TestVisualLinterEngine(unittest.TestCase):

    def test_table_without_overflow_wrapper(self):
        """Verify that <table> without overflow-x-auto wrapper triggers a visual defect error."""
        html_bad = """
        <section id="section-1">
          <h2>Thử nghiệm Bảng</h2>
          <table>
            <tr><th>Header 1</th><th>Header 2</th></tr>
            <tr><td>Data 1</td><td>Data 2</td></tr>
          </table>
        </section>
        """
        is_valid, errors = validate_html_visual_layout(html_bad)
        self.assertFalse(is_valid)
        self.assertTrue(any("overflow-x-auto" in e for e in errors))

    def test_valid_wrapped_table(self):
        """Verify that <table> with overflow-x-auto wrapper passes inspection."""
        html_good = """
        <section id="section-1">
          <h2>Thử nghiệm Bảng Hợp lệ</h2>
          <div class="overflow-x-auto my-4">
            <table class="w-full">
              <tr><th>Header 1</th><th>Header 2</th></tr>
              <tr><td>Data 1</td><td>Data 2</td></tr>
            </table>
          </div>
          <img src="test.jpg">
          <i>Hình 1: Minh họa sơ đồ hệ thống.</i>
        </section>
        """
        is_valid, errors = validate_html_visual_layout(html_good)
        # Filter errors to check no table wrapper errors
        table_errs = [e for e in errors if "overflow-x-auto" in e]
        self.assertEqual(len(table_errs), 0)

    def test_dark_mode_violation(self):
        """Verify Light Mode Rule 11 enforcer catches illegal dark container cards."""
        html_dark = """
        <section id="section-1">
          <h2>Tiêu đề bài học</h2>
          <div class="bg-slate-900 p-4 rounded-xl text-white">
            <p>Nội dung container bị gán nhầm nền đen</p>
          </div>
          <img src="test.png">
          <i>Hình 1: Sơ đồ bối cảnh.</i>
        </section>
        """
        is_valid, errors = validate_html_visual_layout(html_dark)
        self.assertFalse(is_valid)
        self.assertTrue(any("Quy tắc 11" in e or "Nền Đen/Tối" in e for e in errors))

    def test_all_caps_heading_violation(self):
        """Verify Rule 3 enforcer catches ALL CAPS headings."""
        html_all_caps = """
        <section id="section-1">
          <h1>TẠI SAO CẦN DÙNG HÀM VÀ THAM SỐ KHÁC NHAU</h1>
          <p>Nội dung chi tiết...</p>
          <img src="test.jpg">
          <i>Hình 1: Caption minh họa.</i>
        </section>
        """
        is_valid, errors = validate_html_visual_layout(html_all_caps)
        self.assertFalse(is_valid)
        self.assertTrue(any("Quy tắc 3" in e or "IN HOA TOÀN BỘ" in e for e in errors))

    def test_image_without_italic_caption(self):
        """Verify image without italic caption triggers an inspection error."""
        html_no_caption = """
        <section id="section-1">
          <h2>Tiêu đề hợp lệ</h2>
          <img src="test.jpg">
          <p>Đoạn văn tiếp theo không có chú thích nghiêng.</p>
        </section>
        """
        is_valid, errors = validate_html_visual_layout(html_no_caption)
        self.assertFalse(is_valid)
        self.assertTrue(any("chú thích in nghiêng" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
