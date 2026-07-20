---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 01 - Lesson 05
## Định dạng chuỗi hiển thị với f-string

Giảng viên: [Tên giảng viên]
Bộ môn: Khoa học máy tính / Lập trình Python

---

### Đặt vấn đề

* **Nhu cầu thực tế**: Khi phát triển phần mềm, ta thường phải in kết quả ra màn hình ở dạng bảng biểu, hóa đơn hoặc định dạng dữ liệu JSON.
* **Hạn chế của phương pháp cũ**: 
  * Sử dụng toán tử `%` hoặc phương thức `.format()` làm mã nguồn dài dòng, khó đọc.
  * Dễ xảy ra lỗi khi số lượng biến truyền vào lớn hoặc thứ tự đối số bị sai lệch.

---

### So sánh các phương pháp định dạng

Dưới đây là sự khác biệt giữa các phương pháp định dạng chuỗi trong Python:

```python
name = 'Nam'
age = 18

# Cách 1: Sử dụng toán tử cũ %
print('1. Cách %%: Xin chào %s, %d tuổi.' % (name, age))

# Cách 2: Sử dụng phương thức .format()
print('2. Cách .format(): Xin chào {}, {} tuổi.'.format(name, age))

# Cách 3: Sử dụng f-string (Khuyên dùng)
print(f'3. Cách f-string: Xin chào {name}, {age} tuổi.')
```

---

### Phân tích cú pháp f-string

* **Cú pháp cơ bản**: Bắt đầu bằng chữ `f` hoặc `F` trước dấu nháy. Các biểu thức bên trong cặp ngoặc nhọn `{}` sẽ được tính toán trực tiếp tại thời điểm chạy.
* **Bộ chỉ thị định dạng căn lề**:
  * `:<N`: Căn trái với độ rộng cột `N`
  * `:>N`: Căn phải với độ rộng cột `N`
  * `:^N`: Căn giữa với độ rộng cột `N`
* **Bộ chỉ thị định dạng số**:
  * `:.2f`: Làm tròn số thập phân (ví dụ lấy 2 chữ số sau dấu phẩy)
  * `:,`: Thêm dấu phẩy phân tách hàng nghìn

---

### Minh họa: Định dạng số và Căn lề cột

```python
gpa = 8.5678
population = 97000000

# Định dạng số thực 2 chữ số thập phân và thêm dấu phẩy hàng nghìn
print(f'Điểm trung bình: {gpa:.2f}')
print(f'Dân số Việt Nam: {population:,} người')

# Căn lề cột dữ liệu (tên 10 ký tự căn trái, điểm 5 ký tự căn phải)
print(f"{'Tên':<10} | {'Điểm':>5}")
print('-' * 18)
print(f"{'An':<10} | {8.5:>5.1f}")
print(f"{'Bình':<10} | {10.0:>5.1f}")
```

---

### Giải pháp cho dữ liệu phức tạp & JSON

* **Hiển thị cặp ngoặc nhọn**: Khi cần in ra ký tự `{` hoặc `}` vật lý (ví dụ: tạo chuỗi JSON định dạng sẵn), ta cần viết đúp thành `{{` và `}}`.
* Trình biên dịch sẽ hiểu đó là ký tự ngoặc nhọn văn bản thông thường thay vì một biểu thức cần nội suy giá trị.

---

### Minh họa: Xuất hóa đơn & JSON thực tế

```python
san_pham = 'Sách Python'
gia_ban = 120000
soluong = 3
thanh_tien = gia_ban * soluong

# Hiển thị dấu ngoặc nhọn bằng cách viết đúp {{ }}
print(f"Dữ liệu JSON: {{ 'san_pham': '{san_pham}', 'tong': {thanh_tien} }}")

# In hóa đơn căn lề chuyên nghiệp
print()
print('--- HÓA ĐƠN BÁN HÀNG ---')
print(f"{'Tên hàng':<15}{'SL':<5}{'Đơn giá':>10}{'Thành tiền':>12}")
print('-' * 42)
print(f"{san_pham:<15}{soluong:<5}{gia_ban:>10,}{thanh_tien:>12,}")
```

---

### Tổng kết & 3 lỗi thường gặp cần tránh

* **Trùng dấu nháy**: Sử dụng cùng một loại dấu nháy đơn hoặc nháy kép cho cả f-string bên ngoài và chuỗi bên trong `{}`.
  * *Sai*: `f"Hello {"Nam"}"`
  * *Đúng*: `f"Hello {'Nam'}"`
* **Thiếu ký tự f**: Quên đặt `f` hoặc `F` ở đầu chuỗi khiến biểu thức ngoặc nhọn bị giữ nguyên dưới dạng văn bản thuần túy.
* **Nhầm lẫn cú pháp căn lề**: Nhầm lẫn giữa chiều của dấu `<` (căn trái) và `>` (căn phải).