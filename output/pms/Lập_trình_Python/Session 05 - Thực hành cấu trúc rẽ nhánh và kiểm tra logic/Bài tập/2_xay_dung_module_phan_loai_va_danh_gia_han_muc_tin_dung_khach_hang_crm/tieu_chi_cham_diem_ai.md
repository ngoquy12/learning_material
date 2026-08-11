### **Tiêu chí chấm điểm (AI)**
**Module Phân loại và Đánh giá Hạn mức Tín dụng Khách hàng CRM — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **5 điểm**: Tạo cấu trúc file `main.py` đúng quy định, chạy thành công trên Python 3.12 mà không phát sinh lỗi cú pháp (SyntaxError).
- **5 điểm**: Thực hiện nhập đúng 5 tham số đầu vào (`company_name`, `annual_revenue`, `employee_count`, `years_in_business`, `payment_history_score`) từ bàn phím với thông báo hướng dẫn rõ ràng.

#### **2. Logic nghiệp vụ (30 điểm)**
- **15 điểm**: Xây dựng chính xác các câu lệnh rẽ nhánh phân hạng doanh nghiệp (`Enterprise`, `SMB`, `Startup / Micro`) bằng toán tử logic `and`.
- **15 điểm**: Xây dựng chính xác cấu trúc rẽ nhánh lồng nhau để tính toán hạn mức tín dụng và trạng thái phê duyệt phù hợp với từng hạng doanh nghiệp và khoảng điểm lịch sử thanh toán.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **15 điểm**: Đã viết đầy đủ điều kiện kiểm tra dữ liệu đầu vào (`annual_revenue > 0`, `employee_count > 0`, `years_in_business >= 0`, `0 <= payment_history_score <= 100`).
- **15 điểm**: Xuất thông báo lỗi có tiền tố `[ERROR]` chi tiết và ngắt luồng xử lý chương trình ngay khi phát hiện dữ liệu vi phạm.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **10 điểm**: Tận dụng cấu trúc `if-elif-else` hợp lý, tránh lặp lại các câu lệnh kiểm tra điều kiện không cần thiết (tối ưu Short-circuit evaluation).
- **10 điểm**: Thực hiện ép kiểu dữ liệu `float()` và `int()` ngay tại thời điểm nhận dữ liệu từ `input()`.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **5 điểm**: Tuân thủ chuẩn PEP 8 về đặt tên biến (`snake_case`), quy tắc thụt lề 4 spaces, khoảng trắng hợp lý quanh toán tử.
- **5 điểm**: Viết chú thích code (comments) rõ ràng, thể hiện mục đích nghiệp vụ của từng đoạn mã rẽ nhánh.

#### **Điểm cộng (5-10 điểm)**
- **5 điểm**: Định dạng giá trị hạn mức tín dụng hiển thị ra màn hình với dấu phân cách hàng nghìn (ví dụ: `5,000,000,000 VNĐ`).
- **5 điểm**: Xử lý làm sạch khoảng trắng thừa ở hai đầu chuỗi tên doanh nghiệp bằng hàm `.strip()`.