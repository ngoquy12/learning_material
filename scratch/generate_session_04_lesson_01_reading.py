# scratch/generate_session_04_lesson_01_reading.py
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

def generate_lesson_01():
    base_dir = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material")
    target_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 01 - Toán tử số học và toán tử gán\Bài đọc"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    img_dir = target_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    
    out_file = target_dir / "reading.html"
    svg_file = img_dir / "illustration_lesson_01.svg"

    # Generate High-Depth 2D Flat Vector Infographic SVG Asset (Title-Free & 100% Accented Vietnamese)
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%" height="100%">
  <rect width="800" height="280" fill="#f8fafc" rx="16"/>
  <rect x="16" y="16" width="768" height="248" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" rx="12"/>
  
  <!-- TIER 1: THÔNG TIN ĐƠN HÀNG BAN ĐẦU -->
  <g transform="translate(35, 35)">
    <rect width="210" height="210" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" rx="10"/>
    <rect width="210" height="36" fill="#e2e8f0" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">1. Chi tiết đơn hàng ban đầu</text>
    
    <!-- Item row 1 -->
    <rect x="15" y="50" width="180" height="40" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="68" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Cơm tấm sườn nướng</text>
    <text x="25" y="83" font-family="JetBrains Mono, monospace" font-size="11" fill="#be111c">45.000 VNĐ × 3 phần</text>
    
    <!-- Item row 2 -->
    <rect x="15" y="98" width="180" height="40" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="116" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Phí giao hàng tận nơi</text>
    <text x="25" y="131" font-family="JetBrains Mono, monospace" font-size="11" fill="#2563eb">+ 20.000 VNĐ</text>
    
    <!-- Item row 3 -->
    <rect x="15" y="146" width="180" height="40" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="164" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Mã giảm giá Voucher</text>
    <text x="25" y="179" font-family="JetBrains Mono, monospace" font-size="11" fill="#16a34a">- 15.000 VNĐ</text>
  </g>
  
  <!-- Arrow 1 -->
  <path d="M 255 140 L 285 140" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow)"/>

  <!-- TIER 2: THỰC THI TOÁN TỬ SỐ HỌC & GÁN -->
  <g transform="translate(295, 35)">
    <rect width="220" height="210" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5" rx="10"/>
    <rect width="220" height="36" fill="#dbeafe" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#1e40af">2. Xử lý phép tính &amp; Gán dữ liệu</text>

    <!-- Calculation Step 1 -->
    <rect x="15" y="50" width="190" height="42" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="67" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">Tính tiền hàng (Phép nhân *):</text>
    <text x="25" y="83" font-family="JetBrains Mono, monospace" font-size="11" fill="#1d4ed8">subtotal = 45000 * 3</text>

    <!-- Calculation Step 2 -->
    <rect x="15" y="98" width="190" height="42" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="115" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">Tính tổng thanh toán (+ và -):</text>
    <text x="25" y="131" font-family="JetBrains Mono, monospace" font-size="11" fill="#1d4ed8">total = subtotal + 20000 - 15000</text>

    <!-- Calculation Step 3 -->
    <rect x="15" y="146" width="190" height="42" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="163" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">Cộng điểm thưởng (Gán +=):</text>
    <text x="25" y="179" font-family="JetBrains Mono, monospace" font-size="11" fill="#1d4ed8">user_points += 50</text>
  </g>

  <!-- Arrow 2 -->
  <path d="M 525 140 L 555 140" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- TIER 3: KẾT QUẢ GIAO DỊCH THÀNH CÔNG -->
  <g transform="translate(565, 35)">
    <rect width="200" height="210" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" rx="10"/>
    <rect width="200" height="36" fill="#dcfce7" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#166534">3. Kết quả giao dịch</text>

    <rect x="15" y="52" width="170" height="65" fill="#ffffff" stroke="#bbf7d0" rx="8"/>
    <text x="25" y="73" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#15803d">TỔNG TIỀN PHẢI TRẢ</text>
    <text x="25" y="98" font-family="JetBrains Mono, monospace" font-size="15" font-weight="bold" fill="#15803d">140.000 VNĐ</text>

    <rect x="15" y="127" width="170" height="65" fill="#ffffff" stroke="#bbf7d0" rx="8"/>
    <text x="25" y="148" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#15803d">ĐIỂM THƯỞNG TÍCH LŨY</text>
    <text x="25" y="173" font-family="JetBrains Mono, monospace" font-size="15" font-weight="bold" fill="#15803d">+ 50 điểm</text>
  </g>

  <!-- Defs Marker -->
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
  </defs>
