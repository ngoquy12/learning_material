#

# <center>[Vận dụng cơ bản 6] Sửa lỗi xử lý hóa đơn đặt phòng và đóng gói JSON</center>

### **1. Mục tiêu**
*   Hiểu và vận dụng thành thạo cách truy cập, thêm, sửa, xóa thuộc tính của đối tượng (Object Literal) trong JavaScript.
*   Phân biệt sự khác nhau giữa việc gán `undefined` cho thuộc tính và việc sử dụng toán tử `delete` để loại bỏ thuộc tính hoàn toàn khỏi đối tượng.
*   Nắm vững bản chất của chuỗi JSON, hiểu rõ cơ chế chuyển đổi dữ liệu qua `JSON.stringify()` và khôi phục đối tượng bằng `JSON.parse()`.
*   Rèn luyện kỹ năng đọc hiểu mã nguồn (code tracing), phát hiện lỗi truy cập thuộc tính sai trên chuỗi JSON và hoàn thiện báo cáo kiểm thử (Test Case Report).

### **2. Bối cảnh & Vấn đề**
Trong Hệ thống Đặt phòng Khách sạn & Homestay (Agoda / Traveloka), mô-đun xử lý hóa đơn thanh toán (`BookingReservation`) chịu trách nhiệm tiếp nhận thông tin từ phòng đã chọn, áp dụng các quy tắc tính phụ phí và đóng gói dữ liệu hóa đơn chuyển đổi sang dạng chuỗi JSON để lưu trữ hoặc truyền qua lại giữa các thành phần giao diện.

Quy tắc nghiệp vụ của hệ thống quy định:
1. Khi khách hàng đăng ký check-in sớm (trước 12:00 PM), hệ thống sẽ tính thêm **30% giá phòng cơ bản** (`roomPrice`) làm phụ phí check-in sớm và lưu vào thuộc tính có tên key đặc biệt `"early-checkin-fee"`, đồng thời cộng thêm số tiền này vào tổng tiền thanh toán (`totalAmount`).
2. Mã bảo mật thẻ thanh toán tạm thời (`tempSecurityCode`) chỉ được lưu tạm thời để xác minh giao dịch ban đầu. Trước khi đóng gói dữ liệu thành JSON và gửi về màn hình xác nhận, thuộc tính nhạy cảm này **bắt buộc phải xóa hoàn toàn** khỏi đối tượng.
3. Sau khi đóng gói dữ liệu thành chuỗi JSON (`jsonResult`), hệ thống cần truy xuất tổng tiền thanh toán xác nhận (`confirmedTotal`) để hiển thị thông báo cho khách hàng.

Tuy nhiên, đội ngũ hỗ trợ khách hàng phản ánh hai sự cố nghiêm trọng:
- Màn hình thông báo xác nhận luôn hiển thị giá trị tổng tiền thanh toán `confirmedTotal` là `undefined`, mặc dù chuỗi JSON vẫn được tạo ra.
- Bộ phận an toàn thông tin phát hiện thông tin mã bảo mật tạm `tempSecurityCode` vẫn tồn tại dưới dạng thuộc tính trong đối tượng hóa đơn gốc (dù có giá trị là `undefined`), gây rò rỉ dữ liệu nhạy cảm trong bộ nhớ runtime.

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn xử lý hóa đơn đang gặp lỗi logic:```javascript
/**
 * Hàm xử lý hóa đơn đặt phòng khách sạn và đóng gói dữ liệu
 * @param {Object} bookingObj - Đối tượng thông tin đặt phòng
 * @param {boolean} isEarlyCheckin - Cờ xác định khách check-in sớm trước 12h trưa
 * @returns {Object} Khối dữ liệu gồm chuỗi JSON và tổng tiền xác nhận
 */
function processBookingInvoice(bookingObj, isEarlyCheckin) {
    // 1. Gán tổng tiền thanh toán ban đầu từ giá phòng
    bookingObj.totalAmount = bookingObj.roomPrice;

    // 2. Kiểm tra điều kiện phụ thu check-in sớm (thêm 30% giá phòng)
    if (isEarlyCheckin) {
        const earlyFee = bookingObj.roomPrice * 0.3;
        bookingObj["early-checkin-fee"] = earlyFee;
        bookingObj.totalAmount += earlyFee;
    }

    // 3. Loại bỏ mã bảo mật tạm thời khỏi đối tượng
    bookingObj.tempSecurityCode = undefined;

    // 4. Đóng gói đối tượng hóa đơn thành chuỗi JSON
    const jsonPayload = JSON.stringify(bookingObj);

    // 5. Truy xuất tổng tiền thanh toán để hiển thị trên thông báo xác nhận
    const confirmedTotal = jsonPayload.totalAmount;

    return {
        jsonResult: jsonPayload,
        confirmedTotal: confirmedTotal
    };
}

// --- Kiểm thử chạy thử với dữ liệu mẫu ---
const sampleBooking = {
    bookingId: "BK-2026-889",
    guestName: "Nguyen Van A",
    roomPrice: 1000000,
    tempSecurityCode: "CVC-9948"
};

const result = processBookingInvoice(sampleBooking, true);
console.log("Chuỗi JSON hóa đơn:", result.jsonResult);
console.log("Tổng tiền xác nhận:", result.confirmedTotal);
console.log("Kiểm tra key tempSecurityCode còn tồn tại không?:", sampleBooking.hasOwnProperty("tempSecurityCode"));
```

