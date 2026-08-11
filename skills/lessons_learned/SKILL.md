---
name: lessons_learned
description: System Reflection Memory Store containing consolidated technical guardrails, gotchas, and error-prevention directives derived from prior AI Agent iterations and Reviewer feedback logs. Target output language is 100% Accented Vietnamese.
---

# Lessons Learned & Technical Guardrails Memory Store — Rikkei Education Standards

This file serves as the system's **Long-Term Reflection Memory Store**. All AI Agents MUST read these accumulated technical guardrails before generating or reviewing learning materials to prevent regression and avoid repeating past technical mistakes.

---

## 1. Operating System & Environment Guardrails

- **[WINDOWS UTF-8 ENCODING]**:
  - Always reconfigure standard I/O encoding when processing Vietnamese text on Windows:
    ```python
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    ```
  - Prevents `UnicodeEncodeError` crashes caused by default Windows `CP1252` encoding.
  - Set `PYTHONIOENCODING=utf-8` environment variable for subprocess executions.

- **[VIRTUAL ENVIRONMENT DETECTION]**:
  - Use `sys.prefix != sys.base_prefix` to detect active virtual environment (`venv`) status accurately.

---

## 2. Python Core & Language Gotchas

- **[MUTABLE DEFAULT ARGUMENTS]**:
  - FORBIDDEN to define functions with mutable default arguments (`def func(lst=[])`). Use `def func(lst=None)` with `if lst is None: lst = []`.

- **[MULTILINE STRING LITERALS]**:
  - Always use triple quotes (`"""` or `'''`) for multiline strings instead of trailing backslashes `\` to avoid `SyntaxError: unterminated string literal`.

- **[JSON CODE EXTRACTION & PARSING]**:
  - When extracting Python code snippets from JSON fields, ALWAYS use proper JSON parsers (`json.loads`) or regex filters to strip trailing delimiters (e.g. `",` at end of lines) that cause `SyntaxError: unterminated string literal`.

- **[SHORT-CIRCUIT EVALUATION TRAPS]**:
  - In boolean expression quizzes (`and`, `or`), ensure zero-division risk expressions (`10 / x`) are guarded properly (`x != 0 and (10 / x > 1)`).

---

## 3. Web Frameworks & Database ORM (Backend APIs & Data Persistence)

- **[TRANSACTION ROLLBACK ON INTEGRITY ERROR]**:
  - When catching database exceptions in Web APIs, ALWAYS execute `db.rollback()` inside database `IntegrityError` / transaction exception handlers before returning error responses to release failed transactions.

- **[DEPENDENCY INJECTION & ASYNC SESSIONS]**:
  - In web frameworks, always inject database sessions properly using dependencies or context managers (`db: AsyncSession = Depends(get_db)`).

- **[PYDANTIC SCHEMA VALIDATION]**:
  - Input schema fields representing lists MUST declare validation bounds (e.g. `Field(..., min_items=1)` for quiz items).
  - Practical lab schemas MUST define explicit sub-schemas for `objectives`, `steps`, and `checklist`.

- **[STRICT SCOPE BOUNDARY CONTROL]**:
  - FORBIDDEN to introduce future framework/ORM concepts (`APIRouter`, `SQLAlchemy`, `FastAPI`, `Pydantic`) inside foundational `python/core` lessons.

---

## 4. Interactive DOM Visualizers & Wasm Sandbox

- **[NON-BLOCKING WASM EXECUTIONS]**:
  - CLI lessons containing `input()` MUST use mock datasets or input stubs (`unittest.mock.patch`) in testing environments to prevent `TimeoutExpired` sandbox freezes.

- **[DOM ELEMENT ID SYNCHRONIZATION]**:
  - HTML container IDs (`id="custom-input"`) MUST strictly match JavaScript dereferencing selectors (`document.getElementById("custom-input")`).

- **[RAW OPERATORS IN CONSOLE LOGS]**:
  - When logging to terminal visualizers via `innerText`, pass raw boolean string operators (e.g. `&&`) rather than HTML entities (`&amp;&amp;`).

