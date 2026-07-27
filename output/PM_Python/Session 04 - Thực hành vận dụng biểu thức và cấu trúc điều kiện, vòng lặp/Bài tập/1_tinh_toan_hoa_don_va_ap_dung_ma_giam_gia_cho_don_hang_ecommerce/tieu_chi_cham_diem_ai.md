### **Tiêu chí chấm điểm (AI)**
**Tính Toán Hóa Đơn và Áp Dụng Mã Giảm Giá Cho Đơn Hàng Ecommerce — Tổng điểm: 100 điểm**

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
* **Tên file và thư mục (10 điểm):** Đặt tên thư mục dự án và tên tệp tin chính xác theo cấu trúc `tinh_toan_hoa_don_ecommerce/order_calculator.py`.
* **Khai báo hàm có tham số (10 điểm):** Khai báo đúng 3 hàm `calculate_item_total`, `calculate_shipping`, `apply_discount` với số lượng và kiểu dữ liệu tham số đúng như yêu cầu của đề bài.

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
* **Logic tính phí vận chuyển (10 điểm):** Xác định đúng mức phí `30000.0` và chuyển đổi về `0.0` khi đơn hàng đạt mức `500000.0` trở lên hoặc khi nhập coupon `"FREESHIP"`.
* **Logic áp dụng giảm giá (10 điểm):** Áp dụng chính xác giảm giá `10%` cho coupon `"GIAOTRINH10"`, và mặc định trả về `0.0` cho các trường hợp khác.
* **Vòng lặp tích lũy sản phẩm (10 điểm):** Thiết lập đúng cấu trúc vòng lặp `while` để nhập sản phẩm liên tục và dừng chính xác khi nhập đơn giá bằng `0`.

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
* **Kiểm tra đơn giá hợp lệ (15 điểm):** Yêu cầu nhập lại nếu đơn giá nhỏ hơn 0, không làm gián đoạn hay crash chương trình.
* **Kiểm tra số lượng hợp lệ (15 điểm):** Yêu cầu nhập lại nếu số lượng sản phẩm nhập vào nhỏ hơn hoặc bằng 0.

#### **4. Kiểm thử hoặc câu hỏi lý thuyết bổ sung — 10 điểm**
* **Hiển thị báo cáo chi tiết (10 điểm):** Kết quả in ra giao diện console phải hiển thị đầy đủ và rõ ràng các trường dữ liệu: Tạm tính (Subtotal), Phí vận chuyển (Shipping fee), Tiền giảm giá (Discount), và Tổng thanh toán (Total payment) theo định dạng số thực.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **Quy chuẩn mã nguồn (5 điểm):** Tên biến và hàm tuân thủ quy tắc PEP 8 (snake_case), mã nguồn không có mã dư thừa hoặc sử dụng thư viện ngoài phạm vi buổi học (Session 04).
* **Quy chuẩn nộp bài (5 điểm):** Mã nguồn được đẩy lên kho chứa GitHub công khai và liên kết nộp bài hợp lệ.

#### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**
* **Định dạng bảng hóa đơn (5 điểm):** In hóa đơn có viền trang trí sử dụng dấu gạch ngang `-`, dấu cộng `+` và căn lề đẹp mắt.
* **Tính năng tạo nhiều đơn hàng (5 điểm):** Sử dụng vòng lặp lồng để hỏi người dùng có muốn xử lý đơn hàng tiếp theo hay không sau khi xuất hóa đơn.