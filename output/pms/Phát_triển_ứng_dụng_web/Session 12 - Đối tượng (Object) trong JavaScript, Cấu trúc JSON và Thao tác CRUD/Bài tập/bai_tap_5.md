#

# <center>[Vận dụng cơ bản 5] Sửa lỗi đóng gói và tính phụ phí đặt phòng khách sạn</center>

### **1. Mục tiêu**
*   **Kiến thức:** Củng cố cú pháp khai báo Object Literal, phương thức truy cập thuộc tính dynamic key, thao tác cập nhật và loại bỏ thuộc tính bằng toán tử `delete`, cùng cơ chế đóng gói/giải mã chuỗi `JSON.stringify` và `JSON.parse`.
*   **Kỹ năng:** Thực hành kỹ năng đọc mã nguồn (code tracing), phát hiện các điểm sai lệch so với yêu cầu nghiệp vụ và tiến hành sửa lỗi trực tiếp trên đối tượng dữ liệu bộ nhớ.
*   **Thái độ:** Rèn luyện tư duy lập trình cẩn trọng đối với việc quản lý an toàn dữ liệu nhạy cảm trước khi lưu trữ hoặc truyền tải dữ liệu hệ thống.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quản lý đơn đặt phòng của hệ thống khách sạn Agoda/Traveloka, khi khách hàng thực hiện đặt phòng thành công, hệ thống sẽ tạo một đối tượng dữ liệu `BookingReservation`. Đối tượng này chứa các thông tin cơ bản của phòng, thời gian nhận phòng (`checkInHour`), giá gốc (`basePrice`) và mã xác thực giao dịch tạm thời (`tempSecurityToken`).

Hệ thống cần xử lý hai nghiệp vụ quan trọng trước khi lưu trữ dữ liệu:
1.  **Tính phụ phí check-in sớm:** Khách hàng làm thủ tục check-in sớm **trước 12:00 trưa** (`checkInHour` nhỏ hơn 12) sẽ bị tính phụ phí 30% giá phòng cơ bản (`basePrice`). Các trường hợp check-in từ 12:00 trưa trở đi (`checkInHour` từ 12 đến 23) sẽ không tính phụ phí check-in sớm (phụ phí = 0).
2.  **Làm sạch dữ liệu nhạy cảm và đóng gói JSON:** Thuộc tính `tempSecurityToken` chứa mã giao dịch tạm thời chỉ dùng trong bộ nhớ tạm. Trước khi đóng gói dữ liệu thành chuỗi JSON để chuyển sang bộ lưu trữ chính, hệ thống bắt buộc phải **xóa bỏ hoàn toàn** thuộc tính này khỏi đối tượng.

**Phản ánh hiện trạng sự cố từ khách hàng và vận hành:**
*   Khách hàng đặt phòng check-in vào đúng 12:00 trưa phản ánh bị hệ thống tự động tính thêm 30% phụ phí check-in sớm bất hợp lý trên hóa đơn.
*   Đội ngũ kiểm định an toàn thông tin phát hiện chuỗi JSON đầu ra vẫn lưu thuộc tính `tempSecurityToken` dưới dạng giá trị `null` hoặc `undefined`, gây lãng phí dung lượng lưu trữ và không tuân thủ chuẩn làm sạch dữ liệu.

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn JavaScript đang được vận hành trên hệ thống:```javascript
// Mã nguồn xử lý và đóng gói thông tin đặt phòng khách sạn
function processBookingReservation(bookingData) {
  // Tạo đối tượng đặt phòng ban đầu
  const bookingObj = {
    bookingId: bookingData.bookingId,
    roomType: bookingData.roomType,
    basePrice: bookingData.basePrice,
    checkInHour: bookingData.checkInHour,
    tempSecurityToken: bookingData.tempSecurityToken
  };

  // Tính toán phụ phí check-in sớm
  let earlyCheckInSurcharge = 0;
  if (bookingObj.checkInHour <= 12) {
    earlyCheckInSurcharge = bookingObj.basePrice * 0.3;
  }

  // Cập nhật các thuộc tính tổng thanh toán vào đối tượng
  bookingObj.surcharge = earlyCheckInSurcharge;
  bookingObj.totalPrice = bookingObj.basePrice + earlyCheckInSurcharge;

  // Loại bỏ token bảo mật tạm thời trước khi lưu trữ
  bookingObj.tempSecurityToken = undefined;

  // Đóng gói đối tượng thành chuỗi JSON
  const jsonOutput = JSON.stringify(bookingObj);

  return {
    updatedObject: bookingObj,
    jsonPayload: jsonOutput
  };
}

// Chạy thử nghiệm hàm xử lý đơn đặt phòng
const sampleBooking = {
  bookingId: "BK-2026-8899",
  roomType: "Deluxe Ocean View",
  basePrice: 2000000,
  checkInHour: 12,
  tempSecurityToken: "SEC_TOKEN_TMP_998234"
};

const result = processBookingReservation(sampleBooking);
console.log("Kết quả đối tượng xử lý:", result.updatedObject);
console.log("Chuỗi JSON đóng gói:", result.jsonPayload);
```

