"""Đăng ký các cổng kiểm chứng: GATES[kind] = check_<kind>(path, opts) -> GateResult."""
from __future__ import annotations

from typing import Callable

GATES: dict[str, Callable] = {}

from core.harness.gates.reading import check_reading  # noqa: E402

GATES["reading"] = check_reading

from core.harness.gates import quiz  # noqa: E402,F401  (dang ky quiz_lesson, quiz_session)
from core.harness.gates import lab, exercise  # noqa: E402,F401  (dang ky lab, exercise)