</svg>"""
    svg_file.write_text(svg_content, encoding="utf-8")

    session_id = "Session 04"
    lesson_id = "Lesson 01"
    lesson_title = "Toán tử số học và toán tử gán"
    tech_stack = "python"

    # Section 1: Real-World Problem Statement
    sec1_html = """
<p class="text-slate-600 mb-4 leading-relaxed">
Hãy hình dung bạn đang xây dựng mô hình tính toán tài chính cho ứng dụng đặt đồ ăn trực tuyến <strong>ShopeeFood</strong>. Khi một khách hàng thêm 3 phần cơm tấm có giá 45.000 VNĐ vào giỏ hàng, hệ thống phần mềm phải thực hiện chính xác phép nhân giá tiền với số lượng, cộng thêm 20.000 VNĐ phí giao hàng, khấu trừ 15.000 VNĐ từ mã giảm giá voucher, và cuối cùng tính toán số điểm thưởng tích lũy cộng dồn vào tài khoản người dùng.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Tất cả các phép tính toán giá trị tài chính, cập nhật số dư ví điện tử hay tính tiền lẻ hoàn lại cho khách hàng đều dựa trên nền tảng của <strong>Toán tử số học (Arithmetic Operators)</strong> và <strong>Toán tử gán (Assignment Operators)</strong>.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Nếu thiếu đi các toán tử này, máy tính sẽ không thể thực hiện xử lý dữ liệu số hay cập nhật trạng thái bộ nhớ RAM, khiến toàn bộ quy trình thanh toán tự động bị ngưng trệ.
</p>
"""

    # Section 2: Syntax Breakdown & Visualizer
    sec2_html = """
<h3 id="sec-2-1-toan-tu-so-hoc-co-ban" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.1. Cú pháp và giải thích Toán tử số học (Arithmetic Operators)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Toán tử số học được sử dụng để thực hiện các phép tính toán đại số cơ bản và nâng cao giữa các biến hoặc giá trị số trong lập trình Python.
</p>

<!-- 1. CÚ PHÁP CHUẨN (Syntax Card) -->
<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">Cú pháp định nghĩa phép tính số học trong Python</span>
    </span>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs language-python">result = operand_a operator operand_b</code></pre>
</div>

<!-- 2. GIẢI THÍCH CÚ PHÁP (Component Explanation List) -->
<div class="space-y-2 text-slate-700 my-4 pl-2">
  <p class="font-semibold text-slate-900 mb-2">Chi tiết thành phần cú pháp:</p>
  <ul class="list-disc pl-6 space-y-2 text-slate-600">
    <li><strong class="text-slate-900"><code>operand_a</code>, <code>operand_b</code></strong>: Các toán hạng tham gia tính toán (số nguyên <code>int</code> hoặc số thực <code>float</code>).</li>
    <li><strong class="text-slate-900"><code>operator</code> (Toán tử số học)</strong>: Các ký hiệu toán học bao gồm:
      <code class="text-rikkei-red font-mono">+</code> (Cộng), 
      <code class="text-rikkei-red font-mono">-</code> (Trừ), 
      <code class="text-rikkei-red font-mono">*</code> (Nhân), 
      <code class="text-rikkei-red font-mono">/</code> (Chia số thực), 
      <code class="text-rikkei-red font-mono">//</code> (Chia lấy phần nguyên), 
      <code class="text-rikkei-red font-mono">%</code> (Chia lấy phần dư), 
      <code class="text-rikkei-red font-mono">**</code> (Lũy thừa).
    </li>
    <li><strong class="text-slate-900"><code>result</code></strong>: Biến chứa kết quả thu được sau khi thực hiện phép tính.</li>
  </ul>
</div>

<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
  <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-push-pin text-sky-600"></i> Yêu cầu bài toán thực hành:</div>
  <p class="text-sm text-slate-700">Tính tổng tiền 3 phần ăn giá 45,000 VNĐ, cộng 20,000 VNĐ phí ship và trừ 15,000 VNĐ voucher giảm giá.</p>
