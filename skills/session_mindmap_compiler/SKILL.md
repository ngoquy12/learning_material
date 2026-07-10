---
name: session_mindmap_compiler
description: Merge and structure all lesson-level markmap mindmaps into a single, master session-level markdown mindmap document suitable for Markmap preview.
---

# Kỹ năng tổng hợp sơ đồ tư duy toàn bộ Session (Session Mindmap Compiler Skill)

## 1. Mục tiêu
Hợp nhất tất cả các sơ đồ tư duy (Mindmap) đơn lẻ của các bài học thành một sơ đồ tư duy tổng thể duy nhất cho toàn bộ Session (`mindmap_all.md`). Sơ đồ này cung cấp cái nhìn toàn cảnh về toàn bộ lượng kiến thức của buổi học đó cho giảng viên và học viên.

## 2. Tiêu chuẩn cấu trúc phân cấp (Hierarchical Structure)
Sơ đồ tư duy hợp nhất phải tuân thủ định dạng Markmap Markdown:
*   **Tiêu đề cấp 1 (#)**: Là tiêu đề của toàn bộ Session (ví dụ: `# Session 01: Định hướng học tập & Demo sản phẩm`).
*   **Tiêu đề cấp 2 (##)**: Là tiêu đề của từng Lesson tương ứng trong Session.
*   **Tiêu đề cấp 3 (###)**: Các chủ đề chính trong từng Lesson.
*   **Tiêu đề cấp 4 (####)**: Cấu trúc 3 nhánh con bắt buộc (`Khái niệm cốt lõi`, `Cú pháp & Cách khai báo`, `Lưu ý thực chiến`).

## 3. Quy trình gộp & Tránh lặp (Deduplication Rules)
1. Loại bỏ các tiêu đề trùng lặp như tiêu đề gốc của môn học để đưa về một nút gốc duy nhất.
2. Thụt lề (indentation) các nhánh con chính xác bằng dấu gạch đầu dòng `-` hoặc tab để công cụ render Markmap hiển thị chính xác cây thư mục.
3. Đảm bảo toàn bộ sơ đồ được bao bọc trong khối code sạch sẽ.
