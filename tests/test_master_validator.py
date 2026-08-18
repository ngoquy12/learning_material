"""
tests/test_master_validator.py
Comprehensive integration tests for core/validators/master_validator.py and linters.
"""

import pytest
from core.validators.master_validator import validate_resource
from core.validators.syntax_linter import lint_html_syntax, lint_javascript_quotes

def test_validate_reading_html_valid():
    valid_html = """
    <!doctype html>
    <html lang="vi">
      <head><title>Cú pháp Python</title></head>
      <body>
        <h1>Cú pháp hàm print trong Python</h1>
        <section id="section-1">
          <h2>1. Đặt vấn đề và bối cảnh thực tế</h2>
          <p>Bài học này hướng dẫn phân tích cơ chế hiển thị dữ liệu.</p>
        </section>
        <section id="section-2">
          <h2>2. Phân tích bản chất và cơ chế hoạt động</h2>
          <p>Phân tích chi tiết cách Python xuất dữ liệu ra màn hình console.</p>
          <div id="sec-2-4" class="step-by-step execution visualizer">
            <p>Trình mô phỏng cơ chế vận hành từng bước.</p>
          </div>
        </section>
        <section id="section-3">
          <h2>3. Giải pháp thực thi mã nguồn</h2>
          <div class="border-sky-200 bg-sky-50 font-bold text-sky-900">
            <p><strong>Yêu cầu bài toán:</strong> Thực thi câu lệnh in xuất dữ liệu ra console.</p>
          </div>
          <h3>3.1. Ví dụ khởi đầu cơ bản</h3>
          <pre><code class="language-python">print("Hello World")</code></pre>
          <h3>3.2. Ví dụ xử lý định dạng chuỗi</h3>
          <pre><code class="language-python">print(f"User: {name}")</code></pre>
          <h3>3.3. Ví dụ xử lý dữ liệu nâng cao</h3>
          <pre><code class="language-python">print("Data processed")</code></pre>
        </section>
        <section id="section-4">
          <h2>4. Lỗi thường gặp và phòng tránh</h2>
          <p>Tóm tắt các điểm quan trọng khi sử dụng hàm print trong ứng dụng.</p>
        </section>
        <section id="section-5">
          <h2>5. Tóm tắt và tự kiểm tra 1 trang</h2>
          <div class="selftest-question" style="justify-content: flex-start !important;">Câu hỏi 1</div>
        </section>
      </body>
    </html>
    """
    metadata = {"skip_size_check": True, "is_testing": True}
    is_valid, errors = validate_resource("READING", valid_html, metadata=metadata)
    assert is_valid is True, f"Validation failed with errors: {errors}"
    assert len(errors) == 0


def test_validate_reading_orientation_lesson():
    orientation_html = """
    <!doctype html>
    <html lang="vi">
      <head><title>Session 01 - Định hướng khóa học</title></head>
      <body>
        <h1>Tổng quan lộ trình và Demo sản phẩm</h1>
        <section id="part-1">
          <h2>1. Tổng quan nội dung & Lộ trình môn học</h2>
          <p>Tóm tắt lộ trình 24 buổi học và các mốc kiến thức quan trọng.</p>
        </section>
        <section id="part-2">
          <h2>2. Phương pháp học tập hiệu quả & Kiến thức tiền đề</h2>
          <p>Phương pháp tự học, AI Pair-Programming với Cursor/Windsurf và kiến thức tiền đề cần chuẩn bị.</p>
        </section>
        <section id="part-3">
          <h2>3. Demo sản phẩm dự án đầu ra</h2>
          <p>Trình chiếu kết quả dự án ứng dụng Web sinh viên sẽ hoàn thành cuối môn.</p>
        </section>
      </body>
    </html>
    """
    metadata = {
        "session_id": "Session 01",
        "is_orientation": True,
        "lesson_title": "Tổng quan lộ trình và Demo sản phẩm",
        "skip_size_check": True,
        "is_testing": True
    }
    is_valid, errors = validate_resource("READING", orientation_html, metadata=metadata)
    assert is_valid is True, f"Orientation reading validation failed: {errors}"


def test_validate_slide_presentation_valid():
    slides = [
        {
            "scene_title": "Session 01 - Biến số Python",
            "narration": "Chào mừng các bạn đến với buổi học hôm nay về biến số và kiểu dữ liệu trong Python.",
            "bullets": ["Khái niệm biến số", "Các kiểu dữ liệu cơ bản"]
        },
        {
            "scene_title": "Slide 02 - Kiểu dữ liệu int",
            "narration": "Kiểu int biểu diễn các số nguyên không có phần thập phân trong ngôn ngữ lập trình Python.",
            "bullets": ["Số nguyên dương", "Số nguyên âm"]
        },
        {
            "scene_title": "Slide 03 - Kiểu dữ liệu float",
            "narration": "Kiểu float biểu diễn các số thực có phần thập phân trong ngôn ngữ lập trình Python.",
            "bullets": ["Số thực dương", "Số thực âm"]
        },
        {
            "scene_title": "Slide 04 - Tổng kết buổi học",
            "narration": "Tóm tắt các điểm kiến thức cốt lõi về biến số và các kiểu dữ liệu vừa học.",
            "bullets": ["Kiểu int", "Kiểu float", "Quy tắc đặt tên biến"]
        }
    ]
    is_valid, errors = validate_resource("SLIDE", slides)
    assert is_valid is True, f"Slide validation failed: {errors}"


def test_validate_quiz_valid():
    quiz = [
        {
            "question": "Cú pháp khai báo hàm trong Python là gì?",
            "options": ["def func():", "function func()", "void func()", "func() => {}"],
            "correct_option_index": 0,
            "explanation": "Đúng cú pháp Python."
        }
    ]
    is_valid, errors = validate_resource("QUIZ", quiz)
    assert is_valid is True, f"Quiz validation failed: {errors}"


def test_validate_practice_exercise_valid():
    practice = {
        "title": "Bài tập 1: Sửa lỗi hàm tính VAT",
        "steps": ["Bắt lỗi logic trong hàm vat_calc", "Sửa đổi công thức tính thuế"],
        "checklist": ["[ ] Sửa xong hàm vat_calc", "[ ] Lập bộ testcase kiểm thử"],
        "rubric": [
            {"criterion": "Bắt đúng lỗi logic", "max_score": 50},
            {"criterion": "Sửa mã nguồn chính xác", "max_score": 50}
        ]
    }
    is_valid, errors = validate_resource("PRACTICE", practice)
    assert is_valid is True, f"Practice validation failed: {errors}"


def test_validate_project_spec_valid():
    project = {
        "title": "Mini Project: Hệ thống Quản lý Thư viện",
        "requirements": ["Cơ sở dữ liệu", "Giao diện CLI"],
        "checklist": ["Chức năng mượn sách", "Chức năng trả sách"]
    }
    is_valid, errors = validate_resource("PROJECT", project)
    assert is_valid is True


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
