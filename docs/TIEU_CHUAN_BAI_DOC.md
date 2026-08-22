# TIÊU CHUẨN CẤU TRÚC & TRÌNH BÀY BÀI ĐỌC (READING MATERIAL STANDARD)

> **Phạm vi áp dụng:** Tài liệu này là quy chuẩn CHUNG cho toàn bộ hệ thống sinh "Bài đọc"
> (reading.html) — áp dụng cho MỌI môn học/công nghệ (Python, JavaScript, Java, SQL, Git, v.v.),
> không hard-code riêng cho bất kỳ ngôn ngữ/công nghệ nào. Mọi giá trị công nghệ-cụ thể trong tài
> liệu (tên biến, cú pháp mẫu...) chỉ mang tính MINH HỌA từ 1 bài mẫu, không phải yêu cầu bắt buộc
> về nội dung.
>
> **Nguồn tham chiếu khi biên soạn tài liệu này:**
> - Bài đọc mẫu hoàn thiện: `Session 08 - Cấu trúc Vòng lặp for, range() và Vòng lặp while /
>   Lesson 01 - Vòng lặp for và Hàm range() / Bài đọc / reading.html`
> - Template khung: `templates/html/reading_master.html.j2`
> - Tiêu chuẩn cũ: `resources/RE_Tiêu chuẩn bài đọc.pdf` (nguyên tắc "Storytelling in Tech" được
>   GIỮ LẠI về tinh thần, nhưng cấu trúc 7 phần cũ đã được **thay thế** bằng cấu trúc 5 phần mới bên
>   dưới — đây là điểm khác biệt quan trọng nhất so với bản PDF cũ).
>
> Định dạng file: **Markdown** (`.md`) — tài liệu này mô tả *quy chuẩn nội dung + cách trình bày*;
> việc render ra HTML cuối cùng do template Jinja2 (`reading_master.html.j2`) đảm nhiệm, người biên
> soạn/agent sinh nội dung KHÔNG cần viết trực tiếp HTML/CSS, chỉ cần tuân thủ cấu trúc và các
> "khối nội dung chuẩn" (content blocks) mô tả trong tài liệu này.

---

## 1. Nguyên tắc cốt lõi (giữ nguyên tinh thần từ chuẩn cũ)

**"Storytelling in Tech"** — Bài đọc TUYỆT ĐỐI KHÔNG được trình bày kiểu liệt kê định nghĩa khô
khan. Phải theo mạch truyện:

```
Đặt vấn đề (tình huống thực tế) → Giải thích cơ chế (cú pháp) → Ví dụ tiến triển
→ Tổng kết & phòng lỗi → Kiểm tra hiểu bài
```

Toàn bộ vấn đề/ví dụ/bài toán trong 1 bài đọc phải cùng thuộc **MỘT kịch bản nghiệp vụ thống nhất**
(Unified Business Scenario — ví dụ bài mẫu dùng xuyên suốt "Siêu thị MartX": quầy thu ngân, hóa
đơn, điểm thưởng, mã voucher). Nghiêm cấm nhảy sang bối cảnh khác giữa các section.

---

## 2. Cấu trúc 5 Phần bắt buộc (thay thế cấu trúc 7 phần của bản PDF cũ)

| # | Section (`id`) | Tên mặc định (có thể tùy biến qua `section_titles`) | Vai trò |
|---|---|---|---|
| 1 | `section-1` | Đặt vấn đề thực tế | Nêu tình huống nghiệp vụ thực tế cần giải quyết — chưa đưa cú pháp |
| 2 | `section-2` | Cú pháp và cơ chế hoạt động | Dạy cú pháp/khái niệm kỹ thuật, gắn với bài toán con cụ thể mỗi mục |
| 3 | `section-3` | Các ví dụ ứng dụng thực tiễn | 2-3 ví dụ tiến triển độ khó, áp dụng kiến thức Section 2 để giải quyết bài toán Section 1 |
| 4 | `section-4` | Tổng kết bài học | Tóm tắt kiến thức trọng tâm + các lỗi thường gặp (gotchas) |
| 5 | `section-5` | Tài liệu tham khảo | Link tham khảo chính thức + Bộ câu hỏi ôn tập (self-test) |

