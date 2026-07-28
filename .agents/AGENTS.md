# Project Rules & Customizations — Quy Chuẩn Thiết Kế Hệ Thống Học Liệu Rikkei Education

Tài liệu này tổng hợp toàn bộ quy chuẩn thiết kế sư phạm, kỹ thuật và trình bày giao diện áp dụng thống nhất cho tất cả các tài nguyên học liệu (Bài đọc, Bài tập, Mini Project / Lab, Quizz trắc nghiệm, Slide bài giảng, Video sản xuất HyperFrames, Visualizer / Mindmap).

---

## 1. Bài Đọc Học Liệu (Reading Material Standard — `reading.html`)

Tài liệu Bài đọc là **Nguồn Sự Thật Duy Nhất (Single Source of Truth - SSOT)** cho toàn bộ khóa học.

### 1.1. Bố cục & Trình bày Sư phạm
1. **Cấu trúc List / Sublist (Scannable Bullet Structure)**:
   - **TUYỆT ĐỐI CẤM VIẾT ĐOẠN VĂN DÀI DÒNG**: Mọi nội dung phân tích lý thuyết, cơ chế vận hành hay hướng dẫn BẮT BUỘC dùng dạng list (`- Ý chính`) và sublist (`  - Chi tiết hỗ trợ`).
   - **Bôi đậm Từ khóa**: Mỗi ý chính ngắt từ 1-2 câu ngắn gọn, bôi đậm (**bold**) từ khóa chuyên môn cốt lõi.
2. **Hình ảnh Trực quan Bối cảnh 16:9 (Mandatory Scene Image)**:
   - Ngay Bước 1 (Đặt vấn đề), BẮT BUỘC chèn 1 Hình ảnh Trực quan mô tả bối cảnh thực tế/bài toán của bài học.
   - Định dạng: Tỷ lệ `16:9`, max-width `800px`, căn giữa (`margin: 0 auto`), `border-radius: 12px`, `box-shadow: 0 4px 20px rgba(0,0,0,0.08)`, viền nhẹ `border: 1px solid var(--border-color)`. Chú thích ảnh nghiêng bên dưới.
3. **Mã nguồn & Code Comparison Cards**:
   - **GOOD Practice (Mã nguồn Chuẩn)**: Viết mã chuẩn Best Practice, ngắn gọn, minh bạch, có comment giải thích.
   - **BAD Practice (Anti-pattern)**: Viết mã nguồn dễ gây lỗi/kém hiệu quả kèm comment giải thích hậu quả.
4. **Khảo thí & Đánh giá năng lực tự học (Self-Test & Accordion Component Rules)**:
   - **Strict Left-Alignment**: `.selftest-question` BẮT BUỘC dùng `justify-content: flex-start !important; gap: 8px !important; text-align: left !important;`. CẤM dùng `space-between`.
   - `.selftest-answer` và các phần tử con BẮT BUỘC có `text-align: left !important;`.
   - CSS Standard:
     ```css
     .selftest-question { font-weight: 600; color: var(--primary); cursor: pointer; text-align: left !important; display: flex; align-items: center; justify-content: flex-start !important; gap: 8px !important; }
     .selftest-answer { margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border-color); display: none; color: var(--text-main); text-align: left !important; }
     .selftest-answer * { text-align: left !important; }
     ```

---

## 2. Bài Tập (Exercise Standard — 6 Real-World Exercises)

Bộ 6 bài tập thiết kế theo vai trò dự án thực tế doanh nghiệp (LMS, Điểm danh, Tool Khảo thí...), KHÔNG dùng bài tập thuật toán khô khan (như in hình sao, tính giai thừa).

