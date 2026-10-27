"""Dựng đặc tả môn nháp (course_spec.yaml) từ thư mục môn đã có (spec 4.4)."""
from __future__ import annotations

import os
import re
from pathlib import Path

import yaml

from core.harness.course_spec import LESSON_RESOURCES, SESSION_RESOURCES
from core.harness.planner import resolve_target
from core.harness.registry import SKIP_DIRS, normalize_name

SPEC_NAME = "course_spec.yaml"
_EXERCISE_RE = re.compile(r"^(\d+)_")


def _subdirs(parent: Path, prefix: str) -> list[Path]:
    found = [
        p for p in parent.iterdir()
        if p.is_dir()
        and not p.name.startswith(".")
        and normalize_name(p.name) not in SKIP_DIRS
        and normalize_name(p.name).startswith(prefix)
    ]
    return sorted(found, key=lambda p: normalize_name(p.name))


def _has(base: Path, name: str, pattern: str | None = None) -> bool:
    return resolve_target(base, [name], pattern) is not None


def _title(folder: str) -> str:
    _, sep, rest = folder.partition(" - ")
    return rest.strip() if sep else ""


def _lesson_resources(lesson: Path) -> list[str]:
    present = {
        "reading": _has(lesson, "Bai doc"),
        "reading_questions": _has(lesson, "Cau hoi bai doc"),
        "quiz_lesson": _has(lesson, "Quizz lesson"),
    }
    return [r for r in LESSON_RESOURCES if present[r]]


def _exercise_count(session: Path) -> int:
    bai_tap = resolve_target(session, ["Bai tap"])
    if bai_tap is None or not bai_tap.is_dir():
        return 0
    numbers = [
        int(m.group(1)) for p in bai_tap.iterdir()
        if p.is_dir() and (m := _EXERCISE_RE.match(p.name))
    ]
    for n in sorted(set(numbers), reverse=True):
        if resolve_target(session, ["Bai tap"], f"^{n}_") is not None:
            return n
    return 0


def _draft_session(session: Path) -> dict:
    exercises = _exercise_count(session)
    present = {
        "quiz_session": _has(session, "Quizz session"),
        "exercises": exercises > 0,
        "slide_html": _has(session, "Bai giang tren lop"),
        "slide_pptx": _has(session, "Slide bai giang"),
        "mindmap": _has(session, "So do tu duy"),
        "lab": _has(session, "Bai thuc hanh"),
    }
    out: dict = {"folder": session.name}
    if present["lab"]:
        out["kind"] = "practice"
    out["resources"] = [r for r in SESSION_RESOURCES if present[r]]
    if exercises:
        out["exercises"] = exercises
    lessons = []
    for lesson in _subdirs(session, "lesson"):
        item: dict = {"folder": lesson.name}
        title = _title(lesson.name)
        if title:
            item["title"] = title
        res = _lesson_resources(lesson)
        if res != list(LESSON_RESOURCES):
            item["resources"] = res
        lessons.append(item)
    if lessons:
        out["lessons"] = lessons
    return out


def draft_spec(course_dir: Path) -> dict:
    course_dir = Path(course_dir)
    if not course_dir.is_dir():
        raise NotADirectoryError(f"Không tìm thấy thư mục môn: {course_dir}")
    course_dir = course_dir.resolve()
    sessions = _subdirs(course_dir, "session")
    if not sessions:
        raise ValueError(f"Không tìm thấy thư mục Session nào trong {course_dir}")
    return {
        "course_id": course_dir.name,
        "title": course_dir.name,
        "tech_stack": "",
        "notes": "course_spec.md" if (course_dir / "course_spec.md").is_file() else "",
        "sessions": [_draft_session(x) for x in sessions],
    }


def write_spec(course_dir: Path, force: bool = False) -> Path:
    course_dir = Path(course_dir)
    path = course_dir / SPEC_NAME
    if path.exists() and not force:
        raise FileExistsError(f"Đã có tệp {path}; dùng --force để ghi đè")
    text = yaml.safe_dump(draft_spec(course_dir), allow_unicode=True, sort_keys=False)
    tmp = path.with_name(path.name + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8", newline="\n")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
    return path
