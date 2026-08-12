### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Tính toán hóa đơn POS và kiểm định điều kiện ưu đãi đa chỉ tiêu — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê chính xác toàn bộ các biến đầu vào (đơn giá base, mã size, số topping, số lượng, điểm tích lũy, cờ thẻ vàng, cờ giờ vàng) kèm kiểu dữ liệu (`int`, `float`, `bool`) và các biến đầu ra tương ứng.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế sơ đồ luồng:** Giải trình giải pháp toán học đại số boolean thay thế `if/else` và vẽ sơ đồ luồng Mermaid đầy đủ, sử dụng đúng 5 dạng hình chuẩn theo quy định.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo và ép kiểu dữ liệu:** Đọc dữ liệu từ bàn phím bằng `input()` và thực hiện ép kiểu chính xác (`int()`, `float()`, `bool()`) không gây lỗi runtime.
*   **[15 điểm] Triển khai biểu thức số học & phụ thu:** Tính đúng phụ thu Size ly (`size_code == 1` * 6000 + `size_code == 2` * 10000), phụ thu topping, đơn giá ly thành phẩm và tổng tiền hàng trước giảm giá.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Xử lý logic ưu đãi đa điều kiện:** Thiết lập chính xác biểu thức logic kết hợp `and`, `or` đại diện cho 3 tiêu chí ưu đãi (Thẻ vàng OR (Đơn lớn AND Giờ vàng) OR Điểm cao) và tính số tiền giảm giá chính xác.
*   **[15 điểm] Kiểm định hóa đơn & Tích điểm:** Thiết lập biểu thức logic kiểm tra hóa đơn hợp lệ (`is_valid_order`) kết hợp toán tử `not`, `and` và tính đúng số điểm tích lũy mới bằng phép chia lấy phần nguyên `//`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Hiển thị kết quả rõ ràng:** In ra màn hình đầy đủ, định dạng đẹp mắt các thông số hóa đơn và thông điệp trạng thái hợp lệ của giao dịch.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tên biến tuân thủ tiêu chuẩn `snake_case` bằng tiếng Anh, viết chú thích mã nguồn bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu hóa biểu thức logic:** Viết biểu thức tính toán phụ thu và điều kiện giảm giá ngắn gọn, tối ưu, tận dụng triệt để tính chất ép kiểu tự động của toán tử số học trên dữ liệu kiểu boolean.