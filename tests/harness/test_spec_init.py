"""Test dựng đặc tả nháp từ thư mục môn có sẵn."""
from __future__ import annotations

from pathlib import Path

import pytest

from core.harness.course_spec import load_spec
from core.harness.planner import build_tasks
from core.harness.spec_init import draft_spec, write_spec
from tests.harness.conftest import write_tree


def _course(tmp_path):
    course = tmp_path / "mon_demo"
    files = {
        "course_spec.md": "ghi chu",
        "Session 02 - Thuc hanh/Bai thuc hanh/lab_guide.md": "x",
        "Session 02 - Thuc hanh/Bai tap/1_a/x.txt": "x",
        "Session 02 - Thuc hanh/Bai tap/2_b/x.txt": "x",
        "Session 01 - Ly thuyet/Quizz session/quiz.md": "x",
        "Session 01 - Ly thuyet/Bai tap/readme.md": "x",
        "Session 01 - Ly thuyet/Bai giang tren lop/slides.html": "x",
        "Session 01 - Ly thuyet/Slide bai giang/a.pptx": "x",
        "Session 01 - Ly thuyet/So do tu duy/mindmap.md": "x",
        "Session 01 - Ly thuyet/Lesson 01 - Tổng quan/Bài đọc/reading.html": "x",
        "Session 01 - Ly thuyet/Lesson 01 - Tổng quan/Câu hỏi bài đọc/reading_questions.md": "x",
        "Session 01 - Ly thuyet/Lesson 01 - Tổng quan/Quizz lesson/quiz.md": "x",
        "Session 01 - Ly thuyet/Lesson 02 - Chi tiet/Bai doc/reading.html": "x",
        "Session 01 - Ly thuyet/Lesson 02 - Chi tiet/Cau hoi bai doc/reading_questions.md": "x",
        "Session 01 - Ly thuyet/_shared/f.txt": "x",
        "Session 01 - Ly thuyet/node_modules/f.txt": "x",
    }
    write_tree(course, files)
    return course


def test_draft_fields(tmp_path):
    data = draft_spec(_course(tmp_path))
    assert data["course_id"] == "mon_demo"
    assert data["title"] == "mon_demo"
    assert data["tech_stack"] == ""
    assert data["notes"] == "course_spec.md"
    s1, s2 = data["sessions"]
    assert s1["folder"] == "Session 01 - Ly thuyet"
    assert "kind" not in s1
    assert s1["resources"] == ["quiz_session", "slide_html", "slide_pptx", "mindmap"]
    assert "exercises" not in s1
    l1, l2 = s1["lessons"]
    assert l1 == {"folder": "Lesson 01 - Tổng quan", "title": "Tổng quan"}
    assert l2["title"] == "Chi tiet"
    assert l2["resources"] == ["reading", "reading_questions"]
    assert s2["kind"] == "practice"
    assert s2["resources"] == ["exercises", "lab"]
    assert s2["exercises"] == 2
    assert "lessons" not in s2


def test_write_and_load(tmp_path):
    course = _course(tmp_path)
    path = write_spec(course)
    assert path == course / "course_spec.yaml"
    spec = load_spec(path)
    tasks = build_tasks(spec, course)
    assert tasks and all(t.target is not None for t in tasks)
    with pytest.raises(FileExistsError):
        write_spec(course)
    write_spec(course, force=True)


def test_notes_empty_without_file(tmp_path):
    course = tmp_path / "m"
    (course / "Session 01 - A").mkdir(parents=True)
    data = draft_spec(course)
    assert data["notes"] == ""
    assert data["sessions"][0]["resources"] == []


def test_relative_dot_course_id(tmp_path, monkeypatch):
    course = tmp_path / "mon_x"
    (course / "Session 01 - A").mkdir(parents=True)
    monkeypatch.chdir(course)
    data = draft_spec(Path("."))
    assert data["course_id"] == "mon_x" and data["title"] == "mon_x"


def test_missing_dir_and_file(tmp_path):
    with pytest.raises(NotADirectoryError, match="Không tìm thấy thư mục môn"):
        draft_spec(tmp_path / "khong_co")
    f = tmp_path / "f.txt"
    f.write_text("x")
    with pytest.raises(NotADirectoryError):
        draft_spec(f)


def test_no_sessions_raises_and_writes_nothing(tmp_path):
    course = tmp_path / "rong"
    course.mkdir()
    with pytest.raises(ValueError, match="Không tìm thấy thư mục Session nào"):
        write_spec(course)
    assert not (course / "course_spec.yaml").exists()


def test_exercise_numbering(tmp_path):
    padded = write_tree(tmp_path / "a", {"Session 01 - A/Bai tap/01_x/f": "x"})
    assert draft_spec(padded)["sessions"][0].get("exercises") is None
    assert "exercises" not in draft_spec(padded)["sessions"][0]["resources"]
    gap = write_tree(tmp_path / "b", {
        "Session 01 - A/Bai tap/1_x/f": "x", "Session 01 - A/Bai tap/3_y/f": "x"})
    s = draft_spec(gap)["sessions"][0]
    assert s["exercises"] == 3 and "exercises" in s["resources"]
    tasks = build_tasks(load_spec(write_spec(gap)), gap)
    assert [t.id for t in tasks if t.target is None] == ["s01/exercise_2"]


def test_folder_detection_without_files(tmp_path):
    course = tmp_path / "c"
    (course / "Session 01 - A/Bai thuc hanh").mkdir(parents=True)
    data = draft_spec(course)
    s = data["sessions"][0]
    assert s["kind"] == "practice" and s["resources"] == ["lab"]
    tasks = build_tasks(load_spec(write_spec(course)), course)
    assert [(t.kind, t.target) for t in tasks] == [("lab", None)]


def test_session_lesson_prefix_must_be_word(tmp_path):
    course = tmp_path / "c"
    (course / "Session 01 - A" / "Lesson 01 - X" / "Lessons_cu").mkdir(parents=True)
    (course / "Session 01 - A" / "Lessonx").mkdir()
    (course / "Sessions_cu").mkdir()
    data = draft_spec(course)
    assert [s["folder"] for s in data["sessions"]] == ["Session 01 - A"]
    assert [x["folder"] for x in data["sessions"][0]["lessons"]] == ["Lesson 01 - X"]
