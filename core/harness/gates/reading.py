"""Cổng bài đọc: bộ kiểm tra của dự án + kiểm tra bổ sung của skill reading_generator."""
from __future__ import annotations

import importlib.util
import re
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

from core.harness.findings import Finding, GateResult
from core.harness.options import VerifyOptions

GATE = "reading"
REPO = Path(__file__).resolve().parents[3]
CHECK_SCRIPT = REPO / "skills" / "reading_generator" / "scripts" / "check_reading.py"
WORD_MIN, WORD_MAX = 1500, 2000

_SIM_HEADING_RE = re.compile(r"mô phỏng tương tác", re.IGNORECASE)
_SIM_CLASS_RE = re.compile(r"(?:^|[\s_-])sim(?:$|[\s_-])", re.IGNORECASE)
_LANG_RE = re.compile(r"\blanguage-([A-Za-z0-9_+#-]+)")


@lru_cache(maxsize=1)
def _skill_module():
    spec = importlib.util.spec_from_file_location("_harness_check_reading", CHECK_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def infer_tech_stack(html: str) -> str:
    """Lớp `language-<x>` xuất hiện nhiều nhất; chuỗi rỗng nếu không có mã."""
    counts = Counter(m.lower() for m in _LANG_RE.findall(html))
    return counts.most_common(1)[0][0] if counts else ""


def has_section3_simulator(html: str) -> bool:
    """Biến thể mô phỏng ở cuối Mục 3: tiêu đề "Mô phỏng tương tác" hoặc khối lớp/id `l<N>_sim`, kèm điều khiển."""
    from bs4 import BeautifulSoup

    sec = BeautifulSoup(html, "html.parser").find(id="section-3")
    if sec is None or not sec.find(["button", "input", "select"]):
        return False
    for h in sec.find_all(["h2", "h3", "h4"]):
        if _SIM_HEADING_RE.search(h.get_text(" ", strip=True)):
            return True
    for tag in sec.find_all(True):
        ident = " ".join(tag.get("class", [])) + " " + str(tag.get("id", ""))
        if _SIM_CLASS_RE.search(ident):
            return True
    return False


def check_reading(path: Path, opts: VerifyOptions) -> GateResult:
    from core.validators.reading_validator import count_visible_words, validate_reading_material

    start = time.perf_counter()
    path = Path(path)
    result = GateResult(kind="reading", path=str(path), gate=GATE)
    try:
        html = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        result.findings.append(Finding("error", GATE, f"Không đọc được tệp: {exc}"))
        result.duration_s = time.perf_counter() - start
        return result
    if not html.strip():
        result.findings.append(Finding("error", GATE, "Tệp bài đọc rỗng"))
        result.duration_s = time.perf_counter() - start
        return result

    metadata = {
        "tech_stack": infer_tech_stack(html),
        "course_name": "",
        "lesson_title": path.parent.parent.name,
        "is_orientation": False,
        "enforce_word_budget": True,
    }
    _, validator_errors = validate_reading_material(html, metadata)
    sim = has_section3_simulator(html)
    for msg in validator_errors:
        severity = "warning" if (sim and "Section 2.4" in msg) else "error"
        result.findings.append(Finding(severity, GATE, msg))

    words = count_visible_words(html)
    result.detail["word_count"] = words
    if not WORD_MIN <= words <= WORD_MAX:
        result.findings.append(Finding("warning", GATE, f"số từ {words} ngoài khoảng 1.500-2.000"))

    errors, warnings = _skill_module().extra_checks(html)
    result.findings += [Finding("error", GATE, m) for m in errors]
    result.findings += [Finding("warning", GATE, m) for m in warnings]
    result.duration_s = time.perf_counter() - start
    return result
