#

# <center>[Phân tích & Sửa lỗi] Sửa lỗi tính tổng chi phí đăng ký khám bệnh ban đầu</center>

### **1. Mục tiêu**
*   Phát hiện và khắc phục lỗi logic tính toán phát sinh từ việc xử lý sai kiểu dữ liệu nhận được qua hàm `prompt()`.
*   Áp dụng chuẩn khai báo biến ES6 (`const`, `let`), thực thi quy tắc đặt tên `camelCase` và tái cấu trúc thông tin đầu ra bằng chuỗi **Template Literals**.
*   Củng cố quy trình kiểm thử và truy vết mã nguồn (Code Tracing) bằng bảng báo cáo Test Case thực tế.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ Tiếp nhận Bệnh nhân thuộc **Hệ thống Đặt lịch Khám bệnh Phòng khám Tự động (CLINIC_APPOINTMENT)**, bộ phận quầy tiếp đón sử dụng một đoạn mã JavaScript để nhập thông tin và tính tổng chi phí đăng ký khám ban đầu cho bệnh nhân. Chi phí lượt khám ban đầu bao gồm hai khoản tiền chính: Phí khám lâm sàng ban đầu và Phí cấp sổ khám bệnh.

Nhân viên thu ngân phản ánh rằng: Khi nhập phí khám ban đầu là `150000` VNĐ và phí sổ khám là `20000` VNĐ, hệ thống xuất kết quả tính tổng tiền thanh toán hiển thị trên màn hình Console bị sai hoàn toàn so với thực tế (ra số tiền bất thường `15000020000` VNĐ). Sự cố này gây sai lệch báo cáo tài chính và làm gián đoạn quy trình cấp số thứ tự khám cho bệnh nhân.

### **3. Mã nguồn hiện tại**
Dưới đây là cấu trúc tệp HTML và đoạn mã JavaScript xử lý logic tính tiền hiện tại của hệ thống phòng khám:```html
<!-- File: index.html -->
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tiếp nhận Bệnh nhân - CLINIC_APPOINTMENT</title>
</head>
<body>
    <h1 id="clinic-title">Hệ thống Tiếp nhận & Đặt lịch Khám bệnh</h1>

    <!-- Nhúng mã JavaScript xử lý ở cuối phần body -->
    <script src="app.js"></script>
</body>
</html>
``````javascript
// File: app.js
// Kịch bản tính tổng tiền đăng ký khám bệnh tại quầy tiếp đón

var patient_name = prompt("Nhập tên bệnh nhân:");
var consultation_fee = prompt("Nhập phí khám lâm sàng (VNĐ):");
var card_fee = prompt("Nhập phí cấp sổ khám bệnh (VNĐ):");

// Tính tổng chi phí đăng ký khám ban đầu
var total_payment = consultation_fee + card_fee;

// Xuất kết quả ra Developer Console
console.log("Bệnh nhân: " + patient_name + " - Tổng tiền thanh toán: " + total_payment + " VNĐ");
```

#

## **4. Yêu cầu đầu ra**

#### **Phần 1: Báo cáo Truy vết mã nguồn & Phát hiện lỗi (Code Tracing Report)**
Học viên tiến hành chạy thử chương trình, phân tích luồng dữ liệu và hoàn thiện bảng Báo cáo Test Case sau đây vào tệp báo cáo:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: center;">STT</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Đầu ra thực tế bị lỗi (Buggy Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Đầu ra kỳ vọng (Expected Output)</th>
      <th style="border: 1px solid #dddddd; text-align: center;">Dòng code gây lỗi</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">1</td>
      <td style="border: 1px solid #dddddd;">patient_name = "Nguyễn Văn A"<br>consultation_fee = "150000"<br>card_fee = "20000"</td>
      <td style="border: 1px solid #dddddd;">"Bệnh nhân: Nguyễn Văn A - Tổng tiền thanh toán: 15000020000 VNĐ"</td>
      <td style="border: 1px solid #dddddd;">"Bệnh nhân: Nguyễn Văn A - Tổng tiền thanh toán: 170000 VNĐ"</td>
      <td style="border: 1px solid #dddddd; text-align: center;">Dòng 9</td>
      <td style="border: 1px solid #dddddd;">Hàm prompt() trả về dữ liệu kiểu String, toán tử + thực hiện phép nối chuỗi thay vì cộng số học.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">2</td>
      <td style="border: 1px solid #dddddd;">patient_name = "Trần Thị B"<br>consultation_fee = "200000"<br>card_fee = "15000"</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd; text-align: center;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">3</td>
      <td style="border: 1px solid #dddddd;">patient_name = "Lê Văn C"<br>consultation_fee = "100000"<br>card_fee = "0"</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd; text-align: center;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi và Chuẩn hóa Mã nguồn ES6**
Tái cấu trúc lại mã nguồn trong tệp `app.js` đạt các tiêu chuẩn kỹ thuật sau:
1.  **Quản lý biến số chuẩn ES6**: Loại bỏ hoàn toàn từ khóa `var`. Sử dụng `const` cho các giá trị hằng số không gán lại và `let` cho các biến có thể thay đổi.
2.  **Quy tắc đặt tên (Naming Convention)**: Chuyển toàn bộ tên biến từ dạng `snake_case` (`patient_name`, `consultation_fee`) sang chuẩn `camelCase` (`patientName`, `consultationFee`).
3.  **Ép kiểu dữ liệu minh bạch**: Sử dụng hàm `Number()` để chuyển đổi dữ liệu đầu vào từ dạng chuỗi ký tự sang kiểu dữ liệu số trước khi thực hiện tính toán số học.
4.  **Định dạng chuỗi kết quả bằng Template Literals**: Thay thế thao tác nối chuỗi bằng toán tử `+` bằng chuỗi nội suy Template Literals (sử dụng cặp dấu backticks `` `${...}` ``) để xuất thông báo ra `console.log()` và `alert()`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex2`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex2`