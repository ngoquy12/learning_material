"""Cổng slide html: kiểm tĩnh slides.html; với `--runtime` đo vừa khung từng slide và lỗi console bằng trình duyệt."""
from __future__ import annotations

import re
import time
from pathlib import Path

from core.harness.findings import Finding, GateResult
from core.harness.gates import GATES
from core.harness.gates._skill_loader import load_skill_script
from core.harness.options import VerifyOptions
from core.harness.runners import ToolUnavailable
from core.harness.runners import browser as browser_runner
from core.harness.text_rules import find_banned_words, find_emoji

GATE = "slide_html"
_PLACEHOLDER_RE = re.compile(r"\{\{\s*[\w.\-]+\s*\}\}")
_HREF_HASH_RE = re.compile(r"""href\s*=\s*["']#["']""")


def _skill_module():
    return load_skill_script("slide_html", "check_slides_html")


def _without(html: str, names: list[str]) -> str:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(names):
        tag.decompose()
    return str(soup)


def count_slides(html: str) -> int:
    """Số phần tử có đúng lớp `slide` (không tính slide-title, slide-num...)."""
    from bs4 import BeautifulSoup

    return len(BeautifulSoup(html, "html.parser").find_all(class_=lambda c: c is not None and "slide" in c.split()))


def _visible_text(html: str) -> str:
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", text)


def static_html_findings(html: str) -> list[Finding]:
    out: list[Finding] = []

    def err(msg: str) -> None:
        out.append(Finding("error", GATE, msg))

    if _PLACEHOLDER_RE.search(_without(html, ["pre", "code", "script"])):
        err("Còn chỗ giữ chỗ {{...}} chưa thay")
    if _HREF_HASH_RE.search(_without(html, ["pre", "code"])):
        err('Có thẻ <a href="#">')
    for token in _skill_module().BANNED_STYLE:
        if token in html:
            err(f"Có phong cách bị cấm '{token}' (kính mờ, gradient, hoạt ảnh nhấp nháy)")
    visible = _visible_text(html)
    if find_emoji(visible):
        err("Có emoji hoặc ký tự biểu tượng trong nội dung")
    for word in find_banned_words(visible):
        err(f"Có từ bị cấm '{word}'")
    return out


def _runtime(path: Path, result: GateResult) -> None:
    """Đo bằng trình duyệt; thiếu công cụ → skipped_reason, đo hỏng → error."""
    try:
        m = browser_runner.measure_slides(path)
    except ToolUnavailable as exc:
        result.skipped_reason = str(exc)
        return
    except Exception as exc:  # noqa: BLE001 - lỗi trình duyệt khi đo (RunnerError, Playwright) là lỗi của cổng
        result.findings.append(Finding("error", GATE, f"Không đo được slide bằng trình duyệt: {exc}"))
        return
    result.detail["runtime"] = {"slides": m.get("slides", 0),
                                "overflow": len(m.get("slide_overflow", [])),
                                "console_errors": len(m.get("console_errors", []))}
    if not m.get("has_go", True):
        result.findings.append(Finding("error", GATE, "Không có hàm go(i) để chuyển slide"))
    for o in m.get("slide_overflow", []):
        if o["over_px"] > browser_runner.TOLERANCE_PX:
            result.findings.append(Finding(
                "error", GATE,
                f"Nội dung tràn khung ở slide {o['slide']}, độ phân giải {o['viewport']}: "
                f"dư {o['over_px']}px ({o['state']})", f"slide {o['slide']}"))
    for o in m.get("horizontal_overflow", []):
        result.findings.append(Finding(
            "error", GATE, f"Nội dung tràn ngang ở slide {o['slide']}, độ phân giải {o['viewport']}",
            f"slide {o['slide']}"))
    for msg in m.get("console_errors", []):
        result.findings.append(Finding("error", GATE, f"Lỗi console: {msg}"))


def check_slide_html(path: Path, opts: VerifyOptions) -> GateResult:
    start = time.perf_counter()
    path = Path(path)
    result = GateResult(kind="slide_html", path=str(path), gate=GATE)
    try:
        html = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        result.findings.append(Finding("error", GATE, f"Không đọc được tệp: {exc}"))
    else:
        if not html.strip():
            result.findings.append(Finding("error", GATE, "Tệp slides.html rỗng"))
        else:
            result.findings += static_html_findings(html)
            result.detail["slides"] = count_slides(html)
            if opts.runtime:
                _runtime(path, result)
    result.duration_s = time.perf_counter() - start
    return result


GATES["slide_html"] = check_slide_html
