## <center>BÀI KIỂM TRA ĐẦU GIỜ: XỬ LÝ VÀ TÍNH TOÁN LUỒNG GIAO DỊCH THANH TOÁN (ORDER TRANSACTION WORKFLOW PROCESSING)</center>

### **1. Mục tiêu**
- Đánh giá khả năng áp dụng cấu trúc dữ liệu `List` và `Tuple` để lưu trữ chuỗi dữ liệu giao dịch trong Python.
- Đánh giá kĩ năng làm việc với vòng lặp (`while`, `for`), câu lệnh điều kiện (`if-elif-else`) và thao tác nhập/xử lý/ép kiểu dữ liệu từ Console CLI.
- Kiểm tra tư duy tính toán luồng nghiệp vụ dòng tiền thực tế và cập nhật dữ liệu bộ nhớ theo nguyên tắc bất biến (Immutability) của Tuple.

---

### **2. Yêu cầu**

Mô phỏng hệ thống xử lý giao dịch thanh toán đơn hàng. Dữ liệu giao dịch được quản lý dưới dạng một danh sách các Tuple (`transactions_list`), trong đó mỗi giao dịch bao gồm 4 thông tin: `(transaction_id, transaction_type, amount, status)`.

Khởi tạo sẵn danh sách giao dịch ban đầu:
```python
transactions_list = [
    ("TXN001", "PAYMENT", 150000.0, "SUCCESS"),
    ("TXN002", "REFUND", 50000.0, "SUCCESS"),
    ("TXN003", "PAYMENT", 200000.0, "PENDING")
]
```

Thực hiện xây dựng ứng dụng Console hiển thị Menu lặp liên tục (`while True`) cho phép người dùng lựa chọn và thực hiện các thao tác theo bản mô tả kỹ thuật chi tiết dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 22%;">Thao tác / Chức năng</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 20%;">Dữ liệu đầu vào</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 38%;">Logic xử lý & Quy tắc nghiệp vụ</th>
      <th style="border: 1px solid #dddddd; text-align: left; padding: 8px; width: 20%;">Kết quả đầu ra</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Thao tác 1] Ghi nhận giao dịch mới</b><br><code>record_new_transaction</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <code>transaction_id</code> (str)<br>
        <code>transaction_type</code> (str)<br>
        <code>amount</code> (float)<br>
        <code>status</code> (str)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Nhập dữ liệu giao dịch từ bàn phím.<br>
        2. Kiểm tra ràng buộc:<br>
        - <code>transaction_type</code> phải thuộc <code>"PAYMENT"</code> hoặc <code>"REFUND"</code>.<br>
        - <code>amount</code> phải > 0.<br>
        - <code>status</code> phải thuộc <code>"SUCCESS"</code> hoặc <code>"PENDING"</code>.<br>
        3. Nếu vi phạm quy tắc, in thông báo lỗi và không thêm.<br>
        4. Nếu hợp lệ, tạo Tuple mới và dùng <code>append()</code> đưa vào <code>transactions_list</code>.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">In thông báo thêm thành công và in lại danh sách tất cả các giao dịch.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Thao tác 2] Tính toán luồng dòng tiền</b><br><code>calculate_net_balance</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;"><code>transactions_list</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Duyệt từng phần tử Tuple trong <code>transactions_list</code>.<br>
        2. Lọc các giao dịch có <code>status == "SUCCESS"</code>.<br>
        3. Tính toán:<br>
        - <code>total_payment</code>: Tổng <code>amount</code> của các giao dịch <code>PAYMENT</code> thành công.<br>
        - <code>total_refund</code>: Tổng <code>amount</code> của các giao dịch <code>REFUND</code> thành công.<br>
        - <code>net_balance</code> = <code>total_payment</code> - <code>total_refund</code>.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">In báo cáo chi tiết: Số lượng giao dịch thành công, Tổng thu (PAYMENT), Tổng hoàn (REFUND) và Thực thu (Net Balance).</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px;"><b>[Thao tác 3] Cập nhật trạng thái giao dịch</b><br><code>update_transaction_status</code></td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        <code>target_id</code> (str)<br>
        <code>new_status</code> (str)
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">
        1. Nhập <code>target_id</code> và <code>new_status</code> ("SUCCESS" hoặc "PENDING").<br>
        2. Vòng lặp duyệt tìm giao dịch có <code>transaction_id == target_id</code>.<br>
        3. Do Tuple là immutable, tạo một Tuple mới với <code>new_status</code> và ghi đè lại vị trí chỉ số (index) tương ứng trong <code>transactions_list</code>.<br>
        4. Trường hợp không tìm thấy <code>target_id</code>, in thông báo không tìm thấy.
      </td>
      <td style="border: 1px solid #dddddd; padding: 8px;">In thông báo cập nhật thành công kèm thông tin giao dịch đã cập nhật.</td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

- **Thao tác 1 (3.0 điểm):** Kiểm tra chính xác điều kiện đầu vào của `transaction_type`, `amount`, `status`; đóng gói đúng cấu trúc Tuple và `append` thành công vào List.
- **Thao tác 2 (3.0 điểm):** Lọc đúng trạng thái `"SUCCESS"`, phân loại chính xác `PAYMENT` / `REFUND` và tính toán đúng kết quả `net_balance`.
- **Thao tác 3 (3.0 điểm):** Xử lý chuẩn xác việc cập nhật Tuple bằng cách tạo Tuple mới và thay thế vị trí index trong List; xử lý lỗi không tìm thấy `target_id`.
- **Chất lượng mã nguồn (1.0 điểm):** Sử dụng 100% tên biến Tiếng Anh theo chuẩn `snake_case` (ví dụ: `transactions_list`, `total_payment`, `net_balance`, `target_id`), luồng điều khiển CLI menu rõ ràng, không vi phạm phạm vi cấm.

---

### **4. Yêu cầu nộp bài**

1. Tạo file script Python đặt tên theo quy chuẩn: `transaction_processing.py`.
2. Đẩy (push) mã nguồn lên repository GitHub cá nhân theo cây thư mục:
   ```text
   python-core-entry-test/
   └── session_09/
       └── transaction_processing.py
   ```
3. Nộp liên kết (URL) commit hoặc repository GitHub lên hệ thống trước khi hết giờ.