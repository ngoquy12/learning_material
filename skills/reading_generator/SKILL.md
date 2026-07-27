---
name: reading_generator
description: Generate rich, scientific, scannable educational reading materials with bullet/subbullet lists, centered 16:9 visual problem scene images, Mermaid flowcharts, Good vs Bad code comparison cards, Note/Warning callouts, and PEP 8 English snake_case conventions.
---

# Kỹ năng Xây dựng Bài đọc Học liệu Chuẩn Sư phạm Doanh nghiệp (Enterprise Educational Reading Skill)

## 1. Triết lý Đào tạo & Trình bày Khoa học (Educational & Pedagogical Standards)
Tài liệu bài đọc tự học (`reading.html`) đóng vai trò là **Nguồn Sự Thật Duy Nhất (Single Source of Truth - SSOT)** cho toàn bộ môn học. Tất cả các tài nguyên khác (Slide, Quiz, Kịch bản Video, Mindmap) đều được trích xuất từ bài đọc này.

### 1.1. Quy tắc Trình bày Khoa học & Ngắt Ý bằng Markdown Lists / Sublists (Scannable Bullet Structure):
1. **CẤM VIẾT ĐOẠN VĂN DÀI DÒNG**: Tuyệt đối không viết các đoạn văn bản dài tràn lan không có ngắt ý. Mọi nội dung phân tích lý thuyết, cơ chế vận hành hay hướng dẫn kỹ thuật **BẮT BUỘC PHẢI DÙNG DẠNG LIST (`- Ý chính`) VÀ SUBLIST (`  - Chi tiết hỗ trợ`)**.
2. **Ngắt câu rõ ràng & Bôi đậm Từ khóa**:
   - Ý chính: Ngắn gọn từ 1 - 2 câu ngắt rõ ràng, bôi đậm (**bold**) các từ khóa chuyên môn cốt lõi.
   - Sublist ý phụ: Làm rõ bản chất kỹ thuật, tác động tới bộ nhớ/hiệu năng hoặc lưu ý khi triển khai.
3. **Mẫu cấu trúc List sư phạm**:
   - **Tên Khái niệm / Cơ chế**: Mô tả bản chất trong 1 câu ngắn gọn.
     - **Cơ chế hoạt động**: Chi tiết cách hệ thống xử lý từng bước.
     - **Tác động thực tế**: Đánh giá ảnh hưởng tới hiệu năng và bảo trì mã nguồn.

---

### 1.2. Quy tắc Chèn Hình Ảnh Trực Quan Bối Cảnh Bài Toán (Mandatory 16:9 Centered Scene Image):
1. **BẮT BUỘC CHÈN HÌNH ẢNH BỐ CẢNH 16:9**: Bên cạnh sơ đồ luồng Mermaid và khung chạy code, **mỗi bài đọc BẮT BUỘC phải có 1 Hình ảnh Trực quan mô tả bài toán/bối cảnh thực tế** của bài học ở ngay phần Đặt Vấn Đề (Bước 1).
   - *Ví dụ bài Vòng lặp (Loops)*: Hình ảnh 16:9 mô tả sự vất vả khi lập trình viên phải chép đi chép lại thủ công 100 câu lệnh giống hệt nhau so với việc dùng 1 vòng lặp thông minh.
   - *Ví dụ bài Khai báo Biến (Variables)*: Hình ảnh 16:9 mô tả các ô chứa đồ đóng nhãn trong kho hàng tương ứng với các vùng nhớ RAM.
2. **Quy chuẩn Định dạng & Hiển thị Hình ảnh**:
   - **Tỷ lệ khung hình**: `16:9` (`aspect-ratio: 16/9`).
   - **Bố cục căn chỉnh**: Căn giữa chiều ngang tuyệt đối (`margin: 0 auto; display: block; max-width: 800px; width: 100%;`).
   - **Khung chứa & Shadow**: Bo góc tròn `border-radius: 12px`, đổ bóng mờ `box-shadow: 0 4px 20px rgba(0,0,0,0.08)`, có viền nhẹ `border: 1px solid var(--border-color)`.
   - **Chú thích ảnh (Caption)**: Đặt ngay bên dưới ảnh dạng nghiêng `font-style: italic`, chữ nhỏ màu xám nhạt căn giữa.

---

### 1.3. Quy tắc Mã Nguồn & Coding Conventions (PEP 8 Standards):
1. **Ràng buộc Tên biến & Tên hàm bằng Tiếng Anh `snake_case`**:
   - Tất cả mã nguồn ví dụ (Python) **BẮT BUỘC phải dùng tên biến, tên hàm, tên hằng số bằng TIẾNG ANH CÓ Ý NGHĨA dạng `snake_case`** (ví dụ: `user_age`, `rectangle_width`, `total_price`, `calculate_area()`).
   - **TUYỆT ĐỐI CẤM** dùng tên biến tiếng Việt không dấu (như `chieu_dai`, `nhap_chieu_rong`, `bien1`, `temp`, `a`, `b` không có ý nghĩa).
