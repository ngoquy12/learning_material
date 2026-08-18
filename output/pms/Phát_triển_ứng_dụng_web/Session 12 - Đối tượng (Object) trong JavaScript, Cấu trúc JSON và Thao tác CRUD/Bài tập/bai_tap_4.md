#

# <center>[Chẩn đoán & Sửa lỗi] Đóng gói dữ liệu hóa đơn đặt phòng và chuẩn hóa JSON</center>

### **1. Mục tiêu**
*   Phát hiện và sửa các lỗi logic khi thao tác với đối tượng JavaScript (thêm/sửa thuộc tính động bằng Bracket Notation, loại bỏ thuộc tính khỏi bộ nhớ với toán tử `delete`).
*   Thực hiện chuyển đổi qua lại giữa Object và chuỗi JSON (`JSON.stringify()`, `JSON.parse()`) đúng chuẩn kỹ thuật JavaScript ES6+.
*   Rèn luyện kỹ năng đọc mã nguồn (code tracing), hoàn thiện báo cáo kiểm thử (Test Case Report) và đưa ra phương án khắc phục mã nguồn trong hệ thống đặt phòng khách sạn.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng khách sạn trực tuyến, khi người dùng hoàn tất đặt phòng, hệ thống cần xử lý đối tượng hóa đơn lưu trú (`BookingReservation`). Dữ liệu này bao gồm thông tin phòng, phụ phí dịch vụ phát sinh động và các token xác thực tạm thời (`tempAuthToken`).

Trước khi đóng gói dữ liệu thành chuỗi JSON để truyền tải sang bộ phận lưu trữ, hệ thống phải cập nhật phụ phí dịch vụ theo tên thuộc tính động và loại bỏ triệt để token xác thực tạm thời để bảo mật. Tuy nhiên, bộ phận kỹ thuật ghi nhận phản ánh từ hệ thống backend:
1. Thông tin phụ phí dịch vụ không được ghi nhận vào thuộc tính `extra-services` mà lại tạo ra thuộc tính mới không đúng yêu cầu.
2. Mã xác thực tạm thời `tempAuthToken` vẫn xuất hiện dưới dạng key tồn tại trong đối tượng gây lãng phí tài nguyên bộ nhớ.
3. Giao diện xác nhận hóa đơn hiển thị giá trị `undefined` khi cố gắng đọc thông tin khách hàng và chi phí từ chuỗi JSON đã đóng gói.

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn JavaScript legacy đang chạy lỗi trong hệ thống xử lý hóa đơn:```javascript
// Khai báo thông tin phiếu đặt phòng khách sạn ban đầu
const bookingReservation = {
  reservationId: "RES-88219",
  guestName: "Nguyen Van A",
  roomType: "Deluxe Ocean View",
  basePrice: 1500000,
  tempAuthToken: "AUTH_TEMP_998234",
  "extra-services": 0
};

// 1. Cập nhật phụ phí dịch vụ phát sinh từ biến động tên thuộc tính
const surchargeKey = "extra-services";
bookingReservation.surchargeKey = 250000;

// 2. Loại bỏ mã xác thực tạm thời trước khi đóng gói dữ liệu
bookingReservation.tempAuthToken = undefined;

// 3. Đóng gói đối tượng thành chuỗi JSON để chuẩn bị lưu trữ
const jsonPayload = JSON.stringify(bookingReservation);

// 4. Đọc dữ liệu tổng tiền dịch vụ để hiển thị trên giao diện xác nhận
const serviceFee = jsonPayload["extra-services"];
const guestName = jsonPayload.guestName;

console.log("Tên khách hàng:", guestName);
console.log("Phụ phí dịch vụ:", serviceFee);
console.log("Chuỗi JSON gửi đi:", jsonPayload);
```

#

## **4. Yêu cầu bài toán**

#### **Phần 1: Lập báo cáo phân tích lỗi & Kiểm thử (Test Case Report Table)**
Học viên phân tích đoạn mã nguồn trên, phát hiện 3 lỗi logic chính và hoàn thiện bảng báo cáo kiểm thử dưới đây vào bài làm. Hàng đầu tiên đã được điền mẫu làm căn cứ thực hiện.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: center;">STT</th>
      <th style="padding: 8px; text-align: left;">Đầu vào (Input)</th>
      <th style="padding: 8px; text-align: left;">Kết quả thực tế (Buggy Output)</th>
      <th style="padding: 8px; text-align: left;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="padding: 8px; text-align: center;">Dòng code gây lỗi</th>
      <th style="padding: 8px; text-align: left;">Nguyên nhân & Giải thích</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; text-align: center;">1</td>
      <td style="padding: 8px;"><code>surchargeKey = "extra-services"</code>, gán <code>bookingReservation.surchargeKey = 250000</code></td>
      <td style="padding: 8px;">Tạo mới key <code>surchargeKey: 250000</code>, key <code>extra-services</code> vẫn có giá trị <code>0</code></td>
      <td style="padding: 8px;">Giá trị của key <code>extra-services</code> được cập nhật thành <code>250000</code></td>
      <td style="padding: 8px; text-align: center;">Dòng 13</td>
      <td style="padding: 8px;">Sử dụng Dot Notation khiến JS hiểu nhầm là tạo key tên "surchargeKey" thay vì dùng Bracket Notation <code>bookingReservation[surchargeKey]</code> để truy cập key động.</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">2</td>
      <td style="padding: 8px;"><code>bookingReservation.tempAuthToken = undefined</code></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">3</td>
      <td style="padding: 8px;">Truy cập <code>jsonPayload.guestName</code> và <code>jsonPayload["extra-services"]</code></td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Mã nguồn khắc phục lỗi hoàn chỉnh**
Viết lại đoạn mã JavaScript sửa toàn bộ các lỗi trên, đảm bảo tuân thủ các quy tắc sau:
1. Sử dụng **Bracket Notation** để cập nhật thuộc tính `extra-services` thông qua biến động `surchargeKey`.
2. Sử dụng toán tử **`delete`** để loại bỏ hoàn toàn `tempAuthToken` ra khỏi đối tượng trước khi serialization.
3. Sử dụng **`JSON.parse()`** để giải mã `jsonPayload` thành một đối tượng JavaScript hợp lệ trước khi truy cập thuộc tính `guestName` và `extra-services` để in ra màn hình.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 12_Ex4`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 12_Ex4`