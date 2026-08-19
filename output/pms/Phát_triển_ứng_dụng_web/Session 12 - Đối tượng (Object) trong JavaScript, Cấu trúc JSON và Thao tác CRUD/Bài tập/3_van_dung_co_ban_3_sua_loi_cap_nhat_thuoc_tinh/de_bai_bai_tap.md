# <center>[Sửa lỗi mã nguồn] Quản lý Hồ sơ Đặt phòng Khách sạn và Đóng gói Dữ liệu JSON</center>

### **1. Mục tiêu**
*   Nắm vững thao tác thêm, cập nhật và xóa bỏ thuộc tính của JavaScript Object bằng toán tử `delete`.
*   Sử dụng thành thạo Bracket Notation đối với tên thuộc tính chứa ký tự đặc biệt (ví dụ: gạch ngang `-`).
*   Hiểu rõ quy trình chuyển đổi và khôi phục dữ liệu giữa JavaScript Object và chuỗi JSON thông qua `JSON.stringify()` và `JSON.parse()`.
*   Rèn luyện kỹ năng đọc hiểu mã nguồn, truy vết lỗi logic (code tracing) và sửa lỗi trong hệ thống quản lý đặt phòng khách sạn.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng khách sạn Agoda / Traveloka, sau khi khách hàng hoàn tất thông tin đặt phòng (`BookingReservation`), hệ thống thực hiện xử lý dữ liệu trước khi gửi sang máy chủ:
1. Nếu khách hàng chọn dịch vụ check-in sớm (`earlyCheckIn = true`), hệ thống cần tính thêm phụ phí check-in sớm với giá trị bằng 30% giá phòng cơ bản (`basePrice`) và lưu vào thuộc tính có tên `"early-checkin-fee"`.
2. Xóa bỏ mã xác thực tạm thời (`tempAuthToken`) khỏi đối tượng để bảo mật thông tin trước khi đóng gói.
3. Đóng gói đối tượng thành chuỗi dữ liệu JSON và truyền tới module tiếp theo.

Tuy nhiên, đội ngũ kiểm thử (QA) phản ánh hai sự cố nghiêm trọng sau khi triển khai phiên bản thử nghiệm:
*   Mã xác thực nhạy cảm `tempAuthToken` vẫn còn xuất hiện tên thuộc tính (key) trong đối tượng lưu trữ trước khi chuyển sang chuỗi JSON, gây lãng phí bộ nhớ và tiềm ẩn nguy cơ rò rỉ dữ liệu.
*   Khi các module giao diện cố gắng đọc giá trị phụ phí check-in sớm `"early-checkin-fee"` từ dữ liệu trả về của hàm xử lý, kết quả hiển thị trên màn hình luôn bị trả về `undefined`.

Học viên cần kiểm tra mã nguồn hiện tại, thực hiện truy vết lỗi logic (code tracing), hoàn thành bảng báo cáo Test Case và tiến hành sửa lại mã nguồn đúng chuẩn.

### **3. Mã nguồn hiện tại**

```javascript
// Hệ thống Đặt phòng Khách sạn & Homestay (HOTEL_BOOKING)
// Module: Xử lý và đóng gói hồ sơ đặt phòng (BookingReservation)

function processBookingReservation(bookingObj) {
  // 1. Kiểm tra và tính phụ phí check-in sớm (30% giá phòng cơ sở)
  if (bookingObj.earlyCheckIn === true) {
    const feeKey = "early-checkin-fee";
    bookingObj[feeKey] = bookingObj.basePrice * 0.3;
  }

  // 2. Loại bỏ thông tin nhạy cảm mã xác thực tạm thời
  bookingObj.tempAuthToken = undefined;

  // 3. Đóng gói đối tượng thành chuỗi JSON
  const jsonPayload = JSON.stringify(bookingObj);

  // 4. Trả về kết quả chuỗi JSON
  return jsonPayload;
}

// Ví dụ dữ liệu thử nghiệm
const sampleBooking = {
  reservationId: "RES-2026-001",
  guestName: "Nguyen Van A",
  roomType: "Deluxe Ocean View",
  basePrice: 2000000,
  earlyCheckIn: true,
  tempAuthToken: "AUTH_TEMP_998877"
};

// Gọi hàm xử lý
const resultPayload = processBookingReservation(sampleBooking);

// Giả lập thao tác truy xuất dữ liệu phụ phí từ kết quả trả về
console.log("Chuỗi JSON thu được:", resultPayload);
console.log("Phụ phí check-in sớm:", resultPayload["early-checkin-fee"]);
```

# **4. Yêu cầu đầu ra**

#### **Phần 1: Báo cáo phân tích truy vết lỗi (Code Tracing & Test Case Report)**
Học viên hãy phân tích mã nguồn trên, tìm vị trí các dòng code gây ra lỗi và hoàn thành bảng báo cáo Test Case dưới đây.
*   **Lưu ý:** Hàng STT 1 đã được điền sẵn mẫu minh họa. Học viên cần suy luận và điền tiếp thông tin hoàn chỉnh cho hàng STT 2 và STT 3.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: center;">STT</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Kết quả thực tế (Buggy Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Dòng code gây lỗi (Failing Line)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Nguyên nhân & Giải thích logic (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">1</td>
      <td style="border: 1px solid #dddddd;">sampleBooking chứa tempAuthToken = "AUTH_TEMP_998877"</td>
      <td style="border: 1px solid #dddddd;">Object sampleBooking vẫn còn tồn tại key tempAuthToken với giá trị undefined</td>
      <td style="border: 1px solid #dddddd;">Thuộc tính tempAuthToken bị xóa hoàn toàn khỏi Object</td>
      <td style="border: 1px solid #dddddd;">Dòng 12: bookingObj.tempAuthToken = undefined;</td>
      <td style="border: 1px solid #dddddd;">Việc gán undefined chỉ làm rỗng giá trị chứ không xóa key khỏi bộ nhớ Object. Cần sử dụng từ khóa delete để loại bỏ hoàn toàn thuộc tính.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">2</td>
      <td style="border: 1px solid #dddddd;">Truy xuất resultPayload["early-checkin-fee"] trực tiếp</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">3</td>
      <td style="border: 1px solid #dddddd;">sampleBooking với earlyCheckIn = false</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Mã nguồn đã sửa hoàn chỉnh (Source Code Correction)**
Học viên sửa lại mã nguồn JavaScript đáp ứng chính xác các yêu cầu nghiệp vụ:
1. Sử dụng đúng toán tử `delete` để xóa hoàn toàn `tempAuthToken`.
2. Giữ nguyên việc sử dụng Bracket Notation cho thuộc tính `"early-checkin-fee"`.
3. Đảm bảo dữ liệu JSON được đóng gói chuẩn bằng `JSON.stringify()`, đồng thời viết thêm đoạn mã demo giải mã lại bằng `JSON.parse()` để truy xuất thuộc tính `"early-checkin-fee"` đúng giá trị 600,000 VNĐ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_SessionSession 12_Ex3.
    Ví dụ: HNKS25CNTT1_Core_Session_Session 12_Ex3
