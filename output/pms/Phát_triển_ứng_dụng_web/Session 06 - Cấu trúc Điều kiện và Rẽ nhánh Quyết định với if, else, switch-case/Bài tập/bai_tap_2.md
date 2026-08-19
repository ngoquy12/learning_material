# <center>[Vận dụng cơ bản 2] Sửa lỗi trôi lệnh trong module tính phí hành lý ký gửi</center>

### **1. Mục tiêu**
* Hiểu và vận dụng cấu trúc rẽ nhánh `switch-case` để phân loại hạng vé và gán định mức hành lý ký gửi.
* Phát hiện và khắc phục lỗi trôi lệnh (fall-through) do thiếu câu lệnh `break` trong khối `switch-case`.
* Sử dụng biểu thức điều kiện ba ngôi (ternary operator) để tính toán số kg vượt cước và tổng chi phí phát sinh chính xác.

### **2. Bối cảnh & Vấn đề**
Trong Hệ thống Bán Vé & Check-in Máy bay Vietjet / Vietnam Airlines (AIRLINE_CHECKIN), quầy làm thủ tục tự động tại sân bay phụ trách kiểm tra trọng lượng hành lý ký gửi của hành khách và tính phí phạt nếu hành lý vượt quá định mức quy định cho từng hạng vé.

Quy tắc nghiệp vụ của hệ thống được quy định như sau:
1. Hạng vé `Business`: Miễn phí 30 kg hành lý ký gửi.
2. Hạng vé `Deluxe`: Miễn phí 20 kg hành lý ký gửi.
3. Hạng vé `Eco`: Miễn phí 7 kg hành lý xách tay/ký gửi.
4. Trường hợp hạng vé không thuộc 3 loại trên: Trả về thông báo lỗi `"Hạng vé không hợp lệ"`.
5. Chi phí phạt quá cước: Nếu trọng lượng hành lý thực tế vượt quá định mức miễn phí, mỗi kg quá cước bị phạt 50.000 VNĐ/kg. Nếu trọng lượng nhỏ hơn hoặc bằng định mức, phí phạt quá cước là 0 VNĐ.

Bộ phận vận hành nhận được phản ánh từ các hành khách bay hạng `Business`. Mặc dù hành lý ký gửi của họ chỉ nặng 25 kg (hoàn toàn nằm trong định mức 30 kg miễn phí), hệ thống check-in tự động lại thông báo họ bị phạt 250.000 VNĐ tiền quá cước (tương ứng với việc áp sai định mức 20 kg của hạng `Deluxe`).

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn Javascript legacy đang triển khai tại hệ thống kiosk check-in:

```javascript
/**
 * Module tính phí hành lý ký gửi tại quầy check-in sân bay
 * @param {string} ticketClass - Hạng vé hành khách (Business, Deluxe, Eco)
 * @param {number} actualWeight - Trọng lượng hành lý thực tế (kg)
 */
function calculateBaggageFee(ticketClass, actualWeight) {
  let freeWeightLimit = 0;

  // Xác định định mức hành lý dựa trên hạng vé
  switch (ticketClass) {
    case "Business":
      freeWeightLimit = 30;
    case "Deluxe":
      freeWeightLimit = 20;
      break;
    case "Eco":
      freeWeightLimit = 7;
      break;
    default:
      return "Hạng vé không hợp lệ";
  }

  // Tính số kg quá cước và phí phạt tương ứng
  const excessWeight = actualWeight > freeWeightLimit ? actualWeight - freeWeightLimit : 0;
  const excessFee = excessWeight * 50000;

  return {
    ticketClass: ticketClass,
    freeWeightLimit: freeWeightLimit,
    actualWeight: actualWeight,
    excessWeight: excessWeight,
    excessFee: excessFee
  };
}

// Kiểm thử hệ thống với hành khách hạng Business (hành lý 25 kg)
const passengerCheckIn = calculateBaggageFee("Business", 25);
console.log("Kết quả làm thủ tục:", passengerCheckIn);
```

# **4. Yêu cầu đầu ra**

Học viên thực hiện bài tập theo 2 phần bắt buộc sau:

#### **Phần 1: Báo cáo vết mã nguồn (Code Tracing Table)**
Thực hiện chạy vết mã nguồn, tìm dòng gây lỗi và hoàn thiện bảng báo cáo Test Case dưới đây. Dòng đầu tiên đã được điền mẫu làm căn cứ thực hiện:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: center;">STT</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Kết quả thực tế bị lỗi (Buggy Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Kết quả kỳ vọng đúng (Expected Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Dòng code gây lỗi</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Giải thích nguyên nhân logic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">1</td>
      <td style="border: 1px solid #dddddd;"><code>calculateBaggageFee("Business 25)</code></td>
      <td style="border: 1px solid #dddddd;"><code>{ freeWeightLimit: 20, excessFee: 250000 }</code></td>
      <td style="border: 1px solid #dddddd;"><code>{ freeWeightLimit: 30, excessFee: 0 }</code></td>
      <td style="border: 1px solid #dddddd;">Dòng 13</td>
      <td style="border: 1px solid #dddddd;">Thiếu từ khóa <code>break;</code> trong <code>case "Business"</code> khiến luồng thực thi bị trôi xuống <code>case "Deluxe"</code> và ghi đè <code>freeWeightLimit = 20</code>.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">2</td>
      <td style="border: 1px solid #dddddd;"><code>calculateBaggageFee("Deluxe 24)</code></td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">3</td>
      <td style="border: 1px solid #dddddd;"><code>calculateBaggageFee("FirstClass 15)</code></td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Mã nguồn đã sửa hoàn thiện**
* Sửa lại toàn bộ câu lệnh `switch-case` trong hàm `calculateBaggageFee` để đảm bảo không bị lỗi trôi lệnh.
* Thêm logic kiểm chuẩn đầu vào cho biến `actualWeight`: Nếu trọng lượng không phải kiểu số (`typeof actualWeight !== "number"`) hoặc bị âm (`actualWeight < 0`), hàm phải trả về thông báo lỗi: `"Trọng lượng hành lý không hợp lệ"`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
* Phần phân tích/báo cáo và mã nguồn triển khai.
* Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex2`.
  Ví dụ: `HNKS25CNTT1_Core_Session_Session 06_Ex2`
