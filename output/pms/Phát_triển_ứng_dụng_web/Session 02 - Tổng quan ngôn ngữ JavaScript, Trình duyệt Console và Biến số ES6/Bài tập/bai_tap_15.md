#

# <center>[Sáng tạo 3] Thiết kế Mô-đun Tổng hợp Phiếu Đăng ký Khám và Tính Chi phí Phòng khám Tự động</center>

### **1. Mục tiêu**
*   **Về kiến thức & kỹ năng**: Vận dụng toàn diện kiến thức đã học trong Session 02 gồm cơ chế tách biệt tệp HTML và JavaScript giúp V8 Engine tối ưu bytecode, quy tắc quản lý biến ES6 (`let`/`const`, chuẩn `camelCase`), ép kiểu dữ liệu minh bạch (`Number()`), và đóng gói chuỗi báo cáo chuyên nghiệp bằng Chuỗi mẫu (Template Literals).
*   **Về tư duy kiến trúc**: Định hình tư duy tự thiết kế luồng dữ liệu (Data Flow) và chủ động phát hiện bẫy dữ liệu (Edge Cases) trong bài toán quản lý phòng khám thực tế mà không phụ thuộc vào mã khung (skeleton code) cho trước.

### **2. Bối cảnh & Vấn đề**
Hệ thống tiếp đón bệnh nhân tại **Phòng khám Đa khoa Rikkei Care** (`CLINIC_APPOINTMENT`) đang vận hành một ứng dụng tạo phiếu đăng ký khám bệnh tự động. Tuy nhiên, phiên bản thử nghiệm hiện tại gặp phải nhiều sự cố vận hành nghiêm trọng:
1.  Đoạn mã JavaScript xử lý tính toán tiền khám và phí dịch vụ đang bị nhúng trực tiếp vào thuộc tính sự kiện HTML (như `onclick=""`), làm vi phạm nguyên tắc tách biệt giao diện - logic, khiến V8 Engine của trình duyệt không thể lưu bộ nhớ đệm (cache) và tái sử dụng bytecode hiệu quả.
2.  Nhân viên thu nhận dữ liệu đơn giá khám và phí phụ thu dịch vụ từ người dùng nhưng không thực hiện ép kiểu số, dẫn đến hiện tượng cộng chuỗi logic sai lệch (ví dụ: tiền khám `300000` VNĐ cộng phí dịch vụ `50000` VNĐ lại tạo ra tổng chi phí `30000050000` VNĐ).
3.  Sử dụng từ khóa cũ `var` gây ô nhiễm phạm vi toàn cục (global scope) và nguy cơ ghi đè biến không kiểm soát trong quá trình tính toán.

Ban Quản trị yêu cầu bạn thiết kế và triển khai một giải pháp mã nguồn sạch, tách biệt hoàn toàn tệp `index.html` và tệp logic `app.js`, đảm bảo ứng dụng thu thập đầy đủ thông tin bệnh nhân, số bảo hiểm Y tế (BHYT), đơn giá khám, tỷ lệ miễn giảm bảo hiểm, và xuất báo cáo phiếu khám hoàn chỉnh ra Developer Console và thông báo cho bệnh nhân.

### **3. Quy tắc nghiệp vụ**
Ứng dụng quản lý phiếu đăng ký khám bệnh cần tuân thủ các quy tắc nghiệp vụ sau:
*   **Khai báo biến chuẩn ES6**: Tên bệnh nhân, mã thẻ BHYT, đơn giá khám gốc, phí dịch vụ ưu tiên là các hằng số không đổi trong tiến trình phải được khai báo bằng `const`. Các giá trị tính toán thay đổi như số tiền giảm trừ bảo hiểm, tổng chi phí thanh toán cuối cùng phải được khai báo bằng `let`. Tất cả tên biến phải tuân thủ quy tắc `camelCase`.
*   **Cơ chế giảm trừ Bảo hiểm Y tế**: Bệnh nhân có thẻ BHYT hợp lệ được miễn giảm 80% tiền khám ban đầu (không áp dụng miễn giảm cho phí dịch vụ ưu tiên/ngoài giờ).
*   **Nhập xuất & Ép kiểu minh bạch**: Dữ liệu thu thập từ người dùng thông qua hàm `prompt()` phải được chuyển đổi minh bạch từ dạng Chuỗi (`String`) sang Dạng số (`Number`) trước khi thực hiện các phép toán số học.
*   **Đóng gói Báo cáo Nghiệm thu**: Chuỗi kết quả hiển thị phiếu đăng ký và chi phí khám bệnh phải sử dụng cú pháp Template Literals (`` `${...}` ``) để trình bày đẹp mắt, rõ ràng trên Console (`console.log()`) và màn hình (`alert()`).

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Phần mềm Frontend độc lập thực hiện đầy đủ 4 phần công việc:

*   **Phần 1: Thiết kế I/O Schema (Dữ liệu đầu vào & Đầu ra)**
    *   Tự thiết kế và lập bảng mô tả danh sách các biến số đầu vào (tên bệnh nhân, tuổi, mã BHYT, tiền khám gốc, phí dịch vụ ngoài giờ) kèm kiểu dữ liệu, phạm vi biến (`const`/`let`), và cơ chế ép kiểu.
    *   Mô tả cấu trúc chuỗi kết quả đầu ra (định dạng báo cáo Phiếu Khám Bệnh).

*   **Phần 2: Phân tích Bẫy dữ liệu (Edge Cases)**
    *   Liệt kê ít nhất 3 kịch bản bẫy dữ liệu hoặc lỗi vận hành có thể xảy ra (ví dụ: nhập giá trị không phải là số gây ra giá trị `NaN`, lỗi gán lại giá trị cho biến `const`, hoặc lỗi quên ép kiểu gây nối chuỗi toán tử `+`).
    *   Đề xuất phương án phòng ngừa trong mã nguồn.

*   **Phần 3: Sơ đồ luồng dữ liệu (Mermaid Data Flow Diagram)**
    *   Vẽ sơ đồ quy trình thực thi tệp từ lúc HTML tải trang, nhúng `<script src="app.js">`, V8 Engine khởi tạo Parser & Ignition biên dịch Bytecode, nhận dữ liệu qua `prompt()`, ép kiểu `Number()`, tính toán chi phí, đến khi xuất ra `console.log()` và `alert()`.
    *   *Lưu ý*: Phải tuân thủ đúng chuẩn 5 dạng hình khối Mermaid (Terminator `([ ])`, Input/Output `[/ /]`, Decision `?`, Process `[" "]`, Flowline `-->`).

*   **Phần 4: Hiện thực hóa Mã nguồn Dự án**
    *   Tạo cấu trúc thư mục gồm: `index.html` (chuẩn Semantic HTML5, liên kết mã lệnh bên ngoài ở cuối phần body) và `app.js` (logic xử lý JavaScript thuần chuẩn ES6).
    *   Viết mã nguồn xử lý đầy đủ các bước theo nghiệp vụ đã thiết kế, đảm bảo mã nguồn sạch, có chú thích giải thích logic bằng Tiếng Việt có dấu và đặt tên biến bằng Tiếng Anh chuẩn `camelCase`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex15`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex15`