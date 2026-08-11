### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Hệ thống Quản lý và Xử lý Đơn hàng Flash Sale E-Commerce — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Tạo file mã nguồn sạch, cấu trúc dự án đúng chuẩn, khai báo entry point thực thi chương trình.
*   **[10 điểm] Xây dựng Cấu trúc dữ liệu:** Khai báo danh sách sản phẩm (`list[dict]`) với đầy đủ các trường `product_id`, `name`, `price`, `stock` có Type Hints chính xác (`str`, `int | float`).

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Chức năng Đọc/Xem danh sách:** Triển khai chức năng 1 hiển thị toàn bộ danh sách sản phẩm tồn kho bằng vòng lặp `for` rõ ràng, định dạng thông tin trực quan.
*   **[20 điểm] Chức năng Ghi/Thêm mới:** Triển khai thành công chức năng 2 (tiếp nhận đơn hàng, cập nhật số lượng tồn kho và cộng doanh thu) cùng chức năng 3 (bổ sung số lượng tồn kho).

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Xử lý xác thực sản phẩm:** Kiểm tra mã sản phẩm tồn tại trong danh sách kho, xuất thông báo `[LỖI]` nếu mã không tồn tại.
*   **[10 điểm] Xử lý tồn kho & lựa chọn sai:** Kiểm tra điều kiện tồn kho trước khi tạo đơn hàng (`quantity > stock`), đưa ra thông báo cảnh báo chính xác và xử lý khi nhập lựa chọn menu ngoài phạm vi (1-4).

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra sạch:** Tuân thủ PEP 8, Type Hints, sử dụng tiếng Anh cho tên biến/hàm, tiếng Việt có dấu cho thông báo CLI. Tuyệt đối KHÔNG sử dụng `while`, `break`, `continue`.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Push mã nguồn lên GitHub đúng chuẩn định dạng thư mục `[Tên Lớp]_[Môn Học]_Session06_Ex06`.