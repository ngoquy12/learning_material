### **Tiêu chí chấm điểm (AI)**
**Thực Hành Kiểm Tra Logic Và Tính Toán Hóa Đơn Thanh Toán Đơn Hàng Thương Mại Điện Tử — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm**: Khởi tạo file `main.py` đúng cấu trúc, khai báo đầy đủ các biến đầu vào qua hàm `input()`, sử dụng chuẩn đặt tên biến `snake_case` theo PEP 8 (như `customer_name`, `member_tier`, `order_amount`, `promo_code`).
- **5 điểm**: Khởi tạo biến đầy đủ nhưng chưa tuân thủ chuẩn đặt tên `snake_case` hoặc đặt tên biến ngắn gọn, khó hiểu (ví dụ: `a`, `b`, `tier1`).
- **0 điểm**: Không khởi tạo đúng file mã nguồn hoặc thiếu phần nhập dữ liệu đầu vào.

#### **2. Logic nghiệp vụ (30 điểm)**
- **30 điểm**: Thực hiện chính xác tất cả các quy tắc rẽ nhánh kinh doanh:
  + Xác định đúng phần trăm giảm giá theo hạng thành viên `GOLD` (10%), `SILVER` (5%), `BRONZE`/khác (0%).
  + Đánh giá đúng điều kiện miễn phí vận chuyển bằng toán tử logic `or` (`order_amount >= 500000` hoặc `promo_code == "FREESHIP"`).
  + Đánh giá đúng điều kiện giảm giá bổ sung bằng toán tử logic `and` (`promo_code == "SALE10"` và `order_amount >= 200000`).
  + Tính toán chính xác tổng tiền thanh toán theo đúng công thức nghiệp vụ.
- **20 điểm**: Tính toán đúng phần lớn logic nhưng vi phạm 1 điều kiện rẽ nhánh (ví dụ: dùng sai toán tử `and`/`or` khi tính phí ship hoặc mã giảm giá).
- **10 điểm**: Chỉ tính đúng chiết khấu hạng thành viên, sai toàn bộ logic phí vận chuyển và mã giảm giá.
- **0 điểm**: Viết sai cấu trúc rẽ nhánh, kết quả tổng tiền thanh toán không chính xác.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **30 điểm**: Ép kiểu dữ liệu `float()` chính xác cho giá trị đơn hàng. Kiểm tra `order_amount <= 0` ngay từ đầu, in đúng thông báo lỗi và ngăn chặn chương trình thực hiện các phép tính phía sau.
- **15 điểm**: Có chuyển đổi kiểu dữ liệu nhưng thiếu câu lệnh `if` kiểm tra điều kiện `order_amount <= 0`, dẫn đến chương trình vẫn tiếp tục tính toán với số tiền âm.
- **0 điểm**: Không ép kiểu dữ liệu khiến chương trình báo lỗi crash (TypeError) khi thực hiện phép so sánh hoặc toán số học.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **20 điểm**: Sử dụng cấu trúc rẽ nhánh tối ưu `if-elif-else`, không lặp lại các câu lệnh điều kiện thừa. Áp dụng hiệu quả cơ chế Short-circuit Evaluation của toán tử logic Python.
- **10 điểm**: Dùng chuỗi nhiều câu lệnh `if` độc lập thay vì `if-elif-else`, làm chương trình phải đánh giá lại các điều kiện đã thỏa mãn trước đó.
- **0 điểm**: Cấu trúc điều kiện hỗn loạn, lồng nhau quá 4 cấp không cần thiết gây khó đọc và giảm hiệu năng thực thi.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **10 điểm**: Mã nguồn trình bày sạch sẽ, tuân thủ nghiêm ngặt chuẩn PEP 8 (thụt lề 4 khoảng trắng, khoảng cách giữa các toán tử hợp lý), có ghi chú (comment `#`) giải thích rõ ràng các khối logic.
- **5 điểm**: Mã nguồn chạy đúng nhưng trình bày chưa chuẩn PEP 8 (thiếu khoảng trắng xung quanh toán tử, thụt lề không đều) hoặc hoàn toàn không có ghi chú.
- **0 điểm**: Code cẩu thả, đặt tên biến vi phạm quy chuẩn, thụt lề sai gây lỗi IndentationError.

#### **Điểm cộng (5-10 điểm)**
- **+5 điểm**: Chuẩn hóa dữ liệu đầu vào chuỗi ký tự bằng các phương thức xử lý chuỗi cơ bản như `.upper()` hoặc `.strip()` để chấp nhận chữ thường/chữ hoa (ví dụ: nhập `"gold"` vẫn hiểu là `"GOLD"`).
- **+5 điểm**: Định dạng số tiền đầu ra hiển thị có dấu phân cách hàng nghìn rõ ràng hoặc định dạng số thập phân đẹp mắt.