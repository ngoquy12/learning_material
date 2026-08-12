# scratch/generate_session_04_lesson_03_04.py
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

def generate_lesson_03():
    target_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 03 - Cấu trúc rẽ nhánh điều khiển với if, elif và else"
    rd_dir = target_dir / "Bài đọc"
    img_dir = rd_dir / "images"
    rq_dir = target_dir / "Câu hỏi bài đọc"
    qz_dir = target_dir / "Câu hỏi Quizz"
    
    rd_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)
    rq_dir.mkdir(parents=True, exist_ok=True)
    qz_dir.mkdir(parents=True, exist_ok=True)

    # 1. SVG Illustration
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%" height="100%">
  <rect width="800" height="280" fill="#f8fafc" rx="16"/>
  <rect x="16" y="16" width="768" height="248" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" rx="12"/>
  
  <!-- TIER 1: GIÁ TRỊ ĐƠN HÀNG ĐẦU VÀO -->
  <g transform="translate(35, 35)">
    <rect width="210" height="210" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" rx="10"/>
    <rect width="210" height="36" fill="#e2e8f0" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">1. Đầu vào đơn hàng</text>
    
    <rect x="15" y="50" width="180" height="40" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="68" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Tổng tiền đơn hàng</text>
    <text x="25" y="83" font-family="JetBrains Mono, monospace" font-size="11" fill="#be111c">order_amount = 1.500.000</text>
    
    <rect x="15" y="98" width="180" height="40" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="116" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Mã giảm giá Voucher</text>
    <text x="25" y="131" font-family="JetBrains Mono, monospace" font-size="11" fill="#2563eb">voucher_code = 'SUMMER'</text>
  </g>
  
  <!-- Arrow 1 -->
  <path d="M 255 140 L 285 140" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow)"/>

  <!-- TIER 2: CHUỖI ĐIỀU KIỆN RẼ NHÁNH IF-ELIF-ELSE -->
  <g transform="translate(295, 35)">
    <rect width="220" height="210" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5" rx="10"/>
    <rect width="220" height="36" fill="#dbeafe" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#1e40af">2. Chuỗi rẽ nhánh if-elif-else</text>

    <!-- Branch 1 -->
    <rect x="15" y="50" width="190" height="42" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="67" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">if order_amount &gt;= 2.000.000:</text>
    <text x="25" y="83" font-family="JetBrains Mono, monospace" font-size="11" fill="#dc2626">False (Bỏ qua nhánh 1)</text>

    <!-- Branch 2 -->
    <rect x="15" y="98" width="190" height="42" fill="#ffffff" stroke="#bbf7d0" stroke-width="2" rx="6"/>
    <text x="25" y="115" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#166534">elif order_amount &gt;= 1.000.000:</text>
    <text x="25" y="131" font-family="JetBrains Mono, monospace" font-size="11" fill="#16a34a">True ➔ Khớp giảm 10%</text>

    <!-- Branch 3 -->
    <rect x="15" y="146" width="190" height="42" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="163" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">else (Các trường hợp còn lại):</text>
    <text x="25" y="179" font-family="JetBrains Mono, monospace" font-size="11" fill="#64748b">Không thực thi</text>
  </g>

  <!-- Arrow 2 -->
  <path d="M 525 140 L 555 140" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- TIER 3: KẾT QUẢ ÁP DỤNG MỨC GIẢM GIÁ -->
  <g transform="translate(565, 35)">
    <rect width="200" height="210" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" rx="10"/>
    <rect width="200" height="36" fill="#dcfce7" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#166534">3. Kết quả chiết khấu</text>

    <rect x="15" y="52" width="170" height="65" fill="#ffffff" stroke="#bbf7d0" rx="8"/>
    <text x="25" y="73" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#15803d">TỶ LỆ GIẢM GIÁ</text>
    <text x="25" y="98" font-family="JetBrains Mono, monospace" font-size="15" font-weight="bold" fill="#15803d">Giảm 10% (150k)</text>

    <rect x="15" y="127" width="170" height="65" fill="#ffffff" stroke="#bbf7d0" rx="8"/>
    <text x="25" y="148" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#15803d">TỔNG THANH TOÁN SAU GIẢM</text>
    <text x="25" y="173" font-family="JetBrains Mono, monospace" font-size="15" font-weight="bold" fill="#15803d">1.350.000 VNĐ</text>
  </g>

  <!-- Defs Marker -->
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
  </defs>
</svg>"""
    (img_dir / "illustration_lesson_03.svg").write_text(svg_content, encoding="utf-8")

    # 2. Reading HTML JSON payload
    sec1_html = """
<p class="text-slate-600 mb-4 leading-relaxed">
Trong thực tế phát triển hệ thống ShopeeFood, phần mềm phải tự động đưa ra các quyết định rẽ nhánh dựa trên dữ liệu giá trị đơn hàng. Ví dụ: Nếu đơn hàng từ 2.000.000 VNĐ trở lên sẽ được giảm 20%; Nếu đơn từ 1.000.000 VNĐ đến dưới 2.000.000 VNĐ giảm 10%; Nếu từ 500.000 VNĐ giảm 5%; Các đơn nhỏ hơn không áp dụng chiết khấu.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Nếu chỉ sử dụng phép tính số học đơn thuần, chương trình sẽ không thể tự động rẽ nhánh luồng thực thi theo các điều kiện kinh doanh khác nhau. Cấu trúc rẽ nhánh <strong>if, elif, else</strong> là công cụ nền tảng giúp lập trình viên điều khiển luồng chương trình một cách linh hoạt.
</p>
"""

    sec2_html = """