### 2.1. Phân bổ Cấp độ Nhận thức Bloom (6 Bài)
- **I. VẬN DỤNG CƠ BẢN (Bài 1 & Bài 2)**: Cung cấp sẵn code có lỗi logic/thiếu sót → Yêu cầu học viên trace code và sửa lỗi.
- **II. VẬN DỤNG CHUYÊN SÂU (Bài 3 & Bài 4)**: Đóng vai Backend Dev nhận Task mới → Xử lý Business Rules phức tạp và Edge Cases.
- **III. PHÂN TÍCH (Bài 5)**: Tối ưu hóa quy trình hệ thống cũ → Học viên đưa ra ít nhất 2 giải pháp, so sánh ưu/nhược điểm và vẽ sơ đồ luồng (Flowchart) trước khi code.
- **IV. SÁNG TẠO (Bài 6)**: Thiết kế Mini Project / Module hoàn chỉnh dạng Menu (Console hoặc UI) → Tự liệt kê kịch bản lỗi, bẫy lỗi ở mọi thao tác.

### 2.2. Quy chuẩn Định dạng Code Mẫu
- **100% Tiếng Anh**: Tên biến, tên hàm, class, thuộc tính trong code BẮT BUỘC dùng Tiếng Anh có ý nghĩa (`user_age`, `calculate_gpa`). CẤM dùng tiếng Việt không dấu (`chieu_dai`, `bien1`, `temp`).
- **Naming Conventions**: Python/Database dùng `snake_case` (`student_list`, `calculate_gpa`). JavaScript/TypeScript/Java dùng `camelCase` hoặc `PascalCase` (`studentList`, `calculateGpa`).

---

## 3. Bài Thực Hành Lab & Mini Project (Lab Standard)

Bài thực hành Lab là xương sống phát triển kỹ năng thực chiến và tích lũy các cấu phần cho dự án cuối khóa.

### 3.1. Cấu trúc 3 Phần Chuẩn hóa
1. **Mục tiêu (Objectives)**: Nêu 2-3 kỹ năng cụ thể làm chủ + xác định rõ đầu ra kỳ vọng (*"Đạt chuẩn đầu ra kỳ vọng: hoạt động ổn định, không lỗi logic."*).
2. **Mô tả & Các bước thực hiện (Description & Steps)**: Nêu rõ tài nguyên đầu vào + danh sách các bước thực hiện theo thứ tự (Bước 1, Bước 2, Bước 3...) chi tiết, có thể thực thi ngay.
3. **Checklist Đánh giá Định lượng (Evaluation Checklist)**: Bảng kiểm `[ ]` định lượng để học viên tự kiểm tra (VD: `[ ] API GET /items trả về danh sách đầy đủ`, `[ ] Bắt lỗi HTTP 404`).

---

## 4. Khảo Thí & Ngân Hàng Câu Hỏi Trắc Nghiệm (Quizz Standards)

### 4.1. 7 Nguyên Tắc Sư Phạm Quizz
1. **Đơn nhiệm (Single Concept)**: Mỗi câu hỏi chỉ đánh giá 1 kiến thức/kỹ năng duy nhất.
2. **Ngữ cảnh hóa (Context-Driven)**: Đặt học viên vào tình huống nghiệp vụ thực tế (Scenario), không hỏi lý thuyết suông.
3. **Phương án nhiễu thông minh (Plausible Distractors)**: Các đáp án sai dựa trên lỗi thực tế hay gặp của học viên. CẤM đáp án dạng *"Cả 3 đáp án trên đều đúng/sai"*.
4. **Đồng nhất (Homogeneity)**: Cả 4 phương án (A, B, C, D) tương đồng về độ dài, cấu trúc và phạm vi.
5. **No Clues**: Loại bỏ mọi dấu hiệu mách nước hoặc keyword matching giữa câu hỏi và đáp án.
6. **Khách quan & Chính thống**: Nghiêm cấm dùng từ tham chiếu mờ mịt như *"theo video"*, *"lời giảng viên"*, *"trong slide"*.
7. **Ràng buộc Phạm vi Kiến thức Động (Dynamic Scope Boundary)**: 100% câu hỏi CHỈ thuộc phạm vi kiến thức đã học. TUYỆT ĐỐI CẤM câu hỏi hoặc đáp án chứa khái niệm/công nghệ thuộc bài học tương lai.

