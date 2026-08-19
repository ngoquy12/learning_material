# <center>[Phân tích 3] Phân tích và Triển khai Module Tính tiền Hóa đơn Quầy POS</center>

### **1. Mục tiêu**
*   **Kỹ năng đạt được:** Phân tích, so sánh và lựa chọn phương án kỹ thuật tối ưu trong việc tiếp nhận dữ liệu đầu vào (tên món, giá niêm yết, phụ thu size, topping, giảm giá thành viên) và tính toán các chi tiết hóa đơn thanh toán trên phần mềm Highlands POS.
*   **Kiến thức áp dụng:** Sử dụng thành thạo các câu lệnh nhập/xuất dữ liệu (`input()`, `print()`), chuyển đổi kiểu dữ liệu cơ bản (`int()`, `float()`, `str()`), thực hiện phép toán số học và định dạng chuỗi văn bản nâng cao trong Python (không sử dụng cấu trúc điều khiển phức tạp hay thư viện ngoài).
*   **Tư duy lập trình:** Đánh giá trade-off giữa các giải pháp tính toán trực tiếp và giải pháp lưu trữ trung gian về mặt hiệu năng, dung lượng bộ nhớ và khả năng bảo trì mã nguồn.

### **2. Bối cảnh & Vấn đề**
Tại quầy thu ngân của chuỗi Highland Coffee, phần mềm POS (Point of Sale) đóng vai trò cốt lõi trong việc ghi nhận đơn hàng từ thu ngân và in hóa đơn thanh toán cho khách hàng. 

Khi một giao dịch order diễn ra, thu ngân sẽ nhập vào màn hình hệ thống các thông số chi tiết của món đồ uống. Hệ thống cần tiếp nhận các chuỗi dữ liệu nhập từ bàn phím, thực hiện ép kiểu sang dạng số thích hợp, thực hiện chuỗi phép tính tài chính theo quy chuẩn nghiệp vụ, và xuất ra màn hình console một hóa đơn thanh toán dạng văn bản được căn chỉnh lề chuyên nghiệp.

Thu ngân gặp phải bài toán: Cần xử lý các phép tính giảm giá theo tỷ lệ %, tính thuế VAT 8%, và tính tổng tiền thanh toán làm tròn thành số nguyên VNĐ mà không làm mất tính chính xác của dữ liệu tài chính cũng như đảm bảo mã nguồn dễ bảo trì khi quy định phụ thu thay đổi.

### **3. Quy tắc nghiệp vụ**
Hệ thống tính tiền đơn hàng áp dụng các quy tắc tài chính sau:
1.  **Đơn giá cơ bản:** Đơn giá niêm yết áp dụng cho kích thước nhỏ nhất (Size S).
2.  **Phụ thu kích thước (Size):** 
    *   Size S: 0 VNĐ.
    *   Size M: Phụ thu 6.000 VNĐ.
    *   Size L: Phụ thu 10.000 VNĐ.
    *(Thu ngân nhập trực tiếp số tiền phụ thu kích thước dạng số nguyên: 0, 6000, hoặc 10000).*
3.  **Phụ thu Topping:** Mỗi topping thêm có giá cố định **8.000 VNĐ/topping**. 
    *   `Tổng tiền topping = Số lượng topping * 8000`.
4.  **Giá đơn vị 1 ly hoàn chỉnh:** 
    *   `Giá 1 ly = Đơn giá cơ bản + Phụ thu size + Tổng tiền topping`.
5.  **Tổng tiền hàng chưa giảm (Subtotal):** 
    *   `Tổng tiền hàng = Giá 1 ly * Số lượng ly`.
6.  **Chiết khấu thành viên (Gold Discount):** 
    *   Nhập vào tỷ lệ giảm giá (ví dụ: `10` nghĩa là 10%, `0` nghĩa là không giảm).
    *   `Số tiền giảm = Tổng tiền hàng * (Tỷ lệ giảm giá / 100)`.
7.  **Tiền sau chiết khấu:** 
    *   `Tiền sau giảm = Tổng tiền hàng - Số tiền giảm`.
8.  **Thuế giá trị gia tăng (VAT):** 
    *   Áp dụng mức thuế cố định **8%** trên số tiền sau giảm.
    *   `Tiền thuế VAT = Tiền sau giảm * 0.08`.
9.  **Tổng tiền thanh toán cuối cùng (Final Total):** 
    *   `Tổng thanh toán = Tiền sau giảm + Tiền thuế VAT`.
    *   Số tiền thanh toán cuối cùng được ép kiểu số nguyên (`int`) để phù hợp với mệnh giá thanh toán tiền mặt/chuyển khoản VNĐ.

### **4. Yêu cầu bài toán**
Học viên đóng vai trò là Lập trình viên Python cho hệ thống POS, cần hoàn thành 3 phần báo cáo và triển khai sau:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Tự đề xuất ít nhất **2 giải pháp kỹ thuật khác nhau** để giải quyết bài toán nhập liệu, tính toán các thành phần hóa đơn và in kết quả ra console (ví dụ: giải pháp tính toán dồn biểu thức biểu diễn trực tiếp vs giải pháp tách biệt các biến lưu trữ từng bước trung gian).
*   Xây dựng bảng so sánh Trade-off trực quan giữa 2 giải pháp theo 5 tiêu chí bắt buộc:
    1. Tốc độ xử lý (Execution Speed / Time Complexity)
    2. Dung lượng bộ nhớ tiêu thụ (Memory / Variable Overhead)
    3. Khả năng bảo trì và mở rộng (Maintainability)
    4. Độ dễ đọc và hiểu của mã nguồn (Readability)
    5. Trường hợp sử dụng phù hợp (Suitability)

#### **Phần 2: Giải trình Lựa chọn và Thiết kế Lưu đồ Luồng (Flowchart)**
*   Đưa ra lý giải khoa học thuyết phục cho việc lựa chọn giải pháp tối ưu nhất cho phần mềm POS quầy thu ngân.
*   Thiết kế lưu đồ thuật toán (sử dụng biểu đồ Mermaid) hoặc viết mã giả (Pseudocode) chi tiết mô tả chuỗi xử lý từ lúc nhập dữ liệu từ thu ngân đến khi in ra hóa đơn thanh toán.
*   *Lưu ý về Mermaid:* Phải sử dụng đúng 5 dạng hình chuẩn: Oval cho Start/End `([ ])`, Hình bình hành cho Input/Output `[/ /]`, Hình chữ nhật cho Process `[" "]`, Hình thoi cho Decision (nếu có), và Mũi tên luồng `-->`.

#### **Phần 3: Triển khai Mã nguồn & Xử lý lỗi biên**
*   Viết chương trình Python hoàn chỉnh thực thi giải pháp tối ưu đã chọn.
*   Yêu cầu về mã nguồn:
    *   Tên biến, định danh (Identifiers) viết bằng **Tiếng Anh** đúng chuẩn Naming Convention (`snake_case`).
    *   Các đoạn chú thích (Comments) giải thích logic và các thông điệp giao diện CLI viết bằng **Tiếng Việt có dấu**.
    *   Xử lý ép kiểu dữ liệu an toàn (`str` sang `int`/`float`).
    *   In hóa đơn thanh toán có định dạng căn lề, kẻ bảng phân cách rõ ràng, chuyên nghiệp.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex12`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex12`
