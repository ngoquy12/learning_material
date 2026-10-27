"""Lệnh verify: verify_path, ghi báo cáo, CLI."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

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
    out = tmp_path / "rep"
    assert _run(valid_course_tree, "--report-dir", out) == 1
    data = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert [r["kind"] for r in data["results"] if r["status"] == "fail"] == ["quiz_lesson"]


def test_kind_forces_gate_on_txt(tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("hello", encoding="utf-8")
    rep = verify_path(f, VerifyOptions(kind="reading"))
    assert [r.kind for r in rep.results] == ["reading"]


def test_unknown_file_in_tree_info_only(valid_course_tree):
    (valid_course_tree / "ghi_chu.txt").write_text("hello", encoding="utf-8")
    rep = verify_path(valid_course_tree, VerifyOptions())
    unknown = [r for r in rep.results if r.kind == "unknown"]
    assert unknown and all(r.status == "unknown" for r in unknown)
    c = rep.counts()
    assert c["unknown"] == len(unknown)
    assert c["pass"] == len(GATES) and c["fail"] == 0 and c["skipped"] == 0
    assert rep.exit_code == 0
    assert "| unknown |" in rep.to_markdown()


def test_single_unknown_file_exit_1(tmp_path, capsys):
    f = tmp_path / "note.txt"
    f.write_text("hello", encoding="utf-8")
    rep = verify_path(f, VerifyOptions())
    assert rep.exit_code == 1
    assert any("--kind" in fd.message for r in rep.results for fd in r.findings if fd.severity == "error")
    assert _run(f, "--report-dir", tmp_path / "rep") == 1


def test_folder_with_only_unknown_files_exit_1(tmp_path):
    d = tmp_path / "linh_tinh"
    d.mkdir()
    (d / "a.txt").write_text("a", encoding="utf-8")
    (d / "b.md").write_text("b", encoding="utf-8")
    rep = verify_path(d, VerifyOptions())
    assert rep.exit_code == 1
    msgs = [fd.message for r in rep.results for fd in r.findings if fd.severity == "error"]
    assert any("Không tìm thấy tài nguyên nào được nhận diện" in m for m in msgs)
    assert _run(d, "--report-dir", tmp_path / "rep") == 1


def test_skipped_gate_exit_2_report_written(valid_course_tree, tmp_path, monkeypatch, capsys):
    from core.harness.findings import GateResult

    monkeypatch.setitem(GATES, "lab", lambda path, opts: GateResult(
        kind="lab", path=str(path), gate="lab", skipped_reason="thiếu công cụ"))
    out = tmp_path / "rep"
    assert _run(valid_course_tree, "--report-dir", out) == 2
    data = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert data["exit_code"] == 2 and data["counts"]["skipped"] == 1
    assert "Bỏ qua [lab]" in capsys.readouterr().out


def test_invalid_kind_rejected(valid_course_tree):
    with pytest.raises(SystemExit) as exc:
        main(["verify", str(valid_course_tree), "--kind", "khong_co"])
    assert exc.value.code == 2


def test_json_stdout_is_pure_json_subprocess(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    fixture = repo / "tests" / "fixtures" / "harness" / "reading_ok.html"
    proc = subprocess.run(
        [sys.executable, "-m", "core.harness", "verify", str(fixture), "--kind", "reading", "--json",
         "--report-dir", str(tmp_path / "rep")],
        cwd=repo, capture_output=True, text=True, encoding="utf-8", timeout=300)
    data = json.loads(proc.stdout)
    assert data["results"][0]["kind"] == "reading"
    assert proc.returncode == data["exit_code"]


def test_report_dir_inside_target_refused(valid_course_tree, capsys):
    inside = valid_course_tree / "bao_cao"
    assert _run(valid_course_tree, "--report-dir", inside) == 1
    assert "bên trong" in capsys.readouterr().err
    assert not inside.exists()


def test_default_report_root_inside_target_falls_back(valid_course_tree, monkeypatch, capsys):
    monkeypatch.setattr("core.harness.report_io.REPORT_ROOT", valid_course_tree / "storage" / "harness_reports")
    assert _run(valid_course_tree) == 0
    assert not (valid_course_tree / "storage").exists()
    last = capsys.readouterr().out.strip().splitlines()[-1]
    rep_dir = Path(last.split(":", 1)[1].strip())
    assert (rep_dir / "report.json").exists()
    assert valid_course_tree.resolve() not in rep_dir.resolve().parents


def test_kind_on_tree_filters_resources(valid_course_tree):
    rep = verify_path(valid_course_tree, VerifyOptions(kind="quiz_lesson"))
    assert [r.kind for r in rep.results if r.kind != "unknown"] == ["quiz_lesson"]
    assert rep.results[0].path.endswith("Quizz lesson")
    assert rep.exit_code == 0


def test_kind_on_tree_without_that_kind_errors(valid_course_tree):
    for lab in valid_course_tree.rglob("lab_guide.md"):
        lab.unlink()
    rep = verify_path(valid_course_tree, VerifyOptions(kind="lab"))
    assert rep.exit_code == 1
    assert [r.kind for r in rep.results if r.status == "fail"] == ["unknown"]


def test_kind_on_single_resource_folder_runs_directly(valid_course_tree):
    qs = next(valid_course_tree.rglob("Quizz session"))
    rep = verify_path(qs, VerifyOptions(kind="quiz_session"))
    assert [(r.kind, r.path) for r in rep.results] == [("quiz_session", str(qs))]
    renamed = qs.parent / "bo_cau_hoi"
    qs.rename(renamed)
    rep = verify_path(renamed, VerifyOptions(kind="quiz_session"))
    assert [(r.kind, r.path) for r in rep.results] == [("quiz_session", str(renamed))]
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
