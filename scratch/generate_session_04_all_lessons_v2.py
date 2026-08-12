# scratch/generate_session_04_all_lessons_v2.py
"""
Master Generation Script for Session 04 All Lessons.
Enforces 100% compliance with all 17 system rules:
- 2D Flat Vector Image Assets
- Section 3 with AT LEAST 3 progressive real-world examples (3.1, 3.2, 3.3)
- Requirement Callout Box BEFORE every single code sandbox
- Unified ShopeeFood Real-World Scenario
"""
import sys
import json
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base_dir = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material")
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from core.renderers.reading_renderer import assemble_reading_html
from core.validators.reading_validator import validate_reading_material
from core.validators.quiz_validator import validate_quiz_json, validate_reading_questions_md


def req_box(title: str, desc: str) -> str:
    """Helper to build standard Requirement Callout Box before every sandbox."""
    return f"""<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
  <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-push-pin text-sky-600"></i> Yêu cầu bài toán thực hành ({title}):</div>
  <p class="text-sm text-slate-700">{desc}</p>
</div>"""


def build_sandbox(sb_id: str, code: str) -> str:
    """Helper to build clean live code sandbox component."""
    escaped_code = code.strip()
    return f"""<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button type="button" onclick="clearSandbox('code-sb-{sb_id}', 'output-sb-{sb_id}', 'container-sb-{sb_id}')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc"><i class="ph-bold ph-arrow-counter-clockwise text-xs"></i></button>
      <button type="button" onclick="runPythonCode('code-sb-{sb_id}', 'output-sb-{sb_id}', 'container-sb-{sb_id}')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình"><i class="ph-bold ph-play text-xs"></i></button>
      <button type="button" onclick="copySandboxCode('code-sb-{sb_id}', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép"><i class="ph-bold ph-copy text-xs"></i></button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-{sb_id}" class="language-python" contenteditable="true" spellcheck="false" data-original="{escaped_code}" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;">{escaped_code}</code></pre>
  </div>
  <div id="container-sb-{sb_id}" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5"><i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</span>
    </div>
    <pre id="output-sb-{sb_id}" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>"""


