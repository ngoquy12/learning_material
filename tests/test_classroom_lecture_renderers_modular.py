"""
tests/test_classroom_lecture_renderers_modular.py
Verifies the Modular Classroom Lecture Package (core.renderers.lecture):
- Text sanitizer and topic extractor
- Knowledge extractor & scenario deriver
- Presentation deck HTML generator
- Interactive visualizer simulation builder
- ClassroomLectureGeneratorAgent facade
"""

import unittest
from core.renderers.lecture import (
    sanitize_slide_text,
    clean_title_string,
    extract_concise_topic_name,
    get_icon_for_topic,
    detect_file_info_for_tech_stack,
    derive_unified_session_scenario,
    infer_scope_boundary_rules,
    extract_session_summary_bullets,
    render_scene_content_html,
    generate_session_deck_html,
    build_generic_multi_subject_section,
    generate_interactive_visualizer_html
)
from agents.classroom_lecture_generator_agent import classroom_lecture_generator_agent

class TestClassroomLectureRenderersModular(unittest.TestCase):

    def test_text_sanitizer_and_topic_extractor(self):
        """Tests slide text sanitization, title cleaning, and topic icons."""
        sanitized = sanitize_slide_text("bối cảnh thực tế & thách thức kỹ thuật vô cùng tuyệt vời")
        self.assertIn("Bối cảnh dự án & vấn đề cần giải quyết", sanitized)
        self.assertNotIn("vô cùng", sanitized)
        self.assertNotIn("tuyệt vời", sanitized)

        cleaned_title = clean_title_string("Session 02 - Lesson 01: bai_toan_tinh_tong")
        self.assertIn("Bai Toan Tinh Tong", cleaned_title)

        concise = extract_concise_topic_name("Tìm hiểu Toán tử và biểu thức số học nâng cao")
        self.assertIn("Toán tử", concise)

        icon = get_icon_for_topic("Toán tử số học", "Python")
        self.assertEqual(icon, "ph-calculator")

        fname, lang = detect_file_info_for_tech_stack("Python", "Biến số")
        self.assertEqual(fname, "main.py")
        self.assertEqual(lang, "python")

    def test_knowledge_extractor(self):
        """Tests unified scenario derivation and scope boundary inference."""
        scenario = derive_unified_session_scenario("Toán tử và biểu thức số học", "Python")
        self.assertIn("Giỏ hàng & Thanh toán", scenario)

        scope_rules = infer_scope_boundary_rules("Session 02 - Biến và Toán tử", "JavaScript", {})
        self.assertIn("STRICT KNOWLEDGE SCOPE BOUNDARY", scope_rules)

    def test_deck_and_simulation_renderers(self):
        """Tests slide deck generation and interactive simulation builder."""
        lessons_data = [
            {
                "lesson_title": "Toán tử số học cơ bản",
                "scenes": [
                    {
                        "action_title": "Giới thiệu toán tử",
                        "layout_type": "CODE",
                        "code_sample": "let x = 10 + 5;",
                        "bullets": ["Cộng hai số: 10 + 5 = 15."]
                    }
                ]
            }
        ]

        deck_html = generate_session_deck_html(
            session_title="Session 02 - Toán tử",
            module_name="JavaScript",
            lessons_data=lessons_data
        )
        self.assertIn("Session 02", deck_html)
        self.assertIn("Toán tử số học cơ bản", deck_html)

        vis_html = generate_interactive_visualizer_html(
            session_title="Session 02 - Toán tử",
            module_name="JavaScript",
            lessons_data=lessons_data
        )
        self.assertIn("s1", vis_html)
        self.assertIn("run_s1_sim", vis_html)

    def test_facade_agent(self):
        """Tests that classroom_lecture_generator_agent facade delegates correctly."""
        clean = classroom_lecture_generator_agent.clean_title_string("Lesson 01: test_title")
        self.assertEqual(clean, "Test Title")

if __name__ == "__main__":
    unittest.main()
