"""
tests/test_reflexion_engine.py
Verifies the Multi-Turn Reflexion Engine:
- Auto-patches Tier-1 AST violations (tables, figcaptions, container backgrounds).
- Detects code runtime errors via sandbox.
- Generates targeted feedback instructions for LLM retry.
"""

import unittest
from core.reflexion import ReflexionEngine, ReflexionViolation, ViolationSeverity

class TestReflexionEngine(unittest.TestCase):

    def test_auto_patch_ast_table_wrapper(self):
        """Tests that raw <table> is automatically wrapped in an overflow-x-auto container."""
        raw_html = "<article><table><tr><td>Item</td></tr></table></article>"
        patched = ReflexionEngine.auto_patch_ast_violations(raw_html)
        self.assertIn('class="overflow-x-auto', patched)
        self.assertIn("<table>", patched)

    def test_auto_patch_figcaption_italics(self):
        """Tests that figcaption without italic tag gets wrapped in <i>."""
        raw_html = "<figure><img src='pic.png'/><figcaption>Hình 1.1 Sơ đồ kiến trúc</figcaption></figure>"
        patched = ReflexionEngine.auto_patch_ast_violations(raw_html)
        self.assertIn("<i>Hình 1.1 Sơ đồ kiến trúc</i>", patched)

    def test_auto_patch_dark_container_to_light_mode(self):
        """Tests that unexpected dark mode containers are corrected to bg-slate-50."""
        raw_html = "<section class='p-6 bg-slate-900 border border-slate-700'><h2>Tiêu đề</h2></section>"
        patched = ReflexionEngine.auto_patch_ast_violations(raw_html)
        self.assertNotIn("bg-slate-900", patched)
        self.assertIn("bg-slate-50", patched)

    def test_verify_embedded_code_runtime_violation(self):
        """Tests that embedded python code with runtime error produces a Tier-2 violation."""
        content = """
        Dưới đây là mã nguồn:
        ```python
        def divide(a, b):
            return a / b
        print(divide(10, 0))
        ```
        """
        violations = ReflexionEngine.verify_embedded_code_runtime(content, tech_stack="python")
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].severity, ViolationSeverity.TIER_2_RUNTIME_ERROR)
        self.assertIn("ZeroDivisionError", violations[0].message)

    def test_targeted_feedback_generation(self):
        """Tests targeted feedback string compilation."""
        violation = ReflexionViolation(
            rule_id="CODE_RUNTIME_FAILURE",
            severity=ViolationSeverity.TIER_2_RUNTIME_ERROR,
            message="ZeroDivisionError khi chạy divide(10, 0)",
            target_section="Section 3",
            runtime_traceback="ZeroDivisionError: division by zero",
            suggested_patch="Kiểm tra mẫu số khác 0 trước khi chia."
        )
        feedback = ReflexionEngine.create_targeted_feedback([violation])
        self.assertIn("REFLEXION AUDIT FEEDBACK", feedback)
        self.assertIn("ZeroDivisionError", feedback)
        self.assertIn("Hướng dẫn sửa", feedback)

if __name__ == "__main__":
    unittest.main()
