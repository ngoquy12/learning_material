"""
core/sanitizers package — Content, Markdown, LaTeX, Diacritics, and JSON Sanitizers.
"""

from core.sanitizers.diacritics_sanitizer import (
    ensure_vietnamese_diacritics,
    clean_unwanted_text,
)

from core.sanitizers.markdown_sanitizer import (
    clean_markdown_formulas,
    normalize_markdown_headers,
)

from core.sanitizers.scope_guard import (
    validate_and_clean_forbidden_scope,
)

from core.sanitizers.json_recoverer import (
    fix_raw_newlines_in_json_strings,
    robust_json_parse,
)

__all__ = [
    "ensure_vietnamese_diacritics",
    "clean_unwanted_text",
    "clean_markdown_formulas",
    "normalize_markdown_headers",
    "validate_and_clean_forbidden_scope",
    "fix_raw_newlines_in_json_strings",
    "robust_json_parse",
]
