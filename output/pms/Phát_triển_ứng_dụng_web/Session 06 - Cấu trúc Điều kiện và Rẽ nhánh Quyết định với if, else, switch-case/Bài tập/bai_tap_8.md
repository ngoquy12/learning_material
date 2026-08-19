# <center>[Vận dụng nâng cao 2] Triển khai logic kiểm tra check-in và tính toán phụ phí hành lý hàng không</center>

### **1. Mục tiêu**
*   **Tư duy phân tích nghiệp vụ:** Rèn luyện khả năng phân tích các điều kiện nghiệp vụ thực tế nhiều tầng phức tạp trong hệ thống hàng không (hạng vé, cấp độ hội viên, trọng lượng hành lý quá cước, dịch vụ ưu tiên).
*   **Vận dụng kỹ thuật điều kiện:** Sử dụng linh hoạt và tối ưu kết hợp giữa cấu trúc rẽ nhánh `if...else if...else`, câu lệnh nhiều trường hợp `switch-case` và toán tử ba ngôi `ternary operator` nhằm xử lý sạch đẹp mã nguồn.
*   **Xử lý trường hợp biên:** Thiết kế logic xử lý dữ liệu ngoại lệ, các điểm chặn hạn mức an toàn chuyến bay và tính toán đơn giá cước lũy tiến theo từng trường hợp đặc thù.

---

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quầy thủ tục tự động (Kiosk Check-in) của hãng hàng không Vietjet / Vietnam Airlines, hệ thống cần tính toán chính xác quyền lợi hành lý miễn phí và các khoản phụ phí phát sinh cho hành khách trước khi phát hành thẻ lên máy bay (Boarding Pass).

Hành khách thực hiện thủ tục nhập các thông tin cá nhân bao gồm: hạng vé đã đặt, cấp độ hội viên thường xuyên, cân nặng hành lý xách tay thực tế, cân nặng hành lý ký gửi thực tế, và tùy chọn đăng ký dịch vụ lối đi ưu tiên (Priority Boarding). Nếu cân nặng hành lý xách tay vượt quá quy định, toàn bộ số kg dư thừa phải chuyển sang tính chung vào hành lý ký gửi. Ngoài ra, nếu tổng hành lý ký gửi vượt quá số kg an toàn tối đa cho một hành khách, chuyến bay sẽ từ chối vận chuyển hành lý đó dưới dạng thông thường.

Hệ thống yêu cầu bạn phát triển một module xử lý trung tâm bằng JavaScript Vanilla (ES6+) để tự động xác định hạn mức hành lý, tính toán tổng chi phí phụ thu, và đưa ra quyết định chấp nhận check-in cho hành khách.---

### **3. Quy tắc nghiệp vụ**

Hệ thống áp dụng các quy tắc phân định quyền lợi và phí dịch vụ như sau:

#### **A. Quy tắc Hành lý Xách tay (Hand Baggage)**
1.  Hạn mức tiêu chuẩn miễn phí: `7 kg` cho tất cả các loại vé.
2.  Đặc quyền hội viên: Hạng hội viên `"GOLD"` và `"PLATINUM"` được cộng thêm `3 kg` hạn mức miễn phí xách tay (tổng cộng `10 kg`). Các hạng khác (`"STANDARD"`, `"SILVER"`) giữ nguyên `7 kg`.
3.  Xử lý vượt hạn mức: Nếu trọng lượng hành lý xách tay thực tế lớn hơn hạn mức miễn phí, số kg vượt quá sẽ tự động chuyển sang cộng dồn vào trọng lượng hành lý ký gửi thực tế (`checkedBaggageWeight`). Hành lý xách tay hợp lệ còn lại giữ đúng hạn mức tối đa cho phép.

#### **B. Quy tắc Hành lý Ký gửi (Checked Baggage)**
1.  Hạn mức miễn phí tiêu chuẩn theo hạng vé (`ticketClass`):
    *   `"ECO"`: `0 kg` miễn phí.
    *   `"DELUXE"`: `20 kg` miễn phí.
    *   `"BUSINESS"`: `30 kg` miễn phí.
2.  Hạn mức bổ sung theo hạng hội viên (`passengerTier`):
    *   `"SILVER"`: Được tặng thêm `5 kg`.
    *   `"GOLD"`: Được tặng thêm `10 kg`.
    *   `"PLATINUM"`: Được tặng thêm `15 kg`.
    *   `"STANDARD"`: Không được tặng thêm (`0 kg`).
    *(Tổng hạn mức ký gửi miễn phí = Hạn mức theo hạng vé + Hạn mức bổ sung hội viên)*.
3.  Đơn giá phạt cước quá cân (`excessBaggageFee`):
    *   Nếu số kg ký gửi vượt quá tổng hạn mức miễn phí, phần trọng lượng vượt cước được tính đơn giá tiêu chuẩn: **50.000 VNĐ / kg**.
    *   [ĐẶC BIỆT]: Nếu tổng hành lý ký gửi thực tế (sau khi đã cộng dồn hành lý xách tay dư) vượt quá **40 kg**, toàn bộ số kg quá cước vượt hạn mức miễn phí sẽ bị áp đơn giá phạt tải trọng nặng lũy tiến: **75.000 VNĐ / kg** (thay cho đơn giá tiêu chuẩn 50.000 VNĐ / kg).

