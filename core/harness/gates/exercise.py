"""Cổng bài tập (tĩnh): thư mục `Bai tap/<N>_<slug>/` cùng đáp án mẫu và hướng dẫn giảng viên.

Phần chạy thật (runtime) sẽ thêm sau như một bước riêng bên cạnh `_static_findings`.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

from core.harness.findings import Finding, GateResult
from core.harness.gates import GATES
from core.harness.options import VerifyOptions
from core.harness.text_rules import find_banned_words, find_emoji

GATE = "exercise"
BRIEF, CRITERIA, STARTER = "de_bai_bai_tap.md", "tieu_chi_cham_diem_ai.md", "starter"
H3_COUNT = 5
WORD_MIN, WORD_MAX = 350, 700
_H3_RE = re.compile(r"^###\s+\S")
_WORD_RE = re.compile(r"\S+")


def exercise_number(path: Path) -> int:
    m = re.match(r"^(\d+)", Path(path).name)
    if not m:
        raise ValueError(f"Tên thư mục bài tập không bắt đầu bằng số: {Path(path).name}")
    return int(m.group(1))


def teacher_dir(path: Path) -> Path:
    return Path(path).parent / "tai_lieu_giang_vien"


def solution_dir(path: Path) -> Path:
    return teacher_dir(path) / "dap_an_mau" / f"bai_{exercise_number(path)}"


def guide_path(path: Path) -> Path:
    return teacher_dir(path) / f"huong_dan_bai_{exercise_number(path)}.md"


def _split_prose(text: str) -> tuple[str, int]:
    """Văn bản ngoài khối mã và số tiêu đề `### ` ngoài khối mã."""
    prose: list[str] = []
    h3 = 0
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        prose.append(line)
        if _H3_RE.match(line):
            h3 += 1
    return "\n".join(prose), h3


def _nonempty_dir(p: Path) -> bool:
    return p.is_dir() and any(p.iterdir())


def _static_findings(path: Path, result: GateResult) -> None:
    def err(msg: str, loc: str = "") -> None:
        result.findings.append(Finding("error", GATE, msg, loc))

    try:
        n = exercise_number(path)
    except ValueError as exc:
        err(str(exc))
        return
    result.detail["exercise"] = n
    brief = path / BRIEF
    if not brief.is_file():
        err(f"Thiếu tệp {BRIEF}", str(path))
    else:
        try:
            text = brief.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            err(f"Không đọc được {BRIEF}: {exc}", BRIEF)
        else:
            prose, h3 = _split_prose(text)
            words = len(_WORD_RE.findall(prose))
            result.detail["word_count"] = words
            result.detail["h3_count"] = h3
            if h3 != H3_COUNT:
                err(f"{BRIEF} cần đúng {H3_COUNT} tiêu đề `### `, hiện có {h3}", BRIEF)
            if not WORD_MIN <= words <= WORD_MAX:
                result.findings.append(Finding(
                    "warning", GATE, f"{BRIEF}: số từ {words} ngoài khoảng {WORD_MIN}-{WORD_MAX}", BRIEF))
            for w in find_banned_words(prose):
                err(f"{BRIEF}: chứa từ cấm `{w}`", BRIEF)
            if find_emoji(prose):
                err(f"{BRIEF}: chứa emoji", BRIEF)
    if not (path / CRITERIA).is_file():
        err(f"Thiếu tệp {CRITERIA}", str(path))
    if not _nonempty_dir(path / STARTER):
        err(f"Thiếu thư mục {STARTER}/ hoặc thư mục rỗng", str(path))
    sol = solution_dir(path)
    if not _nonempty_dir(sol):
        err(f"Thiếu đáp án mẫu hoặc thư mục rỗng: tai_lieu_giang_vien/dap_an_mau/bai_{n}", str(sol))
    if not guide_path(path).is_file():
        err(f"Thiếu hướng dẫn giảng viên: tai_lieu_giang_vien/huong_dan_bai_{n}.md", str(guide_path(path)))


def check_exercise(path: Path, opts: VerifyOptions) -> GateResult:
    start = time.perf_counter()
    path = Path(path)
    result = GateResult(kind="exercise", path=str(path), gate=GATE)
    _static_findings(path, result)
    result.duration_s = time.perf_counter() - start
    return result


GATES["exercise"] = check_exercise
