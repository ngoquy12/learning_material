"""Test dựng đặc tả nháp từ thư mục môn có sẵn."""
from __future__ import annotations

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
    assert "lessons" not in s2 or s2["lessons"] == []


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
