#

# <center>[Vận dụng nâng cao 3] Quản Lý Chuẩn Hóa và Đóng Gói Dữ Liệu Đặt Phòng Khách Sạn</center>

### **1. Mục tiêu**
*   **Kiến thức:** Hiểu và làm chủ các thao tác nâng cao với Object Literal trong JavaScript ES6+ bao gồm truy cập động bằng Bracket Notation, cập nhật dữ liệu, xóa thuộc tính bằng toán tử `delete`, và quy trình mã hóa/giải mã dữ liệu dạng chuỗi JSON (`JSON.stringify`, `JSON.parse`).
*   **Kỹ năng:** Phân tích bối cảnh dữ liệu thô trong nghiệp vụ đặt phòng du lịch, xây dựng báo cáo thiết kế giải pháp xử lý dữ liệu nhạy cảm, vẽ sơ đồ luồng quy trình làm sạch đối tượng và đóng gói chuỗi JSON chuẩn mực.
*   **Thái độ:** Rèn luyện tư duy lập trình an toàn thông tin (Data Sanitization), cẩn trọng trong việc bảo mật dữ liệu khách hàng và tối ưu hóa bộ nhớ ứng dụng web Frontend.

---

### **2. Bối cảnh & Vấn đề**

Trong nền tảng đặt phòng trực tuyến Agoda / Traveloka, khi khách hàng thực hiện thao tác hoàn tất đơn đặt phòng (`BookingReservation`), giao diện ứng dụng web thu thập dữ liệu từ nhiều nguồn khác nhau (thông tin người đặt, thời gian check-in, số lượng khách, mã token thanh toán tạm thời và ghi chú nội bộ của hệ thống). Dữ liệu thô ban đầu nhận được chứa các key động chứa ký tự đặc biệt như `"check-in-hour"`, `"extra-services"`, cùng các dữ liệu nhạy cảm cần bảo mật trước khi xuất hóa đơn dịch vụ (`ServiceInvoice`) hoặc chuyển tới bộ phận lưu trữ.Nếu không lọc bỏ các thuộc tính nhạy cảm như `securityCode` hay `tempToken` mà chỉ gán giá trị `undefined`, dữ liệu khi đóng gói và hiển thị vẫn gây lãng phí tài nguyên bộ nhớ và có nguy cơ rò riri thông tin. Bạn được giao nhiệm vụ xây dựng module Frontend bằng JavaScript thuần để tự động hóa quy trình: tiếp nhận đối tượng thô, cập nhật phụ phí nghiệp vụ, làm sạch các key dư thừa/nhạy cảm, và đóng gói dữ liệu thành chuỗi JSON an toàn.

---

### **3. Quy tắc nghiệp vụ**

Hệ thống cần áp dụng chính xác các quy tắc tính toán và xử lý thuộc tính trên đối tượng đặt phòng như sau:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: left;">Quy tắc Nghiệp vụ</th>
      <th style="text-align: left;">Chi tiết Thao tác Dữ liệu</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td><strong>Nhận phòng sớm (Early Check-in)</strong></td>
      <td>Nếu thuộc tính động <code>"check-in-hour"</code> trong đối tượng có giá trị nhỏ hơn 12 (trước 12:00 trưa), tính phụ thu 30% trên đơn giá 1 đêm (<code>roomPricePerNight</code>). Giá trị này được gán vào thuộc tính mới <code>earlyCheckInFee</code>. Trái lại, gán bằng 0.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td><strong>Phụ thu người vượt chuẩn</strong></td>
      <td>Số trẻ em dưới 6 tuổi (<code>childrenUnder6</code>) được miễn phí. Nếu số lượng người lớn <code>adultsCount</code> vượt quá sức chứa tiêu chuẩn <code>standardCapacity</code>, mỗi người vượt chuẩn bị phụ thu 200,000 VND/đêm. Tổng tiền phụ thu người phát sinh ghi nhận vào thuộc tính <code>extraGuestFee</code>.</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td><strong>Làm sạch dữ liệu nhạy cảm (Sanitization)</strong></td>
      <td>Bắt buộc xóa bỏ hoàn toàn các thuộc tính nhạy cảm/tạm thời: <code>securityCode</code>, <code>tempToken</code>, và <code>internalNote</code> khỏi đối tượng bằng toán tử <code>delete</code>. Tuyệt đối không gán giá trị <code>undefined</code> hoặc <code>null</code>.</td>
    </tr>
    <tr>
      <td style="text-align: center;">4</td>
      <td><strong>Tổng tiền thanh toán</strong></td>
      <td>Tính tổng tiền thanh toán <code>totalPayment</code> = <code>(roomPricePerNight * nightCount) + earlyCheckInFee + extraGuestFee</code>. Sau đó thêm thuộc tính <code>isPaid: false</code> để quản lý trạng thái.</td>
    </tr>
    <tr>
      <td style="text-align: center;">5</td>
      <td><strong>Đóng gói & Giải mã JSON</strong></td>
      <td>Đóng gói đối tượng hoàn chỉnh sang chuỗi JSON (<code>JSON.stringify</code>). Xây dựng hàm kiểm định cho phép nhận vào chuỗi JSON, giải mã ngược lại (<code>JSON.parse</code>) và kiểm tra nếu thiếu một trong các thuộc tính bắt buộc (<code>bookingId</code>, <code>roomCode</code>, <code>totalPayment</code>) thì thông báo lỗi nghiệp vụ.</td>
    </tr>
  </tbody>
