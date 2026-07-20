---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 02 - Lesson 01: Các loại toán tử số học
### Khóa học Lập trình Python Cơ bản

---

## Vấn đề đặt ra
- Học viên mới thường gặp khó khăn trong việc phân biệt các phép chia (`/`, `//`, `%`).
- Dễ mắc sai lầm về thứ tự ưu tiên của các toán tử số học trong biểu thức phức tạp.
- Hậu quả: Dẫn đến kết quả tính toán sai lệch logic hoặc phát sinh lỗi chương trình.

---

## Giải pháp thực thi
- Sử dụng tường minh các toán tử cơ bản kết hợp cặp ngoặc đơn `()` để định rõ quy trình tính toán.
- Thực hiện chuyển đổi kiểu dữ liệu nhận được từ hàm `input()` bằng `int()` hoặc `float()` trước khi tính toán.

---

## 1. Toán tử số học cơ bản
- Là các ký hiệu đặc biệt dùng để thực hiện các phép toán cơ bản trên kiểu dữ liệu số.
- Bao gồm: cộng (`+`), trừ (`-`), nhân (`*`), chia (`/`) và lũy thừa (`**`).

```python
a = 10
b = 3
tong = a + b
hieu = a - b
tich = a * b
thuong = a / b
luy_thua = a ** b
print("Tong:", tong)
print("Hieu:", hieu)
print("Tich:", tich)
print("Thuong:", thuong)
print("Luy thua:", luy_thua)
```

---

## 2. Phân biệt các phép chia (`/`, `//`, `%`)
- **Phép chia thông thường (`/`)**: Trả về kết quả dưới dạng số thực (`float`), kể cả khi chia hết.
- **Phép chia lấy nguyên (`//`)**: Thực hiện phép chia và làm tròn xuống số nguyên gần nhất (loại bỏ phần thập phân).
- **Phép chia lấy dư (`%`)**: Phép toán modulo, trả về phần dư của phép chia nguyên.

---

## Code minh họa phân biệt phép chia

```python
so_bi_chia = 17
so_chia = 5
print("Phep chia lay so thuc (/):", so_bi_chia / so_chia)
print("Phep chia lay nguyen (//):", so_bi_chia // so_chia)
print("Phep chia lay du (%):", so_bi_chia % so_chia)
```

---

## 3. Thứ tự ưu tiên toán tử
- Quy tắc xác định thứ tự thực hiện các phép toán trong biểu thức:
  1. Biểu thức trong ngoặc đơn `()` được ưu tiên hàng đầu.
  2. Phép lũy thừa `**`.
  3. Phép nhân/chia/chia nguyên/chia dư (`*`, `/`, `//`, `%`).
  4. Phép cộng/trừ (`+`, `-`).

---

## Code minh họa thứ tự ưu tiên

```python
ket_qua_mac_dinh = 5 + 2 * 3 ** 2
# 1. Tinh luy thua: 3 ** 2 = 9
# 2. Tinh phep nhan: 2 * 9 = 18
# 3. Tinh phep cong: 5 + 18 = 23

ket_qua_thay_doi = (5 + 2) * 3 ** 2
# 1. Ngoac don truoc: (5 + 2) = 7
# 2. Tinh luy thua: 3 ** 2 = 9
# 3. Tinh phep nhan: 7 * 9 = 63

print("Ket qua mac dinh:", ket_qua_mac_dinh)
print("Ket qua co ngoac don:", ket_qua_thay_doi)
```

---

## 4. Hàm input và chuyển đổi dữ liệu
- Hàm `input()` luôn nhận dữ liệu nhập từ bàn phím dưới dạng chuỗi (`str`).
- Cần chuyển đổi chuỗi sang kiểu số bằng `int()` hoặc `float()` để thực hiện các phép tính số học chính xác.

---

## Code ứng dụng thực tế quy đổi thời gian

```python
# Chuong trinh doi tu so giay sang phut va giay le
tong_so_giay = int(input("Nhap vao tong so giay (so nguyen): "))

so_phut = tong_so_giay // 60
so_giay_du = tong_so_giay % 60

print("Ket qua quy doi:", so_phut, "phut va", so_giay_du, "giay.")
```

---

## Tổng kết & 3 Sai lầm thường gặp
- Nắm vững sự khác biệt của các phép chia và độ ưu tiên toán tử giúp giảm thiểu lỗi logic.
- **Lỗi chia cho số không (`ZeroDivisionError`)**: Xảy ra khi số chia bằng 0.
- **Quên ép kiểu dữ liệu**: Quên chuyển đổi giá trị thu được từ hàm `input()`.
- **Bỏ quên cặp ngoặc đơn**: Làm sai lệch thứ tự tính toán mong muốn đối với các phép cộng, trừ.