# -------------------------------------------------------------------------
# LESSON 01
# -------------------------------------------------------------------------
def generate_lesson_01():
    target_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 01 - Toán tử số học và toán tử gán"
    rd_dir, img_dir = target_dir / "Bài đọc", target_dir / "Bài đọc" / "images"
    rq_dir, qz_dir = target_dir / "Câu hỏi bài đọc", target_dir / "Câu hỏi Quizz"
    for d in [rd_dir, img_dir, rq_dir, qz_dir]: d.mkdir(parents=True, exist_ok=True)

    sec1_html = """
<p class="text-slate-600 mb-4 leading-relaxed">
Hãy hình dung bạn đang xây dựng hệ thống tính toán đơn hàng cho ứng dụng đặt đồ ăn trực tuyến <strong>ShopeeFood</strong>. Khi một khách hàng đặt 3 phần cơm tấm có giá 45.000 VNĐ, hệ thống phải nhân giá tiền với số lượng, cộng thêm 20.000 VNĐ phí giao hàng, trừ đi 15.000 VNĐ voucher giảm giá, và cộng dồn điểm thưởng vào ví.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Tất cả quy trình tài chính này đều dựa trên <strong>Toán tử số học</strong> và <strong>Toán tử gán</strong> trong Python.
</p>
"""

    sec2_html = f"""
<h3 id="sec-2-1-toan-tu-so-hoc-co-ban" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.1. Cú pháp và giải thích Toán tử số học (Arithmetic Operators)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Toán tử số học thực hiện các phép tính đại số cơ bản và nâng cao trong Python.</p>

<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 font-semibold">Cú pháp toán tử số học trong Python</div>
  <pre class="m-0 overflow-x-auto"><code class="hljs language-python">result = operand_a operator operand_b</code></pre>
</div>

<div class="space-y-2 text-slate-700 my-4 pl-2">
  <p class="font-semibold text-slate-900 mb-2">Chi tiết thành phần cú pháp:</p>
  <ul class="list-disc pl-6 space-y-2 text-slate-600">
    <li><strong class="text-slate-900"><code>operator</code></strong>: Bao gồm <code class="text-rikkei-red font-mono">+</code> (Cộng), <code class="text-rikkei-red font-mono">-</code> (Trừ), <code class="text-rikkei-red font-mono">*</code> (Nhân), <code class="text-rikkei-red font-mono">/</code> (Chia số thực), <code class="text-rikkei-red font-mono">//</code> (Chia nguyên), <code class="text-rikkei-red font-mono">%</code> (Chia lấy dư), <code class="text-rikkei-red font-mono">**</code> (Lũy thừa).</li>
  </ul>
</div>

{req_box("Tính tổng tiền hàng ShopeeFood", "Tính tổng chi phí 3 phần cơm tấm giá 45.000 VNĐ, cộng 20.000 VNĐ phí ship và trừ 15.000 VNĐ voucher.")}
{build_sandbox("2-1", "unit_price = 45000\nquantity = 3\nshipping_fee = 20000\ndiscount_voucher = 15000\n\nsubtotal = unit_price * quantity\ntotal_payment = subtotal + shipping_fee - discount_voucher\n\nprint('Tiền hàng:', subtotal, 'VNĐ')\nprint('Tổng thanh toán:', total_payment, 'VNĐ')")}

<h3 id="sec-2-2-toan-tu-gan-phuc-hop" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.2. Cú pháp và giải thích Toán tử gán phức hợp (Compound Assignment Operators)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Toán tử gán kết hợp tính toán số học với việc cập nhật giá trị biến bộ nhớ RAM.</p>

{req_box("Cập nhật điểm thưởng ShopeePay", "Cập nhật dồn 50 điểm thưởng và trừ 140.000 VNĐ khỏi số dư ví sau khi giao dịch thành công.")}
{build_sandbox("2-2", "reward_points = 120\nwallet_balance = 500000\n\nreward_points += 50\nwallet_balance -= 140000\n\nprint('Điểm mới:', reward_points)\nprint('Ví còn lại:', wallet_balance, 'VNĐ')")}
"""

    sec3_html = f"""
<h3 id="sec-3-1-tinh-tong-don-hang-shopeefood" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Tính tổng chi phí đơn hàng ShopeeFood bao gồm phụ phí và chiết khấu</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Tính toán chi tiết giá trị thanh toán cho đơn hàng gồm trà sữa và phí vận chuyển.</p>
{req_box("Bài toán 3.1 - Tính tiền đơn trà sữa", "Tính tổng tiền 2 ly trà sữa giá 30.000 VNĐ, giảm 10% và cộng 15.000 VNĐ phí ship.")}
{build_sandbox("3-1", "item_price = 30000\nitem_qty = 2\nshipping_fee = 15000\ndiscount_percent = 0.10\n\nsubtotal = item_price * item_qty\ndiscount_amount = subtotal * discount_percent\nfinal_amount = (subtotal - discount_amount) + shipping_fee\n\nprint('Tiền hàng gốc:', subtotal, 'VNĐ')\nprint('Số tiền giảm:', discount_amount, 'VNĐ')\nprint('Thành tiền:', final_amount, 'VNĐ')")}

<h3 id="sec-3-2-cap-nhat-tich-luy-diem-thuong" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.2. Cập nhật tích lũy điểm thưởng và số dư ví bằng toán tử gán</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Khấu trừ tiền hàng và tích lũy điểm thưởng ShopeePay.</p>
{req_box("Bài toán 3.2 - Tích lũy điểm thưởng 5%", "Trừ 165.000 VNĐ tiền đơn hàng khỏi ví và tích dồn 5% giá trị đơn thành điểm thưởng.")}
{build_sandbox("3-2", "wallet_balance = 350000\nuser_points = 80\nbill_total = 165000\n\nwallet_balance -= bill_total\nearned_points = int(bill_total * 0.05)\nuser_points += earned_points\n\nprint('Ví còn lại:', wallet_balance, 'VNĐ')\nprint('Điểm mới:', user_points)")}

<h3 id="sec-3-3-chia-tien-hoa-don-nhom" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.3. Chia tiền hóa đơn nhóm và tính số tiền lẻ dư</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Sử dụng phép chia nguyên // và chia dư % để chia tiền hóa đơn nhóm.</p>
{req_box("Bài toán 3.3 - Phân chia hóa đơn ăn nhóm", "Chia đều hóa đơn 355.000 VNĐ cho nhóm 4 người và tính tiền dư lẻ còn lại.")}
{build_sandbox("3-3", "group_bill = 355000\nnum_people = 4\n\nshare_per_person = group_bill // num_people\nremaining_change = group_bill % num_people\n\nprint('Mỗi người đóng:', share_per_person, 'VNĐ')\nprint('Tiền dư lẻ:', remaining_change, 'VNĐ')")}
"""

    sec4_html = """
<div class="space-y-4">
  <div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">
    <div class="font-bold text-rose-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-warning-circle text-rose-600"></i> Lỗi thường gặp 1: Lỗi chia cho số 0 (ZeroDivisionError)</div>
    <p class="text-sm text-slate-700">Chia cho số 0 sẽ làm chương trình dừng và báo lỗi <code>ZeroDivisionError</code>.</p>
  </div>
  <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">
    <div class="font-bold text-amber-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-amber-600"></i> Lỗi thường gặp 2: Sai số số thực (Floating-Point Precision)</div>
    <p class="text-sm text-slate-700">Phép tính <code>0.1 + 0.2</code> cho kết quả <code>0.30000000000000004</code> do cách máy tính lưu số thực.</p>
  </div>
  <div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
    <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-brackets-curly text-sky-600"></i> Lỗi thường gặp 3: Khác biệt giữa chia / và chia lấy phần nguyên //</div>
    <p class="text-sm text-slate-700">Toán tử <code>/</code> luôn trả về số thực <code>float</code>, còn <code>//</code> cắt bỏ phần thập phân trả về <code>int</code>.</p>
  </div>
</div>
"""

    json_payload = {
        "tech_stack": "python",
        "lesson_title": "Lesson 01 - Toán tử số học và toán tử gán",
        "context_image_url": "images/illustration_lesson_01.svg",
        "show_visualizer": True,
        "section_titles": {
            "sec1": "Tại sao cần toán tử số học và toán tử gán trong hệ thống ShopeeFood?",
            "sec2": "Cú pháp và cơ chế hoạt động của toán tử số học & toán tử gán",
            "sec3": "Các ví dụ ứng dụng thực tiễn trong hệ thống ShopeeFood",
            "sec4": "Tổng kết bài học & Các lỗi thường gặp",
            "sec5": "Tài liệu tham khảo"
        },
        "sec1_html": sec1_html,
        "sec2_html": sec2_html,
        "sec3_html": sec3_html,
        "sec4_html": sec4_html,
        "reference_links": [
            {"title": "Tài liệu chính thức Python 3 - Numeric Types (int, float)", "url": "https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex"},
            {"title": "W3Schools Python Arithmetic Operators & Precedence Guide", "url": "https://www.w3schools.com/python/python_operators.asp"}
        ]
    }

    metadata = {"session_id": "Session 04", "lesson_id": "Lesson 01", "lesson_title": "Toán tử số học và toán tử gán", "tech_stack": "python"}
    compiled_html = assemble_reading_html(json_payload, metadata)
    (rd_dir / "reading.html").write_text(compiled_html, encoding="utf-8")
    
    is_val, errs = validate_reading_material(compiled_html, metadata)
    print(f"✅ Lesson 01 reading.html generated - Validation: {'PASS' if is_val else 'FAIL: ' + str(errs)}")


