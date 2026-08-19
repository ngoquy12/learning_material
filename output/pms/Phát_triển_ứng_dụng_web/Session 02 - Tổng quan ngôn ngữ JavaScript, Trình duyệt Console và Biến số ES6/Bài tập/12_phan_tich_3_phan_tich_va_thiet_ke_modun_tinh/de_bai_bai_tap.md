# <center>[Phân tích 3] Phân tích và thiết kế mô-đun tính chi phí và tạo phiếu xác nhận khám bệnh</center>

### **1. Mục tiêu**
*   **Về kiến thức:** Củng cố hiểu biết về cơ chế thực thi JavaScript ES6, phạm vi biến (`const`, `let`), ép kiểu dữ liệu minh bạch (`Number()`), và kỹ thuật đóng gói chuỗi với Template Literals.
*   **Về kỹ năng phân tích:** Đánh giá trade-off giữa các phương án thiết kế luồng xử lý dữ liệu đầu vào từ người dùng thông qua trình duyệt Console/Prompt.
*   **Về kỹ năng thiết kế:** Vẽ lưu đồ thuật toán (Mermaid Flowchart) chuẩn hóa 5 hình khối kỹ thuật để mô hình hóa tiến trình tính toán chi phí khám bệnh.
*   **Về kỹ năng triển khai:** Viết mã nguồn HTML/JS tách biệt, chạy trên môi trường HTTP Live Server, đảm bảo tính đóng gói và an toàn dữ liệu.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ tiếp nhận bệnh nhân tự động (**CLINIC_APPOINTMENT**), Kiosk tự phục vụ tại sảnh phòng khám cho phép bệnh nhân tự nhập thông tin để đăng ký lượt khám và nhận phiếu xác nhận. Quá trình xử lý bao gồm việc nhận dữ liệu chuỗi từ giao diện (`prompt`), thực hiện ép kiểu sang số để tính tổng chi phí khám sau khi trừ tỷ lệ bảo hiểm y tế (BHYT) và cộng phí dịch vụ ưu tiên, sau đó xuất thông tin phiếu ra Developer Console.

Do dữ liệu nhận được từ hàm `prompt()` luôn ở dạng chuỗi (`String`), nếu không thực hiện ép kiểu rõ ràng hoặc quản lý biến sai phạm vi (ví dụ: dùng `var`, gán lại `const`, hoặc tính toán trực tiếp trên chuỗi chưa ép kiểu), hệ thống sẽ gặp các lỗi logic nguy hiểm như phép cộng chuỗi gây sai lệch tài chính phòng khám hoặc làm tràn phạm vi bộ nhớ toàn cục.

### **3. Quy tắc nghiệp vụ**
Hệ thống cần thu thập và xử lý các thông tin từ bệnh nhân theo các quy tắc sau:
1.  **Dữ liệu đầu vào:**
    *   Mã bệnh nhân (`patientId`): Dạng chuỗi (String), không được để rỗng.
    *   Họ và tên bệnh nhân (`patientName`): Dạng chuỗi (String), không được để rỗng.
    *   Đơn giá khám gốc (`baseExamFee`): Dạng số (VNĐ), ví dụ: 200000.
    *   Tỷ lệ miễn giảm BHYT (`insuranceDiscountRate`): Dạng số thực từ `0` đến `1` (ví dụ: bệnh nhân có BHYT được giảm 80% thì nhập `0.8`, không có BHYT nhập `0`).
    *   Phí khám ưu tiên (`priorityFee`): Dạng số (VNĐ), áp dụng cho đối tượng ưu tiên/khám nhanh (ví dụ: 50000 VNĐ), nếu không ưu tiên nhập `0`.
2.  **Công thức tính toán:**
    *   Số tiền được BHYT chi trả = `baseExamFee * insuranceDiscountRate`
    *   Chi phí khám thực tế = `baseExamFee - (baseExamFee * insuranceDiscountRate)`
    *   Tổng thanh toán (`totalPayment`) = `Chi phí khám thực tế + priorityFee`
3.  **Yêu cầu xử lý và định dạng:**
    *   Toàn bộ biến khởi tạo phải tuân thủ chuẩn ES6 (`const` cho giá trị cố định, `let` cho giá trị thay đổi). Tuyệt đối không dùng `var`.
    *   Thực hiện ép kiểu `Number()` minh bạch ngay sau khi nhận dữ liệu đầu vào.
    *   Kiểm tra nếu giá trị số sau khi ép kiểu bị lỗi (`NaN`), phải thông báo cảnh báo và dừng tiến trình.
    *   Đóng gói thông tin phiếu xác nhận dạng chuỗi đa dòng bằng **Template Literals** và xuất ra `console.log()` cũng như `alert()`.

### **4. Yêu cầu bài toán**

Học viên thực hiện bài nộp gồm 3 phần bắt buộc sau:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Tự suy nghĩ và đề xuất ít nhất **2 phương án kỹ thuật khác nhau** để tổ chức luồng biến, xử lý ép kiểu dữ liệu và đóng gói chuỗi kết quả cho bài toán trên.
*   Lập bảng so sánh Trade-off trực quan giữa các phương án dựa trên 5 tiêu chí kỹ thuật: Tốc độ xử lý (Speed), Tối ưu bộ nhớ (Memory), Khả năng bảo trì (Maintainability), Độ rõ ràng mã nguồn (Readability), Mức độ tuân thủ quy chuẩn ES6.

#### **Phần 2: Lý giải Lựa chọn & Thiết kế Lưu đồ luồng (Flowchart)**
*   Lý giải khoa học lý do lựa chọn phương án tối ưu nhất để triển khai thực tế.
*   Vẽ lưu đồ quy trình xử lý (Mermaid Flowchart) cho phương án đã chọn. Lưu ý tuân thủ nghiêm ngặt 5 hình khối chuẩn:
    *   Terminator: `([Bắt đầu])` / `([Kết thúc])`
    *   Input/Output: `[/Nhập dữ liệu.../]` / `[/Hiển thị kết quả.../]`
    *   Decision: `Kiểm tra điều kiện?`
    *   Process: `["Thực hiện tính toán / Khởi tạo biến"]`
    *   Flowline: `-->`

#### **Phần 3: Triển khai Mã nguồn & Chặn lỗi biên (Implementation)**
*   Tạo cấu trúc dự án chuẩn gồm 1 tệp `index.html` và 1 tệp `app.js` riêng biệt. Nhúng `script` ở trước thẻ đóng `</body>`.
*   Viết mã nguồn JavaScript ES6 hoàn chỉnh triển khai giải pháp tối ưu.
*   Bắt lỗi biên: Xử lý trường hợp người dùng nhập giá trị không phải số (dẫn đến `NaN`) hoặc bỏ trống thông tin quan trọng.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex12`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex12`
