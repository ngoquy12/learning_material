"""Điều phối kiểm chứng: verify_path; CLI nằm ở `core/harness/cli.py`."""
from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path

from core.harness.findings import Finding, GateResult, Report
from core.harness.gates import GATES
from core.harness.options import VerifyOptions
from core.harness.registry import detect_kind, discover
from core.harness.report_io import write_report

__all__ = ["VerifyOptions", "verify_path", "write_report", "main"]

_NOT_RESOURCE = "Tệp không thuộc loại tài nguyên nào, bỏ qua"
_FILE_NOT_RESOURCE = ("Tệp không thuộc loại tài nguyên nào được nhận diện (theo tên tệp và thư mục cha); "
                      "dùng --kind để chỉ định loại")
_NOTHING_FOUND = ("Không tìm thấy tài nguyên nào được nhận diện trong thư mục; "
                  "kiểm tra tên thư mục (Bài đọc, Quizz lesson, Bài tập/<số>_...) hoặc dùng --kind")


def _run_gate(kind: str, path: Path, opts: VerifyOptions) -> GateResult:
    start = time.perf_counter()
    try:
        result = GATES[kind](path, opts)
    except Exception as exc:  # noqa: BLE001 - một cổng lỗi không dừng cả lần chạy
        result = GateResult(
            kind=kind, path=str(path), gate=kind,
            findings=[Finding("error", kind, f"Cổng lỗi: {exc}")],
        )
    result.duration_s = round(time.perf_counter() - start, 3)
    return result


def _unknown(path: Path, severity: str, message: str) -> GateResult:
    return GateResult(kind="unknown", path=str(path), gate="registry",
                      findings=[Finding(severity, "registry", message)])


def _verify_tree(target: Path, opts: VerifyOptions) -> list[GateResult]:
    found, unknown = discover(target)
    results: list[GateResult] = []
    if opts.kind in GATES:
        # --kind trên cây nhiều tài nguyên: chỉ chạy các tài nguyên đúng loại đó.
        picked = [(k, p) for k, p in found if k == opts.kind]
        if picked:
            found = picked
        elif found:
            return [_unknown(target, "error",
                             f"Không tìm thấy tài nguyên loại `{opts.kind}` trong thư mục")]
        else:
            return [_run_gate(opts.kind, target, opts)]  # thư mục một tài nguyên không theo quy ước
    if not found:
        results.append(_unknown(target, "error", _NOTHING_FOUND))
    for k, p in found:
        results.append(_run_gate(k, p, opts))
    for p in unknown:
        results.append(_unknown(p, "info", _NOT_RESOURCE))
    return results


def verify_path(target: Path, opts: VerifyOptions) -> Report:
    """Tệp: --kind hoặc loại nhận diện được. Thư mục tài nguyên (bài tập, quiz): chạy trực tiếp.
    Thư mục khác: duyệt cây; --kind lọc theo loại."""
    target = Path(target)
    started = datetime.now().isoformat(timespec="seconds")
    try:
        detected = detect_kind(target)
        if target.is_file():
            kind = opts.kind if opts.kind in GATES else detected
            results = [_run_gate(kind, target, opts)] if kind else [_unknown(target, "error", _FILE_NOT_RESOURCE)]
        elif detected:
            results = [_run_gate(opts.kind if opts.kind in GATES else detected, target, opts)]
        else:
            results = _verify_tree(target, opts)
    except OSError as exc:  # vd. PermissionError khi duyệt cây: thành lỗi của đích, không traceback
        results = [_unknown(target, "error", f"Không duyệt được đường dẫn: {exc}")]
    return Report(target=str(target), results=results, started_at=started)


def _summary(report: Report, report_dir: Path) -> str:
    c = report.counts()
    lines = [f"pass: {c['pass']}  fail: {c['fail']}  skipped: {c['skipped']}  unknown: {c['unknown']}"]
    for r in report.results:
        for f in r.findings:
            if f.severity == "error":
                lines.append(f"[{r.kind}] {r.path}: {f.message}")
    for r in report.results:
        if r.skipped_reason:
            lines.append(f"Bỏ qua [{r.kind}] {r.path}: {r.skipped_reason}")
    lines.append(f"Báo cáo: {report_dir}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Giữ cho mã cũ: chuyển sang `cli.main` (bộ phân tích lệnh con nằm ở `core/harness/cli.py`)."""
    from core.harness.cli import main as cli_main  # nạp muộn: cli phụ thuộc module này

    return cli_main(argv)
