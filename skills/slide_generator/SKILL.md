---
name: slide_generator
description: Generate rich, interactive, W3Schools-standard master HTML slide decks with 8 dynamic layouts, Action Headlines, Mermaid diagrams, VS Code dark code boxes, clean typography, SVG icons, and Rikkei Education brand identity.
---

# Kỹ năng Xây dựng Slide Bài giảng Master HTML (Master Slide Generator Skill)

## 1. Triết lý & 6 Quy tắc Vàng về Slide Bài giảng (6 Golden Rules)

Slide bài giảng đóng vai trò là **Công cụ Hỗ trợ Giảng dạy Trực quan (Visual Facilitation Tool)** cho Giảng viên đứng lớp trong thời lượng 1.5 giờ. Slide KHÔNG phải là một cuốn sách giáo khoa thu nhỏ (Text Heavy), mà phải cực kỳ cô đọng, chuẩn mực và sắc nét.

> [!IMPORTANT]
> **6 QUY TẮC BẮT BUỘC KHI TẠO SLIDE VÀ BIÊN DỊCH SLIDE SESSION:**
>
> 1. **Slide Trang Bìa (Cover Slide - Slide 1)**:
>    - **Tag đỏ**: Hiển thị tên Session (ví dụ `Session 01` bằng chữ màu đỏ `#be111c`, font Montserrat/Inter).
>    - **Tiêu đề chính**: Bỏ từ "Session" trong chuỗi tiêu đề chính (ví dụ `Giới thiệu Python va Thiết lập môi trường` bằng chữ màu đen đúp đậm `#0f172a`).
>    - **Tên môn học**: Bắt buộc là tên môn học thực tế (như `Môn học: Lập trình Python`), **NGHIÊM CẤM DÙNG UPPERCASE** hoặc dùng từ sai như `RIKKEI ACADEMY`.
>
> 2. **Slide Mục Lục Session (Agenda Slide - Slide 2)**:
>    - Bắt buộc liệt kê đầy đủ danh sách các Lesson trong Session dưới dạng danh sách được đánh số thứ tự (`01. Lesson 01 - ...`, `02. Lesson 02 - ...`).
>    - Tiêu đề mục lục dùng chữ Title Case chuẩn (`Nội dung tổng quan Session`), **CẤM VIẾT HOA TOÀN BỘ (UPPERCASE)**.
>
> 3. **Tiêu Đề Lớn Bài Học (Content Slide Large Title)**:
>    - Tiêu đề lớn nhất trên từng slide nội dung **BẮT BUỘC** là **Tên Lesson kèm theo số thứ tự slide của Lesson đó**, phân cách bằng dấu gạch ngang `-` (ví dụ `Lesson 01 - Giới thiệu ngôn ngữ Python - 1`, `Lesson 01 - Giới thiệu ngôn ngữ Python - 2`).
>    - Phông chữ tiêu đề lớn: Màu đỏ thương hiệu `#be111c`, kích thước 22px, font Montserrat Bold.
>
> 4. **Tiêu Đề Nhỏ / Phụ (Content Slide Subtitle)**:
>    - Tiêu đề nhỏ ngay dưới Tiêu đề lớn chính là tên chủ đề cụ thể của slide đó (ví dụ `Đặt vấn đề & Bối cảnh thực tế doanh nghiệp`).
>    - Phông chữ tiêu đề nhỏ: **BẮT BUỘC CHỮ MÀU ĐEN (`#0f172a`)**, kích thước nhỏ hơn (16px), font Inter Bold. **CẤM LẶP LẠI TIÊU ĐỀ LỚN HOẶC DÙNG DẪN 01.01 LẶP DƯ THỪA**.
>
> 5. **Chuẩn Mực Ngôn Ngữ Sư Phạm Doanh Nghiệp**:
>    - **TUYỆT ĐỐI CẤM** dùng các từ sến súa, khẩu ngữ suồng sã như: *"nhé"*, *"thân mến"*, *"nha"*, *"đó nhé"*, *"các bạn ơi"*.
>    - Ngôn từ phải thể hiện sự chuyên nghiệp, chuẩn sư phạm và kỹ thuật doanh nghiệp.
>
> 6. **Cơ Chế Biểu Tượng & Đồ Họa (No Emoji Policy)**:
>    - **TUYỆT ĐỐI CẤM DÙNG ICON EMOJI** (như 🚀, 💡, 📌, 🎯, 🔥, ⚡, ❌, ✅, 🏢, 🖥️).
>    - **ĐƯỢC PHÉP VÀ KHUYÊN DÙNG**: SVG vector icons, Phosphor Icons (`<i class="ph-bold ph-...">`), hoặc thẻ Badge CSS chuyên nghiệp (`[HOT]`, `[BEST PRACTICE]`, `[WARNING]`).

---

## 2. Danh sách 8 Mẫu Layout Slide Dynamic Engine (8 Slide Layouts)

| Layout Code (`layout_type`) | Mục đích & Mô tả | Cấu trúc trình bày |
| :--- | :--- | :--- |
| `COVER_LAYOUT` | Trang bìa đầu bài giảng | Logo Rikkei Red, Tag đỏ Session, Tiêu đề chính đen, Mã môn học |
| `AGENDA_LAYOUT` | Trang mục lục tiến trình bài học | Danh sách các Lesson kẻ số thứ tự nổi bật |
| `SINGLE_COLUMN_FOCUS` | Trình bày 1 định nghĩa / nguyên lý cốt lõi | 1 Thẻ lớn căn giữa, Typography nổi bật, Callout Note |
| `TWO_COLUMN_COMPARE` | Đối chiếu Vấn đề vs Giải pháp, Good vs Bad Code | 2 Cột thẻ màu sắc đối sánh tương phản |
| `THREE_COLUMN_CARDS` | Trình bày 3 thành phần / 3 quy tắc / 3 bước | Grid 3 cột thẻ song song |
| `CODE_DEMO_EXPLAINER` | Mã nguồn chuẩn kèm giải thích chi tiết | Trái: Khái quát & Gạch đầu dòng; Phải: Khung Code VS Code Dark |
| `MERMAID_DIAGRAM` | Sơ đồ luồng/kiến trúc trực quan chiếm 80% diện tích | Sơ đồ Mermaid Flowchart/Sequence/ClassDiagram render mượt |
| `TABLE_COMPARISON` | Bảng so sánh 4 cột Full-width 100% màn hình | Bảng so sánh Markdown 4 cột (Tiêu chí, A, B, Thực tế) |
| `WARNING_GOTCHAS` | Nhấn mạnh sai lầm đắt giá / Bẫy cú pháp | Khung Cảnh báo Đỏ (Rikkei Warning Alert Box) |
| `TIMELINE_RECAP` | Trang tổng kết mốc tiến trình bài học | Timeline 4 mốc kết nối mượt mà |

---

## 3. Quy chuẩn Định dạng Code & Mermaid trong Slide

1. **Khối Mã Nguồn (Code Box)**:
   - Sử dụng font chữ `Fira Code` hoặc `JetBrains Mono`.
   - Màu nền đen đúa VS Code Dark (`#0f172a`), viền `#334155`.
   - Tên biến, từ khóa chuẩn Tiếng Anh.

2. **Khối Sơ đồ Mermaid (Mermaid Diagram Box)**:
   - Bọc trong thẻ `<div class="mermaid"> ... </div>`.
   - Dùng cú pháp Mermaid chuẩn v10: `flowchart TD`, `sequenceDiagram`, `classDiagram`.
   - Nhãn các bước bằng Tiếng Việt giàu ý nghĩa.
