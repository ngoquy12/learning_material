---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 02 - Lesson 03: Toán tử logic
### Khóa học Lập trình Python

---

## 1. Đặt vấn đề

* **Thách thức:** Khi phát triển phần mềm, ta thường phải quyết định hành động dựa trên nhiều điều kiện đồng thời.
  * *Ví dụ:* Làm sao để kiểm tra tuổi người dùng vừa từ 18 đến 60, vừa có sức khỏe tốt?
* **Hạn chế:** Việc lồng nhiều câu lệnh rẽ nhánh `if` phức tạp sẽ làm code bị rối và khó đọc.
* **Giải pháp:** Sử dụng các toán tử logic để kết hợp các phép so sánh một cách tối ưu, ngắn gọn và tường minh nhất.

---

## 2. Các toán tử logic cơ bản

Python hỗ trợ 3 toán tử logic chính hoạt động dựa trên cơ chế đánh giá chân trị (truthy/falsy):

* **`and`**: Trả về `True` nếu cả hai toán hạng đều đúng.
* **`or`**: Trả về `True` nếu ít nhất một toán hạng đúng.
* **`not`**: Phủ định (đảo ngược) giá trị logic của toán hạng.

---

## Demo: Toán tử logic cơ bản

Dưới đây là ví dụ minh họa cách sử dụng các toán tử `and`, `or`, `not`:

```python
# Định nghĩa các giá trị logic cơ bản
mua = True
lanh = False

# Sử dụng and, or, not
mang_o = mua and lanh
di_choi = mua or (not lanh)

print("Mang o:", mang_o)
print("Di choi:", di_choi)
```

---

## 3. Thứ tự ưu tiên của toán tử

Khi đánh giá một biểu thức logic phức tạp, Python tuân theo quy tắc ưu tiên từ cao xuống thấp:

1. **Toán tử so sánh** (`<`, `<=`, `>`, `>=`, `==`, `!=`)
2. **Toán tử phủ định** `not`
3. **Toán tử và** `and`
4. **Toán tử hoặc** `or`

*Khuyến nghị:* Luôn sử dụng cặp ngoặc đơn `()` để ghi đè thứ tự mặc định và giúp biểu thức tường minh hơn.

---

## Demo: Thứ tự ưu tiên và ngoặc đơn

Sử dụng dấu ngoặc đơn giúp lập trình viên kiểm soát chính xác logic mong muốn:

```python
diem = 7.5
chuyen_can = True

# So sánh thực hiện trước, sau đó đến not, and, or
# Sử dụng ngoặc đơn để đảm bảo thứ tự đánh giá mong muốn
thi_dat = (diem >= 5.0 and diem <= 10.0) and (diem >= 8.0 or chuyen_can)
print("Ket qua thi dat:", thi_dat)
```

---

## Application: Kiểm tra đầu vào hợp lệ

Kết hợp toán tử logic để kiểm tra ràng buộc trước khi xử lý dữ liệu:

```python
# Giả lập dữ liệu nhập từ bàn phím
tuoi_str = "25"
if tuoi_str.isdigit():
    tuoi = int(tuoi_str)
    # Sử dụng toán tử logic kiểm tra miền giá trị hợp lệ
    if tuoi >= 18 and tuoi <= 100:
        print("Tuoi hop le de dang ky.")
    else:
        print("Tuoi phai tu 18 den 100.")
else:
    print("Loi: Vui long nhap mot so nguyen.")
```

---

## 4. Cơ chế đánh giá ngắn mạch (Short-circuit)

Cơ chế ngắn mạch giúp tăng hiệu năng bằng cách dừng đánh giá biểu thức ngay khi biết chắc kết quả:

* **Đối với `and`**: Nếu toán hạng đầu tiên là `False`, kết quả chắc chắn là `False` -> Toán hạng thứ hai sẽ không được đánh giá.
* **Đối với `or`**: Nếu toán hạng đầu tiên là `True`, kết quả chắc chắn là `True` -> Toán hạng thứ hai sẽ bị bỏ qua.

Cơ chế này cực kỳ hữu ích để ngăn ngừa lỗi phát sinh ở vế sau (ví dụ: chia cho 0).

---

## Demo: Tối ưu ngắn mạch chống lỗi

Ngăn lỗi `ZeroDivisionError` bằng cách đưa điều kiện kiểm tra an toàn lên trước:

```python
so_chia = 0
tu_so = 10

# Ngăn lỗi ZeroDivisionError bằng cách kiểm tra so_chia != 0 trước
# Nếu so_chia == 0 là False, phép chia ở vế sau sẽ không được thực hiện
if so_chia != 0 and (tu_so / so_chia > 2):
    print("Thoa man dieu kien kiem tra")
else:
    print("Khong hop le hoac so chia bang 0")
```

---

## 5. Tự động sinh bảng chân trị (Truth Table)

Bảng chân trị giúp ta hệ thống hóa và kiểm chứng tính tương đương logic của các biểu thức phức tạp.

* Quy trình sinh tự động: Sử dụng các vòng lặp lồng nhau duyệt qua tập hợp các giá trị chân lý `{True, False}` của từng biến độc lập để tính toán giá trị đầu ra.

---

## Demo: Sinh bảng chân trị tự động

Đoạn code sau tự động hóa việc xuất bảng chân trị cho biểu thức `A and (not B)`:

```python
# Tự động xuất bảng chân trị cho biểu thức logic: A and (not B)
print("A     | B     | A and (not B)")
print("-" * 30)

# Duyệt qua các tổ hợp chân trị của 2 biến
for A in [True, False]:
    for B in [True, False]:
        ket_qua = A and (not B)
        print(f"{str(A):<5} | {str(B):<5} | {str(ket_qua)}")
```

---

## 6. Tổng kết & Lỗi thường gặp

**Tổng kết:** Các toán tử logic `and`, `or`, `not` kết hợp với các phép so sánh giúp chương trình rẽ nhánh hiệu quả và tối ưu.

**3 lỗi phổ biến cần tránh:**
1. **Sai thứ tự ưu tiên:** Quên dùng ngoặc đơn khiến toán tử `and` chạy trước `or` làm sai lệch kết quả.
2. **Ngăn mạch ngoài ý muốn:** Đưa biểu thức nặng hoặc dễ phát sinh lỗi lên trước biểu thức kiểm tra an toàn.
3. **Mơ hồ Truthy/Falsy:** Đánh giá nhầm lẫn giá trị rỗng (số 0, chuỗi rỗng `""`) dẫn đến logic hoạt động không như kỳ vọng.