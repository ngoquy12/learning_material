"""
tests/test_domain_unification.py
Unit tests verifying 100% Domain Consistency & Anchor Domain Resolution across Session Resources.
"""

import unittest
from core.domain_knowledge import (
    BUSINESS_DOMAINS,
    get_domain_for_session,
    get_domain_blueprint,
    format_domain_rules_for_prompt
)
from agents.creators.homework_creator import generate_homework_exercise

class TestDomainUnification(unittest.TestCase):
    def test_deterministic_domain_resolution(self):
        """Test that get_domain_for_session returns consistent deterministic domain."""
        dom17_a = get_domain_for_session("Session 17", "DOM Interaction")
        dom17_b = get_domain_for_session("Session 17", "DOM Interaction")
        self.assertEqual(dom17_a["domain_id"], dom17_b["domain_id"])

        dom19_a = get_domain_for_session("Session 19", "Event Handling")
        dom19_b = get_domain_for_session("Session 19", "Event Handling")
        self.assertEqual(dom19_a["domain_id"], dom19_b["domain_id"])

    def test_explicit_domain_override(self):
        """Test that explicit default_domain overrides deterministic mapping."""
        dom = get_domain_for_session("Session 17", default_domain="GRAB_RIDE")
        self.assertEqual(dom["domain_id"], "GRAB_RIDE")

    def test_domain_prompt_formatting(self):
        """Test that domain prompt formatting contains required business rules and entities."""
        dom = get_domain_blueprint("SHOPEE_FOOD")
        prompt_block = format_domain_rules_for_prompt(dom)
        self.assertIn("SHOPEE_FOOD", prompt_block)
        self.assertIn("Bối cảnh thực tế", prompt_block)
        self.assertIn("Các quy tắc nghiệp vụ", prompt_block)

    def test_single_homework_exercise_domain_adherence(self):
        """Test generating single exercise with specified unified domain."""
        ex = generate_homework_exercise(
            session_id="Session 17",
            session_title="DOM Interaction",
            tech_stack="javascript/web",
            previous_lessons_text="DOM API basics",
            idx=1,
            level_name="Mức độ 1: Cơ bản - Debug lỗi",
            chosen_domain="EV_CHARGING_STATION",
            forbidden_scope="No Async/Await",
            total_exercises=15
        )
        self.assertEqual(ex["chosen_domain"], "EV_CHARGING_STATION")
        self.assertIn("Mục tiêu", ex["de_bai_content"])
        self.assertIn("Tiêu chuẩn Đánh giá", ex["tieu_chi_content"])

if __name__ == "__main__":
    unittest.main()
