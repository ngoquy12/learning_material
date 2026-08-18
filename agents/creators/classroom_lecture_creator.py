"""
agents/creators/classroom_lecture_creator.py
Facade and Adapter for Classroom Lecture Presentation Generation (HTML).
Exposes classroom_lecture_agent and classroom_lecture_generator_agent.
"""

from typing import Dict, Any, List, Optional
from agents.classroom_lecture_generator_agent import (
    ClassroomLectureGeneratorAgent,
    classroom_lecture_generator_agent,
)

def classroom_lecture_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes classroom lecture generation from state, extracting core_ssot / lesson info,
    and returning updated state with 'lecture_html' and 'slide_html'.
    """
    core_ssot = state.get("core_ssot") or {}
    session_title = core_ssot.get("session_title") or state.get("session_id", "Session 01")
    module_name = core_ssot.get("course_name") or state.get("tech_stack", "Khóa học Công nghệ")
    
    session_lessons = core_ssot.get("session_lessons") or []
    lessons_data = []
    
    if session_lessons:
        for idx, l in enumerate(session_lessons, 1):
            ltitle = l if isinstance(l, str) else l.get("title", f"Bài {idx}")
            lessons_data.append({
                "lesson_id": f"Lesson {idx:02d}",
                "lesson_title": ltitle,
                "scenes": [
                    {
                        "action_title": "Đặt vấn đề & Thực tế",
                        "scene_title": ltitle,
                        "bullets": [f"Tổng quan và ứng dụng thực tiễn của {ltitle}."],
                        "layout_type": "THEORY"
                    }
                ]
            })
    else:
        lessons_data = [{
            "lesson_id": state.get("lesson_id", "Lesson 01"),
            "lesson_title": state.get("lesson_title", session_title),
            "scenes": [
                {
                    "action_title": "Khái niệm cốt lõi",
                    "scene_title": state.get("lesson_title", session_title),
                    "bullets": ["Quy chuẩn thực thi và các điểm lưu ý kỹ thuật."],
                    "layout_type": "THEORY"
                }
            ]
        }]
        
    html = classroom_lecture_generator_agent.generate_session_deck_html(
        session_title=session_title,
        module_name=module_name,
        lessons_data=lessons_data,
        core_ssot=core_ssot
    )
    
    new_state = dict(state)
    new_state["lecture_html"] = html
    new_state["slide_html"] = html
    return new_state

# Backwards compatibility alias
slide_agent = classroom_lecture_agent

__all__ = [
    "ClassroomLectureGeneratorAgent",
    "classroom_lecture_generator_agent",
    "classroom_lecture_agent",
    "slide_agent",
]
