---
name: lessons_learned
description: Kho kinh nghiệm đã gom nhóm và khử trùng lặp, gồm các hàng rào kỹ thuật và quy tắc phòng lỗi rút ra từ phản hồi của reviewer ở các lần sinh học liệu trước. Đầu ra luôn là tiếng Việt có dấu.
---

# Lessons Learned - Kho kinh nghiệm phòng lỗi

Mọi agent PHẢI đọc kho này trước khi sinh hoặc rà soát học liệu để không lặp lại lỗi cũ. Bản đầy đủ chưa gọn hóa (kèm nguồn từng bài) nằm ở `docs/archive/lessons_learned_full_2026-10-12.md`.

Cách tổ chức: nhóm A áp dụng cho mọi môn; nhóm B áp dụng theo công nghệ; mục cuối "Quy tắc bổ sung tự động" do `agents/lessons_learned_agent.py` ghi nối thêm từng dòng (định dạng `* **[CÔNG NGHỆ]**: quy tắc | Source: [[tên bài]]`). Định kỳ gom các dòng đó vào nhóm A hoặc B và xóa dòng trùng.

---

## A. Quy tắc chung cho mọi môn

### A1. Cấu trúc bài đọc và kiểm định tự động (Master Validator)

- Bài đọc có đúng 5 mục với ID `section-1` đến `section-5`; mỗi mục tối thiểu 500 ký tự, tổng dung lượng bài đọc HTML khoảng 50KB-120KB.
- Mỗi thẻ `<img>` có chú thích ngay bên dưới bằng `<figcaption>` hoặc `<i>...</i>`.
- Mọi thẻ `<table>` bọc trong `<div class="overflow-x-auto">` để không vỡ giao diện trên di động.
- Đóng đủ cặp thẻ HTML, `<pre><code class="language-xxx">...</code></pre>` và khối SVG; không để nội dung bị cắt xén giữa chừng. Khối mã Markdown đóng bằng đúng ba dấu backtick, không kèm tên ngôn ngữ ở thẻ đóng.
- Mã ví dụ đặt trong `<pre><code>`; với nhóm 3 ví dụ Section 3 phải đủ 3.1, 3.2, 3.3. Mỗi mục con ở Section 2 có Code Sandbox tương tác riêng để minh họa từng biến thể cú pháp.
- Trước mỗi Code Sandbox có khối "Yêu cầu bài toán thực hành" nêu ngữ cảnh, ràng buộc kỹ thuật và kết quả đầu ra kỳ vọng.
- Không để biến template chưa render (ví dụ `{clean_title}`) hoặc khối HTML Visualizer bị lặp.
- Kịch bản video xuất Blueprint JSON hợp lệ, không rỗng.
- Hộp code dùng đúng một lớp khung giao diện bọc trực tiếp ngoài mã; không lồng hai lớp khung.
- Tiêu đề, mục lục slide và nhãn giữ nguyên tiếng Việt có dấu 100% (không snake_case, không tiếng Việt không dấu); không dùng văn bản rập khuôn hay khái niệm lạc đề.

### A2. Giao diện, màu sắc, ký hiệu

