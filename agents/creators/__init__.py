"""
agents/creators package — Facade for reading, slide, quiz, and media generation agents.
"""

from agents.creators.common_utils import (
    estimate_tokens,
    log_agent_tokens,
    get_base_topic_key,
    get_base_topic_key_for_core,
    determine_visualization_strategy,
    fix_raw_newlines_in_json_strings,
    robust_json_parse,
    generate_offline_master_content,
    get_lesson_content,
    get_lesson_dir,
    ensure_vietnamese_diacritics,
    validate_and_clean_forbidden_scope,
    clean_unwanted_text,
)

from agents.creators.reading_creator import (
    html_writer_agent,
    classify_reading_type,
    convert_markdown_to_html,
    unwrap_svg_and_diagrams,
    render_table,
    force_center_media,
    ensure_comparison_table,
    ensure_problem_scene_image,
)

from agents.creators.quiz_creator import (
    quiz_agent,
)

from agents.creators.session_compiler_creator import (
    session_compiler_agent,
)

from agents.creators.mini_project_creator import (
    mini_project_generator_agent,
)



from agents.creators.mindmap_creator import (
    mindmap_agent,
    process_mindmap_images,
    generate_image_api,
)

from agents.creators.visualizer_creator import (
    visualizer_generator_agent,
    get_topic_fallback_visualizer_engine,
)

from agents.creators.reading_questions_creator import (
    reading_questions_creator_agent,
)

from agents.creators.practical_lab_creator import (
    practical_lab_creator_agent,
)

from agents.creators.blueprint_creator import (
    blueprint_creator_agent,
)

from agents.creators.classroom_lecture_creator import (
    classroom_lecture_agent,
    classroom_lecture_generator_agent,
    slide_agent,
)

__all__ = [
    "estimate_tokens",
    "log_agent_tokens",
    "get_base_topic_key",
    "get_base_topic_key_for_core",
    "determine_visualization_strategy",
    "fix_raw_newlines_in_json_strings",
    "robust_json_parse",
    "generate_offline_master_content",
    "get_lesson_content",
    "get_lesson_dir",
    "ensure_vietnamese_diacritics",
    "validate_and_clean_forbidden_scope",
    "clean_unwanted_text",
    "html_writer_agent",
    "classify_reading_type",
    "convert_markdown_to_html",
    "unwrap_svg_and_diagrams",
    "render_table",
    "force_center_media",
    "ensure_comparison_table",
    "ensure_problem_scene_image",
    "quiz_agent",
    "session_compiler_agent",
    "mini_project_generator_agent",
    "_post_validate_blueprint",
    "_build_offline_fallback_blueprint",
    "mindmap_agent",
    "process_mindmap_images",
    "generate_image_api",
    "visualizer_generator_agent",
    "get_topic_fallback_visualizer_engine",
    "reading_questions_creator_agent",
    "practical_lab_creator_agent",
    "blueprint_creator_agent",
]
