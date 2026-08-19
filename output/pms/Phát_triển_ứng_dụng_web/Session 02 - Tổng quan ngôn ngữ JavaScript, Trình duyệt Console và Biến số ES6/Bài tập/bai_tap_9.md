# <center>[Vận dụng nâng cao 3] Tính toán Chi phí và Xuất Phiếu Khám Bệnh Tự động</center>

### **1. Mục tiêu**
*   **Kiến thức:** Củng cố tư duy xử lý chuỗi nhập vào từ giao diện dòng lệnh/trình duyệt (`prompt`), ép kiểu dữ liệu minh bạch (`Number`), và quản lý hằng số/biến số theo chuẩn ES6 (`const`, `let`).
*   **Kỹ năng:** Đóng gói thông tin báo cáo phức tạp bằng chuỗi Template Literals (`` `...` ``), áp dụng quy chuẩn đặt tên `camelCase`, và tách biệt hoàn toàn mã JavaScript logic ra khỏi giao diện HTML.
*   **Mức độ chủ động:** Tự phân tích bài toán, xây dựng báo cáo phân tích I/O, vẽ sơ đồ luồng dữ liệu nghiệp vụ và lập trình hoàn chỉnh không dựa vào mã mẫu.

### **2. Bối cảnh & Vấn đề**
Phòng khám Đa khoa Rikkei Care đang nâng cấp phân hệ tiếp nhận bệnh nhân tự động tại Kiosk tra cứu. Khi bệnh nhân đến phòng khám, hệ thống sẽ tiếp nhận thông tin đầu vào, tự động tính toán tổng chi phí dịch vụ dựa trên chính sách miễn giảm Bảo hiểm Y tế (BHYT), phân loại thẻ ưu tiên theo độ tuổi và tạo phiếu xác nhận lịch khám hợp lệ.

Do dữ liệu nhận từ người dùng qua trình duyệt luôn ở dạng chuỗi (`String`), nếu không thực hiện kiểm chuẩn và ép kiểu chính xác, các phép tính tài chính sẽ bị sai lệch nghiêm trọng (ví dụ: lỗi nối chuỗi thay vì cộng số). Học viên cần thiết kế mô-đun xử lý dữ liệu đầu vào và xuất phiếu báo cáo chuẩn hóa cho phân hệ này.

### **3. Quy tắc nghiệp vụ**
Hệ thống xử lý thông tin đăng ký khám theo các quy tắc tài chính và ưu tiên như sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">Tên tham số</th>
      <th style="padding: 8px; text-align: left;">Mô tả nghiệp vụ</th>
      <th style="padding: 8px; text-align: left;">Quy tắc tính toán / Điều kiện</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><code>patientName</code></td>
      <td style="padding: 8px;">Họ và tên bệnh nhân</td>
      <td style="padding: 8px;">Dữ liệu chuỗi ký tự nhập vào từ người dùng.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>birthYear</code></td>
      <td style="padding: 8px;">Năm sinh của bệnh nhân</td>
      <td style="padding: 8px;">Ép kiểu về Number. Tuổi = 2026 - birthYear.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>baseFee</code></td>
      <td style="padding: 8px;">Giá khám niêm yết (VNĐ)</td>
      <td style="padding: 8px;">Ép kiểu về Number. Chi phí niêm yết ban đầu.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>hasInsurance</code></td>
      <td style="padding: 8px;">Trạng thái BHYT</td>
      <td style="padding: 8px;">Nhập 1 (Có BHYT) hoặc 0 (Không BHYT). Nếu có BHYT, được giảm 80% giá khám gốc (<code>baseFee * 0.8</code>).</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>serviceFee</code></td>
      <td style="padding: 8px;">Phụ phí dịch vụ khám nhanh</td>
      <td style="padding: 8px;">Ép kiểu về Number. Phụ phí cố định không áp dụng giảm trừ BHYT.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>totalPayment</code></td>
      <td style="padding: 8px;">Tổng tiền thanh toán cuối cùng</td>
      <td style="padding: 8px;">Tổng tiền = (Giá khám gốc - Số tiền giảm BHYT) + Phụ phí dịch vụ.</td>
    </tr>
    <tr>
      <td style="padding: 8px;"><code>isPriority</code></td>
      <td style="padding: 8px;">Cấp thẻ ưu tiên số thứ tự</td>
      <td style="padding: 8px;">Người cao tuổi (Tuổi &gt;= 70) được gắn trạng thái "ƯU TIÊN LẤY SỐ TỰ ĐỘNG".</td>
    </tr>
  </tbody>
</table>

[REQUIREMENT] Mọi hằng số hệ thống (Năm hiện tại = 2026, Tỷ lệ giảm BHYT = 0.8, Ngưỡng tuổi ưu tiên = 70) phải được khai báo bằng từ khóa `const` với tên viết theo chuẩn `camelCase`.

### **4. Yêu cầu bài toán**

Sinh viên thực hiện bài tập theo 2 phần bắt buộc:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Báo cáo văn bản)**
1.  **Phân tích Đầu vào / Đầu ra (I/O Analysis):** Liệt kê chi tiết danh sách tất cả các biến, hằng số sẽ sử dụng, kiểu dữ liệu tương ứng (String, Number, Boolean) và ý nghĩa nghiệp vụ.
2.  **Sơ đồ luồng xử lý dữ liệu (Mermaid Flowchart):** Vẽ sơ đồ biểu diễn các bước thực thi theo đúng quy tắc 5 hình dạng chuẩn:
    *   Terminator `([Bắt đầu/Kết thúc])`
    *   Input/Output `[/Nhập/Xuất dữ liệu/]`
    *   Process `["Thực hiện tính toán/Ép kiểu"]`
    *   Decision `{Kiểm tra điều kiện}`
    *   Flowline `-->`

#### **Phần 2: Triển khai Mã nguồn JavaScript ES6 (Coding)**
1.  **Cấu trúc tệp dán nhãn:** Tạo cấu trúc dự án chuẩn gồm `index.html` và `app.js`. Nhúng `app.js` ở cuối thẻ `<body>` của `index.html`.
2.  **Nhập dữ liệu & Ép kiểu:** Sử dụng `prompt()` để nhận các thông tin đầu vào. Áp dụng ngay `Number()` để chuyển đổi các trường dữ liệu số.
3.  **Xử lý Logic & Tính toán:** Tính tuổi, số tiền được BHYT hỗ trợ, tổng tiền phải thanh toán và xác định đối tượng ưu tiên.
4.  **Xuất kết quả báo cáo:** Sử dụng chuỗi ES6 Template Literals để tạo thông điệp phiếu xác nhận khám bệnh hoàn chỉnh và in ra màn hình thông qua `console.log()` và `alert()`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex9`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex9`
