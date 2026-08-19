# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions) - Lesson 02

## Tình huống & Mã nguồn kiểm tra

Dựa trên mã nguồn nghiệp vụ xét duyệt ưu đãi vận chuyển và quà tặng đơn hàng ShopeeFood:

```python

# Thông số đơn hàng hiện tại
order_amount = 350000

# Tổng tiền đơn hàng (VNĐ)
distance = 4.5

# Khoảng cách giao hàng (km)
is_vip = True

# Khách hàng là thành viên VIP

# Kiểm tra các điều kiện logic
is_freeship = (order_amount >= 300000) or (is_vip and distance <= 5.0)
is_high_value = order_amount > 500000
is_near = distance < 2.0
```

---

### Câu 1: Xác định giá trị Boolean (True/False) của biến `is_freeship` trong trường hợp này. Giải thích cụ thể luồng tính toán.

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Biểu thức thứ nhất: `order_amount >= 300000` (350000 >= 300000) trả về `True`.
> - Do toán tử `or` có tính chất đánh giá ngắn mạch, khi vế trái đã là `True`, Python ngay lập tức kết luận kết quả chung của `is_freeship` là `True` mà không cần tính toán tiếp vế phải.

---

### Câu 2: Xác định giá trị Boolean của `is_high_value` và `is_near` trên bộ dữ liệu mẫu này.

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - `is_high_value = 350000 > 500000` trả về `False`.
> - `is_near = 4.5 < 2.0` trả về `False`.

---

### Câu 3: Nếu khách hàng đổi trạng thái VIP thành thường (`is_vip = False`), giá trị của `is_freeship` có bị thay đổi không? Tại sao?

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Giá trị của `is_freeship` **không thay đổi** (vẫn là `True`).
> - Vì điều kiện thứ nhất `order_amount >= 300000` vẫn thỏa mãn (`True`). Với toán tử `or`, chỉ cần một trong hai vế đúng thì kết quả là `True`.

---

### Câu 4: Hãy giải thích tại sao biểu thức kiểm tra `order_amount == "350000"` lại trả về kết quả `False` mặc dù giá trị đơn hàng là 350.000?

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Trong Python, toán tử so sánh bằng `==` kiểm tra cả giá trị và sự tương đương kiểu dữ liệu.
> - Biến `order_amount` là kiểu số (`int` hoặc `float`), trong khi `"350000"` là kiểu chuỗi ký tự (`str`). Python so sánh khác kiểu dữ liệu nên luôn trả về `False` mà không tự động ép kiểu ngầm định.
