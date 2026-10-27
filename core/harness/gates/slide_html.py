"""Cổng slide html: kiểm tĩnh slides.html (đo vừa khung bằng trình duyệt thuộc bước runtime, Task 7)."""
from __future__ import annotations

import re
import time
from pathlib import Path

from core.harness.findings import Finding, GateResult
from core.harness.gates import GATES
from core.harness.gates._skill_loader import load_skill_script
from core.harness.options import VerifyOptions
from core.harness.text_rules import find_banned_words, find_emoji

GATE = "slide_html"
_PLACEHOLDER_RE = re.compile(r"\{\{\s*[\w.\-]+\s*\}\}")
_HREF_HASH_RE = re.compile(r"""href\s*=\s*["']#["']""")


def _skill_module():
    return load_skill_script("slide_html", "check_slides_html")


def _without_code(html: str) -> str:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["pre", "code"]):
        tag.decompose()
    return str(soup)


def _visible_text(html: str) -> str:
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", text)


def static_html_findings(html: str) -> list[Finding]:
    out: list[Finding] = []

    def err(msg: str) -> None:
        out.append(Finding("error", GATE, msg))

    if _PLACEHOLDER_RE.search(_without_code(html)):
        err("Còn chỗ giữ chỗ {{...}} chưa thay")
    if _HREF_HASH_RE.search(html):
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
            result.detail["slides"] = len(re.findall(r"""class\s*=\s*["'][^"']*\bslide\b""", html))
            # opts.runtime: bước đo vừa khung bằng Playwright sẽ thêm ở đây (Task 7).
    result.duration_s = time.perf_counter() - start
    return result


GATES["slide_html"] = check_slide_html