#

## **4. Yêu cầu bài toán**

#### **Phần 1: Truy vết mã nguồn & Báo cáo Test Case (Code Tracing)**
Học viên tiến hành thực thi mã nguồn bằng tay (code tracing), phát hiện các dòng mã gây lỗi nghiệp vụ và hoàn thành Báo cáo Test Case theo mẫu bảng dưới đây. Bảng bắt buộc phải giữ lại 1 testcase mẫu đã hoàn chỉnh và hoàn thiện các ô có dấu `...`.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th>STT</th>
      <th>Dữ liệu đầu vào (Input)</th>
      <th>Kết quả thực tế (Buggy Output)</th>
      <th>Kết quả kỳ vọng (Expected Output)</th>
      <th>Dòng code gây lỗi (Line of Code)</th>
      <th>Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>basePrice: 2000000<br>checkInHour: 12<br>tempSecurityToken: "TOKEN123"</td>
      <td>surcharge: 600000<br>totalPrice: 2600000<br>tempSecurityToken: undefined</td>
      <td>surcharge: 0<br>totalPrice: 2000000<br>Thuộc tính tempSecurityToken bị xóa hẳn khỏi Object</td>
      <td>Dòng 13: <code>if (bookingObj.checkInHour <= 12)</code><br>Dòng 22: <code>bookingObj.tempSecurityToken = undefined;</code></td>
      <td>Dùng toán tử <code><=</code> khiến mốc 12h trưa bị tính sai phụ phí. Gán <code>undefined</code> chỉ đổi giá trị chứ không xóa key khỏi bộ nhớ Object.</td>
    </tr>
    <tr>
      <td>2</td>
      <td>basePrice: 1500000<br>checkInHour: 9<br>tempSecurityToken: "TOKEN999"</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>3</td>
      <td>basePrice: 3000000<br>checkInHour: 14<br>tempSecurityToken: "TOKEN456"</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

Sơ đồ luồng xử lý chuẩn của hệ thống:```mermaid
flowchart TD
    A([Bắt đầu quy trình]) --> B[/Nhận thông tin đơn đặt phòng bookingData/]
    B --> C["Khởi tạo đối tượng bookingObj từ bookingData"]
    C --> D{Kiểm tra checkInHour < 12?}
    D -- Đúng --> E["Gán phụ phí earlyCheckInSurcharge = basePrice * 0.3"]
    D -- Sai --> F["Gán phụ phí earlyCheckInSurcharge = 0"]
    E --> G["Cập nhật surcharge và totalPrice vào bookingObj"]
    F --> G
    G --> H["Xóa thuộc tính tempSecurityToken bằng toán tử delete"]
    H --> I["Chuyển đổi bookingObj sang chuỗi JSON bằng JSON.stringify"]
    I --> J[/Đầu ra: Đối tượng bookingObj và chuỗi JSON payload/]
    J --> K([Kết thúc quy trình])
```

#

### **Phần 2: Sửa đổi và tối ưu hóa mã nguồn**
Học viên viết lại hàm `processBookingReservation(bookingData)` để giải quyết triệt để các yêu cầu sau:
1.  **Sửa lỗi phụ phí:** Khách check-in trước 12:00 trưa (`checkInHour < 12`) mới tính 30% phụ phí trên `basePrice`. Đúng 12:00 trưa trở đi không tính phụ phí.
2.  **Sửa lỗi xóa dữ liệu:** Sử dụng toán tử `delete` để xóa triệt để thuộc tính `tempSecurityToken` khỏi `bookingObj`.
3.  **Kiểm tra tính hợp lệ dữ liệu (Validation):**
    *   Nếu `basePrice <= 0` hoặc không phải là số hợp lệ, ném ra ngoại lệ `Error("Giá phòng cơ bản phải lớn hơn 0")`.
    *   Nếu `checkInHour < 0` hoặc `checkInHour > 23` hoặc không phải số nguyên, ném ra ngoại lệ `Error("Giờ nhận phòng không hợp lệ (0-23)")`.
4.  **Bổ sung tính năng xác minh JSON:** Viết thêm một hàm `restoreBookingPayload(jsonPayload)` nhận đầu vào là chuỗi JSON, thực hiện `JSON.parse` và trả về đối tượng đã khôi phục để kiểm tra tính toàn vẹn dữ liệu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_Session12_Ex5.
    Ví dụ: HNKS25CNTT1_Core_Session12_Ex5