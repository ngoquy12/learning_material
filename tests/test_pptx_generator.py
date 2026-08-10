import pytest
from agents.pptx_generator_agent import pptx_generator_agent
from agents.slide_generator_agent import slide_generator_agent
from agents.creators.slide_creator import slide_agent

def test_pptx_generator_basic():
    scenes = [
        {
            "action_title": "Đặt Vấn Đề & Bối Cảnh",
            "scene_title": "Đặt Vấn Đề",
            "short_title": "Đặt vấn đề",
            "html_content": "<div class='bento-card bg-red-500'>Test Pain Point</div>",
            "layout_type": "CUSTOM_RAW"
        },
        {
            "action_title": "Thao Tác Thực Chiến",
            "scene_title": "Thao Tác",
            "short_title": "Thao tác",
            "code_sample": "$ git status\n$ git add .\n$ git commit -m 'feat: init'",
            "layout_type": "CODE"
        }
    ]

    pptx_bytes = slide_generator_agent.generate_deck_pptx(
        lesson_title="Lesson 01: Cấu trúc kho chứa và Lệnh Git CLI cơ bản",
        module_name="Quản lý phiên bản với Git",
        scenes=scenes
    )

    assert isinstance(pptx_bytes, bytes)
    assert len(pptx_bytes) > 5000  # Valid PPTX binary data

def test_pptx_generator_save_file(tmp_path):
    out_file = str(tmp_path / "test_presentation.pptx")
    scenes = [
        {
            "action_title": "Sơ Đồ Vận Hành",
            "scene_title": "Sơ Đồ",
            "mermaid": "flowchart LR\nA --> B",
            "layout_type": "MERMAID_DIAGRAM"
        }
    ]

    pptx_bytes = pptx_generator_agent.generate_deck_pptx(
        session_title="Session 01: Tổng quan Git",
        module_name="Quản lý phiên bản với Git",
        lessons_data=[{"lesson_id": "Lesson 01", "lesson_title": "Tổng quan Git", "scenes": scenes}],
        output_path=out_file
    )

    assert len(pptx_bytes) > 3000
    import os
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 3000

def test_slide_creator_multi_lesson_agenda():
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