- Cấm emoji và ký tự biểu tượng Unicode (mũi tên, dấu tích, hình tròn màu...) trong bài đọc, mã, Quiz JSON, mindmap. Thay bằng nhãn chữ thường như `Lưu ý:`, `Mẹo:`, `Cảnh báo:` (KHÔNG dùng thẻ ngoặc vuông kiểu `[NOTE]`) hoặc Phosphor Icons `<i class="ph-bold ph-*"></i>`.
- Giữ chuẩn Light Mode 100%: không dùng tiền tố `dark:`, không dùng nền tối (`bg-slate-900`, `bg-black`, `bg-slate-900/60`, mã `#020617`), không phối nền tối với `text-slate-700`.
- Trên khung nền sáng pastel (`bg-amber-50`, `bg-rose-50`, `bg-emerald-50`...) dùng chữ tối (`text-slate-800`, `text-slate-900`, `text-amber-950`...), không dùng `text-white`, `text-slate-50`, `text-sky-300`. Khung `#viz-console` phải đạt độ tương phản Light Mode.
- Không dùng cụm từ sáo rỗng của AI ("mẹo lập trình", "bẫy cú pháp", "bẫy lập trình"). Dùng "Lỗi thường gặp", "Ngoại lệ cần lưu ý", "Lưu ý thực tế".
- Khung hiển thị mã: nhãn tiêu đề phải ghi đúng tên và phiên bản công nghệ của bài (ví dụ `Mã nguồn thực thi (Python 3.12)`), không nhầm sang ngôn ngữ khác (TypeScript, JavaScript...). Thuộc tính class dùng nhãn ngôn ngữ chuẩn viết thường (`language-python`, `language-bash`), không chèn chuỗi Tech Stack dài, không lặp thuộc tính `class` trong một thẻ.
- Khối mã ngoặc nhọn và toán tử so sánh (`<`, `>`, `<=`, `>=`) nhúng vào HTML phải mã hóa thực thể (`&lt;`, `&gt;`) để tránh cắt xén cú pháp.
- Khối mã tương đối dài, bổ sung có thể bọc trong `<details><summary>...</summary>...</details>` đạt chuẩn truy cập WCAG.
- Sửa lỗi hiển thị thẻ so sánh ĐÚNG/SAI: cả hai cột đều có mã hoàn chỉnh và đóng đủ thẻ.

### A3. Phạm vi kiến thức và bối cảnh nghiệp vụ

- Chỉ dùng cú pháp, thuật ngữ, kiểu dữ liệu, hàm đã dạy đến bài hiện tại; không nhắc khái niệm chưa học ở bất cứ đâu (mã chạy, chú thích, tên biến, lệnh bash, tiêu đề, giải thích). Danh sách cấm cụ thể lấy từ `forbidden_scope` của bài.
- Bài mở đầu về một công cụ hoặc phương pháp (ví dụ VCS) không đưa lệnh thực hành CLI của các bài sau vào nội dung.
- Một bài chỉ dùng MỘT bối cảnh nghiệp vụ được giao (ví dụ `COFFEE_POS`, `GRAB_RIDE`, `HOTEL_BOOKING`, `SHOPEE_FOOD`, `EVENT_TICKETING`, `SAAS_SUBSCRIPTION`, `EV_CHARGING_STATION`); tên biến, tên hàm, chuỗi in ra đồng nhất theo bối cảnh đó.
- Mã trong Visualizer và Sandbox phải là mã thật gắn với chủ đề bài; cấm hàm mẫu chung chung (`processContext()`, `executeStepLogic()`, `load_input_parameters()`).
- Visualizer: khai báo đầy đủ mảng `window.vizSteps` trong thẻ `<script>` trước khi `runVizStep()` và `updateRamMonitor()` truy xuất; thứ tự trace phải đi đúng vào phương thức/hàm được gọi thay vì chạy tuyến tính. Với bài thực hành cấu trúc điều khiển, Visualizer cần canvas trạng thái biến, bộ nút điều khiển (Bắt đầu, Tạm dừng, Từng bước, Đặt lại), Code Tracker có lớp `active-line` đồng bộ dòng thực thi, và khi phù hợp có ô nhập hoặc thanh trượt để người học chỉnh giá trị.
- Id phần tử HTML phải khớp 1-1 với bộ chọn JavaScript (`getElementById`); chữ ký hàm gắn sự kiện khớp thuộc tính `onclick` (ví dụ `copyCode(this, 'id')`). Khi ghi log vào `innerText` dùng ký tự gốc (`&&`), không dùng thực thể `&amp;&amp;`.
- Bài tự kiểm tra: số lựa chọn A, B, C, D trong HTML khớp phím đáp án cấu hình trong hàm `checkSelfTest()`.

### A4. Chuẩn đầu ra và Quiz

