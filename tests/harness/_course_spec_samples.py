"""Mẫu đặc tả môn dùng chung cho các test của course_spec và lịch nhiệm vụ."""
from __future__ import annotations

from pathlib import Path

import yaml

VALID = {
    "course_id": "demo",
    "title": "Môn demo",
    "tech_stack": "javascript",
    "sessions": [
        {
            "folder": "Session 01 - Ly thuyet",
            "kind": "theory",
            "resources": ["quiz_session", "exercises", "slide_html"],
            "exercises": 2,
            "lessons": [
                {"folder": "Lesson 01 - Tong quan", "title": "Tổng quan"},
                {"folder": "Lesson 02 - Chi tiet"},
            ],
        },
        {
            "folder": "Session 02 - Thuc hanh",
            "kind": "practice",
            "resources": ["lab", "exercises"],
            "exercises": 2,
        },
    ],
}


def write_yaml(directory: Path, data) -> Path:
    path = directory / "course_spec.yaml"
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def make_course_tree(root: Path, data: dict = VALID) -> Path:
    """Tạo cây thư mục rỗng khớp đặc tả (session/lesson); trả về thư mục môn."""
    course = root / data["course_id"]
    for session in data["sessions"]:
        (course / session["folder"]).mkdir(parents=True, exist_ok=True)
        for lesson in session.get("lessons", []):
            (course / session["folder"] / lesson["folder"]).mkdir(parents=True, exist_ok=True)
    return course
