# <center>[Vận dụng nâng cao 2] Tính toán Chi phí và Xuất Phiếu Đăng ký Khám bệnh Tự động</center>

### **1. Mục tiêu**
*   **Về kiến thức:** Vận dụng thành thạo việc khai báo biến chuẩn ES6 (`const`, `let`), quy tắc đặt tên `camelCase`, ép kiểu dữ liệu từ chuỗi nhập vào `prompt()` sang số `Number()` và dựng chuỗi kết quả bằng Template Literals.
*   **Về kỹ năng:** Thiết kế và triển khai quy trình nhận dữ liệu đăng ký khám bệnh từ người dùng, thực hiện tính toán tài chính phòng khám (khám ban đầu, xét nghiệm, giảm trừ BHYT) và xuất phiếu thu tiền / lấy số thứ tự ra môi trường Developer Console và Alert.
*   **Về tư duy:** Phân tích toàn diện luồng dữ liệu đầu vào - đầu ra, chủ động phòng ngừa lỗi nối chuỗi ngoài ý muốn (implicit string concatenation) và tuân thủ mô hình tách biệt mã nguồn HTML/JS chuẩn V8 Engine.

### **2. Bối cảnh & Vấn đề**
Hệ thống Đặt lịch Khám bệnh Tự động (CLINIC_APPOINTMENT) tại Phòng khám Đa khoa Quốc tế Rikkei Care cần nâng cấp module tiếp nhận bệnh nhân tại cây Kiosk tự phục vụ. Khi bệnh nhân nhập thông tin đăng ký khám ban đầu, hệ thống phải tự động tính toán tổng chi phí dịch vụ, xác định số tiền BHYT chi trả, tính tổng tiền bệnh nhân phải thanh toán thực tế và xuất ra phiếu xác nhận tiếp nhận khám bệnh.

Hiện tại, hệ thống gặp rủi ro lớn nếu lập trình viên không ép kiểu minh bạch dữ liệu thu thập từ trình duyệt (`prompt`), dẫn đến việc tính toán sai chi phí khám và phí xét nghiệm (ví dụ: `150000` + `200000` bị tính sai thành `150000200000` VNĐ do nối chuỗi), gây hậu quả nghiêm trọng về tài chính và sai lệch dữ liệu phòng khám. Bạn được giao nhiệm vụ phân tích giải pháp và viết chương trình JavaScript hoàn chỉnh để giải quyết triệt để vấn đề này.

### **3. Quy tắc nghiệp vụ**
Hệ thống Kiosk yêu cầu tuân thủ các quy tắc tài chính và vận hành sau:
1.  **Dữ liệu thu thập:** Hệ thống yêu cầu nhập lần lượt 6 thông tin từ người dùng qua cửa sổ `prompt()`:
    *   Mã bệnh nhân (`patientId`)
    *   Họ và tên bệnh nhân (`patientName`)
    *   Tuổi bệnh nhân (`patientAge`)
    *   Đơn giá khám lâm sàng gốc (`baseFee` - VNĐ)
    *   Chi phí xét nghiệm ban đầu (`labFee` - VNĐ)
    *   Tỷ lệ giảm trừ Bảo hiểm Y tế (`insuranceDiscountRate` - tính theo %, ví dụ nhập 80 tương ứng 80%, nhập 0 nếu không có BHYT).
2.  **Công thức tính toán tài chính:**
    *   Tổng chi phí dịch vụ ban đầu = `baseFee + labFee`
    *   Số tiền BHYT chi trả = `(baseFee + labFee) * (insuranceDiscountRate / 100)`
    *   Tổng tiền bệnh nhân thực trả = `(baseFee + labFee) - Số tiền BHYT chi trả`
    *   Xác định đối tượng ưu tiên cao tuổi: Biểu thức kiểm tra điều kiện `patientAge >= 70` (kết quả trả về `true` hoặc `false`).
3.  **Quy chuẩn xuất dữ liệu:**
    *   Xuất phiếu xác nhận khám bệnh hoàn chỉnh ra màn hình Developer Console (`console.log`) dưới dạng chuỗi Template Literals có định dạng chuyên nghiệp, hiển thị minh bạch từng mục tiền và cờ ưu tiên.
    *   Hiển thị thông báo ngắn gọn tới người dùng bằng `alert()` xác nhận đã đăng ký thành công và số tiền thực tế cần thanh toán.
4.  **Kiến trúc mã nguồn:** Mã JavaScript logic phải được tách độc lập vào tệp `app.js`, liên kết đúng vị trí trước thẻ đóng `</body>` của tệp `index.html` và chạy trên môi trường Web Server (Live Server HTTP protocol).

### **4. Yêu cầu bài toán**
Học viên thực hiện bài tập theo 2 phần bắt buộc:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Analysis & Design Report)**
*   **Phân tích I/O:** Liệt kê toàn bộ dữ liệu đầu vào (tên biến, kiểu dữ liệu gốc từ `prompt`, kiểu dữ liệu sau khi chuyển đổi) và dữ liệu đầu ra.
*   **Đề xuất giải pháp logic:** Trình bày giải pháp phòng ngừa lỗi nối chuỗi dữ liệu, phương án quản lý hằng số và biến số theo chuẩn ES6.
*   **Sơ đồ luồng (Flowchart) / Các bước thực hiện:** Thiết kế các bước xử lý dữ liệu chi tiết theo trình tự execution flow (sử dụng Mermaid Diagram tuân thủ đúng 5 dạng hình tiêu chuẩn).

#### **Phần 2: Triển khai Mã nguồn & Xử lý An toàn (Implementation & Coding)**
*   Xây dựng cấu trúc dự án chuẩn HTML5 (`index.html`) và tệp JavaScript độc lập (`app.js`).
*   Khai báo toàn bộ hằng số và biến số tuân thủ nghiêm ngặt quy tắc `camelCase`, phân biệt rõ ràng giữa `const` và `let`.
*   Ép kiểu dữ liệu minh bạch từ String sang Number ngay khi nhận dữ liệu, ngăn chặn triệt để hiện tượng cộng chuỗi ngoài ý muốn.
*   Sử dụng chuỗi Template Literals để tạo định dạng phiếu tiếp nhận thông tin bệnh nhân chuyên nghiệp và dễ đọc.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex8`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex8`
