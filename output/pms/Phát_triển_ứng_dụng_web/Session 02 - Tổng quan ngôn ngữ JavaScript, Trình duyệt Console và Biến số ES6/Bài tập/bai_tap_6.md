# <center>[Vận dụng cơ bản 6] Sửa lỗi tính tổng chi phí đăng ký khám bệnh</center>

### **1. Mục tiêu**
*   **Kiến thức:** Củng cố tư duy xử lý kiểu dữ liệu trong JavaScript ES6, phân biệt sự khác nhau giữa nối chuỗi và cộng số học khi nhận dữ liệu từ người dùng.
*   **Kỹ năng:** Thực hành kỹ năng Code Tracing (truy vết mã nguồn), xác định dòng code gây lỗi logic, lập bảng Báo cáo Test Case và tái cấu trúc mã nguồn theo chuẩn ES6 (`const`/`let`, `Number()`, Template Literals).
*   **Thái độ:** Rèn luyện tính cẩn trọng khi làm việc với các hệ thống quản lý tài chính và hóa đơn y tế.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống Quản lý Đặt lịch Khám bệnh Phòng khám Tự động (**CLINIC_APPOINTMENT**), nhân viên lễ tân sử dụng một mô-đun nhỏ chạy trên trình duyệt để ghi nhận thông tin bệnh nhân và tính toán tổng tiền khám ban đầu. Chi phí này bao gồm: **Phí khám lâm sàng ban đầu** và **Phí dịch vụ chuyên khoa bổ sung**.

Theo quy tắc nghiệp vụ, tổng chi phí thanh toán phải bằng tổng số học của phí khám lâm sàng và phí dịch vụ bổ sung. Tuy nhiên, bộ phận tiếp đón bệnh nhân liên tục phản ánh rằng hệ thống đưa ra con số tính toán bất thường. Cụ thể, khi nhập phí khám là `150000` VNĐ và phí dịch vụ là `50000` VNĐ, màn hình xuất hóa đơn hiển thị tổng tiền cần thanh toán là `15000050000` VNĐ. Sự cố này gây hoang mang cho bệnh nhân và ảnh hưởng nghiêm trọng đến tiến trình bàn giao ca làm việc.

### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn JavaScript hiện tại đang được chạy trong mô-đun tiếp đón bệnh nhân:

```javascript
// Hệ thống Đặt lịch Khám bệnh CLINIC_APPOINTMENT
// Mô-đun: Tính tổng chi phí đăng ký khám ban đầu

// 1. Nhập thông tin bệnh nhân và các khoản phí từ người dùng
const patientName = prompt("Nhập tên bệnh nhân:");
const baseExamFee = prompt("Nhập phí khám lâm sàng ban đầu (VNĐ):");
const specialtyServiceFee = prompt("Nhập phí dịch vụ chuyên khoa bổ sung (VNĐ):");

// 2. Tính tổng tiền thanh toán ban đầu
const totalAmount = baseExamFee + specialtyServiceFee;

// 3. Đóng gói chuỗi thông tin hóa đơn xuất cho bệnh nhân
const invoiceNotice = `Bệnh nhân: ${patientName} | Phí khám: ${baseExamFee} VNĐ | Phí dịch vụ: ${specialtyServiceFee} VNĐ | Tổng thanh toán: ${totalAmount} VNĐ`;

// 4. Xuất kết quả hiển thị ra console
console.log(invoiceNotice);
```

# **4. Yêu cầu bài toán**

#### **Phần 1: Code Tracing & Báo cáo Test Case (Bắt buộc)**
Học viên tiến hành chạy thử chương trình, truy vết mã nguồn và hoàn thành bảng Báo cáo Test Case theo mẫu dưới đây. Hàng đầu tiên (STT 1) đã được hoàn thành mẫu làm căn cứ thực hiện cho các hàng tiếp theo:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: left;">Đầu vào (Input)</th>
      <th style="text-align: left;">Kết quả lỗi (Buggy Output)</th>
      <th style="text-align: left;">Kết quả mong đợi (Expected Output)</th>
      <th style="text-align: left;">Dòng code gây lỗi</th>
      <th style="text-align: left;">Nguyên nhân logic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td>patientName = "Nguyễn Văn A"<br>baseExamFee = "150000"<br>specialtyServiceFee = "50000"</td>
      <td>Bệnh nhân: Nguyễn Văn A | Phí khám: 150000 VNĐ | Phí dịch vụ: 50000 VNĐ | Tổng thanh toán: 15000050000 VNĐ</td>
      <td>Bệnh nhân: Nguyễn Văn A | Phí khám: 150000 VNĐ | Phí dịch vụ: 50000 VNĐ | Tổng thanh toán: 200000 VNĐ</td>
      <td>Dòng 9: <code>const totalAmount = baseExamFee + specialtyServiceFee;</code></td>
      <td>Hàm <code>prompt()</code> mặc định trả về kiểu dữ liệu String. Phép toán <code>+</code> giữa hai chuỗi sẽ thực hiện nối chuỗi thay vì cộng số học.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td>patientName = "Trần Thị B"<br>baseExamFee = "200000"<br>specialtyServiceFee = "100000"</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td>patientName = "Lê Văn C"<br>baseExamFee = "300000"<br>specialtyServiceFee = "0"</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn**
*   Viết lại tệp `app.js` đã được sửa toàn bộ lỗi logic.
*   Đảm bảo thực hiện ép kiểu `Number()` minh bạch ngay khi nhận dữ liệu từ `prompt()`.
*   Khai báo biến chính xác theo quy chuẩn ES6 (`const` cho hằng số không đổi, `let` cho biến thay đổi).
*   Sử dụng chuỗi Template Literals để xuất thông tin chuẩn xác ra Console.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (Bảng Test Case) và mã nguồn đã hoàn thiện sửa lỗi.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session02_Ex6`.
    Ví dụ: `HNKS25CNTT1_Core_Session02_Ex6`
