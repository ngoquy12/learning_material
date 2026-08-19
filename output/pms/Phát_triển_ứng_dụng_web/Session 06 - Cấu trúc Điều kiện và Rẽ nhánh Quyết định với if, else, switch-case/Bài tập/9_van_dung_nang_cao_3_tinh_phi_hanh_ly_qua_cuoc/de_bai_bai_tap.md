# <center>[Vận dụng nâng cao 3] Tính Phí Hành Lý Quá Cước Và Phụ Phí Chọn Ghế Máy Bay</center>

### **1. Mục tiêu**
*   Vận dụng kết hợp thành thạo cấu trúc điều kiện `if...else if...else`, cấu trúc rẽ nhánh nhiều trường hợp `switch-case` và toán tử ba ngôi (Ternary Operator) trong JavaScript (ES6+).
*   Phân tích và giải quyết bài toán nghiệp vụ phức tạp thuộc hệ thống Check-in hàng không (`AIRLINE_CHECKIN`): Tính cước dồn hành lý quá khổ xách tay vào ký gửi, tra cứu hạn mức theo hạng vé, tính phụ phí dịch vụ chỗ ngồi và phân loại trạng thái hóa đơn thanh toán.
*   Rèn luyện tư duy phân tích hệ thống độc lập: Tự xác định I/O, tự thiết kế sơ đồ luồng quy trình (Flowchart) hoặc mã giả (Pseudocode), rà soát bẫy dữ liệu biên trước khi viết mã nguồn.

### **2. Bối cảnh & Vấn đề**
Tại các quầy làm thủ tục bay (Airport Check-in Desk) của hãng hàng không Vietjet / Vietnam Airlines, hệ thống máy tính tự động đóng vai trò cốt lõi trong việc xác nhận thông tin vé, cân đo hành lý và tính toán phụ phí phát sinh trước khi phát hành thẻ lên tàu bay (Boarding Pass).

Khi hành khách làm thủ tục, nhân viên check-in nhập các thông số bao gồm: hạng vé đăng ký, trọng lượng hành lý xách tay thực tế, trọng lượng hành lý ký gửi thực tế, vị trí ghế ngồi mong muốn và trạng thái ưu tiên thủ tục.

Hệ thống cần xử lý luồng tính phí với nhiều quy tắc ràng buộc chéo:
*   Hành lý xách tay vượt quá hạn mức cabin (7 kg) phải tự động chuyển phần trọng lượng thừa sang cộng dồn vào hành lý ký gửi.
*   Mỗi hạng vé (Eco, Deluxe, Business) áp dụng hạn mức ký gửi miễn phí khác nhau và chính sách ưu đãi giá chọn vị trí ghế khác nhau.
*   Trường hợp tổng hành lý ký gửi sau cộng dồn vượt quá ngưỡng cồng kềnh an toàn (50 kg), hệ thống phải tự động tính thêm phụ phí xử lý hàng quá khổ đặc biệt.
*   Dịch vụ ưu tiên làm thủ tục nhanh cần được kiểm tra để tránh tính phí trùng lặp đối với khách hàng hạng Business.

### **3. Quy tắc nghiệp vụ**

Hệ thống yêu cầu áp dụng chính xác các quy tắc tính toán sau:

1. **Quy tắc Hành lý Xách tay & Cộng dồn Quá cước:**
   *   Hạn mức miễn phí hành lý xách tay tiêu chuẩn: Tối đa `7 kg` áp dụng cho tất cả hạng vé.
   *   Nếu trọng lượng xách tay thực tế (`carryOnWeight`) > `7 kg`: Phần trọng lượng vượt quá (`carryOnWeight - 7`) sẽ tự động được cộng dồn vào trọng lượng hành lý ký gửi thực tế (`checkedWeight`) trước khi tính phí ký gửi.

2. **Hạn mức Miễn phí & Phí Hành lý Ký gửi:**
   *   Hạn mức ký gửi miễn phí dựa trên mã hạng vé (`ticketClassCode`):
       *   Mã `1` (Hạng Eco - Phổ thông): `0 kg` miễn phí.
       *   Mã `2` (Hạng Deluxe - Phổ thông đặc biệt): `20 kg` miễn phí.
       *   Mã `3` (Hạng Business - Thương gia): `40 kg` miễn phí.
   *   Công thức tính phí ký gửi:
       *   `tổngKýGửiTínhToán` = `checkedWeight` + `phầnXáchTayVượtNgưỡng` (nếu có).
       *   `sốKgQuáCước` = `tổngKýGửiTínhToán` - `hạnMứcMiễnPhí`.
       *   Nếu `sốKgQuáCước` > 0: Phí quá cước hành lý = `sốKgQuáCước` * `50.000 VNĐ/kg`. Ngược lại phí = `0 VNĐ`.
       *   [Phụ phí cồng kềnh]: Nếu `tổngKýGửiTínhToán` > `50 kg`, cộng thêm khoản phí cố định `500.000 VNĐ` (Phí dịch vụ hàng hóa cồng kềnh đặc biệt).

