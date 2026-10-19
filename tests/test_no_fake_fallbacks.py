import unittest
from unittest import mock

from core.exceptions import GenerationError


def _state(**extra):
    state = {
        "session_id": "Session 01", "lesson_id": "Lesson 01", "technology_stack": "Python",
        "core_ssot": {"session_title": "T", "lesson_details": "d", "expected_output": "o"},
        "artifacts_status": {}, "review_logs": [],
    }
    state.update(extra)
    return state


class TestBlueprintNoFake(unittest.TestCase):
    def test_llm_loi_thi_khong_co_blueprint_gia(self):
        from agents.creators import blueprint_creator

        state = _state()
        with mock.patch.object(blueprint_creator, "call_llm", side_effect=RuntimeError("hong")):
            out = blueprint_creator.blueprint_creator_agent(state)
        self.assertNotIn("lesson_blueprint", out)
        self.assertTrue(any(l["source"] == "Blueprint_Creator" for l in out["review_logs"]))


class TestKnowledgeBaseNoFake(unittest.TestCase):
    def test_llm_loi_thi_ssot_trong_va_danh_dau_chua_kiem_chung(self):
        from agents import strategic_agents

        with mock.patch.object(strategic_agents, "call_llm", return_value="khong phai json", create=True), \
             mock.patch.dict("os.environ", {"GEMINI_API_KEY": "", "GOOGLE_API_KEY": "", "OPENAI_API_KEY": "", "LLM_API_KEY": ""}):
            ssot = strategic_agents.knowledge_base_agent({"session_title": "Bien"}, "python/core")
        self.assertEqual(ssot["concepts"], {})
        self.assertEqual(ssot["code_samples"], {})
        self.assertFalse(ssot["course_metadata"]["verified"])
        self.assertEqual(ssot["course_metadata"]["status"], "LOCKED_UNVERIFIED")


class TestMasterContentNoOfflineMock(unittest.TestCase):
    def test_stage1_that_bai_thi_nem_loi(self):
        from agents.creators import common_utils

        state = _state()
        with mock.patch.object(common_utils, "call_llm", return_value="{}"), \
             mock.patch.dict("os.environ", {"GEMINI_API_KEY": "x"}):
            with self.assertRaises(GenerationError):
                common_utils.get_lesson_content("Session 01", "Lesson 01", "T", "d", "o", 1, state["core_ssot"], state=state)
        self.assertNotIn("master_content", state)


class TestExamStatus(unittest.TestCase):
    def test_de_thi_khong_qua_reviewer_khong_duoc_bao_approved(self):
        import tempfile

        from agents import exam_agents

        practical = {"content": "# De"}
        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.object(exam_agents, "exam_practical_creator", return_value=practical), \
             mock.patch.object(exam_agents, "exam_mcq_creator", return_value=[]), \
             mock.patch.object(exam_agents, "exam_oral_questions_creator", return_value="oral"), \
             mock.patch.object(exam_agents, "exam_reviewer_agent", return_value={"status": "REJECTED", "feedback": "thieu"}), \
             mock.patch.object(exam_agents, "generate_and_link_srs_diagram", side_effect=lambda c, *a, **k: c):
            result = exam_agents.generate_exam_session("Session 05", "Thi", tmp, "Python", "", "", True)
        self.assertFalse(result["approved"])
        self.assertEqual(result["review_feedback"], "thieu")

    def test_de_thi_qua_reviewer_duoc_approved(self):
        import tempfile

        from agents import exam_agents

        with tempfile.TemporaryDirectory() as tmp, \
             mock.patch.object(exam_agents, "exam_practical_creator", return_value={"content": "# De"}), \
             mock.patch.object(exam_agents, "exam_mcq_creator", return_value=[]), \
             mock.patch.object(exam_agents, "exam_oral_questions_creator", return_value="oral"), \
             mock.patch.object(exam_agents, "exam_reviewer_agent", return_value={"status": "APPROVED", "feedback": "ok"}), \
             mock.patch.object(exam_agents, "generate_and_link_srs_diagram", side_effect=lambda c, *a, **k: c):
            result = exam_agents.generate_exam_session("Session 05", "Thi", tmp, "Python", "", "", True)
        self.assertTrue(result["approved"])


class TestSessionAssetIsolation(unittest.TestCase):
    def test_loi_mot_buoc_khong_lam_dung_ca_khoa(self):
        from cli.commands.workflow_cmd import _run_session_asset

        summary = []

        def boom(**kw):
            raise RuntimeError("hong")

        self.assertIsNone(_run_session_asset(summary, "Session 03", "Sơ đồ tư duy", boom, session_id="Session 03"))
        self.assertEqual(len(summary), 1)
        self.assertIn("FAILED", summary[0]["status"])

    def test_thanh_cong_tra_ket_qua(self):
        from cli.commands.workflow_cmd import _run_session_asset

        summary = []
        self.assertEqual(_run_session_asset(summary, "S", "x", lambda **kw: kw["a"], a=5), 5)
        self.assertEqual(summary, [])


if __name__ == "__main__":
    unittest.main()