</div>

<!-- 3. VÍ DỤ MINH HỌA MÃ NGUỒN CHẠY TRỰC TIẾP (Live Code Sandbox) -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-2-1', 'output-sb-2-1', 'container-sb-2-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc">
        <i class="ph-bold ph-arrow-counter-clockwise text-xs"></i>
      </button>
      <button onclick="runPythonCode('code-sb-2-1', 'output-sb-2-1', 'container-sb-2-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình">
        <i class="ph-bold ph-play text-xs"></i>
      </button>
      <button onclick="copySandboxCode('code-sb-2-1', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép">
        <i class="ph-bold ph-copy text-xs"></i>
      </button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-2-1" class="language-python" contenteditable="true" spellcheck="false" data-original="# 1. Tính tổng giá trị đơn hàng ShopeeFood
unit_price = 45000
quantity = 3
shipping_fee = 20000
discount_voucher = 15000

# 2. Phép tính nhân, cộng, trừ kết hợp
subtotal = unit_price * quantity
total_payment = subtotal + shipping_fee - discount_voucher

print('Tiền hàng:', subtotal, 'VNĐ')
print('Tổng thanh toán:', total_payment, 'VNĐ')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># 1. Tính tổng giá trị đơn hàng ShopeeFood
unit_price = 45000
quantity = 3
shipping_fee = 20000
discount_voucher = 15000

# 2. Phép tính nhân, cộng, trừ kết hợp
subtotal = unit_price * quantity
total_payment = subtotal + shipping_fee - discount_voucher

print('Tiền hàng:', subtotal, 'VNĐ')
print('Tổng thanh toán:', total_payment, 'VNĐ')</code></pre>
  </div>
  <div id="container-sb-2-1" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5">
        <i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):
      </span>
    </div>
    <pre id="output-sb-2-1" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>

<h3 id="sec-2-2-toan-tu-gan-phuc-hop" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.2. Cú pháp và giải thích Toán tử gán phức hợp (Compound Assignment Operators)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Toán tử gán phức hợp kết hợp phép tính số học với phép gán giá trị, giúp viết mã ngắn gọn và cập nhật biến bộ nhớ nhanh chóng (như <code>x += 5</code> tương đương với <code>x = x + 5</code>).
</p>

<!-- 1. CÚ PHÁP CHUẨN (Syntax Card) -->
<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">Cú pháp toán tử gán phức hợp trong Python</span>
    </span>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs language-python">variable += value   # Tương đương: variable = variable + value
variable -= value   # Tương đương: variable = variable - value
variable *= value   # Tương đương: variable = variable * value
variable /= value   # Tương đương: variable = variable / value</code></pre>
</div>

<!-- 2. GIẢI THÍCH CÚ PHÁP (Component Explanation List) -->
<div class="space-y-2 text-slate-700 my-4 pl-2">
  <p class="font-semibold text-slate-900 mb-2">Chi tiết thành phần cú pháp:</p>
  <ul class="list-disc pl-6 space-y-2 text-slate-600">
    <li><strong class="text-slate-900"><code>variable</code></strong>: Biến số đã được khởi tạo trước đó trong bộ nhớ RAM.</li>
    <li><strong class="text-slate-900"><code>+=</code> (Cộng dồn)</strong>: Thêm giá trị <code>value</code> vào biến hiện tại.</li>
    <li><strong class="text-slate-900"><code>-=</code> (Trừ dồn)</strong>: Khấu trừ giá trị <code>value</code> khỏi biến hiện tại.</li>
    <li><strong class="text-slate-900"><code>*=</code> (Nhân dồn)</strong>: Nhân biến hiện tại với giá trị <code>value</code>.</li>
  </ul>
</div>

<!-- 3. VÍ DỤ MINH HỌA MÃ NGUỒN CHẠY TRỰC TIẾP (Live Code Sandbox) -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-2-2', 'output-sb-2-2', 'container-sb-2-2')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc">
        <i class="ph-bold ph-arrow-counter-clockwise text-xs"></i>
      </button>
      <button onclick="runPythonCode('code-sb-2-2', 'output-sb-2-2', 'container-sb-2-2')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình">
        <i class="ph-bold ph-play text-xs"></i>
      </button>
      <button onclick="copySandboxCode('code-sb-2-2', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép">
        <i class="ph-bold ph-copy text-xs"></i>
      </button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-2-2" class="language-python" contenteditable="true" spellcheck="false" data-original="# Khởi tạo điểm thưởng tài khoản ShopeeFood