- Chuẩn đầu ra (kể cả nhóm `remembering_understanding`) dùng động từ Bloom đo lường được: "Liệt kê được", "Nêu được", "Trình bày được", "Giải thích được", "Viết được", "Phân biệt được", "Chỉ ra được", "Xây dựng", "Mô phỏng". Không dùng "Hiểu", "Hiểu rõ", "Ghi nhớ", "Nắm vững", "Thực hành" làm động từ chuẩn đầu ra.
- Quiz JSON (`question`, `options`, `explanation`) phải độc lập, khách quan: cấm cụm viện dẫn ngữ cảnh trung gian như "trong bài đọc", "dựa vào bài đọc", "theo bài học", "theo đoạn văn trên", "đã đề cập", "theo mã trên", "trong kịch bản".
- Khối mã Markdown trong trường `question` đóng bằng ba dấu backtick trơn.
- Bài thực hành chỉ dùng kịch bản kiểm thử viết sẵn khi chưa dạy công cụ kiểm thử; không yêu cầu người học tự xây dựng test case bằng công cụ chưa học.

### A5. Môi trường và hệ điều hành

- Windows UTF-8: khi xử lý tiếng Việt, cấu hình `sys.stdout.reconfigure(encoding='utf-8')` và `sys.stderr.reconfigure(encoding='utf-8')`; đặt biến môi trường `PYTHONIOENCODING=utf-8` cho tiến trình con để tránh `UnicodeEncodeError` do mã hóa mặc định CP1252.
- Phát hiện môi trường ảo bằng `sys.prefix != sys.base_prefix`.
- Bài có `input()` khi kiểm thử trong sandbox phải dùng dữ liệu giả hoặc stub (`unittest.mock.patch`) để tránh treo `TimeoutExpired`.

### A6. Mindmap Markmap

