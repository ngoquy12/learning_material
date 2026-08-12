import sys
import os
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.renderers.reading_renderer import assemble_reading_html, resolve_domain_engine
from core.validators.reading_validator import validate_reading_material, validate_reading_json_payload

def run_pipeline_tests():
    print("==========================================================")
    print("Testing Enterprise Reading Material Refactoring Pipeline")
    print("==========================================================")

    test_cases = [
        {
            "tech_stack": "python",
            "title": "Cấu trúc rẽ nhánh điều khiển với if, elif và else",
            "sec1": "<p class='text-slate-600 mb-4 leading-relaxed'>Khi phát triển ứng dụng ShopeeFood, chúng ta cần kiểm tra giá trị đơn hàng để áp dụng mã giảm giá freeship.</p>",
            "sec2": "<h3 id='sec-2-1' class='text-xl font-bold text-slate-900 mb-3'>2.1. Cú pháp câu lệnh if</h3><p class='text-slate-600 mb-4 leading-relaxed'>Cú pháp kiểm tra điều kiện đơn.</p><pre><code class='language-python'>order_amount = 500000\nif order_amount >= 500000:\n    print('Được miễn phí giao hàng')</code></pre>",
            "sec3": "<h3 id='sec-3-1' class='text-xl font-bold text-slate-900 mb-3'>3.1. Ví dụ thực tế ShopeeFood</h3><p class='text-slate-600 mb-4 leading-relaxed'>Chương trình phân loại mức freeship.</p><pre><code class='language-python'>order_amount = 1500000\nif order_amount >= 1000000:\n    shipping_fee = 0\nelse:\n    shipping_fee = 30000\nprint(f'Phí giao hàng: {shipping_fee} VNĐ')</code></pre>",
            "sec4": "<div class='p-4 rounded-xl border border-rose-200 bg-rose-50/60 my-4'><h4 class='font-bold text-rose-900 mb-2'>4.1. Lỗi quên thụt lề (IndentationError)</h4><p class='text-sm text-slate-700'>Trong Python, các khối lệnh sau câu lệnh if bắt buộc phải th thụt lề 4 khoảng trắng.</p></div>"
        },
        {
            "tech_stack": "java",
            "title": "Lập trình hướng đối tượng với Java Class và Object",
            "sec1": "<p class='text-slate-600 mb-4 leading-relaxed'>Trong hệ thống quản lý tài khoản ngân hàng bằng Java, chúng ta cần định nghĩa lớp Account để đại diện cho khách hàng.</p>",
            "sec2": "<h3 id='sec-2-1' class='text-xl font-bold text-slate-900 mb-3'>2.1. Cú pháp khai báo Class</h3><p class='text-slate-600 mb-4 leading-relaxed'>Khai báo thuộc tính và phương thức trong Java.</p><pre><code class='language-java'>public class Account {\n    private String accountNumber;\n    private double balance;\n}</code></pre>",
            "sec3": "<h3 id='sec-3-1' class='text-xl font-bold text-slate-900 mb-3'>3.1. Khởi tạo đối tượng</h3><p class='text-slate-600 mb-4 leading-relaxed'>Tạo đối tượng mới bằng từ khóa new.</p><pre><code class='language-java'>Account acc = new Account();\nSystem.out.println(\"Tài khoản vừa tạo thành công\");</code></pre>",
            "sec4": "<div class='p-4 rounded-xl border border-amber-200 bg-amber-50/60 my-4'><h4 class='font-bold text-amber-900 mb-2'>4.1. Lỗi NullPointerException</h4><p class='text-sm text-slate-700'>Khởi tạo đối tượng trước khi truy cập thuộc tính hoặc phương thức.</p></div>"
        },
        {
            "tech_stack": "javascript",
            "title": "Bất đồng bộ trong JavaScript với Async/Await",
            "sec1": "<p class='text-slate-600 mb-4 leading-relaxed'>Khi gọi API từ server Node.js, JavaScript xử lý bất đồng bộ để tránh làm treo giao diện UI.</p>",
            "sec2": "<h3 id='sec-2-1' class='text-xl font-bold text-slate-900 mb-3'>2.1. Cú pháp Async/Await</h3><p class='text-slate-600 mb-4 leading-relaxed'>Sử dụng async function để chờ Promise hoàn tất.</p><pre><code class='language-javascript'>async function fetchOrderData() {\n    const res = await fetch('/api/orders');\n    const data = await res.json();\n}</code></pre>",
            "sec3": "<h3 id='sec-3-1' class='text-xl font-bold text-slate-900 mb-3'>3.1. Bắt lỗi với Try/Catch</h3><p class='text-slate-600 mb-4 leading-relaxed'>Xử lý lỗi mạng khi fetch API.</p><pre><code class='language-javascript'>try {\n    await fetchOrderData();\n} catch (err) {\n    console.error('Lỗi kết nối API:', err);\n}</code></pre>",
            "sec4": "<div class='p-4 rounded-xl border border-rose-200 bg-rose-50/60 my-4'><h4 class='font-bold text-rose-900 mb-2'>4.1. Quên từ khóa await</h4><p class='text-sm text-slate-700'>Nếu quên await, hàm sẽ trả về Promise chưa được giải quyết (unresolved).</p></div>"
        },
        {
            "tech_stack": "sql",
            "title": "Truy vấn dữ liệu nâng cao với SELECT và WHERE",
            "sec1": "<p class='text-slate-600 mb-4 leading-relaxed'>Trong hệ thống ngân hàng, chúng ta cần lọc danh sách giao dịch có giá trị lớn.</p>",
            "sec2": "<h3 id='sec-2-1' class='text-xl font-bold text-slate-900 mb-3'>2.1. Mệnh đề WHERE trong SQL</h3><p class='text-slate-600 mb-4 leading-relaxed'>Mệnh đề WHERE giúp lọc các dòng thỏa mãn điều kiện.</p><pre><code class='language-sql'>SELECT * FROM transactions WHERE amount >= 50000000;</code></pre>",
            "sec3": "<h3 id='sec-3-1' class='text-xl font-bold text-slate-900 mb-3'>3.1. Bảng dữ liệu giao dịch</h3><p class='text-slate-600 mb-4 leading-relaxed'>Ví dụ thực thi câu lệnh SQL.</p><pre><code class='language-sql'>SELECT customer_id, SUM(amount) AS total FROM transactions GROUP BY customer_id;</code></pre>",
            "sec4": "<div class='p-4 rounded-xl border border-amber-200 bg-amber-50/60 my-4'><h4 class='font-bold text-amber-900 mb-2'>4.1. Lưu ý về kiểu dữ liệu chuỗi</h4><p class='text-sm text-slate-700'>Chuỗi ký tự trong SQL bắt buộc phải bọc trong dấu nháy đơn.</p></div>"
        },
        {
            "tech_stack": "git",
            "title": "Giới thiệu Hệ thống Quản lý Phiên bản Git & VCS",
            "sec1": "<p class='text-slate-600 mb-4 leading-relaxed'>Tại sao lập trình viên cần Git để quản lý lịch sử mã nguồn dự án?</p>",
            "sec2": "<h3 id='sec-2-1' class='text-xl font-bold text-slate-900 mb-3'>2.1. Cấu trúc 3 trạng thái của Git</h3><p class='text-slate-600 mb-4 leading-relaxed'>Working Directory, Staging Area và Local Repository.</p>",
            "sec3": "<h3 id='sec-3-1' class='text-xl font-bold text-slate-900 mb-3'>3.1. Luồng lệnh khởi tạo cơ bản</h3><p class='text-slate-600 mb-4 leading-relaxed'>Các câu lệnh CLI Git phổ biến.</p><pre><code class='language-bash'>git status\ngit add .\ngit commit -m 'Initial commit'</code></pre>",
            "sec4": "<div class='p-4 rounded-xl border border-sky-200 bg-sky-50/60 my-4'><h4 class='font-bold text-sky-900 mb-2'>4.1. Khuyên dùng file .gitignore</h4><p class='text-sm text-slate-700'>Luôn bỏ các file rác hoặc secret key ra khỏi Git track.</p></div>"
        }
    ]

    all_passed = True

    for idx, tc in enumerate(test_cases, 1):
        stack = tc["tech_stack"]
        title = tc["title"]
        print(f"\n--- [Test {idx}] Tech Stack: {stack.upper()} | Title: {title} ---")

        domain_info = resolve_domain_engine(stack)
        print(f"  [Domain Adapter] Resolved Engine: {domain_info['engine_type']} | Visualizer: {domain_info['visualizer_type']}")

        # Create substantial paragraph text to reach realistic lesson content length (> 50KB)
        sample_para = "<p class='text-slate-600 mb-4 leading-relaxed'>Trong phát triển phần mềm doanh nghiệp, việc thiết kế cấu trúc chương trình rõ ràng là yếu tố tiên quyết giúp hệ thống duy trì được tính mở rộng và dễ bảo trì. Mỗi dòng mã lệnh cần được đánh giá dựa trên bối cảnh sử dụng thực tế và rủi ro vận hành.</p>\n" * 25
        
        payload = {
            "section_titles": {
                "sec1": "Đặt vấn đề thực tế",
                "sec2": "Cú pháp & Cơ chế",
                "sec3": "Các ví dụ ứng dụng thực tiễn",
                "sec4": "Tổng kết bài học & Lưu ý",
                "sec5": "Tài liệu tham khảo"
            },
            "sec1_html": tc["sec1"] + "\n" + sample_para,
            "sec2_html": tc["sec2"] + "\n" + sample_para,
            "sec3_html": tc["sec3"] + "\n" + sample_para + "\n" + '''
<div class="border rounded-xl bg-slate-50 my-5">
  <pre><code id="code-sb-1" class="language-python" contenteditable="true" data-original="print('Hello')">print('Hello')</code></pre>
  <button onclick="runPythonCode('code-sb-1', 'output-sb-1')">Chạy</button>
</div>
<div class="border rounded-xl bg-slate-50 my-5">
  <pre><code id="code-sb-2" class="language-python" contenteditable="true" data-original="print('World')">print('World')</code></pre>
  <button onclick="runPythonCode('code-sb-2', 'output-sb-2')">Chạy</button>
</div>''',
            "sec4_html": tc["sec4"] + "\n" + sample_para,
            "show_visualizer": True,
            "self_test_questions": [
                {
                    "question": f"Tình huống thực tế cho môn {stack.upper()}: Khi nào nên áp dụng kiến thức bài học?",
                    "options": ["Khi muốn tối ưu hóa quy trình", "Khi không cần kiểm tra", "Bỏ qua kiểm tra", "Không có đáp án"],
                    "correct_idx": 0,
                    "explanation": "Tối ưu hóa quy trình giúp hệ thống chạy ổn định và chính xác."
                }
            ]
        }

        # 1. Test JSON payload validator
        is_valid_json, json_errs = validate_reading_json_payload(payload)
        if not is_valid_json:
            print(f"  ❌ JSON Payload Validation Failed: {json_errs}")
            all_passed = False
            continue

        # 2. Render HTML via Jinja2 Engine
        metadata = {"lesson_title": title, "tech_stack": stack, "session_id": "Session 02", "lesson_id": "Lesson 01"}
        rendered_html = assemble_reading_html(payload, metadata)
        print(f"  [Jinja2 Engine] Rendered HTML length: {len(rendered_html)} bytes")

        # 3. Validate compiled HTML with Reading Material Validator
        is_valid_html, html_errs = validate_reading_material(rendered_html, metadata)
        if is_valid_html:
            print(f"  ✅ Validation PASS: HTML structural integrity and light-mode standards verified!")
        else:
            print(f"  ❌ HTML Validation Errors ({len(html_errs)}):")
            for err in html_errs:
                print(f"     - {err}")
            all_passed = False

    # 4. Zero-Fallback Fail-Fast Check (Empty tech_stack MUST raise ValueError)
    print("\n--- [Test 6] Zero-Fallback Fail-Fast Check (Empty tech_stack) ---")
    try:
        resolve_domain_engine("")
        print("  ❌ FAIL: resolve_domain_engine('') did NOT raise ValueError!")
        all_passed = False
    except ValueError as ve:
        print(f"  ✅ PASS: Empty tech_stack correctly raised ValueError: {ve}")

    print("\n==========================================================")
    if all_passed:
        print("🎉 ALL TESTS PASSED! Reading Material Refactoring Successful!")
    else:
        print("❌ SOME TESTS FAILED. Check errors above.")
    print("==========================================================")
    return all_passed

if __name__ == "__main__":
    success = run_pipeline_tests()
    sys.exit(0 if success else 1)
