"""Lập kế hoạch nhiệm vụ theo đợt từ đặc tả môn (spec 4.2)."""
from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field
from pathlib import Path

from core.harness.course_spec import CourseSpec, SessionSpec
from core.harness.registry import SKIP_DIRS, normalize_name


@dataclass
class Task:
    id: str
    kind: str
    gate: str | None
    skill: str
    target: Path | None
    target_hint: str
    depends_on: list[str] = field(default_factory=list)
    wave: int = 1
    session_index: int = 0
    lesson_index: int | None = None
    allowed: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)


class PlanError(Exception):
    pass


def _skipped(name: str) -> bool:
    return name.startswith("~$") or normalize_name(name) in SKIP_DIRS


def resolve_target(course_dir: Path, parts: list[str], pattern: str | None = None) -> Path | None:
    """Đi từng phần theo normalize_name; phần cuối có thể là mẫu (`*.pptx`, `^3_`)."""
    current = Path(course_dir)
    for part in parts:
        if not current.is_dir():
            return None
        key = normalize_name(part)
        match = next(
            (c for c in sorted(current.iterdir(), key=lambda p: p.name)
             if normalize_name(c.name) == key and not _skipped(c.name)),
            None,
        )
        if match is None:
            return None
        current = match
    if pattern is None:
        return current
    if not current.is_dir():
        return None
    is_regex = pattern.startswith("^")
    glob = normalize_name(pattern)
    for child in sorted(current.iterdir(), key=lambda p: normalize_name(p.name)):
        if _skipped(child.name):
            continue
        name = normalize_name(child.name)
        if is_regex:
            if child.is_dir() and re.match(pattern, name):
                return child
        elif child.is_file() and fnmatch.fnmatchcase(name, glob):
            return child
    return None


def _disk_hint(course_dir: Path, hint_parts: list[str]) -> str:
    """Gợi ý đường dẫn: dùng tên thật trên đĩa cho phần tiền tố đã có, phần còn lại giữ theo đặc tả."""
    out: list[str] = []
    current: Path | None = Path(course_dir)
    for part in hint_parts:
        match = None
        if current is not None and current.is_dir():
            key = normalize_name(part)
            match = next(
                (c for c in sorted(current.iterdir(), key=lambda p: p.name)
                 if normalize_name(c.name) == key and not _skipped(c.name)),
                None,
            )
        out.append(match.name if match else part)
        current = match
    return "/".join(out)


def _dep_sessions(spec: CourseSpec, index: int) -> list[int]:
    session = spec.sessions[index]
    if session.depends_on_sessions is not None:
        return list(session.depends_on_sessions)
    if session.kind == "practice":
        for j in range(index - 1, -1, -1):
            if spec.sessions[j].kind == "theory":
                return [j]
    return []


def _sid(si: int) -> str:
    return f"s{si + 1:02d}"


