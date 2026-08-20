# QUY ĐỊNH VÀ TIÊU CHUẨN THIẾT KẾ BÀI ĐỌC & BÀI TẬP HỌC LIỆU
### Hệ thống Đào tạo Công nghệ Thông tin Rikkei Education — Tiêu chuẩn Sản xuất Chuẩn mới

---

## 1. NGUYÊN TẮC CỐT LÕI: "STORYTELLING IN TECH & PROBLEM-FIRST"

Mỗi bài học trong hệ thống học liệu Rikkei Education không phải là một tài liệu liệt kê định nghĩa khô khan theo lối mòn giáo trình truyền thống. Mọi tài nguyên học tập đều phải tuân thủ nghiêm ngặt tư duy thiết kế bài giảng dựa trên giải quyết vấn đề thực tế:

```
[Bối cảnh Doanh nghiệp] ➔ [Nỗi đau & Nghẽn cổ chai] ➔ [Giải pháp Kỹ thuật Mới] ➔ [Thực thi Trực quan] ➔ [Lỗi Thường gặp] ➔ [Tự Đánh giá Thực chiến]
```

### 4 Trụ Cột Sư Phạm Bắt Buộc:
1. **Cam kết 1 Bài toán Nghiệp vụ Duy nhất (Single Unified Scenario Contract)**:
   - Mỗi bài học bắt buộc phải thiết lập **đúng một kịch bản bài toán doanh nghiệp cụ thể** ở Phần 1 (Ví dụ: Hệ thống quầy thu ngân Siêu thị MartX, Hệ thống giỏ hàng Shopee, Xử lý giao dịch ngân hàng...).
   - Toàn bộ các ví dụ minh họa, sandbox thực thi, mô phỏng biến và câu hỏi ôn tập xuyên suốt từ Phần 1 đến Phần 5 **phải dùng chung 100% ngữ cảnh, tên biến và luồng nghiệp vụ này**. Nghiêm cấm đổi đề tài lộn xộn giữa các phần trong cùng một bài học.
2. **Triết lý Học Nhanh 10 Phút (10-Minute Micro-Learning)**:
   - Trình bày dạng danh sách gạch đầu dòng phân cấp (`- Ý chính`, `  - Chi tiết bổ trợ`), in đậm (**bold**) các từ khóa kỹ thuật trọng tâm.
   - Tuyệt đối không viết các khối đoạn văn đặc chữ (wall-of-text) kéo dài. Học viên có thể quét nhanh (scan) và nắm trọn vẹn bản chất công nghệ trong vòng 10 phút.
3. **Trực quan hóa Tối đa (Visual-First & Zero Dark Mode)**:
   - 100% bài học phải có ảnh minh họa vector phẳng 2D tỉ lệ 16:9, sơ đồ luồng dữ liệu SVG/Mermaid và sandbox chạy code trực tiếp (Pyodide Wasm Sandbox).
   - Áp dụng triệt để giao diện nền sáng (Light Mode Only), độ tương phản cao, hiện đại và thanh lịch.
4. **Tiêu chuẩn Ngôn ngữ & Chống Văn phong AI Sáo rỗng**:
   - 100% nội dung, nhãn đồ họa và chú thích code viết bằng **Tiếng Việt có dấu chuẩn sản xuất**.
   - **Nghiêm cấm 100% icon emoji văn bản** (❌, ✅, ⚠️, 🔴, ▶). Thay thế hoàn toàn bằng SVG Vector Icons hoặc Phosphor Icons chuyên nghiệp.
   - **Cấm các từ ngữ sáo rỗng / AI markers**: Thay thế từ lóng *"bẫy"*, *"bẫy lập trình"*, *"gotcha"*, *"anti-pattern"* bằng thuật ngữ chuẩn kỹ thuật: *"Lỗi thường gặp"*, *"Sai sót phổ biến"*, *"Ngoại lệ cần lưu ý"*. Loại bỏ các từ khoa trương như *"khám phá"*, *"bí kíp"*, *"thần thánh"*, *"tất tần tật"*.

---

## 2. CẤU TRÚC 5 PHẦN BẮT BUỘC CỦA BÀI ĐỌC (`reading.html`)

