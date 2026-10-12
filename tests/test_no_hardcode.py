import subprocess
import sys
import unittest
from unittest import mock

from agents.creators.quiz_creator import extract_lang_tag


class TestLangTag(unittest.TestCase):
    def test_khop_theo_tu_nguyen_ven(self):
        self.assertEqual(extract_lang_tag("MongoDB"), "mongodb")
        self.assertEqual(extract_lang_tag("Algorithm design"), "algorithmdesign")
        self.assertEqual(extract_lang_tag("Tests"), "tests")

    def test_cong_nghe_thuong_gap(self):
        self.assertEqual(extract_lang_tag("Python 3.11"), "python")
        self.assertEqual(extract_lang_tag("Node.js/Express"), "javascript")
        self.assertEqual(extract_lang_tag("C++"), "cpp")
        self.assertEqual(extract_lang_tag("TypeScript/NestJS"), "typescript")

    def test_rong_khong_mac_dinh_ve_python(self):
        self.assertEqual(extract_lang_tag(""), "text")


class TestStableDomainHash(unittest.TestCase):
    def test_ket_qua_on_dinh_giua_cac_lan_chay(self):
        code = (
            "from core.domain_knowledge import get_domain_for_session as g;"
            "print(g('', 'Tiêu đề không có số')['domain_id'])"
        )
        outs = {
            subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True, text=True, encoding="utf-8",
                env={**__import__("os").environ, "PYTHONHASHSEED": seed, "PYTHONIOENCODING": "utf-8"},
            ).stdout.strip().splitlines()[-1]
            for seed in ("1", "2", "3")
        }
        self.assertEqual(len(outs), 1, outs)


class TestSandboxLanguage(unittest.TestCase):
    def test_ma_javascript_khong_bi_chay_bang_python(self):
        from agents import reviewer_agents

        state = {
            "session_id": "S1", "lesson_id": "L1", "technology_stack": "JavaScript",
            "html_content": '<pre><code class="language-javascript">const a = 1; console.log(a);</code></pre>',
            "quiz_json": [], "core_ssot": {},
        }
        with mock.patch("core.sandbox.execute_code_safely") as run, \
             mock.patch.object(reviewer_agents, "call_llm", return_value='{"status": "APPROVED", "feedback": ""}'), \
             mock.patch.dict("os.environ", {"GEMINI_API_KEY": "x"}):
            reviewer_agents.sandbox_testing_agent(state)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()


class TestPmUpdaterImport(unittest.TestCase):
    def test_rule_fixer_chay_khong_loi_import(self):
        import json

        from agents.reviewer_agents import apply_smart_pedagogical_rule_fixes

        out = apply_smart_pedagogical_rule_fixes(json.dumps([{"title": "S", "lessons": []}]), "Python")
        self.assertIsInstance(out, str)
        self.assertIsInstance(json.loads(out), list)