**Ánh xạ với 7 phần chuẩn cũ** (để không mất tinh thần storytelling khi biên soạn):

| Chuẩn cũ (PDF, 7 phần) | Chuẩn mới (5 phần) |
|---|---|
| 1. Đặt vấn đề | → nằm trong **Section 1** |
| 2. Phân tích | → nằm trong **Section 1** (đoạn giải thích "tại sao cách cũ không ổn") |
| 3. Giới thiệu giải pháp | → mở đầu **Section 2** |
| 4. Ví dụ minh họa | → phần code sandbox trong **Section 2** (mỗi cú pháp con có 1 ví dụ nhỏ đi kèm ngay) |
| 5. Giải quyết vấn đề | → **Section 3** (ví dụ tiến triển, áp dụng để giải quyết trọn vẹn bài toán) |
| 6. Tổng kết và lưu ý | → **Section 4** |
| 7. Bộ câu hỏi kiểm tra | → **Section 5** (self-test, đổi từ 3 câu tự luận → trắc nghiệm 3-4 câu có giải thích tức thời) |

Mỗi `<h2>` section đánh số thứ tự `N. {title}`, có `id="section-N"` và class `scroll-mt-24` (để neo
đúng vị trí khi có header cố định, tránh bị header che khuất khi click mục lục).

---

