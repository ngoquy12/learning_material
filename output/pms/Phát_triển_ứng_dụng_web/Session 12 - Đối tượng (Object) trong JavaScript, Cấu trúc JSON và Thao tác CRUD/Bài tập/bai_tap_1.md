#

# <center>[Vận dụng cơ bản 1] Sửa lỗi đóng gói dữ liệu đặt phòng khách sạn và tính phụ thu check-in sớm</center>

### **1. Mục tiêu**
*   **Kiến thức**: Củng cố cú pháp truy xuất thuộc tính trong JavaScript Object Literal (Dot Notation và Bracket Notation), thao tác thêm/sửa/xóa thuộc tính bằng toán tử `delete`, và quy trình mã hóa/giải mã JSON (`JSON.stringify`, `JSON.parse`).
*   **Kỹ năng**: Phát hiện lỗi truy cập key động do thiếu dấu nháy, nhận biết sự khác biệt giữa việc gán `undefined` và sử dụng toán tử `delete`, thực hiện truy vết lỗi (code tracing) và hoàn thiện báo cáo kiểm thử.
*   **Mức độ tư duy**: Vận dụng cơ bản 1 - Xác định đúng lỗi logic nghiệp vụ đơn giản và sửa lỗi mã nguồn theo các quy tắc đã học.

### **2. Bối cảnh & Vấn đề**
Trong Hệ thống Đặt phòng Khách sạn & Homestay (HOTEL_BOOKING), khi khách hàng tạo đơn đặt phòng trực tuyến, hệ thống sẽ tiếp nhận thông tin đối tượng đơn hàng (`BookingReservation`). Để chuẩn bị dữ liệu lưu trữ và truyền tải qua API backend, hệ thống cần thực hiện tính toán phụ thu và đóng gói đối tượng dưới dạng chuỗi JSON.

Quy tắc nghiệp vụ được định nghĩa như sau:
1.  **Phụ thu check-in sớm**: Nếu thời gian check-in thực tế của khách trước 12:00 PM (`checkInHour < 12`), hệ thống tính phụ thu check-in sớm bằng **30% giá phòng cơ bản** (`roomPrice`) và lưu vào thuộc tính tên `"early-surcharge"`. Trường hợp check-in từ 12:00 PM trở đi, giá trị này bằng `0`.
2.  **Dọn dẹp dữ liệu tạm**: Trước khi đóng gói đối tượng thành chuỗi JSON, thuộc tính tạm thời `tempToken` (dùng cho xác thực giao dịch dở dang) bắt buộc phải được xóa bỏ hoàn toàn khỏi bộ nhớ đối tượng để đảm bảo an toàn và tối ưu kích thước dữ liệu.**Phản ánh sự cố nghiệp vụ**: Bộ phận vận hành ghi nhận hệ thống xuất ra chuỗi JSON có trường phụ thu check-in sớm mang giá trị `null` thay vì số tiền phụ thu chính xác. Ngoài ra, kiểm định viên phát hiện khi chuyển ngược chuỗi JSON thành đối tượng hoặc kiểm tra đối tượng trước khi đóng gói, key `tempToken` vẫn chưa bị xóa triệt để.

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn JavaScript đang vận hành module xử lý đặt phòng bị lỗi:```javascript
// Hàm tính toán phụ thu và chuẩn hóa dữ liệu đơn đặt phòng
function processBookingReservation(rawBooking, checkInHour) {
  // Sao chép đối tượng để tránh thay đổi trực tiếp dữ liệu gốc
  const booking = { ...rawBooking };

  // Kiểm tra điều kiện check-in sớm (trước 12 giờ trưa)
  if (checkInHour < 12) {
    // Tính phụ thu 30% giá phòng cơ bản
    booking["early-surcharge"] = booking[roomPrice] * 0.3;
  } else {
    booking["early-surcharge"] = 0;
  }

  // Dọn dẹp dữ liệu token tạm thời
  booking.tempToken = undefined;

  // Đóng gói đối tượng thành chuỗi JSON
  const jsonResult = JSON.stringify(booking);
  return jsonResult;
}

// Dữ liệu thử nghiệm đơn đặt phòng
const sampleBooking = {
  bookingId: "BK-2026-001",
  roomName: "Deluxe Ocean View",
  roomPrice: 1000000,
  tempToken: "TMP_TOKEN_9981",
  "early-surcharge": 0
};

// Chạy thử nghiệm với giờ check-in 9 giờ sáng
const resultJson = processBookingReservation(sampleBooking, 9);
console.log("Kết quả chuỗi JSON:", resultJson);

const restoredObj = JSON.parse(resultJson);
console.log("Giá trị phụ thu nhận được:", restoredObj["early-surcharge"]);
console.log("Thuộc tính tempToken có còn nằm trong Object gốc không?:", "tempToken" in sampleBooking);
```

#

## **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Phát hiện lỗi logic (Báo cáo Test Case)**
Học viên đọc hiểu mã nguồn hiện tại, thực hiện truy vết dòng code gây lỗi và hoàn thiện bảng Báo cáo Test Case dưới đây. Hàng STT 1 đã được điền mẫu làm căn cứ:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: left;">Đầu vào (Input)</th>
      <th style="text-align: left;">Kết quả thực tế (Buggy Output)</th>
      <th style="text-align: left;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="text-align: center;">Dòng code gây lỗi</th>
      <th style="text-align: left;">Nguyên nhân lỗi (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td>
        rawBooking (roomPrice: 1000000, tempToken: "TMP_TOKEN_9981")<br>
        checkInHour = 9
      </td>
      <td>
        "early-surcharge": null (trong JSON)<br>
        "tempToken" vẫn tồn tại dưới dạng key có giá trị undefined trong Object.
      </td>
      <td>
        "early-surcharge": 300000 (trong JSON)<br>
        Key "tempToken" bị xóa hoàn toàn khỏi Object.
      </td>
      <td style="text-align: center;">Dòng 8 & Dòng 15</td>
      <td>
        - Dòng 8 dùng `booking[roomPrice]` thiếu dấu nháy khiến JS hiểu `roomPrice` là biến chưa khai báo (undefined), dẫn đến tính toán bằng NaN.<br>
        - Dòng 15 gán `undefined` chỉ đổi giá trị chứ không xóa hẳn key khỏi bộ nhớ Object (cần dùng `delete`).
      </td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td>
        rawBooking (roomPrice: 2000000, tempToken: "TMP_TOKEN_5544")<br>
        checkInHour = 10
      </td>
      <td>...</td>
      <td>...</td>
      <td style="text-align: center;">...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td>
        rawBooking (roomPrice: 1500000, tempToken: "TMP_TOKEN_1122")<br>
        checkInHour = 14
      </td>
      <td>...</td>
      <td>...</td>
      <td style="text-align: center;">...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn (Source Code Correction)**
Viết lại hàm `processBookingReservation` đảm bảo:
1.  Truy xuất thuộc tính `roomPrice` đúng cú pháp để tính phụ thu check-in sớm 30% khi `checkInHour < 12`.
2.  Sử dụng đúng toán tử `delete` để loại bỏ hoàn toàn thuộc tính `tempToken` khỏi đối tượng `booking`.
3.  Đóng gói chuỗi JSON hợp lệ và parse ngược lại thành Object thành công.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex1`.
    Ví dụ: `HNKS25CNTT1_Core_Session12_Ex1`