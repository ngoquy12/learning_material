"""
tests/test_risk_mitigations.py
Comprehensive Unit Test Suite verifying all 5 Risk Mitigations for Output Quality & Reliability.
"""

import pytest
from core.vector_store import get_vector_store
from core.validators.syntax_linter import lint_pyodide_compatibility
from core.utils.json_sanitizer import clean_and_parse_json
from core.pm_parser import parse_pm_excel

def test_scope_leak_defense():
    """Test xem cơ chế BM25 có lọt thông tin Tech Stack khác không"""
    # 1. Setup mock data
    store = get_vector_store(storage_path="test_temp_vector.json")
    store.documents = [
        {"text": "FastAPI app instance @app.get('/api')", "metadata": {"tech_stack": "python/fastapi"}},
        {"text": "Python loop for x in range(10): print(x)", "metadata": {"tech_stack": "python/core"}},
        {"text": "React useState hook const [state, setState]", "metadata": {"tech_stack": "web/frontend"}}
    ]

    # Query for Python Core stack - should NEVER return FastAPI or React docs
    results = store.hybrid_query(query_text="vòng lặp python app", k=3, tech_stack="python/core")
    assert len(results) >= 1
    for doc in results:
        meta_stack = doc.get("metadata", {}).get("tech_stack")
        assert meta_stack == "python/core" or not meta_stack

def test_pyodide_compatibility_linter():
    valid_code = "import math\nimport sys\nfrom datetime import datetime\nprint(math.sqrt(16))"
    errs_valid = lint_pyodide_compatibility(valid_code)
    assert len(errs_valid) == 0

    invalid_code = "import requests\nimport pandas as pd\nresponse = requests.get('https://api.com')"
    errs_invalid = lint_pyodide_compatibility(invalid_code)
    assert len(errs_invalid) == 2
    assert "requests" in errs_invalid[0]
    assert "pandas" in errs_invalid[1]

def test_clean_and_parse_json_sanitizer():
    # 1. Clean markdown fences
    raw_fence = "```json\n{\"session_id\": \"Session 01\", \"status\": \"OK\"}\n```"
    parsed_fence = clean_and_parse_json(raw_fence)
    assert parsed_fence["session_id"] == "Session 01"

    # 2. Parse with raw text surrounding JSON
    raw_mixed = "Here is your JSON response:\n```json\n[{\"q\": 1}, {\"q\": 2}]\n```\nHope this helps!"
    parsed_mixed = clean_and_parse_json(raw_mixed)
    assert len(parsed_mixed) == 2
    assert parsed_mixed[0]["q"] == 1

def test_naming_convention_linter():
    from core.validators.syntax_linter import lint_naming_convention
    # Python camelCase function definition should fail
    py_code = "def calculateTotalSum():\n    return 42"
    errs = lint_naming_convention(py_code, "python/core")
    assert len(errs) == 1
    assert "snake_case" in errs[0]

    # JS snake_case function definition should fail
    js_code = "function calculate_total_sum() {\n    return 42;\n}"
    errs_js = lint_naming_convention(js_code, "web/frontend")
    assert len(errs_js) == 1
    assert "camelCase" in errs_js[0]

def test_auto_punctuation_and_emoji_linter():
    from agents.creators.reading_creator import ensure_sentence_ending_period
    assert ensure_sentence_ending_period("Khái niệm biến trong Python") == "Khái niệm biến trong Python."
    assert ensure_sentence_ending_period("Khái niệm biến trong Python.") == "Khái niệm biến trong Python."

    from core.validators.reading_validator import validate_reading_material
    html_with_emoji = "<section id='section-1'><h1>Title</h1></section><section id='section-2'></section><section id='section-3'><pre><code>code</code></pre></section><section id='section-4'></section><section id='section-5'></section> 🚀 💡"
    is_valid, errs = validate_reading_material(html_with_emoji)
    assert is_valid is False
    assert any("emoji" in e.lower() for e in errs)
