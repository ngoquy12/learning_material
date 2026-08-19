"""
tests/test_pydantic_schemas.py
Verifies Pydantic v2 Schema validation for Quizzes, Labs, Homework, and Visualizers.
"""

import unittest
from core.schemas.course_schemas import (
    EnhancedQuizItemSchema,
    EnhancedPracticalLabSchema,
    EnhancedHomeworkExerciseSchema,
    EnhancedVisualizerSchema
)
from core.utils.schema_validator import validate_schema, validate_and_dump

class TestPydanticSchemaValidation(unittest.TestCase):

    def test_quiz_schema_valid_and_auto_padding(self):
        """Tests that quiz items validate properly and pad options if fewer than 4."""
        raw_quiz = {
            "stt": 1,
            "question_type": "SYNTAX",
            "question": "Cú pháp khai báo biến trong Python?",
            "options": ["x = 10", "var x = 10"],
            "correct_option_index": 0,
            "explanation": "Python không cần từ khóa var."
        }
        is_valid, instance, errors = validate_schema(EnhancedQuizItemSchema, raw_quiz)
        self.assertTrue(is_valid)
        self.assertIsNotNone(instance)
        self.assertEqual(len(instance.options), 4, "Options should be auto-padded to 4")
        self.assertEqual(instance.correct_option_index, 0)

    def test_quiz_schema_invalid_index_clamping(self):
        """Tests that out-of-range correct_option_index is clamped between 0 and 3."""
        raw_quiz = {
            "stt": 2,
            "question": "Test question?",
            "options": ["A", "B", "C", "D"],
            "correct_option_index": 99,
            "explanation": "Explanation"
        }
        is_valid, instance, _ = validate_schema(EnhancedQuizItemSchema, raw_quiz)
        self.assertTrue(is_valid)
        self.assertEqual(instance.correct_option_index, 3, "Index 99 should clamp to 3")

    def test_practical_lab_schema_validation(self):
        """Tests practical lab schema validation and dictionary dumping."""
        raw_lab = {
            "title": "Bài thực hành: Cấu hình Virtualenv",
            "objectives": ["Tạo venv", "Cài đặt gói"],
            "description": {
                "inputs": "Python 3.10+",
                "steps": ["1. python -m venv .venv", "2. pip install -r requirements.txt"]
            },
            "evaluation": {
                "checklist": ["[ ] Đã kích hoạt môi trường"]
            }
        }
        is_valid, instance, errors = validate_schema(EnhancedPracticalLabSchema, raw_lab)
        self.assertTrue(is_valid, f"Lab validation failed: {errors}")
        dumped = validate_and_dump(EnhancedPracticalLabSchema, raw_lab)
        self.assertEqual(dumped["title"], "Bài thực hành: Cấu hình Virtualenv")
        self.assertEqual(len(dumped["description"]["steps"]), 2)

    def test_homework_schema_validation(self):
        """Tests homework exercise schema validation."""
        raw_hw = {
            "idx": 1,
            "level_name": "Basic Application",
            "chosen_domain": "E-Commerce",
            "de_bai_content": "### 1. Mục tiêu...",
            "tieu_chi_content": "### Tiêu chuẩn đánh giá..."
        }
        is_valid, instance, errors = validate_schema(EnhancedHomeworkExerciseSchema, raw_hw)
        self.assertTrue(is_valid)
        self.assertEqual(instance.idx, 1)

    def test_visualizer_schema_validation(self):
        """Tests visualizer schema validation."""
        raw_viz = {
            "canvas_title": "SQL Query State Machine",
            "engine_js": "class InteractiveVisualizerEngine { init() {} }"
        }
        is_valid, instance, errors = validate_schema(EnhancedVisualizerSchema, raw_viz)
        self.assertTrue(is_valid)
        self.assertEqual(instance.input_label, "Nhập dữ liệu test:")

if __name__ == "__main__":
    unittest.main()