def build_tasks(spec: CourseSpec, course_dir: Path) -> list[Task]:
    course_dir = Path(course_dir)
    tasks: list[Task] = []
    readings: dict[int, list[str]] = {}
    for si, session in enumerate(spec.sessions):
        readings[si] = [
            f"{_sid(si)}/l{li + 1:02d}/reading"
            for li, lesson in enumerate(session.lessons)
            if "reading" in spec.lesson_resources(lesson)
        ]

    def add(si, kind, gate, skill, task_id, parts, pattern, hint_parts, deps, li=None, lesson=None):
        target = resolve_target(course_dir, parts, pattern)
        tasks.append(Task(
            id=task_id, kind=kind, gate=gate, skill=skill,
            target=target.resolve() if target else None,
            target_hint=_disk_hint(course_dir, hint_parts), depends_on=list(deps),
            session_index=si, lesson_index=li,
            allowed=list(lesson.allowed) if lesson else [],
            forbidden=list(lesson.forbidden) if lesson else [],
        ))

    def session_tasks(si: int, session: SessionSpec) -> None:
        sid, f = _sid(si), session.folder
        own = readings[si]
        dep_readings = [r for d in _dep_sessions(spec, si) for r in readings[d]]
        res = session.resources
        if "quiz_session" in res:
            add(si, "quiz_session", "quiz_session", "quizz_session", f"{sid}/quiz_session",
                [f, "Quizz session"], None, [f, "Quizz session"], own)
        if "exercises" in res:
            deps = own if session.kind == "theory" else dep_readings
            for i in range(1, session.exercises + 1):
                add(si, "exercise", "exercise", "exercise_generator", f"{sid}/exercise_{i}",
                    [f, "Bai tap"], f"^{i}_", [f, "Bai tap", f"{i}_..."], deps)
        if "slide_html" in res:
            add(si, "slide_html", "slide_html", "slide_html", f"{sid}/slide_html",
                [f, "Bai giang tren lop", "slides.html"], None,
                [f, "Bai giang tren lop", "slides.html"], own)
        if "slide_pptx" in res:
            add(si, "slide_pptx", "slide_pptx", "slide_deck", f"{sid}/slide_pptx",
                [f, "Slide bai giang"], "*.pptx", [f, "Slide bai giang", "*.pptx"], own)
        if "mindmap" in res:
            add(si, "mindmap", None, "session_mindmap_compiler", f"{sid}/mindmap",
                [f, "So do tu duy", "mindmap.md"], None, [f, "So do tu duy", "mindmap.md"], own)
        if "lab" in res:
            add(si, "lab", "lab", "lab_generator", f"{sid}/lab",
                [f, "Bai thuc hanh", "lab_guide.md"], None,
                [f, "Bai thuc hanh", "lab_guide.md"], dep_readings)

    for si, session in enumerate(spec.sessions):
        for li, lesson in enumerate(session.lessons):
            res = spec.lesson_resources(lesson)
            lid = f"{_sid(si)}/l{li + 1:02d}"
            base = [session.folder, lesson.folder]
            reading_id = f"{lid}/reading"
            deps = [reading_id] if "reading" in res else []
            if "reading" in res:
                add(si, "reading", "reading", "reading_generator", reading_id,
                    base + ["Bai doc", "reading.html"], None,
                    base + ["Bai doc", "reading.html"], [], li, lesson)
            if "reading_questions" in res:
                add(si, "reading_questions", None, "reading_questions_generator",
                    f"{lid}/reading_questions",
                    base + ["Cau hoi bai doc", "reading_questions.md"], None,
                    base + ["Cau hoi bai doc", "reading_questions.md"], deps, li, lesson)
            if "quiz_lesson" in res:
                add(si, "quiz_lesson", "quiz_lesson", "quiz_generator", f"{lid}/quiz_lesson",
                    base + ["Quizz lesson"], None, base + ["Quizz lesson"], deps, li, lesson)
        session_tasks(si, session)

    _assign_waves(tasks)
    tasks.sort(key=lambda t: (t.wave, t.id))
    return tasks


def _assign_waves(tasks: list[Task]) -> None:
    by_id = {t.id: t for t in tasks}
    state: dict[str, int] = {}  # 1 = đang duyệt, 2 = xong

    def visit(task: Task, chain: list[str]) -> int:
        if state.get(task.id) == 2:
            return task.wave
        if state.get(task.id) == 1:
            raise PlanError("Phát hiện chu trình phụ thuộc: " + " -> ".join([*chain, task.id]))
        state[task.id] = 1
        wave = 1
        for dep in task.depends_on:
            if dep not in by_id:
                raise PlanError(f"Nhiệm vụ {task.id} phụ thuộc vào {dep} không tồn tại")
            wave = max(wave, visit(by_id[dep], [*chain, task.id]) + 1)
        task.wave = wave
        state[task.id] = 2
        return wave

    for task in tasks:
        visit(task, [])
