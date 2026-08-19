"""
tests/test_reading_creator_fixes.py
Unit tests verifying core fixes for reading material generation:
1. Italic leaking & broken HTML tags sanitization
2. Dynamic multi-technology visualizer generation & clean omission for concepts
3. Multi-language syntax highlighting and tab/indent preservation
4. Clean language normalization and redundant text bloat removal
5. Step-by-step engine & fallback step generation
6. Heading class deduplication & duplicate main header removal
"""

import pytest
import re
from agents.creators.reading_creator import (
    sanitize_html_tags_and_italics,
    build_domain_adaptive_visualizer,
    get_clean_language_name,
    highlight_code_syntax,
    generate_fallback_visualizer_steps,
)


def test_get_clean_language_name():
    """Test that long/messy tech stack strings are converted to clean, canonical labels."""
    assert get_clean_language_name("javascript vanilla (es6+), html5/css3, dom api, fetch api") == "JavaScript (ES6+)"
    assert get_clean_language_name("python, pyodide, pandas") == "Python 3"
    assert get_clean_language_name("typescript, react, next.js") == "TypeScript"
    assert get_clean_language_name("java, spring boot") == "Java"
    assert get_clean_language_name("sql, mysql, postgresql") == "SQL"
    assert get_clean_language_name("git bash, linux cli") == "Bash/CLI"
    assert get_clean_language_name("") == "Mã nguồn"


def test_highlight_code_syntax():
    """Test that code lines get proper syntax highlighting spans and keep indentation."""
    js_line = "  const VAT_RATE = 0.1; // 10% tax"
    highlighted = highlight_code_syntax(js_line, "JavaScript")
    assert 'text-purple-600 font-bold' in highlighted  # const
    assert 'text-amber-600 font-mono' in highlighted   # 0.1
    assert 'text-slate-400 italic' in highlighted      # comment
    assert highlighted.startswith("  ")                # indentation preserved

    py_line = "def calculate_total(price):"
    py_high = highlight_code_syntax(py_line, "Python")
    assert 'text-purple-600 font-bold' in py_high      # def
    assert 'text-blue-600 font-semibold' in py_high    # calculate_total


def test_generate_fallback_visualizer_steps():
    """Test smart fallback step generation when LLM omits steps."""
    code_lines = [
        "const VAT_RATE = 0.1;",
        "function createCart() {",
        "  let count = 0;",
        "  return count;",
        "}",
        "const cart = createCart();"
    ]
    variables = [{"name": "VAT_RATE"}, {"name": "count"}, {"name": "cart"}]
    steps = generate_fallback_visualizer_steps(code_lines, variables, "Closure và Scope")
    assert len(steps) >= 3
    assert any(s["line"] == 1 and ("vat_rate" in s["ram"] or "vat-rate" in s["ram"]) for s in steps)
    assert any("createCart" in s["log"] for s in steps)


def test_sanitize_html_tags_broken_unclosed_tags():
    """Test that broken tags like `<h4 ...><i class=` are cleaned up."""
    bad_html = '<h4 class="font-bold text-slate-900"><i class=\n<p>Nội dung đoạn văn bình thường</p>'
    cleaned = sanitize_html_tags_and_italics(bad_html)
    assert '<i class=' not in cleaned
    assert '<p>Nội dung đoạn văn bình thường</p>' in cleaned


def test_sanitize_html_tags_normalize_phosphor_icons():
    """Test that Phosphor icon <i> tags are normalized to <span> tags."""
    html_with_icon = '<p>Lưu ý: <i class="ph-bold ph-lightbulb text-amber-500"></i> Đây là mẹo.</p>'
    cleaned = sanitize_html_tags_and_italics(html_with_icon)
    assert '<i class=' not in cleaned
    assert '<span class="ph-bold ph-lightbulb text-amber-500"></span>' in cleaned


