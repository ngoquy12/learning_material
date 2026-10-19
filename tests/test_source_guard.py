import tempfile
import unittest
import unittest.mock
from pathlib import Path

from core import source_guard as sg


class TestSourceGuard(unittest.TestCase):
    def _repo(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "core").mkdir()
        (root / "core" / "a.py").write_text("x = 1\n", encoding="utf-8")
        (root / "skills").mkdir()
        (root / "skills" / "s.md").write_text("skill\n", encoding="utf-8")
        (root / "output").mkdir()
        (root / "output" / "bai.html").write_text("<p>1</p>", encoding="utf-8")
        (root / "main.py").write_text("print(1)\n", encoding="utf-8")
        return tmp, root

    def test_khong_doi_thi_sach(self):
        tmp, root = self._repo()
        with tmp:
            guard = sg.SourceGuard.start(root)
            self.assertFalse(guard.check().any)

    def test_ghi_vao_output_khong_tinh(self):
        tmp, root = self._repo()
        with tmp:
            guard = sg.SourceGuard.start(root)
            (root / "output" / "bai.html").write_text("<p>2</p>", encoding="utf-8")
            (root / "output" / "moi.html").write_text("moi", encoding="utf-8")
            self.assertFalse(guard.check().any)

    def test_sua_them_xoa_vung_cam_bi_bat(self):
        tmp, root = self._repo()
        with tmp:
            guard = sg.SourceGuard.start(root)
            (root / "core" / "a.py").write_text("x = 2\n", encoding="utf-8")
            (root / "core" / "b.py").write_text("y = 1\n", encoding="utf-8")
            (root / "skills" / "s.md").unlink()
            (root / "main.py").write_text("print(2)\n", encoding="utf-8")
            c = guard.check()
            self.assertEqual(c.modified, ["core/a.py", "main.py"])
            self.assertEqual(c.added, ["core/b.py"])
            self.assertEqual(c.removed, ["skills/s.md"])
            self.assertIn("core/b.py", c.summary())

    def test_crlf_khong_tinh_la_sua(self):
        tmp, root = self._repo()
        with tmp:
            guard = sg.SourceGuard.start(root)
            (root / "core" / "a.py").write_bytes(b"x = 1\r\n")
            self.assertFalse(guard.check().any)

    def test_pycache_bi_bo_qua(self):
        tmp, root = self._repo()
        with tmp:
            guard = sg.SourceGuard.start(root)
            (root / "core" / "__pycache__").mkdir()
            (root / "core" / "__pycache__" / "a.cpython-314.pyc").write_bytes(b"\x00")
            self.assertFalse(guard.check().any)

    def test_luu_va_doi_chieu_anh_chup(self):
        tmp, root = self._repo()
        with tmp:
            snap = root / "snap.json"
            sg.save_snapshot(snap, root)
            (root / "core" / "a.py").write_text("x = 3\n", encoding="utf-8")
            self.assertEqual(sg.verify_snapshot(snap, root).modified, ["core/a.py"])


class TestLessonsLearnedNoLongerWritesSkill(unittest.TestCase):
    def test_khong_ghi_vao_skills(self):
        import hashlib

        skill = Path(__file__).resolve().parent.parent / "skills" / "lessons_learned" / "SKILL.md"
        before = hashlib.sha1(skill.read_bytes()).hexdigest() if skill.exists() else None

        import os
        import tempfile

        from agents.lessons_learned_agent import lessons_learned_agent
        from core import paths

        with tempfile.TemporaryDirectory() as tmp:
            old = os.environ.get("STORAGE_DIR")
            os.environ["STORAGE_DIR"] = tmp
            paths.reset_path_cache()
            try:
                state = {
                    "session_id": "S1", "lesson_id": "L1", "technology_stack": "Python",
                    "core_ssot": {"session_title": "T"},
                    "review_logs": [{"source": "UX_Reviewer", "feedback": "Thiếu sơ đồ"}],
                }
                with unittest.mock.patch.dict(os.environ, {"GEMINI_API_KEY": "", "GOOGLE_API_KEY": "", "OPENAI_API_KEY": "", "LLM_API_KEY": ""}):
                    lessons_learned_agent(state)
                written = list(Path(tmp).rglob("SKILL.md"))
            finally:
                if old is None:
                    os.environ.pop("STORAGE_DIR", None)
                else:
                    os.environ["STORAGE_DIR"] = old
                paths.reset_path_cache()

        after = hashlib.sha1(skill.read_bytes()).hexdigest() if skill.exists() else None
        self.assertEqual(before, after)
        self.assertTrue(written, "luật tự học phải được ghi vào storage/")


if __name__ == "__main__":
    import unittest.mock  # noqa: F401
    unittest.main()