- Chuyển khóa snake_case nội bộ thành tiêu đề H2/H3 tiếng Việt có dấu tự nhiên.
- Khối ` ```markmap ` đóng sạch, không dư dấu backtick.

### A7. Kiểm chứng trước khi giao (rút ra từ hai môn ReactJS và NodeJS)

- Mọi đoạn mã, truy vấn, kết quả in ra, mã trạng thái và đáp án quiz trong tài liệu phải được CHẠY THẬT rồi chép đúng kết quả; không tự tính tay. Câu dạng "dự đoán" có ba đáp án sai thật sự sai.
- Bài tập: đáp án mẫu qua 100% test; mã khởi tạo chạy được (không lỗi cú pháp hay `require`) nhưng phần lớn test đỏ; thử ít nhất 6 lời giải sai điển hình, mỗi lần có test đỏ, ghi đúng số đỏ vào hướng dẫn giảng viên. Chạy lặp 3 lần để thấy test ổn định.
- Lỗi mà test không bắt được (ví dụ quên `return` trước khi trả lỗi, `key={index}`) ghi riêng trong hướng dẫn giảng viên để chấm ở mục chất lượng mã.
- Test không phụ thuộc đồng hồ thật, `Math.random` hay múi giờ máy: không khẳng định chuỗi `createdAt`; timer dùng fake timers; thời gian chờ đủ lớn cho máy chậm.
- Kết quả mong đợi trong lab (log máy chủ, thân JSON, hàng trong bảng) lấy từ lần chạy thật; tên cơ sở dữ liệu và cổng đặt thay đúng như tài liệu hướng dẫn sinh viên.
- Số từ bài đọc đếm một cách thống nhất (cả mã, không tính mô phỏng); đề bài 350-700 từ chữ (không tính khối mã và bảng).

---

## B. Quy tắc theo công nghệ

### B1. Python (core, 3.x)

- Không dùng đối số mặc định có thể thay đổi (`def f(lst=[])`); dùng `lst=None` rồi `if lst is None: lst = []`.
- Chuỗi nhiều dòng dùng ba dấu nháy; chuỗi chứa `\n` trong `print()` hoặc f-string giữ nguyên trên một dòng trong cặp nháy để tránh `SyntaxError: unterminated string literal`.
- Trích mã Python từ trường JSON phải dùng bộ phân tích đúng (`json.loads`) hoặc regex lọc ký tự phân cách cuối dòng (`",`).
- Biểu thức logic có nguy cơ chia cho 0 phải bảo vệ bằng ngắn mạch: `x != 0 and (10 / x > 1)`. Bài toán tử logic cần Bảng giá trị chân lý và minh họa Đánh giá ngắn mạch.
- Cập nhật hoặc xóa phần tử danh sách theo chỉ số: kiểm tra `0 <= index < len(list)` trước khi gán hoặc dùng `del` để tránh `IndexError`. Không thay đổi kích thước danh sách trong lúc duyệt.
- `sort()` và `reverse()` sửa tại chỗ: gọi trực tiếp trên danh sách gốc, không gán kết quả (sẽ là `None`).
- Bài duyệt/đọc danh sách chỉ dùng `in`, `for`, `enumerate()`, `range()`, `len()`; bài thêm phần tử chỉ dùng `.append()`, `.extend()`, toán tử `+` (không `.insert()` nếu bài chưa dạy); bài xóa chỉ dùng `del` kèm kiểm tra chỉ số bằng `len()` khi chưa dạy `remove()`, `pop()`.
- Bài biến, toán tử, rẽ nhánh ban đầu chỉ dùng `int`, `float`, `str`, `bool`; không nhắc `list`, `set`, `tuple`, `dictionary` trong mã, chú thích, tên biến hay lệnh `pip list`. Không dùng `isinstance`, `if/elif/else` trong bài chưa học rẽ nhánh. Bài vòng lặp `while` cơ bản không dùng `break`/`continue` khi chưa dạy.
- Bài môi trường (venv, CLI) chỉ dùng lệnh terminal (`python -m venv`, `source`, `pip install`, `which`), không dùng `def`, vòng lặp, điều kiện, cấu trúc dữ liệu.
- Nội dung bài dữ liệu lồng nhau chỉ mô tả "danh sách chứa các dictionary" và truy xuất hai tầng `list[index][key]`; không dùng thuật ngữ vượt cấp "mô hình list of dictionaries" (trong chú thích, tên biến) hay `oop` khi chưa học.
- Menu console tương tác: `while True` kết hợp `input()`, phân nhánh `if/elif/else` có xử lý lựa chọn sai, thoát an toàn bằng `break`.
- Code theo PEP 8: thụt lề 4 khoảng trắng. Slide Python về toán tử: khối `<code>` chỉ chứa mã thực thi, trình bày đủ toán tử số học (`+ - * / // % **`) và toán tử gán rút gọn (`+= -= *= /=`).
- Bài về Python/Pyodide: không dùng `pyodide.js` hay `runPythonCode` cho môn không phải Python.
- Phạm vi cấm ở bài Python core: không giới thiệu trước `APIRouter`, `SQLAlchemy`, `FastAPI`, `Pydantic`.
- Biểu diễn trực quan OOP: trace `window.vizSteps` nhảy đúng vào `__init__`, phương thức thể hiện, `__str__` để `updateRamMonitor` cập nhật đúng bảng bộ nhớ.

### B2. Web Backend và ORM (FastAPI, SQLAlchemy, Pydantic)

- Khi bắt ngoại lệ cơ sở dữ liệu (ví dụ `IntegrityError`) trong API, luôn `db.rollback()` trước khi trả phản hồi lỗi.
- Tiêm phiên cơ sở dữ liệu bằng dependency hoặc context manager (`db: AsyncSession = Depends(get_db)`).
- Schema đầu vào dạng danh sách khai báo giới hạn (`Field(..., min_items=1)` cho các mục quiz); schema bài thực hành có sub-schema rõ cho `objectives`, `steps`, `checklist`.

### B3. Ngôn ngữ C (C11 cơ bản, GCC)

