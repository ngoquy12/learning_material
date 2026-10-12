import unittest
from unittest import mock

from core.memory_context import learnable_review_logs, memory_prompt_block


class TestMemoryBlock(unittest.TestCase):
    def test_rong_khi_chua_co_kinh_nghiem(self):
        self.assertEqual(memory_prompt_block({}), "")

    def test_cat_theo_do_dai(self):
        state = {"lessons_learned_prompt": "\n".join(f"quy tắc {i}" for i in range(500))}
        self.assertLessEqual(len(memory_prompt_block(state)), 1600)


class TestLearnableLogs(unittest.TestCase):
    def test_chi_giu_reviewer_noi_dung(self):
        logs = [
            {"source": "UX_Reviewer", "feedback": "Thiếu sơ đồ"},
            {"source": "Scope_Gate", "feedback": "dùng decorator"},
            {"source": "Batch_Executor", "feedback": "Traceback"},
            {"source": "Sandbox_Agent", "feedback": ""},
            {"source": "Academic_Reviewer", "feedback": "X không trả về phán quyết đọc được"},
        ]
        self.assertEqual([l["source"] for l in learnable_review_logs(logs)], ["UX_Reviewer"])


class TestCreatorsReceiveMemory(unittest.TestCase):
    def test_quiz_prompt_chua_kinh_nghiem(self):
        from agents.creators import quiz_creator

        captured = {}

        def fake_llm(system, user, **kw):
            captured["user"] = user
            return "[]"

        state = {
            "session_id": "S1", "lesson_id": "L1", "technology_stack": "Python",
            "core_ssot": {"session_title": "T"}, "html_content": "<p>x</p>",
            "lesson_content": {"problem": "p"},
            "lessons_learned_prompt": "QUY TAC DA HOC XYZ",
        }
        with mock.patch.object(quiz_creator, "call_llm", fake_llm):
            with self.assertRaises(Exception):
                quiz_creator.quiz_agent(state)
        self.assertIn("QUY TAC DA HOC XYZ", captured["user"])


if __name__ == "__main__":
    unittest.main()
