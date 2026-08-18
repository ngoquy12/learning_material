#

# <center>[Vận dụng cơ bản 6] Sửa lỗi tính phí hành lý ký gửi quá cước Vietjet</center>

### **1. Mục tiêu**
*   **Phân tích & Phát hiện lỗi trôi lệnh (Fall-through):** Đọc hiểu và truy vết mã nguồn (code tracing) để tìm nguyên nhân gây lỗi khi sử dụng cấu trúc rẽ nhánh `switch-case` trong JavaScript.
*   **Sửa lỗi logic rẽ nhánh:** Bổ sung đúng từ khóa ngắt nhánh `break` và câu lệnh điều kiện `if-else` để đảm bảo luồng điều khiển của chương trình hoạt động chính xác theo quy tắc nghiệp vụ.
*   **Xử lý tính toán hạn mức & Phí vượt cước:** Áp dụng công thức tính toán và ràng buộc giá trị không âm cho chi phí hành lý ký gửi tại quầy check-in sân bay.

---

### **2. Bối cảnh & Vấn đề**
Trong hệ thống làm thủ tục check-in tự động của hãng hàng không Vietjet Air, mỗi khách hàng khi ký gửi hành lý tại quầy sẽ được kiểm tra hạn mức miễn phí dựa trên hạng vé đã đặt:
1.  **Hạng Eco (mã `1`):** Hạn mức ký gửi miễn phí là **0 kg** (hành khách chỉ có 7kg xách tay, mọi hành lý ký gửi đều tính phí).
2.  **Hạng Deluxe (mã `2`):** Hạn mức ký gửi miễn phí là **20 kg**.
3.  **Hạng Business (mã `3`):** Hạn mức ký gửi miễn phí là **30 kg**.

Nếu trọng lượng hành lý ký gửi thực tế (`baggageWeight`) lớn hơn hạn mức miễn phí (`freeAllowance`), số kg vượt cước sẽ bị phạt với mức giá cố định **50.000 VNĐ/kg**.

**Sự cố thực tế:**
Bộ phận quầy thủ tục sân bay phản ánh một sự cố nghiêm trọng: Nhiều hành khách mua vé hạng Eco (mã `1`) mang theo 12 kg hành lý ký gửi, nhưng hệ thống lại in ra phiếu thông báo hạng vé là "Deluxe hạn mức miễn phí 20 kg và tính phí quá cước là **0 VNĐ**. Lỗi này khiến hãng hàng không bị thất thu chi phí dịch vụ ký gửi tại sân bay.---

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã JavaScript xử lý logic tính phí ký gửi hành lý đang chạy trên hệ thống:```javascript
// Hệ thống tính phí hành lý ký gửi tại quầy check-in sân bay Vietjet
const ticketClassCode = 1; // Mã hạng vé (1: Eco, 2: Deluxe, 3: Business)
const baggageWeight = 12;  // Cân nặng hành lý ký gửi thực tế (kg)

let freeAllowance = 0;
let ticketClassName = '';

// Xác định tên hạng vé và hạn mức ký gửi miễn phí
switch (ticketClassCode) {
  case 1:
    ticketClassName = 'Eco';
    freeAllowance = 0;
    // Kiểm tra và thiết lập thông số hạng vé 1
  case 2:
    ticketClassName = 'Deluxe';
    freeAllowance = 20;
    break;
  case 3:
    ticketClassName = 'Business';
    freeAllowance = 30;
    break;
  default:
    ticketClassName = 'Không hợp lệ';
    freeAllowance = 0;
    break;
}

// Tính toán khối lượng hành lý vượt quá hạn mức
let excessWeight = baggageWeight - freeAllowance;

// Đảm bảo số kg quá cước không bị âm
if (excessWeight < 0) {
  excessWeight = 0;
}

// Tính tổng phí phạt quá cước (50.000 VNĐ / kg quá cước)
const excessFee = excessWeight * 50000;

// Hiển thị kết quả kiểm tra
console.log("Hạng vé xác nhận:", ticketClassName);
console.log("Hạn mức miễn phí:", freeAllowance, "kg");
console.log("Hành lý vượt cước:", excessWeight, "kg");
console.log("Phí phạt quá cước phải thu:", excessFee, "VNĐ");
```

---

### **4. Yêu cầu bài toán**

#### **Phần 1: Tracing Code & Lập Báo cáo Test Case (Bắt buộc)**
Học viên tiến hành chạy thử đoạn mã trên với các trường hợp đầu vào khác nhau, tìm ra dòng mã gây lỗi và hoàn thành bảng báo cáo Test Case sau vào bài nộp tự luận.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: left;">Đầu vào (Input)</th>
      <th style="text-align: left;">Đầu ra thực tế (Buggy Output)</th>
      <th style="text-align: left;">Đầu ra mong đợi (Expected Output)</th>
      <th style="text-align: left;">Dòng code gây lỗi</th>
      <th style="text-align: left;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td><code>ticketClassCode = 1</code><br><code>baggageWeight = 12</code></td>
      <td>
        Hạng vé: Deluxe<br>
        Hạn mức: 20 kg<br>
        Vượt cước: 0 kg<br>
        Phí phạt: 0 VNĐ
      </td>
      <td>
        Hạng vé: Eco<br>
        Hạn mức: 0 kg<br>
        Vượt cước: 12 kg<br>
        Phí phạt: 600.000 VNĐ
      </td>
      <td>Dòng 9 - 13 (Khối <code>case 1</code> thiếu <code>break;</code>)</td>
      <td>Khi <code>ticketClassCode = 1</code>, chương trình thực thi <code>case 1</code> nhưng do thiếu lệnh <code>break;</code> nên bị trôi lệnh (fall-through) sang <code>case 2</code>, dẫn đến <code>ticketClassName</code> bị ghi đè thành "Deluxe" và <code>freeAllowance</code> bị ghi đè thành 20.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td><code>ticketClassCode = 1</code><br><code>baggageWeight = 5</code></td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td><code>ticketClassCode = 2</code><br><code>baggageWeight = 25</code></td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa mã nguồn (Source Code Correction)**
Viết lại đoạn mã JavaScript trên để sửa triệt để lỗi logic rẽ nhánh, đảm bảo:
1. Xác định đúng tên hạng vé và hạn mức hành lý miễn phí tương ứng với từng `ticketClassCode`.
2. Trường hợp `ticketClassCode` không hợp lệ (không thuộc 1, 2, 3) phải in thông báo lỗi rõ ràng và không tiến hành tính phí phạt.
3. Tính chính xác số kg vượt cước và tổng phí phạt cần thu của hành khách.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo bảng Test Case và mã nguồn đã sửa hoàn chỉnh.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex6`.
    *   *Ví dụ:* `HNKS25CNTT1_Core_Session06_Ex6`