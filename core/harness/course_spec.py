"""Mô hình đặc tả môn học (course_spec.yaml), kiểm khi nạp."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from core.harness.registry import normalize_name

LESSON_RESOURCES = ("reading", "reading_questions", "quiz_lesson")
SESSION_RESOURCES = ("quiz_session", "exercises", "slide_html", "slide_pptx", "mindmap", "lab")


class SpecError(Exception):
    def __init__(self, messages: list[str]):
        super().__init__("; ".join(messages))
        self.messages = messages


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LessonSpec(_Strict):
    folder: str
    title: str = ""
    allowed: list[str] = Field(default_factory=list)
    forbidden: list[str] = Field(default_factory=list)
    resources: list[str] | None = None


class SessionSpec(_Strict):
    folder: str
    kind: Literal["theory", "practice"] = "theory"
    resources: list[str] = Field(default_factory=list)
    exercises: int = 0
    lessons: list[LessonSpec] = Field(default_factory=list)
    depends_on_sessions: list[int] | None = None


class Defaults(_Strict):
    lesson_resources: list[str] = Field(default_factory=lambda: list(LESSON_RESOURCES))


class CourseSpec(_Strict):
    course_id: str
    title: str = ""
    tech_stack: str = ""
    notes: str = ""
    defaults: Defaults = Field(default_factory=Defaults)
    sessions: list[SessionSpec]

    def lesson_resources(self, lesson: LessonSpec) -> list[str]:
        if lesson.resources is not None:
            return list(lesson.resources)
        return list(self.defaults.lesson_resources)


def _format_loc(loc: tuple) -> str:
    out = ""
    for part in loc:
        if isinstance(part, int):
            out += f"[{part}]"
        else:
            out += f".{part}" if out else str(part)
    return out


_PYDANTIC_VI = {
    "missing": "thiếu trường bắt buộc",
    "string_type": "phải là chuỗi",
    "int_type": "phải là số nguyên",
    "int_parsing": "phải là số nguyên",
    "list_type": "phải là danh sách",
    "dict_type": "phải là một đối tượng (mapping)",
    "literal_error": "giá trị không hợp lệ (không thuộc danh sách cho phép)",
    "model_type": "phải là một đối tượng (mapping)",
    "model_attributes_type": "phải là một đối tượng (mapping)",
    "bool_type": "phải là true hoặc false",
    "extra_forbidden": "khóa không hợp lệ (không có trong đặc tả)",
    "int_from_float": "phải là số nguyên",
    "string_too_short": "không được để trống",
}


def _translate(err: dict) -> str:
    loc = _format_loc(err["loc"])
    reason = _PYDANTIC_VI.get(err["type"], "giá trị không hợp lệ")
    return f"{loc}: {reason}"


def _check_resources(path: str, names: list[str], allowed: tuple[str, ...], out: list[str]) -> None:
    for name in names:
        if name not in allowed:
            out.append(f"{path}: tài nguyên '{name}' không hợp lệ, chỉ nhận: {', '.join(allowed)}")


def _check_semantics(spec: CourseSpec) -> list[str]:
    errors: list[str] = []
    if not spec.course_id.strip():
        errors.append("course_id: không được để trống")
    elif (spec.course_id in (".", "..") or "/" in spec.course_id or "\\" in spec.course_id
          or ":" in spec.course_id or Path(spec.course_id).name != spec.course_id):
        errors.append("course_id: phải là một tên đơn (không chứa dấu phân cách đường dẫn hoặc '..')")
    _check_resources("defaults.lesson_resources", spec.defaults.lesson_resources, LESSON_RESOURCES, errors)
    seen_sessions: dict[str, int] = {}
    for si, session in enumerate(spec.sessions):
        base = f"sessions[{si}]"
        key = normalize_name(session.folder)
        if key in seen_sessions:
            errors.append(
                f"{base}.folder: tên thư mục '{session.folder}' trùng với sessions[{seen_sessions[key]}]"
            )
        else:
            seen_sessions[key] = si
        _check_resources(f"{base}.resources", session.resources, SESSION_RESOURCES, errors)
        if session.exercises < 0:
            errors.append(f"{base}.exercises: không được âm")
        elif "exercises" in session.resources and session.exercises < 1:
            errors.append(f"{base}.exercises: phải >= 1 khi có tài nguyên exercises")
        for dep in session.depends_on_sessions or []:
            if not 0 <= dep < si:
                errors.append(
                    f"{base}.depends_on_sessions: chỉ số {dep} phải trỏ về session đứng trước"
                )
        seen_lessons: dict[str, int] = {}
        for li, lesson in enumerate(session.lessons):
            lbase = f"{base}.lessons[{li}]"
            lkey = normalize_name(lesson.folder)
            if lkey in seen_lessons:
                errors.append(
                    f"{lbase}.folder: tên thư mục '{lesson.folder}' trùng với {base}.lessons[{seen_lessons[lkey]}]"
                )
            else:
                seen_lessons[lkey] = li
            if lesson.resources is not None:
                _check_resources(f"{lbase}.resources", lesson.resources, LESSON_RESOURCES, errors)
    return errors


def load_spec(path: Path) -> CourseSpec:
    try:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise SpecError([f"Không đọc được tệp đặc tả {path}: {exc}"]) from exc
    except UnicodeDecodeError as exc:
        raise SpecError(["Tệp đặc tả không đúng mã hóa UTF-8"]) from exc
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        where = f" ở dòng {mark.line + 1}, cột {mark.column + 1}" if mark else ""
        raise SpecError([f"YAML sai cú pháp{where}"]) from exc
    if not isinstance(data, dict):
        raise SpecError(["Tệp đặc tả phải là một đối tượng YAML (mapping), không phải rỗng hoặc danh sách"])
    try:
        spec = CourseSpec.model_validate(data)
    except ValidationError as exc:
        raise SpecError([_translate(e) for e in exc.errors()]) from exc
    errors = _check_semantics(spec)
    if errors:
        raise SpecError(errors)
    return spec