<h3 id="sec-2-1-cau-lenh-if-va-if-else" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.1. Cú pháp và cơ chế hoạt động của câu lệnh rẽ nhánh đơn if và if-else</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Câu lệnh <code>if</code> kiểm tra một biểu thức điều kiện Boolean. Nếu điều kiện trả về <code>True</code>, khối lệnh bên trong sẽ được thực thi. Nếu đi kèm <code>else</code>, khối lệnh <code>else</code> sẽ được thực thi khi điều kiện trả về <code>False</code>.
</p>

<!-- Syntax Card -->
<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">Cú pháp câu lệnh rẽ nhánh if - else</span>
    </span>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs language-python">if condition:
    # Khối lệnh thực thi khi condition là True
else:
    # Khối lệnh thực thi khi condition là False</code></pre>
</div>

<!-- Component Breakdown List -->
<div class="space-y-2 text-slate-700 my-4 pl-2">
  <p class="font-semibold text-slate-900 mb-2">Chi tiết thành phần cú pháp:</p>
  <ul class="list-disc pl-6 space-y-2 text-slate-600">
    <li><strong class="text-slate-900"><code>condition</code></strong>: Biểu thức logic trả về giá trị kiểu Boolean (<code>True</code> hoặc <code>False</code>).</li>
    <li><strong class="text-slate-900">Dấu hai chấm <code>:</code></strong>: Bắt đầu một khối lệnh rẽ nhánh mới.</li>
    <li><strong class="text-slate-900">Thụt lùi dòng (Indentation)</strong>: Các câu lệnh thuộc nhánh phải thụt lùi vào đúng 4 khoảng trắng.</li>
  </ul>
</div>

<!-- Live Code Sandbox -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-2-1', 'output-sb-2-1', 'container-sb-2-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc"><i class="ph-bold ph-arrow-counter-clockwise text-xs"></i></button>
      <button onclick="runPythonCode('code-sb-2-1', 'output-sb-2-1', 'container-sb-2-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình"><i class="ph-bold ph-play text-xs"></i></button>
      <button onclick="copySandboxCode('code-sb-2-1', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép"><i class="ph-bold ph-copy text-xs"></i></button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-2-1" class="language-python" contenteditable="true" spellcheck="false" data-original="order_amount = 250000

if order_amount >= 200000:
    shipping_fee = 0
    print('Đơn hàng đạt ngưỡng 200k ➔ Miễn phí giao hàng (0 VNĐ)')
else:
    shipping_fee = 20000
    print('Đơn hàng chưa đủ điều kiện ➔ Phí giao hàng:', shipping_fee, 'VNĐ')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;">order_amount = 250000

if order_amount >= 200000:
    shipping_fee = 0
    print('Đơn hàng đạt ngưỡng 200k ➔ Miễn phí giao hàng (0 VNĐ)')
else:
    shipping_fee = 20000
    print('Đơn hàng chưa đủ điều kiện ➔ Phí giao hàng:', shipping_fee, 'VNĐ')</code></pre>
  </div>
  <div id="container-sb-2-1" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5"><i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</span>
    </div>
    <pre id="output-sb-2-1" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>

<h3 id="sec-2-2-cau-truc-da-nhanh-if-elif-else" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.2. Cú pháp và cơ chế hoạt động của cấu trúc đa nhánh if-elif-else</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Khi bài toán kinh doanh có nhiều hơn 2 lựa chọn, cấu trúc <code>if-elif-else</code> cho phép kiểm tra tuần tự từng điều kiện từ trên xuống dưới. Ngay khi có một nhánh điều kiện <code>True</code>, Python sẽ thực thi khối lệnh tương ứng và bỏ qua toàn bộ các nhánh còn lại.
</p>

<!-- Syntax Card -->
<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">Cú pháp cấu trúc đa nhánh if - elif - else</span>
    </span>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs language-python">if condition_1:
    # Khối 1
elif condition_2:
    # Khối 2
else:
    # Khối mặc định khi tất cả các điều kiện trên đều False</code></pre>
</div>

<!-- Live Code Sandbox -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-2-2', 'output-sb-2-2', 'container-sb-2-2')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc"><i class="ph-bold ph-arrow-counter-clockwise text-xs"></i></button>
      <button onclick="runPythonCode('code-sb-2-2', 'output-sb-2-2', 'container-sb-2-2')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình"><i class="ph-bold ph-play text-xs"></i></button>
      <button onclick="copySandboxCode('code-sb-2-2', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép"><i class="ph-bold ph-copy text-xs"></i></button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-2-2" class="language-python" contenteditable="true" spellcheck="false" data-original="order_amount = 1500000

if order_amount >= 2000000:
    discount_rate = 0.20
elif order_amount >= 1000000:
    discount_rate = 0.10
