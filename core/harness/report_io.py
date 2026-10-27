"""Ghi báo cáo verify ra thư mục (report.json, report.md)."""
from __future__ import annotations

import re
import tempfile
from datetime import datetime
from pathlib import Path

from core.harness.findings import Report
from core.harness.registry import normalize_name

REPORT_ROOT = Path(__file__).resolve().parents[2] / "storage" / "harness_reports"


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9_-]", "", normalize_name(name).replace(" ", "_")) or "target"


def is_inside(path: Path, root: Path) -> bool:
    """`path` nằm trong (hoặc trùng) thư mục `root`, so sau khi chuẩn hóa đường dẫn tuyệt đối."""
    root = Path(root).resolve()
    if not root.is_dir():
        return False
    path = Path(path).resolve()
    return path == root or root in path.parents


def default_report_dir(target: Path) -> Path:
    """Thư mục báo cáo mặc định; dùng thư mục tạm của hệ thống nếu REPORT_ROOT nằm trong đích kiểm chứng."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    name = f"{stamp}_{_slug(Path(target).resolve().name)}"
    if not is_inside(REPORT_ROOT, target):
        return REPORT_ROOT / name
    fallback = Path(tempfile.gettempdir()) / "harness_reports" / name
    if is_inside(fallback, target):
        raise ValueError("Thư mục báo cáo mặc định và thư mục tạm đều nằm trong đích kiểm chứng; dùng --report-dir")
    return fallback


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
