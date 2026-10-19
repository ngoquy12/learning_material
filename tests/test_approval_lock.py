import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from core import approvals, paths


class _IsolatedStorage(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._old = os.environ.get("STORAGE_DIR")
        os.environ["STORAGE_DIR"] = self._tmp.name
        paths.reset_path_cache()

    def tearDown(self):
        if self._old is None:
            os.environ.pop("STORAGE_DIR", None)
        else:
            os.environ["STORAGE_DIR"] = self._old
        paths.reset_path_cache()
        self._tmp.cleanup()

    def _state(self, **extra):
        state = {"course_key": "MonA", "session_id": "Session 02", "lesson_id": "Lesson 01",
                 "technology_stack": "Python", "artifacts_status": {}, "review_logs": []}
        state.update(extra)
        return state


class TestLockLookup(_IsolatedStorage):
    def test_khoa_khoa_hoc_dung_chung_voi_cli(self):
        self.assertEqual(approvals.course_key_from_pm("documents/PM_Generated_MonA_Updated.xlsx"), "MonA")

    def test_chua_duyet_thi_khong_khoa(self):
        self.assertFalse(approvals.is_state_artifact_locked(self._state(), "html"))

    def test_da_duyet_thi_khoa_dung_tai_nguyen_dung_bai(self):
        approvals.record_approval("html", "Nguyen Van A", course="MonA", session_id="Session 02", lesson_id="Lesson 01")
        self.assertTrue(approvals.is_state_artifact_locked(self._state(), "html"))
        self.assertFalse(approvals.is_state_artifact_locked(self._state(), "quiz"))
        self.assertFalse(approvals.is_state_artifact_locked(self._state(lesson_id="Lesson 02"), "html"))
        self.assertFalse(approvals.is_state_artifact_locked(self._state(course_key="MonB"), "html"))

    def test_approve_khong_kem_pm_van_khoa(self):
        approvals.record_approval("html", "A", course="", session_id="Session 02", lesson_id="Lesson 01")
        self.assertTrue(approvals.is_state_artifact_locked(self._state(), "html"))

    def test_force_mo_khoa(self):
        approvals.record_approval("html", "Nguyen Van A", course="MonA", session_id="Session 02", lesson_id="Lesson 01")
        self.assertFalse(approvals.is_state_artifact_locked(self._state(force_rebuild=True), "html"))

    def test_tu_choi_thi_khong_khoa(self):
        approvals.record_approval("html", "A", course="MonA", session_id="Session 02", lesson_id="Lesson 01")
        approvals.record_approval("html", "A", course="MonA", session_id="Session 02", lesson_id="Lesson 01",
                                  decision=approvals.DECISION_REJECTED)
        self.assertFalse(approvals.is_state_artifact_locked(self._state(), "html"))


class TestLockEnforced(_IsolatedStorage):
    def test_artifact_writer_khong_ghi_de_ban_da_duyet(self):
        from core.artifact_writer import write_state_artifacts_to_disk

        approvals.record_approval("html", "A", course="MonA", session_id="Session 02", lesson_id="Lesson 01")
        with tempfile.TemporaryDirectory() as tmp:
            lesson_dir = Path(tmp)
            (lesson_dir / "Bài đọc").mkdir()
            target = lesson_dir / "Bài đọc" / "reading.html"
            target.write_text("BAN DA DUYET", encoding="utf-8")
            state = self._state(html_content="BAN MOI", requested_parts=["html"])
            written = write_state_artifacts_to_disk(state, lesson_dir=lesson_dir)
            self.assertEqual(target.read_text(encoding="utf-8"), "BAN DA DUYET")
            self.assertEqual(written["html"], "Locked")

    def test_artifact_writer_van_ghi_khi_chua_duyet(self):
        from core.artifact_writer import write_state_artifacts_to_disk

        with tempfile.TemporaryDirectory() as tmp:
            lesson_dir = Path(tmp)
            state = self._state(html_content="BAN MOI", requested_parts=["html"])
            write_state_artifacts_to_disk(state, lesson_dir=lesson_dir)
            self.assertEqual((lesson_dir / "Bài đọc" / "reading.html").read_text(encoding="utf-8"), "BAN MOI")

    def test_pipeline_khong_sinh_lai_tai_nguyen_da_duyet(self):
        from core import graph

        approvals.record_approval("html", "A", course="MonA", session_id="Session 02", lesson_id="Lesson 01")
        writer = mock.Mock()
        fn = getattr(graph.pipeline_html_production, "func", graph.pipeline_html_production)
        with mock.patch.object(graph, "html_writer_agent", writer):
            out = fn(self._state())
        writer.assert_not_called()
        self.assertEqual(out["artifacts_status"]["html"], graph.ArtifactStatus.APPROVED)

    def test_force_van_sinh_lai(self):
        from core import graph

        approvals.record_approval("html", "A", course="MonA", session_id="Session 02", lesson_id="Lesson 01")
        calls = {"n": 0}

        def fake_writer(state):
            calls["n"] += 1
            state["html_content"] = "<html></html>"
            return state

        fn = getattr(graph.pipeline_html_production, "func", graph.pipeline_html_production)
        with mock.patch.object(graph, "html_writer_agent", fake_writer), \
             mock.patch.object(graph, "html_ux_reviewer", lambda s: {"status": "APPROVED", "feedback": ""}), \
             mock.patch.object(graph, "write_state_artifacts_to_disk", lambda s: None), \
             mock.patch.object(graph, "save_state_checkpoint", lambda s: None):
            fn(self._state(force_rebuild=True))
        self.assertGreaterEqual(calls["n"], 1)


class TestNoPlaceholderOverwrite(_IsolatedStorage):
    def test_sinh_loi_thi_ban_cu_con_nguyen(self):
        from agents.creators import reading_creator

        with tempfile.TemporaryDirectory() as tmp:
            lesson_dir = Path(tmp)
            (lesson_dir / "Bài đọc").mkdir()
            target = lesson_dir / "Bài đọc" / "reading.html"
            target.write_text("BAN CU", encoding="utf-8")
            state = self._state(core_ssot={"session_title": "T"})
            with mock.patch("agents.creator_agents.get_lesson_dir", return_value=lesson_dir), \
                 mock.patch.object(reading_creator, "generate_reading_html", side_effect=RuntimeError("loi LLM")):
                with self.assertRaises(RuntimeError):
                    reading_creator.html_writer_agent(state)
            self.assertEqual(target.read_text(encoding="utf-8"), "BAN CU")


if __name__ == "__main__":
    unittest.main()