elif order_amount >= 500000:
    discount_rate = 0.05
else:
    discount_rate = 0.0

discount_val = order_amount * discount_rate
print('Tỷ lệ giảm giá:', int(discount_rate * 100), '%')
print('Số tiền giảm:', discount_val, 'VNĐ')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;">order_amount = 1500000

if order_amount >= 2000000:
    discount_rate = 0.20
elif order_amount >= 1000000:
    discount_rate = 0.10
elif order_amount >= 500000:
    discount_rate = 0.05
else:
    discount_rate = 0.0

discount_val = order_amount * discount_rate
print('Tỷ lệ giảm giá:', int(discount_rate * 100), '%')
print('Số tiền giảm:', discount_val, 'VNĐ')</code></pre>
  </div>
  <div id="container-sb-2-2" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5"><i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</span>
    </div>
    <pre id="output-sb-2-2" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>
"""

    sec3_html = """
<h3 id="sec-3-1-phan-hang-chiet-khau-shopeefood" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Phân hạng chiết khấu đơn hàng ShopeeFood</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Xác định mức chiết khấu voucher áp dụng cho đơn hàng 1,500,000 VNĐ thông qua chuỗi câu lệnh <code>if-elif-else</code>.
</p>

<!-- Live Sandbox 3.1 -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-3-1', 'output-sb-3-1', 'container-sb-3-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc"><i class="ph-bold ph-arrow-counter-clockwise text-xs"></i></button>
      <button onclick="runPythonCode('code-sb-3-1', 'output-sb-3-1', 'container-sb-3-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình"><i class="ph-bold ph-play text-xs"></i></button>
      <button onclick="copySandboxCode('code-sb-3-1', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép"><i class="ph-bold ph-copy text-xs"></i></button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-3-1" class="language-python" contenteditable="true" spellcheck="false" data-original="order_amount = 1500000

if order_amount >= 2000000:
    voucher = 'GIAM20'
elif order_amount >= 1000000:
    voucher = 'GIAM10'
else:
    voucher = 'KHONG'

print('Mã giảm giá áp dụng:', voucher)" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;">order_amount = 1500000

if order_amount >= 2000000:
    voucher = 'GIAM20'
elif order_amount >= 1000000:
    voucher = 'GIAM10'
else:
    voucher = 'KHONG'

print('Mã giảm giá áp dụng:', voucher)</code></pre>
  </div>
  <div id="container-sb-3-1" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5"><i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</span>
    </div>
    <pre id="output-sb-3-1" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>
"""

    sec4_html = """
