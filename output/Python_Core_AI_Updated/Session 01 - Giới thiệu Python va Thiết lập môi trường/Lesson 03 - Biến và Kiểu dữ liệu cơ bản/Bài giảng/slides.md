---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 01 - Lesson 03<br>Biến và Kiểu dữ liệu cơ bản

Cơ chế lưu trữ và phân loại dữ liệu trong Python

---

## Đặt vấn đề

Khi viết chương trình, máy tính cần lưu trữ các thông tin tạm thời như:
- Thông số cài đặt
- Dữ liệu người dùng
- Trạng thái hệ thống

**Hậu quả nếu thiếu cơ chế lưu trữ và phân loại:**
- Máy tính không thể định vị vùng nhớ trong RAM.
- Hệ thống không hiểu và xử lý chính xác các thông số.
- Chương trình không thể vận hành.

---

## Cơ chế biến trong Python (Dynamic Typing)

- **Định kiểu động:** Python tự động xác định kiểu dữ liệu mà không cần khai báo trước.
- **Bản chất của biến:** Biến không chứa trực tiếp dữ liệu. Nó hoạt động như một nhãn tham chiếu trỏ đến đối tượng lưu trữ trong bộ nhớ RAM.
- **Phép gán (`=`):** Sử dụng toán tử `=` để đưa giá trị hoặc kết quả từ vế phải vào biến ở vế trái.

---

## 4 Kiểu dữ liệu cơ bản

- **int (Integer):** Kiểu số nguyên, không chứa phần thập phân (Ví dụ: `10`, `-5`).
- **float (Floating-point):** Kiểu số thực, có phần thập phân ngăn cách bởi dấu chấm (Ví dụ: `3.14`, `-0.01`).
- **str (String):** Kiểu chuỗi ký tự biểu diễn văn bản, đặt trong cặp nháy đơn `'...'` hoặc nháy kép `"..."` (Ví dụ: `"Hello"`).
- **bool (Boolean):** Kiểu logic chỉ nhận một trong hai giá trị duy nhất là `True` hoặc `False`.

---

## Demo: Khai báo & Phân biệt kiểu dữ liệu

Dưới đây là cách khai báo các biến cơ bản trong Python:

```python
name = "Nguyen Van A"
age = 18
is_student = True

print(name)
print(age)
print(is_student)
```

Kiểu dữ liệu thực tế được gán cho từng biến:

```python
so_nguyen = 25
so_thuc = 7.82
chuoi_ky_tu = "Lap trinh Python co ban"
logic_dung = True
logic_sai = False
```

---

## Quy tắc đặt tên biến

Để tránh lỗi cú pháp (Syntax Error), tên biến phải tuân theo các quy tắc bắt buộc:

- Chỉ chứa chữ cái, chữ số và dấu gạch dưới (`_`).
- Bắt đầu bằng chữ cái hoặc dấu gạch dưới, không được bắt đầu bằng chữ số.
- Không chứa khoảng trắng và các ký tự đặc biệt.
- Không trùng với các từ khóa mặc định của Python (Ví dụ: `class`, `if`, `import`).
- Có phân biệt chữ hoa và chữ thường (Ví dụ: `age` khác `Age`).

---

## Kiểm tra kiểu dữ liệu

Python cung cấp hai hàm tích hợp sẵn để kiểm tra và xuất dữ liệu:
- **Hàm `print()`:** Xuất dữ liệu hoặc giá trị của biến ra màn hình console.
- **Hàm `type()`:** Trả về kiểu dữ liệu thực tế của biến hoặc giá trị được truyền vào.

```python
message = "Hello World"
number = 100
pi_value = 3.14
status = False

print(type(message))
print(type(number))
print(type(pi_value))
print(type(status))
```

---

## 3 Lỗi phổ biến cần tránh

- **Sai quy tắc đặt tên:** Đặt tên chứa ký tự đặc biệt hoặc bắt đầu bằng số.
  * *Sai:* `1st_value = 10`
  * *Sai:* `my-var = 5`
- **Sử dụng từ khóa hệ thống:** Dùng các từ khóa dành riêng cho ngôn ngữ.
  * *Sai:* `class = 5`
- **Viết sai chuẩn kiểu logic:** Nhầm lẫn viết thường từ khóa boolean.
  * *Sai:* `is_active = true` (Phải viết chính xác là `True`).

---

## Thực hành sửa lỗi & Script hoàn chỉnh

Ví dụ về cách tránh lỗi cú pháp và kiểm tra kiểu dữ liệu theo đúng chuẩn Python:

```python
# Vi du loi cu phap: 1st_num = 10 (Dat ten bat dau bang so se gay SyntaxError)
# Vi du loi cu phap: my-var = 5 (Dung dau gach ngang se gay SyntaxError)

# Day la script hoan chinh dung cu phap va kiem tra kieu du lieu:
num_score = 10
price = 99.9
product_name = "Sach giao khoa"
is_available = True

print("Kieu cua num_score:", type(num_score))
print("Kieu cua price:", type(price))
print("Kieu cua product_name:", type(product_name))
print("Kieu cua is_available:", type(is_available))
```

---

## Tổng kết bài học

- **Biến** là nhãn tham chiếu đến vùng nhớ RAM dùng để lưu trữ dữ liệu.
- Phép gán được thực hiện qua toán tử `=`.
- Sử dụng hàm `print()` để in dữ liệu và `type()` để kiểm tra kiểu dữ liệu.
- Luôn luôn nhớ:
  * Tránh đặt tên biến bắt đầu bằng số hoặc chứa ký tự đặc biệt.
  * Không dùng từ khóa hệ thống làm tên biến.
  * Viết hoa chữ cái đầu cho kiểu bool: `True` và `False`.