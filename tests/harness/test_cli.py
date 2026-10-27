"""Lệnh verify: verify_path, ghi báo cáo, CLI."""
from __future__ import annotations

import json

import pytest

from core.harness.gates import GATES
from core.harness.report_io import write_report
from core.harness.verify import VerifyOptions, main, verify_path


def _run(*args):
    return main(["verify", *map(str, args)])


def test_clean_tree_exit_0_and_report(valid_course_tree, tmp_path):
    out = tmp_path / "rep"
    assert _run(valid_course_tree, "--report-dir", out) == 0
    data = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert {r["kind"] for r in data["results"]} == set(GATES)
    assert (out / "report.md").exists()


def test_broken_quiz_exit_1(valid_course_tree, tmp_path):
    q = next(valid_course_tree.rglob("quiz.md"))
    q.write_text("# rong\n", encoding="utf-8")
    assert _run(valid_course_tree, "--report-dir", tmp_path / "rep") == 1


def test_kind_forces_gate_on_txt(tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("hello", encoding="utf-8")
    rep = verify_path(f, VerifyOptions(kind="reading"))
    assert [r.kind for r in rep.results] == ["reading"]


def test_unknown_file_info_only(tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("hello", encoding="utf-8")
    rep = verify_path(f, VerifyOptions())
    assert rep.results[0].kind == "unknown"
    assert rep.exit_code == 0


def test_gate_exception_isolated(valid_course_tree, tmp_path, monkeypatch):
    def boom(path, opts):
        raise RuntimeError("no")

    monkeypatch.setitem(GATES, "lab", boom)
    out = tmp_path / "rep"
    assert _run(valid_course_tree, "--report-dir", out) == 1
    data = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert {r["kind"] for r in data["results"]} == set(GATES)
    lab = next(r for r in data["results"] if r["kind"] == "lab")
    assert "Cổng lỗi" in lab["findings"][0]["message"]


def test_missing_path(tmp_path, capsys):
    assert _run(tmp_path / "khong_co") == 1
    assert "Traceback" not in capsys.readouterr().err


def test_bad_args():
    with pytest.raises(SystemExit):
        main(["bogus"])
    with pytest.raises(SystemExit):
        main(["verify"])


def test_json_output(valid_course_tree, tmp_path, capsys):
    assert _run(valid_course_tree, "--json", "--report-dir", tmp_path / "r") == 0
    assert json.loads(capsys.readouterr().out)["exit_code"] == 0


def test_default_report_dir_outside_tree(tmp_path, monkeypatch):
    monkeypatch.setattr("core.harness.report_io.REPORT_ROOT", tmp_path / "reports")
    tree = tmp_path / "Mon Hoc Đẹp"
    tree.mkdir()
    d = write_report(verify_path(tree, VerifyOptions()))
    assert d.parent == tmp_path / "reports"
    assert d.name.endswith("_mon_hoc_dep")
    assert (d / "report.json").exists()
