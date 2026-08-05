"""
tests/test_scope_calculator.py
Unit tests for core/scope_calculator.py scope contract calculations & violation checks.
"""

import pytest
from core.scope_calculator import (
    calculate_lesson_scope_contract,
    validate_session_cadence_and_lesson_bounds,
    validate_text_against_scope,
)

@pytest.fixture
def mock_syllabus():
    return {
        "sessions": [
            {
                "session_title": "Session 01 - Biến và Kiểu dữ liệu",
                "session_code": "THEORY",
                "lessons": [
                    {
                        "lesson_title": "Khái niệm biến và kiểu int",
                        "keywords": ["biến", "int", "print"],
                        "topics": ["Biến số"]
                    },
                    {
                        "lesson_title": "Kiểu chuỗi string và float",
                        "keywords": ["str", "float", "len"],
                        "forbidden_scope": "CẤM: vòng lặp, list"
                    }
                ]
            },
            {
                "session_title": "Session 02 - Vòng lặp for và while",
                "session_code": "THEORY",
                "lessons": [
                    {
                        "lesson_title": "Vòng lặp for",
                        "keywords": ["vòng lặp", "for", "range"]
                    }
                ]
            }
        ]
    }

def test_calculate_lesson_scope_contract(mock_syllabus):
    allowed, forbidden = calculate_lesson_scope_contract(mock_syllabus, current_session_idx=0, current_lesson_idx=0)
    assert "biến" in allowed
    assert "int" in allowed
    assert "vòng lặp" in forbidden or "vòng lặp, list" in forbidden or "for" in forbidden

def test_validate_text_against_scope():
    forbidden_scope = {"vòng lặp", "dictionary", "class"}
    text_with_violation = "Trong bài học này chúng ta sẽ dùng vòng lặp để duyệt phần tử."
    text_clean = "Bài học này hướng dẫn khai báo biến cơ bản."

    violations = validate_text_against_scope(text_with_violation, forbidden_scope)
    assert "vòng lặp" in violations

    clean_violations = validate_text_against_scope(text_clean, forbidden_scope)
    assert len(clean_violations) == 0

def test_validate_session_cadence_bounds():
    heavy_syllabus = {
        "sessions": [
            {
                "session_title": "Session Quá tải",
                "session_code": "THEORY",
                "lessons": [{}, {}, {}, {}, {}]  # 5 lessons > 4
            }
        ]
    }
    warnings = validate_session_cadence_and_lesson_bounds(heavy_syllabus)
    assert len(warnings) == 1
    assert "Cognitive Load Warning" in warnings[0]
