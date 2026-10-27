"""Lệnh con init, plan, status, next của `python -m core.harness` (spec 4.4)."""
from __future__ import annotations

import copy
import json
import os
import time

import pytest

from core.harness import state as st
from core.harness.cli import main
from core.harness.findings import Finding, GateResult, Report
from tests.harness._course_spec_samples import VALID, make_course_tree, write_yaml
from tests.harness.conftest import write_tree


@pytest.fixture(autouse=True)
def _state_root(tmp_path, monkeypatch):
    monkeypatch.setattr(st, "STATE_ROOT", tmp_path / "state_root")


def _report(code, msg="loi"):
    findings = [Finding("error", "k", msg)] if code == 1 else []
    return Report("p", [GateResult("k", "p", "k", findings=findings)], "t")


def _course(tmp_path, data=None):
    data = copy.deepcopy(data or VALID)
    course = make_course_tree(tmp_path, data)
    spec = write_yaml(course, data)
    for lesson in ("Lesson 01 - Tong quan", "Lesson 02 - Chi tiet"):
        p = course / "Session 01 - Ly thuyet" / lesson / "Bai doc"
        p.mkdir(parents=True)
        (p / "reading.html").write_text("<html>x</html>", encoding="utf-8")
    return course, spec


@pytest.fixture
def fake_verify(monkeypatch):
    calls = []

    def fake(target, opts):
        calls.append((target, opts))
        return _report(0)

    monkeypatch.setattr(st, "verify_path", fake)
    return calls


def test_init_writes_then_refuses_without_force(tmp_path, capsys):
    course = tmp_path / "mon_demo"
    write_tree(course, {"Session 01 - Ly thuyet/Lesson 01 - A/Bai doc/reading.html": "x"})
    assert main(["init", str(course)]) == 0
    out = capsys.readouterr().out
    assert "course_spec.yaml" in out and (course / "course_spec.yaml").is_file()
    assert sorted(p.name for p in course.iterdir()) == ["Session 01 - Ly thuyet", "course_spec.yaml"]
    assert main(["init", str(course)]) == 1
    err = capsys.readouterr().err
    assert "--force" in err and "Traceback" not in err
    assert main(["init", str(course), "--force"]) == 0
    assert not (course / "course_spec.yaml.tmp").exists()


@pytest.mark.parametrize("make", ["missing", "no_session"])
def test_init_errors_exit_1(tmp_path, capsys, make):
    course = tmp_path / "mon"
    if make == "no_session":
        course.mkdir()
    assert main(["init", str(course)]) == 1
    err = capsys.readouterr().err
    assert err.strip() and "Traceback" not in err


