"""Nạp core.llm không được in gì ra stdout (stdout của CLI dành cho kết quả, vd. --json)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def test_import_core_llm_keeps_stdout_clean():
    proc = subprocess.run([sys.executable, "-c", "import core.llm"], cwd=str(REPO),
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "", proc.stdout