| STT | Tên Phần Chuẩn Mới | Tiêu Đề Mục (`<h2>`) | Nội Dung Trọng Tâm & Yêu Cầu Kỹ Thuật |
| :---: | :--- | :--- | :--- |
| **1** | **Bối cảnh & Vấn đề Thực tế** | **Tiêu đề Động** theo bài toán (VD: *1. Tại sao Siêu thị MartX cần Vòng lặp for và Hàm range()?*) | Đưa ra bối cảnh doanh nghiệp, phân tích nỗi đau khi dùng cách làm thủ công, lý do ra đời của công nghệ mới kèm **Ảnh minh họa bối cảnh 16:9 phẳng**. |
| **2** | **Cú pháp & Cơ chế Vận hành** | **Tiêu đề Động** theo kỹ thuật (VD: *2. Cú pháp và Cơ chế Vận hành của Vòng lặp for & Hàm range()*) | Cung cấp Syntax Card chuẩn hóa, danh sách phân tích tham số, **Code Sandbox chạy trực tiếp** và **Bộ mô phỏng cơ chế trực quan (RAM & Log)**. |
| **3** | **Ví dụ Ứng dụng Thực tiễn** | *3. Các ví dụ ứng dụng thực tiễn* | Tối thiểu **3 ví dụ phân tầng lũy tiến** (3.1 Đơn giản ➔ 3.2 Nghiệp vụ ➔ 3.3 Tình huống phức tạp), luôn có **Hộp Yêu cầu bài toán** trước Sandbox. |
| **4** | **Lỗi Thường Gặp & Ngoại Lệ** | *4. Tổng kết bài học & Các lỗi thường gặp* | Bảng so sánh trực quan đối chiếu **Thực hành Xấu (BAD Practice)** vs **Thực hành Tốt (GOOD Practice)** kèm giải pháp khắc phục. |
| **5** | **Tổng kết & Tự Đánh Giá** | *5. Tài liệu tham khảo & Câu hỏi ôn tập* | Bảng tóm tắt Cheatsheet 1 trang, **Bộ 3 câu hỏi trắc nghiệm chống tra cứu**, cụm nút **Nộp bài / Làm lại** căn phải và điểm số tức thì. |

---

## 3. ĐẶC TẢ CHI TIẾT TỪNG PHẦN TRONG BÀI ĐỌC

### 3.1. Phần 1: Bối cảnh Doanh nghiệp & Ảnh Minh Họa 16:9
- **Cấu trúc lời dẫn**:
  - *Đoạn 1 (Bối cảnh)*: Mô tả quy trình thực tế của doanh nghiệp (ví dụ: in 1.000 hóa đơn, lọc mã coupon giảm giá).
  - *Đoạn 2 (Nỗi đau)*: Chỉ ra hậu quả nếu dùng lệnh lặp thủ công (code phình to, dễ sai sót, nghẽn hệ thống).
  - *Đoạn 3 (Giải pháp)*: Giới thiệu cú pháp / công nghệ mới như chìa khóa tự động hóa.
- **Quy chuẩn Ảnh minh họa Bối cảnh (Hình 1.1)**:
  - Tỉ lệ khung hình: `16:9` widescreen, chiều rộng `max-w-[800px]` đến `max-w-[900px]`, căn giữa (`mx-auto`).
  - Thiết kế: Đồ họa Vector SVG 2D phẳng, không bọc các khung thẻ `div` lồng nhau rườm rà.
  - Phân tầng 3 lớp:
    1. **Thẻ Đầu vào (Input)**: Giỏ hàng / Dữ liệu tiếp nhận từ khách hàng.
    2. **Thẻ Động cơ Xử lý (Process Engine)**: Mô phỏng logic code và cơ chế hoạt động.
    3. **Thẻ Kết quả Đầu ra (Output)**: Kết quả hóa đơn/dữ liệu đã xử lý thành công.
  - Mũi tên kết nối (Connectors): Chiều dài tối thiểu `80px - 90px`, nhãn chữ nằm giữa khoảng trống, tuyệt đối không chạm viền thẻ.
  - Chú thích: Thẻ `<figcaption>` in nghiêng font `text-xs text-slate-500` đặt ngay dưới ảnh.

