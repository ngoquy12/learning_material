#

# <center>[Vận dụng nâng cao 1] Tính Toán Chi Phí Khám Bệnh Và Xác Nhận Đặt Lịch Phòng Khám</center>

### **1. Mục tiêu**
*   Vận dụng thành thạo kiến thức về khai báo biến ES6 (`const`, `let`), nguyên tắc đặt tên biến chuẩn doanh nghiệp (`camelCase`).
*   Thực hành thu thập dữ liệu đầu vào từ người dùng qua `prompt()`, ép kiểu dữ liệu minh bạch (`Number()`) và xử lý chính xác phép tính toán số học trên dữ liệu tài chính.
*   Sử dụng chuỗi mẫu Template Literals (`` `${...}` ``) để định dạng và xuất báo cáo xác nhận đa dòng ra Developer Console (`console.log()`) và cửa sổ thông báo trình duyệt (`alert()`).
*   Rèn luyện tư duy phân tích nghiệp vụ thực tế, tự thiết kế báo cáo phân tích I/O và mô hình hóa tiến trình xử lý bằng sơ đồ luồng dữ liệu chuẩn Mermaid trước khi viết mã nguồn.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ tiếp nhận bệnh nhân tự động của Hệ thống Đặt lịch Khám bệnh (CLINIC_APPOINTMENT), khi bệnh nhân thực hiện đăng ký khám trực tuyến hoặc tại kiosk tự phục vụ, hệ thống cần thu thập thông tin cá nhân, tính toán chi phí khám bệnh dự kiến dựa trên quyền lợi Bảo hiểm Y tế (BHYT), tính phí tạo hồ sơ điện tử và phân loại đối tượng ưu tiên.

Hiện tại, việc tính toán hóa đơn tạm tính và xuất thông báo xác nhận vẫn làm thủ công, dẫn đến tình trạng sai sót khi áp dụng tỷ lệ giảm giá BHYT, nhầm lẫn phí dịch vụ cố định và làm chậm quá trình lấy số thứ tự. Bạn được giao nhiệm vụ thiết kế bài báo cáo phân tích giải pháp và xây dựng module xử lý logic bằng JavaScript ES6 chạy trực tiếp trên trình duyệt web.

### **3. Quy tắc nghiệp vụ**
*   **[RULE-01] Thu thập dữ liệu đầu vào**:
    *   Họ và tên bệnh nhân (`patientName`): Chuỗi văn bản đại diện cho tên đầy đủ.
    *   Tuổi bệnh nhân (`patientAge`): Số nguyên đại diện cho tuổi của bệnh nhân.
    *   Đơn giá khám chuyên khoa gốc (`baseExamFee`): Chi phí khám ban đầu niêm yết tại phòng khám (VNĐ).
    *   Mức hưởng BHYT (`insuranceDiscountRate`): Nhập giá trị số thực `0.8` (nếu bệnh nhân có BHYT - được giảm 80% tiền khám ban đầu) hoặc `0` (nếu không có BHYT - trả 100% tiền khám).
    *   Phí tạo hồ sơ dịch vụ cố định (`serviceFee`): Chi phí cố định `30000` VNĐ áp dụng cho tất cả lượt đăng ký.
*   **[RULE-02] Công thức tính toán tài chính**:
    *   Số tiền được BHYT chi trả: `insuranceCoverageAmount = baseExamFee * insuranceDiscountRate`
    *   Tiền khám thực tế bệnh nhân phải trả: `actualExamFee = baseExamFee - insuranceCoverageAmount`
    *   Tổng chi phí thanh toán cuối cùng: `totalPayment = actualExamFee + serviceFee`
*   **[RULE-03] Đánh dấu nhóm ưu tiên**:
    *   Nếu bệnh nhân có tuổi từ `70` trở lên, bệnh nhân được xếp vào nhóm "Ưu tiên cao tuổi". Trược lại xếp vào nhóm "Tiêu chuẩn".
*   **[RULE-04] Đóng gói và xuất kết quả**:
    *   Phiếu xác nhận đặt lịch phải bao gồm đầy đủ: Mã phân loại, Họ tên, Tuổi, Nhóm đối tượng, Chi phí gốc, Tiền BHYT chi trả, Phí hồ sơ dịch vụ và Tổng tiền thực thanh toán.
    *   Thông báo xác nhận phải được hiển thị trên Developer Console và qua hộp thoại `alert()`.

### **4. Yêu cầu bài toán**
Bài làm của học viên phải trình bày đầy đủ 2 phần chi tiết:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Báo cáo văn bản/Markdown)**
*   1.1. **Phân tích I/O**: Xác định chi tiết danh sách tất cả các biến đầu vào (Input), biến đầu ra (Output), hằng số nghiệp vụ, kèm theo kiểu dữ liệu tương ứng trong JavaScript.
*   1.2. **Tự đề xuất giải pháp**: Trình bày phương án thu nhận dữ liệu từ `prompt()`, cơ chế ép kiểu số an toàn với `Number()` và phương pháp tính toán logic tài chính.
*   1.3. **Sơ đồ luồng xử lý (Mermaid Flowchart)**: Vẽ sơ đồ tiến trình từ lúc bắt đầu nhập liệu cho đến khi xuất hóa đơn. Sơ đồ bắt buộc tuân thủ 5 dạng hình chuẩn:
    *   Terminator (Bắt đầu/Kết thúc): Hình viên thuốc `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`.
    *   Input/Output (Nhập/Xuất): Hình bình hành `[/Nhập thông tin bệnh nhân/]` / `[/Hiển thị phiếu xác nhận/]`.
    *   Decision (Kiểm tra điều kiện): Hình thoi `Kiểm tra tuổi >= 70?`.
    *   Process (Thực hiện tính toán): Hình chữ nhật `["Tính tiền BHYT chi trả và tổng thanh toán"]`.
    *   Flowline (Luồng thực thi): Mũi tên `-->` có nhãn `-->|Có|` hoặc `-->|Không|`.

#### **Phần 2: Triển khai Mã nguồn JavaScript ES6 (Tệp `index.html` và `app.js`)**
*   Tạo cấu trúc trang HTML5 chuẩn trong tệp `index.html`, liên kết với mã nguồn JavaScript bên ngoài `app.js` bằng thẻ `<script src="app.js"></script>` đặt ngay trước thẻ đóng `</body>`.
*   Viết mã nguồn xử lý trong `app.js`:
    *   Khai báo biến bằng `const` và `let`, sử dụng chuẩn tên `camelCase` bằng tiếng Anh rõ nghĩa.
    *   Thực hiện nhập liệu từ người dùng qua `prompt()`, ép kiểu dữ liệu từ chuỗi sang số bằng `Number()`.
    *   Tính toán tài chính theo đúng công thức nghiệp vụ đã quy định.
    *   Xây dựng chuỗi thông điệp phiếu xác nhận dạng đa dòng bằng Template Literals (`` `${...}` ``).
    *   Xuất thông điệp xác nhận ra Developer Console (`console.log()`) và hiển thị thông báo trình duyệt (`alert()`).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex7`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex7`