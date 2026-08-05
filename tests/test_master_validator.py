"""
tests/test_master_validator.py
Unit tests for core/validators/master_validator.py and syntax linters.
"""

import pytest
from core.validators.master_validator import validate_resource
from core.validators.syntax_linter import lint_html_syntax, lint_javascript_quotes

def test_validate_reading_html_valid():
    valid_html = """
    <!doctype html>
    <html lang="vi">
      <head><title>Lesson 01 - Cú pháp Python</title></head>
      <body>
        <h1>Cú pháp hàm print trong Python</h1>
        <section id="section-1">
          <h2>1. Đặt vấn đề và bối cảnh thực tế</h2>
          <p>Bài học này hướng dẫn phân tích cơ chế hiển thị dữ liệu.</p>
        </section>
        <section id="section-2">
          <h2>2. Phân tích bản chất và cơ chế hoạt động</h2>
          <p>Phân tích chi tiết cách Python xuất dữ liệu ra màn hình console.</p>
        </section>
        <section id="section-3">
          <h2>3. Giải pháp thực thi mã nguồn</h2>
          <pre><code>print("Hello World")</code></pre>
        </section>
        <section id="section-4">
          <h2>4. Bẫy thực tế và phòng tránh</h2>
          <p>Tóm tắt các điểm quan trọng khi sử dụng hàm print trong ứng dụng.</p>
        </section>
        <section id="section-5">
          <h2>5. Tóm tắt và tự kiểm tra 1 trang</h2>
          <div class="selftest-question" style="justify-content: flex-start !important;">Câu hỏi 1</div>
        </section>
      </body>
    </html>
    """
    is_valid, errors = validate_resource("READING", valid_html)
    assert is_valid is True, f"Validation failed with errors: {errors}"
    assert len(errors) == 0

def test_lint_html_syntax():
    valid_html = "<div class='test'><p>Hello World</p></div>"
    is_valid, errors = lint_html_syntax(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_lint_javascript_quotes():
    clean_js = "console.log('Hello World');"
    bad_js = 'element.innerHTML = "<i class="ph-play"></i>"'
    
    assert len(lint_javascript_quotes(clean_js)) == 0
    assert len(lint_javascript_quotes(bad_js)) > 0