### 3.2. Phần 2: Cú pháp & Cơ Chế Vận Hành
- **Syntax Card Component**: Khung code mẫu nổi bật thể hiện đúng cú pháp chuẩn ngôn ngữ.
- **Danh sách giải thích thành phần**:
  - Dùng code badge `<code class="px-1.5 py-0.5 rounded bg-slate-100 text-rikkei-red font-mono text-sm">...</code>` để làm nổi bật từ khóa và tham số.
  - Giải thích rõ kiểu dữ liệu, giá trị mặc định và giá trị trả về.
- **Bộ Mô Phỏng Cơ Chế Hoạt Động (Interactive Step Mechanism Visualizer)**:
  - Khung code hiển thị số dòng và highlight dòng lệnh đang thực thi (`bg-emerald-50 border-l-4 border-emerald-500`).
  - Bảng giám sát RAM: Cập nhật giá trị biến tức thì theo từng chu kỳ lặp.
  - Dark Terminal Console: Xuất kết quả log màu xanh lá (`#4ade80`) trên nền tối (`#0f172a`).
  - Cụm nút điều khiển: *Quay lại, Tiếp theo, Tự động chạy, Làm lại*.

### 3.3. Phần 3: Bộ Ví Dụ Ứng Dụng Lũy Tiến (Progressive Examples)
Bắt buộc có tối thiểu 3 ví dụ phân tầng theo độ khó tăng dần:
- **Ví dụ 3.1 (Mức Cơ bản)**: Khởi tạo và duyệt dãy số cơ bản.
- **Ví dụ 3.2 (Mức Nghiệp vụ)**: Kết hợp bước nhảy (step) hoặc xử lý điều kiện nghiệp vụ (tính điểm thưởng vị trí lẻ/chẵn).
- **Ví dụ 3.3 (Mức Nâng cao / Xử lý Chuỗi & Ngoại lệ)**: Duyệt từng ký tự, lọc mã voucher coupon kết hợp tích lũy giá trị.
- **Quy chuẩn trước mỗi Sandbox**: Bắt buộc có **Hộp Yêu cầu bài toán** (`p-4 rounded-xl border border-sky-200 bg-sky-50/60 text-slate-800 my-4 shadow-sm`).

### 3.4. Phần 4: Lỗi Thường Gặp & Ngoại Lệ (Gotchas & Best Practices)
- Trình bày theo cặp so sánh đối kháng:
  - **Khối Thực hành Xấu (BAD Practice)**: Minh họa code viết sai logic, thừa thãi hoặc gây tràn bộ nhớ, có comment cảnh báo lỗi.
  - **Khối Thực hành Tốt (GOOD Practice)**: Minh họa code tối ưu, ngắn gọn, chuẩn Clean Code và tuân thủ quy chuẩn ngành.
- Giải thích bản chất tại sao lại xảy ra lỗi và giải pháp phòng tránh triệt để.

### 3.5. Phần 5: Tổng Kết & Bộ Câu Hỏi Ôn Tập Chống Tra Cứu (Anti-AI Self-Test)
- **Thiết kế Bộ 3 Câu hỏi Ôn tập**:
  - *Câu 1 (Thông hiểu)*: Đánh giá bản chất cơ chế hoạt động của cú pháp trong kịch bản bài học.
  - *Câu 2 (Vận dụng)*: Yêu cầu tính toán kết quả đầu ra chính xác khi thay đổi tham số trong kịch bản.
  - *Câu 3 (Phân tích / Xử lý tình huống)*: Phân tích kết quả biến tích lũy hoặc giá trị cuối cùng sau khi chạy xong thuật toán.
  - **Tiêu chuẩn Chống Tra Cứu (Anti-Search / Anti-AI)**: 100% câu hỏi gắn liền với dữ liệu và tên biến độc quyền của bài học (Siêu thị MartX, voucher `SUPER2024`...). Tra Google không thể ra đáp án nếu không đọc bài.
