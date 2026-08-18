#

# <center>[Phân tích 1] Phân tích và Thiết kế Module Tính Chi phí Khám bệnh Ban đầu</center>

### **1. Mục tiêu**
*   Phân tích cấu trúc tổ chức mã nguồn JavaScript ES6+ và cơ chế thực thi của V8 Engine trong phân hệ tiếp đón bệnh nhân thuộc hệ thống **Đặt lịch Khám bệnh Phòng khám Tự động (CLINIC_APPOINTMENT)**.
*   Đánh giá sự khác biệt và tác động của việc quản lý biến số (`const`, `let` so với `var`), vị trí nhúng script HTML, và quy trình ép kiểu dữ liệu đầu vào (`Number()`) tới hiệu năng bộ nhớ RAM và khả năng bảo trì hệ thống.
*   Thiết kế lưu đồ thuật toán và triển khai giải pháp tối ưu cho module tính toán chi phí khám bệnh ban đầu, bảo đảm dữ liệu đầu ra được đóng gói chính xác bằng chuỗi Template Literals.

### **2. Bối cảnh & Vấn đề**
Phòng khám đang tiến hành số hóa quy trình tiếp đón bệnh nhân tại Kiosk tự phục vụ. Khi bệnh nhân nhập thông tin đăng ký khám ban đầu, hệ thống cần tiếp nhận các dữ liệu: Tên bệnh nhân, Năm sinh, Giá khám niêm yết và Tỷ lệ miễn giảm của Bảo hiểm Y tế (BHYT). Từ đó, hệ thống tự động tính toán tuổi của bệnh nhân, số tiền khám thực tế phải trả sau khi giảm trừ BHYT và in phiếu xác nhận ra màn hình Developer Console cũng như hộp thoại thông báo.

Tuy nhiên, đội ngũ phát triển đang gặp khó khăn trong việc lựa chọn kiến trúc mã nguồn phù hợp:
1. Nhập liệu qua `prompt()` trả về dữ liệu kiểu chuỗi (`String`). Nếu không xử lý ép kiểu minh bạch, các phép tính số học sẽ bị biến thành phép nối chuỗi, dẫn đến sai lệch dữ liệu tài chính nghiêm trọng.
2. Việc sử dụng sai phạm vi khai báo biến (`var` thay vì `const`/`let`) làm rò riri biến ra scope toàn cục, gây nguy cơ ghi đè dữ liệu khi nhiều bệnh nhân đăng ký liên tục.
3. Đặt vị trí thẻ `<script>` không đúng chuẩn trong tệp HTML làm cản trở luồng dựng giao diện DOM của trình duyệt và ảnh hưởng đến cơ chế tối ưu Bytecode của V8 Engine (Ignition/TurboFan).

Học viên đóng vai trò Kỹ sư Phần mềm phụ trách kiến trúc Front-end, cần phân tích toàn diện vấn đề, đề xuất các giải pháp kỹ thuật, đánh giá trade-off và trực tiếp triển khai phương án tối ưu nhất.

