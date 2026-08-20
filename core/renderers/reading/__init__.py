"""
core/renderers/reading package — Specialized Renderers, Sanitizers, and Visualizers for Reading Materials.
"""

from core.renderers.reading.markdown_parser import (
    convert_markdown_to_html,
    ensure_sentence_ending_period,
    slugify_id
)

from core.renderers.reading.svg_guard import (
    guard_svg_syntax,
    sanitize_mermaid_code,
    guard_mermaid_syntax
)

from core.renderers.reading.code_sandbox_renderer import (
    LANGUAGE_MAPPING_REGISTRY,
    resolve_language_info,
    get_clean_language_name,
    highlight_code_syntax,
    convert_code_to_live_sandbox
)

from core.renderers.reading.visualizer_component import (
    generate_fallback_visualizer_steps,
    build_domain_adaptive_visualizer
)

from core.renderers.reading.html_sanitizer import (
    CANONICAL_DOC_LINKS,
    validate_scope_boundary,
    sanitize_llm_json_text,
    sanitize_references,
    sanitize_html_tags_and_italics,
    inject_subheading_ids,
    clean_stray_chars,
    ensure_html,
    extract_2tier_toc,
    FORBIDDEN_AI_CLICHES,
    strip_ai_cliches_from_title
)

from core.renderers.reading.lesson_classifier import classify_reading_type

__all__ = [
    "convert_markdown_to_html",
    "ensure_sentence_ending_period",
    "slugify_id",
    "guard_svg_syntax",
    "sanitize_mermaid_code",
    "guard_mermaid_syntax",
    "LANGUAGE_MAPPING_REGISTRY",
    "resolve_language_info",
    "get_clean_language_name",
    "highlight_code_syntax",
    "convert_code_to_live_sandbox",
    "generate_fallback_visualizer_steps",
    "build_domain_adaptive_visualizer",
    "CANONICAL_DOC_LINKS",
    "validate_scope_boundary",
    "sanitize_llm_json_text",
    "sanitize_references",
    "sanitize_html_tags_and_italics",
    "inject_subheading_ids",
    "clean_stray_chars",
    "ensure_html",
    "extract_2tier_toc",
    "classify_reading_type",
    "FORBIDDEN_AI_CLICHES",
    "strip_ai_cliches_from_title"
]
