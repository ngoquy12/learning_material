"""
tests/test_two_stage_reading.py — Unit tests for Two-Stage Reading Generation & Validator.
"""

from agents.creator_agents import determine_visualization_strategy, classify_reading_type
from core.validators.reading_validator import validate_reading_material

def test_visualization_strategy_routing():
    res1 = determine_visualization_strategy("Giới thiệu Python và Lịch sử", "Tổng quan về Guido van Rossum", "python/core")
    assert res1["strategy"] == "EFFECTIVE_HTML_DIAGRAM"

    res2 = determine_visualization_strategy("Toán tử số học", "Cấu trúc tính toán", "python/core")
    assert res2["strategy"] == "INTERACTIVE_CODE_PLAYGROUND"

def test_classify_reading_type():
    res = classify_reading_type("Cài đặt VS Code", "Tải xuống và cấu hình extension")
    assert "type" in res

def test_validate_rich_reading_material():
    sample_html = """<!DOCTYPE html>
<html>
<head><title>Lesson 01</title></head>
<body>
    <div class="step"><h2>Đặt vấn đề & Bối cảnh thực tế</h2><p>Trong phát triển phần mềm doanh nghiệp, Python ra đời năm 1991 bởi Guido van Rossum để giải quyết các bài toán tự động hóa. Với cú pháp đơn giản, minh bạch và thư viện phong phú, Python trở thành ngôn ngữ hàng đầu trong phát triển web, khoa học dữ liệu và trí tuệ nhân tạo.</p></div>
    <div class="step"><h2>Phân tích cơ chế vận hành</h2><p>Python là ngôn ngữ thông dịch hoạt động trên Virtual Machine (PVM). Khi thực thi, trình thông dịch sẽ chuyển đổi mã nguồn Python (.py) thành mã Bytecode (.pyc), sau đó PVM sẽ đọc từng dòng Bytecode và thực thi trực tiếp trên bộ nhớ hệ thống.</p></div>
    <div class="step"><h2>Giải pháp & Mã nguồn</h2><pre><code>print("Hello World")</code></pre><p>Hướng dẫn triển khai chi tiết mã nguồn chuẩn Best Practice theo quy định doanh nghiệp.</p></div>
    <div class="step"><h2>Tóm tắt & Lưu ý</h2><p>Ghi nhớ các quy tắc lùi lề Indentation_Error và luôn sử dụng 4 khoảng trắng thay vì phím Tab. Kiểm tra kỹ kiểu dữ liệu trước khi ép kiểu.</p></div>
</body>
</html>
"""
    is_valid, errors = validate_reading_material(sample_html)
    assert is_valid is True
    assert len(errors) == 0