reward_points = 120
wallet_balance = 500000

# Tích lũy 50 điểm từ đơn hàng vừa hoàn thành
reward_points += 50

# Trừ 140.000 VNĐ tiền đơn hàng vào số dư ví
wallet_balance -= 140000

print('Điểm thưởng mới:', reward_points)
print('Số dư ví còn lại:', wallet_balance, 'VNĐ')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># Khởi tạo điểm thưởng tài khoản ShopeeFood
reward_points = 120
wallet_balance = 500000

# Tích lũy 50 điểm từ đơn hàng vừa hoàn thành
reward_points += 50

# Trừ 140.000 VNĐ tiền đơn hàng vào số dư ví
wallet_balance -= 140000

print('Điểm thưởng mới:', reward_points)
print('Số dư ví còn lại:', wallet_balance, 'VNĐ')</code></pre>
  </div>
  <div id="container-sb-2-2" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5">
        <i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):
      </span>
    </div>
    <pre id="output-sb-2-2" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>

<h3 id="sec-2-3-thu-tu-uu-tien-toan-tu-so-hoc-pemdas" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.3. Quy tắc thứ tự ưu tiên toán tử số học (PEMDAS)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Trong một biểu thức chứa nhiều toán tử số học phức tạp, Python tuân thủ quy tắc ưu tiên tiêu chuẩn <strong>PEMDAS</strong>:
</p>
<ul class="list-disc pl-6 space-y-2 text-slate-600 my-4">
  <li><strong class="text-slate-900">Parentheses <code>()</code></strong>: Phép tính trong ngoặc đơn được ưu tiên thực hiện trước nhất.</li>
  <li><strong class="text-slate-900">Exponents <code>**</code></strong>: Phép tính lũy thừa có độ ưu tiên cao tiếp theo.</li>
  <li><strong class="text-slate-900">Multiplication / Division <code>*</code>, <code>/</code>, <code>//</code>, <code>%</code></strong>: Các phép nhân, chia thực hiện từ trái sang phải.</li>
  <li><strong class="text-slate-900">Addition / Subtraction <code>+</code>, <code>-</code></strong>: Các phép cộng và trừ thực hiện cuối cùng từ trái sang phải.</li>
</ul>
"""

    # Section 3: Progressive Practical Examples
    sec3_html = """
<h3 id="sec-3-1-tinh-tong-chi-phi-don-hang-shopeefood" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Tính tổng chi phí đơn hàng ShopeeFood bao gồm phụ phí và giảm giá</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Ứng dụng ShopeeFood tính tổng tiền thanh toán cho đơn hàng gồm 2 ly trà sữa (30,000 VNĐ/ly), phí giao hàng 15,000 VNĐ và áp dụng voucher giảm 10% trên tổng tiền hàng.
</p>

<!-- Live Code Sandbox 3.1 -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-3-1', 'output-sb-3-1', 'container-sb-3-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc">
        <i class="ph-bold ph-arrow-counter-clockwise text-xs"></i>
      </button>
      <button onclick="runPythonCode('code-sb-3-1', 'output-sb-3-1', 'container-sb-3-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình">
        <i class="ph-bold ph-play text-xs"></i>
      </button>
      <button onclick="copySandboxCode('code-sb-3-1', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép">
        <i class="ph-bold ph-copy text-xs"></i>
      </button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-3-1" class="language-python" contenteditable="true" spellcheck="false" data-original="# Khai báo thông tin giá tiền
item_price = 30000
item_qty = 2
shipping_fee = 15000
discount_percent = 0.10

# Tính toán tiền hàng và chiết khấu
subtotal = item_price * item_qty
discount_amount = subtotal * discount_percent
final_amount = (subtotal - discount_amount) + shipping_fee

