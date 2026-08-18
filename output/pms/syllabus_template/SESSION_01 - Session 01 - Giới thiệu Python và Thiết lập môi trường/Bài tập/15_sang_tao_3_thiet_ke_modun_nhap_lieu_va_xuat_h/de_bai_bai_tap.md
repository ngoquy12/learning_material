## <center>[Sáng tạo 3] Thiết kế mô-đun nhập liệu và xuất hóa đơn POS linh hoạt cho chuỗi Highlands POS</center>

### **1. Mục tiêu**
*   **Vận dụng tổng hợp kiến thức nhập xuất:** Thực hành khai báo biến, chuyển đổi kiểu dữ liệu (`str`, `int`, `float`), tính toán biểu thức đại số và trình bày dữ liệu dạng bảng/biên lai trên giao diện dòng lệnh (CLI).
*   **Tự chủ thiết kế I/O Schema:** Tự xây dựng cấu trúc tham số đầu vào và kết quả đầu ra phù hợp với yêu cầu mở rộng tính năng của hệ thống bán hàng quầy POS Highlands Coffee.
*   **Phân tích kịch bản dữ liệu biên (Edge Cases):** Tự phát hiện các điểm nghẽn, lỗi sai lệch kiểu dữ liệu hoặc giá trị âm/bất hợp lý trong quá trình nhập liệu hóa đơn.
*   **Mô hình hóa bằng Mermaid:** Thiết kế sơ đồ luồng dữ liệu (Data Flow Diagram) chuẩn hóa quy trình xử lý hóa đơn bán hàng trước khi viết mã nguồn.

### **2. Bối cảnh & Vấn đề**
Chuỗi cửa hàng cà phê **Highlands POS** đang chuẩn bị thử nghiệm mô-đun tính tiền tự động thế hệ mới chạy trên thiết bị quầy (POS terminal). Mô-đun này nhận thông tin order trực tiếp từ nhân viên thu ngân thông qua giao diện dòng lệnh, tự động tính toán tổng số tiền dựa trên món chính, phụ thu nâng size, số lượng topping đi kèm và mức chiết khấu dành cho thành viên, sau đó xuất ra biên lai thanh toán chuẩn hóa.

Hiện tại, ban quản lý muốn tạo một bản prototype bằng ngôn ngữ Python nhằm xác minh tính chính xác của thuật toán tính tiền và định dạng xuất hóa đơn trước khi tích hợp vào phần cứng bán hàng.### **3. Quy tắc nghiệp vụ**
Hệ thống tính toán giá hóa đơn theo các quy định thực tế sau:
*   **Giá cơ sở (Base Price):** Tính theo kích thước mặc định chuẩn (Size S).
*   **Phụ thu kích thước (Size Surcharge):**
    *   Size S: +0 VNĐ
    *   Size M: +6,000 VNĐ
    *   Size L: +10,000 VNĐ
*   **Phụ thu Topping:** Mỗi loại topping gọi thêm tính đồng giá **8,000 VNĐ/topping**.
*   **Công thức tính toán:**
    *   `Đơn giá 1 ly = Giá cơ sở + Phụ thu size + (Số lượng topping * 8,000)`
    *   `Tổng tiền hàng = Đơn giá 1 ly * Số lượng ly`
    *   `Số tiền giảm giá = Tổng tiền hàng * (Mức giảm giá % / 100)`
    *   `Thành tiền thanh toán = Tổng tiền hàng - Số tiền giảm giá`

[NOTE] Học viên chỉ sử dụng các kiến thức đã học trong bài: khai báo biến, nhập liệu `input()`, xuất dữ liệu `print()`, phép toán cơ bản và chuyển đổi kiểu dữ liệu (`int()`, `float()`, `str()`).

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Phần mềm phụ trách mô-đun POS và tự chủ thực hiện 4 phần nhiệm vụ sau:

*   **Phần 1 - Tự thiết kế I/O Schema:**
    *   Xác định và đề xuất danh sách tất cả các biến đầu vào cần thu thập từ thu ngân (ví dụ: tên thu ngân, tên món, giá cơ sở, phụ thu size lựa chọn, số lượng topping, số lượng mua, tỷ lệ giảm giá...).
    *   Mô tả rõ kiểu dữ liệu (`str`, `int`, `float`) tương ứng với từng biến.

*   **Phần 2 - Tự phát hiện các bẫy dữ liệu (Edge Cases):**
    *   Liệt kê ít nhất **3 trường hợp dữ liệu biên hoặc dữ liệu không hợp lệ** có thể xảy ra khi thu ngân thao tác (ví dụ: nhập số lượng ly âm, nhập tỷ lệ giảm giá lớn hơn 100%, nhập chuỗi ký tự vào trường giá tiền...).

*   **Phần 3 - Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram):**
    *   Vẽ sơ đồ Mermaid biểu diễn toàn bộ vòng đời xử lý từ lúc nhận dữ liệu nhập CLI -> Ép kiểu & Tính toán -> Tạo định dạng biên lai -> In hóa đơn ra màn hình.
    *   **Quy định bắt buộc về hình khối Mermaid:**
        1. Start / End: Hình bo tròn `([Bắt đầu])` / `([Kết thúc])`.
        2. Input / Output: Hình bình hành `[/Nhập dữ liệu.../]` / `[/Xuất hóa đơn.../]`.
        3. Decision: Hình thoi `Kiểm tra điều kiện?`.
        4. Process: Hình chữ nhật `["Tính toán tổng tiền"]`.
        5. Arrow: `-->`.

*   **Phần 4 - Hiện thực hóa mã nguồn Python:**
    *   Viết chương trình Python hoàn chỉnh từ đầu dựa trên thiết kế cá nhân.
    *   Đảm bảo biên lai in ra màn hình console được căn chỉnh đẹp mắt, trực quan bằng các ký tự trang trí (ví dụ: `=`, `-`, `*`), trình bày đầy đủ thông tin hóa đơn Highlands POS.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Sơ đồ Mermaid) và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex15`.
    Ví dụ: `HNKS25CNTT1_Core_Session_SESSION_01_Ex15`