- **Cụm Nút Điều Khiển & Hiển Thị Điểm Số**:
  - Vị trí: Căn sát lề phải (`justify-end gap-3`).
  - Kích thước: Nhỏ gọn, chiều cao thấp (`px-4 py-1.5`, `text-xs font-semibold`).
  - Nút phụ **"Làm lại"**: Nằm bên trái, viền xám `border border-slate-300`, icon `ph-arrow-counter-clockwise`.
  - Nút chính **"Nộp bài"**: Nằm bên phải, nền đỏ thương hiệu Rikkei `bg-rikkei-red hover:bg-red-700`, icon `ph-paper-plane-tilt`.
  - Hộp thông báo kết quả (`#self-test-score`): Alert card xanh dương căn phải, thông báo tổng số câu đúng (VD: `Kết quả: 3/3 câu trả lời đúng.`).
  - Khung giải thích chi tiết: Luôn căn lề trái (`text-align: left !important;`) hiển thị lời giải rõ ràng cho từng câu sau khi bấm nộp bài.

---

## 4. QUY CHUẨN THIẾT KẾ BỘ 6 BÀI TẬP VỀ NHÀ PHÂN TẦNG BLOOM

Bộ bài tập gồm 6 bài toán thực tế tương ứng với các bậc thang nhận thức Bloom, giải quyết các bài toán hệ thống chuyên nghiệp (LMS, Bán hàng, Ngân hàng, Quản lý kho):

```
Tầng I: Nhận biết & Thông hiểu (Bài 1 & 2) ➔ Tầng II: Vận dụng Kỹ thuật (Bài 3 & 4) ➔ Tầng III: Phân tích & Tối ưu (Bài 5) ➔ Tầng IV: Sáng tạo Toàn diện (Bài 6)
```

### 4.1. Phân Phối Chi Tiết 6 Bài Tập

1. **Bài tập 1 & 2 (Tầng I — Vận dụng Cơ bản & Fix Bug Legacy Code)**:
   - Cung cấp đoạn mã nguồn cũ có lỗi logic tiềm ẩn hoặc sai lệch kết quả.
   - Yêu cầu học viên: Trace luồng thực thi, lập bảng testcase (Input/Expected Output/Actual Output) và sửa lại mã nguồn hoàn chỉnh.
2. **Bài tập 3 & 4 (Tầng II — Vận dụng Nâng cao & Backend Development)**:
   - Đóng vai lập trình viên Backend xây dựng module nghiệp vụ mới.
   - Xử lý các quy tắc nghiệp vụ đa tầng (Multi-tier business rules), phân loại đối tượng và bắt các trường hợp biên (Edge cases).
   - Cung cấp sẵn bộ dữ liệu mẫu I/O để học viên kiểm thử.
3. **Bài tập 5 (Tầng III — Phân tích & Tối ưu Hóa Quy Trình)**:
   - Đưa ra một module hệ thống chạy chậm hoặc tốn tài nguyên.
   - Yêu cầu học viên: Đề xuất ít nhất 2 giải pháp khác nhau, lập bảng so sánh Trade-off (Ưu điểm/Nhược điểm/Độ phức tạp), vẽ sơ đồ Flowchart trước khi bắt tay vào viết code.
4. **Bài tập 6 / Tiered Exercise 5 (Tầng IV — Sáng tạo & Mini Project Tự Chủ)**:
   - **Nguyên tắc Tối đa hóa Quyền tự chủ của Học viên**: Nghiêm cấm áp đặt cấu trúc I/O hay JSON cố định.
   - Học viên tự mình thực hiện trọn vẹn 4 bước kỹ sư:
     1. Tự thiết kế cấu trúc dữ liệu I/O (Schema Design).
     2. Tự suy luận và liệt kê các kịch bản lỗi biên ngoại lệ (Edge Case Matrix).
     3. Tự vẽ sơ đồ luồng dữ liệu (Data Flow Diagram - DFD).
     4. Tự lập trình giải pháp hoàn chỉnh từ bản thiết kế cá nhân.