</table>

---

### **4. Yêu cầu bài toán**

Sinh viên thực hiện bài tập theo 2 phần độc lập:

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Analysis & Design Report)**
1.  **Phân tích Input / Output:**
    *   Xác định cấu trúc dữ liệu đầu vào của đối tượng `BookingReservation` thô (bao gồm các thuộc tính kiểu số, chuỗi, boolean, và các key chứa dấu gạch ngang).
    *   Xác định kiểu dữ liệu của chuỗi JSON đầu ra sau khi đóng gói.
2.  **Đề xuất giải pháp kỹ thuật:**
    *   Trình bày lý do tại sao phải dùng toán tử `delete` thay vì gán `undefined`.
    *   Phân tích trường hợp khi nào bắt buộc phải dùng Bracket Notation `object["key-name"]` thay vì Dot Notation `object.keyName`.
3.  **Sơ đồ luồng quy trình (Mermaid Flowchart):**
    *   Vẽ sơ đồ luồng mô tả chính xác quy trình từ khi nhận object thô đến khi tạo ra chuỗi JSON.
    *   **Yêu cầu tuân thủ chuẩn hình dạng Mermaid:**
        *   Bắt đầu/Kết thúc: Hình bo tròn `([Nội dung])`.
        *   Đầu vào/Đầu ra (I/O): Hình bình hành `[/Nội dung/]`.
        *   Kiểm tra điều kiện (Decision): Hình thoi `Kiểm tra điều kiện?`.
        *   Thao tác/Xử lý/Tính toán (Process): Hình chữ nhật `["Nội dung"]`.

#### **Phần 2: Lập trình Logic Nghiệp vụ & Kiểm chuẩn (Implementation & Error Guards)**
 Viết mã nguồn JavaScript thuần (ES6+) giải quyết bài toán:
1.  Khai báo một Object thô chứa đầy đủ thông tin mẫu của đơn đặt phòng khách sạn.
2.  Thực hiện cập nhật các thuộc tính động, tính phụ thu check-in sớm và phụ thu khách phát sinh.
3.  Sử dụng toán tử `delete` để làm sạch toàn bộ các thuộc tính nhạy cảm.
4.  Chuyển đổi đối tượng hoàn chỉnh sang chuỗi JSON và in kết quả ra màn hình Console.
5.  Viết hàm `restoreAndValidateBooking(jsonString)` thực hiện giải mã chuỗi JSON và kiểm tra tính đầy đủ của các thuộc tính bắt buộc, trả về kết quả hoặc thông báo lỗi thích hợp nếu chuỗi JSON không hợp lệ.

---

### **5. Yêu cầu nộp bài**

Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai trong cùng 1 tệp hoặc thư mục bài làm.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex9`.
    *   *Ví dụ:* `HNKS25CNTT1_Core_Session12_Ex9`