print('Tiền hàng gốc:', subtotal, 'VNĐ')
print('Số tiền giảm giá:', discount_amount, 'VNĐ')
print('Thành tiền thanh toán:', final_amount, 'VNĐ')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># Khai báo thông tin giá tiền
item_price = 30000
item_qty = 2
shipping_fee = 15000
discount_percent = 0.10

# Tính toán tiền hàng và chiết khấu
subtotal = item_price * item_qty
discount_amount = subtotal * discount_percent
final_amount = (subtotal - discount_amount) + shipping_fee

print('Tiền hàng gốc:', subtotal, 'VNĐ')
print('Số tiền giảm giá:', discount_amount, 'VNĐ')
print('Thành tiền thanh toán:', final_amount, 'VNĐ')</code></pre>
  </div>
  <div id="container-sb-3-1" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5">
        <i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):
      </span>
    </div>
    <pre id="output-sb-3-1" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>

<h3 id="sec-3-2-cap-nhat-tich-luy-diem-thuong-va-so-du-vi" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.2. Cập nhật tích lũy điểm thưởng và số dư ví bằng toán tử gán phức hợp</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Cập nhật biến trạng thái ví ShopeePay sau khi thanh toán đơn hàng thành công, trừ tiền đơn hàng và cộng điểm thưởng tích lũy tương ứng 5% giá trị đơn.
</p>

<!-- Live Code Sandbox 3.2 -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-3-2', 'output-sb-3-2', 'container-sb-3-2')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc">
        <i class="ph-bold ph-arrow-counter-clockwise text-xs"></i>
      </button>
      <button onclick="runPythonCode('code-sb-3-2', 'output-sb-3-2', 'container-sb-3-2')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình">
        <i class="ph-bold ph-play text-xs"></i>
      </button>
      <button onclick="copySandboxCode('code-sb-3-2', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép">
        <i class="ph-bold ph-copy text-xs"></i>
      </button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-3-2" class="language-python" contenteditable="true" spellcheck="false" data-original="# Số dư ví ban đầu và điểm thưởng
wallet_balance = 350000
user_points = 80
bill_total = 165000

# Trừ tiền hóa đơn khỏi ví
wallet_balance -= bill_total

# Tích lũy 5% hóa đơn thành điểm thưởng (lấy phần nguyên)
earned_points = int(bill_total * 0.05)
user_points += earned_points

print('Số dư ví sau thanh toán:', wallet_balance, 'VNĐ')
print('Điểm thưởng tích lũy mới:', user_points, 'điểm')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># Số dư ví ban đầu và điểm thưởng
wallet_balance = 350000
user_points = 80
bill_total = 165000

# Trừ tiền hóa đơn khỏi ví
wallet_balance -= bill_total

# Tích lũy 5% hóa đơn thành điểm thưởng (lấy phần nguyên)
earned_points = int(bill_total * 0.05)
user_points += earned_points

print('Số dư ví sau thanh toán:', wallet_balance, 'VNĐ')
print('Điểm thưởng tích lũy mới:', user_points, 'điểm')</code></pre>
  </div>
  <div id="container-sb-3-2" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5">
        <i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):
      </span>
    </div>
    <pre id="output-sb-3-2" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>

<h3 id="sec-3-3-chia-tien-hoa-don-nhom-va-tinh-tien-le-hoan-lai" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.3. Chia tiền hóa đơn nhóm và tính tiền lẻ hoàn lại dư</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Khi nhóm 4 người cùng nhau chia đều một hóa đơn ăn uống ShopeeFood trị giá 355,000 VNĐ, sử dụng phép chia lấy phần nguyên <code>//</code> để tính số tiền tròn mỗi người cần trả và phép chia lấy dư <code>%</code> để tính số tiền thừa dư ra.
</p>

<!-- Live Code Sandbox 3.3 -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-3-3', 'output-sb-3-3', 'container-sb-3-3')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc">
        <i class="ph-bold ph-arrow-counter-clockwise text-xs"></i>
      </button>
      <button onclick="runPythonCode('code-sb-3-3', 'output-sb-3-3', 'container-sb-3-3')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình">
        <i class="ph-bold ph-play text-xs"></i>
      </button>
      <button onclick="copySandboxCode('code-sb-3-3', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép">
        <i class="ph-bold ph-copy text-xs"></i>
      </button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-3-3" class="language-python" contenteditable="true" spellcheck="false" data-original="# Tổng tiền hóa đơn ăn nhóm và số người