def test_sanitize_html_tags_strip_unclosed_italics():
    """Test that lone/unclosed <i> or <em> tags are stripped completely."""
    html_with_italics = '<p>Đoạn văn <i>không được in nghiêng và <em>không có em</em>.</p>'
    cleaned = sanitize_html_tags_and_italics(html_with_italics)
    assert '<i>' not in cleaned
    assert '</i>' not in cleaned
    assert '<em>' not in cleaned
    assert '</em>' not in cleaned
    assert 'không được in nghiêng' in cleaned


def test_build_domain_adaptive_visualizer_javascript():
    """Test dynamic visualizer generation for JavaScript/Object lesson."""
    viz_spec = {
        "is_applicable": True,
        "title": "2.4. Mô phỏng cơ chế vận hành từng bước (Step-by-Step Execution Visualizer)",
        "explanation": "Mô phỏng khởi tạo đối tượng user và gán thuộc tính:",
        "code_lines": [
            "// 1. Khởi tạo đối tượng rỗng",
            "const user = {};",
            "user.name = 'Nguyen Van A';",
            "console.log(user.name);"
        ],
        "variables": [
            {"name": "user", "label": "Đối tượng user"}
        ],
        "steps": [
            {"line": 2, "ram": {"user": "{}"}, "log": "<div>&gt; Khởi tạo user = {}</div>"},
            {"line": 3, "ram": {"user": "{ name: 'Nguyen Van A' }"}, "log": "<div>&gt; Gán user.name</div>"}
        ]
    }
    html = build_domain_adaptive_visualizer("Session 12 - Object trong JavaScript", "javascript vanilla (es6+), html5/css3", viz_spec)
    assert 'id="sec-2-4-mo-phong-co-che-van-hanh-tung-buoc"' in html
    assert 'id="viz-line-1"' in html
    assert 'id="viz-line-2"' in html
    assert 'id="viz-ram-user"' in html
    assert 'window.vizSteps =' in html
    assert 'Đối tượng user:' in html
    # Check that header uses clean language name, not raw bloated string
    assert 'Mã nguồn thực thi (JavaScript (ES6+))' in html
    assert 'JAVASCRIPT VANILLA (ES6+)' not in html
    assert 'Engine' not in html  # Redundant RAM Engine row removed
    # Check that Phosphor icons use <span>, not <i>
    assert '<i class="ph-' not in html


def test_build_domain_adaptive_visualizer_clean_omission_for_concept():
    """Test that pure concept / non-applicable visualizer returns empty string (no fake code)."""
    viz_spec = {"is_applicable": False}
    html = build_domain_adaptive_visualizer("Session 01 - Giới thiệu VCS", "git", viz_spec)
    assert html == ""

    html_none = build_domain_adaptive_visualizer("Session 01 - Giới thiệu VCS", "git", None)
    assert html_none == ""


def test_duplicate_heading_stripping():
    """Test that leading duplicate <h1> and <h2> headers are cleanly stripped."""
    prob_html = "<h2>1. Đặt vấn đề</h2><p>Nội dung thực tế...</p>"
    cleaned_prob = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', prob_html, flags=re.DOTALL | re.IGNORECASE).strip()
    assert "<h2>1. Đặt vấn đề</h2>" not in cleaned_prob
    assert "<p>Nội dung thực tế...</p>" in cleaned_prob

    know_html = "<h2>2. Giới thiệu kiến thức</h2><h3 id='sec-2-1'>2.1. Cú pháp</h3><p>Chi tiết...</p>"
    cleaned_know = re.sub(r'^\s*<(?:h1|h2)\b[^>]*>.*?</(?:h1|h2)>\s*', '', know_html, flags=re.DOTALL | re.IGNORECASE).strip()
    assert "<h2>2. Giới thiệu kiến thức</h2>" not in cleaned_know
    assert "<h3 id='sec-2-1'>2.1. Cú pháp</h3>" in cleaned_know