- **[COPY BUTTON EVENT BINDING]**:
  - Sync function signature `copyCode(button, codeId)` 1-to-1 with element attributes `onclick="copyCode(this, 'id')"` to prevent `TypeError`.

---

## 5. HyperFrames Video & GSAP Animations

- **[INITIAL GSAP TIMELINE INITIALIZATION]**:
  - Every GSAP scene timeline MUST initialize visibility at timestamp 0:
    ```javascript
    tl.set(".clip", { autoAlpha: 1 }, 0);
    ```

- **[MINIMUM 3-STEP ANIMATION SEQUENCE]**:
  - Each scene animation timeline MUST include at least 3 sequential steps:
    1. Clip visibility initialization (`autoAlpha: 1`)
    2. Intro title reveal
    3. Main content breakdown & highlights

- **[SCENE & TTS SCRIPT SYNCHRONIZATION]**:
  - `scene_id` array keys MUST match 1-to-1 between visual `scenes` and audio `tts_scripts`.
  - Cumulative `start_at_root` timestamps MUST equal the sum of durations of all preceding scenes.

---

## 6. Markmap Mindmaps & Design Formatting

- **[BILINGUAL HEADING TRANSLATION]**:
  - Convert internal snake_case keys into natural Accented Vietnamese for all Markdown H2/H3 mindmap headings.

- **[STRICT TEXT EMOJI PROHIBITION]**:
  - 100% FORBIDDEN to render text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶).
  - Use vector Phosphor Icons `<i class="ph-bold ph-*"></i>` or standardized text badges (`[NOTE]`, `[TIP]`, `[WARNING]`).

