---
name: lab_generator
description: Structure practical hands-on labs with clear objectives, sequential execution tasks, and quantitative evaluation checklists.
---

# Kỹ năng tạo Bài thực hành Lab (Lab Generator Skill)

## 1. Tổng quan
Bài thực hành (Hands-on Lab) là xương sống giúp học viên phát triển kỹ năng code thực tế và tích lũy các cấu phần cho dự án cuối khóa. Mỗi bài Lab phải có mục tiêu rõ ràng và hướng dẫn từng bước chi tiết.

## 2. Cấu trúc 3 Phần chuẩn hóa
Mỗi bài Lab bắt buộc tuân theo bố cục sau:
1. **Mục tiêu (Objectives)**:
   - Nêu rõ 2-3 kỹ năng cụ thể học viên sẽ làm chủ (ví dụ: Tạo được Model SQLAlchemy, liên kết quan hệ 1-N).
   - Xác định rõ đầu ra kỳ vọng: *"Đạt chuẩn đầu ra kỳ vọng: hoạt động ổn định, không lỗi logic."*
2. **Mô tả & Các bước thực hiện (Description & Steps)**:
   - Nêu rõ tài nguyên đầu vào (ví dụ: *"Dự án FastAPI hiện tại và cơ sở dữ liệu PostgreSQL đã được cấu hình"*).
   - Liệt kê danh sách các bước thực hiện theo thứ tự tăng dần (Bước 1, Bước 2, Bước 3...) chi tiết và rõ ràng. Tránh các hướng dẫn chung chung không thể thực thi.
3. **Checklist Đánh giá (Evaluation Checklist)**:
   - Cung cấp bảng kiểm checklist định lượng rõ ràng để học viên tự kiểm tra trước khi nộp bài.
   - Ví dụ:
     - `[ ] API GET /items trả về danh sách đầy đủ dữ liệu.`
     - `[ ] Middleware CORS cấu hình đúng danh sách Origin cho phép.`
     - `[ ] Bắt lỗi HTTP 404 khi không tìm thấy thực thể.`

## 💻 3. Quy tắc viết code mẫu trong bài thực hành (Code Styling Guidelines)
Khi viết hoặc cung cấp các đoạn mã nguồn mẫu, hướng dẫn trong bài thực hành Lab, Agent bắt buộc phải tuân thủ nghiêm ngặt các quy tắc định dạng mã nguồn sau:
* **Ngôn ngữ của mã nguồn:** 100% tên biến, tên hàm, tên lớp, tên thuộc tính, và các định danh trong code phải viết bằng **Tiếng Anh**.
* **Quy tắc đặt tên (Naming Conventions):**
  - Sử dụng **`snake_case`** cho tên biến, tên hàm, tên thuộc tính trong Python/Database (ví dụ: `database_connection`, `get_user_by_email`).
  - Sử dụng **`camelCase`** hoặc **`PascalCase`** đối với JavaScript/TypeScript/Java nếu ngôn ngữ đó quy định chuẩn như vậy (ví dụ: `databaseConnection`, `getUserByEmail`).
* **Thụt lề và căn lề (Indentation):**
  - Đảm bảo thụt lề chuẩn bằng khoảng trắng (Indent) hoặc Tab đồng nhất theo tiêu chuẩn của từng ngôn ngữ (ví dụ: Python bắt buộc thụt lề 4 khoảng trắng cho mỗi khối block logic).
  - Không viết mã nguồn dồn cục trên một dòng duy nhất khi trình bày cấu trúc đa dòng. Dùng ký tự xuống dòng `\n` chính xác.
