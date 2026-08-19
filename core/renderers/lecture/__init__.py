"""
core/renderers/lecture package — Classroom Lecture Deck & Interactive Visualizer Generators.
"""

from core.renderers.lecture.text_sanitizer import (
    sanitize_slide_text,
    clean_title_string,
    extract_concise_topic_name,
    get_icon_for_topic,
    detect_file_info_for_tech_stack
)

from core.renderers.lecture.knowledge_extractor import (
    derive_unified_session_scenario,
    find_pm_syllabus,
    infer_scope_boundary_rules,
    extract_knowledge_from_lesson_folder
)

from core.renderers.lecture.deck_renderer import (
    LOGO_URL,
    extract_session_summary_bullets,
    render_scene_content_html,
    generate_session_deck_html
)

from core.renderers.lecture.simulation_builder import (
    clean_and_parse_llm_json,
    generate_section_with_llm,
    build_generic_multi_subject_section,
    render_interactive_section,
    generate_interactive_visualizer_html
)

__all__ = [
    "LOGO_URL",
    "sanitize_slide_text",
    "clean_title_string",
    "extract_concise_topic_name",
    "get_icon_for_topic",
    "detect_file_info_for_tech_stack",
    "derive_unified_session_scenario",
    "find_pm_syllabus",
    "infer_scope_boundary_rules",
    "extract_knowledge_from_lesson_folder",
    "extract_session_summary_bullets",
    "render_scene_content_html",
    "generate_session_deck_html",
    "clean_and_parse_llm_json",
    "generate_section_with_llm",
    "build_generic_multi_subject_section",
    "render_interactive_section",
    "generate_interactive_visualizer_html"
]
