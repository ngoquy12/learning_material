# <center>[Vận dụng cơ bản 6] Sửa lỗi tính toán chiết khấu và phạm vi biến trong module bán vé Ticketbox</center>

### **1. Mục tiêu**
*   **Hiểu và vận dụng cú pháp Arrow Function:** Sử dụng thành thạo Arrow Function trong ES6 để khai báo hàm tính toán logic nghiệp vụ gọn gàng, rõ ràng.
*   **Xử lý tham số mặc định (Default Parameters):** Nắm vững cơ chế hoạt động của tham số mặc định và phân biệt sự khác biệt giữa `undefined`, `null` và giá trị `0` khi áp dụng toán tử điều kiện hoặc gán mặc định.
*   **Quản lý phạm vi biến (Scope):** Kiểm soát phạm vi hoạt động của biến (Global Scope vs Local Scope), khắc phục hiện tượng rò rỉ dữ liệu và ô nhiễm biến toàn cục.
*   **Kỹ năng tìm và sửa lỗi (Debugging):** Xây dựng bảng kiểm thử (Test Case Report), xác định chính xác dòng code gây lỗi và tái cấu trúc mã nguồn theo chuẩn công nghiệp.

### **2. Bối cảnh & Vấn đề**
Hệ thống Bán vé Sự kiện Ca nhạc & Hội thảo (Ticketbox) đang đưa vào vận hành module tính tiền tự động cho sự kiện concert âm nhạc. Hệ thống áp dụng chính sách ưu đãi như sau:
*   Mặc định đợt mở bán Early Bird sẽ tự động giảm giá **15%** (tương đương `0.15`) trên tổng tiền vé gốc nếu khách hàng không nhập tỷ lệ chiết khấu khác.
*   Nếu khách hàng mua trong đợt bán vé thông thường (nhập chiết khấu là `0`), hệ thống **không** được phép áp dụng giảm giá.
*   Mỗi đơn hàng có một phí dịch vụ cố định là `30,000` VNĐ.
*   Quy định nghiệp vụ an toàn: Mỗi tài khoản chỉ được mua **tối đa 4 vé** cho một lần giao dịch. Nếu mua quá 4 vé, hệ thống phải từ chối xử lý và ném ra lỗi (Exception).

Bộ phận Hỗ trợ Khách hàng tiếp nhận phản ánh rằng hệ thống đang gặp sự cố nghiêm trọng: Nhiều khách hàng mua vé đợt bán thông thường (truyền chiết khấu `0`) vẫn bị tính nhầm giảm giá 15%. Ngoài ra, biến tính toán tổng tiền bị đè giá trị giữa các lượt gọi hàm khác nhau.

### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn ES6 đang bị lỗi logic trong hệ thống:

```javascript
// Biến toàn cục lưu trữ tổng tiền đơn hàng
let orderTotalAmount = 0;

// Hàm tính toán tổng tiền vé đơn hàng sử dụng Arrow Function
const calculateTicketOrder = (quantity, baseUnitPrice, discountRate, serviceFee = 30000) => {
  // Kiểm tra giới hạn số lượng vé mua tối đa
  if (quantity > 4) {
    return "Lỗi: Mỗi đơn hàng chỉ được mua tối đa 4 vé!";
  }

  // Gán giá trị mặc định cho tỷ lệ chiết khấu bằng toán tử OR (||)
  const appliedDiscount = discountRate || 0.15;

  // Tính tổng tiền gốc chưa giảm giá
  const rawTotal = quantity * baseUnitPrice;
  
  // Tính số tiền chiết khấu
  const discountAmount = rawTotal * appliedDiscount;

  // Cập nhật giá trị vào biến toàn cục
  orderTotalAmount = rawTotal - discountAmount + serviceFee;

  return orderTotalAmount;
};

// Thực thi kiểm thử các kịch bản mua vé
console.log("Đơn 1 (2 vé VIP 1,000,000 VNĐ - Khuyết tham số chiết khấu):", calculateTicketOrder(2, 1000000));
console.log("Đơn 2 (1 vé GA 500,000 VNĐ - Đợt bán thường discountRate = 0):", calculateTicketOrder(1, 500000, 0));
console.log("Đơn 3 (5 vé GA - Vượt quá giới hạn 4 vé):", calculateTicketOrder(5, 500000));
```

# **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo phân tích vết mã nguồn và Test Case (Trace Code & Bug Report)**
Học viên tiến hành chạy thử chương trình, phân tích luồng thực thi và hoàn thành bảng báo cáo Test Case dưới đây. Bảng phải chứa tối thiểu 3 kịch bản kiểm thử chứng minh các dòng mã sai lệch.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th>STT</th>
      <th>Đầu vào (Input)</th>
      <th>Kết quả hiện tại (Buggy Output)</th>
      <th>Kết quả kỳ vọng (Expected Output)</th>
      <th>Dòng code gây lỗi (Failing Line)</th>
      <th>Nguyên nhân & Logic (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>quantity = 1, baseUnitPrice = 500000, discountRate = 0</td>
      <td>455000</td>
      <td>530000</td>
      <td>Dòng 12: `const appliedDiscount = discountRate || 0.15;`</td>
      <td>Do 0 là falsy value trong JavaScript, toán tử || ép giá trị appliedDiscount thành 0.15 (15%), làm tính sai chiết khấu dù khách hàng nhập 0%.</td>
    </tr>
    <tr>
      <td>2</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td>3</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Tái cấu trúc và sửa lỗi mã nguồn (Source Code Correction)**
Học viên viết lại mã nguồn xử lý tính toán tiền vé tuân thủ các quy chuẩn sau:
1.  Chuyển đổi việc kiểm tra chiết khấu sang cú pháp **Default Parameter** của ES6 (`discountRate = 0.15`) ở mức khai báo tham số hàm.
2.  Loại bỏ hoàn toàn biến toàn cục `orderTotalAmount`, tính toán và trả về kết quả trong Scope cục bộ của hàm (Local Scope).
3.  Thực hiện validation đầu vào và ném ra ngoại lệ (`throw new Error(...)`) khi `quantity > 4` hoặc khi số lượng/đơn giá không hợp lệ (nhỏ hơn hoặc bằng 0).
4.  Sử dụng cấu trúc `try...catch` khi gọi hàm kiểm thử để xử lý các ngoại lệ một cách an toàn.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex6`.
    Ví dụ: `HNKS25CNTT1_Core_Session14_Ex6`
