# <center>[Vận dụng cơ bản 4] Sửa lỗi tính tổng tiền vé sự kiện khi áp dụng mức chiết khấu 0%</center>

### **1. Mục tiêu**
*   Vận dụng cú pháp **Arrow Function** và tính năng **Tham số mặc định (Default Parameters)** của ES6+ để tổ chức hàm tính toán trong hệ thống.
*   Phân biệt sự khác biệt về mặt logic giữa việc khai báo tham số mặc định chuẩn ES6 với kỹ thuật kiểm tra giá trị mặc định bằng toán tử logic `||` (OR).
*   Thực hiện trace code (truy vết mã nguồn), xác định chính xác dòng lệnh gây lỗi và sửa mã nguồn để đảm bảo tính đúng đắn cho các phép tính nghiệp vụ bán vé.

### **2. Bối cảnh & Vấn đề**
Hệ thống Bán vé Sự kiện Ca nhạc & Hội thảo (Ticketbox) đang vận hành module tính toán tổng tiền thanh toán cho đơn đặt vé của khách hàng.

Quy tắc nghiệp vụ của hệ thống:
1. Giá vé gốc tùy thuộc vào từng khu vực (Ví dụ: Vị trí Zone A có giá 1.500.000 VNĐ/vé).
2. Trong giai đoạn mở bán sớm (**Early Bird**), hệ thống áp dụng mức giảm giá mặc định là 15% (`discountRate = 0.15`).
3. Trong giai đoạn mở bán chính thức (**Standard Phase**), vé được bán đúng giá gốc, tức là không áp dụng giảm giá (`discountRate = 0`).
4. Phí dịch vụ xuất vé cố định là 30.000 VNĐ trên mỗi đơn hàng (mặc định nếu không truyền phí khác).
5. Công thức tính tổng tiền thanh toán: `(Giá vé * Số lượng * (1 - Mức giảm giá)) + Phí dịch vụ`.

[REQUIREMENT] Phản ánh từ thực tế:
Bộ phận Kế toán báo cáo rằng trong giai đoạn mở bán chính thức (Standard Phase), tất cả các đơn hàng mua vé với mức giảm giá `0%` (`discountRate = 0`) đều bị tính sai tiền. Hệ thống vẫn tự động trừ 15% trên tổng tiền vé của khách hàng, gây thất thoát doanh thu nghiêm trọng cho ban tổ chức.

### **3. Mã nguồn hiện tại**

Dưới đây là đoạn mã nguồn xử lý tính tổng tiền đơn hàng đang chạy trên hệ thống:

```javascript
// Hàm tính tổng tiền đơn hàng đặt vé concert
const calculateTicketOrderTotal = (ticketPrice, ticketQuantity = 1, discountRate, serviceFee = 30000) => {
  // Xử lý mức chiết khấu giảm giá
  const finalDiscountRate = discountRate || 0.15;

  // Tính tổng tiền vé sau chiết khấu
  const subtotalBeforeFee = ticketPrice * ticketQuantity * (1 - finalDiscountRate);

  // Tính tổng tiền thanh toán cuối cùng bao gồm phí dịch vụ
  const grandTotal = subtotalBeforeFee + serviceFee;

  return grandTotal;
};

// Kịch bản 1: Khách hàng mua 2 vé đợt Early Bird (Khuyết discountRate, sử dụng giảm giá mặc định 15%)
const earlyBirdOrder = calculateTicketOrderTotal(1500000, 2);
console.log('Tổng tiền đơn hàng Early Bird (2 vé):', earlyBirdOrder);

// Kịch bản 2: Khách hàng mua 2 vé đợt Mở bán chính thức (Truyền discountRate = 0)
const standardOrder = calculateTicketOrderTotal(1500000, 2, 0);
console.log('Tổng tiền đơn hàng Standard (2 vé, giảm 0%):', standardOrder);
```

# **4. Yêu cầu bài toán**

#### **Phần 1: Truy vết mã nguồn & Báo cáo Test Case (Code Tracing & Bug Discovery)**
Học viên tiến hành thực thi, phân tích mã nguồn hiện tại và hoàn thành bảng báo cáo kiểm thử bên dưới. Hàng số 1 đã được điền mẫu làm chuẩn, học viên cần tự phân tích và hoàn thiện các hàng còn lại (thay thế các dấu `...`).

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #ccc; padding: 8px; text-align: center;">STT</th>
      <th style="border: 1px solid #ccc; padding: 8px;">Đầu vào (Input)</th>
      <th style="border: 1px solid #ccc; padding: 8px;">Đầu ra hiện tại (Buggy Output)</th>
      <th style="border: 1px solid #ccc; padding: 8px;">Đầu ra mong đợi (Expected Output)</th>
      <th style="border: 1px solid #ccc; padding: 8px;">Dòng code gây lỗi (Failing Line)</th>
      <th style="border: 1px solid #ccc; padding: 8px;">Giải thích nguyên nhân logic (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">1</td>
      <td style="border: 1px solid #ccc; padding: 8px;">ticketPrice = 1500000<br>ticketQuantity = 2<br>discountRate = 0</td>
      <td style="border: 1px solid #ccc; padding: 8px;">2580000</td>
      <td style="border: 1px solid #ccc; padding: 8px;">3030000</td>
      <td style="border: 1px solid #ccc; padding: 8px;">Dòng 3: <code>const finalDiscountRate = discountRate || 0.15;</code></td>
      <td style="border: 1px solid #ccc; padding: 8px;">Toán tử <code>||</code> coi số <code>0</code> là giá trị falsy nên tự động chọn giá trị mặc định vế sau là <code>0.15</code>, dẫn đến việc vé đợt Standard (không giảm giá) bị trừ sai 15%.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">2</td>
      <td style="border: 1px solid #ccc; padding: 8px;">ticketPrice = 2000000<br>ticketQuantity = 1<br>discountRate = 0</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">3</td>
      <td style="border: 1px solid #ccc; padding: 8px;">ticketPrice = 800000<br>ticketQuantity = 4<br>discountRate = 0</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa đổi và tối ưu hóa mã nguồn (Source Code Correction)**
1. Sửa lại hàm `calculateTicketOrderTotal` sử dụng chuẩn cú pháp ES6 **Default Parameters** trực tiếp trên danh sách tham số của Arrow Function (`discountRate = 0.15`), loại bỏ hoàn toàn câu lệnh gắn giá trị mặc định bằng toán tử `||` trong thân hàm.
2. Kiểm tra lại toàn bộ các kịch bản gọi hàm (khi không truyền `discountRate` và khi truyền `discountRate = 0`) để đảm bảo hệ thống trả về chính xác số tiền theo đúng quy tắc nghiệp vụ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex4`.
    Ví dụ: `HNKS25CNTT1_Core_Session14_Ex4`
