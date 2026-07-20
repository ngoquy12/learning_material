````markmap
# Session 01: Giới thiệu ngôn ngữ Python

## Mục tiêu bài học
- Hiểu triết lý thiết kế Zen of Python và cơ chế thực thi của ngôn ngữ thông dịch.
- Nắm vững tính chất kiểu dữ liệu động và các ứng dụng thực tế của Python.
- Nhận diện và phòng tránh các lỗi cơ bản như thụt lề sai và xung đột kiểu dữ liệu.

## Triết lý thiết kế (Zen of Python)
### Khái niệm cốt lõi
- Bộ quy tắc định hướng viết mã nguồn Python tối giản, rõ ràng, đề cao tính mở rộng và khả năng đọc hiểu của con người.
### Cú pháp & Cách khai báo
- Lệnh hiển thị các nguyên tắc thiết kế của Python:
  ```python
  import this
````

### Lưu ý thực chiến

- Ưu tiên viết mã nguồn trực quan, tường minh thay vì viết các đoạn code phức tạp, khó hiểu để tối ưu hóa việc bảo trì.

## Ngôn ngữ thông dịch (Interpreted Language)

### Khái niệm cốt lõi

- Mã nguồn Python không biên dịch trực tiếp ra mã máy mà được trình thông dịch dịch từng dòng thành bytecode rồi thực thi trên máy ảo Python.
- ![](../images/mindmap_img_1.png)

### Cú pháp & Cách khai báo

- Thực thi một script Python trực tiếp từ Terminal:
  ```bash
  python main.py
  ```

### Lưu ý thực chiến

- Tốc độ chạy thường chậm hơn ngôn ngữ biên dịch và lỗi cú pháp chỉ được phát hiện khi luồng chương trình chạy tới dòng code lỗi.

## Kiểu dữ liệu động (Dynamic Typing)

### Khái niệm cốt lõi

- Kiểu dữ liệu của biến được quyết định tự động tại thời điểm chạy dựa trên giá trị gán cho biến mà không cần khai báo trước.

### Cú pháp & Cách khai báo

- Khai báo biến và thay đổi kiểu dữ liệu:
  ```python
  x = 10
  x = "Xin chao Python"
  print(type(x))
  ```

### Lưu ý thực chiến

- Tránh thay đổi kiểu dữ liệu của biến một cách tùy tiện trong cùng một phạm vi để hạn chế lỗi logic khi thực hiện tính toán.

## Ứng dụng đa lĩnh vực của Python

### Khái niệm cốt lõi

- Khả năng ứng dụng rộng rãi từ phân tích dữ liệu, trí tuệ nhân tạo, phát triển web cho đến kiểm thử tự động nhờ thư viện phong phú.

### Cú pháp & Cách khai báo

- Import module từ thư viện chuẩn để xử lý tính toán:
  ```python
  import math
  print(math.sqrt(16))
  ```

### Lưu ý thực chiến

- Luôn tìm kiếm giải pháp từ thư viện chuẩn trước khi cài thêm thư viện bên ngoài nhằm giảm thiểu sự phụ thuộc không cần thiết.

## Tự động hóa (Automation/Scripting)

### Khái niệm cốt lõi

- Viết các đoạn mã ngắn để tự động hóa các tác vụ lặp đi lặp lại như quản lý file, thư mục và tương tác với hệ điều hành.

### Cú pháp & Cách khai báo

- Lấy đường dẫn làm việc hiện tại của hệ thống:
  ```python
  import os
  print(os.getcwd())
  ```

### Lưu ý thực chiến

- Cần nhất quán việc thụt lề (IndentationError) và kiểm tra kỹ quyền truy cập đường dẫn hệ thống để tránh lỗi dừng chương trình đột ngột.

```

```

```

```
