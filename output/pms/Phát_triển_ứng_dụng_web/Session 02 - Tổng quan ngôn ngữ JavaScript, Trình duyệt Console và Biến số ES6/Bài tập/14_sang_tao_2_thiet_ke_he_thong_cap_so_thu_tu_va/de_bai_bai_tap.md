#

# <center>[Sáng tạo 2] Thiết kế Hệ thống Cấp Số Thứ Tự & Tính Chi Phí Khám Bệnh Tự Động</center>

### **1. Mục tiêu**
*   **Tăng cường tư duy thiết kế kiến trúc:** Tự hoạch định cấu trúc dữ liệu I/O Schema và quy chuẩn đặt tên biến số ES6 (`const`, `let`, quy tắc camelCase) cho phân hệ tiếp đón bệnh nhân tự động tại phòng khám.
*   **Tối ưu hóa V8 Engine & Môi trường thực thi:** Tách biệt triệt để HTML và JavaScript (`app.js`), tối ưu vị trí nạp thẻ `<script>` ở cuối phần `<body>` để hỗ trợ V8 Engine tối ưu hóa quá trình biên dịch Bytecode.
*   **Thành thạo nhập xuất & ép kiểu dữ liệu:** Sử dụng `prompt()`, `alert()`, `console.log()` và phương thức ép kiểu minh bạch `Number()` để xử lý các phép tính tài chính chính xác, loại bỏ hoàn toàn nguy cơ nối chuỗi sai logic.
*   **Chủ động phát hiện bẫy lập trình:** Tự xác định và phòng chống các bẫy thực tế (TDZ - Temporal Dead Zone, ô nhiễm phạm vi do `var`, lỗi ép kiểu dữ liệu chuỗi thành `NaN`, sai lệch kết quả nối chuỗi toán tử `+`) thông qua sơ đồ luồng dữ liệu Mermaid.

### **2. Bối cảnh & Vấn đề**
Hệ thống Đặt lịch Khám bệnh Phòng khám Tự động (`CLINIC_APPOINTMENT`) đang nâng cấp phân hệ Kiosk tự phục vụ (Self-service Kiosk) nhằm giảm tải áp lực cho quầy lễ tân. Trong quy trình tiếp đón, khi bệnh nhân đến phòng khám, họ sẽ nhập các thông tin cá nhân (họ tên, mã bệnh nhân, năm sinh), chọn dịch vụ khám chuyên khoa, khai báo tình trạng Bảo hiểm Y tế (BHYT) và đăng ký các dịch vụ đi kèm (như xét nghiệm nhanh, sổ khám bệnh mới).

Hệ thống thử nghiệm trước đó gặp nhiều sự cố nghiêm trọng do lập trình viên cũ khai báo biến bằng `var`, nhúng trực tiếp mã JavaScript vào thuộc tính HTML (`onclick`) làm cản trở V8 Engine tối ưu hóa Bytecode, đồng thời không ép kiểu dữ liệu nhận về từ `prompt()`. Điều này khiến phép tính tổng thanh toán bị sai lệch hoàn toàn do lỗi nối chuỗi (ví dụ: tiền khám `150000` VNĐ cộng phí dịch vụ `30000` VNĐ cho ra kết quả `"15000030000"` VNĐ).

Với vai trò là Kỹ sư Lập trình Web Front-End phụ trách phân hệ này, bạn được giao nhiệm vụ tự chủ thiết kế kịch bản dữ liệu, xây dựng luồng xử lý và phát triển mã nguồn JavaScript chuẩn ES6 hoàn chỉnh để vận hành Kiosk tính chi phí và cấp phiếu khám tự động.

### **3. Quy tắc nghiệp vụ**
*   **Quy tắc 1 (Chuẩn hóa cấu trúc mã nguồn):** Tách biệt toàn bộ mã logic vào file JavaScript độc lập (`app.js`). Liên kết file qua thẻ `<script src="app.js"></script>` đặt ngay trước thẻ đóng `</body>` của tệp `index.html` để đảm bảo DOM đã dựng xong trước khi V8 Engine thực thi mã.
*   **Quy tắc 2 (Quản lý biến chuẩn ES6):** Tuyệt đối không sử dụng từ khóa `var`. Tất cả các đại lượng không thay đổi (như phí khám cố định, tỷ lệ giảm giá BHYT cố định, tên phòng khám) phải khai báo bằng `const`. Các biến lưu trữ thông tin có thể thay đổi hoặc nhận từ người dùng phải khai báo bằng `let`. Tất cả tên biến phải tuân thủ chuẩn `camelCase` bằng tiếng Anh.
*   **Quy tắc 3 (Nhập xuất & Tính toán an toàn):** Thu thập dữ liệu từ người dùng qua `prompt()`. Phải ép kiểu minh bạch dữ liệu đầu vào dạng số bằng `Number()` trước khi thực hiện các phép tính số học.
*   **Quy tắc 4 (Đóng gói phiếu xuất kết quả):** Sử dụng chuỗi Template Literals (`` `${}` ``) để định dạng Phiếu khám bệnh & Tổng chi phí thanh toán. Xuất kết quả rõ ràng ra Developer Console (`console.log`) và hiển thị thông báo tổng hợp tới bệnh nhân qua `alert()`.

### **4. Yêu cầu bài toán**
Học viên thực hiện bài nộp bao gồm các phần bắt buộc sau:

*   **Phần 1: Thiết kế I/O Schema & Kịch bản bẫy dữ liệu (Self-Designed I/O Schema & Edge Cases)**
    *   Đề xuất bảng chi tiết danh mục các dữ liệu đầu vào (Input) và dữ liệu đầu ra (Output) cho ứng dụng cấp phiếu khám.
    *   Liệt kê ít nhất 3 bẫy dữ liệu hoặc bẫy cú pháp có thể xảy ra (ví dụ: người dùng nhập chuỗi không phải số, nhập giá trị rỗng, ô nhiễm phạm vi biến `var`, lỗi TDZ) và nêu phương án xử lý tương ứng.

*   **Phần 2: Sơ đồ luồng dữ liệu Mermaid (Data Flow Diagram)**
    *   Vẽ sơ đồ Mermaid biểu diễn luồng dữ liệu từ khi HTML nạp script, nhận thông tin từ `prompt()`, ép kiểu dữ liệu qua `Number()`, thực thi tính toán chi phí đến khi xuất Template Literals ra Console/Alert.
    *   Tuân thủ nghiêm ngặt 5 hình dạng chuẩn Mermaid: Oval `([Bắt đầu/Kết thúc])`, Parallelogram `[/Đầu vào / Đầu ra/]`, Rectangle `["Xử lý / Tính toán"]`, Diamond `Kiểm tra điều kiện?`.

*   **Phần 3: Triển khai mã nguồn (Implementation)**
    *   Tạo cấu trúc dự án chuẩn HTML5 (`index.html`) và tệp logic (`app.js`).
    *   Viết mã nguồn JS sạch, đặt tên biến tiếng Anh chuẩn `camelCase`, comment giải thích logic bằng Tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Sơ đồ Mermaid) và mã nguồn triển khai (`index.html`, `app.js`).
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex14`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex14`