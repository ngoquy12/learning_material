"""CLI `python -m core.harness`: verify, init, plan, status, next (spec 4.4)."""
from __future__ import annotations

import argparse
import contextlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from core.harness import state as st
from core.harness.course_spec import SpecError, load_spec
from core.harness.gates import GATES
from core.harness.options import VerifyOptions
from core.harness.planner import PlanError, build_tasks
from core.harness.report_io import default_report_dir, is_inside, write_report
from core.harness.spec_init import write_spec
from core.harness.verify import _summary, verify_path

_STATUS_ORDER = ("done", "missing", "failed", "blocked_tool")
_RUNTIME_GATES = {"exercise", "slide_html"}
_EXISTENCE_NOTE = "Cổng tồn tại: đạt khi tệp đích tồn tại và không rỗng; không có lệnh verify riêng"


class _UserError(Exception):
    """Lỗi do đầu vào của người dùng: in thông báo ra stderr, mã 1, không traceback."""

    def __init__(self, messages: list[str]):
        super().__init__("; ".join(messages))
        self.messages = messages


def _positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"phải là số nguyên: {text}") from None
    if value < 1:
        raise argparse.ArgumentTypeError(f"phải >= 1: {text}")
    return value


def _build_parser() -> argparse.ArgumentParser:
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

    i = sub.add_parser("init", help="dựng course_spec.yaml nháp từ thư mục môn đã có")
    i.add_argument("course_dir")
    i.add_argument("--force", action="store_true", help="ghi đè course_spec.yaml đã có")

    p = sub.add_parser("plan", help="in nhiệm vụ theo đợt, không chạy cổng")
    p.add_argument("spec")
    p.add_argument("--json", action="store_true")

    s = sub.add_parser("status", help="chạy cổng, ghi state.json, in bảng trạng thái")
    s.add_argument("spec")
    s.add_argument("--runtime", action="store_true")
    s.add_argument("--json", action="store_true")

    n = sub.add_parser("next", help="in nhiệm vụ sẵn sàng")
    n.add_argument("spec")
    n.add_argument("--limit", type=_positive_int)
    n.add_argument("--json", action="store_true")
    n.add_argument("--cached", action="store_true",
                   help="dùng lại state.json nếu còn mới (đặc tả chưa sửa sau lần tính trước)")
    return parser


# ---------------------------------------------------------------- verify

def _cmd_verify(args) -> int:
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


# ---------------------------------------------------------------- init / plan

def _cmd_init(args) -> int:
    try:
        path = write_spec(Path(args.course_dir), force=args.force)
    except (OSError, ValueError) as exc:  # FileExistsError, NotADirectoryError là OSError
        raise _UserError([str(exc)]) from exc
    print(f"Đã ghi đặc tả nháp: {path}")
    return 0


def _load(spec_path: Path):
    try:
        return load_spec(spec_path)
    except SpecError as exc:
        raise _UserError([f"Đặc tả không hợp lệ: {spec_path}", *exc.messages]) from exc


def _cmd_plan(args) -> int:
    spec_path = Path(args.spec)
    spec = _load(spec_path)
    course_dir = spec_path.parent.resolve()
    try:
        tasks = build_tasks(spec, course_dir)
    except PlanError as exc:
        raise _UserError([str(exc)]) from exc
    rows = [{
        "id": t.id, "kind": t.kind, "gate": t.gate, "skill": t.skill, "wave": t.wave,
        "depends_on": list(t.depends_on),
        "target": str(t.target) if t.target else str(course_dir / t.target_hint),
        "exists": t.target is not None,
    } for t in tasks]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    for r in rows:
        deps = f"  ← {', '.join(r['depends_on'])}" if r["depends_on"] else ""
        print(f"[{r['wave']}] {r['id']}  {r['kind']}  {r['target']}{deps}")
    print(f"Tổng: {len(rows)} nhiệm vụ, {max((r['wave'] for r in rows), default=0)} đợt")
    return 0


# ---------------------------------------------------------------- status / next

def _compute(spec_path: Path, runtime: bool) -> st.StateSnapshot:
    try:
        # Một số module được nạp khi chạy cổng in ra stdout lúc import: dồn sang stderr.
        with contextlib.redirect_stdout(sys.stderr):
            snap = st.compute_status(spec_path, runtime=runtime, verify=st.verify_path)
    except SpecError as exc:
        raise _UserError([f"Đặc tả không hợp lệ: {spec_path}", *exc.messages]) from exc
    except PlanError as exc:
        raise _UserError([str(exc)]) from exc
    except OSError as exc:
        raise _UserError([f"Không đọc được thư mục môn: {exc}"]) from exc
    try:
        st.save_state(snap)
    except OSError as exc:  # vd. không ghi được storage/harness/<course_id>/
        raise _UserError([f"Không ghi được tệp trạng thái: {exc}"]) from exc
    return snap


def _target_of(t: st.TaskState, course_dir: Path) -> str:
    return t.target or str(course_dir / t.target_hint)


def _counts(snap: st.StateSnapshot) -> dict[str, int]:
    c = Counter(t.status for t in snap.tasks.values())
    return {k: c.get(k, 0) for k in _STATUS_ORDER}


