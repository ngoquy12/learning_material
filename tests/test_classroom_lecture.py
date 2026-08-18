"""
tests/test_classroom_lecture.py -> Classroom Lecture HTML Deck Tests.
"""

import os
import pytest
from agents.classroom_lecture_generator_agent import classroom_lecture_generator_agent
from agents.creators.classroom_lecture_creator import classroom_lecture_agent, slide_agent



def test_classroom_lecture_generator_html_basic(tmp_path):
    """Verify Classroom Lecture Agent compiles full HTML lecture presentation."""
    session_dir = tmp_path / "Session_01"
    session_dir.mkdir()

    mock_lessons_data = [
        {
            "lesson_id": "Lesson 01",
            "lesson_title": "Cài đặt và cấu hình Git",
            "scenes": [
                {
                    "title": "Scene 1: Bối cảnh",
                    "action_title": "Đặt vấn đề",
                    "scene_title": "Bối cảnh thực tế",
                    "layout_type": "THEORY",
                    "bullets": ["Giới thiệu hệ thống VCS."]
                },
                {
                    "title": "Scene 2: Thao tác",
                    "action_title": "Thực chiến",
                    "scene_title": "Cấu hình Git Config",
                    "layout_type": "CODE",
                    "code_sample": "$ git config --global user.name 'Dev'"
                },
                {
                    "title": "Scene 3: Lưu ý",
                    "action_title": "Quy chuẩn",
                    "scene_title": "Lỗi thường gặp",
                    "layout_type": "GOOD_BAD_COMPARISON",
                    "bad_practice": {"title": "Lỗi", "code": "$ git init .", "reason": "Lý do."},
                    "good_practice": {"title": "Chuẩn", "code": "$ git init", "reason": "Lý do."}
                }
            ]
        }
    ]

    html = classroom_lecture_generator_agent.generate_lecture(
        session_id="Session 01",
        session_title="Tổng quan Git và Cấu trúc Repository",
        session_dir_path=str(session_dir),
        tech_stack="Git VCS CLI",
        previous_lessons_text="BÀI HỌC 01: Cài đặt và cấu hình Git",
        lessons_data=mock_lessons_data
    )

    assert isinstance(html, str)
    assert len(html) > 3000
    assert "glass-card" in html or "slides-container" in html
    assert "Cài đặt và cấu hình Git" in html
    
    out_file = session_dir / "Bài giảng trên lớp" / "slides.html"
    assert out_file.exists()
    assert out_file.stat().st_size > 3000


def test_slide_creator_multi_lesson_agenda():
    """Verify Agenda Slide in HTML deck contains all multi-lesson items."""
    state = {
        "session_id": "Session 02",
        "lesson_id": "Lesson 01",
        "tech_stack": "Git VCS CLI Terminal",
        "core_ssot": {
            "course_name": "Quản lý phiên bản với Git",
            "session_title": "Session 02: Cấu trúc kho chứa và Lệnh Git CLI cơ bản",
            "session_lessons": [
                "Cấu trúc thư mục .git và Working Tree",
                "Thao tác Staging Area và Git Commit",
                "Kiểm tra lịch sử Git Log và Restore phiên bản"
            ],
            "concepts": {
                "Working Tree": "Thư mục làm việc",
                "Staging Area": "Vùng đệm lưu vết"
            }
        }
    }

    res_state = slide_agent(state)
    html = res_state["slide_html"]

    # Verify Agenda Slide contains ALL 3 multi-lesson items
    assert "Cấu trúc thư mục .git và Working Tree" in html
    assert "Thao tác Staging Area và Git Commit" in html
    assert "Kiểm tra lịch sử Git Log và Restore phiên bản" in html


def test_lecture_ui_reviewer_audit(tmp_path):
    """Verify ClassroomLectureUIReviewerAgent audits an HTML lecture and generates audit reports."""
    from agents.lecture_ui_reviewer_agent import lecture_ui_reviewer_agent

    mock_html = """<!doctype html>
<html lang="vi">
  <head><title>Test Lecture</title></head>
  <body>
    <h1>1. Giới thiệu</h1>
    <div id="test-trace">Ready</div>
  </body>
</html>"""
    html_file = tmp_path / "index.html"
    html_file.write_text(mock_html, encoding="utf-8")

    report = lecture_ui_reviewer_agent.review_lecture_ui(
        html_path=str(html_file),
        session_title="Session Test",
        tech_stack="JavaScript Vanilla"
    )

    assert isinstance(report, dict)
    assert "ui_score" in report
    assert "passed" in report
    assert (tmp_path / "lecture_ui_review_report.json").exists()
    assert (tmp_path / "lecture_ui_review_report.md").exists()
