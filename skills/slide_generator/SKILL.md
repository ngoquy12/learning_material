---
name: slide_generator
description: Generate rich, interactive, W3Schools-standard master HTML slide decks with 8 dynamic layouts, Action Headlines, Mermaid diagrams, VS Code dark code boxes, clean typography, SVG icons, and Rikkei Education brand identity.
---

# Kỹ năng Xây dựng Slide Bài giảng Master HTML (Master Slide Generator Skill)

## 1. Triết lý & 8 Quy tắc Vàng về Slide Bài giảng (8 Golden Rules)

Slide bài giảng đóng vai trò là **Công cụ Hỗ trợ Giảng dạy Trực quan (Visual Facilitation Tool)** cho Giảng viên đứng lớp trong thời lượng 1.5 giờ. Slide KHÔNG phải là một cuốn sách giáo khoa thu nhỏ (Text Heavy), mà phải cực kỳ cô đọng, chuẩn mực và sắc nét.

> [!IMPORTANT]
> **8 QUY TẮC BẮT BUỘC KHI TẠO SLIDE VÀ BIÊN DỊCH SLIDE SESSION:**
>
> 1. **Kiểm Soát Tải Trọng Nhận Thức (Slide Count Limit - 15 đến 20 Slides/Session)**:
>    - **TUYỆT ĐỐI CẤM** tạo các bộ slide dài 50-70 slide vụn vặt gây quá tải nhận thức.
>    - Một Session 1.5 giờ chỉ được phép có **tối đa 15 - 20 slide trọng tâm**. Mỗi Lesson chỉ gồm **3 - 4 slide chất lượng cao**:
>      - _Slide 1: Problem & Hook (Đặt vấn đề thực tế doanh nghiệp)_.
>      - _Slide 2: Core Concept & Visual Diagram (Khái niệm & Sơ đồ luồng)_.
>      - _Slide 3: Code Demo Explainer / Live Playground (Mã nguồn thực chiến)_.
>      - _Slide 4: Pitfalls & Summary (Bẫy cú pháp & Tổng kết)_.
> 2. **Slide Trang Bìa (Cover Slide - Slide 1)**:
>    - **Tag đỏ**: Hiển thị tên Session (ví dụ `Session 01` bằng chữ màu đỏ `#be111c`, font Montserrat/Inter).
>    - **Tiêu đề chính**: Bỏ từ "Session" trong chuỗi tiêu đề chính (ví dụ `Giới thiệu Python va Thiết lập môi trường` bằng chữ màu đen đúp đậm `#0f172a`).
>    - **Tên môn học**: Bắt buộc là tên môn học thực tế (như `Môn học: Lập trình Python`), **NGHIÊM CẤM DÙNG UPPERCASE** hoặc dùng từ sai như `RIKKEI ACADEMY`.
> 3. **Slide Mục Lục Session (Agenda Slide - Slide 2)**:
>    - Bắt buộc liệt kê đầy đủ danh sách các Lesson trong Session dưới dạng danh sách được đánh số thứ tự (`01. Lesson 01 - ...`, `02. Lesson 02 - ...`).
>    - Tiêu đề mục lục đổi thành **`NỘI DUNG BÀI HỌC`** (Font Montserrat Bold 36px, màu đỏ `#be111c`). Các chữ tên bài học kích thước to đậm (24px - 28px) dễ quan sát từ xa.
> 4. **Tiêu Đề Lớn Bài Học (Content Slide Large Title - Áp dụng từ Slide 3)**:
>    - Tiêu đề lớn nhất trên từng slide nội dung **BẮT BUỘC** là **Tên Lesson kèm theo số thứ tự slide của Lesson đó**, phân cách bằng dấu gạch ngang `-` (ví dụ `Lesson 01 - Giới thiệu ngôn ngữ Python - 1`).
>    - Phông chữ tiêu đề lớn: Màu đỏ thương hiệu `#be111c`, kích thước **28px** (Montserrat Bold).
> 5. **Tiêu Đề Nhỏ / Phụ (Content Slide Subtitle)**:
>    - Tiêu đề nhỏ ngay dưới Tiêu đề lớn chính là tên chủ đề cụ thể của slide đó (ví dụ `Đặt vấn đề & Bối cảnh thực tế doanh nghiệp`).
>    - Phông chữ tiêu đề nhỏ: **BẮT BUỘC CHỮ MÀU ĐEN (`#0f172a`)**, kích thước **20px** (Inter Bold). **CẤM LẶP LẠI TIÊU ĐỀ LỚN HOẶC DÙNG DẪN 01.01 LẶP DƯ THỪA**.
> 6. **Quy Chuẩn Kích Thước Chữ Nội Dung & Thẻ (Typography Scaling)**:
>    - **Text Body**: Kích thước **18px** (Inter Medium/Regular).
>    - **Text Con / Sub-bullets**: Kích thước **TỐI THIỂU 16px** (Cấm dùng chữ nhỏ hơn 16px).
>    - **Quy tắc 3-30-300**: Mỗi slide tối đa 3 ý chính, mỗi ý tối đa 30 từ. Tự động in đậm Keyword kỹ thuật (`<b>snake_case</b>`, `<b>PEP 8</b>`).
> 7. **Quy Tắc Phối Màu Khối Thẻ (Card Color Coding System)**:
>    - ⚪ **Khối Mặc Định**: Nền Xám nhạt (`#f8fafc`), Viền `#e2e8f0`.
>    - 🟠 **Khối Cảnh Báo**: Nền Cam nhạt (`#fffbeb`), Viền `#f59e0b`, Chữ `#92400e`.
>    - 🔴 **Khối Lỗi / Bẫy cú pháp**: Nền Đỏ nhạt (`#fef2f2`), Viền `#ef4444`, Chữ `#991b1b`.
>    - 🟢 **Khối Thành Công / Chuẩn**: Nền Xanh lá nhạt (`#f0fdf4`), Viền `#22c55e`, Chữ `#166534`.
>    - 🔵 **Khối Đề Xuất / Thực Tế**: Nền Xanh dương nhạt (`#eff6ff`), Viền `#3b82f6`, Chữ `#1e40af`.
> 8. **Đồ Họa, Render Markdown & Chuẩn Mực Ngôn Ngữ Sư Phạm**:
>    - **Trực quan hóa 100%**: Ưu tiên tạo Sơ đồ luồng (Mermaid Flowchart/Sequence), SVG Vector hoặc Infographic thay vì chỉ toàn chữ.
>    - **Render Markdown 100%**: Mọi cú pháp Markdown (`**bold**`, `` `code` ``) phải được render hoàn chỉnh ra HTML chuẩn.
>    - **Văn phong Học thuật & Chuyên nghiệp**: Ngôn từ chuẩn sư phạm doanh nghiệp, giàu tính kỹ thuật học thuật. **TUYỆT ĐỐI CẤM** dùng từ sến súa (_"nhé"_, _"thân mến"_, _"nha"_).
>    - **NO EMOJI**: TUYỆT ĐỐI CẤM EMOJI. Chỉ dùng Phosphor SVG icons hoặc CSS badges.

