# Cấu trúc Vòng lặp for, range() và Vòng lặp while

## Vòng lặp for và Hàm range()

### Khái niệm & Vai trò

- Định nghĩa ngắn gọn: Lặp qua chuỗi giá trị tuần tự với số lần xác định trước.
- Vai trò: Tự động hóa xử lý danh sách phần tử và các dải số nguyên.

### Cú pháp & Giải nghĩa

- Khai báo cú pháp chuẩn:

```python
  for item in range(start, stop, step):

# Khối lệnh xử lý
```

- Giải thích thành phần:
  - item: Biến nhận giá trị hiện tại trong mỗi lượt lặp.
  - start: Giá trị bắt đầu của dải số (mặc định là 0).
  - stop: Giá trị biên kết thúc (không bao gồm giá trị này).
  - step: Khoảng cách tăng hoặc giảm giữa các bước (mặc định là 1).

### Ví dụ thực hành

- Tính tổng doanh thu tuần tự từ các đơn hàng.

```python
  total_revenue = 0
  for order_id in range(1, 6):
      amount = order_id * 100000
      total_revenue += amount
      print("Đơn hàng", order_id, "giá trị:", amount)
  print("Tổng doanh thu:", total_revenue)
```

- Giải thích ví dụ: Vòng lặp duyệt từ 1 đến 5 để tính và tích lũy doanh thu.

### Lưu ý

- **Dải giá trị stop**: Giá trị stop trong range không bao gồm trong dải lặp.
- **Bước nhảy âm**: Khi step mang giá trị âm, start phải lớn hơn stop.

## Vòng lặp while

### Khái niệm & Vai trò

- Định nghĩa ngắn gọn: Thực thi khối lệnh liên tục khi điều kiện logic còn đúng.
- Vai trò: Xử lý các bài toán lặp chưa xác định trước số lần.

### Cú pháp & Giải nghĩa

- Khai báo cú pháp chuẩn:

```python
  while condition_expression:

# Khối lệnh xử lý

# Cập nhật biến điều kiện
```

- Giải thích thành phần:
  - condition_expression: Biểu thức kiểm tra điều kiện tiếp tục hoặc dừng lặp.
  - Khối lệnh xử lý: Thực hiện nghiệp vụ và cập nhật biến điều kiện.

### Ví dụ thực hành

- Thử lại kết nối mạng tối đa 3 lần đến khi thành công.

```python
  retry_count = 0
  max_retries = 3
  while retry_count < max_retries:
      retry_count += 1
      print("Đang thử lại lần:", retry_count)
  print("Hoàn tất tiến trình kiểm tra kết nối.")
```

- Giải thích ví dụ: Kiểm tra số lần thử lại và tăng biến đếm sau mỗi lượt.

### Lưu ý

- **Lặp vô hạn**: Quên cập nhật biến điều kiện khiến chương trình bị treo vĩnh viễn.
- **Khởi tạo biến đếm**: Biến đếm phải được gán giá trị hợp lệ trước khi lặp.

## Điều khiển Luồng lặp với break, continue và Khối else

### Khái niệm & Vai trò

- Định nghĩa ngắn gọn: Các câu lệnh thay đổi hướng thực thi hoặc ngắt vòng lặp.
- Vai trò: Tối ưu hiệu năng, bỏ qua các lượt dư thừa và kiểm soát hoàn tất.

### Cú pháp & Giải nghĩa

- Khai báo cú pháp chuẩn:

```python
  for item in sequence:
      if skip_condition:
          continue
      if stop_condition:
          break
  else:

# Chạy khi không chạm break
```

- Giải thích thành phần:
  - break: Thoát khỏi vòng lặp ngay lập tức tại thời điểm gọi.
  - continue: Bỏ qua đoạn mã còn lại của lượt hiện tại, sang lượt tiếp.
  - else: Khối lệnh thực thi khi vòng lặp kết thúc bình thường, không chạm break.

### Ví dụ thực hành

- Kịch bản áp dụng: Quét cổng dịch vụ, bỏ qua cổng bảo trì và dừng khi gặp sự cố.

```python
  for port in range(1, 6):
      if port == 3:
          print("Cổng 3 đang bảo trì -> Bỏ qua.")
          continue
      if port == 5:
          print("Cổng 5 có rủi ro! Ngắt khẩn cấp.")
          break
      print("Cổng", port, "kiểm tra an toàn.")
  else:
      print("Tất cả các cổng đã được kiểm tra hoàn tất.")
```

- Giải thích ví dụ: Cổng 3 bị bỏ qua bằng continue, cổng 5 ngắt chương trình bằng break.

### Lưu ý

- **Lỗi bỏ qua bước tăng đếm**: Trong vòng lặp while, gọi continue trước khi tăng đếm gây lặp vô hạn.
- **Điều kiện chạy khối else**: Khối else chỉ chạy khi vòng lặp duyệt hết mà không gọi break.

## Tổng kết

- for xử lý số lần lặp cố định, while xử lý lặp theo điều kiện, break/continue/else tinh chỉnh luồng cho cả hai.
- Luồng dữ liệu xuyên suốt: Dữ liệu đầu vào -> Duyệt lặp (for/while) -> Kiểm tra luồng (break/continue) -> Báo cáo trạng thái (else).
- Ứng dụng tổng hợp: Dùng while duy trì kết nối, for quét danh sách kiểm tra, kết hợp break ngắt khi phát hiện sự cố và else xác nhận hệ thống an toàn.