### **3. Quy tắc nghiệp vụ**
*   **Quy tắc 1 (Tính tuổi):** Năm hiện tại của hệ thống được quy định cố định là `2026`. Tuổi bệnh nhân được tính theo công thức: `patientAge = 2026 - birthYear`.
*   **Quy tắc 2 (Miễn giảm BHYT):** Bệnh nhân có BHYT sẽ được giảm trừ chi phí theo tỷ lệ thập phân `insuranceDiscountRate` (ví dụ: `0.8` tương ứng miễn giảm 80% chi phí khám).
*   **Quy tắc 3 (Chi phí thực trả):** Số tiền khám thực tế bệnh nhân cần thanh toán được tính theo công thức: `finalFee = baseFee * (1 - insuranceDiscountRate)`.
*   **Quy tắc 4 (Chuẩn hóa đầu vào):** Tất cả dữ liệu nhận từ `prompt()` dạng chuỗi phải được chuyển đổi sang kiểu số (`Number()`) trước khi đưa vào các biểu thức tính toán toán học.
*   **Quy tắc 5 (Quản lý biến & Phạm vi):** Tuyệt đối KHÔNG sử dụng từ khóa `var`. Sử dụng `const` cho các giá trị cố định/hằng số không gán lại và `let` cho các biến số có sự thay đổi giá trị. Đặt tên biến theo chuẩn `camelCase` bằng tiếng Anh.
*   **Quy tắc 6 (Xuất kết quả):** Đóng gói thông tin phiếu khám bằng chuỗi Template Literals và hiển thị ra Developer Console (`console.log`) và Alert (`alert`) theo đúng định dạng mẫu.
*   **Quy tắc 7 (Kiến trúc tệp):** Mã lệnh JavaScript phải được viết trong tệp `app.js` riêng biệt và nhúng vào `index.html` ngay trước thẻ đóng `</body>` để tránh cản trở luồng hiển thị HTML.

### **4. Yêu cầu bài toán**
Học viên cần hoàn thành báo cáo phân tích và mã nguồn theo 3 phần sau:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Tự nghiên cứu, đề xuất ít nhất **2 phương án kỹ thuật** khác nhau để giải quyết bài toán trên (khác nhau về cách tổ chức biến, thứ tự chuyển đổi kiểu dữ liệu, và cách thức cấu trúc tệp mã nguồn).
*   Lập bảng so sánh Trade-off trực quan giữa các phương án dựa trên 5 tiêu chí:
    1. Hiệu năng thực thi (Khả năng tối ưu V8 Engine / Bytecode caching).
    2. Dung lượng bộ nhớ (Memory footprint & Scope isolation).
    3. Tính dễ đọc và bảo trì (Readability & Maintainability).
    4. Tránh bẫy lập trình (Phòng ngừa lỗi nối chuỗi ngầm và ô nhiễm biến toàn cục).
    5. Bối cảnh áp dụng phù hợp (Use-case suitability).

#### **Phần 2: Lý giải Lựa chọn & Sơ đồ luồng (Flowchart)**
*   Lý giải lập luận khoa học để chọn ra 1 phương án tối ưu nhất cho hệ thống phòng khám.
*   Vẽ sơ đồ luồng (Mermaid Flowchart) cho phương án đã chọn. Sơ đồ phải tuân thủ nghiêm ngặt chuẩn ký hiệu:
    *   Hình OVAL `([Bắt đầu / Kết thúc])` cho điểm khởi chạy và kết thúc.
    *   Hình BÌNH HÀNH `[/Đầu vào / Đầu ra/]` cho thao tác nhập `prompt()` và xuất `console.log`/`alert`.
    *   Hình CHỮ NHẬT `["Thực hiện hành động / Tính toán"]` cho các phép toán và ép kiểu.
    *   Hình THOI `{"Kiểm tra điều kiện"}` nếu có rẽ nhánh logic.

#### **Phần 3: Triển khai Mã nguồn & Kiểm chuẩn**
*   Tạo thư mục dự án gồm 2 tệp: `index.html` và `app.js`.
*   Viết mã nguồn JavaScript chuẩn ES6+, triển khai hoàn chỉnh phương án đã chọn.
*   Đảm bảo mã nguồn xử lý mượt mà dữ liệu nhập vào, tính toán chính xác chi phí khám và tuổi bệnh nhân, in ra phiếu khám theo định dạng:
    `[PHIẾU KHÁM BỆNH] Bệnh nhân: Nguyễn Văn A | Tuổi: 40 | Giá gốc: 200000 VNĐ | BHYT giảm: 80% | Chi phí thực trả: 40000 VNĐ`

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_Session02_Ex10.
    Ví dụ: HNKS25CNTT1_Core_Session02_Ex10