- **[SYNTAX FENCE INTEGRITY]**:
  - Ensure all Markmap Markdown codeblocks (` ```markmap `) close cleanly without dangling backticks.

- **[COLLAPSIBLE HTML DETAILS]**:
  - Wrap extended supplementary code snippets inside `<details><summary>...</summary>...</details>` blocks with custom WCAG accessible styling.
* **[PYTHON/CORE]**: Khi thiết kế bài học thực hành cấu trúc điều khiển (Is Theory/Diagram Only Lesson = False), luôn sử dụng các động từ Bloom đo lường được (như giải thích được, trình bày được, sử dụng được) trong chuẩn đầu ra, loại bỏ rác hệ thống và tích hợp đầy đủ visualizer-canvas mô phỏng trạng thái biến lặp, bảng điều khiển từng bước (Start, Pause, Step, Reset) cùng Code Tracker có highlight lớp active-line đồng bộ. | Source: [[Lesson 01 - Khái niệm vòng lặp và câu lệnh for]]
* **[PYTHON/CORE]**: Khi thiết kế ví dụ mã nguồn cho bài học vòng lặp while cơ bản, chỉ điều khiển chu kỳ lặp bằng cách cập nhật biến kiểm soát trong thân vòng lặp và không sử dụng các câu lệnh ngắt lặp vượt cấp như break hoặc continue. | Source: [[Lesson 02 - Vòng lặp while và lặp theo điều kiện]]
* **[PYTHON/CORE]**: Khi thiết kế bài đọc và giao diện minh họa cho bài học Tổng quan Python 3.12, không sử dụng cấu trúc rẽ nhánh (if-elif-else, isinstance) thuộc phạm vi cấm và bắt buộc áp dụng giao diện Light Mode cho khung console (#viz-console), tuyệt đối không dùng các class nền tối như bg-slate-900. | Source: [[Lesson 01 - Tổng quan về ngôn ngữ Python 3.12]]
* **[PYTHON/CORE]**: Khi tạo nội dung bài đọc Lesson 02, phải đảm bảo cấu trúc đủ 5 phần (`section-1` đến `section-5`) đạt tối thiểu 500 ký tự và chỉ sử dụng các lệnh CLI Terminal (`python -m venv`, `source`, `pip install`, `which`), tuyệt đối không sử dụng hàm (`def`), vòng lặp (`for`/`while`), câu điều kiện (`if`/`else`) hoặc cấu trúc dữ liệu (`list`/`dict`) trong mã minh họa. | Source: [[Lesson 02 - Thiết lập môi trường làm việc và công cụ hỗ trợ AI]]
* **[PYTHON/CORE]**: Khi khởi tạo bài đọc thực hành, phải xây dựng đầy đủ 5 Section theo đúng ID từ section-1 đến section-5 với độ dài tối thiểu 500 ký tự, đồng thời nhúng khối HTML Interactive Web Visualizer chuẩn gồm Visualizer Canvas, bộ nút điều khiển (▶ Bắt đầu / ⏸ Tạm dừng / ⏭ Từng bước / ↻ Đặt lại) và Code Tracker chứa CSS class active-line đúng cú pháp HTML để đồng bộ dòng thực thi. | Source: [[Lesson 03 - Khởi tạo và thực thi chương trình Python đầu tiên]]
* **[PYTHON/CORE]**: Khi khởi tạo tài liệu bài đọc, phải tuân thủ cấu trúc 5 phần cố định chứa đầy đủ các thẻ định danh section-1, section-2, section-3, section-4, section-5 và đảm bảo tổng độ dài văn bản đạt tối thiểu 500 ký tự để vượt qua Master Validator. | Source: [[Lesson 04 - Khai báo biến, quy tắc đặt tên và các kiểu dữ liệu cơ sở]]
* **[PYTHON/CORE]**: Khi tạo nội dung bài đọc HTML/Markdown, phải cấu trúc đầy đủ 5 Section cố định có ID từ section-1 đến section-5 với độ dài trên 500 ký tự, tuyệt đối không dùng emoji hoặc ký tự mũi tên Unicode như '➔' mà phải thay bằng nhãn [NOTE], [TIP], [WARNING] hoặc thẻ Phosphor Icons <i class='ph-...'>. | Source: [[Lesson 05 - Thao tác nhập xuất dữ liệu console và chuyển đổi kiểu dữ liệu]]
* **[GIT 2.45+, GITHUB CLOUD, GIT BASH, VS CODE SOURCE CONTROL]**: Khi soạn thảo bài học "Giới thiệu VCS", tuyệt đối không đưa các lệnh thực hành CLI (`git config`, `git init`, `git add`, `git commit`, `git remote`, `git push`) vào nội dung, đồng thời phải gắn đúng nhãn ngôn ngữ `bash`/`shell` cho khối mã lệnh và đảm bảo đóng đầy đủ, chính xác cú pháp thẻ SVG trong khối HTML. | Source: [[Lesson 01 - Giới thiệu Hệ thống quản lý phiên bản VCS]]
* **[GIT 2.45+, GITHUB CLOUD, GIT BASH, VS CODE SOURCE CONTROL]**: Khi sinh nội dung bài đọc và giao diện tương tác Git, phải dùng nhãn "Mã lệnh Git Bash" kèm class `language-bash`, gán class `active-line` cho dòng Code Tracker đang chạy, sử dụng đúng bộ nút điều khiển (`▶ Bắt đầu / ⏸ Tạm dừng / ⏭ Từng bước / ↻ Đặt lại`), đảm bảo tương phản Light Mode (không phối màu `bg-slate-900` với `text-slate-700`), và thay thế toàn bộ emoji văn bản bằng thẻ Phosphor Icons `<i class='ph-...'>` hoặc các nhãn `[NOTE]`, `[TIP]`, `[WARNING]`. | Source: [[Lesson 02 - Kiến trúc 3 cây của Git]]
* **[GIT 2.45+, GITHUB CLOUD, GIT BASH, VS CODE SOURCE CONTROL]**: Khi thiết kế bài đọc Git Bash, hàm `runVizStep` phải mô phỏng chính xác vòng đời tập tin (`Untracked`, `Staged`, `Unmodified`, `Modified`) kết hợp cập nhật class `active-line` trên các phần tử `viz-line-*`, loại bỏ hoàn toàn thư viện `pyodide.js` và hàm `runPythonCode`, gán đúng nhãn syntax `bash` hoặc `shell` cho khối lệnh Git, đảm bảo 100% Tiếng Việt có dấu và thay thế ký tự cấm `➔` bằng Phosphor Icons `<i class='ph-...'>` hoặc các nhãn `[NOTE]`, `[TIP]`, `[WARNING]`. | Source: [[Lesson 03 - Vòng đời file trong Git]]
* **[GIT 2.45+, GITHUB CLOUD, GIT BASH, VS CODE SOURCE CONTROL]**: Khi soạn thảo bài học về Git/CLI, bắt buộc gắn nhãn syntax highlight `language-bash` (tuyệt đối không dùng `language-c`), loại bỏ hoàn toàn các script runtime không thuộc scope như Pyodide (`pyodide.js`), đóng đầy đủ cặp thẻ `<pre><code>` và tuyệt đối không sử dụng các class Tailwind nền tối (`bg-slate-900`, `bg-black`) để bảo đảm chuẩn Light Mode. | Source: [[Lesson 04 - Cài đặt và cấu hình Git]]
* **[GIT 2.45+, GITHUB CLOUD, GIT BASH, VS CODE SOURCE CONTROL]**: Khi trình bày các câu lệnh Git Bash/CLI, bắt buộc khai báo thẻ mã nguồn với class `language-bash` (hoặc `language-shell`), không lặp thuộc tính `class` trong thẻ HTML và đảm bảo khung `#viz-console` sử dụng cặp màu nền/chữ đáp ứng chuẩn độ tương phản Light Mode. | Source: [[Lesson 05 - Chu trình lưu vết cốt lõi]]
* **[GIT 2.45+, GITHUB CLOUD, GIT BASH, VS CODE SOURCE CONTROL]**: Khi biên soạn bài đọc Git/GitHub Cloud, phải gắn nhãn chính xác thẻ `<code class="language-bash">` cho các câu lệnh CLI (thay vì `language-c`), tích hợp đầy đủ hướng dẫn cho cả Git Bash lẫn VS Code Source Control Panel, hoàn thiện trọn bộ 3 thành phần Visualizer (Canvas mô phỏng dịch chuyển commit, Bảng State Tracker, Terminal Console Log) và loại bỏ hoàn toàn các lớp phủ tối màu như `bg-slate-900/60`. | Source: [[Lesson 06 - Liên kết Remote và Push code]]
* **[GIT 2.45+, GITHUB CLOUD, GIT BASH, VS CODE SOURCE CONTROL]**: Khi thiết kế bài đọc về Git CLI, bắt buộc gán đúng nhãn Terminal/Bash với thẻ class `language-bash` hoặc `language-shell`, loại bỏ hoàn toàn thư viện `pyodide.js`, đồng bộ logic hàm `runVizStep()` phản ánh đúng trạng thái câu lệnh Git và thay thế toàn bộ ký tự emoji/unicode (như '➔') bằng thẻ Phosphor Icons `<i class='ph-...'>` hoặc các nhãn `[NOTE]`, `[TIP]`, `[WARNING]`. | Source: [[Lesson 01 - Thực hành tổng hợp - Luyện tập chu trình GIT cơ bản]]
* **[DEVOPS/DOCKER]**: Khi chèn hình ảnh bằng thẻ <img> trong bài giảng, luôn phải thêm chú thích ngay bên dưới bằng thẻ <i>...</i> hoặc <figcaption>...</figcaption>, đồng thời đảm bảo cấu trúc Blueprint JSON trong kịch bản video không rỗng và hợp lệ về cú pháp. | Source: [[Lesson 02 - Các lệnh thao tác với nhánh]]
* **[DEVOPS/DOCKER]**: Khi khởi tạo nội dung bài đọc HTML, bắt buộc phải phân chia đủ 5 phần với các ID định danh từ `section-1` đến `section-5`, đảm bảo tổng độ dài tối thiểu 500 ký tự và mọi thẻ `<img>` phải có chú thích bằng thẻ `<i>...</i>` hoặc `<figcaption>` nằm trực tiếp phía dưới. | Source: [[Lesson 01 - Tư duy phân nhánh trong phát triển phần mềm]]
* **[DEVOPS/DOCKER]**: Khi chèn hình ảnh minh họa bằng thẻ `<img>` trong nội dung bài học, bắt buộc phải đặt ngay bên dưới thẻ chú thích `<i>...</i>` hoặc `<figcaption>...</figcaption>` và xuất đầy đủ nội dung cấu trúc Blueprint JSON hợp lệ. | Source: [[Lesson 03 - Nguyên lý Trộn mã nguồn (Merging)]]
* **[DEVOPS/DOCKER]**: Khi chèn hình ảnh minh họa bằng thẻ <img> trong bài giảng, luôn phải thêm chú thích ảnh nằm ngay bên dưới bằng thẻ <i>...</i> hoặc thẻ <figcaption> để đảm bảo đúng quy chuẩn hiển thị và vượt qua bộ kiểm định tự động. | Source: [[Lesson 03 - Quy trình Pull Request và Code Review chuẩn doanh nghiệp]]
* **[DEVOPS/DOCKER]**: Khi chèn hình ảnh minh họa bằng thẻ <img> trong nội dung bài học, bắt buộc phải thêm chú thích hình ảnh nằm trực tiếp ngay bên dưới bằng thẻ <i>...</i> hoặc <figcaption>...</figcaption>. | Source: [[Lesson 01 - Quy trình phối hợp nhóm Fork, Clone, Fetch, Pull]]
* **[DEVOPS/DOCKER]**: Khi chèn các thẻ HTML vào nội dung bài giảng, luôn bọc thẻ `<table>` bên trong thẻ `<div>` có class `overflow-x-auto` để đảm bảo hiển thị đáp ứng (responsive) trên thiết bị di động, đồng thời bắt buộc bổ sung chú thích minh họa ngay bên dưới thẻ `<img>` bằng thẻ `<figcaption>` hoặc `<i>...</i>`. | Source: [[Lesson 02 - Nguyên nhân và kỹ thuật xử lý Merge Conflict]]
* **[DEVOPS/DOCKER]**: Khi khởi tạo bài đọc cho bài học, bắt buộc phải đảm bảo độ dài tối thiểu 500 ký tự, cấu trúc đủ 5 phần cố định với các ID từ section-1 đến section-5, đồng thời luôn đặt thẻ chú thích <i>...</i> hoặc <figcaption> ngay trực tiếp phía dưới mỗi thẻ <img>. | Source: [[Lesson 02 - Chuẩn Conventional Commits và AI IDE hỗ trợ]]
* **[DEVOPS/DOCKER]**: Khi khởi tạo nội dung bài đọc và Video Script, bắt buộc cấu trúc đủ 5 phần với ID từ `section-1` đến `section-5` (đạt tối thiểu 500 ký tự), đính kèm thẻ `<i>` hoặc `<figcaption>` ngay sau thẻ `<img>`, và đảm bảo trả về cấu trúc Blueprint JSON hợp lệ không được để rỗng. | Source: [[Lesson 03 - Nhật ký Git, Tạm cất code và Hoàn tác mã nguồn]]
* **[DEVOPS/DOCKER]**: Khi chèn thẻ HTML `<img>` để hiển thị hình ảnh minh họa trong nội dung bài học, bắt buộc phải đặt ngay bên dưới một thẻ chú thích `<i>...</i>` hoặc `<figcaption>...</figcaption>` tương ứng. | Source: [[Lesson 01 - Bảo mật kho lưu trữ với .gitignore]]
* **[GIT CLI 2.45+, GITHUB CLOUD (CONVENTIONAL COMMITS, GIT FLOW, SEMANTIC BRANCHING)]**: Khi chèn thẻ <img> trong nội dung bài học, luôn thêm thẻ chú thích <i>...</i> hoặc <figcaption> ngay trực tiếp bên dưới thẻ <img> để vượt qua kiểm định tự động Master Validator. | Source: [[Lesson 02 - Phương pháp học tập hiệu quả]]
* **[GIT CLI 2.45+, GITHUB CLOUD (CONVENTIONAL COMMITS, GIT FLOW, SEMANTIC BRANCHING)]**: Khi khởi tạo bài đọc và kịch bản học liệu, phải cấu hình chuẩn 5 Section mang đúng ID từ `section-1` đến `section-5` với độ dài tối thiểu 500 ký tự, bắt buộc kèm thẻ `<i>` hoặc `<figcaption>` ngay dưới thẻ `<img>`, sử dụng động từ Bloom đo lường được (như Xây dựng, Lập kế hoạch, Mô phỏng) và đảm bảo cấu trúc Blueprint JSON hợp lệ không rỗng. | Source: [[Lesson 03 - Demo sản phẩm thực tế & Kỳ vọng đầu ra]]
* **[GIT CLI 2.45+, GITHUB CLOUD (CONVENTIONAL COMMITS, GIT FLOW, SEMANTIC BRANCHING)]**: Khi chèn thẻ <img> trong nội dung bài học, bắt buộc phải đặt thẻ chú thích <i>...</i> hoặc <figcaption> trực tiếp ngay bên dưới hình ảnh để vượt qua bộ kiểm định Master Validator. | Source: [[Lesson 01 - Tổng quan nội dung & Lộ trình môn học]]
* **[GIT CLI 2.45+, GITHUB CLOUD (CONVENTIONAL COMMITS, GIT FLOW, SEMANTIC BRANCHING)]**: Khi khởi tạo nội dung bài đọc và kịch bản bài học, bắt buộc cấu trúc đủ 5 phần chứa ID từ `section-1` đến `section-5` với độ dài tối thiểu 500 ký tự, mọi thẻ `<img>` phải có chú thích `<i>` hoặc `<figcaption>` trực tiếp bên dưới, tuyệt đối không dùng emoji chữ mà thay bằng Phosphor Icons `<i class='ph-...'>` hoặc các nhãn `[NOTE]`/`[TIP]`/`[WARNING]`, và kịch bản video phải xuất dữ liệu Blueprint JSON hợp lệ không rỗng. | Source: [[Lesson 03 - Khởi tạo kho chứa & Kiến trúc 3 vùng dữ liệu]]
* **[GIT CLI 2.45+, GITHUB CLOUD (CONVENTIONAL COMMITS, GIT FLOW, SEMANTIC BRANCHING)]**: Khi chèn thẻ `<img>` và `<table>` trong nội dung bài giảng HTML, luôn bổ sung chú thích ngay bên dưới `<img>` bằng thẻ `<i>...</i>` hoặc `<figcaption>`, đồng thời bọc thẻ `<table>` trong thẻ `<div class="overflow-x-auto">` để tránh lỗi vỡ giao diện trên di động. | Source: [[Lesson 04 - Quản lý vùng chờ Staging & Tập tin loại trừ .gitignore cho dự án Web framework]]
* **[GIT CLI 2.45+, GITHUB CLOUD (CONVENTIONAL COMMITS, GIT FLOW, SEMANTIC BRANCHING)]**: Khi xuất cấu trúc bài đọc và kịch bản video, phải bao bọc nội dung bằng 5 phân đoạn có thuộc tính ID từ `section-1` đến `section-5` đạt tối thiểu 500 ký tự, chèn thẻ `<i>...</i>` hoặc `<figcaption>` ngay dưới mọi thẻ `<img>`, và kiểm tra đối tượng Blueprint JSON không được rỗng hoặc sai định dạng. | Source: [[Lesson 01 - Tổng quan về hệ thống quản lý phiên bản Git]]
* **[GIT CLI 2.45+, GITHUB CLOUD (CONVENTIONAL COMMITS, GIT FLOW, SEMANTIC BRANCHING)]**: Khi thiết lập chuẩn đầu ra và nội dung bài đọc, bắt buộc sử dụng các động từ hành động đo lường được ('Liệt kê được', 'Nêu được', 'Viết được') thay cho động từ nhận thức ('Nhớ được', 'Hiểu'), đồng thời cấu hình bài đọc đủ 5 phần với các ID từ section-1 đến section-5 (độ dài tối thiểu 500 ký tự) và luôn chèn thẻ <i>...</i> hoặc <figcaption> trực tiếp bên dưới thẻ <img> để tránh lỗi Master Validator. | Source: [[Lesson 02 - Cài đặt & Cấu hình môi trường Git CLI]]
* **[GIT CLI 2.45+, GITHUB CLOUD (CONVENTIONAL COMMITS, GIT FLOW, SEMANTIC BRANCHING)]**: Khi khởi tạo cấu trúc HTML bài đọc, phải chia thành 5 phần chứa các thuộc tính `id` từ `section-1` đến `section-5` với tổng độ dài tối thiểu 500 ký tự, sử dụng thẻ `<pre><code>...</code></pre>` cho khối mã nguồn thực hành ở Section 3 và bắt buộc đính kèm chú thích `<i>...</i>` hoặc `<figcaption>...</figcaption>` ngay phía dưới thẻ `<img>`. | Source: [[Lesson 05 - Ghi nhận phiên bản Commit & Chuẩn Conventional Commits]]
* **[PYTHON]**: Khi tạo nội dung slide bài giảng Python về toán tử, tất cả tiêu đề phải dùng Tiếng Việt có dấu (không dùng snake_case hoặc tiếng Việt không dấu), khối mã `<code>` chỉ được chứa mã Python thực thi (không chứa văn bản mô tả), bọc mọi thẻ `<table>` trong `<div class="overflow-x-auto">` và phải trình bày trực quan Bảng giá trị chân lý (Truth Table) cùng minh họa cơ chế Đánh giá ngắn mạch (Short-circuit Evaluation). | Source: [[Lesson 02 - Toán tử so sánh và toán tử logic]]
* **[PYTHON]**: Khi xuất nội dung bài đọc HTML, bắt buộc phải cấu trúc đủ 5 phần với ID từ `section-1` đến `section-5` (độ dài tối thiểu 500 ký tự), bọc tất cả thẻ `<table>` trong thẻ div có lớp `overflow-x-auto` và chèn thẻ chú thích `<i>` hoặc `<figcaption>` ngay bên dưới mỗi thẻ `<img>`. | Source: [[Lesson 04 - Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8]]
* **[PYTHON]**: Khi khởi tạo slide và nội dung bài học Python, tất cả tiêu đề và mục lục phải giữ nguyên 100% tiếng Việt có dấu, không sử dụng văn bản rập khuôn (boilerplate) hay khái niệm lạc đề, đồng thời bắt buộc nhúng mã nguồn Python thực tế minh họa các toán tử số học (`+`, `-`, `*`, `/`, `//`, `%`, `**`) và toán tử gán phím tắt (`+=`, `-=`, `*=`, `/=`) từ nguồn tri thức gốc. | Source: [[Lesson 01 - Toán tử số học và toán tử gán]]
* **[PYTHON]**: Khi thiết kế bài học cấu trúc rẽ nhánh cơ bản (if/elif/else) trong Python, không yêu cầu người học tự xây dựng test case với Pytest 8.3 mà chỉ sử dụng kịch bản kiểm thử viết sẵn, đồng thời phải minh họa bằng mã nguồn Python thực tế tuân thủ quy tắc thụt lề 4 khoảng trắng theo chuẩn PEP 8. | Source: [[Lesson 03 - Cấu trúc rẽ nhánh điều khiển với if, elif và else]]
* **[PYTHON 3.12]**: Khi khởi tạo nội dung bài đọc và kịch bản video, phải đảm bảo bài đọc đạt tối thiểu 500 ký tự gồm 5 phần gắn ID `section-1` đến `section-5`, bọc thẻ `<table>` trong thẻ div chứa class `overflow-x-auto`, gắn chú thích `<i>` hoặc `<figcaption>` trực tiếp dưới `<img>`, đồng thời xuất Video Script Blueprint dưới dạng chuỗi JSON hợp lệ không được để rỗng. | Source: [[Lesson 04 - Thao tác Xóa phần tử trong List và Tính bất biến của Tuple]]
* **[PYTHON]**: Khi thiết kế Menu Console tương tác trong Python, phải triển khai cấu trúc vòng lặp while True kết hợp hàm input() để nhận dữ liệu người dùng, phân nhánh chức năng bằng các câu lệnh điều kiện if/elif/else có xử lý trường hợp nhập sai lựa chọn, và dùng lệnh break để thoát vòng lặp an toàn. | Source: [[Lesson 04 - Nguyên lý xây dựng Menu Console lặp tương tác]]