#### **C. Quy tắc Phụ phí Dịch vụ Ưu tiên (Priority Boarding)**
*   Hạng vé `"BUSINESS"` hoặc hội viên `"PLATINUM"` được miễn phí dịch vụ lối đi ưu tiên (**0 VNĐ**).
*   Các trường hợp còn lại: Nếu đăng ký dịch vụ (`isPriorityBoarding === true`), phụ thu **100.000 VNĐ**.

#### **D. Quy tắc Giới hạn An toàn & Trạng thái Check-in**
*   Giới hạn ký gửi tối đa tuyệt đối cho 1 hành khách là **50 kg** (sau khi đã dồn kg xách tay vượt mức).
*   Nếu tổng hành lý ký gửi thực tế `> 50 kg`: Trạng thái duyệt check-in là `"REJECTED_OVERWEIGHT"` và phí ký gửi quá cước được giữ nguyên để thông báo.
*   Nếu tổng hành lý ký gửi thực tế `<= 50 kg`: Trạng thái duyệt check-in là `"APPROVED"`.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: left;">Hạng vé (`ticketClass`)</th>
      <th style="text-align: left;">Hạn mức vé</th>
      <th style="text-align: left;">Hội viên (`passengerTier`)</th>
      <th style="text-align: left;">Hạn mức cộng thêm</th>
      <th style="text-align: left;">Ưu tiên Boarding</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>ECO</code></td>
      <td>0 kg</td>
      <td><code>STANDARD</code></td>
      <td>+0 kg</td>
      <td>100.000 VNĐ (Nếu chọn)</td>
    </tr>
    <tr>
      <td><code>DELUXE</code></td>
      <td>20 kg</td>
      <td><code>SILVER</code></td>
      <td>+5 kg</td>
      <td>100.000 VNĐ (Nếu chọn)</td>
    </tr>
    <tr>
      <td><code>BUSINESS</code></td>
      <td>30 kg</td>
      <td><code>GOLD</code></td>
      <td>+10 kg</td>
      <td>Miễn phí (0 VNĐ)</td>
    </tr>
    <tr>
      <td>-</td>
      <td>-</td>
      <td><code>PLATINUM</code></td>
      <td>+15 kg (+3kg xách tay)</td>
      <td>Miễn phí (0 VNĐ)</td>
    </tr>
  </tbody>
</table>

---

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Lập trình viên Front-end / Logic Engine triển khai bài tập theo đúng 2 phần sau:

#### **Phần 1: Báo cáo Phân tích Logic & Sơ đồ Quy trình (Analysis & Design)**
1.  **Phân tích Input / Output:**
    *   Liệt kê rõ ràng danh sách tham số đầu vào (tên biến, kiểu dữ liệu JavaScript, miền giá trị).
    *   Liệt kê danh sách kết quả đầu ra (tổng tiền phụ phí hành lý, phí dịch vụ ưu tiên, tổng chi phí thanh toán cuối cùng, trạng thái check-in, thông điệp phản hồi).
2.  **Đề xuất Giải pháp Logic & Sơ đồ Luồng:**
    *   Mô tả giải pháp rẽ nhánh bằng cách phối hợp `if...else`, `switch-case` và toán tử ba ngôi `ternary operator`.
    *   Vẽ sơ đồ quy trình xử lý Mermaid Flowchart tuân thủ đúng 5 chuẩn hình dạng:
        *   `([Bắt đầu / Kết thúc])`: Hình Oval (Stadium).
        *   `[/Đầu vào / Đầu ra/]` hình Hình bình hành (Parallelogram).
        *   `Kiểm tra điều kiện?` hình Thoi (Diamond).
        *   `["Thực hiện hành động / Tính toán"]` hình Chữ nhật (Rectangle).
        *   Mũi tên luồng dữ liệu `-->` hoặc `-->|Đúng/Sai|`.

#### **Phần 2: Triển khai Mã nguồn JavaScript Vanilla (Implementation)**
*   Viết đoạn mã JavaScript ES6+ hoàn chỉnh khai báo các thông tin đầu vào mẫu để kiểm thử logic.
*   Yêu cầu bắt buộc về mặt cú pháp trong code:
    *   Sử dụng cấu trúc `switch-case` để phân định hạn mức ký gửi miễn phí ban đầu theo `ticketClass` (có xử lý trường hợp `default` cho hạng vé không hợp lệ).
    *   Sử dụng khối `if...else if...else` để kiểm tra điều kiện hành lý xách tay quá cân và tính toán hạn mức cộng thêm của hội viên `passengerTier`.
    *   Sử dụng **Toán tử Ba ngôi (Ternary Operator)** để tính phí dịch vụ `isPriorityBoarding` và xác định trạng thái chấp nhận check-in (`"APPROVED"` hoặc `"REJECTED_OVERWEIGHT"`).
    *   Bắt bẫy dữ liệu đầu vào âm (ví dụ: trọng lượng kg < 0) hoặc sai định dạng bằng cách in thông báo lỗi rõ ràng.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex8`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 06_Ex8`
