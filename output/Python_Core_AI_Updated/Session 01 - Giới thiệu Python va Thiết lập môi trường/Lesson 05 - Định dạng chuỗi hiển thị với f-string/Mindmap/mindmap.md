```markmap
# Session 01: Định dạng chuỗi hiển thị với f-string

## Mục tiêu bài học
- Nắm vững cú pháp f-string để hiển thị thông tin trực quan và tối ưu hơn phương pháp truyền thống.
- Làm chủ kỹ thuật làm tròn số thực, hiển thị số lớn và can lề dữ liệu dạng bảng.
- Nhận biết và phòng ngừa các lỗi cú pháp phổ biến khi sử dụng f-string.

## Định dạng f-string cơ bản
### Khái niệm cốt lõi
Dạng định dạng chuỗi trực quan bằng cách chèn trực tiếp các biến hoặc biểu thức vào bên trong cặp dấu ngoặc nhọn của chuỗi ký tự có tiền tố f hoặc F.
### Cú pháp & Cách khai báo
- Cú pháp mẫu khai báo f-string cơ bản:
  ```python
  name = "Nam"
  content = f"Xin chao {name}"
  print(content)
  ```
### Lưu ý thực chiến
Cho phép thực thi biểu thức toán học hoặc gọi phương thức xử lý chuỗi trực tiếp bên trong cặp ngoặc nhọn.

## Phương pháp định dạng truyền thống
### Khái niệm cốt lõi
Các phương pháp định dạng chuỗi trước phiên bản Python 3.6, bao gồm sử dụng toán tử phần trăm hoặc gọi phương thức format.
### Cú pháp & Cách khai báo
- Cú pháp mẫu sử dụng toán tử phần trăm và phương thức format:
  ```python
  name = "Nam"
  # Dinh dang qua toan tu phan tram
  print("Xin chao %s" % name)
  # Dinh dang qua phuong thuc format
  print("Xin chao {}".format(name))
  ```
### Lưu ý thực chiến
Phương pháp truyền thống dễ gây nhầm lẫn khi truyền nhiều tham số và làm giảm tốc độ thực thi so với f-string.

## Định dạng số thực và số lớn
### Khái niệm cốt lõi
Cơ chế kiểm soát số lượng chữ số thập phân hiển thị và phân tách nhóm hàng nghìn bằng dấu phẩy để dữ liệu số dễ đọc hơn.
### Cú pháp & Cách khai báo
- Cú pháp định dạng số thực và phân tách hàng nghìn:
  ```python
  gpa = 8.5678
  population = 97000000
  # Lam tron 2 chu so thap phan
  print(f"GPA: {gpa:.2f}")
  # Phan tach hang nghin bang dau phay
  print(f"Dan so: {population:,}")
  ```
### Lưu ý thực chiến
Quên ký tự hai chấm trước phần chỉ dẫn định dạng sẽ gây lỗi cú pháp. Không áp dụng định dạng số cho biến kiểu chuỗi chưa ép kiểu.

## Căn lề dữ liệu
### Khái niệm cốt lõi
Cách căn chỉnh dữ liệu sang trái, sang phải hoặc căn giữa trong một khoảng không gian ký tự xác định để tạo cấu trúc cột thẳng hàng.
### Cú pháp & Cách khai báo
- Cú pháp căn lề trái và lề phải kèm độ rộng:
  ```python
  name = "Nam"
  gpa = 8.5678
  # Can le trai voi do rong 10 va le phai voi do rong 5
  print(f"{'Ten':<10} | {'Diem':>5}")
  print(f"{name:<10} | {gpa:>5.1f}")
  ```
- ![](../images/mindmap_img_1.png)
### Lưu ý thực chiến
Nhập sai thứ tự định dạng sẽ sinh lỗi. Phải xác định trước độ rộng tối đa của chuỗi để tránh việc dữ liệu bị đè hoặc lệch cột.

## Tránh lỗi cú pháp f-string
### Khái niệm cốt lõi
Các quy tắc kết hợp dấu nháy và ký hiệu ngoặc nhọn để không làm vỡ cấu trúc chuỗi hoặc phát sinh lỗi biên dịch.
### Cú pháp & Cách khai báo
- Cú pháp xử lý dấu nháy và in ngoặc nhọn vật lý:
  ```python
  name = "Nam"
  # In ngoac nhon vat ly bang double bracket
  print(f"JSON: {{ 'name': '{name}' }}")
  ```
### Lưu ý thực chiến
Không sử dụng cùng một loại dấu nháy đơn hoặc nháy kép cho cả bao chuỗi và biểu thức bên trong vì sẽ làm phát sinh lỗi SyntaxError.
```
```
```