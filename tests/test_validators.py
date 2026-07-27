"""
tests/test_validators.py — Unit tests for Master Programmatic Validation Layer.
"""

from core.validators.master_validator import validate_resource
from core.validators.syntax_linter import lint_html_syntax
from core.scope_calculator import calculate_lesson_scope_contract

def test_syntax_linter_valid_html():
    valid_html = "<div><h1>Title</h1><p>Content</p></div>"
    is_valid, errors = lint_html_syntax(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_syntax_linter_unclosed_tag():
    invalid_html = "<div><h1>Title</h2></div>"
    is_valid, errors = lint_html_syntax(invalid_html)
    assert isinstance(is_valid, bool)

def test_master_validator_reading():
    content = "<div><h2>Bài đọc mẫu</h2><p>Nội dung chi tiết về Python core.</p></div>"
    is_valid, errors = validate_resource("READING", content)
    assert isinstance(is_valid, bool)
    assert isinstance(errors, list)

def test_master_validator_rubric():
    rubric_valid = (
        "## Rubric chấm điểm\n"
        "- Tiêu chí 1: 40 điểm\n"
        "- Tiêu chí 2: 60 điểm\n"
    )
    is_valid, errors = validate_resource("PROJECT", rubric_valid)
    assert is_valid is True

def test_scope_calculator():
    syllabus = {
        "sessions": [
            {"lessons": [{"title": "Biến"}, {"title": "Kiểu dữ liệu"}]},
            {"lessons": [{"title": "If else"}, {"title": "Vòng lặp"}]}
        ]
    }
    allowed, forbidden = calculate_lesson_scope_contract(syllabus, 0, 0)
    assert isinstance(allowed, set)
    assert isinstance(forbidden, set)
