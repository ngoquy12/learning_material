import json

from core.harness.findings import Finding, GateResult, Report


def ok_result():
    return GateResult("reading", "a.html", "reading", [])


def fail_result():
    return GateResult("quiz_lesson", "q.md", "quiz", [Finding("error", "quiz", "thiếu đáp án", "dòng 3")])


def test_status_and_exit_code():
    ok = ok_result()
    warn = GateResult("reading", "b.html", "reading", [Finding("warning", "reading", "x")])
    bad = fail_result()
    skip = GateResult("slide_html", "s.html", "slide_html", [], skipped_reason="Thiếu Playwright")
    assert (ok.status, warn.status, bad.status, skip.status) == ("pass", "pass", "fail", "skipped")
    assert Report("t", [ok, warn], "2026-10-27T00:00:00").exit_code == 0
    assert Report("t", [ok, skip], "x").exit_code == 2
    assert Report("t", [skip, bad], "x").exit_code == 1
    assert Report("t", [], "x").exit_code == 0


def test_defaults_not_shared():
    a, b = ok_result(), ok_result()
    a.detail["k"] = 1
    a.findings.append(Finding("info", "g", "m"))
    assert b.detail == {} and b.findings == []


def test_json_roundtrip_has_status():
    r = Report("t", [ok_result(), fail_result()], "x")
    d = json.loads(r.to_json())
    assert [x["status"] for x in d["results"]] == ["pass", "fail"]
    assert d["counts"] == {"pass": 1, "fail": 1, "skipped": 0, "unknown": 0}
    assert r.to_dict()["exit_code"] == 1


def test_markdown_lists_failures_first():
    md = Report("t", [ok_result(), fail_result()], "x").to_markdown()
    assert md.index("[fail]") < md.index("[pass]")
    assert "- [error] thiếu đáp án (dòng 3)" in md
