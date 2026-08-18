#

# <center>[Sáng tạo 1] Thiết kế mô-đun tiếp nhận bệnh nhân và dự tính chi phí khám</center>

### **1. Mục tiêu**
*   **Mục tiêu kiến thức:** Vận dụng linh hoạt khai báo biến ES6 (`const`, `let`), quy tắc đặt tên `camelCase`, ép kiểu dữ liệu minh bạch (`Number()`), và chuỗi thông minh Template Literals trong JavaScript.
*   **Mục tiêu kỹ năng:** Tự phân tích bài toán thực tế thuộc hệ thống Đặt lịch Khám bệnh Phòng khám Tự động (CLINIC_APPOINTMENT), thiết kế cấu trúc I/O, chủ động tìm kiếm các trường hợp biên (Edge Cases), vẽ sơ đồ luồng dữ liệu (Data Flow) và xây dựng chương trình tiếp nhận bệnh nhân chạy trên môi trường Trình duyệt/Node.js.

### **2. Bối cảnh & Vấn đề**
Phòng khám đa khoa đang triển khai Kiosk tự phục vụ đặt tại sảnh chờ. Khi bệnh nhân đến đăng ký, Kiosk cần thực hiện quy trình thu thập thông tin cá nhân cơ bản, cấp số thứ tự tạm thời và dự tính tổng chi phí khám bệnh ban đầu trước khi bệnh nhân vào phòng bác sĩ. Hiện tại, nhân viên hỗ trợ tại sảnh vẫn phải thực hiện tính toán thủ công bằng máy tính cầm tay, dễ dẫn đến sai sót khi nối chuỗi dữ liệu hoặc tính sai mức giảm trừ bảo hiểm y tế (BHYT).

Hệ thống mới cần một script xử lý tương tác trực tiếp trên trình duyệt bằng các hộp thoại nhập xuất chuẩn (`prompt()`, `alert()`, `console.log()`), đảm bảo dữ liệu được ép kiểu rõ ràng, tránh cạm bẫy cộng chuỗi và hiển thị kết quả phiếu đăng ký chuyên nghiệp.

### **3. Quy tắc nghiệp vụ**
1.  **Thông tin tiếp nhận:** Thu thập tên bệnh nhân, tuổi, đơn giá khám cơ bản (VNĐ) và phụ phí khám chuyên khoa (VNĐ).
2.  **Tính toán chi phí dự kiến:**
    *   Tổng chi phí gốc = Phí khám cơ bản + Phụ phí chuyên khoa.
    *   Số tiền BHYT chi trả = Phí khám cơ bản * 0.8 (áp dụng cho bệnh nhân có BHYT).
    *   Tổng chi phí bệnh nhân cần thanh toán = Tổng chi phí gốc - Số tiền BHYT chi trả.
3.  **Quy chuẩn dữ liệu:**
    *   Sử dụng `const` cho các giá trị cố định (tỷ lệ BHYT, tên phòng khám) và các giá trị không thay đổi sau khi khởi tạo.
    *   Sử dụng `let` cho các biến tính toán có thể thay đổi hoặc nhận giá trị trong tiến trình xử lý.
    *   Bắt buộc ép kiểu dữ liệu từ chuỗi nhập vào (`prompt`) sang kiểu số (`Number`) trước khi thực hiện các phép tính số học.
    *   Xuất kết quả phiếu xác nhận dạng văn bản chuẩn mực qua Template Literals ra cửa sổ Console và hộp thoại Alert.

### **4. Yêu cầu bài toán**
Học viên đóng vai trò là Lập trình viên Web Front-End triển khai mô-đun này theo 4 phần:

*   **Phần 1: Tự thiết kế cấu trúc dữ liệu I/O (I/O Schema Definition)**
    *   Tự đề xuất bảng mô tả danh sách các biến đầu vào (Input) và đầu ra (Output) bao gồm: Tên biến (`camelCase`), Kiểu dữ liệu (`String`, `Number`, `Boolean`), Ý nghĩa nghiệp vụ.
*   **Phần 2: Chủ động phát hiện các bẫy dữ liệu (Edge Cases)**
    *   Liệt kê ít nhất 3 trường hợp biên hoặc lỗi nhập liệu có thể xảy ra khi người dùng tương tác với Kiosk (ví dụ: nhập chữ vào ô đơn giá, bấm Cancel trên prompt, nhập tuổi âm,...).
*   **Phần 3: Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram với Mermaid)**
    *   Vẽ sơ đồ quy trình xử lý dữ liệu từ lúc Kiosk hiển thị prompt cho đến khi xuất phiếu ra Console/Alert.
    *   *Lưu ý tuân thủ đúng 5 dạng hình khối Mermaid quy chuẩn:* Oval cho Bắt đầu/Kết thúc `([...])`, Hình bình hành cho Đầu vào/Đầu ra `[/.../]`, Hình thoi cho Kiểm tra `...`, Hình chữ nhật cho Xử lý/Tính toán `["..."]`.
*   **Phần 4: Viết mã nguồn triển khai thực tế**
    *   Tạo file `index.html` liên kết tới file mã nguồn JavaScript bên ngoài (`app.js`).
    *   Viết mã nguồn JavaScript đạt chuẩn ES6+, đầy đủ ghi chú giải thích bằng tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_SessionSession 02_Ex13.
    Ví dụ: HNKS25CNTT1_Core_Session_Session 02_Ex13