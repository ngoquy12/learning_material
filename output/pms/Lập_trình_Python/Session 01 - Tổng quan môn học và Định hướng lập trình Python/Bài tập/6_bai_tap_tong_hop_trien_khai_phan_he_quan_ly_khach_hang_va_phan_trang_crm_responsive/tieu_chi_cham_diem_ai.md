### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Triển khai phân hệ quản lý khách hàng và phân trang CRM responsive — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Tạo file mã nguồn Python tiêu chuẩn, chạy thành công bằng Python 3.10+ mà không phụ thuộc thư viện bên ngoài.
*   **[10 điểm] Xây dựng Cấu trúc dữ liệu:** Khai báo cấu trúc lưu trữ thông tin khách hàng (class hoặc dict) đầy đủ các trường `customer_id`, `full_name`, `contract_value` với Type Hints chính xác.

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Chức năng Thêm & Xóa bản ghi trong RAM:**
    *   Thêm mới thành công khách hàng vào tập dữ liệu lưu trữ RAM.
    *   Xóa thành công khách hàng theo `customer_id`.
*   **[20 điểm] Chức năng Tính toán Layout & Phân trang Responsive:**
    *   Phân loại chính xác `device_category` (MOBILE, TABLET, DESKTOP) dựa trên `viewport_width`.
    *   Tính toán đúng `max_customers_per_page` và `layout_columns`.
    *   Cắt đúng danh sách khách hàng ứng với số trang `page_number` được truyền vào.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Xử lý trùng lặp và dữ liệu không hợp lệ:** Kích hoạt chính xác ngoại lệ `ValueError` khi thêm trùng mã `customer_id` hoặc khi `contract_value < 0`.
*   **[10 điểm] Xử lý bản ghi không tồn tại:** Kích hoạt chính xác ngoại lệ `KeyError` khi thực hiện xóa mã `customer_id` không có trong hệ thống.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra & Quy chuẩn PEP 8:** Tên biến/hàm 100% bằng Tiếng Anh (`snake_case`), chú thích logic bằng Tiếng Việt có dấu, output kết quả phân trang rõ ràng, định dạng đẹp mắt.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session01_Ex06`.