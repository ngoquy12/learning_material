## <center>Bài Kiểm Tra Đầu Giờ: Xây Dựng Luồng Xử Lý Giao Dịch Bán Hàng Console (Console Transaction & Workflow Processing System)</center>

### **1. Mục tiêu**
- **Đánh giá kiến thức nền tảng:** Kiểm tra khả năng vận dụng biến ES6 (`let`, `const`), kiểu dữ liệu nguyên thủy, toán tử số học, toán tử so sánh nghiêm ngặt (`===`), toán tử ba ngôi (ternary operator) và các câu lệnh điều khiển luồng.
- **Thao tác với Cấu trúc Dữ liệu:** Đánh giá kỹ năng thao tác trên Mảng (`Array`) các Đối tượng (`Object`), kỹ thuật duyệt mảng bằng vòng lặp (`for`, `for...of`), và phương thức làm việc với chuỗi JSON (`JSON.stringify()`).
- **Tư duy Xử lý Giao dịch (Transaction Logic):** Rèn luyện tư duy lập trình luồng nghiệp vụ tính toán chiết khấu, tổng tiền hóa đơn và ghi nhận lịch sử giao dịch trong môi trường Console (CLI Core Application).

---

### **2. Yêu cầu**

Sinh viên thực hiện bài lập trình Console bằng JavaScript (Node.js runtime hoặc Browser Console trong Cursor AI IDE) để hoàn thành quy trình xử lý giao dịch bán hàng và tính toán doanh thu theo bảng mô tả chi tiết dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 25%;">Tên chức năng / Khối xử lý</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 20%;">Dữ liệu đầu vào</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 35%;">Quy tắc & Logic xử lý</th>
      <th style="border: 1px solid #dddddd; padding: 8px; text-align: left; width: 20%;">Kết quả đầu ra mong đợi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>Khởi tạo danh sách giỏ hàng</b><br><code>initializeCart()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <code>cartItems</code> (Array),<br>
        <code>customerCategory</code> (String),<br>
        <code>paymentMethod</code> (String)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Khai báo mảng <code>cartItems</code> chứa ít nhất 3 phần tử dạng Object đại diện cho mặt hàng mua: <code>itemId</code>, <code>itemName</code>, <code>unitPrice</code>, <code>quantity</code>.<br>
        2. Khai báo <code>customerCategory</code> ("VIP" hoặc "REGULAR") và <code>paymentMethod</code> ("CASH" hoặc "CARD").
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Mảng <code>cartItems</code> và các biến thông tin giao dịch được khởi tạo thành công với dữ liệu hợp lệ.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>Tính toán tổng tiền & Chiết khấu</b><br><code>calculateTransactionTotal()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <code>cartItems</code>,<br>
        <code>customerCategory</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Duyệt mảng <code>cartItems</code> bằng vòng lặp để tính tổng giá trị hàng <code>subtotalAmount</code> (bằng <code>unitPrice * quantity</code>).<br>
        2. Kiểm tra nếu <code>customerCategory === "VIP"</code> thì giảm giá 10% trên <code>subtotalAmount</code>.<br>
        3. Sử dụng toán tử ba ngôi (ternary operator): Nếu <code>subtotalAmount > 500000</code> thì giảm thêm chiết khấu cố định 20,000 VND, ngược lại chiết khấu thêm bằng 0.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Số thực <code>finalTotalAmount</code> phản ánh chính xác số tiền phải thanh toán sau khi áp dụng toàn bộ logic giảm giá.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>Ghi nhận nhật ký & Xuất hóa đơn</b><br><code>recordTransactionHistory()</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <code>transactionLog</code> (Array),<br>
        <code>finalTotalAmount</code>,<br>
        <code>paymentMethod</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Đóng gói dữ liệu giao dịch thành Object <code>transactionRecord</code> gồm: <code>transactionId</code>, <code>finalTotalAmount</code>, <code>paymentMethod</code>, <code>status</code> ("COMPLETED").<br>
        2. Thêm <code>transactionRecord</code> vào mảng <code>transactionLog</code> bằng phương thức <code>push()</code>.<br>
        3. Chuyển đổi <code>transactionRecord</code> thành chuỗi JSON bằng <code>JSON.stringify()</code> và in ra màn hình Console cùng hóa đơn dạng Template Literals.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Màn hình Console hiển thị thông tin hóa đơn rõ ràng và chuỗi dữ liệu JSON của giao dịch.
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

| STT | Tiêu chí đánh giá | Điểm tối đa |
| :--- | :--- | :---: |
| 1 | **Khởi tạo dữ liệu:** Khai báo chính xác mảng đối tượng giỏ hàng và các biến loại khách hàng, phương thức thanh toán bằng từ khóa ES6 (`const`, `let`). | **2.0 điểm** |
| 2 | **Tính toán dòng tiền:** Duyệt mảng chính xác để tính tổng tiền hàng (`subtotalAmount`) và tiền từng món (`unitPrice * quantity`). | **2.5 điểm** |
| 3 | **Logic nghiệp vụ & Toán tử:** Thực hiện chính xác điều kiện giảm giá VIP và toán tử ba ngôi (ternary operator) cho chiết khấu đơn hàng lớn. | **2.5 điểm** |
| 4 | **Xử lý Object & JSON:** Đóng gói bản ghi giao dịch, thêm vào mảng bằng `push()`, định dạng hóa đơn Template Literals và chuyển đổi JSON bằng `JSON.stringify()`. | **2.0 điểm** |
| 5 | **Chuẩn mực Mã nguồn:** Đặt tên biến 100% Tiếng Anh (`camelCase`), trình bày mã nguồn sạch sẽ, đúng quy chuẩn mã lệnh Console CLI. | **1.0 điểm** |
| **Tổng** | **Tổng điểm đánh giá** | **10.0 điểm** |

---

### **4. Yêu cầu nộp bài**
- **Định dạng tập tin:** Nộp file mã nguồn JavaScript có tên `transaction_process.js` (hoặc thực thi trực tiếp trong thư mục dự án Cursor AI IDE).
- **Môi trường thực thi:** Kiểm tra chương trình chạy thành công trên môi trường Node.js CLI (`node transaction_process.js`) hoặc Browser Developer Tools Console.
- **Quy trình nộp bài:** Commit mã nguồn lên kho chứa GitHub cá nhân và dán liên kết (URL) vào hệ thống quản lý học tập trước khi hết thời gian làm bài.