### 4.2. Cấu Trúc Bắt Buộc Của Tài Liệu Bài Tập (Markdown File)
Tài liệu đề bài gửi học viên phải có đúng 5 phần tiêu đề H3:
- `### 1. Mục tiêu bài tập`: Nêu rõ 2-3 kỹ năng thành thạo sau khi làm bài.
- `### 2. Bối cảnh & Bài toán`: Mô tả ngữ cảnh thực tế kèm sơ đồ Mermaid Flowchart.
- `### 3. Quy tắc Nghiệp vụ / Mã nguồn Hiện tại`: Đặc tả quy tắc tính toán hoặc code legacy.
- `### 4. Yêu cầu Thực hiện`: Danh sách công việc cần nộp theo checklist định lượng.
- `### 5. Quy định Nộp bài`: Định dạng file, cấu trúc thư mục nộp và thời hạn.

### 4.3. Tiêu Chí Chấm Điểm Độc Lập (Instructor Rubric - Thang Điểm 100)
Tách riêng vào file `rubric_XX.md`, gồm 5 tiêu chí rõ ràng:
- **Độ chính xác nghiệp vụ (Business Logic Accuracy)**: 30 điểm.
- **Xử lý tình huống biên & ngoại lệ (Edge Case Handling)**: 20 điểm.
- **Chất lượng mã nguồn & Clean Code (Code Quality & PEP 8)**: 20 điểm.
- **Tối ưu hóa hiệu năng & cấu trúc (Optimization & Architecture)**: 15 điểm.
- **Tài liệu hóa & Sơ đồ thiết kế (Documentation & Flowchart)**: 15 điểm.

---

## 5. HỆ THỐNG DESIGN TOKENS & STYLE GUIDE TRỰC QUAN

Toàn bộ tài nguyên HTML/CSS phải tuân thủ bảng mã màu, kiểu chữ và kích thước chuẩn của hệ thống Rikkei Education:

### 5.1. Bảng Màu Chuẩn (Color Palette Tokens)

| Tên Token | Mã Hex | Ý Nghĩa Sử Dụng Trong Giao Diện |
| :--- | :---: | :--- |
| **Rikkei Primary Red** | `#be111c` | Màu đỏ nhận diện thương hiệu, tiêu đề phụ, icon chính, nút hành động chính (Nộp bài). |
| **Rikkei Dark Red** | `#990d16` | Trạng thái hover/active của nút bấm đỏ. |
| **Corporate Navy Slate** | `#0f172a` | Tiêu đề chính `<h1>`, `<h2>`, thanh header, thanh điều hướng, nền Terminal code. |
| **Neutral Slate Text** | `#334155` | Màu chữ nội dung bài đọc, mô tả, danh sách phân tích. |
| **Light Canvas Background** | `#f8fafc` | Nền toàn trang, nền thẻ code sandbox, nền sơ đồ minh họa. |
| **Pure White Card** | `#ffffff` | Nền thẻ nội dung bài viết, nền hộp câu hỏi ôn tập, ô nhập liệu. |
| **Border Slate** | `#e2e8f0` | Viền khung thẻ, đường phân cách mục, viền bảng dữ liệu. |
| **Success Emerald** | `#059669` | Highlight kết quả đúng, thông báo thành công, kết quả xuất ra Console. |
| **Flow & Info Sky** | `#0284c7` | Mũi tên luồng dữ liệu SVG, hộp yêu cầu bài toán, huy hiệu thông tin. |
| **Warning Amber** | `#d97706` | Thoi kiểm tra điều kiện (Decision node), thông báo nhắc nhở chưa chọn đáp án. |
| **Error & Pitfall Rose** | `#dc2626` | Nhánh luồng sai, thẻ minh họa BAD Practice, thông báo đáp án sai. |

### 5.2. Kiểu Chữ & Typography Chuẩn
- **Tiêu đề (`<h1>`, `<h2>`, `<h3>`, `<h4>`)**: Font `Montserrat`, `font-weight: 700`, màu `#0f172a`.
- **Văn bản Nội dung (`p`, `li`, `td`)**: Font `Inter`, system-ui, `font-size: 1rem (16px)`, line-height: `1.7`, màu `#334155`.
- **Mã Nguồn & Console (`code`, `pre`, `.font-mono`)**: Font `JetBrains Mono`, monospace, `font-size: 0.875rem (14px)`.

