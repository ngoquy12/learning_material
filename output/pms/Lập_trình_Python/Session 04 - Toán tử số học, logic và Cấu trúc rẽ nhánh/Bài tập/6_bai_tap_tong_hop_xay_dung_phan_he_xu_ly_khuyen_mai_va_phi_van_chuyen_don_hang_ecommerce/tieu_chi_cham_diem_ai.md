### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Xây dựng phân hệ xử lý khuyến mãi và phí vận chuyển đơn hàng E-commerce — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Tạo thư mục dự án chuẩn, tệp thực thi Python độc lập, không sử dụng thư viện ngoài trái phép.
*   **[10 điểm] Xây dựng Cấu trúc dữ liệu:** Định nghĩa cấu trúc dictionary/object chứa kết quả tính toán chi tiết đơn hàng đầy đủ các trường thông tin theo đúng yêu cầu.

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Xử lý logic giảm giá và phí vận chuyển:** Áp dụng đúng thứ tự ưu tiên giảm giá (Loại 1 -> Loại 2 -> Loại 3), tính đúng số tiền giảm thực tế có áp mức trần (max cap) và phí vận chuyển.
*   **[20 điểm] Tính tổng thanh toán và quà tặng:** Tính toán chính xác tổng chi phí cuối cùng `final_payment` và xác định đúng trạng thái nhận quà tặng `has_gift`.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Kiểm soát dữ liệu đầu vào:** Bắt lỗi chính xác và bắn ngoại lệ `ValueError` khi `order_value` <= 0 hoặc hạng thành viên / phương thức thanh toán nằm ngoài danh sách cho phép.
*   **[10 điểm] Phẳng hóa điều kiện (PEP 8 Flattening):** Loại bỏ hoàn toàn bẫy Arrow Anti-Pattern, sử dụng hiệu quả toán tử logic `and`, `or`, `not` cùng cấu trúc `if-elif-else` phẳng.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra sạch:** Mã nguồn tuân thủ PEP 8 (snake_case, thụt lề 4 khoảng trắng, Type Hints), tên biến/hàm bằng tiếng Anh, có chú thích tiếng Việt minh bạch.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub tuân thủ chính xác định dạng thư mục `[Tên Lớp]_[Môn Học]_Session04_Ex06`.