- Bài khai báo biến chỉ dùng khai báo và gán đơn giản (`int`, `float`, `char`), không tự định nghĩa hàm, không `if`/`switch`, không vòng lặp.
- Bài `printf()`/`scanf()` không nhắc "hàm", "toán tử" (kể cả khi giải thích `&`) hay vòng lặp. Bài giới thiệu C chỉ mô tả `main()` là điểm khởi chạy và `printf()` là câu lệnh in; không dùng các thuật ngữ "hàm", "toán tử", "kiểu dữ liệu" chưa học.
- Bài toán tử logic (`&&`, `||`, `!`) trước bài rẽ nhánh: không dùng từ "điều kiện"; dùng "biểu thức logic", "tiêu chuẩn", "giá trị đúng/sai (1/0)". Bài toán tử so sánh gán kết quả vào biến `int` (0 hoặc 1), không dùng `if/else`, `&&`, `||`.
- Bài vòng lặp `break`/`continue` chỉ thao tác biến đơn trong `main()`, không mảng, không hàm tự định nghĩa.
- Nhập mảng bằng vòng lặp `for` truyền đúng địa chỉ `&array[i]` vào `scanf()`.
- Khai báo `char a[N] = "..."`: phần tử còn lại tự gán `'\0'` theo C99/C11; chỉ mảng không khởi tạo (`char a[N];`) mới chứa giá trị rác.
- Bài `fgets()` và bộ đệm bàn phím: dùng "Lưu ý thực tế", "Các lỗi thường gặp", không dùng "hàm" khi bài chưa dạy. Bài nhập xuất mảng struct không đưa dọn bộ đệm hay hàm tự định nghĩa vào nếu ngoài phạm vi; định dạng cột bằng `%-Ns`, `%-N.2f`.
- Bài mảng cần Visualizer có ô nhập hoặc thanh trượt cho `index` và giá trị phần tử trước khi chạy từng bước.

### B4. JavaScript và Web (ES6+, DOM)

- Bài mở đầu về biến, điều kiện, hàm: chỉ dùng cú pháp đã học (không `Array`, `.forEach()` khi chưa dạy).
- Mã xử lý sự kiện `submit` của form phải đầy đủ logic validation, đóng khối `addEventListener` bằng `});`, và truy cập đúng thuộc tính chuẩn (`.value`, `.checked`) thay vì thuộc tính không tồn tại.
- Mã Visualizer cho Object/JSON phải dùng thao tác thật (thuộc tính Object, `JSON.stringify()`, `JSON.parse()`, `try...catch`), khai báo `window.vizSteps` mô phỏng chi tiết bộ nhớ từng dòng; bài hàm/phạm vi dùng mã Scope cụ thể.

### B5. Git, GitHub và CLI (Git 2.45+, Git Bash, VS Code Source Control)

- Khối lệnh Git dùng nhãn "Mã lệnh Git Bash" và `<code class="language-bash">` (hoặc `language-shell`); tuyệt đối không dùng `language-c`. Đóng đủ cặp `<pre><code>`.
- Không nhúng `pyodide.js` hay `runPythonCode` vào bài Git/CLI; Visualizer dùng `runVizStep()` phản ánh đúng vòng đời tập tin (`Untracked`, `Staged`, `Unmodified`, `Modified`) và cập nhật `active-line` trên các phần tử `viz-line-*`.
- Bài Git có đủ hướng dẫn cho cả Git Bash và VS Code Source Control Panel; Visualizer gồm ba thành phần: canvas mô phỏng dịch chuyển commit, bảng State Tracker, Terminal Console Log.
- Bài mở đầu (VCS) không đưa `git config`, `git init`, `git add`, `git commit`, `git remote`, `git push` vào nội dung.
- Chuẩn đầu ra cho Git dùng động từ Bloom đo lường được (ví dụ "Xây dựng", "Lập kế hoạch", "Mô phỏng", "Liệt kê được").

### B6. React 18 (Vite, Vitest, React Testing Library, React Router 6)

