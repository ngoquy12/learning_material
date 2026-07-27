```markmap
# Session 02 - Lesson 02: Toán tử so sánh

## Mục tiêu bài học
- Hiểu rõ kiểu dữ liệu logic Boolean đại diện cho True và False.
- Vận dụng thành thạo nhóm toán tử so sánh trong Python.
- Làm quen kỹ thuật ép kiểu, xử lý dữ liệu đầu vào và định dạng chuỗi.

## Kieu_du_lieu_Boolean

### Khái niệm cốt lõi
- Kiểu dữ liệu logic bool đại diện cho hai giá trị chân trị duy nhất là True (Đúng) và False (Sai).

### Cú pháp & Cách khai báo
- Khởi tạo giá trị Boolean:
  ```python
  is_active = True
  is_admin = False
  print(type(is_active))
  ```

### Lưu ý thực chiến
- Phải viết hoa chữ cái đầu (True, False). Các từ viết thường true hay false sẽ báo lỗi NameError.
- ![](../images/mindmap_img_1.png)

## Toan_tu_so_sanh

### Khái niệm cốt lõi
- Nhóm công cụ so sánh hai toán hạng toán học và biểu thức logic để trả về kết quả kiểu Boolean.

### Cú pháp & Cách khai báo
- Thực thi so sánh đơn và so sánh chuỗi:
  ```python
  a, b = 10, 20
  is_less = a < b
  is_equal = a == b
  chain_check = 5 < a < 15
  ```

### Lưu ý thực chiến
- Không được viết đảo ngược dấu như => hay =< vì sẽ gây lỗi cú pháp SyntaxError.
- Hạn chế so sánh trực tiếp không đồng nhất kiểu dữ liệu (chuỗi chữ và số thực) để tránh lỗi TypeError.

## Phan_biet_gan_va_so_sanh_bang

### Khái niệm cốt lõi
- Phân biệt toán tử gán giá trị (=) và toán tử kiểm tra sự tương đương (==) trong mã nguồn.

### Cú pháp & Cách khai báo
- Gán giá trị và so sánh:
  ```python
  value = 100
  is_hundred = (value == 100)
  ```

### Lưu ý thực chiến
- Lỗi logic gõ nhầm dấu gán = trong các điều kiện kiểm tra gây lỗi hoặc sai lệch kết quả runtime.
- ![](../images/mindmap_img_2.png)

## Ep_kieu_du_lieu

### Khái niệm cốt lõi
- Chuyển đổi chủ động giá trị từ kiểu dữ liệu gốc sang kiểu dữ liệu đích cần sử dụng (Type Casting).

### Cú pháp & Cách khai báo
- Chuyển đổi sang nguyên, thực, chuỗi:
  ```python
  x = int("12")
  y = float("12.5")
  z = str(100)
  ```

### Lưu ý thực chiến
- Định dạng dữ liệu nguồn không thể ánh xạ (chẳng hạn ép kiểu "abc" sang int) sẽ kích hoạt lỗi ValueError.

## Ham_input

### Khái niệm cốt lõi
- Hàm tích hợp sẵn dùng để tiếp nhận đầu vào nhập từ người dùng thông qua Console dưới dạng chuỗi mặc định.

### Cú pháp & Cách khai báo
- Nhận dữ liệu đầu vào:
  ```python
  user_input = input("Nhập tuổi: ")
  age = int(user_input)
  ```

### Lưu ý thực chiến
- Giá trị trả về từ input() luôn là chuỗi (str) nên bắt buộc phải ép kiểu số trước khi thực hiện so sánh số học.
- ![](../images/mindmap_img_3.png)

## Dinh_dang_chuoi_f_string

### Khái niệm cốt lõi
- Phương pháp nhúng trực tiếp giá trị của biểu thức hoặc biến vào chuỗi văn bản bằng cách đặt tiền tố 'f'.

### Cú pháp & Cách khai báo
- Định dạng f-string:
  ```python
  cart_total = 120.0
  threshold = 100.0
  print(f"Tổng: {cart_total}, điều kiện: {threshold}")
  ```

### Lưu ý thực chiến
- Quên đặt ký tự f trước dấu nháy kép khiến biểu thức trong dấu ngoặc nhọn không định dạng được và hiển thị nguyên bản.

## Chuan_PEP_8

### Khái niệm cốt lõi
- Quy chuẩn định dạng mã nguồn Python chuẩn mực giúp nâng cao tính tường minh và độ dễ đọc của mã.

### Cú pháp & Cách khai báo
- Viết code chuẩn khoảng cách:
  ```python
  a = 5
  b = 10
  result = a >= b
  ```

### Lưu ý thực chiến
- Bắt buộc đặt đúng 1 khoảng cách trắng đơn xung quanh các toán tử gán (=) và toán tử so sánh (==, !=, <, >, <=, >=).
```
```
```