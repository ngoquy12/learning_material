"""Ghi báo cáo verify ra thư mục (report.json, report.md)."""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from core.harness.findings import Report
from core.harness.registry import normalize_name

REPORT_ROOT = Path(__file__).resolve().parents[2] / "storage" / "harness_reports"


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9_-]", "", normalize_name(name).replace(" ", "_")) or "target"


def write_report(report: Report, report_dir: Path | None = None) -> Path:
    """Ghi report.json và report.md; trả thư mục đã ghi."""
    if report_dir is None:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_dir = REPORT_ROOT / f"{stamp}_{_slug(Path(report.target).name)}"
    report_dir = Path(report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "report.json").write_text(report.to_json(), encoding="utf-8")
    (report_dir / "report.md").write_text(report.to_markdown(), encoding="utf-8")
    return report_dir
