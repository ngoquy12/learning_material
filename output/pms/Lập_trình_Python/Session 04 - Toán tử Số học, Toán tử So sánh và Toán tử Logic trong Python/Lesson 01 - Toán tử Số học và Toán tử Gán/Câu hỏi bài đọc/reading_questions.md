# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions) - Lesson 01

## Tình huống & Mã nguồn kiểm tra

Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc về tính toán đơn hàng ShopeeFood:

```python
# Thông số đơn hàng cơm tấm
price = 55000        # Đơn giá một phần cơm tấm (VNĐ)
quantity = 3         # Số lượng mua
shipping = 22000     # Phí giao hàng (VNĐ)
voucher = 15000      # Mã giảm giá voucher (VNĐ)
wallet = 100000      # Số dư ví điện tử ban đầu (VNĐ)

# Tính toán các chỉ số thanh toán
subtotal = price * quantity
discounted_subtotal = subtotal - voucher
total_payment = discounted_subtotal + shipping
cashback = subtotal * 0.1
wallet += cashback
```

---

### Câu 1: Tính toán giá trị của `subtotal` và `total_payment` từ đoạn mã trên. Giải thích các phép toán đã sử dụng.

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - `subtotal = 55000 * 3 = 165000` VNĐ (Sử dụng toán tử nhân `*`).
> - `discounted_subtotal = 165000 - 15000 = 150000` VNĐ.
> - `total_payment = 150000 + 22000 = 172000` VNĐ (Sử dụng toán tử cộng `+` và trừ `-`).

---

### Câu 2: Giá trị của biến `cashback` là bao nhiêu và nó mang kiểu dữ liệu gì trong Python? Tại sao?

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - `cashback = 165000 * 0.1 = 16500.0`.
> - Kiểu dữ liệu của `cashback` là `float`. Nguyên nhân là do phép nhân giữa một số nguyên (`int`) và một số thực (`0.1`) luôn trả về kiểu số thực (`float`) trong Python.

---

### Câu 3: Sau khi thực thi toàn bộ đoạn mã trên, số dư ví điện tử `wallet` cuối cùng của khách hàng là bao nhiêu? Giải thích cơ chế hoạt động của toán tử gán gộp `+=`.

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Số dư cuối cùng là `116500.0` VNĐ.
> - Toán tử gán gộp `wallet += cashback` tương đương với `wallet = wallet + cashback`. Nó lấy giá trị hiện tại của `wallet` (`100000`), cộng thêm `cashback` (`16500.0`) rồi gán ngược lại kết quả cho biến `wallet`.

---

### Câu 4: Nếu khách hàng tăng số lượng mua thêm 2 phần cơm tấm nữa (`quantity += 2`), hãy viết biểu thức sử dụng toán tử gán gộp để cập nhật lại biến `quantity`.

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Biểu thức cập nhật: `quantity += 2`.
> - Dòng lệnh này giúp tăng giá trị hiện tại của `quantity` từ `3` lên `5` trước khi thực hiện các bước tính toán tiếp theo.
