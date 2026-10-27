"""Cổng slide html: kiểm tĩnh slides.html."""
from __future__ import annotations

from core.harness.gates import GATES
from core.harness.gates.slide_html import check_slide_html, static_html_findings
from core.harness.options import VerifyOptions

OK = "<html><body><div class='slide active'><h2>Biến và kiểu dữ liệu</h2><p>Nội dung</p></div></body></html>"


def msgs(html):
    return [f.message for f in static_html_findings(html) if f.severity == "error"]


def test_registered():
    assert GATES["slide_html"] is check_slide_html


def test_clean_html_no_findings():
    assert static_html_findings(OK) == []


def test_banned_style():
    assert any("backdrop-filter" in m for m in msgs("<div style='backdrop-filter: blur(4px)'>x</div>"))


def test_emoji_and_banned_word_and_href():
    out = msgs("<p>Tuyệt vời \U0001F600</p><a href=\"#\">x</a>")
    assert any("emoji" in m for m in out)
    assert any("tuyệt vời" in m for m in out)
    assert any("href" in m for m in out)


def test_placeholder_outside_code_is_error():
    assert any("{{" in m for m in msgs("<p>Xin chào {{ name }}</p>"))


def test_jsx_inside_pre_is_fine():
    html = "<pre><code>&lt;div style={{ color }}&gt;</code></pre>"
    assert msgs(html) == []
    assert msgs("<pre>style={{ color }}</pre>") == []


def test_gate_reads_file(tmp_path):
    d = tmp_path / "Bai giang tren lop"
    d.mkdir()
    p = d / "slides.html"
    p.write_text(OK, encoding="utf-8")
    r = check_slide_html(p, VerifyOptions())
    assert r.status == "pass", r.findings
    p.write_text("<p>neon</p>", encoding="utf-8")
    assert check_slide_html(p, VerifyOptions()).status == "fail"