<div class="space-y-4">
  <div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">
    <div class="font-bold text-rose-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-warning-circle text-rose-600"></i> Lỗi thường gặp 1: Quên dấu hai chấm (:) gây SyntaxError</div>
    <p class="text-sm text-slate-700">Mỗi dòng khai báo <code>if</code>, <code>elif</code>, hoặc <code>else</code> bắt buộc phải kết thúc bằng dấu hai chấm <code>:</code>. Thiếu dấu này sẽ khiến trình biên dịch báo lỗi <code>SyntaxError</code> ngay lập tức.</p>
  </div>
  <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">
    <div class="font-bold text-amber-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-amber-600"></i> Lỗi thường gặp 2: Thụt lùi dòng không thống nhất (IndentationError)</div>
    <p class="text-sm text-slate-700">Các dòng lệnh bên trong một khối rẽ nhánh phải thụt lùi thẳng hàng (chuẩn 4 khoảng trắng). Trộn lẫn giữa phím Tab và dấu cách sẽ gây lỗi <code>IndentationError</code>.</p>
  </div>
  <div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
    <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-brackets-curly text-sky-600"></i> Lỗi thường gặp 3: Sai thứ tự điều kiện trong chuỗi if-elif</div>
    <p class="text-sm text-slate-700">Nếu đặt điều kiện nhỏ hơn lên trước (ví dụ <code>>= 500k</code> đặt trước <code>>= 2 triệu</code>), đơn hàng 2.500.000 VNĐ sẽ bị khớp ngay ở nhánh đầu và không bao giờ xuống tới nhánh 2 triệu.</p>
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

    metadata = {
        "session_id": "Session 04",
        "lesson_id": "Lesson 03",
        "lesson_title": "Cấu trúc rẽ nhánh điều khiển với if, elif và else",
        "tech_stack": "python"
    }

    compiled_html = assemble_reading_html(json_payload, metadata)
    (rd_dir / "reading.html").write_text(compiled_html, encoding="utf-8")
    print("✅ Lesson 03 reading.html generated successfully!")

    # 3. Lesson 03 reading_questions.md
    rq_content = """# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn phân hạng giảm giá đơn hàng ShopeeFood:

```python
order_amount = 1500000

if order_amount >= 2000000:
    discount_rate = 0.20
elif order_amount >= 1000000:
    discount_rate = 0.10
elif order_amount >= 500000:
    discount_rate = 0.05
else:
    discount_rate = 0.0

final_payment = order_amount * (1 - discount_rate)
```

---

### Câu 1: Với giá trị đơn hàng đầu vào `order_amount = 1500000`, hãy giải thích tuần tự từng bước kiểm tra điều kiện của chuỗi `if-elif-else` và xác định giá trị cuối cùng của biến `discount_rate`.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Điều kiện `order_amount >= 2000000` (1.500.000 >= 2.000.000) trả về `False` ➔ Chuyển sang nhánh `elif` tiếp theo.
> - Bước 2: Điều kiện `order_amount >= 1000000` (1.500.000 >= 1.000.000) trả về `True` ➔ Thực thi gán `discount_rate = 0.10` (10%).
> - Python lập tức thoát khỏi toàn bộ cấu trúc rẽ nhánh, bỏ qua nhánh `elif >= 500000` và nhánh `else`.

---

### Câu 2: Nếu sửa giá trị biến đầu vào thành `order_amount = 400000`, nhánh điều khiển nào sẽ được kích hoạt và số tiền thanh toán cuối cùng `final_payment` nhận kết quả là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Các điều kiện `>= 2000000`, `>= 1000000`, `>= 500000` đều trả về `False`.
> - Nhánh mặc định `else` được kích hoạt, gán `discount_rate = 0.0` (0%).
> - Giá trị `final_payment = 400000 * (1 - 0) = 400.000 VNĐ`.

---

### Câu 3: Hãy phân tích vì sao việc đặt sai thứ tự điều kiện (ví dụ đưa nhánh `elif order_amount >= 500000:` lên trước nhánh `elif order_amount >= 2000000:`) sẽ gây ra sai sót logic nghiêm trọng cho hệ thống ShopeeFood.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Khi đơn hàng đạt 2.500.000 VNĐ, do điều kiện `>= 500000` đứng trước trả về `True` ngay lập tức, Python sẽ thực thi gán `discount_rate = 0.05` (5%) và thoát nhánh.
> - Khách hàng bị mất quyền lợi giảm 20% vì nhánh `>= 2000000` đứng phía sau không bao giờ được chạm tới.
"""
    (rq_dir / "reading_questions.md").write_text(rq_content, encoding="utf-8")

    # 4. Lesson 03 quiz.json
    quiz_data = [
        {
            "question": "Hệ thống ShopeeFood cần kiểm tra đơn hàng có đạt giá trị tối thiểu 200.000 VNĐ để áp dụng Freeship hay không. Cú pháp rẽ nhánh Python nào dưới đây là chuẩn xác?",
            "options": [
                "if order_amount >= 200000:\n    freeship = True",
                "if order_amount >= 200000\n    freeship = True",
                "if (order_amount >= 200000)\n    freeship = True",
                "if order_amount >= 200000 then:\n    freeship = True"
            ],
            "correct_option_index": 0,
            "explanation": "Trong Python, câu lệnh `if` bắt buộc kết thúc bằng dấu hai chấm `:` và khối lệnh bên trong phải thụt lùi dòng."
        },
        {
            "question": "Cho đoạn mã phân hạng chiết khấu đơn hàng ShopeeFood như sau:\n\n```python\namount = 1200000\nif amount >= 2000000:\n    rate = 0.20\nelif amount >= 1000000:\n    rate = 0.10\nelse:\n    rate = 0.0\n```\n\nGiá trị của biến `rate` sau khi hoàn tất đoạn mã trên là bao nhiêu?",
            "options": [
                "0.20",
                "0.10",
                "0.0",
                "0.15"
            ],
            "correct_option_index": 1,
            "explanation": "Biến `amount = 1200000` không thỏa mãn `1200000 >= 2000000` (False), nhưng thỏa mãn `1200000 >= 1000000` (True) nên `rate` nhận giá trị `0.10`."
        },
        {
            "question": "Trong Python, cú pháp biểu thức rẽ nhánh rút gọn (Ternary Operator) nào dưới đây gán `fee = 0` nếu `amount >= 200000`, ngược lại `fee = 20000`?",
            "options": [
                "fee = 0 if amount >= 200000 else 20000",
                "fee = if amount >= 200000 then 0 else 20000",
                "fee = amount >= 200000 ? 0 : 20000",
                "fee = (amount >= 200000) ? 0 else 20000"
            ],
            "correct_option_index": 0,
            "explanation": "Cú pháp biểu thức điều kiện rút gọn chuẩn trong Python là `val_true if condition else val_false`."
        },
        {
            "question": "Lập trình viên viết chuỗi rẽ nhánh `if-elif-else` trong Python nhưng quên không thụt lùi dòng 4 khoảng trắng ở câu lệnh phía sau dấu hai chấm. Trình biên dịch sẽ trả về thông báo lỗi nào?",
            "options": [
                "SyntaxError: invalid syntax",
                "IndentationError: expected an indented block",
                "TypeError: unsupported operand types",
                "NameError: name is not defined"
            ],
            "correct_option_index": 1,
            "explanation": "Quên thụt lùi dòng sau câu lệnh rẽ nhánh sẽ gây ra lỗi `IndentationError: expected an indented block`."
        },
        {
            "question": "Phát biểu nào sau đây phản ánh đúng cơ chế hoạt động của chuỗi câu lệnh `if-elif-else` khi có nhiều nhánh điều kiện cùng trả về `True`?",
            "options": [
                "Python sẽ thực thi tất cả các nhánh có điều kiện True từ trên xuống dưới.",
                "Python sẽ chỉ thực thi duy nhất nhánh `elif` đầu tiên thỏa mãn True và bỏ qua tất cả các nhánh còn lại.",
                "Python sẽ chỉ thực thi nhánh cuối cùng thỏa mãn điều kiện True.",
                "Python sẽ báo lỗi xung đột điều kiện RuntimeErrors và dừng chương trình."
            ],
            "correct_option_index": 1,
            "explanation": "Chuỗi `if-elif-else` hoạt động theo cơ chế loại trừ: ngay khi gặp nhánh đầu tiên thỏa mãn `True`, Python thực thi khối lệnh đó và thoát khỏi toàn bộ chuỗi."
        }
    ]
    (qz_dir / "quiz.json").write_text(json.dumps(quiz_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Lesson 03 all resources generated successfully!")


def generate_lesson_04():
    target_dir = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 04 - Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8"
    rd_dir = target_dir / "Bài đọc"
    img_dir = rd_dir / "images"
    rq_dir = target_dir / "Câu hỏi bài đọc"
    qz_dir = target_dir / "Câu hỏi Quizz"
    
    rd_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)
    rq_dir.mkdir(parents=True, exist_ok=True)
    qz_dir.mkdir(parents=True, exist_ok=True)

    # 1. SVG Illustration
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%" height="100%">
  <rect width="800" height="280" fill="#f8fafc" rx="16"/>
  <rect x="16" y="16" width="768" height="248" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" rx="12"/>
  
  <!-- TIER 1: KIỂM TRA TÀI KHOẢN VÒNG NGOÀI -->
  <g transform="translate(35, 35)">
    <rect width="210" height="210" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" rx="10"/>
    <rect width="210" height="36" fill="#e2e8f0" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">1. Vòng ngoài (Outer IF)</text>
    
    <rect x="15" y="50" width="180" height="65" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="70" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Trạng thái đăng nhập</text>
    <text x="25" y="88" font-family="JetBrains Mono, monospace" font-size="11" fill="#be111c">is_logged_in == True</text>
    <text x="25" y="103" font-family="Inter, sans-serif" font-size="10" fill="#16a34a">➔ Hợp lệ, vào vòng trong</text>
  </g>
  
  <!-- Arrow 1 -->
  <path d="M 255 140 L 285 140" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow)"/>

  <!-- TIER 2: KIỂM TRA ĐƠN HÀNG VÒNG TRONG (NESTED IF) -->
  <g transform="translate(295, 35)">
    <rect width="220" height="210" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5" rx="10"/>
    <rect width="220" height="36" fill="#dbeafe" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#1e40af">2. Vòng trong (Nested IF)</text>

    <rect x="15" y="50" width="190" height="65" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="70" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">if order_amount &gt;= 500k:</text>
    <text x="25" y="88" font-family="JetBrains Mono, monospace" font-size="11" fill="#16a34a">True ➔ Đủ chuẩn áp mã</text>

    <rect x="15" y="125" width="190" height="65" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="145" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">Chuẩn hóa PEP 8:</text>
    <text x="25" y="163" font-family="JetBrains Mono, monospace" font-size="10" fill="#2563eb">Thụt lùi 8 spaces (2 level)</text>
  </g>

  <!-- Arrow 2 -->
  <path d="M 525 140 L 555 140" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- TIER 3: KẾT QUẢ XÁC THỰC HOÀN CHỈNH -->
  <g transform="translate(565, 35)">
    <rect width="200" height="210" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" rx="10"/>
    <rect width="200" height="36" fill="#dcfce7" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#166534">3. Quyết định duyệt đơn</text>

    <rect x="15" y="52" width="170" height="65" fill="#ffffff" stroke="#bbf7d0" rx="8"/>
    <text x="25" y="73" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#15803d">DUYỆT VOUCHER ĐẶC QUYỀN</text>
    <text x="25" y="98" font-family="JetBrains Mono, monospace" font-size="14" font-weight="bold" fill="#15803d">ÁP MÃ THÀNH CÔNG</text>

    <rect x="15" y="127" width="170" height="65" fill="#ffffff" stroke="#bbf7d0" rx="8"/>
    <text x="25" y="148" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#15803d">CHUẨN MÃ NGUỒN</text>
    <text x="25" y="173" font-family="JetBrains Mono, monospace" font-size="14" font-weight="bold" fill="#15803d">ĐẠT ĐIỂM PEP 8</text>
  </g>

  <!-- Defs Marker -->
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
  </defs>
