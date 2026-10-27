"""Tùy chọn chạy kiểm chứng, dùng chung cho mọi cổng."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VerifyOptions:
    runtime: bool = False
    render: bool = False
    kind: str | None = None
