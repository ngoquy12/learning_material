```markmap
# Session 01 - Lesson 06: Ép kiểu dữ liệu và f-string

## Nhập dữ liệu với hàm input()
- Cơ chế hoạt động
  - Dừng chương trình chờ người dùng nhập dữ liệu từ bàn phím.
  - Giá trị trả về luôn là kiểu chuỗi (str), kể cả khi nhập số.
  - Ví dụ: Nhập `10` -> Kết quả nhận được là `"10"` (str).
- Hệ quả logic
  - Thực hiện phép toán không số học (nhân chuỗi): `"10" * 3` ra kết quả `"101010"`.
  - ![](../images/mindmap_img_1.png)

## Ép kiểu dữ liệu (Type Casting)
- Ép kiểu tường minh (Explicit Type Casting)
  - Sử dụng các hàm dựng sẵn: `int()` để chuyển sang số nguyên, `float()` để chuyển sang số thực.
  - Chuyển đổi dữ liệu thô từ `input()` thành kiểu số để tính toán.
- Mã nguồn mẫu thực chiến
  - Đoạn mã thực thi:
    ```python
    price_raw = input("Nhập đơn giá: ")
    qty_raw = input("Nhập số lượng: ")
    price = float(price_raw)
    qty = int(qty_raw)
    total = price * qty
    ```
- Cơ chế quản lý bộ nhớ
  - ![](../images/mindmap_img_2.png)

## Định dạng chuỗi nâng cao với f-string
- Cú pháp cơ bản
  - Khai báo bằng tiền tố `f` hoặc `F` trước cặp nháy: `f"Chuỗi {bien}"`.
  - Python tự động tính toán biểu thức hoặc hiển thị giá trị của biến bên trong ngoặc nhọn `{}`.
- Định dạng nâng cao `{gia_tri:dinh_dang}`
  - Làm tròn số thập phân: Sử dụng `:.2f` để lấy 2 chữ số sau dấu phẩy.
  - Phân tách phần nghìn: Sử dụng `,` để tự động thêm dấu phẩy ngăn cách.
- Mã nguồn định dạng hỗn hợp
  - Đoạn mã thực thi:
    ```python
    total = 1250.756
    print(f"Tổng thanh toán: ${total:,.2f}")
    # Kết quả: Tổng thanh toán: $1,250.76
    ```

## Lỗi ngoại lệ thường gặp (Exceptions)
- Lỗi ValueError
  - Nguyên nhân: Ép kiểu chuỗi ký tự không đúng định dạng số.
  - Ví dụ: `int("abc")` hoặc `float("12.3a")`.
- Lỗi TypeError
  - Nguyên nhân: Thực hiện phép toán không hợp lệ giữa các kiểu dữ liệu không tương thích.
  - Ví dụ: Nhân hai chuỗi với nhau `"10" * "5"`.
- Lỗi SyntaxError
  - Nguyên nhân: Viết thiếu tiền tố `f` khi định dạng chuỗi hoặc quên đóng dấu ngoặc nhọn `{}`.
```
```
```