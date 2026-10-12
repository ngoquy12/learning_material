import tempfile
import unittest
from pathlib import Path

from scripts import check_exercise_scope as cli

STARTER = """// ===== Mã nền (không sửa) =====
const fake = { run() { return this.x; } };
// ===== HẾT MÃ NỀN =====
function solve() { return 1; }
"""
SOLUTION = """const fake = { run() { return this.x; } };
function solve() { return 2; }
"""


class TestCli(unittest.TestCase):
    def _course(self, solution):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        s = root / "Session 01" / "Bai tap" / "1_co_ban"
        (s / "starter").mkdir(parents=True)
        (s / "starter" / "script.js").write_text(STARTER, encoding="utf-8")
        sol = root / "Session 01" / "Bai tap" / "tai_lieu_giang_vien" / "dap_an_mau" / "bai_1"
        sol.mkdir(parents=True)
        (sol / "script.js").write_text(solution, encoding="utf-8")
        return tmp, root

    def test_ma_nen_cua_starter_va_dap_an_khong_tinh(self):
        tmp, root = self._course(SOLUTION)
        with tmp:
            self.assertEqual(cli.main([str(root), "--forbid", "this", "--no-drift"]), 0)

    def test_bai_lam_dung_this_bi_bat(self):
        tmp, root = self._course(SOLUTION.replace("return 2;", "return this.y;"))
        with tmp:
            self.assertEqual(cli.main([str(root), "--forbid", "this", "--no-drift"]), 1)


if __name__ == "__main__":
    unittest.main()