### 4.2. Ma Trận Đề Thi
- **Lesson Quiz (5 câu)**: Câu 1 Nhớ (Cú pháp) ➔ Câu 2 Hiểu (Cơ chế luồng) ➔ Câu 3 Vận dụng (Đọc code) ➔ Câu 4 Phân tích (So sánh) ➔ Câu 5 Đánh giá (Dự đoán kết quả có bẫy).
- **Session Entrance Quiz (45 câu đầu giờ)**: Tỷ lệ 30 câu Bài cũ (Vận dụng 12 câu diff 4, Phân tích 9 câu diff 6, Sáng tạo 9 câu diff 8) + 15 câu Bài mới (Thông hiểu 6 câu diff 5, Vận dụng 6 câu diff 7, Phân tích 3 câu diff 9).
- **Session Exit Quiz (45 câu cuối giờ)**: 100% Bài mới (18 câu Vận dụng diff 6, 15 câu Debug diff 10, 12 câu Sáng tạo diff 11).

---

## 5. Slide Bài Giảng Master HTML (Slide Presentation Standard)

Slide là **Công cụ Hỗ trợ Giảng dạy Trực quan** cho Giảng viên trong 1.5 giờ, không phải cuốn sách giáo khoa thu nhỏ.

### 5.1. 8 Quy Tắc Vàng Slide
1. **Giới hạn Slide Count (15-20 Slides/Session)**: Mỗi Session 1.5 giờ tối đa 15-20 slide. Mỗi Lesson 3-4 slide trọng tâm (Problem & Hook ➔ Core Concept & Diagram ➔ Code Demo ➔ Pitfalls & Summary).
2. **Slide Bìa (Cover)**: Tag đỏ tên Session (`Session 01`), tiêu đề chính chữ đen đúp đậm (`#0f172a`), tên môn học chuẩn (`Môn học: Lập trình Python`).
3. **Slide Mục Lục (Agenda)**: Liệt kê đầy đủ Lesson dạng `01. Lesson 01 - ...`. Tiêu đề **`NỘI DUNG BÀI HỌC`** (Montserrat Bold 36px, màu đỏ `#be111c`).
4. **Tiêu đề Lớn Nội dung**: `Lesson XX - Tên Lesson - Số slide` (Màu đỏ `#be111c`, Montserrat Bold 28px).
5. **Tiêu đề Phụ**: Tên chủ đề cụ thể của slide (Chữ màu đen `#0f172a`, Inter Bold 20px).
6. **Typography (Quy tắc 3-30-300)**: Body text 18px, sub-bullets minimum 16px. Mỗi slide max 3 ý chính, mỗi ý max 30 từ. Bôi đậm từ khóa kỹ thuật.
7. **Card Color Coding**: Default (`#f8fafc`), Warning (`#fffbeb` viền cam), Error/Pitfall (`#fef2f2` viền đỏ), Success (`#f0fdf4` viền xanh lá), Info/Best Practice (`#eff6ff` viền xanh dương).
8. **No Emoji**: TUYỆT ĐỐI CẤM EMOJI. Chỉ dùng Phosphor SVG icons hoặc CSS badges.

---

## 6. Sản Xuất Video HyperFrames (Video Production Standard SOP)

Tuân thủ nghiêm ngặt quy trình 8 giai đoạn sản xuất video chuẩn mực.

### 6.1. Voice-UI Separation & Alignment
- **Voice-UI Separation**: TTS Narration = Giọng đọc tự nhiên, câu văn hoàn chỉnh với lời dẫn dắt gợi mở (bối cảnh thực tế ➔ khái niệm ➔ ví dụ ➔ câu chốt). UI = Từ khóa ngắn 3-6 từ, code snippet, sơ đồ diagram, icon vector. KHÔNG chép nguyên câu đọc lên UI card.
- **Bước Duyệt Kịch Bản (Human Review Gate)**: Trình bày `blueprint.json` / `script_review.md` và TẠM DỪNG chờ người dùng duyệt TRƯỚC KHI sinh voiceover AI.
- **Voice-Driven Composition Pipeline**: Script ➔ Approval ➔ Kokoro Voice AI ➔ Audio Probing in `durations.json` ➔ Generate HTML GSAP Compositions driven by probed voice lengths ➔ Puppeteer MP4 Render.
- **Background Music**: Kênh `track-index="99"`, `data-volume="0.12"`, `data-loop="true"`.

