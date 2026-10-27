"""Cổng lab: tiêu đề Lab N, Tổng kết, Rubric, Kết quả mong đợi mỗi Lab."""
from __future__ import annotations

from core.harness.gates import GATES
from core.harness.gates.lab import check_lab
from core.harness.options import VerifyOptions

OPTS = VerifyOptions()


def lab_md(skip_expected_in=None, with_summary=True, with_rubric=True, labs=2) -> str:
    out = ["# Session 02 - Thực hành", "", "Kết quả mong đợi ở phần mở đầu không tính cho Lab nào.", ""]
    for n in range(1, labs + 1):
        out += [f"## Lab {n} - Nội dung lab {n} ({n * 10} phút)", "", "Làm theo các bước.", "",
                "```bash", "## không phải tiêu đề", "```", ""]
        if n != skip_expected_in:
            out += ["Kết quả mong đợi:", "", "```", "ok", "```", ""]
    if with_summary:
        out += ["## Tổng kết (5 phút)", "", "Ôn lại.", ""]
    if with_rubric:
        out += ["## Rubric chấm lab (10 điểm)", "", "Bảng điểm.", ""]
    return "\n".join(out)


def run(tmp_path, text):
    d = tmp_path / "Bai thuc hanh"
    d.mkdir()
    p = d / "lab_guide.md"
    p.write_text(text, encoding="utf-8")
    return check_lab(p, OPTS)


def test_registered():
    assert GATES["lab"] is check_lab


def test_full_lab_passes(tmp_path):
    r = run(tmp_path, lab_md())
    assert r.status == "pass", r.findings
    assert r.detail["minutes"] == 30


def test_missing_expected_result_in_lab2(tmp_path):
    r = run(tmp_path, lab_md(skip_expected_in=2))
    errs = [f for f in r.findings if f.severity == "error"]
    assert any("Lab 2" in f.message for f in errs)
    assert not any("Lab 1" in f.message for f in errs)


def test_missing_summary_and_rubric(tmp_path):
    r = run(tmp_path, lab_md(with_summary=False, with_rubric=False))
    msgs = " ".join(f.message for f in r.findings if f.severity == "error")
    assert "Tổng kết" in msgs and "Rubric" in msgs


def test_no_lab_heading(tmp_path):
    r = run(tmp_path, "# Tiêu đề\n\n## Tổng kết\n\n## Rubric\n")
    assert any(f.severity == "error" and "Lab" in f.message for f in r.findings)


def test_unaccented_headings_match(tmp_path):
    text = lab_md().replace("Tổng kết", "Tong ket").replace("Rubric chấm", "RUBRIC cham")
    assert run(tmp_path, text).status == "pass"


def test_heading_in_fence_ignored(tmp_path):
    text = lab_md(with_summary=False) + "\n```\n## Tổng kết\n```\n"
    r = run(tmp_path, text)
    assert any("Tổng kết" in f.message for f in r.findings if f.severity == "error")


def _errs(r):
    return [f.message for f in r.findings if f.severity == "error"]


def test_duplicate_lab_number_is_error(tmp_path):
    text = lab_md(labs=3).replace("## Lab 3 - Nội dung lab 3", "## Lab 2 - Nội dung lab 3")
    r = run(tmp_path, text)
    assert any("Lab 2" in m and "trùng" in m for m in _errs(r)), r.findings


def test_non_ascending_lab_numbers_is_error(tmp_path):
    text = (lab_md(labs=2).replace("## Lab 1 - ", "## Lab X1 - ")
            .replace("## Lab 2 - ", "## Lab 1 - ").replace("## Lab X1 - ", "## Lab 2 - "))
    r = run(tmp_path, text)
    assert any("tăng dần" in m for m in _errs(r)), r.findings


def test_gap_in_lab_numbers_is_allowed(tmp_path):
    text = lab_md(labs=2).replace("## Lab 2 - ", "## Lab 3 - ")
    assert run(tmp_path, text).status == "pass"


def test_expected_result_inside_code_fence_not_counted(tmp_path):
    text = lab_md(skip_expected_in=2).replace(
        "## Tổng kết", "```text\nKết quả mong đợi: chỉ là ví dụ trong mã\n```\n\n## Tổng kết")
    r = run(tmp_path, text)
    assert any("Lab 2" in m and "Kết quả mong đợi" in m for m in _errs(r)), r.findings
