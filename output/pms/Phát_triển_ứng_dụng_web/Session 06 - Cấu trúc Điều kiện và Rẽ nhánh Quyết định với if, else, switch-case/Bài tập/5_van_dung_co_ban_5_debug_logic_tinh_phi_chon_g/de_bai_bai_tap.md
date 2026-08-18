#

# <center>[Sửa lỗi code] Debug Logic Tính Phí Chọn Ghế Và Hành Lý Máy Bay</center>

### **1. Mục tiêu**
*   Rèn luyện kỹ năng truy vết mã nguồn (code tracing) và phát hiện lỗi logic khi sử dụng cấu trúc rẽ nhánh `switch-case` và câu lệnh điều kiện `if-else`.
*   Hiểu rõ hiện tượng trôi lệnh (fall-through) do thiếu từ khóa `break` trong khối lệnh `switch-case`.
*   Thực hành sửa lỗi và bổ sung các điều kiện biên kiểm chuẩn dữ liệu cho chức năng làm thủ tục check-in trong hệ thống AIRLINE_CHECKIN.

### **2. Bối cảnh & Vấn đề**
Hệ thống AIRLINE_CHECKIN đang vận hành mô-đun tính phí dịch vụ bổ sung khi hành khách thực hiện check-in trực tuyến. Quy định nghiệp vụ tính phí dịch vụ của hãng bao gồm hai phần:

1.  **Phí chọn chỗ ngồi trước (`seatFee`):**
    *   Hạng Eco (`ticketClass = 1`): Ghế VIP (hàng ghế đầu/cửa thoát hiểm, `isVipSeat = true`) tính phí 100.000 VNĐ; ghế thường (`isVipSeat = false`) tính phí 30.000 VNĐ.
    *   Hạng Deluxe (`ticketClass = 2`): Ghế VIP tính phí 50.000 VNĐ; ghế thường được miễn phí (0 VNĐ).
    *   Hạng Business (`ticketClass = 3`): Miễn phí chọn mọi vị trí ghế (0 VNĐ).
2.  **Phí hành lý quá cước tại sân bay (`excessBaggageFee`):**
    *   Mỗi hành khách được miễn phí 7 kg hành lý xách tay.
    *   Nếu tổng khối lượng hành lý (`baggageWeight`) lớn hơn 7 kg, số kg vượt quá sẽ bị tính phí 50.000 VNĐ/kg. Nếu khối lượng từ 7 kg trở xuống, phí quá cước là 0 VNĐ.

Bộ phận chăm sóc khách hàng tiếp nhận nhiều phản ánh từ người dùng: Hành khách đặt vé hạng Eco khi chọn ghế VIP chỉ bị hệ thống tính 50.000 VNĐ thay vì 100.000 VNĐ. Ngoài ra, những hành khách chỉ mang 5 kg hành lý lại thấy tổng tiền hóa đơn bị trừ đi 100.000 VNĐ (xuất hiện số tiền âm bất thường).

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn JavaScript đang triển khai logic nghiệp vụ bị lỗi:```javascript
// Tính tổng phí dịch vụ check-in của hành khách
function calculateCheckinFee(ticketClass, isVipSeat, baggageWeight) {
  let seatFee = 0;

  // Tính phí chọn chỗ ngồi theo mã hạng vé
  switch (ticketClass) {
    case 1:
      seatFee = isVipSeat ? 100000 : 30000;
    case 2:
      seatFee = isVipSeat ? 50000 : 0;
      break;
    case 3:
      seatFee = 0;
      break;
    default:
      seatFee = 0;
      break;
  }

  // Tính phí hành lý quá cước tại sân bay
  let excessBaggageFee = 0;
  if (baggageWeight >= 0) {
    excessBaggageFee = (baggageWeight - 7) * 50000;
  }

  const totalFee = seatFee + excessBaggageFee;
  return { seatFee, excessBaggageFee, totalFee };
}

// Chạy thử nghiệm với dữ liệu khách hàng
const passenger1 = calculateCheckinFee(1, true, 5);
console.log("Kết quả tính phí hành khách 1:", passenger1);
```

#

## **4. Yêu cầu bài toán**

#### **Phần 1: Truy vết mã nguồn & Lập báo cáo Test Case**
Học viên phân tích đoạn code legacy trên, xác định các dòng code gây ra lỗi và hoàn thiện bảng Test Case sau vào báo cáo (dòng 1 đã được điền mẫu làm cơ sở):

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: center;">Đầu vào (Input)</th>
      <th style="text-align: center;">Đầu ra thực tế (Buggy Output)</th>
      <th style="text-align: center;">Đầu ra kỳ vọng (Expected Output)</th>
      <th style="text-align: center;">Dòng code gây lỗi (Failing Line)</th>
      <th style="text-align: center;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td>ticketClass = 1, isVipSeat = true, baggageWeight = 5</td>
      <td>{ seatFee: 50000, excessBaggageFee: -100000, totalFee: -50000 }</td>
      <td>{ seatFee: 100000, excessBaggageFee: 0, totalFee: 100000 }</td>
      <td>Dòng 7-8 & Dòng 21</td>
      <td>Do thiếu từ khóa break ở case 1 nên lệnh bị trôi xuống case 2 làm ghi đè seatFee. Đồng thời điều kiện kiểm tra hành lý (>= 0) dẫn đến phép trừ (5 - 7) ra số âm.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td>ticketClass = 1, isVipSeat = false, baggageWeight = 10</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td>ticketClass = 2, isVipSeat = true, baggageWeight = 7</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi & Tối ưu mã nguồn**
1.  Viết lại hàm `calculateCheckinFee` đảm bảo tính chính xác phí chọn ghế và phí hành lý quá cước theo đúng quy tắc nghiệp vụ.
2.  Bổ sung logic kiểm chuẩn dữ liệu đầu vào:
    *   Nếu `ticketClass` không thuộc các giá trị hợp lệ `[1, 2, 3]`, hàm trả về thông báo lỗi hoặc đối tượng chứa thông tin không hợp lệ.
    *   Nếu `baggageWeight < 0`, phí hành lý phải gán bằng 0 và in cảnh báo dữ liệu không hợp lệ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex5`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 06_Ex5`