2. **Mã nguồn Đối chiếu Chuẩn doanh nghiệp**:
   - **Mã nguồn Đúng (GOOD Practice)**: Viết mã chuẩn Best Practice, ngắn gọn, minh bạch có comment giải thích lý do.
   - **Mã nguồn Sai (BAD Practice / Anti-pattern)**: Viết mã nguồn dễ gây bẫy lỗi hoặc kém hiệu quả kèm comment giải thích hậu quả.

---

### 1.4. Loại bỏ Từ khóa Dư thừa & Chuẩn hóa Nhãn Thuần (Clean Pedagogical Labels):
1. **TUYỆT ĐỐI CẤM DÙNG TỪ KHÓA W3SCHOOLS**: Không đưa từ "W3Schools" vào tiêu đề, nội dung hay bảng so sánh để tránh tạo cảm giác đi sao chép. Thay bằng các cụm từ chuẩn mực sư phạm doanh nghiệp.
2. **TẠM TẠM BỎ CÁC TEXT BỌC TRONG NGOẶC VUÔNG `[...]`**:
   - Thay `[NOTE]` -> `Lưu ý:`
   - Thay `[WARNING]` -> `Cảnh báo:`
   - Thay `[TIP]` -> `Mẹo:`
   - Thay `[BEST PRACTICE]` -> `Thực hành tốt:`
   - Thay `[ANTI-PATTERN]` -> `Mẫu nên tránh:`
   - Thay `[YÊU CẦU]` -> `Yêu cầu:`

---

## 2. Cấu Trúc Bố Cục Bài Đọc Chuẩn Sư Phạm Doanh Nghiệp

```
+───────────────────────────────────────────────────────────────────────────────────────────────+
| [Header/Navbar]  TÊN MÔN HỌC & BÀI HỌC • Badges: [Chuẩn Sư Phạm • Doanh Nghiệp]               |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 1. BỐ CẢNH & BÀI TOÁN THỰC TẾ (Introduction & Context)                                        |
|    • HÌNH ẢNH TRỰC QUAN 16:9 CĂN GIỮA (Illustration Scene Image aspect 16:9 centered)        |
|      [Caption chú thích hình ảnh bối cảnh bài toán...]                                       |
|    • List ngắt ý khoa học (- Ý chính, sub-bullet chi tiết) phân tích bối cảnh.              |
|    • Lưu ý: Nhấn mạnh điểm quan trọng trong bối cảnh.                                         |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 2. PHÂN TÍCH BẢN CHẤT KỸ THUẬT & CƠ CHẾ NỘI BỘ (Technical Internals)                          |
|    • List ngắt ý khoa học phân tích cơ chế bộ nhớ, thông dịch, Bytecode, PVM.                 |
|    • BẢNG SO SÁNH MARKDOWN KỸ THUẬT (Technical Comparison Table full-width).                 |
|    • Mẹo: Mẹo tối ưu cấu trúc mã nguồn.                                                      |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 3. GIẢI PHÁP KỸ THUẬT & SƠ ĐỒ LUỒNG (Architecture & Flow)                                     |
|    • SƠ ĐỒ MERMAID DIAGRAM (flowchart TD / sequenceDiagram) giải thích luồng thực thi.        |
|    • Cấu trúc mã nguồn chuẩn Best Practice vs Anti-Pattern.                                   |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 4. QUY CHUẨN MÃ NGUỒN & PHÂN TÍCH THỰC THI (Code & Console Analysis)                          |
|    • Khối code minh họa Python tuân thủ PEP 8 English snake_case.                            |
|    • Nút ▶ Thử chạy Pyodide WebAssembly và Nút Sao chép.                                      |
|    • Phân tích Console Output và luồng chạy từng dòng.                                        |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 5. KHẢO THÍ & ĐÁNH GIÁ NĂNG LỰC TỰ HỌC (Self-Test Accordion)                                 |
|    • Bộ 3 câu hỏi khảo thí tự luyện dạng thẻ nhấp mở gợi ý đáp án.                            |
|    • **BẮT BUỘC**: Text câu hỏi và câu trả lời **CĂN GIỮA 100%** (`text-align: center`).      |
|    • **BẮT BUỘC**: Có tính năng **ĐÓNG / MỞ ĐỘNG** (Collapsible toggle state).                |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 6. TÀI LIỆU THAM KHẢO CHÍNH THỨC (Official References)                                        |
|    • Danh sách đường dẫn tài liệu chính thức (PEP, Python Docs, Official Specs).              |
+───────────────────────────────────────────────────────────────────────────────────────────────+
| 7. LƯU Ý QUAN TRỌNG & BẪY LẬP TRÌNH (Important Warnings & Runtime Pitfalls)                   |
|    • Cảnh báo: Cảnh báo các bẫy lỗi đắt giá (IndentationError, TypeError...) bôi đậm.        |
+───────────────────────────────────────────────────────────────────────────────────────────────+
```

