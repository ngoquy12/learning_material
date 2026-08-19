"""
tests/test_cli_and_sanitizers_modular.py
Verifies the Modular CLI Commands and Sanitizers Packages:
- core.sanitizers (diacritics, markdown, scope guard, json recoverer)
- cli.commands (init_config, generate_pm, workflow_cmd)
- agents.creators.common_utils backward compatibility
"""

import unittest
from pathlib import Path
from core.sanitizers import (
    ensure_vietnamese_diacritics,
    clean_unwanted_text,
    clean_markdown_formulas,
    normalize_markdown_headers,
    validate_and_clean_forbidden_scope,
    fix_raw_newlines_in_json_strings,
    robust_json_parse,
)
from agents.creators.common_utils import (
    clean_markdown_formulas as cu_clean_formulas,
    ensure_vietnamese_diacritics as cu_ensure_diacritics,
    robust_json_parse as cu_robust_parse,
)
from cli.commands import handle_init_config

class TestCliAndSanitizersModular(unittest.TestCase):

    def test_diacritics_and_unwanted_text_sanitizer(self):
        """Tests Vietnamese diacritics fixing and AI buzzword cleaning."""
        raw_text = "tai sao nguoi dung can su dung toan tu so hoc va gotcha?"
        sanitized = ensure_vietnamese_diacritics(raw_text)
        self.assertIn("tại sao", sanitized)
        self.assertIn("người dùng", sanitized)
        self.assertIn("toán tử", sanitized)

        buzzword_text = "Đây là bẫy lập trình và bí kíp thần thánh W3Schools"
        cleaned_buzz = clean_unwanted_text(buzzword_text)
        self.assertNotIn("bẫy lập trình", cleaned_buzz)
        self.assertNotIn("bí kíp", cleaned_buzz)
        self.assertNotIn("thần thánh", cleaned_buzz)
        self.assertNotIn("W3Schools", cleaned_buzz)

    def test_markdown_and_formula_sanitizer(self):
        """Tests LaTeX formula transformation and header normalization."""
        formula_text = r"Công thức tính tổng: \frac{A}{B} và \text{doanh thu} $$x \times y$$"
        cleaned_formula = clean_markdown_formulas(formula_text)
        self.assertIn("(A) / (B)", cleaned_formula)
        self.assertIn("`x * y`", cleaned_formula)

        unspaced_markdown = "Đoạn văn kết thúc.### Tiêu đề con\n```python\nx = 1\n```"
        normalized = normalize_markdown_headers(unspaced_markdown)
        self.assertIn("\n\n### Tiêu đề con", normalized)

    def test_scope_guard_and_json_recoverer(self):
        """Tests forbidden scope cleaner and resilient JSON recovery parser."""
        content = {
            "problem": "Chúng ta sẽ sử dụng vòng lặp for và while trong bài này.",
            "solution": "Áp dụng biến số let x = 10;"
        }
        cleaned_content, violations = validate_and_clean_forbidden_scope(content, "while, break")
        self.assertTrue(len(violations) > 0)
        self.assertIn("/* [Scope Guard: Filtered 'while'] */", cleaned_content["problem"])

        broken_json = '{\n"problem": "Khởi tạo dữ liệu\\nđúng chuẩn",\n"analysis": "Đánh giá chi tiết"\n}'
        recovered = robust_json_parse(broken_json)
        self.assertEqual(recovered.get("analysis"), "Đánh giá chi tiết")

    def test_common_utils_backward_compatibility(self):
        """Ensures common_utils re-exports match core.sanitizers exactly."""
        res1 = cu_ensure_diacritics("nguoi dung")
        self.assertEqual(res1, "người dùng")
        
        parsed = cu_robust_parse('{"problem": "Test"}')
        self.assertEqual(parsed.get("problem"), "Test")

    def test_cli_init_config_command(self):
        """Tests init-config command generation."""
        handle_init_config("TEST-MODULAR-COURSE")
        cfg_file = Path("config/pm_generator_config_testmodularcourse.json")
        self.assertTrue(cfg_file.exists())
        cfg_file.unlink(missing_ok=True)

if __name__ == "__main__":
    unittest.main()