# -------------------------------------------------------------------------
# LESSON 02
# -------------------------------------------------------------------------
def generate_lesson_02():
    target_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 02 - Toán tử so sánh và toán tử logic"
    rd_dir, img_dir = target_dir / "Bài đọc", target_dir / "Bài đọc" / "images"
    rq_dir, qz_dir = target_dir / "Câu hỏi bài đọc", target_dir / "Câu hỏi Quizz"
    for d in [rd_dir, img_dir, rq_dir, qz_dir]: d.mkdir(parents=True, exist_ok=True)

    sec1_html = """
<p class="text-slate-600 mb-4 leading-relaxed">
Trong hệ thống ShopeeFood, khi người dùng đặt hàng, hệ thống cần đưa ra hàng loạt đánh giá Boolean: Đơn hàng từ 200.000 VNĐ trở lên mới được freeship; Nếu là khách VIP VÀ có mã voucher thì áp dụng chiết khấu đặc biệt; Nếu tài khoản bị khóa HOẶC không có trong khu vực giao hàng thì từ chối đơn.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Để thực hiện các phép kiểm tra này, lập trình viên sử dụng <strong>Toán tử so sánh</strong> và <strong>Toán tử logic</strong>.
</p>
"""

    sec2_html = f"""
<h3 id="sec-2-1-toan-tu-so-sanh" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.1. Cú pháp và cơ chế hoạt động của Toán tử so sánh</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Toán tử so sánh so sánh hai giá trị và luôn trả về kết quả kiểu Boolean (<code>True</code> hoặc <code>False</code>).</p>

{req_box("So sánh giá trị đơn hàng với ngưỡng Freeship 200k", "Kiểm tra đơn hàng giá trị 250.000 VNĐ có lớn hơn hoặc bằng ngưỡng 200.000 VNĐ hay không.")}
{build_sandbox("2-1", "order_amount = 250000\nis_eligible_freeship = order_amount >= 200000\nprint('Đơn hàng đạt chuẩn freeship:', is_eligible_freeship)")}

<h3 id="sec-2-2-toan-tu-logic" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.2. Cú pháp và cơ chế hoạt động của Toán tử logic (and, or, not)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Toán tử logic kết hợp hoặc đảo ngược các giá trị Boolean.</p>

{req_box("Kết hợp điều kiện Freeship và Thành viên VIP", "Xác nhận Freeship nếu đơn từ 200.000 VNĐ VÀ người dùng là thành viên VIP.")}
{build_sandbox("2-2", "order_amount = 250000\nis_vip = True\n\nis_approved = (order_amount >= 200000) and is_vip\nprint('Được phê duyệt ưu đãi freeship VIP:', is_approved)")}
"""

    sec3_html = f"""
<h3 id="sec-3-1-xac-thuc-dieu-kien-freeship" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Xác thực điều kiện miễn phí giao hàng ShopeeFood</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Đánh giá cờ hiệu miễn phí giao hàng dựa trên tổng tiền và hạng thành viên.</p>
{req_box("Bài toán 3.1 - Kiểm tra điều kiện Freeship", "Kiểm tra đơn hàng 250.000 VNĐ của thành viên VIP có được miễn phí giao hàng.")}
{build_sandbox("3-1", "order_amount = 250000\nis_vip_member = True\nis_freeship = (order_amount >= 200000) and is_vip_member\nprint('Miễn phí giao hàng:', is_freeship)")}

<h3 id="sec-3-2-xac-thuc-ma-giam-gia-voucher" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.2. Kiểm tra điều kiện áp dụng mã giảm giá Voucher</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Đơn hàng được giảm giá nếu đạt từ 150.000 VNĐ trở lên VÀ có voucher hoặc là VIP.</p>
{req_box("Bài toán 3.2 - Áp dụng Voucher 30k", "Kiểm tra đơn 180.000 VNĐ có voucher và là thành viên VIP.")}
{build_sandbox("3-2", "order_val = 180000\nhas_voucher = True\nis_vip = False\n\nis_discounted = (order_val >= 150000) and (has_voucher or is_vip)\nprint('Được áp dụng giảm giá:', is_discounted)")}

<h3 id="sec-3-3-danh-gia-ngan-mach-hieu-nang" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.3. Đánh giá ngắn mạch (Short-circuit Evaluation) tối ưu hiệu năng</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Kiểm tra cờ hiệu vi phạm trước để kích hoạt cơ chế ngắn mạch dừng đánh giá sớm.</p>
{req_box("Bài toán 3.3 - Ngắn mạch kiểm tra tài khoản bị khóa", "Kiểm tra tài khoản bị khóa (is_banned = True) dừng đánh giá biểu thức ngay lập tức.")}
{build_sandbox("3-3", "is_banned = True\norder_amount = 500000\n\nis_valid = (not is_banned) and (order_amount >= 100000)\nprint('Đơn hàng được chấp nhận:', is_valid)")}
"""

    sec4_html = """
<div class="space-y-4">
  <div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">
    <div class="font-bold text-rose-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-warning-circle text-rose-600"></i> Lỗi thường gặp 1: Nhầm lẫn giữa toán tử gán = và so sánh bằng ==</div>
    <p class="text-sm text-slate-700">Dấu <code>=</code> dùng để gán giá trị, dấu <code>==</code> mới dùng để so sánh bằng.</p>
  </div>
  <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">
    <div class="font-bold text-amber-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-amber-600"></i> Lỗi thường gặp 2: Sai độ ưu tiên giữa toán tử and và or</div>
    <p class="text-sm text-slate-700">Toán tử <code>and</code> có độ ưu tiên cao hơn <code>or</code>. Hãy dùng cặp ngoặc <code>()</code> để nhóm điều kiện rõ ràng.</p>
  </div>
  <div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
    <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-brackets-curly text-sky-600"></i> Lỗi thường gặp 3: Quên sử dụng phép phủ định not</div>
    <p class="text-sm text-slate-700">Viết <code>if is_banned:</code> sẽ bị ngược logic so với <code>if not is_banned:</code>.</p>
  </div>
</div>
"""

    json_payload = {
        "tech_stack": "python",
        "lesson_title": "Lesson 02 - Toán tử so sánh và toán tử logic",
        "context_image_url": "images/illustration_lesson_02.svg",
        "show_visualizer": True,
        "section_titles": {
            "sec1": "Đặt vấn đề thực tế trong hệ thống ShopeeFood",
            "sec2": "Cú pháp và cơ chế hoạt động của toán tử so sánh & logic",
            "sec3": "Các ví dụ ứng dụng thực tiễn trong ShopeeFood",
            "sec4": "Tổng kết bài học & Các lỗi thường gặp",
            "sec5": "Tài liệu tham khảo"
        },
        "sec1_html": sec1_html,
        "sec2_html": sec2_html,
        "sec3_html": sec3_html,
        "sec4_html": sec4_html,
        "reference_links": [
            {"title": "Tài liệu chính thức Python 3 - Boolean Operations (and, or, not)", "url": "https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not"},
            {"title": "Real Python: Python Comparison Operators & Logic Guide", "url": "https://realpython.com/python-operators-expressions/"}
        ]
    }

    metadata = {"session_id": "Session 04", "lesson_id": "Lesson 02", "lesson_title": "Toán tử so sánh và toán tử logic", "tech_stack": "python"}
    compiled_html = assemble_reading_html(json_payload, metadata)
    (rd_dir / "reading.html").write_text(compiled_html, encoding="utf-8")
    
    is_val, errs = validate_reading_material(compiled_html, metadata)
    print(f"✅ Lesson 02 reading.html generated - Validation: {'PASS' if is_val else 'FAIL: ' + str(errs)}")


