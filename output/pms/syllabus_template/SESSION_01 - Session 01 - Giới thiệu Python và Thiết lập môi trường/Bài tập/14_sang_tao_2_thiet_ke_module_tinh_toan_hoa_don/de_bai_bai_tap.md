# <center>[Sáng tạo 2] Thiết kế Module Tính toán Hóa đơn và Phân tích Doanh thu POS Linh hoạt</center>

### **1. Mục tiêu**
*   Vận dụng sáng tạo kiến thức khai báo biến, chuyển đổi kiểu dữ liệu (`int`, `float`, `str`) và định dạng chuỗi xuất dữ liệu trong Python để thiết kế mô hình tính toán hóa đơn thanh toán linh hoạt cho quầy bán hàng.
*   Tự chủ đề xuất cấu trúc dữ liệu đầu vào/đầu ra (I/O Schema) và phân tích các kịch bản dữ liệu biên (Edge Cases) thực tế tại quầy thanh toán POS.
*   Xây dựng sơ đồ luồng dữ liệu (Data Flow Diagram) chuẩn kỹ thuật bằng Mermaid biểu thị toàn bộ tiến trình xử lý tài chính của giao dịch bán hàng.
*   Rèn luyện tư duy thiết kế giải pháp phần mềm độc lập, viết mã nguồn sạch (Clean Code) tuân thủ tiêu chuẩn công nghiệp.

### **2. Bối cảnh & Vấn đề**
Chuỗi cửa hàng trà sữa và cà phê Highlands POS đang nâng cấp hệ thống máy tính tiền tại quầy. Ban quản lý mong muốn triển khai một module xử lý hóa đơn tự động có khả năng tùy biến các thông số đầu vào một cách linh hoạt. Trong thực tế giao dịch, nhân viên thu ngân cần nhập thông tin sản phẩm, số lượng, các khoản phụ thu tùy chỉnh (như chọn kích thước ly, topping đi kèm), tỷ lệ chiết khấu cho khách hàng thân thiết và tỷ lệ thuế VAT quy định.

Hệ thống cần tự động tính toán chính xác tất cả các chỉ số tài chính từ tổng tiền hàng thô, số tiền được giảm giá, tiền thuế VAT, tổng tiền thanh toán cuối cùng và số tiền thừa phải trả lại cho khách hàng dựa trên lượng tiền mặt nhận từ khách.

### **3. Quy tắc nghiệp vụ**
Mô hình tính toán tài chính của đơn hàng cần tuân thủ các công thức nghiệp vụ sau:
1.  **Đơn giá sản phẩm hoàn chỉnh (Item Unit Price):**
    `Đơn giá thực tế = Giá gốc đồ uống + Phụ thu kích thước (Size) + Tổng tiền các loại Topping`
2.  **Tổng tiền hàng thô (Subtotal):**
    `Subtotal = Đơn giá thực tế * Số lượng`
3.  **Số tiền chiết khấu (Discount Amount):**
    `Discount Amount = Subtotal * \left((Tỷ lệ giảm giá \%) / (100)\right)`
4.  **Tổng tiền sau giảm giá (Net Subtotal):**
    `Net Subtotal = Subtotal - Discount Amount`
5.  **Số tiền thuế giá trị gia tăng (VAT Amount):**
    `VAT Amount = Net Subtotal * \left((Tỷ lệ thuế VAT \%) / (100)\right)`
6.  **Tổng tiền thanh toán cuối cùng (Final Total):**
    `Final Total = Net Subtotal + VAT Amount`
7.  **Tiền thừa trả khách (Change Amount):**
    `Change Amount = Tiền mặt khách đưa - Final Total`

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Phần mềm phụ trách module POS, thực hiện bài tập sáng tạo theo 4 phần nhiệm vụ sau:

*   **Phần 1: Tự thiết kế I/O Schema (Cấu trúc Đầu vào/Đầu ra)**
    *   Tự xác định và lập bảng danh sách toàn bộ các biến đầu vào thu nhập từ bàn phím (`input()`), chỉ rõ kiểu dữ liệu (`str`, `int`, `float`) và mục đích nghiệp vụ.
    *   Tự xác định và lập bảng danh sách các biến trung gian và biến đầu ra kết quả xuất ra màn hình (`print()`), kèm theo định dạng hiển thị tiền tệ (ví dụ: làm tròn số nguyên, hiển thị phân cách dòng).

*   **Phần 2: Tự phát hiện bẫy dữ liệu (Edge Cases)**
    *   Phát hiện và phân tích tối thiểu 3 kịch bản dữ liệu bất thường hoặc xung đột logic có thể xảy ra khi thu ngân nhập liệu từ CLI (ví dụ: nhập số tiền khách đưa nhỏ hơn tổng thanh toán, nhập tỷ lệ chiết khấu vượt quá 100%, nhập số lượng không hợp lệ).
    *   Đề xuất phương án định hướng xử lý/bảo vệ dữ liệu tính toán cho từng kịch bản trong phạm vi các lệnh tính toán và ép kiểu đã học.

*   **Phần 3: Vẽ sơ đồ luồng dữ liệu (Mermaid Data Flow Diagram)**
    *   Vẽ sơ đồ Mermaid biểu diễn chi tiết luồng di chuyển và biến đổi của dữ liệu từ công đoạn tiếp nhận Input -> Ép kiểu dữ liệu -> Tính toán Subtotal/Discount/VAT -> Tính Change Amount -> Xuất Hóa đơn POS hoàn chỉnh.
    *   [REQUIREMENT] Phải sử dụng đúng 5 hình dạng chuẩn Mermaid: Oval/Stadium `([Start/End])`, Parallelogram `[/Input/Output/]`, Rectangle `["Process/Calculation"]`, Arrow `-->`.

*   **Phần 4: Triển khai mã nguồn Python**
    *   Triển khai mã nguồn Python từ đầu dựa trên thiết kế cá nhân ở Phần 1, 2, 3.
    *   Sử dụng kỹ thuật f-string để xuất ra một mẫu hóa đơn thanh toán quầy POS chuyên nghiệp, minh bạch và căn chỉnh đẹp mắt trên màn hình console.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (bao gồm I/O Schema, phân tích Edge Cases, sơ đồ luồng Mermaid) và mã nguồn Python triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex14`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex14`
