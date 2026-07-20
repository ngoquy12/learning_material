---
name: exercise_generator
description: Generate a set of 6 role-based, real-world scenario coding exercises matching the Rikkei Education exercise standard (Bối cảnh & Nghiệp vụ, Vấn đề hiện tại, Yêu cầu nộp bài).
---

# Kỹ năng tạo Bài tập (Exercise Generator Skill)

## 1. Tổng quan
Kỹ năng này hướng dẫn AI đóng vai trò như một Giám đốc Học thuật để thiết kế một bộ gồm **6 bài tập (Exercises)** cho một chủ đề/bài học. 
Tiêu chuẩn bài tập của Rikkei Education KHÔNG phải là các bài tập thuật toán khô khan (như in hình sao, tính giai thừa). Thay vào đó, mỗi bài tập phải được đặt trong một **Bối cảnh thực tế (Real-world Scenario)**, đóng vai trò như một dự án nhỏ trong doanh nghiệp (VD: Hệ thống LMS, Module Điểm danh, Tool Thống kê Khảo thí).

## 2. Phân bổ Cấp độ Nhận thức (6 Bài tập)
Bộ 6 bài tập phải được chia thành 4 cấp độ như sau:

- **I. VẬN DỤNG CƠ BẢN (Bài 1 & Bài 2)**
  - Học viên được cung cấp sẵn một đoạn mã nguồn (Mã nguồn có chứa lỗi logic hoặc thiếu sót).
  - Yêu cầu học viên phân tích lỗi (Trace code) và sửa lại cho đúng.
- **II. VẬN DỤNG CHUYÊN SÂU (Bài 3 & Bài 4)**
  - Học viên đóng vai trò Backend Dev/Software Engineer nhận Task mới.
  - Phải xử lý các nghiệp vụ (Business Rules) phức tạp hơn và có các **Bẫy dữ liệu (Edge Cases)**.
- **III. PHÂN TÍCH (Bài 5)**
  - Xử lý các bài toán về tối ưu hóa quy trình (Ví dụ: tool cũ chạy chậm, tool cũ bắt nhập thủ công...).
  - Học viên phải đưa ra **ít nhất 2 giải pháp**, so sánh ưu/nhược điểm và vẽ sơ đồ luồng (Flowchart) trước khi code.
- **IV. SÁNG TẠO (Bài 6)**
  - Bài tập thiết kế một Mini Project / Module hoàn chỉnh dạng Menu (Console hoặc UI).
  - Yêu cầu học viên tự liệt kê các kịch bản lỗi, thiết kế cấu trúc code khối và bẫy lỗi ở mọi thao tác.

## 3. Cấu trúc Chuẩn của 1 Bài tập
Mỗi bài tập bắt buộc phải bao gồm các phần sau (format chính xác theo heading):

### [Tên Cấp độ]
### Bài [X]: [Tên Module/Tính năng] (VD: Bài 1: Module Kiểm soát nhập điểm thi)

**▪ Bối cảnh & Nghiệp vụ (Context & Business Rules):**
- Đặt ra bối cảnh doanh nghiệp (VD: Hệ thống LMS cần tính năng...).
- Nêu rõ quy tắc nghiệp vụ (VD: Điểm hợp lệ từ 0-10, nếu sai phải bắt nhập lại).

**▪ Vấn đề hiện tại / Ràng buộc (Current Issue / Constraints):**
- Tùy cấp độ, có thể là phàn nàn của người dùng về tool cũ, hoặc các ràng buộc nghiệp vụ, bẫy dữ liệu (Edge cases) bắt buộc phải xử lý (VD: sĩ số <= 0 thì văng lỗi).

**▪ Mã nguồn (Source Code):**
- *(Chỉ áp dụng cho cấp độ Vận dụng cơ bản)*. Cung cấp một đoạn code lỗi do "thực tập sinh" viết.

**▪ Yêu cầu nộp bài (Submission Requirements):**
Chia làm các phần nhỏ (Parts) để đánh giá toàn diện:
- **Phần 1 - Phân tích / Thiết kế:** Yêu cầu dùng mắt đọc code tìm lỗi, hoặc đưa ra các giải pháp/vẽ sơ đồ luồng.
- **Phần 2 - Thực thi (Coding):** Viết lại đoạn code, bổ sung chặn bẫy dữ liệu, hoàn thiện tính năng.

## 4. Định dạng Đầu ra (Output Format)
Sử dụng Markdown. Đảm bảo ngôn từ chuyên nghiệp, mang đậm tính thực chiến doanh nghiệp (sử dụng các từ vựng như: Khách hàng, Phòng Đào tạo, Giáo vụ, Bug, Crash hệ thống, Edge case).

---

## 💻 5. Quy tắc viết code mẫu trong bài tập (Code Styling Guidelines)
Khi viết hoặc cung cấp các đoạn mã nguồn mẫu (Source Code) trong bài tập, Agent bắt buộc phải tuân thủ nghiêm ngặt các quy tắc định dạng mã nguồn sau:
* **Ngôn ngữ của mã nguồn:** 100% tên biến, tên hàm, tên lớp, tên thuộc tính, và các định danh trong code phải viết bằng **Tiếng Anh**.
* **Quy tắc đặt tên (Naming Conventions):**
  - Sử dụng **`snake_case`** cho tên biến, tên hàm, tên thuộc tính trong Python/Database (ví dụ: `student_list`, `calculate_gpa`).
  - Sử dụng **`camelCase`** hoặc **`PascalCase`** đối với JavaScript/TypeScript/Java nếu ngôn ngữ đó quy định chuẩn như vậy (ví dụ: `studentList`, `calculateGpa`).
* **Thụt lề và căn lề (Indentation):**
  - Đảm bảo thụt lề chuẩn bằng khoảng trắng (Indent) hoặc Tab đồng nhất theo tiêu chuẩn của từng ngôn ngữ (ví dụ: Python bắt buộc thụt lề 4 khoảng trắng cho mỗi khối block logic).
  - Không viết mã nguồn dồn cục trên một dòng duy nhất khi trình bày cấu trúc đa dòng. Dùng ký tự xuống dòng `\n` chính xác.

