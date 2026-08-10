"""
tests/test_guard_svg_syntax.py
Unit tests for guard_svg_syntax in agents/creators/reading_creator.py.
"""

import pytest
from agents.creators.reading_creator import guard_svg_syntax

def test_guard_svg_syntax_basic():
    raw_svg = '<svg><text>INPUT DATA</text></svg>'
    result = guard_svg_syntax(raw_svg)
    
    assert 'xmlns="http://www.w3.org/2000/svg"' in result
    assert 'rikkei-diagram' in result
    assert 'viewBox=' in result
    assert 'Input Data' in result  # ALL CAPS converted to Title Case
    assert '<div class="my-6">' in result


def test_guard_svg_syntax_existing_attributes():
    raw_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" class="my-custom-svg"><text font-family="Inter">LOGISTICS WORKFLOW</text></svg>'
    result = guard_svg_syntax(raw_svg)
    
    assert 'rikkei-diagram' in result
    assert 'viewBox="0 0 1000 500"' in result
    assert 'Logistics Workflow' in result


def test_guard_svg_syntax_strip_dark_wrapper():
    raw_svg = '<div class="p-4 bg-slate-900"><svg viewBox="0 0 800 300"><text>SERVER PROCESS</text></svg></div>'
    result = guard_svg_syntax(raw_svg)
    
    assert 'bg-slate-900' not in result
    assert 'Server Process' in result
    assert 'xmlns=' in result


def test_guard_svg_syntax_non_svg_passthrough():
    text = "This is simple html text without svg."
    assert guard_svg_syntax(text) == text
    assert guard_svg_syntax("") == ""