## 3. Bố cục trang tổng thể (Page Layout)

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER (fixed, h-16, z-40)                                   │
│  Logo Rikkei | Tên bài học | ── thanh scroll-progress đỏ ──  │
├───────────┬─────────────────────────────────────────────────┤
│ SIDEBAR   │ ARTICLE (bg-white, rounded-2xl, border, shadow)  │
│ TOC       │  H1: Tên bài học (đã strip prefix "Session/      │
│ (sticky,  │      Lesson NN -")                                │
│ w-80,     │  Section 1..5 (như bảng trên)                     │
│ ẩn <lg)   │                                                    │
└───────────┴─────────────────────────────────────────────────┘
  max-w-[1680px] mx-auto, gap-8, px-6, pt-24 (chừa chỗ header), pb-16
```

- **Header**: `fixed top-0`, nền `bg-white/95 backdrop-blur-md`, viền dưới `border-slate-200`.
  Bên trong: logo (link cố định `https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png`,
  `h-9`), tên bài học rút gọn (font `text-sm font-semibold text-slate-500`), và 1 thanh tiến trình
  cuộn trang (`#scroll-progress`, cao `h-1`, màu `bg-rikkei-red`, cập nhật `width` theo % scroll).
- **Sidebar TOC** (desktop `lg:block`, `w-80`, `sticky top-24`): liệt kê đúng 5 mục, active-state
  tự động theo section đang xem (dùng `IntersectionObserver`, style active:
  `border-rikkei-red text-rikkei-red font-bold`).
- **Mobile TOC**: nút tròn nổi góc dưới-phải (`fixed bottom-6 right-6`, nền đỏ, icon list) mở
  drawer trượt từ phải (`w-80 max-w-[85vw]`), có overlay mờ nền `bg-slate-900/60 backdrop-blur-sm`.
- **Article container**: nền trắng, `rounded-2xl`, `border border-slate-200`, `shadow-sm`,
  padding `p-6 sm:p-10`. Tiêu đề H1 nằm trong khối riêng có `border-b` phân cách với nội dung.

---

## 4. Bảng màu & Typography chuẩn (Style Guide)

### 4.1 Bảng màu thương hiệu (KHÔNG được đổi)

| Token | Hex | Dùng cho |
|---|---|---|
| `rikkei-red` | `#be111c` | Điểm nhấn chính: thanh progress, link, số badge TOC, border khi active, icon chính |
| `rikkei-darkred` | `#90000a` | Hover state của các nút/link màu đỏ |
| `rikkei-dark` | `#0f172a` | Màu chữ heading (H1-H6), nền badge tối |

### 4.2 Bảng màu ngữ nghĩa cho khối nội dung (semantic content blocks)

| Ngữ cảnh | Nền | Viền | Chữ tiêu đề khối |
|---|---|---|---|
| **Yêu cầu bài toán** (problem-box, đặt trước mỗi ví dụ code) | `bg-sky-50/60` | `border-sky-200` | `text-sky-900` |
| **Thông tin/khái niệm bổ sung** (info-box trung tính) | `bg-slate-50/50` | `border-slate-200` | `text-slate-800` |
| **Lỗi thường gặp / Cảnh báo** (gotcha-box, chỉ dùng ở Section 4) | `bg-rose-50/60` | `border-rose-200` | `text-rose-900` |
| **Trạng thái thành công/RAM cập nhật** (visualizer feedback) | `bg-emerald-50` / `bg-emerald-100` | `border-emerald-300` | `text-emerald-800` |
| **Badge bước đang chạy** (step visualizer) | `bg-amber-100` | `border-amber-300` | `text-amber-800` |

Mọi khối nội dung dùng `rounded-xl`, `p-4`, `shadow-sm`, `my-4` để đồng nhất khoảng cách/bo góc.

> **Quy tắc High-Contrast bắt buộc**: mọi text bên trong các khối màu nền nhạt (`bg-amber-50`,
> `bg-rose-50`, `bg-emerald-50`, `bg-sky-50`) PHẢI ép về `color: #1e293b` (đã enforce ở tầng CSS
> `!important` trong template) — không được để màu chữ nhạt hơn nền gây khó đọc.

### 4.3 Typography

| Phần tử | Font | Cỡ chữ | Trọng số |
|---|---|---|---|
| H1 (tiêu đề bài) | Montserrat | `text-3xl` (30px) | `font-bold` |
| H2 (tiêu đề section) | Montserrat | `text-2xl` (24px) | `font-bold` |
| H3 (tiêu đề mục con, vd "2.1.") | Montserrat | `text-xl` (20px) | `font-bold` |
| H4 (tiêu đề khối nội dung) | Montserrat | `text-sm`/`text-base` | `font-bold` |
| Nội dung văn bản (`p`, `li`) | Inter | `text-sm`/mặc định | `text-slate-600`, `leading-relaxed` |
| Code inline | JetBrains Mono | `text-sm` | nền `bg-slate-100`, chữ `text-rikkei-red` |
| Code block | JetBrains Mono | `text-sm` (`0.875rem`) | `line-height: 1.6`, nền `#f8fafc` |

**Zero-italic policy**: toàn bộ nội dung bài đọc (heading, paragraph, list, table, strong) PHẢI
`font-style: normal`. Chỉ được phép in nghiêng ở đúng 2 chỗ: `figcaption` (chú thích hình) và
`p.italic`/`.img-caption` (ghi chú ảnh) — enforce cứng bằng CSS safety-net trong template, KHÔNG
được lách qua bằng cách chèn `<em>`/`<i>` tùy tiện trong nội dung.

---

## 5. Chi tiết nội dung từng Section

### Section 1 — Đặt vấn đề thực tế

- 2-3 đoạn văn (`<p>`) dẫn dắt: mô tả 1 tình huống nghiệp vụ CỤ THỂ (có tên riêng thực thể — vd
  "Siêu thị MartX", không dùng chung chung "một hệ thống"), nêu hệ quả nếu làm thủ công (cồng kềnh,
  dễ sai sót khi quy mô lớn), rồi đặt câu hỏi dẫn tới nhu cầu công nghệ/cú pháp sắp học.
- Từ khóa kỹ thuật xuất hiện lần đầu phải được bọc `<code>` (class: nền `bg-slate-100`, chữ
  `text-rikkei-red`).
- **Bắt buộc 1 hình minh họa** ngay sau đoạn văn — ưu tiên **SVG sơ đồ luồng tự vẽ** (3 khối:
  Input → Xử lý (khối trung tâm màu sky/blue biểu diễn đúng cú pháp) → Output, nối bằng mũi tên có
  nhãn, xem chi tiết ở mục 6.4) hơn là ảnh raster ngoài; nếu dùng ảnh ngoài (`context_image_url`)
  phải có `figcaption` mô tả và xử lý `onerror` ẩn khối nếu ảnh lỗi.

### Section 2 — Cú pháp và cơ chế hoạt động

Chia thành nhiều mục con `<h3>` đánh số `2.1`, `2.2`, ... — mỗi mục con là **MỘT ĐƠN VỊ HỌC ĐỘC
LẬP** theo khuôn cố định:

1. 1 đoạn `<p>` giải thích khái niệm cú pháp.
2. **1 khối "Yêu cầu bài toán"** (problem-box, màu sky) — đặt ra 1 bài toán nhỏ, CỤ THỂ, thuộc
   đúng kịch bản nghiệp vụ chung của bài, mà mục con này sẽ giải quyết.
3. **1 Code Sandbox** thực thi được (xem mục 6.1) — code giải bài toán vừa nêu, có comment tiếng
   Việt giải thích ý nghĩa nghiệp vụ từng dòng quan trọng.
4. 1 danh sách `<ul>` giải nghĩa từng thành phần cú pháp vừa dùng (mỗi `<li>` bắt đầu bằng
   `<code>tên_thành_phần</code>:` in đậm, sau đó giải thích).
5. (Tùy chọn, dùng khi cú pháp có nhiều đặc tính kỹ thuật cần nhấn mạnh) 1 khối "Thông tin bổ
   sung" (info-box, màu slate) liệt kê bản chất/cơ chế (vd: lazy evaluation, tính bất biến...).

Ở mục con **cuối cùng** của Section 2, bắt buộc có **1 Bộ mô phỏng từng bước (Step-by-Step
Execution Visualizer)** — xem mục 6.2. Đây là điểm nhấn tương tác quan trọng nhất của bài đọc,
giúp học viên "nhìn thấy" cơ chế chạy ngầm (biến trong RAM, dòng đang thực thi).

### Section 3 — Các ví dụ ứng dụng thực tiễn

2-3 ví dụ (`<h3>` đánh số `3.1`, `3.2`, `3.3`), đúng khuôn:
`<p>` mô tả bối cảnh ví dụ → problem-box "Yêu cầu bài toán" → Code Sandbox hoàn chỉnh giải quyết
trọn vẹn bài toán đó → (tùy chọn) `<ul>` giải thích nếu ví dụ có điểm kỹ thuật mới chưa nói ở
Section 2.

**Nguyên tắc tiến triển độ khó (progressive complexity)**: ví dụ sau phải khó hơn hoặc kết hợp
thêm 1 khía cạnh mới so với ví dụ trước (vd bài mẫu: 3.1 lặp số nguyên đơn giản → 3.2 thêm bước
nhảy + tính toán → 3.3 chuyển sang duyệt chuỗi + rẽ nhánh điều kiện lồng bên trong).

### Section 4 — Tổng kết bài học

Gồm 2 mục con cố định:

- **`4.1. Kiến thức trọng tâm`**: `<ul>` 3-5 gạch đầu dòng, mỗi dòng súc tích ≤ 1 câu, tóm tắt đúng
  các cú pháp/khái niệm đã dạy ở Section 2 — KHÔNG lặp lại nguyên văn câu chữ đã dùng, phải diễn
  đạt cô đọng hơn.
- **`4.2. Các lỗi thường gặp & Lưu ý thực tế`**: 2-3 khối **gotcha-box** (màu rose), mỗi khối gồm:
  - `<h4>` tên lỗi ngắn gọn (vd "Lỗi thiếu giá trị cuối cùng (Off-by-one Error)").
  - `<p>` giải thích NGUYÊN NHÂN lỗi.
  - **1 cặp code block SAI → ĐÚNG** (2 khối `<pre><code class="hljs language-...">`, KHÔNG dùng
    sandbox thực thi ở đây — chỉ hiển thị đối chiếu tĩnh, có header giả lập cửa sổ terminal 3 chấm
    tròn đỏ/vàng/xanh + nút "Sao chép").

### Section 5 — Tài liệu tham khảo & Câu hỏi ôn tập

1. `<ul>` link tham khảo chính thức (ưu tiên tài liệu hãng/ngôn ngữ chính thức, KHÔNG dùng blog cá
   nhân/nguồn không đáng tin), mỗi link có icon `ph-link`, mở tab mới (`target="_blank"`).
2. **Bộ câu hỏi ôn tập (Self-Test)** — xem mục 6.3.

---

## 6. Component Catalog (Khối nội dung chuẩn tái sử dụng)

### 6.1 Code Sandbox (thực thi được)

```
┌───────────────────────────────────────────── [↺] [▶] [⧉] ┐
│  <code contenteditable> ... code có thể sửa trực tiếp ... │
└─────────────────────────────────────────────────────────┘
  (ẩn cho tới khi bấm ▶) ──▶
┌─────────────────────────────────────────────────────────┐
│ KẾT QUẢ THỰC THI (CONSOLE OUTPUT):                        │
│  > output thật từ engine thực thi                         │
└─────────────────────────────────────────────────────────┘
```

- Container ngoài: `border border-slate-200 rounded-xl overflow-hidden shadow-sm my-5 bg-slate-50`.
- Vùng code: `contenteditable="true"`, `spellcheck="false"`, lưu bản gốc vào `data-original` (dùng
  cho nút ↺ khôi phục), highlight bằng `hljs` với `language-{ngôn ngữ tương ứng}`.
- 3 nút góc phải: **↺ Khôi phục** (`clearSandbox`), **▶ Chạy** (gọi hàm thực thi tương ứng
  `engine_type`), **⧉ Sao chép** (`copySandboxCode`).
- Vùng output: ẩn mặc định (`hidden`), hiện ra khi bấm Chạy, nền trắng, font mono, có nhãn
  "KẾT QUẢ THỰC THI (CONSOLE OUTPUT):" kèm icon terminal.

**Lựa chọn Engine (`engine_type`) — BẮT BUỘC chọn đúng theo bản chất công nghệ, không hard-code:**

| `engine_type` | Dùng khi | Hàm JS thực thi |
|---|---|---|
| `pyodide` | Tech stack là Python | `runPythonCode()` — nạp Pyodide Wasm, chạy Python thật trong trình duyệt |
| `js_worker` | Tech stack là JavaScript/TypeScript | `runJsCode()` — chạy bằng `new Function()`, bắt `console.log/warn/error` |
| `sql_sim` | Tech stack là SQL/Database | `runSqlCode()` — dùng AlaSQL mô phỏng truy vấn trong trình duyệt |
| *(không set)* | CLI/Terminal, Git, Bash, DevOps, cấu hình... | KHÔNG dùng sandbox thực thi — chỉ hiển thị **block code tĩnh** cho phép copy (xem mục 6.1.1) |

#### 6.1.1 Block Code tĩnh (static, không sandbox)

Áp dụng cho lệnh CLI/terminal/config/SQL DDL thuần túy không có "output" thực sự ý nghĩa khi chạy
độc lập trong sandbox trình duyệt (vd `git commit -m "..."`, nội dung file `.yaml`/`.env`). Trình
bày dạng "cửa sổ terminal giả lập": header có 3 chấm tròn (đỏ/vàng/xanh, tái tạo cảm giác cửa sổ
macOS terminal), nhãn "Cú pháp mẫu {ngôn ngữ}", nút "Sao chép" duy nhất (không có nút Chạy/Khôi
phục vì không thực thi được). **Không được lồng CLI/config vào code sandbox thực thi** — đây là
lỗi đã ghi nhận thực tế (sandbox báo lỗi/không chạy được với lệnh CLI).

### 6.2 Step-by-Step Execution Visualizer (bắt buộc ở cuối Section 2)

Bố cục 2 cột trong 1 khung `bg-slate-50 border rounded-2xl p-5`:

```
┌─────────────────────────────┬─────────────────────────────┐
│ MÃ NGUỒN THỰC THI            │ TRẠNG THÁI BIẾN TRONG RAM    │
│  từng dòng có id viz-line-N  │  mỗi biến 1 dòng, giá trị    │
│  dòng đang chạy: highlight   │  đổi màu xanh emerald khi    │
│  amber + border trái         │  vừa cập nhật rồi fade về    │
├─────────────────────────────┴─────────────────────────────┤
│ [◀ Bước trước] [Tiếp theo ▶] [↺ Đặt lại]   [Tự động chạy]  │
├─────────────────────────────────────────────────────────┤
│ NHẬT KÝ THỰC THI (terminal, tích lũy log từng bước đã qua) │
└─────────────────────────────────────────────────────────┘
```

- Dữ liệu từng bước nạp qua biến JS `window.vizSteps` (mảng object `{line, ram: {...}, log, badge}`)
  — line trỏ đúng `id="viz-line-N"` tương ứng dòng code.
- Nút "Tự động chạy" tự động next từng bước cách nhau 1.8s, đổi label "Tạm dừng" khi đang chạy.
- Badge trạng thái góc trên-phải code (`#viz-step-badge`): "Sẵn sàng" (mặc định) → "Bước N/Tổng".

### 6.3 Self-Test Quiz (Section 5)

- 3-4 câu trắc nghiệm (KHÔNG phải tự luận như bản PDF cũ — trắc nghiệm cho phép chấm/giải thích
  tức thời tự động trên trình duyệt).
- Mỗi câu: số thứ tự badge tròn xám, nội dung câu hỏi neo THẲNG vào ví dụ/tình huống cụ thể đã học
  trong bài (không hỏi lý thuyết trừu tượng chung chung), 4 lựa chọn `A-D` dạng radio.
- Bấm "Nộp bài" → chấm client-side, mỗi câu hiện khối giải thích màu theo kết quả (xanh emerald =
  đúng, đỏ rose = sai kèm đáp án đúng, vàng amber = chưa chọn), cuối cùng hiện tổng điểm `N/Tổng`.
  Có nút "Làm lại" reset toàn bộ.
- 3 mức độ câu hỏi khuyến nghị (kế thừa tinh thần chuẩn cũ): (1) hiểu bản chất/dự đoán kết quả với
  input cho trước, (2) vận dụng — đổi tham số, dự đoán kết quả mới, (3) suy luận ngược/phân tích
  lỗi — cho kết quả/lỗi, hỏi nguyên nhân hoặc điều kiện đầu vào.

### 6.4 Sơ đồ SVG minh họa (Section 1, và tùy chọn ở nơi khác)

- Tự vẽ bằng SVG (KHÔNG dùng ảnh raster generic không liên quan bài học), bố cục 3 khối ngang nối
  bằng mũi tên có nhãn hành động (vd "Nạp dữ liệu", "Xuất kết quả"):
  1. **Khối trái** (nền `#f8fafc`, header đen `#0f172a`): Input/dữ liệu đầu vào của kịch bản.
  2. **Khối giữa** (nền `#f0f9ff`, header xanh dương `#0284c7`): mô phỏng đúng cú pháp/cơ chế đang
     dạy — có thể nhúng 1 đoạn code rút gọn dạng "code trong khối màu tối" để trực quan.
  3. **Khối phải** (nền `#faf5ff`, header tím `#7e22ce`): Output/kết quả xử lý.
- Bắt buộc `class="rikkei-diagram"` (đảm bảo responsive, `max-width:100%`), có `<figcaption>` mô tả
  đầy đủ ý nghĩa hình (định dạng "Hình X.Y: mô tả...").
- Wrap trong `<figure class="my-6 text-center max-w-[900px] mx-auto">`.

---

## 7. Thiết kế "Bài toán" (Problem Design Guidelines)

1. **Một kịch bản nghiệp vụ, nhiều bài toán con**: chọn 1 bối cảnh doanh nghiệp cụ thể cho toàn bài
   (không đổi giữa các section), rồi chia thành các bài toán con nhỏ tương ứng từng mục cú pháp/ví
   dụ — mỗi bài toán con nêu trong khối "Yêu cầu bài toán" (sky-box) ngay trước code sandbox liên
   quan.
2. **Số liệu cụ thể, không trừu tượng**: bài toán phải có số liệu/tên riêng thực tế (vd "5 sản
   phẩm", "mã voucher 'SUPER2024'"), không dùng biến chung chung `a, b, x, y, temp`.
3. **Domain phải khớp Domain SSOT của Session** (nếu hệ thống đã ấn định domain thống nhất cho
   session qua `core.domain_knowledge.get_domain_for_session()`, bài đọc PHẢI dùng đúng domain đó
   — không tự bịa domain khác biệt với các tài nguyên khác cùng session).
4. **Phạm vi kiến thức (Scope Boundary)**: bài toán chỉ được dùng cú pháp/khái niệm đã học tính đến
   lesson hiện tại — tuyệt đối không dùng trước cú pháp của lesson/session sau (kiểm tra qua
   `allowed_scope`/`forbidden_scope`).
5. **Tính giải quyết được trọn vẹn**: bài toán ở Section 1 (đặt vấn đề) phải được GIẢI QUYẾT THỰC
   SỰ bằng 1 trong các ví dụ ở Section 3 — không đặt vấn đề rồi bỏ lửng.

---

## 8. Văn phong & Ngôn ngữ

- 100% tiếng Việt có dấu chuẩn sản xuất, văn phong đối thoại gần gũi (không hàn lâm khô cứng), giữ
  thuật ngữ kỹ thuật bằng tiếng Anh khi là tên hàm/từ khóa (`for`, `range()`, `range`).
- Nghiêm cấm: emoji dạng text, từ ngữ sáo rỗng kiểu AI ("thực chiến", "khai phá", "vô cùng", "tuyệt
  vời", "bậc nhất", "triệt để" — bị strip tự động ở tầng code, nhưng người biên soạn không nên dùng
  từ đầu).
- Tiêu đề bài học (H1) phải là tên chủ đề THUẦN TÚY, không chứa tiền tố "Session XX -"/"Lesson YY -".

---

## 9. Checklist tuân thủ (dùng để tự kiểm tra trước khi coi 1 bài đọc là đạt chuẩn)

- [ ] Đúng 5 section theo bảng mục 2, đủ `id="section-N"`.
- [ ] Toàn bài dùng đúng 1 kịch bản nghiệp vụ thống nhất, khớp Domain SSOT của session.
- [ ] Section 1 có tình huống cụ thể + 1 sơ đồ SVG minh họa 3 khối.
- [ ] Section 2: mỗi mục con có đủ khuôn khái niệm → yêu cầu bài toán → sandbox → giải nghĩa cú
      pháp; mục con cuối có Step-by-Step Visualizer.
- [ ] Section 3: 2-3 ví dụ tiến triển độ khó, giải quyết trọn vẹn bài toán Section 1.
- [ ] Section 4: đủ 4.1 (kiến thức trọng tâm) + 4.2 (2-3 gotcha-box có cặp code sai/đúng).
- [ ] Section 5: link tham khảo chính thức + 3-4 câu self-test trắc nghiệm neo vào ví dụ thật.
- [ ] `engine_type` sandbox chọn đúng theo tech_stack (Pyodide/JS Worker/AlaSQL/không sandbox cho CLI).
- [ ] Không vi phạm Zero-italic policy, không dùng AI cliché, không lộ prefix "Session/Lesson" ở H1.
- [ ] Không dùng cú pháp/khái niệm vượt phạm vi đã học (scope boundary).