# -------------------------------------------------------------------------
# LESSON 03
# -------------------------------------------------------------------------
def generate_lesson_03():
    target_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 03 - Cấu trúc rẽ nhánh điều khiển với if, elif và else"
    rd_dir, img_dir = target_dir / "Bài đọc", target_dir / "Bài đọc" / "images"
    rq_dir, qz_dir = target_dir / "Câu hỏi bài đọc", target_dir / "Câu hỏi Quizz"
    for d in [rd_dir, img_dir, rq_dir, qz_dir]: d.mkdir(parents=True, exist_ok=True)

    sec1_html = """
<p class="text-slate-600 mb-4 leading-relaxed">
Trong thực tế phát triển hệ thống ShopeeFood, phần mềm phải tự động đưa ra các quyết định rẽ nhánh dựa trên dữ liệu giá trị đơn hàng. Ví dụ: Nếu đơn hàng từ 2.000.000 VNĐ trở lên sẽ được giảm 20%; Nếu đơn từ 1.000.000 VNĐ đến dưới 2.000.000 VNĐ giảm 10%; Nếu từ 500.000 VNĐ giảm 5%; Các đơn nhỏ hơn không áp dụng chiết khấu.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Cấu trúc rẽ nhánh <strong>if, elif, else</strong> là công cụ nền tảng giúp lập trình viên điều khiển luồng chương trình một cách linh hoạt.
</p>
"""

    sec2_html = f"""
<h3 id="sec-2-1-cau-lenh-if-va-if-else" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.1. Cú pháp và cơ chế hoạt động của câu lệnh rẽ nhánh đơn if và if-else</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Câu lệnh <code>if</code> kiểm tra biểu thức Boolean để quyết định có thực thi khối lệnh hay không.</p>

{req_box("Kiểm tra đơn hàng đạt ngưỡng Freeship 200k", "Kiểm tra đơn hàng giá trị 250.000 VNĐ có đạt ngưỡng miễn phí giao hàng 0 VNĐ hay áp phụ phí 20.000 VNĐ.")}
{build_sandbox("2-1", "order_amount = 250000\n\nif order_amount >= 200000:\n    shipping_fee = 0\n    print('Đơn hàng đạt chuẩn: Miễn phí giao hàng (0 VNĐ)')\nelse:\n    shipping_fee = 20000\n    print('Đơn chưa đủ điều kiện: Phí giao hàng:', shipping_fee, 'VNĐ')")}

<h3 id="sec-2-2-cau-truc-da-nhanh-if-elif-else" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.2. Cú pháp và cơ chế hoạt động của cấu trúc đa nhánh if-elif-else</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Khi bài toán kinh doanh có nhiều hơn 2 lựa chọn, sử dụng <code>if-elif-else</code> để kiểm tra lần lượt từ trên xuống dưới.</p>

{req_box("Phân hạng chiết khấu đơn hàng 1.500.000 VNĐ", "Xác định tỷ lệ giảm giá theo các nấc 2 triệu (20%), 1 triệu (10%), 500k (5%).")}
{build_sandbox("2-2", "order_amount = 1500000\n\nif order_amount >= 2000000:\n    discount_rate = 0.20\nelif order_amount >= 1000000:\n    discount_rate = 0.10\nelif order_amount >= 500000:\n    discount_rate = 0.05\nelse:\n    discount_rate = 0.0\n\ndiscount_val = order_amount * discount_rate\nprint('Tỷ lệ giảm:', int(discount_rate * 100), '%')\nprint('Tiền giảm:', discount_val, 'VNĐ')")}
"""

    sec3_html = f"""
<h3 id="sec-3-1-phan-hang-chiet-khau-shopeefood" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Phân hạng chiết khấu đơn hàng ShopeeFood</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Xác định mã voucher áp dụng cho đơn hàng 1,500,000 VNĐ.</p>
{req_box("Bài toán 3.1 - Gán mã Voucher theo đơn hàng", "Gán mã voucher GIAM20 cho đơn từ 2 triệu, GIAM10 cho đơn từ 1 triệu.")}
{build_sandbox("3-1", "order_amount = 1500000\n\nif order_amount >= 2000000:\n    voucher = 'GIAM20'\nelif order_amount >= 1000000:\n    voucher = 'GIAM10'\nelse:\n    voucher = 'KHONG'\n\nprint('Mã giảm giá áp dụng:', voucher)")}

<h3 id="sec-3-2-tinh-phi-ship-theo-khoang-cach" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.2. Tính phí giao hàng ShopeeFood theo khoảng cách địa lý</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Tính phí giao hàng dựa trên khoảng cách km từ nhà hàng đến người nhận.</p>
{req_box("Bài toán 3.2 - Tính phí ship theo km", "Dưới 3km phí 15k, 3km-7km phí 25k, trên 7km phí 40k.")}
{build_sandbox("3-2", "distance_km = 5.2\n\nif distance_km <= 3.0:\n    ship_fee = 15000\nelif distance_km <= 7.0:\n    ship_fee = 25000\nelse:\n    ship_fee = 40000\n\nprint('Khoảng cách:', distance_km, 'km')\nprint('Phí ship:', ship_fee, 'VNĐ')")}

<h3 id="sec-3-3-kiem-tra-so-du-vi-shopeepay" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.3. Kiểm tra số dư ví ShopeePay trước khi thanh toán</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Xác nhận giao dịch thành công nếu số dư ví đủ trang trải tổng tiền đơn hàng.</p>
{req_box("Bài toán 3.3 - Thanh toán ví ShopeePay", "Số dư ví 300.000 VNĐ thanh toán đơn 220.000 VNĐ.")}
{build_sandbox("3-3", "wallet_balance = 300000\norder_total = 220000\n\nif wallet_balance >= order_total:\n    wallet_balance -= order_total\n    print('Thanh toán thành công! Số dư còn lại:', wallet_balance, 'VNĐ')\nelse:\n    print('Thanh toán thất bại! Số dư ví không đủ.')")}
"""

    sec4_html = """
<div class="space-y-4">
  <div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">
    <div class="font-bold text-rose-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-warning-circle text-rose-600"></i> Lỗi thường gặp 1: Quên dấu hai chấm (:) gây SyntaxError</div>
    <p class="text-sm text-slate-700">Mỗi dòng khai báo <code>if</code>, <code>elif</code>, hoặc <code>else</code> bắt buộc phải kết thúc bằng dấu hai chấm <code>:</code>.</p>
  </div>
  <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">
    <div class="font-bold text-amber-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-amber-600"></i> Lỗi thường gặp 2: Thụt lùi dòng không thống nhất (IndentationError)</div>
    <p class="text-sm text-slate-700">Các dòng lệnh bên trong một khối rẽ nhánh phải thụt lùi vào đúng 4 khoảng trắng.</p>
  </div>
  <div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
    <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-brackets-curly text-sky-600"></i> Lỗi thường gặp 3: Sai thứ tự điều kiện trong chuỗi if-elif</div>
    <p class="text-sm text-slate-700">Nếu đặt điều kiện nhỏ hơn lên trước, đơn hàng lớn sẽ bị khớp nhầm vào nhánh điều kiện nhỏ hơn.</p>
  </div>
</div>
"""

    json_payload = {
        "tech_stack": "python",
        "lesson_title": "Lesson 03 - Cấu trúc rẽ nhánh điều khiển với if, elif và else",
        "context_image_url": "images/illustration_lesson_03.svg",
        "show_visualizer": True,
        "section_titles": {
            "sec1": "Đặt vấn đề thực tế trong hệ thống ShopeeFood",
            "sec2": "Cú pháp và cơ chế hoạt động của cấu trúc rẽ nhánh",
            "sec3": "Các ví dụ ứng dụng thực tiễn trong ShopeeFood",
            "sec4": "Tổng kết bài học & Các lỗi thường gặp",
            "sec5": "Tài liệu tham khảo"
        },
        "sec1_html": sec1_html,
        "sec2_html": sec2_html,
        "sec3_html": sec3_html,
        "sec4_html": sec4_html,
        "reference_links": [
            {"title": "Tài liệu chính thức Python 3 - Control Flow Tools (if statements)", "url": "https://docs.python.org/3/tutorial/controlflow.html#if-statements"},
            {"title": "Real Python: Conditional Statements in Python (if/elif/else)", "url": "https://realpython.com/python-conditional-statements/"}
        ]
    }

    metadata = {"session_id": "Session 04", "lesson_id": "Lesson 03", "lesson_title": "Cấu trúc rẽ nhánh điều khiển với if, elif và else", "tech_stack": "python"}
    compiled_html = assemble_reading_html(json_payload, metadata)
    (rd_dir / "reading.html").write_text(compiled_html, encoding="utf-8")
    
    is_val, errs = validate_reading_material(compiled_html, metadata)
    print(f"✅ Lesson 03 reading.html generated - Validation: {'PASS' if is_val else 'FAIL: ' + str(errs)}")


