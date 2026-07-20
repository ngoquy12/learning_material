---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 02 - Lesson 02: Toán tử so sánh
Chương trình học Python cơ bản

---

## Đặt vấn đề

* Khi viết ứng dụng, chương trình cần đưa ra quyết định tương tác dựa trên điều kiện thực tế.
  * Ví dụ: Kiểm tra tài khoản có đủ số dư, kiểm tra người dùng đủ tuổi đăng ký.
* Nếu thiếu khả năng so sánh đối chiếu giá trị:
  * Lập trình viên không thể điều hướng luồng xử lý hoặc rẽ nhánh chương trình.
  * Không thể kiểm tra tính đúng đắn của dữ liệu đầu vào.

---

## Phân tích: Toán tử & Kiểu Boolean

* **Kiểu dữ liệu Boolean**: Chỉ gồm hai giá trị là `True` (đúng) và `False` (sai).
* **Biểu thức so sánh**: Sử dụng các toán tử so sánh để đánh giá mối quan hệ giữa các dữ liệu và trả về một giá trị Boolean.
* **6 toán tử so sánh cơ bản**:
  * So sánh bằng: `==`
  * So sánh khác: `!=`
  * Lớn hơn: `>` | Nhỏ hơn: `<`
  * Lớn hơn hoặc bằng: `>=` | Nhỏ hơn hoặc bằng: `<=`

---

## Code Demo: Toán tử so sánh cơ bản

```python
a = 15
b = 10

print("a == b:", a == b)  # False
print("a != b:", a != b)  # True
print("a > b:", a > b)    # True
print("a < b:", a < b)    # False
print("a >= b:", a >= b)  # True
print("a <= b:", a <= b)  # False
```

---

## Phân biệt Gán (=) và So sánh bằng (==)

* **Toán tử gán (`=`)**:
  * Được dùng để gán giá trị cho một biến.
  * Ví dụ: `x = 5` (lưu giá trị 5 vào vùng nhớ của biến x).
* **Toán tử so sánh bằng (`==`)**:
  * Được dùng để so khớp giá trị của hai vế xem có bằng nhau hay không.
  * Kết quả luôn trả về kiểu Boolean (`True` hoặc `False`).

---

## Code Demo: Gán và So sánh

```python
# Gan gia tri cho bien
x = 10
y = 20

# So sanh hai gia tri
ket_qua = (x == y)
print("Gia tri cua x:", x)
print("Gia tri cua y:", y)
print("x co bang y khong?:", ket_qua)
```

---

## Quy tắc so sánh Chuỗi và Số

* **So sánh số**: Python so sánh dựa trên giá trị số học thuần túy.
* **So sánh chuỗi**:
  * Python so sánh từng ký tự từ trái qua phải dựa trên mã Unicode tương ứng (ví dụ: `'a'` có mã nhỏ hơn `'b'`).
  * Đối với chuỗi có cùng ký tự nhưng độ dài khác nhau, chuỗi ngắn hơn sẽ nhỏ hơn.
* **Lỗi TypeError**: Không thể so sánh trực tiếp chuỗi với số bằng các toán tử `>`, `<`, `>=`, `<=` vì không tương thích kiểu dữ liệu.

---

## Code Demo: So sánh Chuỗi và Số

```python
# So sanh so
print(10.5 > 10)  # True

# So sanh chuoi theo thu tu alphabet (ma Unicode)
print("apple" < "banana")  # True vi 'a' dung truoc 'b'
print("Alice" == "alice")  # False vi phan biet chu hoa chu thuong

# So sanh chuoi co cung ky tu nhung do dai khac nhau
print("app" < "apple")    # True
```

---

## Biểu thức logic trong thực tế

* Xây dựng các biểu thức so sánh giúp giải quyết các bài toán kiểm tra điều kiện thực tế:
  * Kiểm tra độ tuổi hợp lệ (ví dụ: `tuoi >= 18`).
  * Xếp loại điểm số (ví dụ: `diem_so >= 5.0`).
* **Chuỗi so sánh liên tiếp**:
  * Python hỗ trợ kiểm tra một khoảng giá trị một cách tự nhiên.
  * Ví dụ: `18 <= tuoi <= 60` (kiểm tra độ tuổi lao động).

---

## Code Demo: Điều kiện thực tế

```python
# Kiem tra tuoi bau cu
tuoi = 20
co_quyen_bau_cu = tuoi >= 18
print("Co quyen bau cu?:", co_quyen_bau_cu)

# Kiem tra diem dat / truot
diem_so = 4.5
status_pass = diem_so >= 5.0
print("Da dat yeu cau?:", status_pass)

# Kiem tra do tuoi lao dong (trong khoang 18 den 60)
tuoi_lao_dong = 18 <= tuoi <= 60
print("Trong do tuoi lao dong?:", tuoi_lao_dong)
```

---

## Tổng kết & 3 lỗi thường gặp

* **Tổng kết**: Toán tử so sánh luôn trả về giá trị Boolean hỗ trợ rẽ nhánh luồng xử lý hoặc kiểm tra tính đúng đắn dữ liệu.
* **3 lỗi thường gặp cần tránh**:
  1. **Nhầm lẫn giữa toán tử gán (`=`) và so sánh bằng (`==`)**: Làm sai lệch logic hoặc gây lỗi cú pháp.
  2. **So sánh trực tiếp giữa chuỗi ký tự và số**: Sử dụng `>`, `<`, `>=`, `<=` giữa chuỗi và số sẽ phát sinh lỗi `TypeError`.
  3. **Bỏ qua quy tắc so sánh chữ hoa - chữ thường**: Do mã Unicode của chữ hoa và chữ thường khác nhau nên kết quả so sánh chuỗi sẽ sai lệch nếu bỏ qua yếu tố này.