---
name: slide_generator
description: Generate rich, interactive, W3Schools-standard master HTML slide decks with 8 dynamic layouts, Action Headlines, Mermaid diagrams, VS Code dark code boxes, and Rikkei Education brand identity.
---

# Kỹ năng Xây dựng Slide Bài giảng Master HTML (Master Slide Generator Skill)

## 1. Triết lý Đào tạo Slide Bài giảng (Slide Pedagogical Philosophy)
Slide bài giảng đóng vai trò là **Công cụ Hỗ trợ Giảng dạy Trực quan (Visual Facilitation Tool)** cho Giảng viên đứng lớp trong thời lượng 1.5 giờ. Slide KHÔNG phải là một cuốn sách giáo khoa thu nhỏ (Text Heavy), mà phải cực kỳ cô đọng, giàu hình ảnh trực quan và kích thích tư duy.

### 4 Quy tắc Vàng về Slide Sư phạm:
1. **Quy tắc 6x6 (Concise & Impactful)**: Tối đa 4 - 6 gạch đầu dòng / thẻ thông tin trên 1 slide. Mỗi dòng tối đa 6 - 8 từ. Tuyệt đối KHÔNG đưa nguyên đoạn văn bản dài 100-200 từ lên slide.
2. **Chiến lược Tiêu đề Hành động (Action Headline Strategy)**:
   - Mỗi slide bắt buộc phải có một **Tiêu đề Tuyên bố Hành động (Action Title)** độc nhất giải thích thông điệp cốt lõi của slide đó (Ví dụ: `03. Tối Ưu Hóa Môi Trường Ảo Virtualenv Trong Dự Án`).
   - TUYỆT ĐỐI CẤM sử dụng tiêu đề rỗng tuếch lặp đi lặp lại kèm số đếm `- 1`, `- 2` (như `2. Cài đặt môi trường - 1`).
3. **Quy tắc Song ngữ Tiếng Anh / Tiếng Việt (Bilingual Policy for Vietnamese Students)**:
   - **TIẾNG ANH**: Từ khóa công nghệ (Python, Bytecode, PVM, Interpreter, RAM, Stack, Heap), cú pháp, tên biến, tên hàm (`def`, `class`, `id()`, `print()`, `total_price`).
   - **TIẾNG VIỆT**: Tiêu đề slide, nhãn các thẻ (Card Titles), nhãn nút sơ đồ và mô tả luồng di chuyển dữ liệu.
4. **Không Emoji Icon**: Không dùng biểu tượng cảm xúc/emoji trong slide. Sử dụng icon HTML Phosphor `<i class="ph-duotone ph-...">` hoặc ký hiệu chữ chuyên nghiệp `[HOT]`, `[BEST PRACTICE]`, `[ANTI-PATTERN]`.

---

## 2. Danh sách 8 Mẫu Layout Slide Dynamic Engine (8 Slide Layouts)

| Layout Code (`layout_type`) | Mục đích & Mô tả | Cấu trúc trình bày |
| :--- | :--- | :--- |
| `COVER_LAYOUT` | Trang bìa đầu bài giảng | Logo Rikkei Red, Tiêu đề chính lớn, Mã môn học, Số trang 1 |
| `AGENDA_LAYOUT` | Trang mục lục tiến trình bài học | Danh sách 4-6 mục trọng tâm kẻ số thứ tự nổi bật |
| `SINGLE_COLUMN_FOCUS` | Trình bày 1 định nghĩa / nguyên lý cốt lõi | 1 Thẻ lớn căn giữa, Typography nổi bật, Callout Note |
| `TWO_COLUMN_COMPARE` | Đối chiếu Vấn đề vs Giải pháp, Good vs Bad Code | 2 Cột thẻ màu sắc đối sánh tương phản |
| `THREE_COLUMN_CARDS` | Trình bày 3 thành phần / 3 quy tắc / 3 bước | Grid 3 cột thẻ song song |
| `CODE_DEMO_EXPLAINER` | Mã nguồn chuẩn kèm giải thích chi tiết | Trái: Khai quát & Gạch đầu dòng; Phải: Khung Code VS Code Dark |
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
   - Dùng cú pháp Mermaid chuẩn: `graph TD`, `sequenceDiagram`, `classDiagram`.
   - Nhãn các bước bằng Tiếng Việt giàu ý nghĩa.