### 6.2. Quy chuẩn Thiết kế Video UI (Dark Theme Standard)
- **Background**: Đen thuần `#09090b` / `#0a0a0f`. KHÔNG dùng logo.
- **Title Header**: Top-left (`top: 40px`, `left: 80px`), cỡ chữ 44px Bold 800, màu **Trắng thuần (`#ffffff !important`)**, gạch chân trắng mờ (`rgba(255,255,255,0.15)`).
- **Text & Contrast**: Toàn bộ chữ nội dung màu sáng high-contrast (`#ffffff` / `#e2e8f0` / `#f8fafc`). CẤM chữ xám tối mờ.
- **Font Sizes**: Title 44px, Card Title 28-30px, Desc Text 32px, Bullet Text 26px, Code Body 25px (Fira Code, line-height 1.75).
- **Visual Structure**: Nền card `#13131f`, viền mỏng mờ `border: 1px solid rgba(255,255,255,0.08)`.
- **TUYỆT ĐỐI CẤM `border-left` màu accent** (`border-left: 8px solid #6366f1`): Cấm đường viền màu sặc sỡ bên hông card làm rối mắt.
- **TUYỆT ĐỐI CẤM badge số thứ tự thừa** (`card-badge`, `card-badge-lg`): Chỉ dùng `step-num` tròn nhỏ trong `step-list`.
- **Code Highlighting**: Tiêu chuẩn IDE tối với màu sáng high-contrast (`#d8b4fe` keywords, `#93c5fd` functions, `#6ee7b7` strings, `#fdba74` numbers, `#64748b` comments). Tên hàm/biến BẮT BUỘC giữ nguyên chữ thường đúng cú pháp.

---

## 7. Quy Tắc Hệ Thống Chung (System-Wide Core Rules)

1. **High-Contrast Dark Theme Code Trackers & Code Blocks**:
   - Inside dark-theme code blocks, NEVER use dark inline colors (`#005cc5`, `#032f62`, `#d73a49`).
   - ALWAYS use bright, high-contrast dark theme colors (`#79c0ff` for variables, `#7ee787` for strings/numbers, `#ff7b72` for keywords, `#ffa657` for functions).
2. **100% Accented Vietnamese (Tiếng Việt Có Dấu Chuẩn Sản Xuất)**:
   - All text, titles, questions, answers, SVG labels, and Mermaid flowchart node labels MUST use proper Vietnamese diacritics (dấu tiếng Việt). Never leave un-accented Vietnamese words in production content.
3. **Synchronized Visualizer DOM IDs**:
   - All interactive visualizer JS scripts MUST strictly reference standard HTML DOM element IDs (`#visualizer-canvas`, `#custom-data-input`, `#stepper-progress`, `#stepper-bar`, `#console-output`).
4. **Strict No ALL CAPS Text Standard**:
   - FORBID using ALL CAPS / fully uppercase text in titles, badges, headers, or buttons (NEVER use `text-transform: uppercase` or ALL CAPS strings like `TIẾN TRÌNH LUỒNG CHẠY`, `BẢNG SO SÁNH`, `CODE TRACKER`, `NHẬT KÝ THUẬT TOÁN`).
   - ALWAYS use proper Sentence case or Title case (e.g. `Tiến trình luồng chạy`, `Bảng so sánh đặc tính kỹ thuật`, `Code Tracker (Python/Core)`, `Nhật ký thuật toán`).
5. **No Forced Generic Comparison Tables**:
   - DO NOT forcibly inject a generic C/C++/Java comparison table into every lesson. Only include a comparison table if comparing two contrasting concepts (e.g. `for` vs `while`, `break` vs `continue`).
6. **Dark Terminal Console Output Component**:
   - Never output console results as plain `<li><code>` items. Always wrap in a Dark Terminal container with `JetBrains Mono` font, `#4ade80` green text, `>_ Console Output` header bar, and `● Executed Successfully` status tag.
