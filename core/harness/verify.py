"""Điều phối kiểm chứng: verify_path và CLI `python -m core.harness verify`."""
from __future__ import annotations

import argparse
import contextlib
import sys
import time
from datetime import datetime
from pathlib import Path

from core.harness.findings import Finding, GateResult, Report
from core.harness.gates import GATES
from core.harness.options import VerifyOptions
from core.harness.registry import detect_kind, discover
from core.harness.report_io import default_report_dir, is_inside, write_report

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
    detected = detect_kind(target)
    if target.is_file():
        kind = opts.kind if opts.kind in GATES else detected
        results = [_run_gate(kind, target, opts)] if kind else [_unknown(target, "error", _FILE_NOT_RESOURCE)]
    elif detected:
        results = [_run_gate(opts.kind if opts.kind in GATES else detected, target, opts)]
    else:
        results = _verify_tree(target, opts)
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
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(prog="python -m core.harness")
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("verify", help="kiểm chứng học liệu")
    v.add_argument("path")
    v.add_argument("--kind", choices=sorted(GATES),
                   help="ép loại cho một tệp hoặc thư mục một tài nguyên; với thư mục môn: chỉ chạy tài nguyên loại này")
    v.add_argument("--runtime", action="store_true")
    v.add_argument("--render", action="store_true")
    v.add_argument("--json", action="store_true")
    v.add_argument("--report-dir")
    args = parser.parse_args(argv)

    target = Path(args.path)
    if not target.exists():
        print(f"Không tìm thấy đường dẫn: {target}", file=sys.stderr)
        return 1
    if args.report_dir:
        report_dir = Path(args.report_dir)
        if is_inside(report_dir, target):
            print(f"Thư mục báo cáo {report_dir} nằm bên trong đích kiểm chứng {target}; "
                  "chọn --report-dir ở ngoài", file=sys.stderr)
            return 1
    else:
        try:
            report_dir = default_report_dir(target)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
    opts = VerifyOptions(runtime=args.runtime, render=args.render, kind=args.kind)
    # Một số module được nạp khi chạy cổng (vd. core/llm.py) in ra stdout lúc import:
    # dồn sang stderr để stdout chỉ còn kết quả (JSON thuần với --json).
    with contextlib.redirect_stdout(sys.stderr):
        report = verify_path(target, opts)
    report_dir = write_report(report, report_dir)
    print(report.to_json() if args.json else _summary(report, report_dir))
    return report.exit_code