</svg>"""
    (img_dir / "illustration_lesson_04.svg").write_text(svg_content, encoding="utf-8")

    # 2. Reading HTML JSON payload
    sec1_html = """
<p class="text-slate-600 mb-4 leading-relaxed">
Trong quy trình duyệt voucher đặc quyền tại ShopeeFood, hệ thống phải trải qua 2 cấp xác thực: Đầu tiên kiểm tra tài khoản người dùng đã đăng nhập và hoạt động bình thường hay chưa; Tiếp theo nếu tài khoản hợp lệ mới tiến hành kiểm tra giá trị đơn hàng có đạt từ 500.000 VNĐ trở lên để tặng voucher giảm giá 50.000 VNĐ.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Việc lồng ghép một câu lệnh <code>if</code> bên trong một câu lệnh <code>if</code> khác được gọi là <strong>Cấu trúc rẽ nhánh lồng nhau (Nested if)</strong>. Tuy nhiên, việc lồng quá sâu sẽ làm cho mã nguồn trở nên rối rắm. Do đó, kỹ sư phần mềm cần tuân thủ quy tắc <strong>Chuẩn hóa mã nguồn PEP 8</strong> để giữ cho mã nguồn sạch đẹp, dễ đọc và dễ bảo trì.
</p>
"""

    sec2_html = """
