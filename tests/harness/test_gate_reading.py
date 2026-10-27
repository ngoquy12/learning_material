"""Cổng bài đọc."""
from __future__ import annotations

import re
from pathlib import Path

from core.harness.gates import GATES
from core.harness.gates.reading import check_reading
from core.harness.options import VerifyOptions

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "harness" / "reading_ok.html"
OPTS = VerifyOptions()


def _put(tmp_path: Path, html: str) -> Path:
    p = tmp_path / "Lesson 01 - Demo" / "Bai doc" / "reading.html"
    p.parent.mkdir(parents=True)
    p.write_text(html, encoding="utf-8")
    return p


def test_registered():
    assert GATES["reading"] is check_reading


def test_good_reading_passes(tmp_path):
    r = check_reading(_put(tmp_path, FIXTURE.read_text(encoding="utf-8")), OPTS)
    assert r.status == "pass", [f.message for f in r.findings if f.severity == "error"]
    assert r.kind == "reading" and r.detail["word_count"] > 1000


def test_bad_href_and_emoji_fail(tmp_path):
    html = FIXTURE.read_text(encoding="utf-8").replace("</body>", '<a href="#">x</a><p>\u2705</p></body>')
    r = check_reading(_put(tmp_path, html), OPTS)
    assert r.status == "fail"
    msgs = [f.message for f in r.findings if f.severity == "error"]
    assert any('href="#"' in m for m in msgs)
    assert any("emoji" in m.lower() for m in msgs)


def test_empty_fails(tmp_path):
    assert check_reading(_put(tmp_path, ""), OPTS).status == "fail"


def _strip_sim(html: str) -> str:
    # bỏ dấu hiệu mô phỏng ở Mục 3 (tiêu đề + lớp *_sim), giữ phần còn lại
    html = re.sub(r"Mô phỏng tương tác", "Minh họa", html)
    return re.sub(r"\bl\d+[_-]sim\b", "l1_demo", html)


def test_section_24_downgraded_when_section3_has_simulator(tmp_path):
    r = check_reading(_put(tmp_path, FIXTURE.read_text(encoding="utf-8")), OPTS)
    assert any("Section 2.4" in f.message and f.severity == "warning" for f in r.findings)
    assert not any("Section 2.4" in f.message and f.severity == "error" for f in r.findings)


def test_section_24_stays_error_without_simulator(tmp_path):
    r = check_reading(_put(tmp_path, _strip_sim(FIXTURE.read_text(encoding="utf-8"))), OPTS)
    assert r.status == "fail"
    assert any("Section 2.4" in f.message and f.severity == "error" for f in r.findings)