def _cmd_status(args) -> int:
    spec_path = Path(args.spec)
    snap = _compute(spec_path, args.runtime)
    code = st.status_exit_code(snap)
    path = st.state_path(snap.course_id)
    counts = _counts(snap)
    if args.json:
        data = json.loads(snap.to_json())
        print(json.dumps({"counts": counts, "exit_code": code, "state_path": str(path), **data},
                         ensure_ascii=False, indent=2))
        return code
    course_dir = spec_path.parent.resolve()
    print(f"Tổng {len(snap.tasks)} nhiệm vụ  " + "  ".join(f"{k}: {v}" for k, v in counts.items()))
    for t in sorted(snap.tasks.values(), key=lambda t: (t.wave, t.id)):
        if t.status != "done":
            line = f"[{t.status}] {t.id}  {_target_of(t, course_dir)}"
            print(f"{line}  {t.first_error}" if t.first_error else line)
    print(f"Trạng thái tính lúc {snap.updated_at}")
    print(f"Trạng thái: {path}")
    return code


def _is_stale(snap: st.StateSnapshot | None, spec, spec_path: Path) -> bool:
    if snap is None or snap.course_id != spec.course_id:
        return True
    if Path(snap.spec_path).resolve() != spec_path.resolve():
        return True
    try:
        updated = datetime.fromisoformat(snap.updated_at)
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)
        mtime = datetime.fromtimestamp(spec_path.stat().st_mtime, tz=timezone.utc)
    except (ValueError, OSError):
        return True
    # updated_at chỉ chính xác tới giây: so ở cùng độ chính xác.
    return mtime.replace(microsecond=0) > updated


_RENAME_NOTE = "Đích là mẫu chưa có tệp/thư mục thật: đổi đường dẫn sau khi tạo"


def _is_pattern_missing(t: st.TaskState) -> bool:
    return not t.target and any(m in t.target_hint.rsplit("/", 1)[-1] for m in ("...", "*"))


def _verify_command(t: st.TaskState, target: str) -> str:
    if t.kind not in GATES:
        return ""
    cmd = f'python -m core.harness verify "{target}" --kind {t.kind}'
    return cmd + " --runtime" if t.kind in _RUNTIME_GATES else cmd


def _block(t: st.TaskState, course_dir: Path, notes: str) -> dict:
    target = _target_of(t, course_dir)
    command = _verify_command(t, target)
    return {
        "id": t.id, "kind": t.kind, "wave": t.wave, "target": target, "status": t.status,
        "skill": f"skills/{t.skill}/SKILL.md", "depends_on": list(t.depends_on), "notes": notes,
        "allowed": list(t.allowed), "forbidden": list(t.forbidden), "first_error": t.first_error,
        "verify_command": command,
        "verify_note": _EXISTENCE_NOTE if not command else (_RENAME_NOTE if _is_pattern_missing(t) else ""),
    }


def _print_block(b: dict) -> None:
    print(f"== [{b['wave']}] {b['id']} ({b['kind']}, {b['status']})")
    print(f"   Đích: {b['target']}")
    print(f"   Skill: {b['skill']}")
    print(f"   Phụ thuộc: {', '.join(b['depends_on']) or '(không)'}")
    if b["notes"]:
        print(f"   Ghi chú môn: {b['notes']}")
    if b["allowed"]:
        print(f"   Được dạy: {', '.join(b['allowed'])}")
    if b["forbidden"]:
        print(f"   Không được dạy: {', '.join(b['forbidden'])}")
    if b["first_error"]:
        print(f"   Lỗi đầu tiên: {b['first_error']}")
    print(f"   Kiểm: {b['verify_command'] or b['verify_note']}")


def _cmd_next(args) -> int:
    spec_path = Path(args.spec)
    spec = _load(spec_path)
    snap = st.load_state(spec.course_id) if args.cached else None
    if snap is None or _is_stale(snap, spec, spec_path):
        snap = _compute(spec_path, runtime=False)  # luôn tĩnh; kiểm runtime dùng `status --runtime`
    course_dir = spec_path.parent.resolve()
    notes = str((course_dir / spec.notes).resolve()) if spec.notes else ""
    ready = st.ready_tasks(snap)
    if args.limit:
        ready = ready[:args.limit]
    blocks = [_block(t, course_dir, notes) for t in ready]
    if args.json:
        print(json.dumps({"updated_at": snap.updated_at, "tasks": blocks}, ensure_ascii=False, indent=2))
        return 0
    print(f"Trạng thái tính lúc {snap.updated_at}")
    if not blocks:
        done = all(t.status == "done" for t in snap.tasks.values())
        print("Mọi nhiệm vụ đã xong." if done else
              "Không có nhiệm vụ sẵn sàng; chạy `status` để xem nhiệm vụ đang chờ.")
        return 0
    for b in blocks:
        _print_block(b)
    return 0


_COMMANDS = {"verify": _cmd_verify, "init": _cmd_init, "plan": _cmd_plan,
             "status": _cmd_status, "next": _cmd_next}


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    args = _build_parser().parse_args(argv)
    try:
        return _COMMANDS[args.command](args)
    except _UserError as exc:
        for msg in exc.messages:
            print(msg, file=sys.stderr)
        return 1