<h3 id="sec-2-1-cau-truc-re-nhanh-long-nhau" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.1. Cú pháp và cơ chế hoạt động của Cấu trúc rẽ nhánh lồng nhau (Nested if)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Một câu lệnh <code>if</code> có thể chứa một hoặc nhiều câu lệnh <code>if</code> khác bên trong khối lệnh của nó. Mức độ thụt lùi dòng sẽ tăng thêm 4 khoảng trắng cho mỗi cấp lồng nhau.
</p>

<!-- Syntax Card -->
<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">Cú pháp cấu trúc rẽ nhánh lồng nhau (Nested if)</span>
    </span>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs language-python">if outer_condition:
    # Khối lệnh cấp 1 (Thụt lùi 4 spaces)
    if inner_condition:
        # Khối lệnh cấp 2 (Thụt lùi 8 spaces)
        print("Cả 2 điều kiện đều True")</code></pre>
</div>

<!-- Live Code Sandbox -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-2-1', 'output-sb-2-1', 'container-sb-2-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc"><i class="ph-bold ph-arrow-counter-clockwise text-xs"></i></button>
      <button onclick="runPythonCode('code-sb-2-1', 'output-sb-2-1', 'container-sb-2-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình"><i class="ph-bold ph-play text-xs"></i></button>
      <button onclick="copySandboxCode('code-sb-2-1', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép"><i class="ph-bold ph-copy text-xs"></i></button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-2-1" class="language-python" contenteditable="true" spellcheck="false" data-original="is_user_active = True
order_amount = 600000

if is_user_active:
    print('Tài khoản hoạt động hợp lệ.')
    if order_amount >= 500000:
        print('Đơn hàng đủ điều kiện ➔ Tặng voucher đặc quyền 50.000 VNĐ!')
    else:
        print('Đơn hàng chưa đủ 500k ➔ Không áp dụng voucher.')
else:
    print('Tài khoản bị khóa hoặc chưa đăng nhập.')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;">is_user_active = True
order_amount = 600000

if is_user_active:
    print('Tài khoản hoạt động hợp lệ.')
    if order_amount >= 500000:
        print('Đơn hàng đủ điều kiện ➔ Tặng voucher đặc quyền 50.000 VNĐ!')
    else:
        print('Đơn hàng chưa đủ 500k ➔ Không áp dụng voucher.')
else:
    print('Tài khoản bị khóa hoặc chưa đăng nhập.')</code></pre>
  </div>
  <div id="container-sb-2-1" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5"><i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</span>
    </div>
    <pre id="output-sb-2-1" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>

<h3 id="sec-2-2-chuan-hoa-ma-nguon-pep8" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.2. Quy tắc chuẩn hóa mã nguồn Python theo tiêu chuẩn PEP 8</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
<strong>PEP 8</strong> là tài liệu hướng dẫn quy chuẩn viết mã chính thức cho ngôn ngữ Python. Tuân thủ PEP 8 giúp mã nguồn đồng nhất và chuyên nghiệp trong các dự án phần mềm doanh nghiệp:
</p>
<ul class="list-disc pl-6 space-y-2 text-slate-600 my-4">
  <li><strong class="text-slate-900">Thụt lùi dòng (Indentation)</strong>: Bắt buộc dùng 4 khoảng trắng (spaces) cho mỗi cấp độ lồng nhau. Không trộn lẫn phím Tab và phím Space.</li>
  <li><strong class="text-slate-900">Khoảng trắng xung quanh toán tử</strong>: Sử dụng đúng 1 khoảng trắng trước và sau các toán tử gán (<code>=</code>) và so sánh (<code>==</code>, <code>>=</code>).</li>
  <li><strong class="text-slate-900">Quy tắc đặt tên biến</strong>: Sử dụng kiểu <code>snake_case</code> chữ thường phân cách bằng dấu gạch dưới (ví dụ: <code>order_total_amount</code>).</li>
</ul>
"""

    sec3_html = """
<h3 id="sec-3-1-xac-thuc-giao-dich-duyet-voucher-pep8" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Tối ưu hóa xác thực duyệt voucher ShopeeFood chuẩn PEP 8</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Thay vì lồng ghép quá nhiều cấp <code>if</code>, sử dụng toán tử logic <code>and</code> để phẳng hóa cấu trúc mã nguồn theo đúng khuyến nghị của PEP 8.
</p>

