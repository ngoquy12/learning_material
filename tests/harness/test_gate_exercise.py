"""Cổng bài tập (tĩnh)."""
from __future__ import annotations

from pathlib import Path

from core.harness.gates import GATES
from core.harness.gates.exercise import check_exercise, exercise_number, solution_dir
from core.harness.options import VerifyOptions

OPTS = VerifyOptions()


def prose(n_words: int) -> str:
    return " ".join(["từ"] * n_words)


def de_bai(h3=5, words=450, extra="") -> str:
    out = ["## <center>Bài tập</center>", ""]
    per = max(words // max(h3, 1), 1)
    for i in range(h3):
        out += [f"### **{i + 1}. Mục**", "", prose(per), ""]
    out += [extra]
    return "\n".join(out)


def make(tmp_path, n=3, text=None, criteria=True, starter=True, solution=True, guide=True) -> Path:
    base = tmp_path / "Bai tap"
    ex = base / f"{n}_tong_hop_demo"
    ex.mkdir(parents=True)
    (ex / "de_bai_bai_tap.md").write_text(text if text is not None else de_bai(), encoding="utf-8")
    if criteria:
        (ex / "tieu_chi_cham_diem_ai.md").write_text("tiêu chí", encoding="utf-8")
    if starter:
        (ex / "starter").mkdir()
        (ex / "starter" / "index.js").write_text("x", encoding="utf-8")
    teacher = base / "tai_lieu_giang_vien"
    teacher.mkdir()
    if solution:
        (teacher / "dap_an_mau" / f"bai_{n}").mkdir(parents=True)
        (teacher / "dap_an_mau" / f"bai_{n}" / "index.js").write_text("y", encoding="utf-8")
    if guide:
        (teacher / f"huong_dan_bai_{n}.md").write_text("hd", encoding="utf-8")
    return ex


def errors(r):
    return [f.message for f in r.findings if f.severity == "error"]


def test_registered():
    assert GATES["exercise"] is check_exercise


def test_helpers(tmp_path):
    ex = make(tmp_path, n=3)
    assert exercise_number(ex) == 3
    assert solution_dir(ex) == ex.parent / "tai_lieu_giang_vien" / "dap_an_mau" / "bai_3"


def test_complete_passes(tmp_path):
    r = check_exercise(make(tmp_path), OPTS)
    assert r.status == "pass", r.findings
    assert r.detail["h3_count"] == 5


def test_missing_criteria(tmp_path):
    r = check_exercise(make(tmp_path, criteria=False), OPTS)
    assert any("tieu_chi_cham_diem_ai.md" in m for m in errors(r))


def test_missing_solution(tmp_path):
    r = check_exercise(make(tmp_path, solution=False), OPTS)
    assert any("dap_an_mau" in m for m in errors(r))


def test_empty_solution(tmp_path):
    ex = make(tmp_path, solution=False)
    (ex.parent / "tai_lieu_giang_vien" / "dap_an_mau" / "bai_3").mkdir(parents=True)
    assert any("dap_an_mau" in m for m in errors(check_exercise(ex, OPTS)))


def test_missing_guide_and_starter(tmp_path):
    r = check_exercise(make(tmp_path, guide=False, starter=False), OPTS)
    msgs = " ".join(errors(r))
    assert "huong_dan_bai_3.md" in msgs and "starter" in msgs


def test_four_h3_is_error(tmp_path):
    r = check_exercise(make(tmp_path, text=de_bai(h3=4)), OPTS)
    assert any("### " in m for m in errors(r))


def test_h3_in_fence_not_counted(tmp_path):
    r = check_exercise(make(tmp_path, text=de_bai(h3=5, extra="```\n### giả\n```")), OPTS)
    assert r.status == "pass", r.findings


def test_900_words_is_warning(tmp_path):
    r = check_exercise(make(tmp_path, text=de_bai(words=900)), OPTS)
    assert not errors(r)
    assert any(f.severity == "warning" and "từ" in f.message for f in r.findings)


def test_code_words_not_counted(tmp_path):
    code = "```js\n" + prose(2000) + "\n```"
    r = check_exercise(make(tmp_path, text=de_bai(words=450, extra=code)), OPTS)
    assert r.status == "pass", r.findings


def test_banned_word_and_emoji(tmp_path):
    r = check_exercise(make(tmp_path, text=de_bai(extra="Tuyệt vời \U0001F600")), OPTS)
    assert len([m for m in errors(r)]) >= 2