#

## **4. Yêu cầu đầu ra**

#### **Phần 1: Phân tích & Báo cáo kiểm thử (Test Case Report)**
Học viên tiến hành chạy thử mã nguồn, phân tích nguyên nhân gây ra lỗi hiển thị `undefined` và lỗi sót thuộc tính bảo mật. Sau đó, hoàn thiện bảng báo cáo kiểm thử bên dưới vào bài nộp. 

*Lưu ý:* Hàng STT 1 đã được làm mẫu hoàn chỉnh, học viên bắt buộc phải tự trace code và điền đầy đủ thông tin cho Hàng STT 2 và Hàng STT 3 (thay thế các dấu `...`).

<table border="1" style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: center;">STT</th>
      <th style="padding: 8px; text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="padding: 8px; text-align: left;">Đầu ra thực tế bị lỗi (Buggy Output)</th>
      <th style="padding: 8px; text-align: left;">Đầu ra mong đợi (Expected Output)</th>
      <th style="padding: 8px; text-align: center;">Dòng code gây lỗi</th>
      <th style="padding: 8px; text-align: left;">Phân tích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; text-align: center;">1</td>
      <td style="padding: 8px;"><code>bookingObj</code> = { roomPrice: 1000000, tempSecurityCode: "CVC-9948" }<br><code>isEarlyCheckin</code> = true</td>
      <td style="padding: 8px;"><code>confirmedTotal</code> = undefined<br><code>hasOwnProperty("tempSecurityCode")</code> = true</td>
      <td style="padding: 8px;"><code>confirmedTotal</code> = 1300000<br><code>hasOwnProperty("tempSecurityCode")</code> = false</td>
      <td style="padding: 8px; text-align: center;">Dòng 16 & Dòng 22</td>
      <td style="padding: 8px;">- Dòng 16: Gán <code>undefined</code> chỉ làm rỗng giá trị chứ không xóa thuộc tính khỏi memory đối tượng.<br>- Dòng 22: Truy cập thuộc tính <code>totalAmount</code> trực tiếp trên chuỗi JSON string dẫn đến trả về <code>undefined</code>.</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">2</td>
      <td style="padding: 8px;"><code>bookingObj</code> = { roomPrice: 2000000, tempSecurityCode: "CVC-1234" }<br><code>isEarlyCheckin</code> = false</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">3</td>
      <td style="padding: 8px;"><code>bookingObj</code> = { roomPrice: 1500000, tempSecurityCode: "CVC-5555" }<br><code>isEarlyCheckin</code> = true</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px; text-align: center;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa đổi và hoàn thiện mã nguồn**
Viết lại hàm `processBookingInvoice(bookingObj, isEarlyCheckin)` đảm bảo tuân thủ các yêu cầu sau:
1. Thao tác xóa dữ liệu: Sử dụng đúng toán tử `delete` để xóa hoàn toàn thuộc tính `tempSecurityCode` khỏi đối tượng hóa đơn trước khi thực hiện đóng gói chuỗi JSON.
2. Xử lý dữ liệu JSON: Để lấy được `confirmedTotal` chính xác từ dữ liệu đã đóng gói, phải giải mã chuỗi JSON `jsonPayload` thông qua `JSON.parse()` rồi mới truy cập thuộc tính `totalAmount` trên đối tượng đã khôi phục.
3. Kiểm chuẩn dữ liệu đầu vào (Validation):
   - Nếu `bookingObj` bị `null`, `undefined` hoặc không phải kiểu đối tượng (`typeof bookingObj !== "object"`), ném lỗi `throw new Error("Dữ liệu hóa đơn không hợp lệ")`.
   - Nếu `roomPrice` bị thiếu, không phải kiểu số hoặc có giá trị `<= 0`, ném lỗi `throw new Error("Giá phòng phải là một số dương lớn hơn 0")`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex6`.
    Ví dụ: `HNKS25CNTT1_Core_Session12_Ex6`