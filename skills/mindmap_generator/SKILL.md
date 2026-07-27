---
name: mindmap_generator
description: Generate clean, structured, and academic markdown suitable for Markmap visualization for 1.5-hour classroom lectures.
---

# Kỹ năng tạo Sơ đồ tư duy (Mindmap Generator Skill)

## 1. Tổng quan & Thiết kế sư phạm
Sơ đồ tư duy (Mindmap) giúp giảng viên hệ thống hóa kiến thức và hướng dẫn thảo luận lớp học trong thời lượng 1.5 giờ. Học viên đã học lý thuyết ở nhà trước qua E-learning, do đó Mindmap trên lớp phải cực kỳ cô đọng, trực quan, đi thẳng vào bản chất kỹ thuật và dễ tra cứu.

## 2. Tiêu chuẩn Nội dung & Nhánh (Heading Hierarchy)
Bọc toàn bộ sơ đồ tư duy trong duy nhất một khối mã:
```markmap
# [Session/Lesson ID]: [Tiêu đề Bài học]
...
```

### Quy tắc xây dựng nhánh:
1. **Tiêu đề cấp 1 (#)**: Là gốc sơ đồ, có dạng `# [Lesson ID]: [Tiêu đề chính bài học]`.
2. **Đi thẳng vào Module Kiến thức**: TUYỆT ĐỐI KHÔNG tạo nhánh `## Mục tiêu bài học`. Gốc sơ đồ (#) phân nhánh trực tiếp ra các Chủ đề Kiến thức Cốt lõi (`## Chủ đề 1`, `## Chủ đề 2`).
3. **Chính sách không bỏ sót (Zero-drop Policy)**: Tất cả các chủ đề chính của bài học (từ PM/SSOT) đều phải có một nhánh lớn cấp 2 (##) tương ứng.
4. **Phân nhánh động theo Bản chất Nội dung (Content-Driven Branching)**:
   - CẤM lặp lại rập khuôn 3 nhánh `Khái niệm`, `Cú pháp`, `Lưu ý` ở tất cả các mục.
   - **Đối với Chủ đề Lập trình / Code**: Trình bày đoạn mã mẫu cô đọng (bọc trong ` ```python ... ``` ` hoặc ` ```typescript ... ``` `) ngay bên dưới nhánh chủ đề kèm theo 1-2 điểm lưu ý thực chiến (`Gotchas`).
   - **Đối với Chủ đề Khái niệm / Luồng vận hành**: Phân nhánh theo luồng tư duy tự nhiên (Bản chất & Nguyên lý $\rightarrow$ Cơ chế hoạt động $\rightarrow$ Ứng dụng thực tế).
5. **Độ sâu tối đa 3-4 cấp (Max-Depth Rule)**: Không chẻ nhỏ quá 3-4 cấp thụt lề để cây sơ đồ Markmap không bị mở rộng lê thê theo chiều ngang.

## 3. Quy tắc hạn chế & Cấm đoán
- **KHÔNG làm kịch bản giảng dạy**: Nghiêm cấm đưa các từ khóa kịch bản đứng lớp như: "Slide 1", "Lecture Note", "Concept Check", "Khởi động", "Live Demo", v.v. Sơ đồ chỉ tập trung vào kiến thức học thuật.
- **TUYỆT ĐỐI KHÔNG dùng emoji**: Đảm bảo tính học thuật nghiêm túc, không chèn bất kỳ icon/emoji nào trong các nhánh.
- **TUYỆT ĐỐI KHÔNG rò rỉ kiến thức (Scope Leakage)**: Nội dung trong mindmap không chứa cú pháp hay khái niệm vượt quá phạm vi bài học hiện tại (ví dụ: Lesson 01 chỉ giới thiệu Web API nhưng không được nhắc tới SQLite/SQLAlchemy/Database).
- **Tránh ký tự # thừa thãi**: Không có ký tự # thừa thãi bên trong văn bản của các nút, tránh làm vỡ bố cục hiển thị của markmap. Ký tự # chỉ được sử dụng ở đầu dòng để định nghĩa tiêu đề.
- **Hình ảnh logic trực quan (BẮT BUỘC)**: Với các kiến trúc phức tạp hoặc luồng dữ liệu khó hiểu, chèn thêm nút con: `[Prompt: <Viết prompt tiếng Anh mô tả chi tiết sơ đồ logic/sequence/architecture để AI vẽ>]` hoặc `[Tạo ảnh: <Viết prompt tiếng Anh mô tả chi tiết sơ đồ logic/sequence/architecture để AI vẽ>]`.

## 4. Định dạng Code trong Sơ đồ tư duy
Khi trình bày code mẫu dưới các nhánh, code phải được bọc trong block Markdown chỉ định ngôn ngữ chuẩn xác và thụt lề chuẩn bằng dấu cách (space) dưới gạch đầu dòng (-) tương ứng để hiển thị highlight sắc nét trên Markmap.

## 🌐 5. Quy tắc Song ngữ Tiếng Anh / Tiếng Việt trong Sơ đồ & Prompt Tạo ảnh (Bilingual Diagram & Image Rule)
* **TIẾNG ANH (English)**: Giữ nguyên từ khóa công nghệ, cú pháp, tên biến, tên hàm, tên lớp (`Bytecode`, `PVM`, `Interpreter`, `id()`, `str/int/float`).
* **TIẾNG VIỆT (Vietnamese)**: Tiêu đề sơ đồ, nhãn các nhánh và mô tả luồng diễn giải trong hình ảnh (`[Khởi tạo đối tượng]`, `[Trình thông dịch xử lý]`, `[Phân bố vùng nhớ RAM]`). Giúp sinh viên Việt Nam không bị áp lực tiếng Anh nhưng vẫn nắm chuẩn thuật ngữ chuyên ngành.
