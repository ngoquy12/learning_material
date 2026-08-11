### **Tiêu chí chấm điểm (AI)**
**Xây dựng Module Tính Hóa Đơn Đơn Hàng Thương Mại Điện Tử — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- Khởi tạo thành công thư mục dự án và tạo môi trường ảo `.venv` đúng quy cách (5 điểm).
- Khai báo đầy đủ header docstring đầu file `calculate_order.py` mô tả thông tin bài tập và cấu trúc mã nguồn (5 điểm).

#### **2. Logic nghiệp vụ (30 điểm)**
- Nhập đầy đủ 6 tham số thông tin từ bàn phím qua hàm `input()` (10 điểm).
- Áp dụng chính xác 3 công thức tính toán toán học: tính tiền hàng `subtotal`, tính tiền chiết khấu `discount_amount`, và tính tổng thanh toán `total_payment` (20 điểm).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- Thực hiện ép kiểu dữ liệu tường minh (Explicit Type Casting) từ `str` sang `int` cho số lượng sản phẩm (10 điểm).
- Thực hiện ép kiểu dữ liệu tường minh từ `str` sang `float` cho đơn giá, tỷ lệ giảm giá và phí giao hàng (15 điểm).
- Chuyển đổi và xử lý hiển thị đúng kiểu dữ liệu ra màn hình không phát sinh lỗi kiểu dữ liệu (TypeError) khi thực hiện cộng chuỗi/tính toán (5 điểm).

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- Cấu trúc luồng thực thi chương trình tuần tự rõ ràng: Nhập dữ liệu (Input) -> Chuyển đổi dữ liệu & Tính toán (Process) -> Xuất kết quả (Output) (10 điểm).
- Sử dụng hiệu quả hàm `print()` kết hợp tham số `sep` hoặc `end` để định dạng kết quả hiển thị Console gọn gàng, trực quan (10 điểm).

#### **5. Chất lượng mã nguồn (10 điểm)**
- Tuân thủ 100% quy tắc đặt tên biến theo chuẩn `snake_case` của Python PEP 8 (5 điểm).
- Mã nguồn trình bày sạch sẽ, thụt lề chuẩn xác 4 dấu cách, có bổ sung các dòng ghi chú (comment `#`) giải thích các bước tính toán (5 điểm).

#### **Điểm cộng (5-10 điểm)**
- (5 điểm) Định dạng xuất dữ liệu đẹp mắt bằng `f-string` kết hợp căn chỉnh lề chuyên nghiệp.