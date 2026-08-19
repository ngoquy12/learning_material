"""
agents/creators/classroom_lecture_creator.py
Modular Classroom Lecture Presentation Creator for Elearning Content Factory.
Adheres to:
- Rikkei Education Golden Slide Standards (3-30-300 rule, Bento Grid, Light Mode only).
- Jinja2 Template-driven generation (classroom_lecture.j2).
- Type-Safe Schema Validation with Pydantic v2 (ClassroomSlideDeckSchema, ClassroomSlideItemSchema).
- Zero Text Emoji & 100% Accented Vietnamese Contract.
"""

from typing import Dict, Any, List, Optional
from core.prompts import render_prompt
from core.state import require_tech_stack
from core.schemas.course_schemas import ClassroomSlideDeckSchema, ClassroomSlideItemSchema
from core.utils.schema_validator import validate_schema
from core.utils.llm_parser import extract_json_from_response
from core.llm import call_llm
from agents.classroom_lecture_generator_agent import (
    ClassroomLectureGeneratorAgent,
    classroom_lecture_generator_agent,
)

from core.domain_knowledge import get_domain_for_session, format_domain_rules_for_prompt

def generate_lecture_slide_outline(
    session_id: str,
    session_title: str,
    tech_stack: str,
    lesson_outline_text: str = "",
    course_name: str = "",
    lang_tag: str = "python",
    chosen_domain: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates structured slide presentation deck outline using Jinja2 prompt
    and validates via Pydantic v2 ClassroomSlideDeckSchema.
    """
    session_domain_data = get_domain_for_session(session_id, session_title, chosen_domain or "")
    active_domain = chosen_domain or session_domain_data.get("name_vi", "Hệ thống Doanh nghiệp")
    domain_prompt_block = format_domain_rules_for_prompt(session_domain_data)

    # 1. Render prompt
    user_prompt = render_prompt(
        "classroom_lecture.j2",
        {
            "session_id": session_id,
            "session_title": session_title,
            "tech_stack": tech_stack,
            "course_name": course_name or tech_stack,
            "lesson_outline_text": lesson_outline_text or session_title,
            "lang_tag": lang_tag,
            "chosen_domain": active_domain,
            "domain_prompt_block": domain_prompt_block
        }
    )

    system_prompt = (
        "You are an Expert Presentation & Pedagogical Architect at Rikkei Education. "
        "Generate a structured 15-20 slide presentation deck adhering strictly to the 3-30-300 rule. "
        "Return ONLY a valid JSON object matching ClassroomSlideDeckSchema."
    )

    # 2. Call LLM with fallback
    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        agent_name="Classroom_Lecture_Architect",
        session_id=session_id
    )

    raw_json = extract_json_from_response(response or "")
    if not isinstance(raw_json, dict):
        raw_json = {
            "session_id": session_id,
            "session_title": session_title,
            "module_name": course_name or tech_stack,
            "total_slides": 18,
            "slides": [
                {
                    "slide_num": 1,
                    "slide_type": "COVER",
                    "title": session_title,
                    "bullets": []
                },
                {
                    "slide_num": 2,
                    "slide_type": "AGENDA",
                    "title": "LESSON AGENDA",
                    "bullets": [f"01. Tổng quan {session_title}"]
                },
                {
                    "slide_num": 3,
                    "slide_type": "THEORY_DEMO",
                    "title": "Khái niệm và Cơ chế hoạt động",
                    "action_title": "Bối cảnh & Thực tế",
                    "bullets": [f"Quy chuẩn thực thi và các điểm lưu ý kỹ thuật trong {tech_stack}."]
                }
            ]
        }

    # 3. Validate with Pydantic v2
    is_valid, validated_deck, errs = validate_schema(ClassroomSlideDeckSchema, raw_json)
    if is_valid and validated_deck:
        return validated_deck.model_dump()
    return raw_json


def classroom_lecture_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes classroom lecture generation from state, extracting core_ssot / lesson info,
    compiling full HTML deck, and returning updated state with 'lecture_html' and 'slide_html'.
    """
    core_ssot = state.get("core_ssot") or {}
    session_title = core_ssot.get("session_title") or state.get("session_id", "Session 01")
    tech_stack = state.get("technology_stack") or state.get("tech_stack") or "python"
    module_name = core_ssot.get("course_name") or tech_stack
    
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
                    "bullets": [f"Quy chuẩn thực thi và các điểm lưu ý kỹ thuật trong {tech_stack}."],
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
    "generate_lecture_slide_outline",
]
