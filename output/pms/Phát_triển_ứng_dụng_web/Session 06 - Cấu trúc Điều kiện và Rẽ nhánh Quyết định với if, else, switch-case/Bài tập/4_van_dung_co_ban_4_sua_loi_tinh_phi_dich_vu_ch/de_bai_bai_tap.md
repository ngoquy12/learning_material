#

# <center>Sửa lỗi tính phí dịch vụ check-in và chọn vị trí ghế máy bay</center>

### **1. Mục tiêu**
*   Phát hiện và khắc phục sự cố trôi lệnh (fall-through) trong cấu trúc điều kiện rẽ nhánh `switch-case`.
*   Sử dụng thành thạo từ khóa `break` và câu lệnh `switch-case`, `if-else` kết hợp toán tử ba ngôi để tính toán phí cước chính xác.
*   Rèn luyện kỹ năng vạch vết mã nguồn (code tracing) và lập bảng báo cáo Test Case phân tích lỗi logic hệ thống.

### **2. Bối cảnh & Vấn đề**
Hệ thống check-in tự động tại sân bay của hãng hàng không quy định mức phụ phí hành lý ký gửi và phí chọn chỗ ngồi dựa trên mã hạng vé đăng ký của hành khách:
*   **Hạng 3 (Business - Thương gia):** Hạn mức hành lý miễn phí là 30 kg, phí vượt cước 0 VNĐ/kg (miễn phí), phí chọn chỗ ngồi trước 0 VNĐ (miễn phí).
*   **Hạng 2 (Deluxe - Linh hoạt):** Hạn mức hành lý miễn phí là 10 kg, phí vượt cước 40.000 VNĐ/kg cho mỗi kg vượt hạn mức, phí chọn chỗ ngồi trước là 15.000 VNĐ.
*   **Hạng 1 (Eco - Phổ thông):** Hạn mức hành lý miễn phí là 7 kg, phí vượt cước 50.000 VNĐ/kg cho mỗi kg vượt hạn mức, phí chọn chỗ ngồi trước là 30.000 VNĐ.
*   **Trường hợp mã hạng vé khác (không thuộc 1, 2, 3):** Đặt tên hạng vé là "Không hợp lệ hạn mức hành lý 0 kg, phí vượt cước 0 VNĐ/kg, phí chọn ghế 0 VNĐ.

**Triệu chứng sự cố:**
Khách hàng đặt vé hạng Thương gia (mã hạng 3) gửi phản ánh khi làm thủ tục check-in tự động: mặc dù số cân hành lý mang theo (12 kg) nằm trong hạn mức cho phép (30 kg) và chọn ghế trước, màn hình quầy check-in lại hiển thị tên hạng vé là "Deluxe" và tự động cộng thêm phí chọn ghế 15.000 VNĐ cùng phí hành lý quá cước, dẫn đến tổng số tiền thanh toán hiển thị bị sai.

### **3. Mã nguồn hiện tại**
Đoạn mã nguồn dưới đây được trích xuất từ mô-đun xử lý phụ phí check-in của hệ thống:```javascript
// Mô-đun tính phí dịch vụ check-in hành lý và chọn chỗ ngồi
const ticketClass = 3; // Mã hạng vé: 1 - Eco, 2 - Deluxe, 3 - Business
const baggageWeight = 12; // Cân nặng hành lý ký gửi của hành khách (kg)
const isSelectSeat = true; // Trạng thái chọn chỗ ngồi trước (true/false)

let freeWeightLimit = 0;
let excessFeePerKg = 0;
let seatFee = 0;
let className = "";

// Cấu trúc kiểm tra phân loại hạng vé
switch (ticketClass) {
  case 3:
    className = "Business";
    freeWeightLimit = 30;
    excessFeePerKg = 0;
    seatFee = 0;
  case 2:
    className = "Deluxe";
    freeWeightLimit = 10;
    excessFeePerKg = 40000;
    seatFee = 15000;
    break;
  case 1:
    className = "Eco";
    freeWeightLimit = 7;
    excessFeePerKg = 50000;
    seatFee = 30000;
    break;
  default:
    className = "Không hợp lệ";
    freeWeightLimit = 0;
    excessFeePerKg = 0;
    seatFee = 0;
    break;
}

// Tính số kg hành lý vượt hạn mức
let excessWeight = baggageWeight - freeWeightLimit;

// Tính tiền phụ phí hành lý quá cước
let excessBaggageFee = excessWeight > 0 ? excessWeight * excessFeePerKg : 0;

// Tính tổng phí dịch vụ bổ sung
let totalServiceFee = excessBaggageFee + (isSelectSeat ? seatFee : 0);

console.log("Hạng vé xác nhận:", className);
console.log("Khối lượng hành lý quá cước (kg):", excessWeight > 0 ? excessWeight : 0);
console.log("Phí hành lý quá cước (VNĐ):", excessBaggageFee);
console.log("Phí chọn chỗ ngồi (VNĐ):", isSelectSeat ? seatFee : 0);
console.log("Tổng phí dịch vụ check-in (VNĐ):", totalServiceFee);
```

#

## **4. Yêu cầu bài toán**
Học viên thực hiện bài tập theo 2 phần:

**Phần 1: Vạch vết mã nguồn và Hoàn thiện Báo cáo Test Case**
Đọc hiểu đoạn mã legacy, vạch vết dòng lệnh gây lỗi và hoàn thiện bảng phân tích 3 trường hợp kiểm thử dưới đây. Hãy hoàn thành các ô có dấu `...` dựa trên dòng mẫu tham chiếu STT 1.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="6" cellSpacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: center;">STT</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Kết quả thực tế (Buggy Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Dòng code gây lỗi (Failing Line)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Phân tích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">1</td>
      <td style="border: 1px solid #dddddd;">ticketClass = 3<br>baggageWeight = 12<br>isSelectSeat = true</td>
      <td style="border: 1px solid #dddddd;">Hạng vé: Deluxe<br>Tổng phí: 95.000 VNĐ</td>
      <td style="border: 1px solid #dddddd;">Hạng vé: Business<br>Tổng phí: 0 VNĐ</td>
      <td style="border: 1px solid #dddddd;">Dòng 17 (Kết thúc khối case 3)</td>
      <td style="border: 1px solid #dddddd;">Khối <code>case 3</code> thiếu từ khóa <code>break;</code> làm chương trình trôi lệnh xuống <code>case 2</code>, ghi đè toàn bộ giá trị hạng Business bằng Deluxe.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">2</td>
      <td style="border: 1px solid #dddddd;">ticketClass = 1<br>baggageWeight = 10<br>isSelectSeat = true</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">3</td>
      <td style="border: 1px solid #dddddd;">ticketClass = 99<br>baggageWeight = 5<br>isSelectSeat = false</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
  </tbody>
</table>

**Phần 2: Sửa lỗi mã nguồn**
Tiến hành chỉnh sửa mã nguồn JavaScript để đảm bảo tính đúng 100% quy tắc nghiệp vụ tính phí dịch vụ check-in máy bay cho tất cả các hạng vé và trường hợp đầu vào.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_SessionSession 06_Ex4.
    Ví dụ: HNKS25CNTT1_Core_Session_Session 06_Ex4