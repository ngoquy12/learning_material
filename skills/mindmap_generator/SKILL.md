---
name: mindmap_generator
description: Generate clean, structured, and academic markdown suitable for Markmap visualization for 1.5-hour classroom lectures.
---

# Kỹ năng tạo Sơ đồ tư duy (Mindmap Generator Skill)

## 1. Tổng quan & Thiết kế sư phạm
Sơ đồ tư duy (Mindmap) giúp giảng viên hệ thống hóa kiến thức và hướng dẫn thảo luận lớp học trong thời lượng 1.5 giờ. Học viên đã học lý thuyết ở nhà trước qua E-learning, do đó Mindmap trên lớp phải cực kỳ cô đọng, súc tích và trực quan.

## 2. Tiêu chuẩn Nội dung & Nhánh (Heading Hierarchy)
Bọc toàn bộ sơ đồ tư duy trong duy nhất một khối mã:
```markmap
# [Session ID]: [Tiêu đề Session/Bài học]
...
```

### Quy tắc xây dựng nhánh:
1. **Tiêu đề cấp 1 (#)**: Là gốc sơ đồ, có dạng `# [Session ID]: [Tiêu đề chính]`.
2. **Nhánh cấp 2 đầu tiên (## Mục tiêu bài học)**: Bắt buộc phải là `## Mục tiêu bài học`. Nhánh này chỉ nêu ngắn gọn 2-3 gạch đầu dòng về kiến thức/kỹ năng cốt lõi đạt được.
3. **Chính sách không bỏ sót (Zero-drop Policy)**: Tất cả các chủ đề chính của bài học (từ PM/SSOT) đều phải có một nhánh lớn cấp 2 (##) tương ứng.
4. **Cấu trúc 3 nhánh con bắt buộc (###)**: Dưới mỗi chủ đề chính (##) (trừ nhánh Mục tiêu bài học), chỉ tập trung vào đúng 3 nhánh con cấp 3 sau:
   - `### Khái niệm cốt lõi`: Định nghĩa bản chất ngắn gọn nhất (1-2 câu).
   - `### Cú pháp & Cách khai báo`: Cú pháp code mẫu cô đọng, định dạng chuẩn ngôn ngữ (ví dụ: ` ```python ... ``` ` hoặc ` ```typescript ... ``` ` hoặc ` ```java ... ``` `) được thụt lề dưới gạch đầu dòng (-) tương ứng để đảm bảo render highlight cú pháp chính xác.
   - `### Lưu ý thực chiến`: 1-2 điểm mấu chốt, lỗi thường gặp hoặc kinh nghiệm thực hành thực chiến.

## 3. Quy tắc hạn chế & Cấm đoán
- **KHÔNG làm kịch bản giảng dạy**: Nghiêm cấm đưa các từ khóa kịch bản đứng lớp như: "Slide 1", "Lecture Note", "Concept Check", "Khởi động", "Live Demo", v.v. Sơ đồ chỉ tập trung vào kiến thức học thuật.
- **TUYỆT ĐỐI KHÔNG dùng emoji**: Đảm bảo tính học thuật nghiêm túc, không chèn bất kỳ icon/emoji nào trong các nhánh.
- **TUYỆT ĐỐI KHÔNG rò rỉ kiến thức (Scope Leakage)**: Nội dung trong mindmap không chứa cú pháp hay khái niệm vượt quá phạm vi bài học hiện tại (ví dụ: Bài học chỉ giới thiệu Web API nhưng không được nhắc tới SQLite/SQLAlchemy/Database).
- **Tránh ký tự # thừa thãi**: Không có ký tự # thừa thãi bên trong văn bản của các nút, tránh làm vỡ bố cục hiển thị của markmap. Ký tự # chỉ được sử dụng ở đầu dòng để định nghĩa tiêu đề.
- **Hình ảnh logic trực quan (BẮT BUỘC)**: Với các kiến trúc phức tạp hoặc luồng dữ liệu khó hiểu, chèn thêm nút con: `[Prompt: <Viết prompt tiếng Anh mô tả chi tiết sơ đồ logic/sequence/architecture để AI vẽ>]` hoặc `[Tạo ảnh: <Viết prompt tiếng Anh mô tả chi tiết sơ đồ logic/sequence/architecture để AI vẽ>]`.

## 4. Định dạng Code trong Sơ đồ tư duy
Khi trình bày code mẫu dưới nhánh `### Cú pháp & Cách khai báo`, code phải được bọc trong block Markdown chỉ định ngôn ngữ và thụt lề bằng dấu cách (space) chuẩn xác dưới gạch đầu dòng để tránh làm vỡ cây sơ đồ khi hiển thị.