### 5.3. Kích Thước & Căn Chỉnh Giao Diện (Layout & Sizing)
- **Khung chứa trang chính**: `max-w-[1680px] mx-auto px-6`.
- **Thanh Mục lục Bên trái (TOC Sidebar Desktop)**: Độ rộng `w-80`, dính cố định `sticky top-24`, chiều cao `calc(100vh - 120px)`.
- **Mục lục Nổi Di động (Mobile Drawer)**: Nút tròn góc dưới phải `fixed bottom-6 right-6 z-50 bg-rikkei-red text-white p-3.5 rounded-full`.
- **Khung Bài viết Nội dung**: `flex-1 min-w-0 bg-white border border-slate-200 rounded-2xl p-6 sm:p-10 shadow-sm`.
- **Ảnh Minh Họa SVG**: Tỉ lệ 16:9, chiều rộng `max-w-[800px] - max-w-[900px]`, căn giữa `margin: 0 auto`.
- **Khoảng cách Mũi tên Flowchart**: Tối thiểu `80px - 90px`, nhãn chữ căn giữa không chạm viền thẻ.
- **Cụm Nút Nộp Bài / Làm Lại**: Căn phải `justify-end gap-3`, nút bấm nhỏ gọn `px-4 py-1.5 rounded-lg text-xs font-semibold`.

---

## 6. QUY TRÌNH 5 BƯỚC BIÊN SOẠN DÀNH CHO GIẢNG VIÊN

```
Bước 1: Chọn Bài toán Nghiệp vụ Đơn nhất (Unified Scenario)
  ⬇
Bước 2: Phác thảo Sơ đồ Kiến trúc & Luồng Dữ liệu (SVG / Mermaid)
  ⬇
Bước 3: Biên soạn Cú pháp & Tích hợp Code Sandbox / Interactive Visualizer
  ⬇
Bước 4: Xây dựng Bộ 3 Ví dụ Lũy tiến & Phân tích Lỗi Thường gặp
  ⬇
Bước 5: Thiết kế Bộ 3 Câu hỏi Tự kiểm tra Chống Tra cứu & Bộ 6 Bài tập Bloom
```

1. **Bước 1: Chọn Bài toán Nghiệp vụ Đơn nhất**:
   - Chọn 1 hệ thống thực tế gần gũi với doanh nghiệp (Thương mại điện tử, Đặt xe công nghệ, Siêu thị, Ngân hàng số).
   - Đặt câu hỏi kích thích tư duy: *"Làm thế nào để hệ thống tự động xử lý hàng nghìn tác vụ lặp lại mà không làm treo server?"*.
2. **Bước 2: Phác thảo Sơ đồ Kiến trúc & Luồng Dữ liệu**:
   - Vẽ sơ đồ 3 tầng (Đầu vào ➔ Xử lý ➔ Kết quả).
   - Sử dụng màu sắc theo đúng Design Tokens ở Mục 5.
3. **Bước 3: Biên soạn Cú pháp & Tích hợp Bộ Công cụ Trực quan**:
   - Trình bày thẻ cú pháp Syntax Card.
   - Giải thích từng từ khóa và tham số kèm code badge đỏ.
   - Cung cấp cấu hình biến RAM và log console cho bộ Interactive Code Tracker.
4. **Bước 4: Xây dựng Ví dụ Lũy tiến & Phân tích Lỗi**:
   - Soạn 3 ví dụ nối tiếp nhau cùng phát triển trên bài toán nghiệp vụ ban đầu.
   - Viết cặp khối BAD Practice vs GOOD Practice để học viên nhận diện sai lầm thường gặp.
5. **Bước 5: Thiết kế Đánh giá & Bài tập Phân tầng**:
   - Soạn 3 câu hỏi trắc nghiệm gắn chặt với số liệu/tên biến của bài đọc.
   - Soạn trọn bộ 6 bài tập phân tầng Bloom kèm Rubric chấm điểm 100 điểm độc lập.

---
*Tài liệu Quy chuẩn Kỹ thuật Học liệu — Rikkei Education (Ban hành và Áp dụng Toàn hệ thống).*