3. **Bảng Phụ phí Chọn Vị trí Ghế ngồi (`seatSelectionType` & `ticketClassCode`):**
   *   Mã vị trí ghế mong muốn (`seatSelectionType`): `1` (Tiêu chuẩn), `2` (Chân rộng Extra Legroom), `3` (Cửa thoát hiểm Emergency Exit).
   *   Áp dụng cấu trúc `switch-case` theo `ticketClassCode` để tính phí chọn ghế:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">Mã Hạng Vé (ticketClassCode)</th>
      <th style="text-align: center;">Loại 1: Tiêu chuẩn</th>
      <th style="text-align: center;">Loại 2: Chân rộng</th>
      <th style="text-align: center;">Loại 3: Thoát hiểm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1 (Hạng Eco)</strong></td>
      <td style="text-align: right;">30.000 VNĐ</td>
      <td style="text-align: right;">80.000 VNĐ</td>
      <td style="text-align: right;">150.000 VNĐ</td>
    </tr>
    <tr>
      <td><strong>2 (Hạng Deluxe)</strong></td>
      <td style="text-align: right;">0 VNĐ (Miễn phí)</td>
      <td style="text-align: right;">50.000 VNĐ</td>
      <td style="text-align: right;">100.000 VNĐ</td>
    </tr>
    <tr>
      <td><strong>3 (Hạng Business)</strong></td>
      <td style="text-align: right;">0 VNĐ (Miễn phí)</td>
      <td style="text-align: right;">0 VNĐ (Miễn phí)</td>
      <td style="text-align: right;">0 VNĐ (Miễn phí)</td>
    </tr>
  </tbody>
</table>

4. **Dịch vụ Ưu tiên Check-in & Phân loại Trạng thái:**
   *   Trạng thái mua dịch vụ ưu tiên check-in nhanh (`isPriorityCheckin = true`):
       *   Nếu khách thuộc Hạng Business (Mã 3): Phụ phí ưu tiên = `0 VNĐ` (vì đặc quyền đã có sẵn).
       *   Nếu khách thuộc Hạng Eco hoặc Deluxe (Mã 1, 2): Tính phụ phí `100.000 VNĐ`.
   *   Toán tử ba ngôi gán nhãn trạng thái check-in (`checkinStatus`):
       *   Nếu `tổngPhụPhí === 0` -> Nhãn: `"Check-in Hoàn tất - Miễn phụ thu"`
       *   Ngược lại -> Nhãn: `"Check-in Phụ thu - Chờ thanh toán"`

5. **Ràng buộc Kiểm chuẩn Dữ liệu (Input Validation):**
   *   `carryOnWeight` và `checkedWeight` phải là số thực/số nguyên không âm (`>= 0`).
   *   `ticketClassCode` phải thuộc tập giá trị hợp lệ `{1, 2, 3}`.
   *   `seatSelectionType` phải thuộc tập giá trị hợp lệ `{1, 2, 3}`.
   *   Nếu phát hiện bất kỳ dữ liệu nào không hợp lệ, hệ thống phải ngắt tính toán và xuất thông báo lỗi định danh rõ ràng.

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Kỹ sư Lập trình Logic Front-End/Core, thực hiện 2 phần việc bắt buộc sau:

#### **Phần 1: Báo cáo Phân tích Logic & Sơ đồ Luồng (Analysis & Design Report)**
1. **Phân tích I/O:** Xác định danh sách tham số đầu vào (tên biến, mô tả, kiểu dữ liệu) và các giá trị đầu ra cần in ra màn hình.
2. **Giải pháp Logic:** Mô tả chi tiết phương pháp tính toán dồn cước hành lý, logic rẽ nhánh tra cứu bảng phí ghế và logic gán trạng thái hóa đơn.
3. **Sơ đồ luồng (Flowchart):** Thiết kế sơ đồ luồng quy trình bằng cú pháp Mermaid tuân thủ đúng chuẩn ký hình (Terminator, Input/Output, Decision, Process).

#### **Phần 2: Triển khai Mã nguồn & Xử lý Ngoại lệ (Implementation)**
1. Viết chương trình bằng JavaScript (ES6+) hoàn chỉnh xử lý kịch bản trên, chạy thành công trong môi trường Node.js hoặc Cursor AI IDE.
2. Khai báo biến/hằng số hoàn toàn bằng tiếng Anh (`const`, `let`), mã nguồn sạch, căn lề chuẩn 2 spaces.
3. Áp dụng đúng cấu trúc điều kiện:
   *   `if...else if...else` cho việc validate đầu vào, tính cước quá cân và phụ phí cồng kềnh.
   *   `switch-case` cho việc tra cứu phụ phí chọn ghế theo hạng vé.
   *   Toán tử ba ngôi (`? :`) cho việc gán nhãn trạng thái thanh toán `checkinStatus`.
4. Xử lý triệt để các bẫy dữ liệu biên (cân nặng âm, sai mã hạng vé, sai mã chọn ghế).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex9`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex9`
