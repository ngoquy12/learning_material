## <center>Quản Lý Giao Dịch Điểm Thưởng (Reward Points Transaction Ledger CLI)</center>

### **1. Mục tiêu**
Bài kiểm tra nhằm đánh giá khả năng vận dụng kiến thức nền tảng Python 3.12 trong việc xây dựng ứng dụng Console điều khiển luồng giao dịch và tính toán nghiệp vụ cơ bản. Học viên cần áp dụng cấu trúc dữ liệu `List` kết hợp `Tuple`, vòng lặp `while`/`for`, câu lệnh điều kiện `if-elif-else` và kỹ thuật xử lý ngoại lệ `try-except` để thực hiện xử lý dữ liệu giao dịch trực tiếp trong luồng chương trình chính mà không sử dụng hàm tùy chỉnh hay lớp đối tượng.

---

### **2. Yêu cầu**

#### **b. Phạm vi kĩ thuật và quy định ràng buộc**
* **Phạm vi cho phép:** Biến, kiểu dữ liệu nguyên bản, `List`, `Tuple`, toán tử, `if-elif-else`, vòng lặp `while`/`for`, menu CLI tương tác, `try-except` cơ bản (`ValueError`).
* **Phạm vi nghiêm cấm:** 
  * TUYỆT ĐỐI CẤM sử dụng Từ điển (`Dictionary`), Tập hợp (`Set`).
  * TUYỆT ĐỐI CẤM định nghĩa hàm tùy chỉnh (`def`), CẤM lập trình hướng đối tượng (`class`).
  * TUYỆT ĐỐI CẤM sử dụng thư viện bên thứ ba hoặc framework kiểm thử (`Pytest`).
* **Đặt tên biến:** 100% Tiếng Anh có nghĩa theo chuẩn `snake_case` (ví dụ: `transactions`, `transaction_id`, `points_amount`, `total_earned`).

#### **c. Bảng tả chi tiết chức năng ứng dụng CLI**

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left; width: 20%;">Tên chức năng</th>
      <th style="padding: 8px; text-align: left; width: 20%;">Dữ liệu đầu vào / Biến</th>
      <th style="padding: 8px; text-align: left; width: 40%;">Luồng xử lý & Quy tắc nghiệp vụ</th>
      <th style="padding: 8px; text-align: left; width: 20%;">Kết quả đầu ra mong đợi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;">
        <b>1. Ghi nhận giao dịch mới</b><br>
        <code>add_transaction()</code>
      </td>
      <td style="padding: 8px;">
        <code>transaction_id</code> (str)<br>
        <code>transaction_type</code> (str)<br>
        <code>points_amount</code> (float)
      </td>
      <td style="padding: 8px;">
        - Yêu cầu nhập mã giao dịch, loại giao dịch (chỉ chấp nhận giá trị <code>"EARN"</code> hoặc <code>"REDEEM"</code>), và số điểm.<br>
        - Dùng <code>try-except</code> để bắt lỗi nếu số điểm không phải là số hợp lệ hoặc số điểm &le; 0.<br>
        - Nếu hợp lệ, đóng gói thành <code>Tuple</code> dạng <code>(transaction_id, transaction_type, points_amount)</code> và thêm vào <code>List</code> lưu trữ <code>transactions</code>.
      </td>
      <td style="padding: 8px;">
        In thông báo ghi nhận thành công hoặc hiển thị thông báo lỗi cụ thể ra màn hình Console nếu dữ liệu nhập sai quy tắc.
      </td>
    </tr>
    <tr>
      <td style="padding: 8px;">
        <b>2. Tính tổng quan và số dư điểm</b><br>
        <code>calculate_summary()</code>
      </td>
      <td style="padding: 8px;">
        Danh sách <code>transactions</code> dạng <code>List</code> các <code>Tuple</code>
      </td>
      <td style="padding: 8px;">
        - Sử dụng vòng lặp <code>for</code> duyệt từng phần tử trong <code>transactions</code>.<br>
        - Cộng dồn điểm tích lũy vào biến <code>total_earned</code> nếu loại là <code>"EARN"</code>.<br>
        - Cộng dồn điểm đã quy đổi vào biến <code>total_redeemed</code> nếu loại là <code>"REDEEM"</code>.<br>
        - Tính số dư hiện tại: <code>net_balance = total_earned - total_redeemed</code>.
      </td>
      <td style="padding: 8px;">
        Hiển thị báo cáo gồm: Tổng điểm tích lũy, Tổng điểm đã dùng, Số dư điểm hiện tại.
      </td>
    </tr>
    <tr>
      <td style="padding: 8px;">
        <b>3. Tra cứu lịch sử giao dịch</b><br>
        <code>filter_transactions()</code>
      </td>
      <td style="padding: 8px;">
        <code>search_type</code> (str: "EARN" hoặc "REDEEM")
      </td>
      <td style="padding: 8px;">
        - Nhập loại giao dịch cần tra cứu từ bàn phím.<br>
        - Duyệt danh sách <code>transactions</code> và in các giao dịch có loại trùng khớp.<br>
        - Đếm số lượng giao dịch khớp và tính tổng điểm của các giao dịch đó.
      </td>
      <td style="padding: 8px;">
        Hiển thị danh sách các giao dịch tìm thấy kèm thông tin số lượng và tổng điểm; hoặc in thông báo không có dữ liệu phù hợp.
      </td>
    </tr>
  </tbody>
</table>

---

### **3. Tiêu chí đánh giá**

| STT | Tiêu chí đánh giá | Điểm tối đa |
| :---: | :--- | :---: |
| 1 | **Giao diện Menu CLI:** Khởi tạo được menu dạng vòng lặp `while`, hiển thị tùy chọn và thoát chương trình chính xác. | **2.0 điểm** |
| 2 | **Ghi nhận giao dịch:** Xử lý nhập liệu, validate loại giao dịch ("EARN"/"REDEEM"), kiểm tra số điểm > 0 và đóng gói dữ liệu vào `Tuple` lưu trữ trong `List`. | **3.0 điểm** |
| 3 | **Tính toán số dư & Tổng quan:** Sử dụng vòng lặp duyệt `List` để tính toán chính xác tổng điểm nạp, tổng điểm rút và số dư khả dụng. | **2.5 điểm** |
| 4 | **Tra cứu dữ liệu:** Lọc và hiển thị danh sách giao dịch theo loại chính xác, đếm đúng số lượng kết quả. | **1.5 điểm** |
| 5 | **Chuẩn mã nguồn & Xử lý lỗi:** Đặt tên biến 100% Tiếng Anh (`snake_case`), không sử dụng các kiến thức bị cấm (`def`, `dict`, `set`, `class`), có `try-except` bắt lỗi ép kiểu. | **1.0 điểm** |
| **Tổng** | | **10.0 điểm** |

---

### **4. Yêu cầu nộp bài**
1. Học viên tạo file mã nguồn với tên `main.py` trong thư mục bài làm.
2. Cam kết toàn bộ mã nguồn được viết trực tiếp trong khối lệnh chính, không sử dụng hàm `def` hoặc cấu trúc `dict`/`set`.
3. Kiểm tra chương trình chạy thành công trên môi trường Python 3.12 trước khi nộp.
4. Thực hiện `git add`, `git commit` với thông điệp: `"feat: complete entry test session 09 - reward points CLI"` và đẩy bài làm lên repository được cấp.