def test_plan_json_and_text(tmp_path, capsys):
    _, spec = _course(tmp_path)
    assert main(["plan", str(spec), "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data and all({"id", "wave", "depends_on"} <= set(t) for t in data)
    by_id = {t["id"]: t for t in data}
    assert by_id["s01/l01/reading"]["wave"] == 1
    assert by_id["s01/quiz_session"]["depends_on"] == ["s01/l01/reading", "s01/l02/reading"]
    assert main(["plan", str(spec)]) == 0
    text = capsys.readouterr().out
    assert "[1] s01/l01/reading" in text and "←" in text


def test_status_exit_3_and_json(tmp_path, capsys, fake_verify):
    _, spec = _course(tmp_path)
    assert main(["status", str(spec)]) == 3
    out = capsys.readouterr().out
    assert "missing" in out and "[missing] s01/quiz_session" in out
    assert str(st.state_path("demo")) in out and "Trạng thái tính lúc" in out
    assert main(["status", str(spec), "--json"]) == 3
    data = json.loads(capsys.readouterr().out)
    assert data["counts"]["done"] == 2 and data["counts"]["missing"] > 0
    assert data["exit_code"] == 3
    assert st.load_state("demo") is not None


def test_status_failed_exit_1_shows_first_error(tmp_path, capsys, monkeypatch):
    _, spec = _course(tmp_path)
    monkeypatch.setattr(st, "verify_path", lambda t, o: _report(1, "thiếu mục 3"))
    assert main(["status", str(spec)]) == 1
    assert "thiếu mục 3" in capsys.readouterr().out


def test_status_runtime_passed(tmp_path, fake_verify):
    course, spec = _course(tmp_path)
    ex = course / "Session 01 - Ly thuyet" / "Bai tap" / "1_a"
    ex.mkdir(parents=True)
    (ex / "x.txt").write_text("x", encoding="utf-8")
    main(["status", str(spec), "--runtime"])
    seen = {o.kind: o.runtime for _, o in fake_verify}
    assert seen["exercise"] is True and seen["reading"] is False


def test_next_limit_json_block(tmp_path, capsys, fake_verify):
    course, spec = _course(tmp_path)
    assert main(["next", str(spec), "--limit", "1", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["updated_at"] == st.load_state("demo").updated_at
    [block] = data["tasks"]
    assert block["skill"].startswith("skills/") and block["skill"].endswith("/SKILL.md")
    assert "--kind" in block["verify_command"]
    assert block["wave"] == 2  # các reading đã done, đợt 2 là đợt sẵn sàng đầu tiên
    assert os.path.isabs(block["target"])
    for key in ("id", "kind", "status", "depends_on", "notes", "allowed", "forbidden", "first_error"):
        assert key in block


def test_next_blocks_fields(tmp_path, capsys, fake_verify):
    data = copy.deepcopy(VALID)
    data["notes"] = "course_spec.md"
    data["sessions"][0]["lessons"][0]["allowed"] = ["biến"]
    data["sessions"][0]["lessons"][0]["forbidden"] = ["class"]
    course, spec = _course(tmp_path, data)
    (course / "Session 01 - Ly thuyet" / "Lesson 01 - Tong quan" / "Bai doc" / "reading.html").unlink()
    assert main(["next", str(spec), "--json"]) == 0
    blocks = {b["id"]: b for b in json.loads(capsys.readouterr().out)["tasks"]}
    reading = blocks["s01/l01/reading"]
    assert reading["skill"] == "skills/reading_generator/SKILL.md"
    assert reading["allowed"] == ["biến"] and reading["forbidden"] == ["class"]
    assert reading["notes"] == str((course / "course_spec.md").resolve())
    assert reading["verify_command"].startswith("python -m core.harness verify \"")
    assert reading["verify_command"].endswith("--kind reading")
    assert reading["target"].endswith("reading.html") and os.path.isabs(reading["target"])
    rq = blocks["s01/l02/reading_questions"]
    assert rq["verify_command"] == "" and rq["verify_note"]
    assert "s01/l01/quiz_lesson" not in blocks  # chờ reading của lesson 01
    ex = blocks["s01/exercise_1"] if "s01/exercise_1" in blocks else None
    assert ex is None  # chờ mọi reading của session 01


def test_next_runtime_flag_for_exercise(tmp_path, capsys, fake_verify):
    data = copy.deepcopy(VALID)
    data["sessions"] = data["sessions"][:1]
    course, spec = _course(tmp_path, data)
    assert main(["next", str(spec), "--json"]) == 0
    blocks = {b["id"]: b for b in json.loads(capsys.readouterr().out)["tasks"]}
    assert blocks["s01/exercise_1"]["verify_command"].endswith("--kind exercise --runtime")
    assert blocks["s01/slide_html"]["verify_command"].endswith("--kind slide_html --runtime")
    assert blocks["s01/quiz_session"]["verify_command"].endswith("--kind quiz_session")


def test_next_text_output(tmp_path, capsys, fake_verify):
    _, spec = _course(tmp_path)
    assert main(["next", str(spec), "--limit", "2"]) == 0
    out = capsys.readouterr().out
    assert out.count("skills/") == 2 and "python -m core.harness verify" in out
    assert "Trạng thái tính lúc" in out


def test_next_recomputes_by_default(tmp_path, capsys, fake_verify):
    _, spec = _course(tmp_path)
    main(["next", str(spec), "--json"])
    first = len(fake_verify)
    assert first > 0 and st.load_state("demo") is not None
    main(["next", str(spec), "--json"])
    assert len(fake_verify) == 2 * first  # mặc định luôn tính lại
    capsys.readouterr()


def test_next_cached_reuses_and_recomputes_when_stale(tmp_path, capsys, fake_verify):
    _, spec = _course(tmp_path)
    main(["next", str(spec), "--cached", "--json"])  # chưa có state.json: tính
    first = len(fake_verify)
    assert first > 0 and st.load_state("demo") is not None
    main(["next", str(spec), "--cached", "--json"])
    assert len(fake_verify) == first  # dùng state.json
    future = time.time() + 120
    os.utime(spec, (future, future))
    main(["next", str(spec), "--cached", "--json"])
    assert len(fake_verify) > first  # đặc tả mới hơn: tính lại
    count = len(fake_verify)
    snap = st.load_state("demo")
    snap.course_id = "khac"
    st.state_path("demo").write_text(snap.to_json(), encoding="utf-8")
    main(["next", str(spec), "--cached", "--json"])
    assert len(fake_verify) > count
    capsys.readouterr()


@pytest.mark.parametrize("cmd", ["status", "next"])
def test_save_state_oserror_exit_1(tmp_path, capsys, fake_verify, monkeypatch, cmd):
    _, spec = _course(tmp_path)

    def denied(snap):
        raise PermissionError(13, "Access is denied")

    monkeypatch.setattr(st, "save_state", denied)
    assert main([cmd, str(spec), "--json"]) == 1
    captured = capsys.readouterr()
    assert "Không ghi được tệp trạng thái" in captured.err
    assert "Traceback" not in captured.err + captured.out and captured.out == ""


@pytest.mark.parametrize("cmd", [["plan"], ["status"], ["next"], ["status", "--json"]])
def test_bad_spec_exit_1_with_location(tmp_path, capsys, cmd):
    data = copy.deepcopy(VALID)
    data["sessions"][1]["lessons"] = [{"folder": "L", "resources": ["khong_co"]}]
    course = make_course_tree(tmp_path, data)
    spec = write_yaml(course, data)
    assert main([cmd[0], str(spec), *cmd[1:]]) == 1
    captured = capsys.readouterr()
    assert "sessions[1].lessons[0].resources" in captured.err
    assert "Traceback" not in captured.err + captured.out
    assert captured.out == ""


def test_missing_spec_exit_1(tmp_path, capsys):
    assert main(["status", str(tmp_path / "khong_co.yaml")]) == 1
    err = capsys.readouterr().err
    assert err.strip() and "Traceback" not in err


def test_limit_must_be_positive(tmp_path):
    _, spec = _course(tmp_path)
    with pytest.raises(SystemExit):
        main(["next", str(spec), "--limit", "0"])


def test_compute_oserror_not_labelled_as_write(tmp_path, capsys, fake_verify, monkeypatch):
    _, spec = _course(tmp_path)

    def boom(*a, **k):
        raise PermissionError(13, "Access is denied")

    monkeypatch.setattr(st, "build_tasks", boom)
    assert main(["status", str(spec)]) == 1
    err = capsys.readouterr().err
    assert "Không đọc được thư mục môn" in err and "Không ghi được" not in err


def test_next_missing_pattern_target_has_rename_note(tmp_path, capsys, fake_verify):
    _, spec = _course(tmp_path)
    main(["next", str(spec), "--json"])
    tasks = json.loads(capsys.readouterr().out)["tasks"]
    ex = [t for t in tasks if t["kind"] == "exercise"]
    assert ex and all("đổi đường dẫn sau khi tạo" in t["verify_note"] and t["verify_command"] for t in ex)
    assert all(t["verify_note"] == "" for t in tasks if t["kind"] == "reading")
