"""Điều phối kiểm chứng: verify_path và CLI `python -m core.harness verify`."""
from __future__ import annotations

import argparse
import sys
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


def verify_path(target: Path, opts: VerifyOptions) -> Report:
    target = Path(target)
    started = datetime.now().isoformat(timespec="seconds")
    results: list[GateResult] = []
    kind = opts.kind if opts.kind in GATES else detect_kind(target)
    if kind:
        results.append(_run_gate(kind, target, opts))
    elif target.is_file():
        results.append(_unknown(target, "info", _NOT_RESOURCE))
    else:
        found, unknown = discover(target)
        if not found and not unknown:
            results.append(_unknown(target, "error",
                                    "Không nhận diện được loại tài nguyên, dùng --kind"))
        for k, p in found:
            results.append(_run_gate(k, p, opts))
        for p in unknown:
            results.append(_unknown(p, "info", _NOT_RESOURCE))
    return Report(target=str(target), results=results, started_at=started)


def _summary(report: Report, report_dir: Path) -> str:
    c = report.counts()
    lines = [f"pass: {c['pass']}  fail: {c['fail']}  skipped: {c['skipped']}"]
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
    v.add_argument("--kind", choices=sorted(GATES))
    v.add_argument("--runtime", action="store_true")
    v.add_argument("--render", action="store_true")
    v.add_argument("--json", action="store_true")
    v.add_argument("--report-dir")
    args = parser.parse_args(argv)

    target = Path(args.path)
    if not target.exists():
        print(f"Không tìm thấy đường dẫn: {target}", file=sys.stderr)
        return 1
    opts = VerifyOptions(runtime=args.runtime, render=args.render, kind=args.kind)
    report = verify_path(target, opts)
    report_dir = write_report(report, Path(args.report_dir) if args.report_dir else None)
    print(report.to_json() if args.json else _summary(report, report_dir))
    return report.exit_code
