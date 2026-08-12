"""
scratch/generate_session_04_lesson_02_reading.py
Generate Reading Material for Session 04 - Lesson 02: Toán tử so sánh và toán tử logic
applying all 5 pedagogical and standard directives.
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from core.renderers.reading_renderer import assemble_reading_html
from core.validators.reading_validator import validate_reading_material

def generate_lesson_02_reading():
    session_id = "Session 04"
    lesson_id = "Lesson 02"
    lesson_title = "Toán tử so sánh và toán tử logic"
    tech_stack = "python"

    out_dir = PROJECT_ROOT / "output" / "pms" / "Lập_trình_Python" / "Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh" / "Lesson 02 - Toán tử so sánh và toán tử logic" / "Bài đọc"
    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir = out_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "reading.html"

    # Generate High-Depth 2D Flat Vector Infographic SVG Asset (Title-Free & 100% Accented Vietnamese)
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%" height="100%">
  <rect width="800" height="280" fill="#f8fafc" rx="16"/>
  <rect x="16" y="16" width="768" height="248" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" rx="12"/>
  
  <!-- TIER 1: ĐẦU VÀO DỮ LIỆU ĐƠN HÀNG -->
  <g transform="translate(35, 35)">
    <rect width="210" height="210" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1.5" rx="10"/>
    <rect width="210" height="36" fill="#e2e8f0" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#0f172a">1. Đầu vào đơn hàng</text>
    
    <rect x="15" y="50" width="180" height="40" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="68" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Giá trị đơn hàng</text>
    <text x="25" y="83" font-family="JetBrains Mono, monospace" font-size="11" fill="#be111c">order_amount = 250.000</text>
    
    <rect x="15" y="98" width="180" height="40" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="116" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Hạng thành viên VIP</text>
    <text x="25" y="131" font-family="JetBrains Mono, monospace" font-size="11" fill="#2563eb">is_vip_member = True</text>
    
    <rect x="15" y="146" width="180" height="40" fill="#ffffff" stroke="#e2e8f0" rx="6"/>
    <text x="25" y="164" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#334155">Mã giảm giá Voucher</text>
    <text x="25" y="179" font-family="JetBrains Mono, monospace" font-size="11" fill="#16a34a">has_voucher = True</text>
  </g>
  
  <!-- Arrow 1 -->
  <path d="M 255 140 L 285 140" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow)"/>

  <!-- TIER 2: ĐÁNH GIÁ ĐIỀU KIỆN LOGIC -->
  <g transform="translate(295, 35)">
    <rect width="220" height="210" fill="#eff6ff" stroke="#93c5fd" stroke-width="1.5" rx="10"/>
    <rect width="220" height="36" fill="#dbeafe" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#1e40af">2. Đánh giá toán tử logic</text>

    <!-- Condition 1 -->
    <rect x="15" y="50" width="190" height="42" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="67" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">So sánh (order_amount &gt;= 200k):</text>
    <text x="25" y="83" font-family="JetBrains Mono, monospace" font-size="11" fill="#059669">True (Đúng điều kiện)</text>

    <!-- Condition 2 -->
    <rect x="15" y="98" width="190" height="42" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="115" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">Logic và (AND condition):</text>
    <text x="25" y="131" font-family="JetBrains Mono, monospace" font-size="11" fill="#059669">True and True ➔ True</text>

    <!-- Condition 3 -->
    <rect x="15" y="146" width="190" height="42" fill="#ffffff" stroke="#bfdbfe" rx="6"/>
    <text x="25" y="163" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e3a8a">Quyết định ưu đãi Freeship:</text>
    <text x="25" y="179" font-family="JetBrains Mono, monospace" font-size="11" fill="#1d4ed8">is_eligible_freeship = True</text>
  </g>

  <!-- Arrow 2 -->
  <path d="M 525 140 L 555 140" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>

  <!-- TIER 3: KẾT QUẢ ÁP DỤNG ƯU ĐÃI -->
  <g transform="translate(565, 35)">
    <rect width="200" height="210" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5" rx="10"/>
    <rect width="200" height="36" fill="#dcfce7" rx="10"/>
    <text x="15" y="23" font-family="Inter, sans-serif" font-size="13" font-weight="bold" fill="#166534">3. Kết quả áp dụng</text>

    <rect x="15" y="52" width="170" height="65" fill="#ffffff" stroke="#bbf7d0" rx="8"/>
    <text x="25" y="73" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#15803d">MIỄN PHÍ GIAO HÀNG</text>
    <text x="25" y="98" font-family="JetBrains Mono, monospace" font-size="15" font-weight="bold" fill="#15803d">FREESHIP (True)</text>

    <rect x="15" y="127" width="170" height="65" fill="#ffffff" stroke="#bbf7d0" rx="8"/>
    <text x="25" y="148" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#15803d">MỨC GIẢM GIÁ VOUCHER</text>
    <text x="25" y="173" font-family="JetBrains Mono, monospace" font-size="15" font-weight="bold" fill="#15803d">Giảm 15%</text>
  </g>

  <!-- Defs Marker -->
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/>
    </marker>
  </defs>
</svg>"""
    (images_dir / "illustration_lesson_02.svg").write_text(svg_content, encoding="utf-8")

    # Section 1: Problem Statement
    sec1_html = """
<p class="text-slate-600 mb-4 leading-relaxed">
Hãy tưởng tượng bạn đang xây dựng hệ thống thanh toán tự động cho ứng dụng mua sắm <strong>ShopeeFood</strong> hoặc cổng thanh toán ngân hàng số. Khi khách hàng nhấn nút <em>"Đặt hàng"</em>, ứng dụng không chỉ đơn thuần kiểm tra số tiền trong ví mà còn phải đồng thời đánh giá hàng loạt điều kiện thực tế: Số dư tài khoản có đủ thanh toán không? Mã giảm giá có còn hạn sử dụng không? Người dùng có thuộc nhóm thành viên VIP để nhận ưu đãi freeship không?
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Nếu máy tính chỉ biết tính toán cộng trừ đơn thuần, làm sao chương trình có thể đưa ra quyết định thông minh như <code>Đồng ý duyệt đơn</code> hoặc <code>Từ chối giao dịch</code>? Đây chính là lúc bạn cần đến <strong>Toán tử so sánh (Comparison Operators)</strong> để so sánh các giá trị và <strong>Toán tử logic (Logical Operators)</strong> để kết hợp nhiều điều kiện nghiệp vụ phức tạp lại với nhau.
</p>
<p class="text-slate-600 mb-4 leading-relaxed">
Nhờ sự kết hợp chặt chẽ giữa hai nhóm toán tử này, các hệ thống phần mềm doanh nghiệp có thể tự động hóa hàng triệu giao dịch mỗi phút với độ chính xác tuyệt đối mà không cần bất kỳ sự can thiệp thủ công nào từ con người.
</p>
"""

    # Section 2: Syntax Breakdown -> Component Explanation -> Live Runnable Sandbox
    sec2_html = """
<h3 id="sec-2-1-toan-tu-so-sanh-bang-gia-tri-va-kieu-boolean" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.1. Cú pháp và giải thích Toán tử so sánh (Comparison Operators)</h3>

<p class="text-slate-600 mb-4 leading-relaxed">
Toán tử so sánh dùng để so sánh giữa 2 biểu thức hoặc 2 giá trị. Kết quả của một phép so sánh <strong>luôn luôn trả về kiểu dữ liệu Boolean (Logic)</strong>: chỉ có thể là <code>True</code> (Đúng) hoặc <code>False</code> (Sai).
</p>

<!-- 1. CÚ PHÁP CHUẨN (Syntax Card) -->
<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">Cú pháp định nghĩa phép so sánh trong Python</span>
    </span>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs language-python">result = value_a operator value_b</code></pre>
</div>

<!-- 2. GIẢI THÍCH CÚ PHÁP (Component Explanation List) -->
<div class="space-y-2 text-slate-700 my-4 pl-2">
  <p class="font-semibold text-slate-900 mb-2">Chi tiết thành phần cú pháp:</p>
  <ul class="list-disc pl-6 space-y-2 text-slate-600">
    <li><strong class="text-slate-900"><code>value_a</code>, <code>value_b</code></strong>: Các hằng số, biến số hoặc biểu thức cần mang ra so sánh (số nguyên, số thực, chuỗi ký tự).</li>
    <li><strong class="text-slate-900"><code>operator</code> (Toán tử so sánh)</strong>: Ký hiệu so sánh bao gồm:
      <code class="text-rikkei-red font-mono">==</code> (Bằng), 
      <code class="text-rikkei-red font-mono">!=</code> (Khác), 
      <code class="text-rikkei-red font-mono">&gt;</code> (Lớn hơn), 
      <code class="text-rikkei-red font-mono">&lt;</code> (Nhỏ hơn), 
      <code class="text-rikkei-red font-mono">&gt;=</code> (Lớn hơn hoặc bằng), 
      <code class="text-rikkei-red font-mono">&lt;=</code> (Nhỏ hơn hoặc bằng).
    </li>
    <li><strong class="text-slate-900"><code>result</code></strong>: Biến nhận kết quả kiểu Boolean, lưu trữ giá trị <code>True</code> hoặc <code>False</code>.</li>
  </ul>
</div>

<div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
  <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-push-pin text-sky-600"></i> Yêu cầu bài toán thực hành:</div>
  <p class="text-sm text-slate-700">So sánh giá trị đơn hàng 250,000 VNĐ với hạn mức tối thiểu 200,000 VNĐ để xác định xem có đủ điều kiện nhận ưu đãi hay không.</p>
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
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-2-1" class="language-python" contenteditable="true" spellcheck="false" data-original="# 1. Khai báo giá trị đơn hàng thực tế
order_total = 250000
min_threshold = 200000

# 2. Thực hiện các phép so sánh cơ bản
is_eligible = order_total >= min_threshold
is_equal = order_total == min_threshold
is_different = order_total != min_threshold

print('Đủ điều kiện freeship:', is_eligible)    # Trả về: True
print('Đơn hàng bằng đúng hạn mức:', is_equal) # Trả về: False
print('Đơn hàng khác hạn mức:', is_different)  # Trả về: True" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># 1. Khai báo giá trị đơn hàng thực tế
order_total = 250000
min_threshold = 200000

# 2. Thực hiện các phép so sánh cơ bản
is_eligible = order_total >= min_threshold
is_equal = order_total == min_threshold
is_different = order_total != min_threshold

print('Đủ điều kiện freeship:', is_eligible)    # Trả về: True
print('Đơn hàng bằng đúng hạn mức:', is_equal) # Trả về: False
print('Đơn hàng khác hạn mức:', is_different)  # Trả về: True</code></pre>
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

<div class="overflow-x-auto my-6">
  <table class="w-full text-sm text-left text-slate-700 border border-slate-200 rounded-lg">
    <thead class="bg-slate-100 text-slate-900 font-montserrat font-bold text-xs uppercase">
      <tr>
        <th class="px-4 py-3 border-b">Toán tử</th>
        <th class="px-4 py-3 border-b">Tên gọi kỹ thuật (Tiếng Anh)</th>
        <th class="px-4 py-3 border-b">Ví dụ minh họa</th>
        <th class="px-4 py-3 border-b">Kết quả trả về</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-200">
      <tr>
        <td class="px-4 py-3 font-mono font-bold text-rikkei-red">==</td>
        <td class="px-4 py-3">So sánh bằng (Equal to)</td>
        <td class="px-4 py-3 font-mono">10 == 10</td>
        <td class="px-4 py-3 font-mono font-bold text-emerald-600">True (Đúng)</td>
      </tr>
      <tr>
        <td class="px-4 py-3 font-mono font-bold text-rikkei-red">!=</td>
        <td class="px-4 py-3">So sánh khác (Not equal to)</td>
        <td class="px-4 py-3 font-mono">10 != 5</td>
        <td class="px-4 py-3 font-mono font-bold text-emerald-600">True (Đúng)</td>
      </tr>
      <tr>
        <td class="px-4 py-3 font-mono font-bold text-rikkei-red">&gt;</td>
        <td class="px-4 py-3">Lớn hơn (Greater than)</td>
        <td class="px-4 py-3 font-mono">15 &gt; 20</td>
        <td class="px-4 py-3 font-mono font-bold text-rose-600">False (Sai)</td>
      </tr>
      <tr>
        <td class="px-4 py-3 font-mono font-bold text-rikkei-red">&lt;</td>
        <td class="px-4 py-3">Nhỏ hơn (Less than)</td>
        <td class="px-4 py-3 font-mono">15 &lt; 20</td>
        <td class="px-4 py-3 font-mono font-bold text-emerald-600">True (Đúng)</td>
      </tr>
      <tr>
        <td class="px-4 py-3 font-mono font-bold text-rikkei-red">&gt;=</td>
        <td class="px-4 py-3">Lớn hơn hoặc bằng (Greater than or equal to)</td>
        <td class="px-4 py-3 font-mono">20 &gt;= 20</td>
        <td class="px-4 py-3 font-mono font-bold text-emerald-600">True (Đúng)</td>
      </tr>
      <tr>
        <td class="px-4 py-3 font-mono font-bold text-rikkei-red">&lt;=</td>
        <td class="px-4 py-3">Nhỏ hơn hoặc bằng (Less than or equal to)</td>
        <td class="px-4 py-3 font-mono">25 &lt;= 20</td>
        <td class="px-4 py-3 font-mono font-bold text-rose-600">False (Sai)</td>
      </tr>
    </tbody>
  </table>
</div>

<h3 id="sec-2-2-toan-tu-logic-and-or-not" class="font-montserrat font-bold text-xl text-slate-900 mb-3">2.2. Cú pháp và giải thích Toán tử logic (Logical Operators: and, or, not)</h3>

<p class="text-slate-600 mb-4 leading-relaxed">
Toán tử logic cho phép bạn kết hợp nhiều phép so sánh đơn lẻ lại với nhau để tạo thành một biểu thức điều kiện hoàn chỉnh.
</p>

<!-- 1. CÚ PHÁP CHUẨN (Syntax Card) -->
<div class="my-5 rounded-xl overflow-hidden border border-slate-200 bg-slate-50 shadow-sm">
  <div class="px-3.5 py-2 bg-slate-100/90 text-xs font-sans text-slate-700 border-b border-slate-200 flex justify-between items-center">
    <span class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-[#ff5f56] border border-[#e0443e] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#ffbd2e] border border-[#dea123] inline-block shadow-sm"></span>
      <span class="w-3 h-3 rounded-full bg-[#27c93f] border border-[#1aab29] inline-block shadow-sm"></span>
      <span class="ml-2 font-semibold text-slate-800">Cú pháp kết hợp điều kiện logic trong Python</span>
    </span>
  </div>
  <pre class="m-0 overflow-x-auto"><code class="hljs language-python"># Cú pháp kết hợp VÀ (and), HOẶC (or), PHỦ ĐỊNH (not)
check_and = (condition_1) and (condition_2)
check_or  = (condition_1) or (condition_2)
check_not = not (condition_1)</code></pre>
</div>

<!-- 2. GIẢI THÍCH CÚ PHÁP (Component Explanation List) -->
<div class="space-y-2 text-slate-700 my-4 pl-2">
  <p class="font-semibold text-slate-900 mb-2">Chi tiết thành phần cú pháp:</p>
  <ul class="list-disc pl-6 space-y-2 text-slate-600">
    <li><strong class="text-slate-900"><code>and</code> (Toán tử VÀ)</strong>: Trả về <code>True</code> <strong>chỉ khi tất cả</strong> các điều kiện thành phần đều trả về <code>True</code>. Nếu có ít nhất 1 điều kiện Sai (<code>False</code>), toàn bộ phép tính sẽ bằng <code>False</code>.</li>
    <li><strong class="text-slate-900"><code>or</code> (Toán tử HOẶC)</strong>: Trả về <code>True</code> chỉ cần <strong>ít nhất một</strong> điều kiện thành phần là <code>True</code>. Chỉ trả về <code>False</code> khi toàn bộ các điều kiện đều Sai.</li>
    <li><strong class="text-slate-900"><code>not</code> (Toán tử PHỦ ĐỊNH)</strong>: Đảo ngược kết quả logic. Đổi <code>True</code> thành <code>False</code> và ngược lại.</li>
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
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-2-2" class="language-python" contenteditable="true" spellcheck="false" data-original="# Demo đánh giá điều kiện toán tử logic
account_balance = 500000
cart_total = 350000
is_vip_member = True
has_coupon = False

# Kiểm tra điều kiện mua hàng: Số dư >= Giá hàng VÀ (Thành viên VIP HOẶC Có Coupon)
can_checkout = (account_balance >= cart_total) and (is_vip_member or has_coupon)

print('Kết quả duyệt thanh toán đơn hàng:', can_checkout)" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># Demo đánh giá điều kiện toán tử logic
account_balance = 500000
cart_total = 350000
is_vip_member = True
has_coupon = False

# Kiểm tra điều kiện mua hàng: Số dư >= Giá hàng VÀ (Thành viên VIP HOẶC Có Coupon)
can_checkout = (account_balance >= cart_total) and (is_vip_member or has_coupon)

print('Kết quả duyệt thanh toán đơn hàng:', can_checkout)</code></pre>
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
"""

    # Section 3: Clean Sub-headings (NO "Ví dụ cơ bản:", NO "Ví dụ nghiệp vụ:") + All Live Executable Sandboxes
    sec3_html = """
<h3 id="sec-3-1-kiem-tra-do-tuoi-xem-phim-c18" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Kiểm tra độ tuổi xem phim chiếu rạp (C18)</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Ứng dụng rạp chiếu phim RATP cần xác minh khán giả có đủ từ 18 tuổi trở lên VÀ có mang theo Căn cước công dân (CCCD) hợp lệ để được cấp vé vào xem các bộ phim giới hạn độ tuổi.
</p>

<h3 id="sec-3-1-kiem-tra-han-muc-don-hang-nhan-ma-freeship" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.1. Kiểm tra hạn mức đơn hàng nhận mã Freeship ShopeeFood</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Hệ thống thanh toán tự động kiểm tra xem đơn hàng mua đồ ăn có đạt giá trị tối thiểu 200,000 VNĐ VÀ người dùng đã lưu mã miễn phí vận chuyển trong ví hay chưa.
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
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-3-1" class="language-python" contenteditable="true" spellcheck="false" data-original="# Khai báo thông tin đơn hàng
order_total = 250000
min_threshold = 200000
has_freeship_voucher = True

# Yêu cầu: Giá trị đơn >= 200k VÀ có mã freeship
is_eligible = (order_total >= min_threshold) and has_freeship_voucher

print('Được miễn phí giao hàng ShopeeFood:', is_eligible)" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># Khai báo thông tin đơn hàng
order_total = 250000
min_threshold = 200000
has_freeship_voucher = True

# Yêu cầu: Giá trị đơn >= 200k VÀ có mã freeship
is_eligible = (order_total >= min_threshold) and has_freeship_voucher

print('Được miễn phí giao hàng ShopeeFood:', is_eligible)</code></pre>
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

<h3 id="sec-3-2-xet-duyet-uu-dai-dac-quyen-khach-hang-vip" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.2. Xét duyệt ưu đãi đặc quyền cho Khách hàng VIP ShopeeFood</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Hệ thống khuyến mãi tự động áp dụng giảm giá 20% nếu giá trị đơn hàng đạt từ 500,000 VNĐ trở lên HOẶC tài khoản người dùng đã nâng cấp lên hạng thành viên VIP.
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
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-3-2" class="language-python" contenteditable="true" spellcheck="false" data-original="# Khai báo thông tin giao dịch
order_total = 450000
is_vip_member = True
has_gold_voucher = False

# Điều kiện: Đơn >= 500k HOẶC là thành viên VIP
is_eligible_vip_discount = (order_total >= 500000) or is_vip_member

print('Đạt điều kiện ưu đãi đặc quyền VIP:', is_eligible_vip_discount)" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># Khai báo thông tin giao dịch
order_total = 450000
is_vip_member = True
has_gold_voucher = False

# Điều kiện: Đơn >= 500k HOẶC là thành viên VIP
is_eligible_vip_discount = (order_total >= 500000) or is_vip_member

print('Đạt điều kiện ưu đãi đặc quyền VIP:', is_eligible_vip_discount)</code></pre>
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

<h3 id="sec-3-3-tu-dong-duyet-thanh-toan-va-xuat-hoa-don-don-hang" class="font-montserrat font-bold text-xl text-slate-900 mb-3">3.3. Tự động duyệt thanh toán và xuất hóa đơn đơn hàng ShopeeFood</h3>
<p class="text-slate-600 mb-4 leading-relaxed">
Tại bước xác nhận thanh toán cuối cùng, hệ thống kiểm tra số dư ví phải đủ trả tiền đơn hàng VÀ tài khoản ở trạng thái hoạt động VÀ tài khoản KHÔNG bị tạm khóa bảo mật.
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
    <pre class="m-0 p-0 bg-transparent"><code id="code-sb-3-3" class="language-python" contenteditable="true" spellcheck="false" data-original="# Khai báo số dư ví và trạng thái tài khoản
order_total = 350000
wallet_balance = 500000
is_account_active = True
is_blocked = False

# Đánh giá tổng hợp điều kiện thanh toán đơn hàng
can_checkout = (wallet_balance >= order_total and is_account_active) and not is_blocked

print('Xác nhận duyệt đơn hàng ShopeeFood thành công:', can_checkout)" style="display:block; padding:0.75rem 6rem 0.75rem 0.75rem; min-height:2.5rem; outline:none !important; border:none !important; box-shadow:none !important; white-space:pre; overflow-x:auto;"># Khai báo số dư ví và trạng thái tài khoản
order_total = 350000
wallet_balance = 500000
is_account_active = True
is_blocked = False

# Đánh giá tổng hợp điều kiện thanh toán đơn hàng
can_checkout = (wallet_balance >= order_total and is_account_active) and not is_blocked

print('Xác nhận duyệt đơn hàng ShopeeFood thành công:', can_checkout)</code></pre>
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

    # Section 4: Production Gotchas - Formal Technical Terms (NO AI buzzwords like 'bẫy', 'gotcha')
    sec4_html = """