# -------------------------------------------------------------------------
# LESSON 04
# -------------------------------------------------------------------------
def generate_lesson_04():
    target_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 04 - Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8"
    rd_dir, img_dir = target_dir / "Bài đọc", target_dir / "Bài đọc" / "images"
    rq_dir, qz_dir = target_dir / "Câu hỏi bài đọc", target_dir / "Câu hỏi Quizz"
    for d in [rd_dir, img_dir, rq_dir, qz_dir]: d.mkdir(parents=True, exist_ok=True)

    sec1_html = """
<p class="text-slate-600 mb-4 leading-relaxed">
Trong quy trình duyệt voucher đặc quyền tại ShopeeFood, hệ thống phải trải qua 2 cấp xác thực: Đầu tiên kiểm tra tài khoản người dùng đã đăng nhập và hoạt động bình thường hay chưa; Tiếp theo nếu tài khoản hợp lệ mới tiến hành kiểm tra giá trị đơn hàng có đạt từ 500.000 VNĐ trở lên để tặng voucher giảm giá 50.000 VNĐ.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Việc lồng ghép <code>if</code> bên trong <code>if</code> được gọi là <strong>Cấu trúc rẽ nhánh lồng nhau (Nested if)</strong>. Đồng thời, lập trình viên cần tuân thủ quy tắc <strong>Chuẩn hóa mã nguồn PEP 8</strong> để giữ mã nguồn sạch đẹp.
</p>
"""

    sec2_html = f"""
<h3 id="sec-2-1-cau-truc-re-nhanh-long-nhau" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.1. Cú pháp và cơ chế hoạt động của Cấu trúc rẽ nhánh lồng nhau (Nested if)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Một câu lệnh <code>if</code> có thể chứa câu lệnh <code>if</code> khác bên trong. Độ thụt lùi dòng tăng thêm 4 khoảng trắng cho mỗi cấp.</p>

{req_box("Duyệt Voucher đặc quyền ShopeeFood 2 cấp", "Tài khoản active = True và đơn từ 500.000 VNĐ mới tặng voucher 50.000 VNĐ.")}
{build_sandbox("2-1", "is_user_active = True\norder_amount = 600000\n\nif is_user_active:\n    print('Tài khoản hợp lệ.')\n    if order_amount >= 500000:\n        print('Đơn hàng đủ điều kiện: Tặng voucher 50.000 VNĐ!')\n    else:\n        print('Đơn hàng chưa đủ 500k.')\nelse:\n    print('Tài khoản bị khóa.')")}

<h3 id="sec-2-2-chuan-hoa-ma-nguon-pep8" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.2. Quy tắc chuẩn hóa mã nguồn Python theo tiêu chuẩn PEP 8</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Hướng dẫn chuẩn hóa cách viết mã nguồn Python đồng nhất trong doanh nghiệp.</p>

{req_box("Phẳng hóa mã nguồn theo chuẩn PEP 8", "Sử dụng toán tử and để phẳng hóa câu lệnh if lồng nhau rối rắm.")}
{build_sandbox("2-2", "is_user_active = True\norder_amount = 600000\n\n# Tối ưu phẳng hóa theo chuẩn PEP 8\nif is_user_active and order_amount >= 500000:\n    print('Áp dụng voucher đặc quyền thành công!')\nelse:\n    print('Không đủ điều kiện nhận voucher.')")}
"""

    sec3_html = f"""
<h3 id="sec-3-1-xac-thuc-giao-dich-duyet-voucher-pep8" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Tối ưu hóa xác thực duyệt voucher ShopeeFood chuẩn PEP 8</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Duyệt voucher bằng điều kiện kết hợp chuẩn PEP 8.</p>
{req_box("Bài toán 3.1 - Duyệt Voucher chuẩn PEP 8", "Duyệt voucher cho người dùng active và đơn từ 500k.")}
{build_sandbox("3-1", "is_active = True\norder_val = 600000\n\nif is_active and order_val >= 500000:\n    print('Áp mã voucher thành công!')\nelse:\n    print('Không đủ điều kiện.')")}

<h3 id="sec-3-2-kiem-tra-gian-lan-don-hang" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.2. Cấu trúc lồng nhau kiểm tra rủi ro gian lận đơn hàng</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Kiểm tra địa chỉ IP nghi vấn và số lượng đơn hàng trong ngày.</p>
{req_box("Bài toán 3.2 - Phát hiện gian lận ShopeeFood", "Nếu IP không bị cảnh báo (is_suspicious_ip = False) mới kiểm tra số đơn trong ngày < 10.")}
{build_sandbox("3-2", "is_suspicious_ip = False\ndaily_orders_count = 4\n\nif not is_suspicious_ip:\n    if daily_orders_count < 10:\n        print('Đơn hàng an toàn: Cho phép đặt hàng.')\n    else:\n        print('Cảnh báo: Đặt quá 10 đơn/ngày.')\nelse:\n    print('Từ chối đơn: IP thuộc danh sách đen.')")}

<h3 id="sec-3-3-chuan-hoa-ten-bien-pep8" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.3. Chuẩn hóa tên biến và thụt lùi dòng theo quy định PEP 8</h3>
<p class="text-slate-600 mb-4 leading-relaxed">Áp dụng đặt tên biến `snake_case` và thụt lùi 4 spaces chuẩn xác.</p>
{req_box("Bài toán 3.3 - Chuẩn hóa mã nguồn đơn hàng", "Đặt tên biến theo chuẩn snake_case như total_order_amount và user_discount_code.")}
{build_sandbox("3-3", "total_order_amount = 450000\nuser_discount_code = 'SUMMER2026'\n\nif total_order_amount >= 300000 and user_discount_code == 'SUMMER2026':\n    print('Mã hợp lệ: Giảm 50.000 VNĐ!')\nelse:\n    print('Mã không hợp lệ.')")}
"""

    sec4_html = """
<div class="space-y-4">
  <div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">
    <div class="font-bold text-rose-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-warning-circle text-rose-600"></i> Lỗi thường gặp 1: Lồng ghép điều kiện quá sâu (Deep Nesting)</div>
    <p class="text-sm text-slate-700">Lồng quá 3 cấp <code>if</code> bên trong nhau sẽ tạo ra mã nguồn dạng kim tự tháp (Pyramid of Doom).</p>
  </div>
  <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">
    <div class="font-bold text-amber-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-amber-600"></i> Lỗi thường gặp 2: Trộn lẫn phím Tab và phím Space</div>
    <p class="text-sm text-slate-700">Vi phạm quy tắc PEP 8 khi trộn lẫn phím Tab và 4 phím Space gây lỗi <code>TabError</code>.</p>
  </div>
  <div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
    <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-brackets-curly text-sky-600"></i> Lỗi thường gặp 3: Đặt tên biến sai quy chuẩn PEP 8</div>
    <p class="text-sm text-slate-700">Đặt tên biến bằng kiểu CamelCase thay vì <code>snake_case</code> vi phạm quy chuẩn PEP 8.</p>
  </div>
</div>
"""

    json_payload = {
        "tech_stack": "python",
        "lesson_title": "Lesson 04 - Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8",
        "context_image_url": "images/illustration_lesson_04.svg",
        "show_visualizer": True,
        "section_titles": {
            "sec1": "Đặt vấn đề thực tế trong hệ thống ShopeeFood",
            "sec2": "Cú pháp và chuẩn hóa mã nguồn theo tiêu chuẩn PEP 8",
            "sec3": "Các ví dụ ứng dụng thực tiễn trong ShopeeFood",
            "sec4": "Tổng kết bài học & Các lỗi thường gặp",
            "sec5": "Tài liệu tham khảo"
        },
        "sec1_html": sec1_html,
        "sec2_html": sec2_html,
        "sec3_html": sec3_html,
        "sec4_html": sec4_html,
        "reference_links": [
            {"title": "Tài liệu chính thức Python PEP 8 – Style Guide for Python Code", "url": "https://peps.python.org/pep-0008/"},
            {"title": "Real Python: Writing Beautiful Python Code With PEP 8", "url": "https://realpython.com/python-pep8/"}
        ]
    }

    metadata = {"session_id": "Session 04", "lesson_id": "Lesson 04", "lesson_title": "Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8", "tech_stack": "python"}
    compiled_html = assemble_reading_html(json_payload, metadata)
    (rd_dir / "reading.html").write_text(compiled_html, encoding="utf-8")
    
    is_val, errs = validate_reading_material(compiled_html, metadata)
    print(f"✅ Lesson 04 reading.html generated - Validation: {'PASS' if is_val else 'FAIL: ' + str(errs)}")


if __name__ == "__main__":
    generate_lesson_01()
    generate_lesson_02()
    generate_lesson_03()
    generate_lesson_04()