> [!IMPORTANT]
> **QUY TẮC CĂN GIỮA VÀ ĐÓNG MỞ PHẦN KHẢO THÍ & ĐÁNH GIÁ NĂNG LỰC TỰ HỌC:**
> 1. **Căn Giữa Text (`text-align: center`)**:
>    - Tiêu đề câu hỏi (`.selftest-question`) và nội dung câu trả lời (`.selftest-answer`) **BẮT BUỘC** phải được căn giữa chiều ngang (`text-align: center !important; justify-content: center !important;`).
> 2. **Đóng / Mở Động (Collapsible Accordion Toggle)**:
>    - Khi nhấp vào tiêu đề câu hỏi, khối thẻ phải tự động bật/tắt hiển thị câu trả lời (`onclick="this.parentElement.classList.toggle('active')"` hoặc dùng `<details class="selftest-item"><summary class="selftest-question">...` ). Mũi tên indicator tự động xoay chuyển chỉ báo trạng thái.

---

---

## 3. Quy Chuẩn Kỹ Thuật JavaScript & Chống Reload Trang (Strict JS & Anti-Reload Rules)
1. **Bắt buộc 100% thẻ `<button>` phải khai báo `type="button"`**:
   - Mọi nút bấm trong giao diện bài đọc và bảng điều khiển trực quan hóa (Visualizer Panel) tuyệt đối phải ghi rõ `<button type="button" ...>` để ngăn ngừa hành vi tự động reload/submit form của trình duyệt.
2. **Chống Reload khi click hoặc bấm Enter**:
   - Tất cả các sự kiện click, gõ phím trong form hoặc input phải có `event.preventDefault()` để tránh làm trang bị tải lại.
3. **Mã nguồn Trực quan hóa chi tiết (Detailed Code Visualizer Logic)**:
   - Bộ Visualizer phải mô phỏng chính xác từng bước chạy mã nguồn theo thời gian thực (Step-by-step Execution Tracker).
   - Phải có 3 phân vùng hiển thị đồng bộ:
     a) **Code Tracker Box**: Highlight dòng lệnh đang chạy (`.active-line`).
     b) **Memory State / Variable Table**: Hiển thị tên biến, kiểu dữ liệu và giá trị biến thay đổi theo từng bước.
     c) **Console Execution Log**: Nhật ký log hiển thị kết quả in ra màn hình hoặc trạng thái hệ thống.
4. **Cô lập Scope JavaScript**:
   - Mã nguồn JS phải tự chứa (self-contained), khai báo biến và hàm chuẩn xác, không được dùng stub `// todo` hay dùng biến chưa khai báo.

---

## 4. Quy Tắc Phân Loại 7 Dạng Bài Đọc (Smart 7-Type Rules)
1. `SETUP_GUIDE`: Cài đặt & Môi trường -> Timeline các bước CLI, Terminal code, Version check.
2. `TECH_COMPARISON`: So sánh công nghệ -> Bảng so sánh 4 cột Full-width, Sơ đồ so sánh luồng.
3. `SYNTAX_OPERATIONS`: Cú pháp & Thao tác -> Syntax spec, Pyodide Sandbox, Bảng phương thức.
4. `ALGORITHM_PATTERN`: Thuật toán & Bài toán -> Flowchart bài toán, Phân tích độ phức tạp O(N), Step tracker.
5. `SYSTEM_WORKFLOW`: Kiến trúc hệ thống -> System diagram (Client <-> API <-> DB), Phân rã module.
6. `DEBUG_REFACTOR`: Refactoring & Debug -> Anti-pattern vs Clean Code, Exception flow, Checklist.
7. `THEORY_CONCEPT`: Khái niệm & Lý thuyết -> Đặt vấn đề, Internals bộ nhớ/PVM, Memory Diagram, Gotchas.

---

## 5. Tiêu Chuẩn Phê Duyệt Bài Đọc (Approval Rubric)
1. **Độ chính xác ngữ cảnh**: Bài đọc chỉ tập trung 100% vào nội dung Lesson hiện tại, không rò rỉ môn khác hay kiến thức chưa học.
2. **Độ sâu học thuật**: Bài đọc đầy đủ 800 - 1,200 từ, giải thích sâu cơ chế nội bộ.
3. **Trình bày khoa học dạng List**: Mọi đoạn lý thuyết dài đều được ngắt ý khoa học dạng List/Sublist.
4. **Có Hình ảnh bối cảnh 16:9 căn giữa**: Có khối hình ảnh 16:9 mô tả bối cảnh bài toán ở Bước 1.
5. **Có khối Good vs Bad Code**: Bắt buộc có khối ví dụ đối chiếu mã chuẩn Best Practice vs Mã sai Anti-pattern.
6. **Trực quan hóa hoạt động**: Khung Pyodide / Code Tracker / Playground hoạt động tương tác thực sự trên trình duyệt, không reload trang.
