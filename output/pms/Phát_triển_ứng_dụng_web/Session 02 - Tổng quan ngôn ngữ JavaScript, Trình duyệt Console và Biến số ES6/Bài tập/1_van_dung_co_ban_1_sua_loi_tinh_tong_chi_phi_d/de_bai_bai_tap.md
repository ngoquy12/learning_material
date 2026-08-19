# <center>[Vận dụng cơ bản 1] Sửa lỗi tính tổng chi phí đăng ký khám bệnh ban đầu</center>

### **1. Mục tiêu**
*   Vận dụng kiến thức về khai báo biến số ES6 (`let`, `const`), quy tắc đặt tên camelCase và ép kiểu dữ liệu từ chuỗi sang số (`Number()`).
*   Sử dụng chuỗi Template Literals để xuất thông tin phiếu khám và tổng chi phí lên Console/Alert theo chuẩn doanh nghiệp.
*   Phân tích, phát hiện và sửa lỗi phép toán cộng chuỗi ngoài ý muốn (string concatenation bug) trong phân hệ tiếp nhận bệnh nhân.

### **2. Bối cảnh & Vấn đề**
Hệ thống Đặt lịch Khám bệnh Phòng khám Tự động (`CLINIC_APPOINTMENT`) đang triển khai tính năng cấp phiếu đăng ký khám bệnh ban đầu cho bệnh nhân trên nền tảng Web. Khi bệnh nhân đăng ký trực tuyến, ứng dụng sẽ thu nhận thông tin gồm Tên bệnh nhân, Phí khám cơ bản và Phí dịch vụ chuyên khoa (ví dụ: Tim mạch, Nhi khoa, Tai Mũi Họng). Sau đó, ứng dụng tự động tổng hợp thông tin và xuất tổng tiền thanh toán để hiển thị cho bộ phận thu ngân.

Tuy nhiên, bộ phận lễ tân phản ánh rằng phiếu xác nhận đặt lịch xuất ra tổng số tiền thanh toán bị sai lệch hoàn toàn so với giá niêm yết. Cụ thể: Bệnh nhân đăng ký mức phí khám cơ bản là `150000` VNĐ và phí chuyên khoa là `50000` VNĐ, nhưng phiếu tính tiền lại hiển thị tổng thanh toán là `15000050000` VNĐ. Sự cố này gây phiền hà cho người bệnh và làm gián đoạn quy trình đối soát tự động của phòng khám.

### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn của phân hệ tiếp nhận bệnh nhân đang gặp lỗi thực thi:

*   **Tệp HTML (`index.html`):**

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hệ thống Đặt lịch Khám bệnh CLINIC_APPOINTMENT</title>
</head>
<body>
    <main>
        <section>
            <h1>Phòng khám Đa khoa Quốc tế - Đăng ký Khám bệnh</h1>
            <p id="system-status">Đang khởi tạo hệ thống cấp số...</p>
        </section>
    </main>

    <!-- Liên kết mã lệnh JavaScript bên ngoài ở cuối phần body -->
    <script src="app.js"></script>
</body>
</html>
```

*   **Tệp JavaScript (`app.js`):**

```javascript
// Khởi tạo thông tin đăng ký khám bệnh từ người dùng
const patientName = prompt("Nhập tên bệnh nhân:");
const baseFeeInput = prompt("Nhập phí khám cơ bản (VNĐ):");
const specialistFeeInput = prompt("Nhập phí dịch vụ chuyên khoa (VNĐ):");

// Tính toán tổng chi phí khám bệnh
const totalPayment = baseFeeInput + specialistFeeInput;

// Tạo chuỗi thông tin phiếu hẹn
const appointmentSummary = "Bệnh nhân: " + patientName + " | Phí khám cơ bản: " + baseFeeInput + " VNĐ | Phí chuyên khoa: " + specialistFeeInput + " VNĐ | Tổng thanh toán: " + totalPayment + " VNĐ";

// Xuất thông báo lên màn hình console và alert
console.log(appointmentSummary);
alert(appointmentSummary);
```

# **4. Yêu cầu đầu ra**

#### **Phần 1: Trace mã nguồn & Báo cáo kiểm thử lỗi logic (Test Case Report)**
Học viên tiến hành trace mã nguồn hiện tại, xác định dòng lệnh gây lỗi và hoàn thiện bảng báo cáo kiểm thử 3 kịch bản dưới đây (dòng STT 1 đã được làm mẫu, học viên điền tiếp thông tin cho STT 2 và STT 3):

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr>
      <th style="border: 1px solid #dddddd; padding: 8px;">STT</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Input (Tên, Phí cơ bản, Phí chuyên khoa)</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Output thực tế (Buggy Output)</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Output mong đợi (Expected Output)</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Dòng code gây lỗi</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Giải thích nguyên nhân</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">1</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Tên: "Nguyễn Văn A"<br>Phí cơ bản: "150000"<br>Phí chuyên khoa: "50000"</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Bệnh nhân: Nguyễn Văn A | Phí khám cơ bản: 150000 VNĐ | Phí chuyên khoa: 50000 VNĐ | Tổng thanh toán: 15000050000 VNĐ</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Bệnh nhân: Nguyễn Văn A | Phí khám cơ bản: 150000 VNĐ | Phí chuyên khoa: 50000 VNĐ | Tổng thanh toán: 200000 VNĐ</td>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">Dòng 7 (app.js)</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Hàm prompt() trả về dữ liệu kiểu String. Toán tử + thực hiện phép nối chuỗi chứ không phải cộng số.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">2</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Tên: "Trần Thị B"<br>Phí cơ bản: "200000"<br>Phí chuyên khoa: "100000"</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">3</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Tên: "Lê Văn C"<br>Phí cơ bản: "180000"<br>Phí chuyên khoa: "0"</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa đổi mã nguồn (Source Code Correction)**
Sửa đổi toàn bộ mã nguồn trong tệp `app.js` để giải quyết triệt để lỗi nghiệp vụ:
*   [REQUIREMENT 1] Ép kiểu minh bạch dữ liệu đầu vào từ `prompt()` từ `String` sang `Number` bằng hàm `Number()`.
*   [REQUIREMENT 2] Đảm bảo biến số tuân thủ quy tắc khai báo ES6 (`const` cho hằng số/biến không gán lại, `let` cho biến thay đổi) và cách đặt tên theo chuẩn camelCase.
*   [REQUIREMENT 3] Thay thế toàn bộ việc nối chuỗi bằng toán tử `+` thủ công sang định dạng chuỗi Template Literals (cú pháp dấu backtick `` `... ${...}` ``).
*   [REQUIREMENT 4] Xuất kết quả đã sửa chính xác ra trình duyệt Console (`console.log`) và cửa sổ thông báo (`alert`).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo bảng Test Case và mã nguồn triển khai đã được sửa hoàn chỉnh.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex1`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex1`