- Phiên bản ghim: React 18.3.1, React Router 6.30.1, axios 1.7.9, Vitest 3.1.4. Không tạo dự án bằng `npm create vite@latest` (sinh React bản mới hơn); dùng `package.json` đã ghim.
- Bài chỉ dùng function component, `useState`, `useEffect`, `useReducer`, `useContext`, custom hook. Không dùng `useRef`, `useMemo`, `useCallback`, `React.memo`, class component trong phạm vi chưa dạy.
- Không truyền `async` trực tiếp cho `useEffect` (React cảnh báo và có thể ném lỗi khi unmount): định nghĩa hàm async bên trong rồi gọi.
- `StrictMode` ở `npm run dev` chạy effect hai lần lúc mount: đây là kiểm tra có chủ đích, không phải lỗi.
- Test dùng timer giả với `userEvent` dễ treo: dùng `fireEvent` khi có fake timers. Trả `vi.useRealTimers()` cuối test.
- API giả (`tests/mock-api.js`) chỉ chạy trong Vitest, không nạp được vào `npm run dev`; mã của sinh viên luôn gọi URL thật. Mock không tái hiện vòng lặp vô hạn khi thiếu mảng phụ thuộc: không dùng khẳng định đó trong quiz.
- Cảnh báo "React Router Future Flag" bị lọc trong `tests/setup.js` vì chỉ nói về nâng cấp lên bản 7.

### B7. NodeJS, Express 4 và MySQL 8 (CommonJS, mysql2, zod, bcryptjs, jsonwebtoken, Vitest, Supertest)

- Phiên bản ghim: Express 4.21.2 (không dùng Express 5), mysql2 3.11.5, zod 3.24.1, bcryptjs 2.4.3, jsonwebtoken 9.0.2, Vitest 3.1.4, Supertest 7.0.0. Dự án dùng CommonJS (`require`, `module.exports`); không `class`, không `this`.
- `src/app.js` xuất `app` KHÔNG gọi `listen`; `src/server.js` mới gọi `listen`. Test dùng Supertest gọi thẳng `app`.
- Phân trang dùng `pool.query` với `LIMIT ? OFFSET ?`; `pool.execute` với `LIMIT ?` báo `ER_WRONG_ARGUMENTS` trên MySQL 8.0.45 và mysql2 3.11.5. `pool.execute` với `IN (?)` và mảng trả 0 dòng mà không báo lỗi: tránh.
- `SUM` và `AVG` trả DECIMAL (chuỗi); bật `decimalNumbers: true` trong `createPool` để nhận số. `TIMESTAMP` trả đối tượng `Date`.
- Truy vấn luôn tham số hóa bằng `?`; tên cột sắp xếp lấy từ danh sách trắng, không nối chuỗi.
- Route `async` trong Express 4 không tự bắt lỗi: dùng `try/catch` với `next(error)` hoặc `asyncHandler`. `express.json()` phải khai báo trước router, nếu không `req.body` là `undefined`.
- Giao dịch: `getConnection`, `beginTransaction`, `commit` hoặc `rollback`, và `release` trong `finally`; thiếu `release` làm pool cạn kết nối.
- JWT: `sub` là chuỗi (`String(id)`), đọc lại bằng `Number(payload.sub)`; không đưa thông tin bí mật vào payload; không trả `passwordHash`. `bcryptjs` dùng số vòng nhỏ trong test (`BCRYPT_ROUNDS=4`).
- Cơ sở dữ liệu thử có tên kết thúc bằng `_test` và `resetDatabase()` từ chối chạy nếu tên không đúng; `fileParallelism: false` trong Vitest vì các tệp test dùng chung một cơ sở dữ liệu.
- Bộ đếm `express-rate-limit` là riêng cho từng tệp test: test khác ký token trực tiếp thay vì gọi `/auth/login`.

### B8. Docker, DevOps

- Quy tắc khi chèn ảnh và bảng ở nhóm A1 áp dụng nguyên cho bài DevOps/Docker/quy trình nhóm (Pull Request, Merge, Conventional Commits); bổ sung: bài Docker cần Blueprint JSON video hợp lệ khi có kịch bản video.

---

## Quy tắc bổ sung tự động

Phần dưới do `agents/lessons_learned_agent.py` ghi nối thêm. Không xóa dòng tiêu đề này.

