marp: true
theme: gaia
_class: lead
paginate: true

---

# Session 01 - Lesson 04
## Nhập xuất dữ liệu & Ép kiểu dữ liệu

---

# Vấn đề thực tế

- Tương tác với người dùng qua bàn phím là cốt lõi của ứng dụng dòng lệnh (CLI).
- Hàm `input()` luôn trả về kiểu dữ liệu chuỗi (`str`).
- Thực hiện phép tính trực tiếp trên kết quả của `input()` sẽ gây lỗi hoặc cho ra kết quả không mong muốn (ví dụ: ghép chuỗi thay vì cộng số).

---

# Hàm Nhập / Xuất Cơ Bản

- **Hàm `input()`**:
  - Hàm built-in dùng để tạm dừng chương trình và nhận dữ liệu nhập vào từ bàn phím.
  - Kết quả trả về luôn luôn là một chuỗi ký tự (`str`).
- **Hàm `print()`**:
  - Hàm built-in dùng để xuất dữ liệu hoặc thông điệp ra màn hình console.
  - Có thể nhận nhiều đối số và kết hợp định dạng đầu ra linh hoạt.

---

# Demo: Nhập xuất dữ liệu cơ bản

```python
ten = input("Nhap ten cua ban: ")
tuoi = input("Nhap tuoi cua ban: ")
print("Xin chao", ten, "-", tuoi, "tuoi")
```

---

# Ép kiểu dữ liệu (Type Casting)

- **Định nghĩa**: Là quá trình chuyển đổi giá trị của một biến từ kiểu dữ liệu này sang kiểu dữ liệu khác.
- **Mục đích**: Chuyển từ chuỗi văn bản (`str`) sang số nguyên (`int`) hoặc số thực (`float`) để thực hiện các phép toán số học.
- **Hàm hỗ trợ**:
  - `int()`: Ép kiểu sang số nguyên
  - `float()`: Ép kiểu sang số thực

---

# Demo: Ép kiểu dữ liệu

```python
so_nguyen_str = "25"
so_thuc_str = "10.5"

# Ep kieu sang so de tinh toan
so_nguyen = int(so_nguyen_str)
so_thuc = float(so_thuc_str)

tong = so_nguyen + so_thuc
print("Tong gia tri:", tong)
```

---

# Lỗi giá trị (ValueError) trong ép kiểu

- Là một dạng lỗi Runtime (Runtime Error) xảy ra trong quá trình chạy chương trình.
- Xảy ra khi các hàm ép kiểu như `int()` hoặc `float()` nhận vào một chuỗi không đúng định dạng số.
- Ví dụ: Cố gắng ép kiểu chuỗi `"abc"` hoặc `"12a"` thành số sẽ gây ra lỗi `ValueError`.

---

# Quy trình thiết kế chương trình CLI

1. **Nhận dữ liệu**: Sử dụng hàm `input()` để lấy dữ liệu dạng chuỗi từ người dùng.
2. **Xử lý (Ép kiểu)**: Dùng `int()` hoặc `float()` để đưa dữ liệu về dạng số học.
3. **Tính toán**: Thực hiện các công thức toán học trên dữ liệu đã ép kiểu.
4. **Xuất kết quả**: Định dạng và hiển thị kết quả ra màn hình bằng hàm `print()`.

---

# Demo: Chương trình CLI hoàn chỉnh

```python
# Buoc 1: Nhap du lieu
ten_san_pham = input("Nhap ten san pham: ")
so_luong_str = input("Nhap so luong: ")
don_gia_str = input("Nhap don gia: ")

# Buoc 2: Xu ly (Ep kieu va tinh toan)
so_luong = int(so_luong_str)
don_gia = float(don_gia_str)
thanh_tien = so_luong * don_gia

# Buoc 3: Xuat ban tin
print("--- THONG TIN DON HANG ---")
print("Ten san pham:", ten_san_pham)
print("So luong:", so_luong)
print("Don gia:", don_gia, "VND")
print("Thanh tien:", thanh_tien, "VND")
```

---

# Tổng kết & 3 Sai lầm cần tránh

- Chương trình tương tác chuẩn cần kết hợp chặt chẽ: Nhập (`input`) $\rightarrow$ Ép kiểu (`int`/`float`) $\rightarrow$ Xuất (`print`).
- **3 Sai lầm phổ biến cần tránh**:
  1. Quên chuyển đổi kiểu dữ liệu (gây ghép chuỗi thay vì tính toán).
  2. Ép kiểu chuỗi ký tự chứa chữ hoặc định dạng sai (gây ra lỗi `ValueError`).
  3. Thiếu các bước kiểm tra logic nghiệp vụ (ví dụ: chấp nhận số lượng hoặc đơn giá âm).