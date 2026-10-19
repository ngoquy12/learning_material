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


class TestBannedTermReplacement(unittest.TestCase):
    def test_thay_tu_cam_trong_van_ban_khong_dung_id_hay_ten_bien(self):
        html = ('<html><head></head><body><h2 id="sec-gotchas">Gotchas phổ biến</h2>'
                '<p>Một anti-pattern và Gotcha.</p><pre><code>gotcha_points = 1</code></pre></body></html>')
        out, changed = sanitize_reading_html(html)
        self.assertTrue(changed)
        self.assertIn('id="sec-gotchas"', out)
        self.assertIn("gotcha_points", out)
        # Chỉ còn "gotcha" trong id và tên biến; văn bản hiển thị không còn từ cấm.
        self.assertEqual(out.lower().count("gotcha"), 2)
        self.assertNotIn("anti-pattern", out.lower())


class TestSandboxReviewerStripsMarkup(unittest.TestCase):
    def test_class_trong_thuoc_tinh_html_khong_bi_coi_la_khai_niem_vuot_cap(self):
        from unittest import mock

        from agents import reviewer_agents

        state = {"session_id": "S", "lesson_id": "L", "technology_stack": "JavaScript",
                 "forbidden_scope": ["class", "this"], "core_ssot": {},
                 "html_content": '<div class="p-4"><script>const o={f(){return this.x}}</script><p>Hàm có tham số.</p></div>',
                 "quiz_json": [{"question": "Hàm trả về gì?"}]}
        with mock.patch.object(reviewer_agents, "call_llm", return_value='{"status": "APPROVED", "feedback": ""}'), \
             mock.patch.dict("os.environ", {"GEMINI_API_KEY": "x"}):
            result = reviewer_agents.sandbox_testing_agent(state)
        self.assertNotIn("vượt cấp", result.get("feedback", ""))

    def test_van_bat_duoc_khai_niem_cam_trong_cau_hoi_quiz(self):
        from unittest import mock

        from agents import reviewer_agents

        state = {"session_id": "S", "lesson_id": "L", "technology_stack": "JavaScript",
                 "forbidden_scope": ["closure"], "core_ssot": {}, "html_content": "<p>Nội dung.</p>",
                 "quiz_json": [{"question": "Closure là gì?"}]}
        with mock.patch.object(reviewer_agents, "call_llm", return_value='{"status": "APPROVED", "feedback": ""}'), \
             mock.patch.dict("os.environ", {"GEMINI_API_KEY": "x"}):
            result = reviewer_agents.sandbox_testing_agent(state)
        self.assertEqual(result["status"], "REJECTED")
        self.assertIn("vượt cấp", result["feedback"])


class TestBannedWordValidatorUsesVisibleText(unittest.TestCase):
    def _errs(self, html):
        from core.validators.reading_validator import validate_reading_material

        return [e for e in validate_reading_material(html, {"tech_stack": "javascript"})[1] if "từ lóng bị cấm" in e]

    def test_chu_thich_va_id_cua_mau_trang_khong_bi_tinh(self):
        html = '<html><body><!-- SECTION 4: GOTCHAS --><h2 id="sec-gotchas">Lỗi thường gặp</h2><script>var gotcha=1</script></body></html>'
        self.assertEqual(self._errs(html), [])

    def test_van_ban_hien_thi_chua_tu_cam_van_bi_bat(self):
        self.assertTrue(self._errs("<html><body><p>Một Gotcha điển hình.</p></body></html>"))
