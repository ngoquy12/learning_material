"""Nhận diện loại tài nguyên học liệu theo cấu trúc thư mục (spec 4.2).

Nhận diện theo tên thư mục cha và tên tệp, sau khi bỏ dấu tiếng Việt và
không phân biệt hoa thường; không phụ thuộc tên môn.
"""
from __future__ import annotations

import os
import re
import unicodedata
from pathlib import Path

KINDS = (
    "reading", "slide_pptx", "slide_html",
    "quiz_lesson", "quiz_session", "exercise", "lab",
)

SKIP_DIRS = frozenset({"node_modules", ".git", "screenshots", "tai_lieu_giang_vien"})
_EXERCISE_RE = re.compile(r"^\d+_")
_QUIZ_DIR_KIND = {"quizz lesson": "quiz_lesson", "quizz session": "quiz_session"}
_QUIZ_SUFFIXES = (".md", ".xlsx")


def normalize_name(name: str) -> str:
    """Bỏ dấu (NFD, bỏ dấu kết hợp, đ -> d) và casefold."""
    decomposed = unicodedata.normalize("NFD", name.replace("đ", "d").replace("Đ", "D"))
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return stripped.casefold()


def _quiz_dir_kind(directory: Path) -> str | None:
    return _QUIZ_DIR_KIND.get(normalize_name(directory.name))


def _is_exercise_dir(path: Path) -> bool:
    return bool(_EXERCISE_RE.match(path.name)) and normalize_name(path.parent.name) == "bai tap"


def detect_kind(path: Path) -> str | None:
    """Trả loại tài nguyên của một thư mục (bài tập, quiz) hoặc tệp, hoặc None."""
    path = Path(path)
    if path.is_dir():
        if _is_exercise_dir(path):
            return "exercise"
        return _quiz_dir_kind(path)
    name = normalize_name(path.name)
    if name.startswith("~$"):
        return None
    parent = normalize_name(path.parent.name)
    suffix = Path(name).suffix
    if parent == "bai doc" and suffix == ".html":
        return "reading"
    if parent == "slide bai giang" and suffix == ".pptx":
        return "slide_pptx"
    if parent == "bai giang tren lop" and name == "slides.html":
        return "slide_html"
    if parent == "bai thuc hanh" and name == "lab_guide.md":
        return "lab"
    quiz_kind = _QUIZ_DIR_KIND.get(parent)
    if quiz_kind == "quiz_lesson" and (name == "quiz.md" or suffix == ".xlsx"):
        return quiz_kind
    if quiz_kind == "quiz_session" and suffix in _QUIZ_SUFFIXES:
        return quiz_kind
    return None


def _has_quiz_files(directory: Path) -> bool:
    return any(
        child.is_file() and child.suffix.lower() in _QUIZ_SUFFIXES and not child.name.startswith("~$")
        for child in directory.iterdir()
    )


def discover(root: Path) -> tuple[list[tuple[str, Path]], list[Path]]:
    """Duyệt cây môn học: (các đích có kind, các tệp không nhận diện được)."""
    root = Path(root)
    found: list[tuple[str, Path]] = []
    unknown: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        keep: list[str] = []
        for d in sorted(dirnames):
            if normalize_name(d) in SKIP_DIRS:
                continue
            child = current / d
            if _is_exercise_dir(child):
                found.append(("exercise", child))
                continue
            quiz_kind = _quiz_dir_kind(child)
            if quiz_kind and _has_quiz_files(child):
                found.append((quiz_kind, child))
                continue
            keep.append(d)
        dirnames[:] = keep
        siblings = {f.casefold() for f in filenames}
        for f in sorted(filenames):
            file_path = current / f
            kind = detect_kind(file_path)
            if kind:
                found.append((kind, file_path))
            elif (
                f.lower().endswith(".md")
                and f"{Path(f).stem}.html".casefold() in siblings
                and normalize_name(current.name) == "bai doc"
            ):
                continue  # reading.md đi kèm reading.html
            else:
                unknown.append(file_path)
    return found, unknown
