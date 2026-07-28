"""
scratch/build_lesson02_s08.py  — v2 (narration + UI revamp)

Cải tiến so với v1:
  - Narration: dẫn dắt hấp dẫn trước khi giải thích, câu chốt cuối scene
  - UI: bỏ border-left accent, bỏ badge thừa, layout thoáng sạch
  - SCRIPT.md ghi vào thư mục Video/SCRIPT.md cho review
"""

import sys, os, json
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent))

from pathlib import Path
from hyperframes.video_pipeline_engine import VoiceDrivenVideoEngine

# ──────────────────────────────────────────────────────────────────────────────
LESSON_SLUG  = "session_08_lesson_02"
LESSON_TITLE = "Tham số và giá trị trả về"
TECH_STACK   = "Python/Core"

BASE = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material"
            r"\output\PM_Python\Session 08 - Hàm (Function) va Phạm vi biến"
            r"\Lesson 02 - Tham số và giá trị trả về\Video")

OUTPUT_DIR   = BASE / LESSON_SLUG
SCRIPT_PATH  = BASE / "SCRIPT.md"

# ──────────────────────────────────────────────────────────────────────────────
# Blueprint: narration dẫn dắt + UI thoáng (no border-left, no badge)
# ──────────────────────────────────────────────────────────────────────────────
SCENES = [
    # ── Scene 01 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_01",
        "scene_title": "Tổng quan bài học",
        "duration": 27.0,
        "narration": (
            "Hãy cùng bắt đầu bài học thứ hai trong Session 8. "
            "Nếu ở bài trước chúng ta đã biết cách khai báo một hàm, "
            "thì hôm nay chúng ta sẽ đi sâu hơn vào hai phần mà bất kỳ hàm nào cũng cần: "
            "tham số — cách chúng ta đưa dữ liệu vào hàm — "
            "và giá trị trả về — cách hàm gửi kết quả trở lại nơi đã gọi nó. "
            "Đây là hai cơ chế làm cho hàm thực sự trở nên linh hoạt và có ích trong dự án thực tế. "
            "Hãy cùng khám phá từng phần một."
        ),
        "clean_content": (
            "Tham số (Parameters) — đưa dữ liệu vào hàm\n"
            "Giá trị trả về (Return) — hàm gửi kết quả ra ngoài\n"
            "Ứng dụng thực tế trong dự án"
        ),
        "html_structure": """
<div class="split-3col" style="height:100%;gap:28px;">
  <div class="card-left" style="display:flex;flex-direction:column;gap:16px;background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:32px 36px;">
    <h2 class="card-title" style="font-size:28px;color:#a5b4fc;font-weight:700;margin:0;">Tham số</h2>
    <p class="card-subtitle" style="color:#94a3b8;font-size:21px;margin:0;">Đưa dữ liệu vào hàm</p>
    <ul class="bullet-list">
      <li>Positional, Keyword, Default</li>
      <li>*args &amp; **kwargs</li>
      <li>Thứ tự kết hợp bắt buộc</li>
    </ul>
  </div>
  <div class="card-left" style="display:flex;flex-direction:column;gap:16px;background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:32px 36px;">
    <h2 class="card-title" style="font-size:28px;color:#6ee7b7;font-weight:700;margin:0;">Giá trị trả về</h2>
    <p class="card-subtitle" style="color:#94a3b8;font-size:21px;margin:0;">Hàm gửi kết quả ra ngoài</p>
    <ul class="bullet-list">
      <li>Câu lệnh return</li>
      <li>Không có return → None</li>
      <li>Trả về nhiều giá trị</li>
    </ul>
  </div>
  <div class="card-left" style="display:flex;flex-direction:column;gap:16px;background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:32px 36px;">
    <h2 class="card-title" style="font-size:28px;color:#fdba74;font-weight:700;margin:0;">Ứng dụng thực tế</h2>
    <p class="card-subtitle" style="color:#94a3b8;font-size:21px;margin:0;">Hàm hoàn chỉnh trong dự án</p>
    <ul class="bullet-list">
      <li>PEP 8 chuẩn doanh nghiệp</li>
      <li>Type hint tự tài liệu hóa</li>
      <li>Best practices chuyên nghiệp</li>
    </ul>
  </div>
</div>
"""
    },
    # ── Scene 02 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_02",
        "scene_title": "Positional Arguments",
        "duration": 28.0,
        "narration": (
            "Hãy cùng tìm hiểu loại tham số đầu tiên và cơ bản nhất — "
            "đó là Positional Argument, hay còn gọi là tham số vị trí. "
            "Đây là một trong những khái niệm vô cùng quan trọng mà mọi lập trình viên Python cần nắm vững. "
            "Nguyên lý hoạt động rất trực quan: Python ghép từng giá trị bạn truyền vào "
            "với từng tham số theo đúng thứ tự từ trái sang phải. "
            "Xem ví dụ bên phải — hàm greet nhận name rồi mới đến age. "
            "Khi gọi greet('An', 25), Python tự động hiểu 'An' là name và 25 là age. "
            "Điều quan trọng cần nhớ: sai thứ tự sẽ dẫn đến sai logic mà Python không báo lỗi."
        ),
        "clean_content": (
            "Ghép giá trị theo thứ tự từ trái sang phải\n"
            "Số lượng argument phải khớp chính xác\n"
            "Sai thứ tự → sai logic, không có lỗi cú pháp"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Cơ chế hoạt động</h2>
    <ul class="bullet-list">
      <li>Ghép theo thứ tự trái → phải</li>
      <li>Số argument phải khớp chính xác</li>
      <li>Sai thứ tự → sai logic (không có lỗi cú pháp)</li>
    </ul>
    <div class="alert-box alert-warning" style="margin-top:auto;">
      <div class="alert-content">
        <p class="alert-title">Lưu ý</p>
        <p class="alert-body" style="font-family:'Fira Code',monospace;font-size:20px;">greet("An", 25) → name="An", age=25</p>
      </div>
    </div>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">greet.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">greet</span>(name, age):
    <span class="fn">print</span>(<span class="str">f"Xin chào {name}, {age} tuổi"</span>)

<span class="cm"># Positional — theo thứ tự khai báo</span>
<span class="fn">greet</span>(<span class="str">"An"</span>, <span class="num">25</span>)
<span class="cm"># Output: Xin chào An, 25 tuổi</span>

<span class="cm"># Nếu đảo thứ tự → sai logic</span>
<span class="fn">greet</span>(<span class="num">25</span>, <span class="str">"An"</span>)
<span class="cm"># Output: Xin chào 25, An tuổi</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 03 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_03",
        "scene_title": "Keyword Arguments",
        "duration": 27.0,
        "narration": (
            "Bây giờ hãy cùng khám phá một cải tiến rất thú vị so với tham số vị trí — "
            "đó là Keyword Argument, hay tham số định danh. "
            "Thay vì phải nhớ thứ tự, bạn chỉ cần ghi rõ tên tham số kèm dấu bằng khi gọi hàm. "
            "Python sẽ tự biết giá trị nào đi với tham số nào, dù bạn viết theo thứ tự nào. "
            "Lợi ích rõ ràng nhất là code trở nên tự giải thích — "
            "nhìn vào lời gọi hàm là biết ngay từng giá trị có ý nghĩa gì. "
            "Trong dự án thực tế, khi hàm có từ ba tham số trở lên, "
            "dùng keyword argument là lựa chọn được khuyến nghị."
        ),
        "clean_content": (
            "Ghi rõ tên tham số khi gọi: name='An'\n"
            "Thứ tự hoàn toàn tự do\n"
            "Code tự giải thích, dễ đọc hơn"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Ưu điểm nổi bật</h2>
    <ul class="bullet-list">
      <li>Ghi rõ tên tham số khi gọi hàm</li>
      <li>Thứ tự hoàn toàn tự do</li>
      <li>Code tự giải thích ý nghĩa</li>
    </ul>
    <div class="alert-box alert-success" style="margin-top:auto;">
      <div class="alert-content">
        <p class="alert-title">Khuyến nghị</p>
        <p class="alert-body">Dùng khi hàm có từ 3 tham số trở lên</p>
      </div>
    </div>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">keyword_args.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">greet</span>(name, age):
    <span class="fn">print</span>(<span class="str">f"Xin chào {name}, {age} tuổi"</span>)

<span class="cm"># Keyword — thứ tự hoàn toàn tự do</span>
<span class="fn">greet</span>(age=<span class="num">25</span>, name=<span class="str">"An"</span>)
<span class="cm"># Output: Xin chào An, 25 tuổi</span>

<span class="cm"># Kết hợp cả hai kiểu</span>
<span class="fn">greet</span>(<span class="str">"An"</span>, age=<span class="num">25</span>)
<span class="cm"># Output: Xin chào An, 25 tuổi</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 04 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_04",
        "scene_title": "Default Arguments",
        "duration": 28.0,
        "narration": (
            "Hãy tưởng tượng bạn đang xây dựng hàm tính thuế cho một hệ thống kế toán. "
            "Hầu hết giao dịch đều dùng thuế suất mặc định mười phần trăm, "
            "chỉ một số ít trường hợp cần thuế suất khác. "
            "Đây chính là lúc Default Argument — tham số mặc định — phát huy giá trị. "
            "Bạn gán sẵn giá trị ngay khi định nghĩa hàm; "
            "nếu người gọi không truyền vào, Python dùng giá trị đó. "
            "Tuy nhiên có một quy tắc sắt: tham số mặc định phải đứng SAU tất cả tham số bắt buộc. "
            "Vi phạm quy tắc này, Python sẽ báo SyntaxError ngay lập tức."
        ),
        "clean_content": (
            "Gán sẵn giá trị khi định nghĩa hàm\n"
            "Không bắt buộc truyền khi gọi\n"
            "Phải đứng SAU tham số bắt buộc — vi phạm gây SyntaxError"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Default Arguments</h2>
    <ul class="bullet-list">
      <li>Gán giá trị sẵn khi định nghĩa</li>
      <li>Không bắt buộc khi gọi hàm</li>
    </ul>
    <div class="alert-box alert-danger" style="margin-top:12px;">
      <div class="alert-content">
        <p class="alert-title">Quy tắc bắt buộc</p>
        <p class="alert-body">Tham số mặc định phải đứng SAU tham số bắt buộc. Vi phạm → SyntaxError.</p>
      </div>
    </div>
    <div class="flow-row" style="margin-top:12px;">
      <div class="flow-node" style="font-size:19px;">price</div>
      <span class="flow-arrow">→</span>
      <div class="flow-node active" style="font-size:19px;">rate=0.1</div>
    </div>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">default_args.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">calculate_tax</span>(price, rate=<span class="num">0.1</span>):
    <span class="kw">return</span> price * rate

<span class="cm"># Dùng giá trị mặc định rate=0.1</span>
<span class="fn">print</span>(<span class="fn">calculate_tax</span>(<span class="num">100</span>))       <span class="cm"># 10.0</span>

<span class="cm"># Ghi đè giá trị mặc định</span>
<span class="fn">print</span>(<span class="fn">calculate_tax</span>(<span class="num">100</span>, <span class="num">0.2</span>))  <span class="cm"># 20.0</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 05 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_05",
        "scene_title": "*args — Tham số vị trí động",
        "duration": 27.0,
        "narration": (
            "Hãy đặt ra một câu hỏi thú vị: điều gì xảy ra nếu bạn muốn viết một hàm "
            "nhưng không biết trước người dùng sẽ truyền vào bao nhiêu giá trị? "
            "Đây chính là bài toán mà star args giải quyết một cách thanh lịch. "
            "Viết dấu sao trước tên tham số, Python sẽ tự động gom tất cả giá trị positional "
            "thành một tuple để bạn dễ dàng duyệt qua. "
            "Nhìn vào hàm sum_all bên phải — dù bạn truyền ba hay một trăm số, "
            "hàm vẫn hoạt động hoàn hảo. "
            "Pattern này cực kỳ phổ biến trong các utility function, logging, và decorator."
        ),
        "clean_content": (
            "Dấu * gom tất cả positional arguments thành tuple\n"
            "Số lượng argument hoàn toàn linh hoạt\n"
            "Phổ biến trong utility, logging, decorator"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Cơ chế *args</h2>
    <p class="desc-text" style="font-size:24px;color:#94a3b8;">Gom toàn bộ positional arguments vào một <span style="color:#fdba74;font-family:'Fira Code',monospace;">tuple</span></p>
    <ul class="bullet-list">
      <li>Số lượng argument linh hoạt</li>
      <li>Kết quả là tuple có thể duyệt</li>
      <li>Dùng trong utility, logging, decorator</li>
    </ul>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">args_demo.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">sum_all</span>(*args):
    total = <span class="num">0</span>
    <span class="kw">for</span> n <span class="kw">in</span> args:
        total += n
    <span class="kw">return</span> total

<span class="fn">print</span>(<span class="fn">sum_all</span>(<span class="num">1</span>, <span class="num">2</span>, <span class="num">3</span>))          <span class="cm"># 6</span>
<span class="fn">print</span>(<span class="fn">sum_all</span>(<span class="num">10</span>, <span class="num">20</span>, <span class="num">30</span>, <span class="num">40</span>))  <span class="cm"># 100</span>
<span class="fn">print</span>(<span class="fn">sum_all</span>())                <span class="cm"># 0</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 06 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_06",
        "scene_title": "**kwargs — Tham số từ khóa động",
        "duration": 28.0,
        "narration": (
            "Tiếp nối từ star args, hãy cùng khám phá người anh em song sinh của nó — "
            "double star kwargs. "
            "Nếu star args gom positional arguments thành tuple, "
            "thì double star kwargs gom tất cả keyword arguments thành một dictionary. "
            "Điều này cực kỳ mạnh mẽ khi bạn cần xây dựng hàm nhận cấu hình động. "
            "Bạn sẽ gặp pattern này ở khắp nơi trong các framework lớn — "
            "Django, Flask, FastAPI đều dùng kwargs để xây dựng API nhận payload JSON linh hoạt. "
            "Nắm vững kwargs sẽ giúp bạn đọc hiểu và viết được framework-level code."
        ),
        "clean_content": (
            "Dấu ** gom tất cả keyword arguments thành dict\n"
            "Linh hoạt với cấu hình động\n"
            "Nền tảng của Django, Flask, FastAPI"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Cơ chế **kwargs</h2>
    <p class="desc-text" style="font-size:24px;color:#94a3b8;">Gom toàn bộ keyword arguments vào một <span style="color:#fdba74;font-family:'Fira Code',monospace;">dict</span></p>
    <ul class="bullet-list">
      <li>key = tên tham số, value = giá trị</li>
      <li>Số lượng linh hoạt, thứ tự tự do</li>
      <li>Nền tảng: Django, Flask, FastAPI</li>
    </ul>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">kwargs_demo.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">build_profile</span>(**kwargs):
    <span class="kw">for</span> key, value <span class="kw">in</span> kwargs.<span class="fn">items</span>():
        <span class="fn">print</span>(<span class="str">f"{key}: {value}"</span>)

<span class="fn">build_profile</span>(
    name=<span class="str">"An"</span>,
    age=<span class="num">25</span>,
    role=<span class="str">"Developer"</span>
)
<span class="cm"># name: An</span>
<span class="cm"># age: 25</span>
<span class="cm"># role: Developer</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 07 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_07",
        "scene_title": "Thứ tự kết hợp tham số",
        "duration": 27.0,
        "narration": (
            "Đến đây bạn đã biết bốn loại tham số. "
            "Câu hỏi tự nhiên xuất hiện là: khi cần dùng nhiều loại trong cùng một hàm, "
            "thì thứ tự chúng phải viết như thế nào? "
            "Python có quy định rất rõ ràng và bắt buộc bạn phải tuân theo. "
            "Đầu tiên là tham số bắt buộc, tiếp đến là tham số mặc định, "
            "rồi star args gom positional động, sau đó là keyword-only, "
            "và cuối cùng là double star kwargs. "
            "Đây không phải quy ước — vi phạm thứ tự này Python sẽ báo SyntaxError ngay khi đọc file. "
            "Hãy nhớ kỹ thứ tự này, nó sẽ theo bạn suốt sự nghiệp lập trình Python."
        ),
        "clean_content": (
            "1. Tham số bắt buộc\n"
            "2. Tham số mặc định\n"
            "3. *args\n"
            "4. Keyword-only\n"
            "5. **kwargs"
        ),
        "html_structure": """
<div class="card-full" style="height:100%;background:#13131f;border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:36px 44px;">
  <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0 0 28px 0;">Thứ tự kết hợp bắt buộc trong Python</h2>
  <ol class="step-list">
    <li><span class="step-num">1</span><span>Tham số bắt buộc <span style="color:#94a3b8;margin-left:8px;font-family:'Fira Code',monospace;">(positional)</span></span></li>
    <li><span class="step-num">2</span><span>Tham số mặc định <span style="color:#94a3b8;margin-left:8px;font-family:'Fira Code',monospace;">(default=value)</span></span></li>
    <li><span class="step-num">3</span><span>Variadic positional <span style="color:#fdba74;margin-left:8px;font-family:'Fira Code',monospace;">*args</span></span></li>
    <li><span class="step-num">4</span><span>Keyword-only parameters</span></li>
    <li><span class="step-num">5</span><span>Variadic keyword <span style="color:#fdba74;margin-left:8px;font-family:'Fira Code',monospace;">**kwargs</span></span></li>
  </ol>
  <div class="alert-box alert-info" style="margin-top:28px;">
    <div class="alert-content">
      <p class="alert-title">Ví dụ kết hợp đúng</p>
      <p class="alert-body" style="font-family:'Fira Code',monospace;font-size:21px;">def fn(a, b=1, *args, kw, **kwargs): ...</p>
    </div>
  </div>
</div>
"""
    },
    # ── Scene 08 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_08",
        "scene_title": "Câu lệnh return",
        "duration": 27.0,
        "narration": (
            "Hãy cùng chuyển sang phần thứ hai của bài học — giá trị trả về. "
            "Cho đến giờ các hàm của chúng ta mới chỉ in ra màn hình. "
            "Nhưng trong thực tế, bạn thường muốn hàm tính toán một kết quả "
            "để dùng tiếp trong logic chương trình. "
            "Đây là lúc câu lệnh return xuất hiện. "
            "Return kết thúc hàm ngay lập tức và gửi giá trị trở về nơi gọi. "
            "Một hàm có thể có nhiều return ở nhiều nhánh điều kiện — "
            "Python dừng tại return đầu tiên được thực thi. "
            "Nếu không viết return, hàm tự động trả về None."
        ),
        "clean_content": (
            "return kết thúc hàm và trả giá trị về\n"
            "Nhiều return ở các nhánh điều kiện khác nhau\n"
            "Không có return → tự động trả về None"
        ),
        "html_structure": """
<div class="split-container" style="height:100%;gap:28px;">
  <div style="display:flex;flex-direction:column;gap:20px;">
    <h2 class="card-title" style="font-size:30px;color:#e2e8f0;font-weight:700;margin:0;">Cơ chế return</h2>
    <ul class="bullet-list">
      <li>Kết thúc hàm ngay lập tức</li>
      <li>Trả về bất kỳ kiểu dữ liệu</li>
      <li>Nhiều return trong nhánh điều kiện</li>
    </ul>
    <div class="alert-box alert-warning" style="margin-top:auto;">
      <div class="alert-content">
        <p class="alert-title">Cần nhớ</p>
        <p class="alert-body">Không có <span style="font-family:'Fira Code',monospace;">return</span> → hàm trả về <span style="font-family:'Fira Code',monospace;color:#fdba74;">None</span></p>
      </div>
    </div>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">return_demo.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">check_age</span>(age):
    <span class="kw">if</span> age &lt; <span class="num">0</span>:
        <span class="kw">return</span> <span class="str">"Tuổi không hợp lệ"</span>
    <span class="kw">if</span> age &lt; <span class="num">18</span>:
        <span class="kw">return</span> <span class="str">"Vị thành niên"</span>
    <span class="kw">return</span> <span class="str">"Người trưởng thành"</span>

<span class="fn">print</span>(<span class="fn">check_age</span>(<span class="num">25</span>)) <span class="cm"># Người trưởng thành</span>
<span class="fn">print</span>(<span class="fn">check_age</span>(<span class="num">10</span>)) <span class="cm"># Vị thành niên</span>
<span class="fn">print</span>(<span class="fn">check_age</span>(-<span class="num">1</span>)) <span class="cm"># Tuổi không hợp lệ</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 09 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_09",
        "scene_title": "Trả về nhiều giá trị",
        "duration": 28.0,
        "narration": (
            "Một trong những tính năng đặc biệt của Python mà nhiều ngôn ngữ khác không có "
            "đó là khả năng trả về nhiều giá trị từ một hàm duy nhất. "
            "Bí quyết ở đây là Python tự động đóng gói chúng vào một tuple. "
            "Và với tuple unpacking, bạn có thể nhận từng giá trị vào biến riêng biệt "
            "chỉ với một dòng code. "
            "Xem hai ví dụ bên phải — hàm divide trả về cả thương và phần dư cùng lúc, "
            "hàm min_max trả về cả giá trị nhỏ nhất và lớn nhất. "
            "Pattern này giúp code súc tích và biểu đạt ý tưởng tự nhiên hơn nhiều."
        ),
        "clean_content": (
            "Python tự đóng gói nhiều giá trị thành tuple\n"
            "Tuple unpacking nhận từng biến một dòng\n"
            "Pattern súc tích, tự nhiên"
        ),
        "html_structure": """
<div class="split-equal" style="height:100%;gap:28px;">
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">divmod_custom.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">divide</span>(a, b):
    quotient  = a // b
    remainder = a % b
    <span class="kw">return</span> quotient, remainder

<span class="cm"># Tuple unpacking</span>
q, r = <span class="fn">divide</span>(<span class="num">17</span>, <span class="num">5</span>)
<span class="fn">print</span>(<span class="str">f"Thương: {q}, Dư: {r}"</span>)
<span class="cm"># Thương: 3, Dư: 2</span></code></pre>
  </div>
  <div class="code-panel-right">
    <div class="code-header-bar">
      <div class="mac-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div>
      <span class="code-filename">min_max.py</span>
    </div>
    <pre class="code-body"><code><span class="kw">def</span> <span class="fn">min_max</span>(numbers):
    <span class="kw">return</span> <span class="fn">min</span>(numbers), <span class="fn">max</span>(numbers)

<span class="cm"># Nhận hai giá trị cùng lúc</span>
low, high = <span class="fn">min_max</span>([<span class="num">3</span>, <span class="num">1</span>, <span class="num">9</span>, <span class="num">5</span>, <span class="num">2</span>])
<span class="fn">print</span>(<span class="str">f"Min: {low}, Max: {high}"</span>)
<span class="cm"># Min: 1, Max: 9</span></code></pre>
  </div>
</div>
"""
    },
    # ── Scene 10 ─────────────────────────────────────────────────────────────
    {
        "scene_id": "Scene_10",
        "scene_title": "Tổng kết & Best Practices",
        "duration": 27.0,
        "narration": (
            "Chúng ta đã đi qua toàn bộ hệ thống tham số và giá trị trả về của Python. "
            "Hãy cùng chốt lại những điểm quan trọng nhất. "
            "Bốn loại tham số: positional theo thứ tự, keyword theo tên, "
            "default có giá trị sẵn, và variadic args kwargs cho số lượng linh hoạt. "
            "Return kết thúc hàm và trả giá trị — không có return thì trả None. "
            "Python cho phép trả về nhiều giá trị qua tuple unpacking. "
            "Và best practice quan trọng nhất: hãy dùng type hint "
            "để code tự tài liệu hóa và IDE hỗ trợ tốt hơn nhiều. "
            "Đây là nền tảng vững chắc để bạn viết hàm chuyên nghiệp."
        ),
        "clean_content": (
            "4 loại tham số: positional, keyword, default, variadic\n"
            "return trả giá trị — không có return → None\n"
            "Type hint: def fn(x: int) -> str"
        ),
        "html_structure": """
<div style="height:100%;display:flex;flex-direction:column;gap:24px;">
  <div class="split-equal" style="flex:1;gap:24px;">
    <div style="display:flex;flex-direction:column;gap:16px;">
      <div class="alert-box alert-info">
        <div class="alert-content">
          <p class="alert-title" style="font-size:22px;">Positional</p>
          <p class="alert-body" style="font-size:19px;">Theo thứ tự khai báo, bắt buộc truyền</p>
        </div>
      </div>
      <div class="alert-box alert-success">
        <div class="alert-content">
          <p class="alert-title" style="font-size:22px;">Keyword</p>
          <p class="alert-body" style="font-size:19px;">Gọi theo tên, thứ tự tự do</p>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:16px;">
      <div class="alert-box alert-warning">
        <div class="alert-content">
          <p class="alert-title" style="font-size:22px;">Default</p>
          <p class="alert-body" style="font-size:19px;">Giá trị dự phòng, không bắt buộc truyền</p>
        </div>
      </div>
      <div class="alert-box alert-danger">
        <div class="alert-content">
          <p class="alert-title" style="font-size:22px;">*args / **kwargs</p>
          <p class="alert-body" style="font-size:19px;">Thu thập động không giới hạn</p>
        </div>
      </div>
    </div>
  </div>
  <div class="alert-box alert-info" style="margin-top:0;">
    <div class="alert-content">
      <p class="alert-title">Type Hint — best practice chuyên nghiệp</p>
      <p class="alert-body" style="font-family:'Fira Code',monospace;font-size:22px;">def calculate(x: int, rate: float = 0.1) -&gt; float: ...</p>
    </div>
  </div>
</div>
"""
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# Ghi SCRIPT.md để review
# ──────────────────────────────────────────────────────────────────────────────
def write_script_md():
    lines = [
        "# Kịch Bản Video — Session 08 Lesson 02",
        "## Tham số và giá trị trả về",
        "",
        "> **Tech stack:** Python/Core | **Lesson slug:** `session_08_lesson_02`",
        "",
        "---",
        "",
    ]
    for sc in SCENES:
        lines += [
            f"## {sc['scene_id']} — {sc['scene_title']}",
            "",
            "### Giọng đọc (TTS):",
            f"> {sc['narration']}",
            "",
            "### Nội dung UI (màn hình):",
            "```",
            sc['clean_content'],
            "```",
            "",
            "---",
            "",
        ]
    SCRIPT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[SCRIPT] SCRIPT.md written to {SCRIPT_PATH}")


# ──────────────────────────────────────────────────────────────────────────────
# Run pipeline
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    write_script_md()

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
