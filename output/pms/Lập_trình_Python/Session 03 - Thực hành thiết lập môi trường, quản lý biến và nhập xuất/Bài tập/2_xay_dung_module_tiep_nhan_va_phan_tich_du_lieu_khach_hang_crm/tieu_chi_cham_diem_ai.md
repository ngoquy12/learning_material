### **Tiêu chí chấm điểm (AI)**

**Xây dựng Module Tiếp nhận và Phân tích Dữ liệu Khách hàng CRM — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm**: Tạo tập tin `crm_intake.py` đúng cấu trúc, có khai báo Module Docstring ở đầu file mô tả đầy đủ tác giả, mục đích chương trình và ngữ cảnh CRM.

#### **2. Logic nghiệp vụ (30 điểm)**
- **15 điểm**: Tiếp nhận đầy đủ 4 tham số từ bàn phím bằng `input()` đúng thứ tự bài toán yêu cầu.
- **15 điểm**: Áp dụng chuẩn xác công thức tính toán `loyalty_score` và `estimated_clv`. Kết quả phép tính chính xác tuyệt đối theo dữ liệu đầu vào.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **15 điểm**: Ép kiểu dữ liệu bắt buộc (Explicit Type Casting) chính xác: `annual_spending` sang `float`, `support_ticket_count` sang `int`.
- **15 điểm**: Định dạng số liệu đầu ra chính xác 2 chữ số thập phân bằng `f-string` (ví dụ: `:.2f`).

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **10 điểm**: Sử dụng hiệu quả hàm `print()` với tham số `sep` hoặc `end` để định dạng khung hiển thị thay vì cộng chuỗi thủ công.
- **10 điểm**: Tối ưu toán tử số học, không khai báo các biến trung gian thừa thãi không sử dụng.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **5 điểm**: Tuân thủ hoàn toàn quy tắc đặt tên biến `snake_case` theo chuẩn PEP 8. Không có tên biến vô nghĩa hay viết tắt gây khó hiểu.
- **5 điểm**: Viết ghi chú (comments) giải thích rõ ràng cho từng bước: Nhập dữ liệu -> Ép kiểu -> Tính toán -> In báo cáo.

#### **Điểm cộng (5-10 điểm)**
- **+5 điểm**: Sử dụng phương thức `.strip()` hoặc `.title()` xử lý chuỗi nhập vào cho `customer_name` và `customer_email` để dữ liệu chuẩn hóa sạch sẽ trước khi in.
- **+5 điểm**: Định dạng số tiền hiển thị có dấu phân cách hàng nghìn (ví dụ: `25,000,000.50`) bằng định dạng chuỗi nâng cao `f"{annual_spending:,.2f}"`.