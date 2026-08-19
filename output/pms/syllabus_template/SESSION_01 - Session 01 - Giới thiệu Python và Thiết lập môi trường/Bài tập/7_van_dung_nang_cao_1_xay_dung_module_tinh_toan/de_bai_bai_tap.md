# <center>Xây dựng Module Tính toán và Xuất Hóa đơn Bán hàng POS</center>

### **1. Mục tiêu**
*   **Về kiến thức:** Củng cố kỹ năng khai báo biến, ép kiểu dữ liệu (`type casting`), sử dụng các phép toán số học và định dạng chuỗi ký tự (`string formatting`) trong môi trường Python CLI.
*   **Về kỹ năng:** Luyện tập khả năng phân tích yêu cầu nghiệp vụ thực tế, xác định dữ liệu đầu vào/đầu ra, thiết kế luồng xử lý logic tuyến tính và trình bày hóa đơn bán hàng chuyên nghiệp.
*   **Về tư duy:** Xây dựng tư duy kiểm soát bẫy dữ liệu biên (Edge Cases) trong quá trình thu thập dữ liệu đầu vào từ người dùng tại quầy thanh toán POS.

### **2. Bối cảnh & Vấn đề**
Hệ thống Quản lý Bán hàng Quán Cà phê (Highlands POS) đang nâng cấp phần mềm thu ngân tại quầy. Khi thực hiện order cho khách hàng, thu ngân nhập thông tin sản phẩm, tùy chọn kích thước (Size), số lượng topping đi kèm, cùng thông tin giảm giá dành cho hội viên.

Hiện tại, việc tính toán tiền phụ thu, tiền giảm giá hội viên và tiền thuế giá trị gia tăng (VAT) thủ công thường xảy ra sai sót vào các giờ cao điểm. Bộ phận kỹ thuật yêu cầu bạn phát triển một module tự động bằng Python để nhận dữ liệu từ màn hình thu ngân, thực hiện tính toán chính xác số tiền và xuất phiếu thu (Receipt) ra màn hình với định dạng rõ ràng, minh bạch.

### **3. Quy tắc nghiệp vụ**
Hệ thống POS áp dụng các quy tắc tính giá tiền cho đơn hàng như sau:

1. **Giá sản phẩm cơ bản (Size S):** Được nhập trực tiếp vào hệ thống dưới dạng số nguyên (VNĐ).
2. **Phụ thu Kích thước (Size):**
   * Size S: Phụ thu 0 VNĐ.
   * Size M: Phụ thu 6.000 VNĐ.
   * Size L: Phụ thu 10.000 VNĐ.
3. **Phụ thu Topping:** Mỗi loại topping thêm có đơn giá cố định là 8.000 VNĐ/topping.
4. **Đơn giá một ly hoàn chỉnh (Item Unit Price):**
   `Đơn giá 1 ly = Giá cơ bản (Size S) + Phụ thu Size + (Số lượng topping * 8.000)`
5. **Tổng tiền hàng trước giảm giá (Subtotal):**
   `Subtotal = Đơn giá 1 ly * Số lượng mua`
6. **Chiết khấu thành viên (Discount):**
   * Khách hàng nhập tỷ lệ giảm giá dạng phần trăm (ví dụ: `10` tương đương `10%` đối với Thẻ Vàng, `0` đối với Thẻ Thường).
   * `Số tiền giảm giá = Subtotal * \left((Tỷ lệ giảm giá) / (100)\right)`
7. **Thuế giá trị gia tăng (VAT):**
   * Thuế suất VAT áp dụng cố định là 8% trên tổng số tiền sau khi đã giảm giá.
   * `Số tiền VAT = (Subtotal - Số tiền giảm giá) * 0.08`
8. **Tổng tiền thanh toán cuối cùng (Final Total):**
   * `Tổng thanh toán = (Subtotal - Số tiền giảm giá) + Số tiền VAT`
   * Kết quả tổng tiền phải được làm tròn về số nguyên gần nhất trước khi in ra hóa đơn.

### **4. Yêu cầu bài toán**

Học viên hoàn thành bài tập theo 2 phần bắt buộc:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Report)**
1. **Phân tích I/O (Input/Output):** Xác định toàn bộ các biến dữ liệu đầu vào (tên biến, kiểu dữ liệu, ý nghĩa) và các biến dữ liệu đầu ra cần hiển thị.
2. **Thiết kế các bước xử lý:** Lập danh sách các bước tính toán theo thứ tự thực thi hoặc vẽ sơ đồ luồng dữ liệu (Flowchart) chuẩn hóa Mermaid.

#### **Phần 2: Triển khai Mã nguồn Python (CLI Code)**
1. Viết chương trình Python thu thập thông tin từ bàn phím thông qua hàm `input()` gồm:
   * Tên đồ uống (`str`).
   * Đơn giá cơ bản của Size S (`int` hoặc `float`).
   * Số tiền phụ thu Size (`int` hoặc `float`).
   * Số lượng topping đi kèm (`int`).
   * Số lượng ly đặt mua (`int`).
   * Tỷ lệ giảm giá hội viên (%) (`float`).
2. Thực hiện ép kiểu dữ liệu phù hợp để phục vụ tính toán.
3. Áp dụng công thức nghiệp vụ để tính toán: Đơn giá thực tế 1 ly, Tổng tiền hàng (Subtotal), Số tiền giảm giá, Số tiền VAT, và Tổng tiền thanh toán.
4. Xử lý các bẫy dữ liệu biên (ví dụ: kiểm tra số lượng phải lớn hơn 0, đơn giá không được âm).
5. In ra màn hình hóa đơn bán hàng (POS Receipt) chuẩn hóa dạng text với đường viền căn chỉnh chuyên nghiệp.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex7`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex7`
