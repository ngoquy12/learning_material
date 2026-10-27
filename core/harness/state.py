"""Trạng thái nhiệm vụ: chạy cổng kiểm chứng trên đích của từng nhiệm vụ và lưu ảnh chụp (spec 4.3)."""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Literal

from core.harness.course_spec import load_spec
from core.harness.options import VerifyOptions
from core.harness.planner import build_tasks
from core.harness.verify import verify_path

Status = Literal["missing", "failed", "blocked_tool", "done"]

STATE_ROOT = Path(__file__).resolve().parents[2] / "storage" / "harness"
_STATUSES = {"missing", "failed", "blocked_tool", "done"}
_RUNTIME_GATES = {"exercise", "slide_html"}


@dataclass
class TaskState:
    id: str
    kind: str
    status: Status
    target: str
    target_hint: str
    wave: int
    depends_on: list[str] = field(default_factory=list)
    errors: int = 0
    warnings: int = 0
    first_error: str = ""
    checked_at: str = ""
    skill: str = ""
    allowed: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)


@dataclass
class StateSnapshot:
    course_id: str
    spec_path: str
    updated_at: str
    runtime: bool
    tasks: dict[str, TaskState] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, text: str) -> "StateSnapshot":
        data = json.loads(text)
        raw = data["tasks"]
        if not isinstance(raw, dict):
            raise ValueError("tasks phải là dict")
        tasks = {}
        for k, v in raw.items():
            if (not isinstance(v, dict) or v.get("status") not in _STATUSES
                    or not isinstance(v.get("depends_on", []), list)):
                raise ValueError(f"nhiệm vụ {k} không hợp lệ")
            tasks[k] = TaskState(**v)
        return cls(course_id=data["course_id"], spec_path=data["spec_path"],
                   updated_at=data["updated_at"], runtime=data["runtime"], tasks=tasks)


def state_path(course_id: str) -> Path:
    return STATE_ROOT / course_id / "state.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _is_empty(target: Path) -> bool:
    if target.is_dir():
        return not any(target.iterdir())
    return target.stat().st_size == 0


def _check(task, runtime: bool, verify: Callable) -> dict:
    target = task.target
    if target is None or not target.exists() or _is_empty(target):
        return {"status": "missing"}
    if task.gate is None:
        return {"status": "done"}
    opts = VerifyOptions(kind=task.gate, runtime=runtime and task.gate in _RUNTIME_GATES)
    try:
        report = verify(target, opts)
    except Exception as exc:  # noqa: BLE001 - lỗi của cổng thành `failed`, không dừng cả lần quét
        return {"status": "failed", "errors": 1, "first_error": f"Lỗi khi kiểm chứng: {exc}"}
    findings = [f for r in report.results for f in r.findings]
    errors = [f for f in findings if f.severity == "error"]
    status = {0: "done", 1: "failed", 2: "blocked_tool"}.get(report.exit_code, "failed")
    return {"status": status, "errors": len(errors),
            "warnings": sum(1 for f in findings if f.severity == "warning"),
            "first_error": errors[0].message if errors else
            "; ".join(r.skipped_reason for r in report.results if r.skipped_reason)
            if status == "blocked_tool" else ""}


def compute_status(spec_path: Path, runtime: bool = False, verify=verify_path) -> StateSnapshot:
    """Chỉ đọc đặc tả và đích; không ghi báo cáo vào thư mục môn (verify_path không ghi tệp)."""
    spec_path = Path(spec_path)
    spec = load_spec(spec_path)
    tasks: dict[str, TaskState] = {}
    for task in build_tasks(spec, spec_path.parent):
        res = _check(task, runtime, verify)
        tasks[task.id] = TaskState(
            id=task.id, kind=task.kind, status=res["status"],
            target=str(task.target) if task.target else "", target_hint=task.target_hint,
            wave=task.wave, depends_on=list(task.depends_on),
            errors=res.get("errors", 0), warnings=res.get("warnings", 0),
            first_error=res.get("first_error", ""), checked_at=_now(),
            skill=task.skill, allowed=list(task.allowed), forbidden=list(task.forbidden))
    return StateSnapshot(course_id=spec.course_id, spec_path=str(spec_path),
                         updated_at=_now(), runtime=runtime, tasks=tasks)


def save_state(snap: StateSnapshot) -> Path:
    path = state_path(snap.course_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(snap.to_json(), encoding="utf-8")
    os.replace(tmp, path)
    return path


def load_state(course_id: str) -> StateSnapshot | None:
    try:
        return StateSnapshot.from_json(state_path(course_id).read_text(encoding="utf-8"))
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def ready_tasks(snap: StateSnapshot) -> list[TaskState]:
    ready = [t for t in snap.tasks.values() if t.status != "done"
             and all(d in snap.tasks and snap.tasks[d].status == "done" for d in t.depends_on)]
    return sorted(ready, key=lambda t: (t.wave, t.id))


def status_exit_code(snap: StateSnapshot) -> int:
    statuses = {t.status for t in snap.tasks.values()}
    if "failed" in statuses:
        return 1
    if "missing" in statuses:
        return 3
    if "blocked_tool" in statuses:
        return 2
    return 0
