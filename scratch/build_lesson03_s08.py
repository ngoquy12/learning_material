"""
scratch/build_lesson03_s08.py

Build toàn bộ HyperFrames video project cho:
  Session 08 – Lesson 03: Phạm vi biến và scope (Variable Scope & LEGB Rule)

Pipeline:
  Stage 1: Setup directories
  Stage 2: Kokoro TTS synthesis (hung_thinh, speed=0.95)
  Stage 3: Probe audio durations → durations.json
  Stage 4: Generate Scene HTML files (voice-driven GSAP, dark theme, pure white title, no border-left, no card-badge)
  Stage 5: Build index.html + package.json + meta.json
  Stage 6: Launch npm run render → MP4
"""

import sys, os, json
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent))

from pathlib import Path
from hyperframes.video_pipeline_engine import VoiceDrivenVideoEngine

# ──────────────────────────────────────────────────────────────────────────────
LESSON_SLUG  = "session_08_lesson_03"
LESSON_TITLE = "Phạm vi biến và scope"
TECH_STACK   = "Python/Core"

BASE = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material"
            r"\output\PM_Python\Session 08 - Hàm (Function) va Phạm vi biến"
            r"\Lesson 03 - Phạm vi biến và scope\Video")

OUTPUT_DIR   = BASE / LESSON_SLUG