---

## 2. Các Tính Năng Đột Phá Tiêu Chuẩn Gamma.app & Google Slides AI

1. **Layout Bento Grid Modern**: Thẻ bo tròn góc 16px - 20px, bóng mờ `box-shadow: 0 20px 40px rgba(0,0,0,0.06)`, Gradient highlights.
2. **Dual-Theme Engine (1-Click Dark 🌙 / Light ☀️ Switcher)**: Cho phép Giảng viên đổi theme Đêm/Sáng linh hoạt theo ánh sáng phòng học.
3. **Interactive In-Slide Tabs & Accordions**: Gộp các nội dung phụ vào Tab tương tác trong 1 slide duy nhất thay vì xé nhỏ thành nhiều slide.
4. **Split Screen Code Comparison**: Đối sánh mã nguồn vi phạm ❌ vs Mã nguồn chuẩn PEP 8 ✅.
5. **Presenter View Mode (Phím P / Button 🎤)**: Bật hiển thị ghi chú sư phạm (Speaker Notes) & Bộ đếm giờ cho Giảng viên.

---

## 3. Danh sách 8 Mẫu Layout Slide Dynamic Engine (8 Slide Layouts)

| Layout Code (`layout_type`) | Mục đích & Mô tả                                    | Cấu trúc trình bày                                             |
| :-------------------------- | :-------------------------------------------------- | :------------------------------------------------------------- |
| `COVER_LAYOUT`              | Trang bìa đầu bài giảng                             | Logo Rikkei Red, Tag đỏ Session, Tiêu đề chính đen, Mã môn học |
| `AGENDA_LAYOUT`             | Trang mục lục tiến trình bài học                    | Danh sách các Lesson kẻ số thứ tự nổi bật (Badge đỏ 24px)      |
| `SINGLE_COLUMN_FOCUS`       | Trình bày 1 định nghĩa / nguyên lý cốt lõi          | 1 Thẻ lớn căn giữa, Typography 20px-24px, Callout Note         |
| `TWO_COLUMN_COMPARE`        | Đối chiếu Vấn đề vs Giải pháp, Good vs Bad Code     | 2 Cột thẻ màu sắc đối sánh tương phản (Xanh vs Đỏ)             |
| `THREE_COLUMN_CARDS`        | Trình bày 3 thành phần / 3 quy tắc / 3 bước         | Grid 3 cột thẻ song song                                       |
| `CODE_DEMO_EXPLAINER`       | Mã nguồn chuẩn kèm giải thích chi tiết              | Trái: Khái quát & Gạch đầu dòng 18px; Phải: Khung Code VS Dark |
| `MERMAID_DIAGRAM`           | Sơ đồ luồng/kiến trúc trực quan chiếm 80% diện tích | Sơ đồ Mermaid Flowchart/Sequence/ClassDiagram render mượt      |
| `TABLE_COMPARISON`          | Bảng so sánh 4 cột Full-width 100% màn hình         | Bảng so sánh Markdown 4 cột (Tiêu chí, A, B, Thực tế)          |
| `WARNING_GOTCHAS`           | Nhấn mạnh sai lầm đắt giá / Bẫy cú pháp             | Khung Cảnh báo Đỏ nhạt (`#fef2f2`, viền `#ef4444`)             |
| `TIMELINE_RECAP`            | Trang tổng kết mốc tiến trình bài học               | Timeline 4 mốc kết nối mượt mà                                 |

---

## 4. Quy chuẩn Định dạng Code & Mermaid trong Slide

1. **Khối Mã Nguồn (Code Box)**:
   - Sử dụng font chữ `Fira Code` hoặc `JetBrains Mono`.
   - Màu nền đen đúa VS Code Dark (`#0f172a`), viền `#334155`.
   - Tên biến, từ khóa chuẩn Tiếng Anh.

2. **Khối Sơ đồ Mermaid (Mermaid Diagram Box)**:
   - Bọc trong thẻ `<div class="mermaid"> ... </div>`.
   - Dùng cú pháp Mermaid chuẩn v10: `flowchart TD`, `sequenceDiagram`, `classDiagram`.
   - Nhãn các bước bằng Tiếng Việt giàu ý nghĩa.

> [!IMPORTANT]
> Tệp đầu ra duy nhất của Agent Slide cho từng Lesson là **`slides.html`** (Nằm trong thư mục `Bài giảng/slides.html`). TUYỆT ĐỐI KHÔNG LƯU THÀNH `slides.md`.
