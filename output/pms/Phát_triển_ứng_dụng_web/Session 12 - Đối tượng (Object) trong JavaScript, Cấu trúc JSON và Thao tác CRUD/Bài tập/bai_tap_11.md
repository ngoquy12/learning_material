#

# <center>[Phân tích 2] Chuẩn hóa và Đóng gói Dữ liệu Đặt phòng Khách sạn Agoda</center>

### **1. Mục tiêu**
*   **Phân tích kỹ thuật đối tượng JavaScript (`Object Literal`):** Hiểu rõ cơ chế lưu trữ dạng key-value, truy cập thuộc tính tĩnh (`Dot Notation`), truy cập thuộc tính động hoặc chứa ký tự đặc biệt (`Bracket Notation`).
*   **Thao tác Mutation & Sanitization:** Thành thạo các thao tác thêm mới, cập nhật và xóa bỏ triệt để trường dữ liệu nhạy cảm bằng toán tử `delete` thay vì gán `undefined`.
*   **Chuyển đổi và Đóng gói JSON:** Thành thạo việc đóng gói dữ liệu đối tượng thành chuỗi `JSON.stringify()` và giải mã chuỗi `JSON.parse()` để đảm bảo tính toàn vẹn dữ liệu trong hệ thống đặt phòng khách sạn.
*   **Tư duy Phân tích & So sánh Trade-off:** Tự đề xuất các phương án xử lý cấu trúc dữ liệu, so sánh ưu nhược điểm về hiệu năng, bộ nhớ và độ sạch mã nguồn.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng khách sạn Agoda / Traveloka (`HOTEL_BOOKING`), khi người dùng hoàn tất các bước chọn phòng và dịch vụ trên giao diện web, hệ thống tiếp nhận một đối tượng dữ liệu thô (`bookingPayload`) chứa thông tin đơn hàng. Dữ liệu thô này thu thập từ nhiều nguồn khác nhau, bao gồm cả các mã token tạm thời của phiên làm việc (`tempToken`, `draftSessionId`), thời gian nhận phòng (`checkInHour`), giá phòng gốc (`roomPrice`), và các yêu cầu đặc biệt dưới dạng key đặc biệt chứa dấu gạch ngang (ví dụ `"special-request"`).

Trước khi gửi dữ liệu này sang hệ thống lưu trữ hoặc truyền qua mạng, kỹ sư Frontend cần xây dựng một mô-đun chuẩn hóa dữ liệu với các nhiệm vụ:
1.  **Tính toán phụ thu:** Nếu khách nhận phòng sớm trước 12:00 trưa, tự động tính phụ thu check-in sớm bằng 30% giá phòng gốc và cập nhật tổng tiền thanh toán (`totalAmount`).
2.  **Làm sạch dữ liệu (Sanitization):** Loại bỏ hoàn toàn các trường dữ liệu nhạy cảm hoặc tạm thời (`tempToken`, `draftSessionId`) khỏi đối tượng trước khi gửi đi. Việc chỉ gán `undefined` là một bẫy lỗi phổ biến vì key vẫn tồn tại trong đối tượng gốc gây tốn bộ nhớ.
3.  **Đóng gói và Phục hồi:** Chuyển đổi đối tượng đã làm sạch thành chuỗi JSON hợp lệ để truyền tải, đồng thời thực hiện giải mã thử nghiệm để xác minh tính chính xác của dữ liệu sau đóng gói.

### **3. Quy tắc nghiệp vụ**
Dữ liệu đối tượng đầu vào đại diện cho một đơn đặt phòng có cấu trúc ban đầu như sau:```javascript
const rawBookingData = {
  bookingId: "BK_AGODA_8892",
  guestName: "Nguyen Van A",
  roomPrice: 1500000,
  checkInHour: 10, // Khách check-in lúc 10 giờ sáng
  "special-request": "Phòng tầng cao, hướng biển",
  tempToken: "tmp_session_xyz_99812",
  draftSessionId: "draft_sess_4412"
};
```

Cần áp dụng các quy tắc nghiệp vụ sau để xử lý đối tượng:
1.  **Quy tắc Phụ thu Check-in sớm (`earlyCheckInFee`):**
    *   Nếu `checkInHour < 12`, phụ thu `earlyCheckInFee = roomPrice * 0.3` (30% giá phòng).
    *   Nếu `checkInHour >= 12`, phụ thu `earlyCheckInFee = 0`.
2.  **Quy tắc Tính Tổng tiền (`totalAmount`):**
    *   Thêm thuộc tính `totalAmount = roomPrice + earlyCheckInFee` vào đối tượng.
