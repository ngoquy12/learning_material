# <center>[Vận dụng cơ bản 1] Sửa Lỗi Tính Phí Hành Lý Quá Cước Tại Quầy Check-in</center>

### **1. Mục tiêu**
*   Hiểu và vận dụng cấu trúc rẽ nhánh điều kiện `if`, `else if`, `else` trong ngôn ngữ JavaScript (ES6+).
*   Rèn luyện kỹ năng đọc hiểu mã nguồn legacy (Code Tracing), phát hiện lỗi logic liên quan đến thứ tự kiểm tra biểu thức điều kiện.
*   Thực hành xây dựng bảng kịch bản kiểm thử (Test Case Report) và khắc phục lỗi mã nguồn trong hệ thống quản lý thủ tục bay (`AIRLINE_CHECKIN`).

### **2. Bối cảnh & Vấn đề**
Tại quầy làm thủ tục check-in tự động của hãng hàng không Vietjet / Vietnam Airlines, hệ thống máy tính tự động cân trọng lượng hành lý ký gửi của hành khách và tính toán phí cước phát sinh trước khi cấp thẻ lên tàu bay (Boarding Pass).

**Quy tắc nghiệp vụ tính phí hành lý ký gửi của hãng:**
1. Trọng lượng từ 0 kg đến 7 kg: Miễn phí cước hành lý (0 VNĐ).
2. Trọng lượng trên 7 kg đến 20 kg: Áp dụng phí cước tiêu chuẩn là **150.000 VNĐ**.
3. Trọng lượng trên 20 kg đến 35 kg: Áp dụng phí cước vượt mức là **350.000 VNĐ**.
4. Trọng lượng trên 35 kg: Áp dụng phí cước quá tải đặc biệt là **500.000 VNĐ** cộng thêm **50.000 VNĐ** cho mỗi kg vượt quá mốc 35 kg (Ví dụ: 37 kg sẽ tính $500.000 + (37 - 35) * 50.000 = 600.000$ VNĐ).

**Sự cố ghi nhận:**
Bộ phận CSKH nhận được phàn nàn từ nhiều hành khách ký gửi hành lý nặng 25 kg và 40 kg. Mặc dù hành lý vượt rất nhiều so với hạn mức miễn cước, hệ thống chỉ hiển thị mức phí 150.000 VNĐ trên hóa đơn thanh toán. Sự cố này gây thất thoát doanh thu đáng kể cho hãng bay và gây sai lệch dữ liệu tải trọng chuyến bay.

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn JavaScript đang vận hành trên thiết bị quầy check-in gặp sự cố:

```javascript
// Hệ thống tính phí hành lý ký gửi tại quầy Check-in
const passengerName = "Nguyen Van A";
const baggageWeight = 25; // Trọng lượng hành lý đo được (kg)

let excessFee = 0;
let noticeMessage = "";

// Kiểm tra trọng lượng hành lý và tính toán phí cước phát sinh
if (baggageWeight <= 7) {
  excessFee = 0;
  noticeMessage = "Hành lý trong tiêu chuẩn miễn phí.";
} else if (baggageWeight > 7) {
  excessFee = 150000;
  noticeMessage = "Áp dụng phí cước tiêu chuẩn.";
} else if (baggageWeight > 20) {
  excessFee = 350000;
  noticeMessage = "Áp dụng phí cước vượt mức.";
} else if (baggageWeight > 35) {
  const extraKg = baggageWeight - 35;
  excessFee = 500000 + extraKg * 50000;
  noticeMessage = "Áp dụng phí hành lý đặc biệt quá trọng tải.";
} else {
  excessFee = 0;
  noticeMessage = "Trọng lượng hành lý không hợp lệ.";
}

console.log("Hành khách:", passengerName);
console.log("Trọng lượng hành lý:", baggageWeight, "kg");
console.log("Phí cước phải trả:", excessFee, "VNĐ");
console.log("Trạng thái:", noticeMessage);
```

# **4. Yêu cầu đầu ra**

#### **Phần 1: Báo cáo phân tích & Bảng kịch bản kiểm thử (Test Case Report)**
Học viên thực hiện vết mã (Code Tracing), xác định chính xác dòng lệnh gây lỗi và hoàn thành bảng kịch bản kiểm thử theo mẫu dưới đây để chứng minh lỗi logic của chương trình:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8" cellspacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center; width: 5%;">STT</th>
      <th style="text-align: center; width: 15%;">Đầu vào (baggageWeight)</th>
      <th style="text-align: center; width: 20%;">Kết quả thực tế (Buggy Output)</th>
      <th style="text-align: center; width: 20%;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="text-align: center; width: 15%;">Dòng code gây lỗi</th>
      <th style="text-align: center; width: 25%;">Nguyên nhân & Giải thích logic</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td style="text-align: center;">25 kg</td>
      <td>excessFee = 150000</td>
      <td>excessFee = 350000</td>
      <td style="text-align: center;">Dòng 11</td>
      <td>Điều kiện <code>baggageWeight &gt; 7</code> thỏa mãn với giá trị 25, khiến khối lệnh gán 150.000 VNĐ thực thi ngay và bỏ qua toàn bộ các khối <code>else if</code> phía sau.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td style="text-align: center;">40 kg</td>
      <td>...</td>
      <td>...</td>
      <td style="text-align: center;">...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td style="text-align: center;">5 kg</td>
      <td>...</td>
      <td>...</td>
      <td style="text-align: center;">...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa mã nguồn nghiệp vụ**
Viết lại đoạn mã JavaScript đảm bảo xử lý chính xác 100% tất cả các trường hợp trọng lượng hành lý theo đúng Quy tắc nghiệp vụ của hãng hàng không.
*   Yêu cầu bổ sung: Thêm kiểm tra validation để xử lý trường hợp trọng lượng nhập vào không hợp lệ (ví dụ: `baggageWeight < 0` hoặc không phải số).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex1`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session_Session 06_Ex1`
