"""Cổng bài tập: thư mục `Bai tap/<N>_<slug>/` cùng đáp án mẫu và hướng dẫn giảng viên.

Tĩnh: `_static_findings`. Với `--runtime`: `_runtime_findings` chạy test thật của đáp án mẫu và starter;
bộ chạy chọn theo nội dung thư mục (spec 4.2), không theo tên môn.
"""
from __future__ import annotations

import json
import re
import time
from contextlib import nullcontext
from pathlib import Path

from core.harness.findings import Finding, GateResult
from core.harness.gates import GATES
from core.harness.options import VerifyOptions
from core.harness import runners
from core.harness.runners import RunnerError, ToolUnavailable
from core.harness.runners import browser as browser_runner
from core.harness.runners import vitest as vitest_runner
from core.harness.runners.mysql_sandbox import MySQLSandbox
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


NO_RUNNER = "Không có bộ test chạy được"
_SQL_DIRS = ("db", "sql", "database")


def _package(proj: Path) -> dict | None:
    try:
        return json.loads((proj / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _tests_html(proj: Path) -> Path | None:
    """tests.html nằm cùng thư mục với harness.js (ưu tiên gốc dự án)."""
    for html in [proj / "tests.html", *sorted(proj.rglob("tests.html"))]:
        if html.is_file() and "node_modules" not in html.parts and (html.parent / "harness.js").is_file():
            return html
    return None


def select_runner(proj: Path) -> str | None:
    """"vitest" | "browser" | None theo nội dung thư mục dự án."""
    pkg = _package(proj)
    if pkg and any("vitest" in (pkg.get(sec) or {}) for sec in ("dependencies", "devDependencies")):
        return "vitest"
    if _tests_html(proj):
        return "browser"
    return None


def needs_mysql(proj: Path) -> bool:
    """Có thư mục SQL khởi tạo (db/*.sql...) hoặc biến DB_* trong .env.example."""
    if any(any((proj / d).glob("*.sql")) for d in _SQL_DIRS if (proj / d).is_dir()):
        return True
    try:
        env = (proj / ".env.example").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return any(line.strip().startswith("DB_") for line in env.splitlines())


def db_env(db: dict) -> dict:
    return {"DB_HOST": str(db["host"]), "DB_PORT": str(db["port"]),
            "DB_USER": str(db["user"]), "DB_PASSWORD": str(db["password"])}


def run_project(proj: Path, db: dict | None = None) -> dict:
    """Chạy bộ test của một dự án; trả `{runner, passed, failed, total, ok, failed_tests, suite_errors}`."""
    runner = select_runner(proj)
    if runner == "vitest":
        ws = vitest_runner.NodeWorkspace(runners.CACHE_ROOT / "node_ws").prepare(proj / "package.json")
        out = vitest_runner.run_vitest(proj, ws, env=db_env(db) if db else None)
    elif runner == "browser":
        out = browser_runner.run_tests_html(_tests_html(proj))
    else:
        raise RunnerError(NO_RUNNER)
    out["runner"] = runner
    return out


def _judge(label: str, is_solution: bool, r: dict, result: GateResult, loc: str) -> None:
    def add(sev: str, msg: str) -> None:
        result.findings.append(Finding(sev, GATE, msg, loc))

    p, t = r.get("passed", 0), r.get("total", 0)
    failed = "; ".join(x for x in r.get("failed_tests", [])[:3] if x)
    suites = "; ".join(r.get("suite_errors", [])[:2])
    if t == 0:
        tail = f": {r['error'][-300:]}" if r.get("error") else (f": {suites}" if suites else "")
        add("error", f"{label} chạy được 0 test (không chạy được hoặc lỗi khi nạp){tail}")
        return
    if is_solution:
        if p < t:
            add("error", f"{label} chỉ đạt {p}/{t} test, cần đạt 100%" + (f"; hỏng: {failed}" if failed else ""))
        if suites:
            add("error", f"{label} có tệp test không chạy được: {suites}")
    else:
        if p >= t:
            add("error", f"Thư mục starter đã đạt hết {p}/{t} test; starter phải còn test chưa đạt để sinh viên làm")
        if suites:
            add("warning", f"{label} có tệp test không nạp được: {suites}")


def _runtime_findings(path: Path, result: GateResult) -> None:
    try:
        sol = solution_dir(path)
    except ValueError:
        return
    targets = [(key, label, proj, key == "solution") for key, label, proj in
               (("solution", "Đáp án mẫu", sol), ("starter", "Starter", path / STARTER)) if _nonempty_dir(proj)]
    plan = [(key, label, proj, is_sol, select_runner(proj)) for key, label, proj, is_sol in targets]
    if not any(runner for *_, runner in plan):
        result.skipped_reason = NO_RUNNER
        return
    detail: dict = {}
    result.detail["runtime"] = detail
    use_db = any(runner == "vitest" and needs_mysql(proj) for _, _, proj, _, runner in plan)
    try:
        with (MySQLSandbox() if use_db else nullcontext(None)) as db:
            for key, label, proj, is_sol, runner in plan:
                if runner is None:
                    result.findings.append(Finding("error", GATE, f"{label}: {NO_RUNNER.lower()}", str(proj)))
                    continue
                try:
                    r = run_project(proj, db if runner == "vitest" and needs_mysql(proj) else None)
                except RunnerError as exc:
                    result.findings.append(Finding("error", GATE, f"{label}: {exc}", str(proj)))
                    continue
                detail[key] = {k: r.get(k) for k in ("runner", "passed", "failed", "total")}
                _judge(label, is_sol, r, result, str(proj))
    except ToolUnavailable as exc:
        result.skipped_reason = str(exc)
    except RunnerError as exc:
        result.findings.append(Finding("error", GATE, f"Không chạy được MySQL tạm: {exc}"))


def check_exercise(path: Path, opts: VerifyOptions) -> GateResult:
    start = time.perf_counter()
    path = Path(path)
    result = GateResult(kind="exercise", path=str(path), gate=GATE)
    _static_findings(path, result)
    if opts.runtime:
        _runtime_findings(path, result)
    result.duration_s = time.perf_counter() - start
    return result


GATES["exercise"] = check_exercise
