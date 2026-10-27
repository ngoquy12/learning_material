import copy

import pytest

from core.harness import state as st
from core.harness.findings import Finding, GateResult, Report
from core.harness.state import (StateSnapshot, TaskState, compute_status, load_state,
                                ready_tasks, save_state, status_exit_code)
from tests.harness._course_spec_samples import VALID, make_course_tree, write_yaml


def _data():
    data = copy.deepcopy(VALID)
    data["sessions"] = data["sessions"][:1]
    data["sessions"][0]["resources"] = ["slide_html", "exercises"]
    data["sessions"][0]["exercises"] = 1
    return data


def _course(tmp_path):
    data = _data()
    course = make_course_tree(tmp_path, data)
    spec = write_yaml(course, data)
    for lesson in ("Lesson 01 - Tong quan", "Lesson 02 - Chi tiet"):
        p = course / "Session 01 - Ly thuyet" / lesson / "Bai doc"
        p.mkdir(parents=True)
        (p / "reading.html").write_text("<html>x</html>", encoding="utf-8")
    return course, spec


def _report(code, msg="loi"):
    if code == 0:
        res = GateResult("k", "p", "k")
    elif code == 1:
        res = GateResult("k", "p", "k", findings=[Finding("error", "k", msg)])
    else:
        res = GateResult("k", "p", "k", skipped_reason="thiếu công cụ")
    return Report("p", [res], "t")


def test_status_mapping_and_blocked_not_unlocking(tmp_path):
    course, spec = _course(tmp_path)

    def fake(target, opts):
        return _report(0 if "Lesson 01" in str(target) else 1)

    snap = compute_status(spec, verify=fake)
    assert snap.tasks["s01/l01/reading"].status == "done"
    assert snap.tasks["s01/l02/reading"].status == "failed"
    assert snap.tasks["s01/l02/reading"].first_error == "loi"
    assert snap.tasks["s01/slide_html"].status == "missing"

    snap = compute_status(spec, verify=lambda t, o: _report(2))
    assert snap.tasks["s01/l01/reading"].status == "blocked_tool"
    ids = [t.id for t in ready_tasks(snap)]
    assert ids == ["s01/l01/reading", "s01/l02/reading"]  # phụ thuộc chưa mở khóa


def test_empty_file_is_missing(tmp_path):
    course, spec = _course(tmp_path)
    (course / "Session 01 - Ly thuyet" / "Lesson 01 - Tong quan" / "Bai doc" / "reading.html").write_text("")
    snap = compute_status(spec, verify=lambda t, o: _report(0))
    assert snap.tasks["s01/l01/reading"].status == "missing"
    assert snap.tasks["s01/l02/reading"].status == "done"


def test_verify_exception_failed(tmp_path):
    _, spec = _course(tmp_path)

    def boom(t, o):
        raise RuntimeError("hỏng rồi")

    snap = compute_status(spec, verify=boom)
    t = snap.tasks["s01/l01/reading"]
    assert t.status == "failed" and "hỏng rồi" in t.first_error


def test_runtime_only_for_exercise_and_slide_html(tmp_path):
    course, spec = _course(tmp_path)
    s = course / "Session 01 - Ly thuyet"
    (s / "Bai giang tren lop").mkdir()
    (s / "Bai giang tren lop" / "slides.html").write_text("x")
    seen = {}

    def fake(target, opts):
        seen[opts.kind] = opts.runtime
        return _report(0)

    compute_status(spec, runtime=True, verify=fake)
    assert seen["slide_html"] is True and seen["reading"] is False
    seen.clear()
    compute_status(spec, runtime=False, verify=fake)
    assert not any(seen.values())


def _snap(statuses, deps=None):
    deps = deps or {}
    tasks = {k: TaskState(id=k, kind="x", status=v, target="", target_hint="", wave=1,
                          depends_on=deps.get(k, [])) for k, v in statuses.items()}
    return StateSnapshot("c", "s", "t", False, tasks)


@pytest.mark.parametrize("statuses,code", [
    (["done", "done"], 0), (["done", "failed", "missing"], 1), (["missing", "done"], 3),
    (["blocked_tool", "done"], 2), (["missing", "blocked_tool"], 3),
])
def test_exit_code(statuses, code):
    assert status_exit_code(_snap({f"t{i}": s for i, s in enumerate(statuses)})) == code


def test_ready_order():
    snap = _snap({"b": "missing", "a": "missing", "c": "missing"}, {"c": ["a"]})
    snap.tasks["c"].wave = 2
    assert [t.id for t in ready_tasks(snap)] == ["a", "b"]
    snap.tasks["a"].status = "done"
    assert [t.id for t in ready_tasks(snap)] == ["b", "c"]


def test_save_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(st, "STATE_ROOT", tmp_path / "s")
    snap = _snap({"a": "done"})
    path = save_state(snap)
    assert path == tmp_path / "s" / "c" / "state.json"
    assert load_state("c") == snap
    path.write_text("{hỏng", encoding="utf-8")
    assert load_state("c") is None
    assert load_state("none") is None