group_bill = 355000
num_people = 4

# Phép chia lấy phần nguyên (Số tiền mỗi người đóng)
share_per_person = group_bill // num_people

# Phép chia lấy phần dư (Số tiền thừa dư ra)
remaining_change = group_bill % num_people

print('Mỗi người đóng:', share_per_person, 'VNĐ')
print('Tiền dư lẻ:', remaining_change, 'VNĐ')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># Tổng tiền hóa đơn ăn nhóm và số người
group_bill = 355000
num_people = 4

# Phép chia lấy phần nguyên (Số tiền mỗi người đóng)
share_per_person = group_bill // num_people

# Phép chia lấy phần dư (Số tiền thừa dư ra)
remaining_change = group_bill % num_people

print('Mỗi người đóng:', share_per_person, 'VNĐ')
print('Tiền dư lẻ:', remaining_change, 'VNĐ')</code></pre>
  </div>
  <div id="container-sb-3-3" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5">
        <i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):
      </span>
    </div>
    <pre id="output-sb-3-3" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>
"""

    # Section 4: Production Gotchas - Clean Terms (No AI buzzwords like 'bẫy', 'gotcha')
    sec4_html = """
<div class="space-y-4">
  <div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">
    <div class="font-bold text-rose-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-warning-circle text-rose-600"></i> Lỗi thường gặp 1: Lỗi chia cho số 0 (ZeroDivisionError)</div>
    <p class="text-sm text-slate-700">Trong lập trình, việc chia một số cho số 0 với toán tử <code>/</code> hoặc <code>//</code> sẽ ngay lập tức làm chương trình bị đứt luồng và báo ngoại lệ <code>ZeroDivisionError</code>. Bạn luôn cần kiểm tra giá trị mẫu số khác 0 trước khi thực hiện phép chia.</p>
  </div>

  <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">
    <div class="font-bold text-amber-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-amber-600"></i> Lỗi thường gặp 2: Lỗi sai số số thực (Floating-Point Precision Issues)</div>
    <p class="text-sm text-slate-700">Do cách máy tính lưu trữ số thực dưới dạng nhị phân, phép tính như <code>0.1 + 0.2</code> trong Python sẽ cho kết quả là <code>0.30000000000000004</code> thay vì <code>0.3</code> tròn trịa. Khi xử lý giao dịch tiền tệ ngân hàng, bạn nên sử dụng thư viện <code>decimal</code> thay vì số thực <code>float</code> mặc định.</p>
  </div>

  <div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
    <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-brackets-curly text-sky-600"></i> Lỗi thường gặp 3: Khác biệt giữa chia số thực (/) và chia lấy phần nguyên (//)</div>
    <p class="text-sm text-slate-700">Toán tử <code>/</code> luôn luôn trả về kiểu số thực <code>float</code> (ví dụ: <code>10 / 2</code> trả về <code>5.0</code>), trong khi toán tử <code>//</code> làm tròn xuống số nguyên nhỏ hơn gần nhất. Hãy chú ý chọn đúng loại toán tử phù hợp với yêu cầu bài toán.</p>
  </div>
</div>
"""

    json_payload = {
        "tech_stack": tech_stack,
        "lesson_title": f"{lesson_id} - {lesson_title}",
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

    metadata = {
        "session_id": session_id,
        "lesson_id": lesson_id,
        "lesson_title": lesson_title,
        "tech_stack": tech_stack
    }

    print(f"🚀 Compiling Jinja2 Master Reading Material for {session_id} - {lesson_id}...")
    compiled_html = assemble_reading_html(json_payload, metadata)

    out_file.write_text(compiled_html, encoding="utf-8")
    print(f"📄 Rendered HTML length: {len(compiled_html)} bytes")

    is_valid, errors = validate_reading_material(compiled_html)
    if is_valid:
        print("✅ Validation PASS! 100% structural, light-mode, and DOM standards satisfied.")
    else:
        print(f"⚠️ Validation Warnings/Errors ({len(errors)}):")
        for err in errors:
            print(f"   - {err}")

    print(f"🎉 Successfully saved reading.html to:\n   {out_file}")

if __name__ == "__main__":
    generate_lesson_01()
