"""
tests/test_prompts_engine.py
Verifies that all Jinja2 prompt templates in templates/prompts/ compile and render cleanly.
"""

import unittest
from pathlib import Path
from core.prompts import PromptManager, TEMPLATES_PROMPT_DIR

class TestPromptEngineTemplates(unittest.TestCase):

    def setUp(self):
        self.pm = PromptManager.get_instance()

    def test_all_templates_compile_and_render(self):
        """Discovers all .j2 files in templates/prompts and tests rendering with standard context."""
        template_files = list(TEMPLATES_PROMPT_DIR.glob("*.j2"))
        self.assertGreaterEqual(len(template_files), 8, "Expected at least 8 prompt templates in templates/prompts/")

        sample_context = {
            "tech_stack": "python",
            "session_id": "Session 01",
            "lesson_id": "Lesson 01",
            "lesson_title": "Cú pháp cơ bản",
            "idx": 1,
            "level_name": "Basic Application",
            "chosen_domain": "E-Commerce",
            "domain_rules_text": "Tính tổng tiền đơn hàng.",
            "course_id": "PYTHON_CORE",
            "lang_tag": "python",
            "curriculum_json_str": "[]",
            "master_content_summary": "Tóm tắt bài học...",
            "raw_code": "x = 10\nprint(x)",
            "forbidden_scope": "None",
            "allowed_scope": "Python variables",
            "tech_stack_convention": "snake_case",
            "lessons_learned_prompt": "No errors."
        }

        for t_file in template_files:
            t_name = t_file.name
            try:
                rendered = self.pm.render(t_name, sample_context)
                self.assertTrue(len(rendered) > 20, f"Template '{t_name}' produced empty output.")
            except Exception as e:
                self.fail(f"Failed to render template '{t_name}': {e}")

if __name__ == "__main__":
    unittest.main()
