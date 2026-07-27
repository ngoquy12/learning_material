# 📑 BÁO CÁO THẨM ĐỊNH CHƯƠNG TRÌNH HỌC (PM REVIEW)
**Công nghệ mục tiêu:** `python/core`

## 1. 📊 Tổng Quan & Điểm Đánh Giá
- **Điểm sẵn sàng (Readiness Score):** 6.5/10
- **Nhận định chung:** Khung chương trình Session 05 về Xử lý Chuỗi (String) có cấu trúc phân rã bài học khá mạch lạc và đi theo tiến trình sư phạm hợp lý từ lý thuyết cơ bản đến các ứng dụng định dạng. Tuy nhiên, chương trình đang gặp một lỗi nghiêm trọng liên quan đến việc **vi phạm phân vùng phạm vi kiến thức (Scope Boundary Violation)** khi đưa các phương thức liên quan chặt chẽ đến cấu trúc dữ liệu mảng/danh sách vào bài học trong khi cấu trúc này đang bị cấm.

## 2. 🧠 Phân Tích Dòng Chảy Nhận Thức & Kế Thừa
- **Điểm sáng:** 
  - Tiến trình đi từ khái niệm cơ bản (Khái niệm chuỗi, Indexing, Tính bất biến ở Lesson 01) chuyển tiếp sang Slicing & Toán tử (Lesson 02) là rất tự nhiên.
  - Tách biệt phần Định dạng chuỗi (String formatting - Lesson 04) ra cuối cùng là hợp lý, giúp học viên tập trung xử lý dữ liệu trước khi học cách hiển thị/đầu ra trực quan.
- **Lỗ hổng "Nhảy cóc" (Missing Prerequisites):**
  - **Lesson 03 (`methods`):** Khái niệm và cách hoạt động của hai hàm `split()` và `join()`. 
    - Hàm `split()` mặc định trả về một **List** các chuỗi con.
    - Hàm `join()` yêu cầu đầu vào (iterable) là một tập hợp các chuỗi, thường gặp nhất là một **List**.
    - Việc giới thiệu và yêu cầu học viên làm việc với `split()` và `join()` tại thời điểm này sẽ dẫn đến việc bắt buộc phải giải thích và thao tác với thực thể **List**. Điều này tạo ra một sự "nhảy cóc" nhận thức lớn khi học viên chưa hề có khái niệm về List (danh sách), cách truy cập phần tử trong List hoặc duyệt qua List.

## 3. ⚠️ Các Điểm Yếu Cần Khắc Phục Khẩn Cấp (Critical Issues)
- **Lesson số:** Lesson 03
  - **Tiêu đề:** String methods
  - **Vấn đề:** Đưa hàm `split()` và `join()` vào nội dung học trong khi cấu trúc dữ liệu **List** thuộc danh sách `forbidden_scope` (CẤM: List, Dict, Set, Function, Class...).
  - **Hậu quả nếu đưa nội dung này vào hệ thống tự động sinh học liệu:** 
    - Hệ thống AI khi sinh bài tập/học liệu cho `split()` sẽ bắt buộc phải tạo ra các đoạn code gán kết quả cho một biến và/hoặc thao tác trên List kết quả đó (ví dụ: lấy phần tử đầu tiên của danh sách sau khi split, hoặc lặp qua danh sách). Việc này vi phạm nghiêm trọng luật chặn (Guardrails), khiến sinh viên hoang mang vì gặp phải cấu trúc dữ liệu lạ chưa được học.
    - Nếu AI cố ép không dùng List, bài giảng về `split()` và `join()` sẽ cực kỳ gượng ép, thiếu tính thực tế và mất đi bản chất ứng dụng của hai hàm này.

- **Lesson số:** Lesson 04
  - **Tiêu đề:** String formatting
  - **Vấn đề:** Việc đưa giữ cả 3 phương pháp định dạng bao gồm `% format`, `.format()`, và `f-string` có thể gây quá tải thông tin không cần thiết với Python hiện đại. Cách dùng `% format` đã cũ (legacy style) và dễ gây nhầm lẫn với toán tử chia lấy dư `%` đã học ở các session trước.

## 4. 🛠 Đề Xuất Chỉnh Sửa Cụ Thể Gửi PM
- **Yêu cầu 1 (Sửa đổi Lesson 03):** 
  - Loại bỏ hoàn toàn hai hàm `split()` và `join()` ra khỏi Lesson 03 của Session 05. Di dời hai hàm này sang Session học về **List** (sau khi học viên đã hiểu khái niệm Danh sách/Mảng và cách duyệt List).
  - Thay thế bằng các String methods hữu ích khác không đòi hỏi kiến thức về List như: `find()`, `count()`, `startswith()`, `endswith()`, hoặc các hàm kiểm tra định dạng như `isdigit()`, `isalpha()`, `isalnum()`.
- **Yêu cầu 2 (Tối ưu hóa Lesson 04):**
  - Khuyến nghị tập trung sâu vào `f-string` (định dạng chuẩn từ Python 3.6+) và `.format()`. Hạn chế hoặc chỉ nhắc qua dạng lý thuyết sơ lược đối với `% format` để tránh gây quá tải nhận thức dòng chảy cho học viên mới bắt đầu.
- **Yêu cầu 3 (Chuẩn hóa Expected Output):**
  - Viết lại phần `expected_output` cho từng Lesson sao cho chi tiết hơn, tránh dùng mẫu câu copy-paste chung chung. Ví dụ, với Lesson 01: *"Học viên hiểu rõ tính bất biến (immutable) của chuỗi qua ví dụ thực tế cố gắng thay đổi một ký tự bằng index và nhận lỗi TypeError; biết cách sử dụng index âm để truy cập từ cuối chuỗi."*

## 5. 🛑 Kết Luận (Verdict)
- **REJECTED** (Chương trình cần được PM điều chỉnh lại cấu trúc phân bổ các hàm `split()` / `join()` để đảm bảo tính toàn vẹn của ràng buộc `forbidden_scope` trước khi đưa vào hệ thống tự động sinh học liệu).