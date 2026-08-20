"""
agents/classroom_lecture_generator_agent.py
AI Classroom Lecture Presentation & Interactive Visualizer Agent.
Delegates presentation deck rendering, slide layout generation, and interactive simulation building
to core.renderers.lecture package.
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List, Optional

from core.renderers.lecture import (
    LOGO_URL,
    sanitize_slide_text,
    clean_title_string,
    extract_concise_topic_name,
    get_icon_for_topic,
    detect_file_info_for_tech_stack,
    derive_unified_session_scenario,
    find_pm_syllabus,
    infer_scope_boundary_rules,
    extract_knowledge_from_lesson_folder,
    extract_session_summary_bullets,
    render_scene_content_html,
    generate_session_deck_html,
    clean_and_parse_llm_json,
    generate_section_with_llm,
    build_generic_multi_subject_section,
    render_interactive_section,
    generate_interactive_visualizer_html
)

class ClassroomLectureGeneratorAgent:
    """
    Classroom Lecture Generator Agent:
    Compiles a complete Master HTML Presentation Deck and Interactive Visualizer Dashboard
    for all lessons in a Session, strictly matching the classroom_lecture_generator skill.
    Saves output files to: Session XX/Bài giảng trên lớp/slides.html and Visualizer/index.html.
    """

    LOGO_URL = LOGO_URL

    def __init__(self):
        pass

    def sanitize_slide_text(self, text: str) -> str:
        return sanitize_slide_text(text)

    def clean_title_string(self, text: str) -> str:
        return clean_title_string(text)

    def extract_session_summary_bullets(self, lessons_data: List[Dict[str, Any]], core_ssot: Optional[Dict[str, Any]] = None) -> List[str]:
        return extract_session_summary_bullets(lessons_data, core_ssot)

    def _render_scene_content_html(self, scene: Dict[str, Any], clean_stitle: str, is_cli_or_tooling: bool = False) -> str:
        return render_scene_content_html(scene, clean_stitle, is_cli_or_tooling)

    def generate_session_deck_html(self, session_title: str, module_name: str, lessons_data: List[Dict[str, Any]], core_ssot: Optional[Dict[str, Any]] = None) -> str:
        return generate_session_deck_html(session_title, module_name, lessons_data, core_ssot)

    def _get_icon_for_topic(self, topic: str, tech_stack: str = "") -> str:
        return get_icon_for_topic(topic, tech_stack)

    def _derive_unified_session_scenario(self, session_title: str, tech_stack: str) -> str:
        return derive_unified_session_scenario(session_title, tech_stack)

    def _find_pm_syllabus_for_session_and_lesson(self, session_dir: Optional[Path], session_title: str, lesson_title: str) -> Dict[str, Any]:
        return find_pm_syllabus(session_dir, session_title, lesson_title)

    def _infer_scope_boundary_rules(self, session_title: str, tech_stack: str, pm_syllabus: Dict[str, Any]) -> str:
        return infer_scope_boundary_rules(session_title, tech_stack, pm_syllabus)

    def _extract_concise_topic_name(self, title: str) -> str:
        return extract_concise_topic_name(title)

    def _detect_file_info_for_tech_stack(self, tech_stack: str, lesson_title: str) -> tuple[str, str]:
        return detect_file_info_for_tech_stack(tech_stack, lesson_title)

    def _clean_and_parse_llm_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        return clean_and_parse_llm_json(raw_text)

    def _extract_knowledge_from_lesson_folder(self, session_dir: Optional[Path], session_title: str, lesson_title: str) -> Dict[str, Any]:
        return extract_knowledge_from_lesson_folder(session_dir, session_title, lesson_title)

    def _generate_section_with_llm(self, *args, **kwargs) -> Optional[Dict[str, Any]]:
        return generate_section_with_llm(*args, **kwargs)

    def _build_generic_multi_subject_section(self, *args, **kwargs) -> Dict[str, Any]:
        return build_generic_multi_subject_section(*args, **kwargs)

    def _render_interactive_section(self, *args, **kwargs) -> Dict[str, Any]:
        return render_interactive_section(*args, **kwargs)

    def generate_interactive_visualizer_html(
        self,
        session_title: str,
        module_name: str,
        lessons_data: List[Dict[str, Any]],
        core_ssot: Optional[Dict[str, Any]] = None,
        session_dir_path: Optional[str] = None,
        chosen_domain: str = "",
        forbidden_scope: str = "",
        allowed_scope: str = ""
    ) -> str:
        return generate_interactive_visualizer_html(
            session_title=session_title,
            module_name=module_name,
            lessons_data=lessons_data,
            core_ssot=core_ssot,
            session_dir_path=session_dir_path,
            chosen_domain=chosen_domain,
            forbidden_scope=forbidden_scope,
            allowed_scope=allowed_scope
        )

    def generate_lecture(
        self,
        session_id: str,
        session_title: str,
        session_dir_path: str,
        tech_stack: str,
        previous_lessons_text: str,
        lessons_data: Optional[List[Dict[str, Any]]] = None,
        chosen_domain: str = "",
        forbidden_scope: str = "",
        allowed_scope: str = ""
    ) -> str:
        """
        Generates complete Interactive Visual Lecture Dashboard for all lessons in a Session.
        Saves output to: Session XX/Bài giảng trên lớp/slides.html and Visualizer/index.html.
        """
        import re
        session_dir = Path(session_dir_path)
        session_dir.mkdir(parents=True, exist_ok=True)
        
        slides_dir = session_dir / "Bài giảng trên lớp"
        slides_dir.mkdir(exist_ok=True)

        visualizer_dir = session_dir / "Visualizer"
        visualizer_dir.mkdir(exist_ok=True)
        
        print(f"\n  ---> [Classroom Lecture Agent] Đang tạo Bài giảng trên lớp Trực quan Tương tác cho Session: {session_id} - {session_title}...")
        
        parsed_lessons = []
        if lessons_data and len(lessons_data) > 0:
            parsed_lessons = lessons_data
        else:
            raw_matches = re.findall(
                r'^BÀI HỌC\s+(?:Lesson\s*\d+|Bài\s*\d+|\d+)[\:\-]?\s*(.*?)(?=\n|$)',
                previous_lessons_text, re.IGNORECASE | re.MULTILINE
            )
            if not raw_matches:
                raw_matches = re.findall(r'^Lesson\s*\d+\s*[\:\-]?\s*(.*?)(?=\n|$)', previous_lessons_text, re.IGNORECASE | re.MULTILINE)
            
            for idx, match in enumerate(raw_matches, 1):
                clean_t = match.strip()
                clean_t = re.sub(r'^\s*(Session\s*\d+|Lesson\s*\d+|Bài\s*\d+|\[\d+\.\d+\]|\d+\.)\s*[\:\-]?\s*', '', clean_t, flags=re.IGNORECASE).strip()
                if clean_t and clean_t not in [l.get("lesson_title") for l in parsed_lessons]:
                    parsed_lessons.append({
                        "lesson_id": f"Lesson {idx:02d}",
                        "lesson_title": clean_t,
                        "summary_text": ""
                    })

        if not parsed_lessons:
            parsed_lessons = [{
                "lesson_id": "Lesson 01",
                "lesson_title": session_title,
                "summary_text": previous_lessons_text[:300]
            }]

        final_html = self.generate_interactive_visualizer_html(
            session_title=session_title,
            module_name=tech_stack,
            lessons_data=parsed_lessons,
            session_dir_path=str(session_dir),
            chosen_domain=chosen_domain,
            forbidden_scope=forbidden_scope,
            allowed_scope=allowed_scope
        )

        out_html_file = slides_dir / "slides.html"
        with open(out_html_file, "w", encoding="utf-8") as f:
            f.write(final_html)

        vis_file = visualizer_dir / "index.html"
        with open(vis_file, "w", encoding="utf-8") as f:
            f.write(final_html)

        print(f"  [Success] Lưu Bài giảng trên lớp HTML ({len(parsed_lessons)} lessons): {out_html_file}")
        print(f"  [Success] Lưu Visualizer HTML: {vis_file}")
        return final_html

classroom_lecture_generator_agent = ClassroomLectureGeneratorAgent()

__all__ = [
    "ClassroomLectureGeneratorAgent",
    "classroom_lecture_generator_agent",
]
