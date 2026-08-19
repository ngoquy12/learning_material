# <center>Bài Kiểm Tra Đầu Giờ: Quản Lý Danh Mục Thiết Bị Văn Phòng (Office Equipment Catalog Management)</center>

### **1. Mục tiêu**
- Kiểm tra kĩ năng khai báo và sử dụng biến số ES6 (`let`, `const`), kiểu dữ liệu nguyên thủy và cấu trúc dữ liệu đối tượng (`Object Literal`).
- Đánh giá khả năng thao tác với mảng đối tượng (`Array of Objects`): thêm phần tử (`push`), truy cập và cập nhật thuộc tính đối tượng theo chỉ số.
- Vận dụng vòng lặp (`for` hoặc `for...of`), câu lệnh điều kiện (`if-else` / toán tử ba ngôi `ternary`) và biểu thức toán tử để duyệt mảng, tính toán tổng giá trị tồn kho.
- Định dạng chuỗi đầu ra chuyên nghiệp bằng Template Literals (backticks `${}`) hiển thị trực tiếp trên màn hình Console CLI.

---

### **2. Yêu cầu**

Một công ty cần xây dựng kịch bản mã nguồn JavaScript (Console Script) để quản lý danh mục thiết bị văn phòng. Bạn hãy thực hiện các thao tác quản lý dữ liệu theo thông số chi tiết trong bảng bên dưới:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2; text-align: left;">
      <th style="border: 1px solid #dddddd; padding: 8px; width: 22%;">Tên Thao Tác / Quyền Xử Lý</th>
      <th style="border: 1px solid #dddddd; padding: 8px; width: 20%;">Dữ Liệu Đầu Vào (Input)</th>
      <th style="border: 1px solid #dddddd; padding: 8px; width: 38%;">Logic Xử Lý & Quy Tắc Business</th>
      <th style="border: 1px solid #dddddd; padding: 8px; width: 20%;">Đầu Ra Mong Đổi (Output)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Khởi tạo danh mục thiết bị]</b><br>
        <code>initEquipmentCatalog</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Dữ liệu thô gồm 3 đối tượng thiết bị ban đầu:
        <ul>
          <li><code>equipmentId</code> (string)</li>
          <li><code>equipmentName</code> (string)</li>
          <li><code>category</code> (string)</li>
          <li><code>price</code> (number)</li>
          <li><code>stockQuantity</code> (number)</li>
        </ul>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Khai báo mảng <code>equipmentList</code> chứa 3 đối tượng thiết bị mẫu.<br>
        2. Đảm bảo thuộc tính <code>price</code> và <code>stockQuantity</code> có kiểu dữ liệu <code>number</code> hợp lệ (không phải chuỗi).
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Mảng <code>equipmentList</code> khởi tạo thành công với 3 phần tử đối tượng.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Thêm thiết bị & Cập nhật]</b><br>
        <code>addEquipmentProcess</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        - Đối tượng thiết bị mới <code>newEquipment</code>.<br>
        - Vị trí chỉ số cần cập nhật <code>targetIndex</code> (ví dụ: <code>0</code>).<br>
        - Số lượng tồn kho mới <code>updatedStock</code>.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Sử dụng phương thức <code>push()</code> để thêm <code>newEquipment</code> vào cuối mảng <code>equipmentList</code>.<br>
        2. Dùng câu lệnh điều kiện <code>if</code> kiểm tra <code>targetIndex</code> nằm trong phạm vi chỉ số hợp lệ của mảng.<br>
        3. Nếu hợp lệ, tiến hành cập nhật thuộc tính <code>stockQuantity</code> của thiết bị tại chỉ số đó bằng giá trị <code>updatedStock</code>.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Mảng <code>equipmentList</code> được tăng số lượng phần tử và thông tin tồn kho tại chỉ số chỉ định được sửa đổi.
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <b>[Duyệt danh mục & Tính tổng]</b><br>
        <code>calculateInventoryProcess</code>
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Mảng <code>equipmentList</code> sau khi đã cập nhật dữ liệu.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Khai báo biến tích lũy <code>totalInventoryValue = 0</code>.<br>
        2. Duyệt mảng bằng vòng lặp <code>for</code> hoặc <code>for...of</code>.<br>
        3. Với mỗi thiết bị:<br>
        &nbsp;&nbsp;- Tính thành tiền = <code>price * stockQuantity</code> và cộng dồn vào <code>totalInventoryValue</code>.<br>
        &nbsp;&nbsp;- Xác định trạng thái nhập hàng: Nếu <code>stockQuantity < 5</code> thì gán <code>status = "CẦN NHẬP THÊM"</code>, ngược lại <code>status = "ĐỦ HÀNG"</code> (khuyên dùng toán tử 3 ngôi).<br>
        &nbsp;&nbsp;- In thông tin thiết bị ra Console bằng Template Literals.<br>
        4. In kết quả tổng giá trị tồn kho của toàn bộ danh mục ở dòng cuối cùng.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        Hiển thị danh sách thiết bị có định dạng rõ ràng và dòng thông báo tổng giá trị kho hàng trên màn hình Console CLI.
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

| STT | Tiêu chí đánh giá | Điểm tối đa |
| :---: | :--- | :---: |
| 1 | Khai báo đúng cấu trúc mảng đối tượng `equipmentList` với các kiểu dữ liệu chuẩn xác và chuẩn đặt tên `camelCase`. | 2.0 điểm |
| 2 | Thực hiện thêm thiết bị mới bằng `.push()` và cập nhật thuộc tính tồn kho của đối tượng theo chỉ số an toàn. | 2.5 điểm |
| 3 | Xử lý đúng vòng lặp duyệt mảng và tính toán tổng giá trị tồn kho chính xác (`price * stockQuantity`). | 2.5 điểm |
| 4 | Phân loại trạng thái hàng tồn bằng câu lệnh điều kiện/toán tử 3 ngôi và định dạng xuất Console bằng Template Literals. | 2.0 điểm |
| 5 | Mã nguồn trình bày sạch sẻ, không bị lỗi cú pháp, chạy thành công trong môi trường Node.js / Browser Console. | 1.0 điểm |
| **Tổng** | **Tổng điểm bài kiểm tra** | **10.0 điểm** |

---

### **4. Yêu cầu nộp bài**
- Tạo tệp tin mã nguồn đặt tên là `script.js` và thực thi kịch bản bằng Node.js (`node script.js`) hoặc nhúng vào file HTML để kiểm tra trên màn hình Browser Console.
- Cam kết toàn bộ tên biến, tham số và thuộc tính đối tượng được viết bằng 100% Tiếng Anh có nghĩa theo chuẩn `camelCase`.
- Thực hiện commit mã nguồn lên tài khoản Git cá nhân với cú pháp:  
  `feat(entry-test-1): complete office equipment catalog script`
- Dán liên kết repository GitHub vào hệ thống nộp bài trước khi hết thời gian làm bài.
