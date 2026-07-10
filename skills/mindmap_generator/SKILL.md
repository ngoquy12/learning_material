---
name: mindmap_generator
description: Generate clean, structured, and academic markdown suitable for Markmap visualization for 1.5-hour classroom lectures.
---

# Kỹ năng tạo Sơ đồ tư duy (Mindmap Generator Skill)

## 1. Tổng quan

Sơ đồ tư duy (Mindmap) giúp giảng viên chốt kiến thức và hướng dẫn thảo luận trên lớp trong thời lượng 1.5 giờ. Học viên đã học lý thuyết ở nhà, nên Mindmap phải cực kỳ cô đọng, súc tích và trực quan.

## 2. Tiêu chuẩn Nội dung & Nhánh (Heading Hierarchy)

Bọc toàn bộ sơ đồ tư duy trong duy nhất một khối mã: ` ```markmap ... ``` `.

- **Nhánh lớn cấp 2 đầu tiên (##)**: Bắt buộc là `## Mục tiêu bài học` (chứa 2-3 gạch đầu dòng ngắn gọn về kiến thức/kỹ năng đạt được).
- **Chính sách không bỏ sót (Zero-drop Policy)**: Tất cả các chủ đề chính của bài học đều phải có một nhánh lớn cấp 2 (##) tương ứng.
- **Cấu trúc 3 nhánh con bắt buộc (###)**: Dưới mỗi chủ đề chính (##), chỉ tập trung vào đúng 3 nhánh con cấp 3 sau:
  - `### Khái niệm`: Định nghĩa bản chất ngắn gọn (1-2 câu).
  - `### Cú pháp & Cách dùng`: Cú pháp code mẫu cô đọng, định dạng chuẩn ngôn ngữ (ví dụ: ` ```python `) và phải thụt lề thụt dòng chính xác dưới gạch đầu dòng tương ứng.
  - `### Lưu ý`: 1-2 điểm mấu chốt, lỗi thường gặp hoặc kinh nghiệm thực tế.

## 3. Quy tắc hạn chế & Cấm đoán

- **KHÔNG làm kịch bản giảng dạy**: Nghiêm cấm đưa các từ khóa kịch bản đứng lớp như: "Slide 1", "Lecture Note", "Concept Check", "Khởi động", v.v. Chỉ tập trung vào kiến thức học thuật.
- **TUYỆT ĐỐI KHÔNG dùng emoji**: Tránh làm xao nhãng và đảm bảo tính học thuật nghiêm túc.
- **Hình ảnh logic trực quan**: Với các kiến trúc phức tạp, chèn thêm nút con: `[Prompt: <Viết prompt tiếng Anh mô tả chi tiết sơ đồ logic để AI vẽ>]. Content with Vietnamese`.
