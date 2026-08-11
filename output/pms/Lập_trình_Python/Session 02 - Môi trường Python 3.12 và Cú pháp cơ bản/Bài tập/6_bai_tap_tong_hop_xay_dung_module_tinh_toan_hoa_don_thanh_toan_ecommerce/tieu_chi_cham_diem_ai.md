### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Xây dựng module tính toán hóa đơn thanh toán E-commerce — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Tạo cấu trúc thư mục và file `main.py` chuẩn xác, chạy thành công bằng môi trường Python 3.12 không gặp lỗi cú pháp.
*   **[10 điểm] Xây dựng Cấu trúc dữ liệu:** Khai báo đầy đủ các biến lưu trữ thông tin sản phẩm bằng tiếng Anh (`product_name`, `unit_price`, `quantity`, `discount_rate`, `shipping_fee`) chuẩn định dạng `snake_case`.

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Chức năng Đọc/Xem danh sách:** Sử dụng hàm `input()` để nhận thông tin từ người dùng và thực hiện ép kiểu dữ liệu chính xác (`float()` cho đơn giá, chiết khấu, phí vận chuyển; `int()` cho số lượng mua).
*   **[20 điểm] Chức năng Ghi/Thêm mới:** Thực hiện đúng và đủ các phép tính số học: tổng tiền hàng gốc, tiền giảm giá, tiền hàng sau giảm và tổng tiền thanh toán cuối cùng.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Xử lý trùng lặp:** Chặn hoàn toàn bẫy cộng/nhân chuỗi (string concatenation) bằng cách thực hiện ép kiểu số ngay sau khi nhận dữ liệu từ `input()`.
*   **[10 điểm] Xử lý bản ghi không tồn tại:** Tính toán đúng tỷ lệ phần trăm chiết khấu (`discount_rate / 100`) và cộng phụ phí vận chuyển vào tổng hóa đơn mà không phát sinh sai lệch số học.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra sạch:** Xuất hóa đơn ra màn hình console gọn gàng, sử dụng hợp lý các tham số `sep` và `end` của hàm `print()`, tuyệt đối không dùng emoji, giải thích mã nguồn bằng tiếng Việt có dấu.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn hoàn chỉnh lên repository GitHub theo đúng quy định tên thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex06`.