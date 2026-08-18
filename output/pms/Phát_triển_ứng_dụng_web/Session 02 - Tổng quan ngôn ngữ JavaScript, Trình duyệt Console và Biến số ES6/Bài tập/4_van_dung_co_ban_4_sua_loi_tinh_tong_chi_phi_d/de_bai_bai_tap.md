#

# <center>[Vận dụng cơ bản 4] Sửa lỗi tính tổng chi phí đăng ký khám bệnh tự động</center>

### **1. Mục tiêu**
*   Nắm vững cơ chế ép kiểu dữ liệu minh bạch từ chuỗi `String` sang dạng `Number` trong JavaScript (ES6+).
*   Phân biệt sự khác nhau giữa toán tử cộng số học và toán tử nối chuỗi khi làm việc với kết quả trả về từ `prompt()`.
*   Áp dụng đúng quy tắc khai báo biến `const`/`let`, quy chuẩn đặt tên `camelCase` và cú pháp Template Literals để xuất hóa đơn khám bệnh.
*   Rèn luyện kỹ năng đọc vết mã nguồn (code tracing) và xây dựng bảng báo cáo kiểm thử lỗi logic (Test Case Report).

### **2. Bối cảnh & Vấn đề**
Trong phân hệ Đặt lịch & Cấp số thứ tự khám bệnh tự động (CLINIC_APPOINTMENT), phòng khám triển khai hệ thống ki-ốt tự phục vụ cho phép bệnh nhân tự nhập thông tin và nhận phiếu đăng ký khám bệnh. Mỗi lượt đăng ký bao gồm hai khoản chi phí: giá khám ban đầu và phụ phí khám chuyên khoa.

Tuy nhiên, bộ phận kế toán của phòng khám nhận được nhiều phản ánh từ bệnh nhân rằng số tiền trên hóa đơn hiển thị ra màn hình bị sai lệch bất thường. Ví dụ: khi bệnh nhân nhập chi phí khám ban đầu là `150000` VNĐ và phụ phí khám chuyên khoa là `50000` VNĐ, hệ thống lại tính tổng chi phí thanh toán lên tới `15000050000` VNĐ.

### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn JavaScript hiện tại đang chạy trên ki-ốt đăng ký khám bệnh tự động:```javascript
// Hệ thống Đặt lịch Khám bệnh CLINIC_APPOINTMENT
// Tệp mã nguồn: appointment.js

// Bước 1: Nhập thông tin bệnh nhân và các khoản phí từ ki-ốt tự phục vụ
const patientName = prompt("Nhập tên bệnh nhân:");
const baseFeeInput = prompt("Nhập giá khám ban đầu (VNĐ):");
const specialistSurchargeInput = prompt("Nhập phụ phí khám chuyên khoa (VNĐ):");

// Bước 2: Ép kiểu dữ liệu cho phí khám ban đầu
const baseFee = Number(baseFeeInput);

// Bước 3: Gán giá trị phụ phí khám chuyên khoa
const specialistSurcharge = specialistSurchargeInput;

// Bước 4: Tính tổng chi phí khám bệnh
const totalFee = baseFee + specialistSurcharge;

// Bước 5: Tạo chuỗi thông báo kết quả hóa đơn
const invoiceMessage = `Bệnh nhân: ${patientName} | Tiền khám: ${baseFee} VNĐ | Phụ phí: ${specialistSurcharge} VNĐ | Tổng chi phí: ${totalFee} VNĐ`;

// Bước 6: Xuất kết quả ra màn hình Console và Hộp thoại Alert
console.log(invoiceMessage);
alert(invoiceMessage);
```

#

## **4. Yêu cầu đầu ra**

#### **Phần 1: Trace code và Lập bảng báo cáo Test Case (Bug Discovery)**
Học viên phân tích mã nguồn hiện tại, xác định chính xác dòng code gây lỗi và hoàn thiện bảng báo cáo Test Case theo mẫu dưới đây. Dòng STT 1 là ví dụ mẫu đã hoàn thiện, học viên hãy truy vết và điền tiếp thông tin còn thiếu vào dòng STT 2 và STT 3:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: center;">Input (Dữ liệu đầu vào)</th>
      <th style="text-align: center;">Buggy Output (Kết quả lỗi)</th>
      <th style="text-align: center;">Expected Output (Kết quả kỳ vọng)</th>
      <th style="text-align: center;">Failing Line of Code (Dòng code gây lỗi)</th>
      <th style="text-align: center;">Logic Note (Giải thích nguyên nhân)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td>patientName = "Nguyễn Văn A"<br>baseFeeInput = "150000"<br>specialistSurchargeInput = "50000"</td>
      <td>"Bệnh nhân: Nguyễn Văn A | Tiền khám: 150000 VNĐ | Phụ phí: 50000 VNĐ | Tổng chi phí: 15000050000 VNĐ"</td>
      <td>"Bệnh nhân: Nguyễn Văn A | Tiền khám: 150000 VNĐ | Phụ phí: 50000 VNĐ | Tổng chi phí: 200000 VNĐ"</td>
      <td><code>const specialistSurcharge = specialistSurchargeInput;</code> (Dòng 12)</td>
      <td>Biến <code>specialistSurchargeInput</code> lấy từ <code>prompt()</code> mang kiểu String. Do không qua <code>Number()</code> nên toán tử <code>+</code> thực hiện nối chuỗi thay vì cộng số.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td>patientName = "Trần Thị B"<br>baseFeeInput = "200000"<br>specialistSurchargeInput = "100000"</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td>patientName = "Lê Văn C"<br>baseFeeInput = "300000"<br>specialistSurchargeInput = "0"</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa đổi và Tối ưu mã nguồn**
*   Tạo tệp mã nguồn mới `appointment_fixed.js` để tiến hành sửa lỗi.
*   Thực hiện ép kiểu dữ liệu minh bạch cho tất cả các đầu vào dạng số nhận từ `prompt()`.
*   Đảm bảo phép tính tổng chi phí trả về kết quả số học chính xác.
*   Sử dụng đúng cú pháp Template Literals để hiển thị hóa đơn đạt chuẩn nghiệp vụ trên cả Developer Console và hộp thoại Alert.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex4`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex4`