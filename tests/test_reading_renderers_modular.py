"""
tests/test_reading_renderers_modular.py
Verifies the Modular Reading Renderers Package (core.renderers.reading):
- Markdown parser
- SVG & Mermaid syntax guards
- Code sandbox & Syntax highlighter
- Step-by-step visualizer component builder
- HTML sanitizer & Reference validator
- Lesson classifier
"""

import unittest
from core.renderers.reading import (
    convert_markdown_to_html,
    ensure_sentence_ending_period,
    slugify_id,
    guard_svg_syntax,
    sanitize_mermaid_code,
    guard_mermaid_syntax,
    resolve_language_info,
    highlight_code_syntax,
    convert_code_to_live_sandbox,
    build_domain_adaptive_visualizer,
    sanitize_references,
    clean_stray_chars,
    classify_reading_type
)

class TestReadingRenderersModular(unittest.TestCase):

    def test_markdown_parser(self):
        """Tests markdown to HTML conversion and punctuation helpers."""
        self.assertEqual(ensure_sentence_ending_period("Khái niệm cơ bản"), "Khái niệm cơ bản.")
        self.assertEqual(ensure_sentence_ending_period("Đã kết thúc."), "Đã kết thúc.")

        slug = slugify_id("2.1. Cú pháp và cách sử dụng biến")
        self.assertEqual(slug, "sec-2-1-cu-phap-va-cach-su-dung-bien")

        md = "- Điểm thứ nhất\n- Điểm thứ hai"
        html_out = convert_markdown_to_html(md)
        self.assertIn("<ul", html_out)
        self.assertIn("<li>Điểm thứ nhất.</li>", html_out)

    def test_svg_and_mermaid_guards(self):
        """Tests SVG sanitization and Mermaid syntax repairs."""
        raw_svg = '<svg><text>HELLO WORLD</text></svg>'
        guarded_svg = guard_svg_syntax(raw_svg)
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', guarded_svg)
        self.assertIn('rikkei-diagram', guarded_svg)
        self.assertIn('Hello World', guarded_svg)

        broken_mermaid = "graph TD\nA -- Lỗi kết nối --> B"
        fixed_mermaid = sanitize_mermaid_code(broken_mermaid)
        self.assertIn("A -->|Lỗi kết nối| B", fixed_mermaid)

    def test_code_sandbox_renderer(self):
        """Tests language resolution, syntax highlighting, and sandbox creation."""
        py_info = resolve_language_info("Python 3")
        self.assertEqual(py_info["engine"], "pyodide")

        git_info = resolve_language_info("Git & GitHub")
        self.assertEqual(git_info["engine"], "static")
        self.assertEqual(git_info["hljs"], "language-bash")

        highlighted = highlight_code_syntax("def calculate_sum(a, b):", "Python")
        self.assertIn("def", highlighted)
        self.assertIn("calculate_sum", highlighted)

        raw_pre = "<pre><code>print('Xin chào Rikkei')</code></pre>"
        sb_html = convert_code_to_live_sandbox(raw_pre, py_info, force_static=False, sb_prefix="test_sb")
        self.assertIn("runPythonCode", sb_html)
        self.assertIn("code-sb-test_sb-1", sb_html)

    def test_visualizer_component_builder(self):
        """Tests building interactive step-by-step visualizer component."""
        viz_spec = {
            "is_applicable": True,
            "title": "2.4. Mô phỏng cơ chế thực thi",
            "explanation": "Theo dõi từng bước thực thi biến số",
            "code_lines": ["x = 10", "y = x + 5"],
            "variables": [{"name": "x", "label": "Biến x"}, {"name": "y", "label": "Biến y"}],
            "steps": [
                {"line": 1, "ram": {"x": "10"}, "log": "> Khởi tạo x = 10"},
                {"line": 2, "ram": {"x": "10", "y": "15"}, "log": "> Tính toán y = 15"}
            ]
        }
        viz_html = build_domain_adaptive_visualizer("Biến và Kiểu dữ liệu", "Python", viz_spec)
        self.assertIn("sec-2-4-mo-phong-co-che-van-hanh-tung-buoc", viz_html)
        self.assertIn("viz-ram-x", viz_html)
        self.assertIn("viz-ram-y", viz_html)
        self.assertIn("window.vizSteps", viz_html)

    def test_html_sanitizer_and_classifier(self):
        """Tests reference sanitizing, cliché cleanup, and reading classification."""
        clean_text = clean_stray_chars("<p>Bài học vô cùng tuyệt vời</p>")
        self.assertIn("cực kỳ", clean_text)
        self.assertIn("hiệu quả", clean_text)
        self.assertNotIn("vô cùng", clean_text)

        refs = sanitize_references([], "python")
        self.assertGreater(len(refs), 0)
        self.assertIn("docs.python.org", refs[0]["url"])

        cls_res = classify_reading_type("Tổng quan lộ trình môn học", "Giới thiệu roadmap khóa học")
        self.assertEqual(cls_res["type"], "ORIENTATION_LESSON")

if __name__ == "__main__":
    unittest.main()
