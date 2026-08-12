# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn xác thực duyệt voucher ShopeeFood lồng nhau:

```python
is_user_active = True
order_amount = 600000

if is_user_active:
    if order_amount >= 500000:
        voucher_status = "Áp dụng thành công"
    else:
        voucher_status = "Chưa đủ giá trị đơn 500k"
else:
    voucher_status = "Tài khoản không hợp lệ"
```

---

### Câu 1: Khi biến đầu vào là `is_user_active = True` và `order_amount = 600000`, hãy giải thích luồng thực thi của từng cấp rẽ nhánh `if` lồng nhau và xác định giá trị biến `voucher_status`.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Vòng ngoài: Điều kiện `is_user_active` (True) thỏa mãn ➔ Hệ thống đi vào khối rẽ nhánh bên trong.
> - Vòng trong: Điều kiện `order_amount >= 500000` (600000 >= 500000) thỏa mãn ➔ Thực thi gán `voucher_status = 'Áp dụng thành công'`.

---

### Câu 2: Áp dụng nguyên tắc tối ưu hóa mã nguồn theo quy chuẩn PEP 8, hãy viết lại đoạn mã rẽ nhánh lồng nhau trên thành một câu lệnh `if-else` phẳng duy nhất sử dụng toán tử logic `and`.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Đoạn mã phẳng chuẩn PEP 8:
> ```python
> if is_user_active and order_amount >= 500000:
>     voucher_status = "Áp dụng thành công"
> else:
>     voucher_status = "Không đủ điều kiện"
> ```

---

### Câu 3: Hãy nêu 2 quy tắc thụt lùi dòng (Indentation) và khoảng trắng xung quanh toán tử theo chuẩn PEP 8 để tránh gây lỗi `IndentationError` và `TabError` khi lập trình Python.
> **Gợi ý trả lời & Định hướng đáp án:**
> 1. Thụt lùi dòng: Bắt buộc dùng đúng 4 khoảng trắng (spaces) cho mỗi cấp độ lồng nhau, không trộn lẫn phím Tab và phím Space.
> 2. Khoảng trắng: Đặt đúng 1 khoảng trắng trước và sau các toán tử gán (`=`) và so sánh (`>=`).
