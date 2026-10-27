"""Đăng ký các cổng kiểm chứng: GATES[kind] = check_<kind>(path, opts) -> GateResult."""
from __future__ import annotations

from typing import Callable

GATES: dict[str, Callable] = {}

from core.harness.gates.reading import check_reading  # noqa: E402

GATES["reading"] = check_reading