<div class="space-y-4">
  <div class="p-4 rounded-xl border border-rose-200 bg-rose-50/60 text-slate-800 my-4">
    <div class="font-bold text-rose-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-warning-circle text-rose-600"></i> Lỗi thường gặp 1: Nhầm lẫn giữa toán tử gán (=) và toán tử so sánh bằng (==)</div>
    <p class="text-sm text-slate-700">Trong Python, dấu <code>=</code> dùng để gán giá trị cho biến, trong khi <code>==</code> mới dùng để so sánh giá trị. Việc viết <code>if x = 10:</code> sẽ làm chương trình báo lỗi cú pháp <code>SyntaxError</code> ngay lập tức!</p>
  </div>

  <div class="p-4 rounded-xl border border-amber-200 bg-amber-50/60 text-slate-800 my-4">
    <div class="font-bold text-amber-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-lightning text-amber-600"></i> Lỗi thường gặp 2: Hiện tượng Đánh giá ngắn mạch (Short-circuit Evaluation)</div>
    <p class="text-sm text-slate-700">Với toán tử <code>and</code> (VÀ), nếu biểu thức điều kiện đầu tiên trả về <code>False</code> (Sai), Python sẽ lập tức dừng lại và kết luận kết quả là <code>False</code> mà không cần tính toán tiếp điều kiện phía sau. Tương tự với <code>or</code> (HOẶC), nếu biểu thức đầu là <code>True</code>, các biểu thức phía sau cũng sẽ được bỏ qua để tối ưu tốc độ xử lý.</p>
  </div>

  <div class="p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4">
    <div class="font-bold text-sky-900 mb-1 flex items-center gap-1.5"><i class="ph-bold ph-brackets-curly text-sky-600"></i> Lỗi thường gặp 3: Thứ tự ưu tiên toán tử (Operator Precedence)</div>
    <p class="text-sm text-slate-700">Toán tử <code>and</code> có độ ưu tiên cao hơn toán tử <code>or</code>. Do đó, biểu thức <code>A or B and C</code> sẽ luôn được Python tự động hiểu là <code>A or (B and C)</code>. Bạn nên dùng dấu ngoặc đơn <code>()</code> để thể hiện rõ ràng ý đồ nghiệp vụ của mình.</p>
  </div>
</div>
"""

    json_payload = {
        "tech_stack": tech_stack,
        "lesson_title": f"{lesson_id} - {lesson_title}",
        "context_image_url": "images/illustration_lesson_02.svg",
        "show_visualizer": True,
        "section_titles": {
            "sec1": "Tại sao cần toán tử so sánh và toán tử logic trong lập trình?",
            "sec2": "Cú pháp và cơ chế hoạt động của toán tử so sánh & logic",
            "sec3": "Các ví dụ ứng dụng thực tiễn trong hệ thống tài chính & ShopeeFood",
            "sec4": "Tổng kết bài học & Các lỗi thường gặp",
            "sec5": "Tài liệu tham khảo"
        },
        "sec1_html": sec1_html,
        "sec2_html": sec2_html,
        "sec3_html": sec3_html,
        "sec4_html": sec4_html,
        "reference_links": [
            {"title": "Tài liệu chính thức Python 3 - Comparisons & Boolean Operations", "url": "https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not"},
            {"title": "W3Schools Python Operators & Truth Tables Guide", "url": "https://www.w3schools.com/python/python_operators.asp"}
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
    generate_lesson_02_reading()
