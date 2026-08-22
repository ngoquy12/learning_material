"""
tests/test_homework_creator.py
Verifies the Modular Homework Creator Agent:
- Jinja2 prompt rendering via PromptManager (homework_creator.j2).
- Type-safe schema validation with Pydantic v2 (EnhancedHomeworkExerciseSchema).
- Markdown sanitization (zero-emoji, header normalization).
- Full session homework suite generation.
"""

import unittest
from pathlib import Path
from unittest.mock import patch
from agents.creators.homework_creator import (
    generate_homework_exercise,
    generate_session_homework_suite,
    sanitize_homework_markdown,
    clean_markdown_formulas
)
from core.schemas.course_schemas import EnhancedHomeworkExerciseSchema
from core.utils.schema_validator import validate_schema

class TestHomeworkCreator(unittest.TestCase):

    def test_sanitize_homework_markdown_strips_emoji(self):
        """Tests that emojis and excessive whitespace are stripped from homework markdown."""
        dirty_md = "## Bài tập 01 🚀✨\n### 1. Mục tiêu 🔥\nNội dung bài tập."
        cleaned = sanitize_homework_markdown(dirty_md)
        self.assertNotIn("🚀", cleaned)
        self.assertNotIn("✨", cleaned)
        self.assertNotIn("🔥", cleaned)
        self.assertIn("Bài tập 01", cleaned)

    def test_clean_markdown_formulas(self):
        """Tests header depth normalization in formulas."""
        raw = "##### Tiêu chí chấm điểm\nNội dung"
        cleaned = clean_markdown_formulas(raw)
        self.assertIn("### Tiêu chí chấm điểm", cleaned)

    @patch("agents.creators.homework_creator.call_llm", return_value="")
    def test_generate_single_homework_exercise_structure(self, mock_call_llm):
        """
        Tests generating a single homework exercise with fallback and validation.

        LLM trả rỗng để ép chạy nhánh fallback (_fallback_de_bai/_fallback_tieu_chi) —
        đúng thứ test này khẳng định: cấu trúc heading + schema Pydantic, không phải
        chất lượng nội dung do LLM sinh.
        """
        ex = generate_homework_exercise(
            session_id="Session 02",
            session_title="Cú pháp cơ bản",
            tech_stack="Python 3.12",
            previous_lessons_text="Biến, kiểu dữ liệu, toán tử",
            idx=1,
            level_name="Cơ bản 1 - Debug lỗi",
            chosen_domain="E-Commerce",
            total_exercises=6
        )
        self.assertEqual(ex["idx"], 1)
        self.assertEqual(ex["chosen_domain"], "E-Commerce")
        self.assertIn("### 1. Mục tiêu bài tập", ex["de_bai_content"])
        self.assertIn("### Tiêu chuẩn Đánh giá", ex["tieu_chi_content"])

        # Pydantic schema validation
        is_valid, validated_obj, errs = validate_schema(EnhancedHomeworkExerciseSchema, ex)
        self.assertTrue(is_valid)
        self.assertEqual(validated_obj.idx, 1)

    @patch("agents.creators.homework_creator.call_llm", return_value="")
    def test_generate_session_homework_suite(self, mock_call_llm):
        """Tests generating a suite of tiered exercises (fallback path, no live LLM)."""
        suite = generate_session_homework_suite(
            session_id="Session 02",
            session_title="Cú pháp cơ bản",
            tech_stack="Python 3.12",
            previous_lessons_text="Biến, kiểu dữ liệu",
            total_exercises=6
        )
        self.assertEqual(len(suite), 6)
        self.assertEqual([e["idx"] for e in suite], [1, 2, 3, 4, 5, 6])

    @patch("agents.creators.homework_creator.call_llm", return_value="")
    def test_generate_inclass_synthesis_and_mindmap(self, mock_call_llm):
        """Tests generating in-class synthesis exercise and mindmap exercise (fallback path)."""
        from agents.creators.homework_creator import (
            generate_inclass_synthesis_exercise,
            generate_mindmap_exercise
        )
        inclass_md = generate_inclass_synthesis_exercise(
            session_id="Session 02",
            session_title="Cú pháp cơ bản",
            tech_stack="Python 3.12",
            previous_lessons_text="Biến, kiểu dữ liệu"
        )
        self.assertIn("# Bài tập tổng hợp trên lớp", inclass_md)
        self.assertIn("## 1. Mục tiêu bài tập", inclass_md)

        mindmap_md = generate_mindmap_exercise(
            session_id="Session 02",
            session_title="Cú pháp cơ bản",
            tech_stack="Python 3.12",
            previous_lessons_text="Biến, kiểu dữ liệu"
        )
        self.assertIn("# Bài tập sơ đồ tư duy mindmap", mindmap_md)
        self.assertIn("## 1. Mục tiêu bài tập", mindmap_md)

if __name__ == "__main__":
    unittest.main()