3.  **Quy tắc Xóa Dữ liệu tạm thời (Data Sanitization):**
    *   Loại bỏ hoàn toàn thuộc tính `tempToken` và `draftSessionId` bằng toán tử `delete`. Tuyệt đối không gán `undefined` hay `null`.
4.  **Quy tắc Truy cập Thuộc tính Đặc biệt:**
    *   Đọc thông tin yêu cầu đặc biệt từ trường `"special-request"` bằng ngoặc vuông `[]` (Bracket Notation) và in ra console dưới dạng thông điệp xác nhận.
5.  **Quy tắc Chuẩn hóa JSON:**
    *   Chuyển đổi đối tượng sau khi làm sạch thành chuỗi JSON tiêu chuẩn bằng `JSON.stringify()`.
    *   Thực hiện `JSON.parse()` chuỗi JSON vừa tạo để thu được đối tượng phục hồi (`restoredBooking`), sau đó in kiểm tra các trường dữ liệu trên đối tượng mới này.

### **4. Yêu cầu bài toán**

Học viên cần trình bày bài làm theo 3 phần bắt buộc sau:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Tự đề xuất ít nhất 2 giải pháp kỹ thuật khác nhau để xử lý, làm sạch và đóng gói dữ liệu đối tượng đặt phòng (ví dụ: Biến đổi trực tiếp trên đối tượng gốc - In-place Mutation vs Tạo đối tượng mới thông qua sao chép/tái cấu trúc thuộc tính sạch - Pure Object Transformation). Học viên tự nghiên cứu và mô tả chi tiết, đề bài không cung cấp sẵn các giải pháp.
*   Xây dựng bảng so sánh Trade-off trực quan giữa các giải pháp dựa trên 5 tiêu chí bắt buộc: Tốc độ xử lý (Time Complexity), Tiêu tốn bộ nhớ (Memory), Khả năng bảo trì (Maintainability), Độ rõ ràng của mã nguồn (Readability), Mức độ phù hợp với hệ thống thực tế (Suitability).

Sử dụng định dạng bảng HTML sau:
<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr>
      <th>Tiêu chí so sánh</th>
      <th>Giải pháp 1 (Mô tả tên GP)</th>
      <th>Giải pháp 2 (Mô tả tên GP)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Tốc độ xử lý (Time)</strong></td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td><strong>Tiêu tốn bộ nhớ (Memory)</strong></td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td><strong>Khả năng bảo trì (Maintainability)</strong></td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td><strong>Độ rõ ràng mã nguồn (Readability)</strong></td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td><strong>Mức độ phù hợp hệ thống (Suitability)</strong></td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Giải trình Lựa chọn và Mã giả / Lưu đồ thuật toán**
*   Lý giải nguyên nhân lựa chọn phương án tối ưu dựa trên phân tích đánh giá ở Phần 1.
*   Vẽ lưu đồ thuật toán (Mermaid Flowchart) mô tả chi tiết luồng dữ liệu từ đối tượng thô đến chuỗi JSON đã làm sạch.
*   **Quy chuẩn ký hiệu Mermaid bắt buộc:**
    *   Khối Bắt đầu / Kết thúc: Dùng hình bo tròn Stadium `([Bắt đầu])` / `([Kết thúc])`.
    *   Khối Nhập / Xuất dữ liệu (Input/Output): Dùng hình bình hành `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
    *   Khối Xử lý / Tính toán (Action/Process): Dùng hình chữ nhật `["Tính toán / Thao tác..."]`.
    *   Khối Rẽ nhánh điều kiện (Decision): Dùng hình thoi `Kiểm tra điều kiện?` kết hợp các nhánh `-->|Đúng|` và `-->|Sai|`.

#### **Phần 3: Triển khai Mã nguồn & Chặn lỗi biên (JavaScript Vanilla ES6+)**
*   Triển khai mã nguồn JavaScript hoàn chỉnh thực thi phương án đã chọn.
*   Đặt tên biến, thuộc tính bằng Tiếng Anh chuẩn camelCase. Các dòng ghi chú giải thích logic viết bằng Tiếng Việt có dấu.
*   Xử lý triệt để các trường hợp biên và bẫy lỗi thường gặp:
    *   Bẫy lỗi SyntaxError khi cố tình dùng Dot Notation cho key chứa gạch ngang (`booking."special-request"`).
    *   Bẫy lỗi gán `undefined` khiến thuộc tính tạm vẫn xuất hiện trong Object gốc.
    *   Kiểm tra tính an toàn khi parse chuỗi JSON không hợp lệ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex11`.
    Ví dụ: `HNKS25CNTT1_Core_Session12_Ex11`