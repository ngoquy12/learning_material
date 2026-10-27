"""Bộ chạy thật cho cổng `--runtime`: Vitest, MySQL tạm, trình duyệt.

`ToolUnavailable`: máy thiếu công cụ (npm, mysqld, Playwright, Chrome) → cổng báo `skipped`.
`RunnerError`: công cụ có nhưng chạy hỏng hoặc quá thời gian → cổng báo `error`.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CACHE_ROOT = REPO / "storage" / "harness_cache"


class ToolUnavailable(Exception):
    """Thiếu công cụ cần cho bước chạy thật."""


class RunnerError(Exception):
    """Bước chạy thật thất bại (cài đặt lỗi, quá thời gian, tiến trình chết)."""