# ──────────────────────────────────────────────────────────────────────────────
# Blueprint: Approved script for Lesson 03
# ──────────────────────────────────────────────────────────────────────────────
SCENES = [
    # ── Scene 01 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_01",
        "scene_title": "Tổng quan bài học & Bối cảnh thực tế",
        "duration": 28.0,
        "narration": (
            "Chào mừng bạn đến với bài học thứ ba trong Session 8. "
            "Trong phát triển phần mềm doanh nghiệp, đã bao giờ bạn gặp tình huống "
            "một hàm vô tình sửa đổi dữ liệu của hàm khác khiến toàn bộ hệ thống gặp lỗi khó hiểu chưa? "
            "Đây là bài toán về kiểm soát xung đột dữ liệu. "
            "Hôm nay chúng ta sẽ cùng tìm hiểu về Phạm vi biến và Scope — "
            "cơ chế nền tảng giúp Python phân định rõ ranh giới hoạt động và bảo vệ an toàn cho dữ liệu trong chương trình."
        ),
        "clean_content": (
            "Phạm vi biến (Scope) — Ranh giới truy cập dữ liệu\n"
            "Quy tắc LEGB — Thứ tự ưu tiên tìm kiếm biến\n"
            "Từ khóa global & nonlocal — Quản lý vùng nhớ nâng cao"
        ),
        "html_structure": """
<div class="split-3col" style="height:100%;gap:28px;">
  <div class="card-left" style="display:flex;flex-direction:column;gap:16px;background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:32px 36px;">
    <h2 class="card-title" style="font-size:28px;color:#a5b4fc;font-weight:700;margin:0;">Phạm vi biến</h2>
    <p class="card-subtitle" style="color:#94a3b8;font-size:21px;margin:0;">Scope trong Python</p>
    <ul class="bullet-list">
      <li>Ranh giới truy cập dữ liệu</li>
      <li>Ngăn chặn side-effects</li>
      <li>Bảo vệ an toàn bộ nhớ</li>
    </ul>
  </div>
  <div class="card-left" style="display:flex;flex-direction:column;gap:16px;background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:32px 36px;">
    <h2 class="card-title" style="font-size:28px;color:#6ee7b7;font-weight:700;margin:0;">Quy tắc LEGB</h2>
    <p class="card-subtitle" style="color:#94a3b8;font-size:21px;margin:0;">Thứ tự tìm kiếm biến</p>
    <ul class="bullet-list">
      <li>Local &amp; Enclosing</li>
      <li>Global &amp; Built-in</li>
      <li>Ưu tiên từ trong ra ngoài</li>
    </ul>
  </div>
  <div class="card-left" style="display:flex;flex-direction:column;gap:16px;background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:32px 36px;">
    <h2 class="card-title" style="font-size:28px;color:#fdba74;font-weight:700;margin:0;">Từ khóa chuyên dụng</h2>
    <p class="card-subtitle" style="color:#94a3b8;font-size:21px;margin:0;">Quản lý vùng nhớ nâng cao</p>
    <ul class="bullet-list">
      <li>Từ khóa global</li>
      <li>Từ khóa nonlocal</li>
      <li>Best practices chuyên nghiệp</li>
    </ul>
  </div>
</div>
"""
    },
    # ── Scene 02 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_02",
        "scene_title": "Local Scope (Phạm vi cục bộ)",
        "duration": 30.0,
        "narration": (
            "Hãy cùng khám phá cấp độ phạm vi đầu tiên và phổ biến nhất — đó là Local Scope, hay phạm vi cục bộ. "
            "Mỗi khi bạn tạo một biến bên trong một hàm, biến đó sẽ sinh ra và chỉ sống nội bộ trong hàm đó mà thôi. "
            "Khi hàm thực thi xong và trả về kết quả, toàn bộ vùng nhớ Local Scope sẽ bị giải phóng tự động. "
            "Điều này giúp code độc lập và không sợ làm ảnh hưởng đến các biến ở bên ngoài."
        ),
        "clean_content": (
            "Biến khai báo bên trong hàm\n"
            "Chỉ truy cập được trong nội bộ hàm\n"
            "Tự động giải phóng bộ nhớ khi hàm kết thúc"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Đặc tính Local Scope</h2>
    <ul class="bullet-list">
      <li>Khai báo bên trong hàm</li>
      <li>Chỉ tồn tại trong thời gian hàm chạy</li>
      <li>Tự động xoá khi hàm return</li>
    </ul>
    <div class="alert-box alert-info" style="margin-top:auto;">
      <div class="alert-content">
        <p class="alert-title">Lợi ích</p>
        <p class="alert-body">Đảm bảo tính đóng gói (encapsulation) của dữ liệu</p>
      </div>
    </div>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">local_scope.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">calculate_discount</span>(price):
    discount_rate = <span class="num">0.15</span>  <span class="cm"># Local variable</span>
    <span class="kw">return</span> price * (<span class="num">1</span> - discount_rate)

result = <span class="fn">calculate_discount</span>(<span class="num">100</span>)
<span class="fn">print</span>(result)  <span class="cm"># 85.0</span>

<span class="cm"># discount_rate bị xoá sau khi hàm chạy xong!</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 03 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_03",
        "scene_title": "Global Scope (Phạm vi toàn cục)",
        "duration": 29.0,
        "narration": (
            "Trái ngược với phạm vi cục bộ, Global Scope đại diện cho các biến được khai báo ở cấp cao nhất của file mã nguồn. "
            "Một biến toàn cục tồn tại suốt vòng đời của chương trình và có thể được đọc từ bất kỳ hàm nào. "
            "Tuy nhiên, mặc định các hàm con chỉ được phép đọc giá trị chứ không thể tự ý sửa đổi biến toàn cục. "
            "Quy tắc này giúp ngăn chặn các tác dụng phụ không mong muốn trong ứng dụng."
        ),
        "clean_content": (
            "Khai báo ở cấp cao nhất của file code\n"
            "Tồn tại suốt vòng đời chương trình\n"
            "Các hàm được phép đọc nhưng CẤM tự ý ghi đè"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Đặc tính Global Scope</h2>
    <ul class="bullet-list">
      <li>Khai báo ở cấp cao nhất trong file</li>
      <li>Tồn tại suốt vòng đời tiến trình</li>
      <li>Mọi hàm con đều có quyền đọc</li>
    </ul>
    <div class="alert-box alert-warning" style="margin-top:auto;">
      <div class="alert-content">
        <p class="alert-title">Quy tắc bảo vệ</p>
        <p class="alert-body">Hàm được đọc tự do, nhưng muốn ghi đè bắt buộc phải dùng từ khóa <span style="font-family:'Fira Code',monospace;">global</span>.</p>
      </div>
    </div>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">global_scope.py</span>
    </div>
    <pre class="code-body"><code>tax_rate = <span class="num">0.08</span>  <span class="cm"># Global variable</span>

<span class="kw">def</span> <span class="fn">print_invoice</span>(amount):
    <span class="cm"># Đọc biến toàn cục tax_rate</span>
    total = amount * (<span class="num">1</span> + tax_rate)
    <span class="fn">print</span>(<span class="str">f"Tổng hóa đơn: {total}"</span>)

<span class="fn">print_invoice</span>(<span class="num">100</span>)  <span class="cm"># Tổng hóa đơn: 108.0</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 04 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_04",
        "scene_title": "Quy tắc tìm kiếm LEGB",
        "duration": 31.0,
        "narration": (
            "Khi một biến được gọi trong code, làm thế nào Python biết phải lấy giá trị từ đâu? "
            "Bộ thông dịch Python áp dụng một quy tắc tìm kiếm tuần tự từ trong ra ngoài gọi là LEGB. "
            "Viết tắt của bốn cấp độ: L là Local, E là Enclosing, G là Global, và B là Built-in. "
            "Python sẽ kiểm tra từng phân vùng theo đúng thứ tự này và dừng lại ngay khi tìm thấy biến đầu tiên khớp tên."
        ),
        "clean_content": (
            "1. L — Local (Hàm hiện tại)\n"
            "2. E — Enclosing (Hàm cha bao ngoài)\n"
            "3. G — Global (Phạm vi file)\n"
            "4. B — Built-in (Hàm có sẵn)"
        ),
        "html_structure": """
<div class="card-full" style="height:100%;background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:36px 44px;">
  <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0 0 28px 0;">Quy tắc tìm kiếm biến LEGB (từ trong ra ngoài)</h2>
  <ol class="step-list">
    <li><span class="step-num">1</span><span><strong style="color:#6ee7b7;font-family:'Fira Code',monospace;">L — Local</strong>: Tìm trong nội bộ hàm đang thực thi</span></li>
    <li><span class="step-num">2</span><span><strong style="color:#818cf8;font-family:'Fira Code',monospace;">E — Enclosing</strong>: Tìm trong hàm bao ngoài (nested function)</span></li>
    <li><span class="step-num">3</span><span><strong style="color:#fdba74;font-family:'Fira Code',monospace;">G — Global</strong>: Tìm ở cấp cao nhất của file mã nguồn</span></li>
    <li><span class="step-num">4</span><span><strong style="color:#f87171;font-family:'Fira Code',monospace;">B — Built-in</strong>: Tìm trong các hàm hệ thống <span style="font-family:'Fira Code',monospace;color:#a5b4fc;">(len, print, sum)</span></span></li>
  </ol>
  <div class="alert-box alert-info" style="margin-top:28px;">
    <div class="alert-content">
      <p class="alert-title">Nguyên lý hoạt động</p>
      <p class="alert-body">Python quét tuần tự từ L ➔ E ➔ G ➔ B và trả về giá trị ngay khi tìm thấy vị trí đầu tiên khớp tên.</p>
    </div>
  </div>
</div>
"""
    },
    # ── Scene 05 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_05",
        "scene_title": "Từ khóa global",
        "duration": 30.0,
        "narration": (
            "Giả sử bạn thực sự cần thay đổi một giá trị cấu hình toàn cục từ bên trong một hàm thì phải làm thế nào? "
            "Đây là lúc từ khóa global phát huy tác dụng. "
            "Khai báo global cùng tên biến ở đầu hàm là cách bạn thông báo cho Python biết: "
            "hãy thao tác trực tiếp lên ô nhớ toàn cục thay vì tạo một biến cục bộ mới. "
            "Xem ví dụ hàm update_tax bên phải để thấy cách biến tax_rate bị thay đổi."
        ),
        "clean_content": (
            "Cho phép hàm ghi đè trực tiếp biến toàn cục\n"
            "Khai báo ở dòng đầu tiên bên trong hàm\n"
            "Tránh tự động tạo biến Local trùng tên"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Từ khóa global</h2>
    <ul class="bullet-list">
      <li>Cho phép ghi đè biến Global trong hàm</li>
      <li>Khai báo ở dòng đầu bên trong hàm</li>
      <li>Liên kết trực tiếp ô nhớ toàn cục</li>
    </ul>
    <div class="alert-box alert-warning" style="margin-top:auto;">
      <div class="alert-content">
        <p class="alert-title">Cú pháp</p>
        <p class="alert-body" style="font-family:'Fira Code',monospace;">global tax_rate</p>
      </div>
    </div>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">global_keyword.py</span>
    </div>
    <pre class="code-body"><code>tax_rate = <span class="num">0.08</span>  <span class="cm"># Global</span>

<span class="kw">def</span> <span class="fn">update_tax</span>(new_rate):
    <span class="kw">global</span> tax_rate  <span class="cm"># Liên kết biến Global</span>
    tax_rate = new_rate

<span class="fn">print</span>(tax_rate)   <span class="cm"># 0.08</span>
<span class="fn">update_tax</span>(<span class="num">0.10</span>)
<span class="fn">print</span>(tax_rate)   <span class="cm"># 0.1</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 06 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_06",
        "scene_title": "Cảnh báo lạm dụng global (Anti-pattern)",
        "duration": 28.0,
        "narration": (
            "Mặc dù từ khóa global rất tiện lợi, nhưng lạm dụng nó lại là một anti-pattern bị nghiêm cấm trong các dự án doanh nghiệp. "
            "Khi quá nhiều hàm cùng sửa chung biến toàn cục, chương trình sẽ rơi vào trạng thái khó kiểm soát và cực kỳ dễ sinh bug. "
            "Giải pháp chuẩn mực hơn là truyền dữ liệu qua tham số và nhận kết quả trả về thông qua câu lệnh return."
        ),
        "clean_content": (
            "BAD: Phụ thuộc biến Global (lạm dụng global) ❌\n"
            "GOOD: Hàm thuần khiết (Pure Function) dùng tham số & return ✅"
        ),
        "html_structure": """
<div class="split-equal" style="height:100%;gap:28px;">
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">bad_global.py (KHÔNG NÊN ❌)</span>
    </div>
    <pre class="code-body"><code><span class="cm"># BAD: Phụ thuộc biến Global</span>
count = <span class="num">0</span>

<span class="kw">def</span> <span class="fn">increment</span>():
    <span class="kw">global</span> count
    count += <span class="num">1</span>

<span class="fn">increment</span>()</code></pre>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">good_pure.py (KHUYẾN NGHỊ ✅)</span>
    </div>
    <pre class="code-body"><code><span class="cm"># GOOD: Pure function</span>
<span class="kw">def</span> <span class="fn">increment</span>(current_count):
    <span class="kw">return</span> current_count + <span class="num">1</span>

count = <span class="num">0</span>
count = <span class="fn">increment</span>(count)</code></pre>
  </div>
</div>
"""
    },
    # ── Scene 07 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_07",
        "scene_title": "Enclosing Scope & Từ khóa nonlocal",
        "duration": 32.0,
        "narration": (
            "Trong Python, bạn có thể định nghĩa một hàm nằm bên trong một hàm khác — gọi là nested function. "
            "Phạm vi biến của hàm cha đối với hàm con được gọi là Enclosing Scope. "
            "Nếu hàm con muốn sửa đổi biến của hàm cha mà không chạm vào biến Global, chúng ta sử dụng từ khóa nonlocal. "
            "Đây là nền tảng kỹ thuật quan trọng để xây dựng Closure và Decorator trong Python."
        ),
        "clean_content": (
            "Phạm vi xuất hiện trong hàm lồng nhau (nested functions)\n"
            "Biến thuộc hàm cha bao ngoài\n"
            "nonlocal cho phép hàm con sửa biến hàm cha\n"
            "Nền tảng của Closure & Decorator"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Enclosing &amp; nonlocal</h2>
    <ul class="bullet-list">
      <li>Phạm vi hàm bao ngoài (nested function)</li>
      <li>Biến thuộc hàm cha nhưng nằm ngoài hàm con</li>
      <li><span style="font-family:'Fira Code',monospace;color:#fdba74;">nonlocal</span> cho phép hàm con sửa biến hàm cha</li>
      <li>Nền tảng của Closure &amp; Decorator</li>
    </ul>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">nonlocal_demo.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">outer_calculator</span>():
    fee = <span class="num">15.0</span>  <span class="cm"># Enclosing scope</span>

    <span class="kw">def</span> <span class="fn">inner_apply</span>():
        <span class="kw">nonlocal</span> fee  <span class="cm"># Sửa biến hàm cha</span>
        fee = <span class="num">20.0</span>

    <span class="fn">inner_apply</span>()
    <span class="kw">return</span> fee

<span class="fn">print</span>(<span class="fn">outer_calculator</span>())  <span class="cm"># 20.0</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 08 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_08",
        "scene_title": "Lỗi UnboundLocalError",
        "duration": 30.0,
        "narration": (
            "Một trong những cái bẫy kinh điển khiến nhiều lập trình viên mới gặp lỗi là UnboundLocalError. "
            "Lỗi này xảy ra khi bạn vừa đọc vừa gán một biến trùng tên với biến toàn cục trong cùng một hàm mà không khai báo global. "
            "Python thấy lệnh gán nên đánh dấu biến đó là Local, dẫn đến việc dòng đọc giá trị trước đó bị sụp đổ vì biến Local chưa được khởi tạo."
        ),
        "clean_content": (
            "UnboundLocalError: local variable referenced before assignment\n"
            "Vừa đọc vừa gán biến trùng tên Global trong hàm\n"
            "Python tự coi biến đó là Local ➔ văng lỗi khi đọc"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Bẫy UnboundLocalError</h2>
    <div class="alert-box alert-danger">
      <div class="alert-content">
        <p class="alert-title">Thông báo lỗi</p>
        <p class="alert-body" style="font-family:'Fira Code',monospace;font-size:18px;">UnboundLocalError: local variable 'counter' referenced before assignment</p>
      </div>
    </div>
    <ul class="bullet-list">
      <li>Phép gán làm Python coi biến là Local</li>
      <li>Dòng đọc phía trên văng lỗi vì chưa khởi tạo</li>
    </ul>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">bug_unbound.py (LỖI RUNTIME ❌)</span>
    </div>
    <pre class="code-body"><code>counter = <span class="num">10</span>

<span class="kw">def</span> <span class="fn">invalid_increment</span>():
    <span class="cm"># LỖI: counter được coi là Local do gán ở dưới!</span>
    <span class="fn">print</span>(counter)  <span class="cm"># UnboundLocalError!</span>
    counter += <span class="num">1</span>

<span class="fn">invalid_increment</span>()</code></pre>
  </div>
</div>
"""
    },
    # ── Scene 09 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_09",
        "scene_title": "Lỗi NameError khi truy cập ngoài scope",
        "duration": 28.0,
        "narration": (
            "Tương tự, một lỗi phổ biến khác là NameError khi bạn cố gắng truy cập một biến cục bộ từ bên ngoài hàm. "
            "Hãy nhớ rằng biến trong Local Scope sẽ biến mất ngay khi hàm kết thúc. "
            "Việc gọi tên biến đó ở scope bên ngoài là hành vi vi phạm ranh giới bộ nhớ, và Python sẽ ngắt chương trình bằng thông báo NameError ngay lập tức."
        ),
        "clean_content": (
            "NameError: name 'temp_val' is not defined\n"
            "Cố tình gọi biến Local ở bên ngoài phạm vi hàm\n"
            "Biến Local đã bị xoá khỏi bộ nhớ khi hàm kết thúc"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Bẫy NameError</h2>
    <div class="alert-box alert-danger">
      <div class="alert-content">
        <p class="alert-title">Thông báo lỗi</p>
        <p class="alert-body" style="font-family:'Fira Code',monospace;font-size:18px;">NameError: name 'temp_val' is not defined</p>
      </div>
    </div>
    <ul class="bullet-list">
      <li>Cố gọi biến Local ở Global Scope</li>
      <li>Biến đã bị giải phóng bộ nhớ khi hàm return</li>
    </ul>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">bug_name_error.py (LỖI RUNTIME ❌)</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">create_session</span>():
    temp_val = <span class="str">"SECRET_123"</span>  <span class="cm"># Local</span>
    <span class="kw">return</span> <span class="kw">True</span>

<span class="fn">create_session</span>()
<span class="cm"># LỖI: temp_val không tồn tại ở Global Scope!</span>
<span class="fn">print</span>(temp_val)  <span class="cm"># NameError!</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 10 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_10",
        "scene_title": "Tổng kết & Best Practices",
        "duration": 31.0,
        "narration": (
            "Tổng kết lại bài học hôm nay: Bạn đã làm chủ bốn cấp độ quy tắc LEGB từ Local, Enclosing, Global đến Built-in. "
            "Hãy nhớ dùng global khi muốn sửa biến toàn cục và nonlocal khi làm việc với hàm lồng nhau. "
            "Tuy nhiên, Best practice hàng đầu trong phát triển phần mềm chuyên nghiệp là hạn chế tối đa biến toàn cục, "
            "giữ các hàm độc lập và luôn truyền nhận dữ liệu qua tham số và giá trị trả về."
        ),
        "clean_content": (
            "L — Local: Sinh ra & mất đi cùng hàm\n"
            "E — Enclosing: Hàm bao ngoài, dùng nonlocal\n"
            "G — Global: Cấp file, dùng global khi ghi đè\n"
            "B — Built-in: Hàm tích hợp hệ thống"
        ),
        "html_structure": """
<div style="height:100%;display:flex;flex-direction:column;gap:24px;">
  <div class="split-equal" style="flex:1;gap:24px;">
    <div style="display:flex;flex-direction:column;gap:16px;">
      <div class="alert-box alert-info">
        <div class="alert-content">
          <p class="alert-title" style="font-size:22px;">Local (L)</p>
          <p class="alert-body" style="font-size:19px;">Sinh ra &amp; mất đi cùng vòng đời của hàm</p>
        </div>
      </div>
      <div class="alert-box alert-success">
        <div class="alert-content">
          <p class="alert-title" style="font-size:22px;">Enclosing (E)</p>
          <p class="alert-body" style="font-size:19px;">Hàm bao ngoài, dùng từ khóa <span style="font-family:'Fira Code',monospace;">nonlocal</span></p>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:16px;">
      <div class="alert-box alert-warning">
        <div class="alert-content">
          <p class="alert-title" style="font-size:22px;">Global (G)</p>
          <p class="alert-body" style="font-size:19px;">Cấp file, dùng <span style="font-family:'Fira Code',monospace;">global</span> khi cần ghi đè</p>
        </div>
      </div>
      <div class="alert-box alert-danger">
        <div class="alert-content">
          <p class="alert-title" style="font-size:22px;">Built-in (B)</p>
          <p class="alert-body" style="font-size:19px;">Hàm tích hợp hệ thống <span style="font-family:'Fira Code',monospace;">(len, print, sum)</span></p>
        </div>
      </div>
    </div>
  </div>
  <div class="alert-box alert-info" style="margin-top:0;">
    <div class="alert-content">
      <p class="alert-title">Best Practice hàng đầu</p>
      <p class="alert-body" style="font-family:'Fira Code',monospace;font-size:21px;">Hạn chế dùng global, giữ hàm độc lập (pure), truyền tham số &amp; dùng return.</p>
    </div>
  </div>
</div>
"""
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# Run pipeline
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    engine = VoiceDrivenVideoEngine(
        workspace_root=Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material")
    )
    result = engine.build_video_project(
        output_dir=OUTPUT_DIR,
        lesson_slug=LESSON_SLUG,
        lesson_title=LESSON_TITLE,
        scenes=SCENES,
        tts_voice="hung_thinh",
        tts_speed=0.95,
    )
    print(f"\n[DONE] Project built at: {result['output_dir']}")
    print(f"[DONE] Total duration: {result['total_duration']}s")
