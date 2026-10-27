"""Cổng lab: cấu trúc `lab_guide.md` (Lab N, Tổng kết, Rubric, Kết quả mong đợi)."""
from __future__ import annotations

import re
import time
from pathlib import Path

from core.harness.findings import Finding, GateResult
from core.harness.gates import GATES
from core.harness.options import VerifyOptions
from core.harness.registry import normalize_name

GATE = "lab"
_H2_RE = re.compile(r"^##\s+(?!#)(.+?)\s*$")
_LAB_RE = re.compile(r"^lab\s+(\d+)\b")
_MINUTES_RE = re.compile(r"\((\d+)\s*phut\)\s*$")
_EXPECTED = "ket qua mong doi"


def _sections(text: str) -> list[tuple[str, list[str]]]:
    """Các mục `## ` (tiêu đề, dòng thân) ngoài khối mã."""
    out: list[tuple[str, list[str]]] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        m = None if in_fence else _H2_RE.match(line)
        if m:
            out.append((m.group(1), []))
        elif out:
            out[-1][1].append(line)
    return out


def check_lab(path: Path, opts: VerifyOptions) -> GateResult:
    start = time.perf_counter()
    path = Path(path)
    result = GateResult(kind="lab", path=str(path), gate=GATE)

    def err(msg: str) -> None:
        result.findings.append(Finding("error", GATE, msg))

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        err(f"Không đọc được tệp: {exc}")
        result.duration_s = time.perf_counter() - start
        return result

    sections = _sections(text)
    labs = []
    for title, body in sections:
        norm = normalize_name(title)
        m = _LAB_RE.match(norm)
        if m:
            labs.append((int(m.group(1)), norm, "\n".join(body)))
    if not labs:
        err("Lab guide không có mục `## Lab N - … (K phút)` nào")
    minutes = 0
    for n, norm, body in labs:
        mm = _MINUTES_RE.search(norm)
        if mm:
            minutes += int(mm.group(1))
        else:
            err(f"Lab {n}: tiêu đề thiếu thời lượng dạng `(K phút)`")
        if _EXPECTED not in normalize_name(body):
            err(f"Lab {n}: thiếu \"Kết quả mong đợi\"")
    norms = [normalize_name(t) for t, _ in sections]
    if not any(t.startswith("tong ket") for t in norms):
        err("Thiếu mục `## Tổng kết`")
    if not any(t.startswith("rubric") for t in norms):
        err("Thiếu mục `## Rubric`")
    result.detail["minutes"] = minutes
    result.detail["labs"] = len(labs)
    result.duration_s = time.perf_counter() - start
    return result


GATES["lab"] = check_lab
