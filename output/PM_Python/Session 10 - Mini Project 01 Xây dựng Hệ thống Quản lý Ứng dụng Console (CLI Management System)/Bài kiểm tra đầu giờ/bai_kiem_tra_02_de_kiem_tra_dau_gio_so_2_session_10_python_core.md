## <center>Hệ thống Xử lý Giao dịch và Đổi điểm Tích lũy (Transaction and Reward Points Processing System)</center>

### **1. Mục tiêu**
Đánh giá khả năng thiết kế hàm xử lý nghiệp vụ, kiểm soát lỗi logic và thao tác với cấu trúc danh bạ dữ liệu (dictionary) của học viên. Bài thi tập trung vào kỹ năng viết mã sạch (clean code), chuẩn hóa kiểu dữ liệu đầu vào và kiểm soát các ngoại lệ nghiệp vụ (business exceptions) thông qua cơ chế xử lý ngoại lệ gốc (native exceptions) của Python trong môi trường Console CLI.

### **2. Yêu cầu**

Giả định cấu trúc ví của người dùng được lưu trữ dưới dạng một Dictionary như sau:
```python
user_wallet = {
    "balance": 150000.0,  # Số dư tài khoản (float)
    "points": 500         # Điểm tích lũy (int)
}
```

Học viên thiết lập 2 hàm cốt lõi chịu trách nhiệm tính toán dòng tiền tệ và điểm thưởng theo các chỉ định nghiệp vụ chi tiết trong bảng dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="width: 25%; padding: 8px;">Tên chức năng/Hàm</th>
      <th style="width: 20%; padding: 8px;">Tham số/Input</th>
      <th style="padding: 8px;">Logic xử lý</th>
      <th style="width: 25%; padding: 8px;">Output / Kết quả trả về</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;"><b>Xử lý thanh toán đơn hàng</b><br><code>process_payment()</code></td>
      <td style="padding: 8px;">
        - <code>wallet</code>: dict<br>
        - <code>amount</code>: float
      </td>
      <td style="padding: 8px;">
        1. Kiểm tra nếu <code>amount</code> bé hơn hoặc bằng 0, ném ra ngoại lệ <code>ValueError</code> với thông báo phù hợp.<br>
        2. Kiểm tra nếu số dư tài khoản (<code>balance</code>) trong ví nhỏ hơn <code>amount</code>, ném ra ngoại lệ <code>ValueError</code>.<br>
        3. Khấu trừ số tiền thanh toán khỏi <code>balance</code>.<br>
        4. Tích điểm thưởng mới: <b>10%</b> giá trị thanh toán (chuyển đổi kết quả tích điểm này về kiểu số nguyên - <code>int</code>). Cộng số điểm mới này vào khóa <code>points</code>.<br>
        5. Cập nhật trực tiếp và trả về ví sau xử lý.
      </td>
      <td style="padding: 8px;">
        - Trả về <code>dict</code> ví đã cập nhật.<br>
        - Hoặc ném ra ngoại lệ <code>ValueError</code> nếu dữ liệu hoặc số dư không hợp lệ.
      </td>
    </tr>
    <tr>
      <td style="padding: 8px;"><b>Quy đổi điểm thưởng ra tiền</b><br><code>redeem_points_to_cash()</code></td>
      <td style="padding: 8px;">
        - <code>wallet</code>: dict<br>
        - <code>points_to_redeem</code>: int
      </td>
      <td style="padding: 8px;">
        1. Tỷ lệ quy đổi cố định: <b>1 điểm = 100 VND</b>.<br>
        2. Kiểm tra nếu <code>points_to_redeem</code> bé hơn hoặc bằng 0, ném ra ngoại lệ <code>ValueError</code>.<br>
        3. Kiểm tra nếu số điểm đang tích lũy (<code>points</code>) trong ví nhỏ hơn số điểm yêu cầu quy đổi, ném ra ngoại lệ <code>ValueError</code>.<br>
        4. Khấu trừ số điểm quy đổi khỏi <code>points</code>.<br>
        5. Tính giá trị tiền quy đổi được và cộng tiền này vào số dư <code>balance</code>.<br>
        6. Cập nhật trực tiếp và trả về ví sau xử lý.
      </td>
      <td style="padding: 8px;">
        - Trả về <code>dict</code> ví đã cập nhật.<br>
        - Hoặc ném ra ngoại lệ <code>ValueError</code> nếu yêu cầu quy đổi không hợp lệ.
      </td>
    </tr>
  </tbody>
</table>

*Yêu cầu bổ sung*: Viết một đoạn mã chạy thử nghiệm (simulation script) trong khối `try-except` để trình diễn tất cả các tình huống: thanh toán thành công, đổi điểm thành công, lỗi không đủ số dư và lỗi không đủ điểm tích lũy. In kết quả trạng thái ví ra màn hình sau mỗi giao dịch.

### **3. Tiêu chí đánh giá**
- **Đúng cú pháp & Quy chuẩn đặt tên (3.0 điểm)**: Viết đúng dạng `snake_case`, sử dụng hoàn toàn danh từ/động từ tiếng Anh có nghĩa cho biến và hàm.
- **Implement Logic nghiệp vụ (4.0 điểm)**:
  - Khấu trừ và cộng tích lũy tiền tệ chính xác theo tỷ lệ quy định khách quan (2.0 điểm).
  - Tích lũy và quy đổi điểm thưởng chuẩn xác đúng kiểu dữ liệu (2.0 điểm).
- **Kiểm soát lỗi đầu vào & Ngoại lệ (2.0 điểm)**: Nhận biết, kiểm tra chặn trước các điều kiện biên (nhỏ hơn 0, số dư âm) và phát ngoại lệ `ValueError`.
- **Kịch bản Demo & Hiển thị Console (1.0 điểm)**: Viết kịch bản mẫu trực quan hóa đầy đủ trường hợp biên xảy ra lỗi và phục hồi luồng hoạt động mà không bị crash ứng dụng.

### **4. Yêu cầu nộp bài**
- Học viên lưu mã nguồn vào một file duy nhất đặt tên là `transaction_processing.py`.
- Thiết lập kho lưu trữ và đẩy mã nguồn lên GitHub. Cung cấp đường dẫn phục vụ chấm bài theo cấu trúc sau:
  - GitHub Repository URL: `https://github.com/username/project-name`
  - Commit Hash của lần đẩy mã nguồn cuối cùng: `abcdef1234567890...`