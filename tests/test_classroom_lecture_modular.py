"""
tests/test_classroom_lecture_modular.py
Verifies the Modular Classroom Lecture Presentation Creator:
- Jinja2 prompt rendering via PromptManager (classroom_lecture.j2).
- Type-safe schema validation with Pydantic v2 (ClassroomSlideDeckSchema).
- Interactive HTML slide deck compilation from AgentState.
"""

import unittest
from agents.creators.classroom_lecture_creator import (
    generate_lecture_slide_outline,
    classroom_lecture_agent,
    slide_agent
)
from core.schemas.course_schemas import ClassroomSlideDeckSchema
from core.utils.schema_validator import validate_schema

class TestClassroomLectureModular(unittest.TestCase):

    def test_generate_lecture_slide_outline_schema(self):
        """Tests that slide deck outline conforms to ClassroomSlideDeckSchema."""
        deck = generate_lecture_slide_outline(
            session_id="Session 02",
            session_title="Cú pháp và Biến",
            tech_stack="Python 3.12",
            lesson_outline_text="1. Khai báo biến\n2. Kiểu dữ liệu cơ sở",
            course_name="Lập trình Python"
        )
        self.assertIn("session_id", deck)
        self.assertIn("slides", deck)
        self.assertGreaterEqual(len(deck["slides"]), 2)

        is_valid, validated_obj, errs = validate_schema(ClassroomSlideDeckSchema, deck)
        self.assertTrue(is_valid)
        self.assertEqual(validated_obj.session_id, "Session 02")

    def test_classroom_lecture_agent_html_compilation(self):
        """Tests compiling full HTML presentation from state."""
        state = {
            "session_id": "Session 02",
            "technology_stack": "Python 3.12",
            "core_ssot": {
                "session_title": "Cú pháp và Biến",
                "course_name": "Lập trình Python",
                "session_lessons": [
                    {"title": "Khai báo biến"},
                    {"title": "Kiểu dữ liệu cơ sở"}
                ]
            }
        }
        res_state = classroom_lecture_agent(state)
        self.assertIn("lecture_html", res_state)
        self.assertIn("slide_html", res_state)
        self.assertIn("<!DOCTYPE html>", res_state["lecture_html"])
        self.assertIn("Cú pháp và Biến", res_state["lecture_html"])

if __name__ == "__main__":
    unittest.main()