<!-- Live Sandbox 3.1 -->
<div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50">
  <div class="relative bg-slate-50/50 text-slate-800 font-mono text-sm border-b border-slate-200">
    <div class="absolute top-2.5 right-2.5 flex items-center gap-1.5 z-10 bg-white/90 backdrop-blur px-2 py-1 rounded-md border border-slate-200 shadow-sm">
      <button onclick="clearSandbox('code-sb-3-1', 'output-sb-3-1', 'container-sb-3-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Khôi phục code gốc"><i class="ph-bold ph-arrow-counter-clockwise text-xs"></i></button>
      <button onclick="runPythonCode('code-sb-3-1', 'output-sb-3-1', 'container-sb-3-1')" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Chạy chương trình"><i class="ph-bold ph-play text-xs"></i></button>
      <button onclick="copySandboxCode('code-sb-3-1', this)" class="p-1 rounded hover:bg-slate-100 text-slate-400 hover:text-rikkei-red transition-all" title="Sao chép"><i class="ph-bold ph-copy text-xs"></i></button>
    </div>
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-3-1" class="language-python" contenteditable="true" spellcheck="false" data-original="is_user_active = True
order_amount = 600000

# Tối ưu phẳng hóa điều kiện theo chuẩn PEP 8
if is_user_active and order_amount >= 500000:
    print('Tài khoản hợp lệ & Đơn từ 500k ➔ Áp dụng voucher thành công!')
else:
    print('Không đủ điều kiện nhận voucher đặc quyền.')" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;">is_user_active = True
order_amount = 600000

# Tối ưu phẳng hóa điều kiện theo chuẩn PEP 8
if is_user_active and order_amount >= 500000:
    print('Tài khoản hợp lệ & Đơn từ 500k ➔ Áp dụng voucher thành công!')
else:
    print('Không đủ điều kiện nhận voucher đặc quyền.')</code></pre>
  </div>
  <div id="container-sb-3-1" class="hidden bg-slate-100/90 border-t border-slate-200 p-3.5">
    <div class="flex items-center justify-between text-xs text-slate-500 font-mono mb-1">
      <span class="text-slate-700 font-bold flex items-center gap-1.5"><i class="ph-bold ph-terminal text-rikkei-red"></i> KẾT QUẢ THỰC THI (CONSOLE OUTPUT):</span>
    </div>
    <pre id="output-sb-3-1" class="font-mono text-sm text-slate-800 bg-white p-2.5 rounded-lg border border-slate-200 select-text whitespace-pre-wrap m-0 shadow-inner"></pre>
  </div>
</div>
"""

    sec4_html = """
