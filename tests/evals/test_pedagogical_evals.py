"""
tests/evals/test_pedagogical_evals.py
Automated Pedagogical Evaluation Suite for Elearning Content Factory.
Verifies Bloom Cognitive Taxonomy alignment, Unified Scenario Integrity,
Anti-AI Cliché vocabulary checks, and Strict Light Mode UI compliance.
"""

import unittest
from core.validators.visual_linter import validate_html_visual_layout
from core.validators.reading_validator import validate_reading_material
from core.scope_calculator import calculate_lesson_scope_contract

class TestPedagogicalEvaluationSuite(unittest.TestCase):

    def test_anti_ai_cliche_detection(self):
        """Ensures that forbidden AI marketing buzzwords are strictly flagged."""
        bad_samples = [
            "<section id='section-1'><h2>Cùng khám phá bẫy lập trình trong Python</h2><img src='a.png'><i>Hình 1</i></section>",
            "<section id='section-1'><h2>Bí kíp tất tần tật về vòng lặp</h2><img src='a.png'><i>Hình 1</i></section>",
            "<section id='section-1'><h2>Tính năng vô cùng tuyệt vời và vi diệu</h2><img src='a.png'><i>Hình 1</i></section>"
        ]
        for sample in bad_samples:
            is_valid, errors = validate_html_visual_layout(sample)
            self.assertFalse(is_valid, f"Failed to flag AI cliché in: {sample}")
            self.assertTrue(any("sáo rỗng" in e for e in errors))

    def test_strict_light_mode_ast_compliance(self):
        """Verifies that dark background containers are rejected while dark code blocks are permitted."""
        # Illegal dark container
        illegal_dark = """
        <section id="section-1">
          <h2>Tổng quan kiến trúc</h2>
          <div class="bg-slate-900 rounded-xl p-4">
            <p>Khung container bị tô màu đen</p>
          </div>
          <img src="img.png">
          <i>Hình 1: Sơ đồ hệ thống.</i>
        </section>
        """
        is_valid, errors = validate_html_visual_layout(illegal_dark)
        self.assertFalse(is_valid)
        self.assertTrue(any("Strict Light Mode" in e for e in errors))

        # Legal dark terminal code block
        legal_light_with_code = """
        <section id="section-1">
          <h2>Tổng quan kiến trúc</h2>
          <div class="bg-white border border-slate-200 rounded-xl p-4">
            <p>Khung container nền trắng đạt chuẩn</p>
            <pre class="bg-slate-900 text-green-400 p-4 font-mono"><code>console.log('Hello');</code></pre>
          </div>
          <img src="img.png">
          <i>Hình 1: Sơ đồ hệ thống.</i>
        </section>
        """
        is_valid, errors = validate_html_visual_layout(legal_light_with_code)
        light_mode_errors = [e for e in errors if "Strict Light Mode" in e]
        self.assertEqual(len(light_mode_errors), 0)

    def test_dynamic_scope_calculator_boundaries(self):
        """Tests that dynamic knowledge scope properly separates taught vs future concepts."""
        mock_curriculum = {
            "sessions": [
                {
                    "session_id": "Session 01",
                    "lessons": [
                        {"title": "Cú pháp cơ bản", "keywords": ["biến", "print", "kiểu dữ liệu"]},
                        {"title": "Câu lệnh if-else", "keywords": ["if", "else", "elif"]}
                    ]
                },
                {
                    "session_id": "Session 02",
                    "lessons": [
                        {"title": "Vòng lặp for", "keywords": ["for", "range", "loop"]},
                        {"title": "Hàm cơ bản", "keywords": ["def", "function", "return"]}
                    ]
                }
            ]
        }
        # For Session 01 - Lesson 0 (Cú pháp cơ bản)
        allowed, forbidden = calculate_lesson_scope_contract(mock_curriculum, 0, 0)
        self.assertIn("biến", allowed)
        self.assertIn("câu lệnh if-else", forbidden)
        self.assertIn("vòng lặp for", forbidden)
        self.assertIn("hàm cơ bản", forbidden)

if __name__ == "__main__":
    unittest.main()