<div class="space-y-4">
  <div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">
    <div class="font-bold text-rose-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-warning-circle text-rose-600"></i> Lỗi thường gặp 1: Lồng ghép điều kiện quá sâu (Deep Nesting)</div>
    <p class="text-sm text-slate-700">Lồng quá 3 cấp <code>if</code> bên trong nhau sẽ tạo ra mã nguồn dạng kim tự tháp (Pyramid of Doom), khiến mã cực kỳ khó đọc và dễ bỏ sót trường hợp kiểm tra. Hãy gộp điều kiện bằng toán tử <code>and</code>.</p>
  </div>
  <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">
    <div class="font-bold text-amber-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-amber-600"></i> Lỗi thường gặp 2: Trộn lẫn phím Tab và phím Space</div>
    <p class="text-sm text-slate-700">Vi phạm quy tắc PEP 8 khi trộn lẫn phím Tab và 4 phím Space trong cùng một tập tin sẽ làm trình biên dịch Python 3 báo lỗi <code>TabError: inconsistent use of tabs and spaces in indentation</code>.</p>
  </div>
  <div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
    <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-brackets-curly text-sky-600"></i> Lỗi thường gặp 3: Đặt tên biến viết hoa sai quy chuẩn PEP 8</div>
    <p class="text-sm text-slate-700">Đặt tên biến bằng kiểu CamelCase (như <code>OrderAmount</code>) thay vì <code>snake_case</code> (như <code>order_amount</code>) vi phạm quy chuẩn PEP 8 dành cho biến số trong Python.</p>
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

    metadata = {
        "session_id": "Session 04",
        "lesson_id": "Lesson 04",
        "lesson_title": "Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8",
        "tech_stack": "python"
    }

    compiled_html = assemble_reading_html(json_payload, metadata)
    (rd_dir / "reading.html").write_text(compiled_html, encoding="utf-8")
    print("✅ Lesson 04 reading.html generated successfully!")

    # 3. Lesson 04 reading_questions.md
    rq_content = """# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn xác thực duyệt voucher ShopeeFood lồng nhau:

```python
is_user_active = True
order_amount = 600000

if is_user_active:
    if order_amount >= 500000:
        voucher_status = "Áp dụng thành công"
    else:
        voucher_status = "Chưa đủ giá trị đơn 500k"
else:
    voucher_status = "Tài khoản không hợp lệ"
```

---

### Câu 1: Khi biến đầu vào là `is_user_active = True` và `order_amount = 600000`, hãy giải thích luồng thực thi của từng cấp rẽ nhánh `if` lồng nhau và xác định giá trị biến `voucher_status`.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Vòng ngoài: Điều kiện `is_user_active` (True) thỏa mãn ➔ Hệ thống đi vào khối rẽ nhánh bên trong.
> - Vòng trong: Điều kiện `order_amount >= 500000` (600000 >= 500000) thỏa mãn ➔ Thực thi gán `voucher_status = 'Áp dụng thành công'`.

---

### Câu 2: Áp dụng nguyên tắc tối ưu hóa mã nguồn theo quy chuẩn PEP 8, hãy viết lại đoạn mã rẽ nhánh lồng nhau trên thành một câu lệnh `if-else` phẳng duy nhất sử dụng toán tử logic `and`.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Đoạn mã phẳng chuẩn PEP 8:
> ```python
> if is_user_active and order_amount >= 500000:
>     voucher_status = "Áp dụng thành công"
> else:
>     voucher_status = "Không đủ điều kiện"
> ```

---

### Câu 3: Hãy nêu 2 quy tắc thụt lùi dòng (Indentation) và khoảng trắng xung quanh toán tử theo chuẩn PEP 8 để tránh gây lỗi `IndentationError` và `TabError` khi lập trình Python.
> **Gợi ý trả lời & Định hướng đáp án:**
> 1. Thụt lùi dòng: Bắt buộc dùng đúng 4 khoảng trắng (spaces) cho mỗi cấp độ lồng nhau, không trộn lẫn phím Tab và phím Space.
> 2. Khoảng trắng: Đặt đúng 1 khoảng trắng trước và sau các toán tử gán (`=`) và so sánh (`>=`).
"""
    (rq_dir / "reading_questions.md").write_text(rq_content, encoding="utf-8")

    # 4. Lesson 04 quiz.json
    quiz_data = [
        {
            "question": "Theo quy chuẩn đặt tên biến dành cho Python trong tài liệu PEP 8, cách đặt tên biến nào dưới đây tuân thủ đúng định dạng `snake_case`?",
            "options": [
                "total_order_amount",
                "TotalOrderAmount",
                "totalOrderAmount",
                "TOTAL_ORDER_AMOUNT"
            ],
            "correct_option_index": 0,
            "explanation": "Quy chuẩn PEP 8 quy định tên biến trong Python phải viết bằng chữ cái thường và phân cách giữa các từ bằng dấu gạch dưới `snake_case`."
        },
        {
            "question": "Theo quy định của chuẩn PEP 8, độ dài thụt lùi dòng (Indentation) tiêu chuẩn cho mỗi cấp khối lệnh rẽ nhánh trong Python là bao nhiêu khoảng trắng?",
            "options": [
                "2 khoảng trắng (spaces)",
                "4 khoảng trắng (spaces)",
                "8 khoảng trắng (spaces)",
                "1 phím Tab tùy chỉnh"
            ],
            "correct_option_index": 1,
            "explanation": "PEP 8 quy định rõ ràng sử dụng đúng 4 khoảng trắng (spaces) cho mỗi cấp độ thụt lùi dòng trong Python."
        },
        {
            "question": "Cho đoạn mã rẽ nhánh lồng nhau trong ShopeeFood như sau:\n\n```python\nis_active = True\namount = 300000\nif is_active:\n    if amount >= 500000:\n        result = \"A\"\n    else:\n        result = \"B\"\nelse:\n    result = \"C\"\n```\n\nGiá trị của biến `result` thu được là bao nhiêu?",
            "options": [
                "A",
                "B",
                "C",
                "None"
            ],
            "correct_option_index": 1,
            "explanation": "`is_active = True` vào vòng trong. Tại vòng trong: `amount >= 500000` (300000 >= 500000) trả về False, do đó thực thi nhánh `else` bên trong và gán `result = 'B'`."
        },
        {
            "question": "Kỹ thuật nào dưới đây được khuyến nghị trong PEP 8 để xử lý hiện tượng lồng ghép quá nhiều cấp lệnh `if` (Pyramid of Doom)?",
            "options": [
                "Bỏ hẳn dấu hai chấm và câu lệnh rẽ nhánh trong chương trình.",
                "Kết hợp các điều kiện bằng toán tử logic `and` hoặc sử dụng Guard Clauses để phẳng hóa luồng mã nguồn.",
                "Tăng độ thụt lùi dòng từ 4 khoảng trắng lên 8 khoảng trắng cho mỗi cấp.",
                "Chuyển toàn bộ các biến điều kiện sang kiểu dữ liệu danh sách list."
            ],
            "correct_option_index": 1,
            "explanation": "Sử dụng toán tử logic `and` để gộp điều kiện giúp phẳng hóa mã nguồn, tránh lồng ghép câu lệnh quá sâu."
        },
        {
            "question": "Theo quy chuẩn PEP 8, cách đặt khoảng trắng xung quanh toán tử gán `=` nào dưới đây là chuẩn xác nhất?",
            "options": [
                "order_amount=1500000",
                "order_amount = 1500000",
                "order_amount  =  1500000",
                "order_amount =1500000"
            ],
            "correct_option_index": 1,
            "explanation": "PEP 8 khuyến nghị luôn luôn đặt đúng 1 khoảng trắng ở cả hai bên toán tử gán `=` (ví dụ: `order_amount = 1500000`)."
        }
    ]
    (qz_dir / "quiz.json").write_text(json.dumps(quiz_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("✅ Lesson 04 all resources generated successfully!")

if __name__ == "__main__":
    generate_lesson_03()
    generate_lesson_04()
