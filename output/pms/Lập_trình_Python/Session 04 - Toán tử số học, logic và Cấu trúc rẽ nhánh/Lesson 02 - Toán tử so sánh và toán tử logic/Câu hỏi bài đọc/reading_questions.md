# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên đoạn mã xác thực điều kiện ưu đãi đơn hàng ShopeeFood:

```python
order_amount = 250000
is_vip_member = True
has_voucher = True

is_eligible_freeship = (order_amount >= 200000) and is_vip_member
```

---

### Câu 1: Phân tích giá trị chân lý của từng biểu thức thành phần trong câu lệnh xác thực freeship trên (`order_amount >= 200000` và `is_vip_member`) và giải thích vì sao cờ hiệu `is_eligible_freeship` lại nhận giá trị `True`.
> **Gợi ý trả lời & Định hướng đáp án:**
> 1. Biểu thức `order_amount >= 200000`: Thay giá trị `order_amount = 250000`, phép so sánh `250000 >= 200000` trả về giá trị `True`.
> 2. Biến `is_vip_member`: Khởi tạo sẵn mang giá trị `True`.
> 3. Kết hợp toán tử logic `AND`: Biểu thức `True and True` cho kết quả cuối cùng là `True`. Do đó, cờ hiệu `is_eligible_freeship` nhận giá trị `True`.

---

### Câu 2: Giải thích cơ chế đánh giá ngắn mạch (Short-circuit Evaluation) của toán tử logic `and` và `or` trong Python. Trong hệ thống xử lý hàng triệu đơn hàng ShopeeFood, việc chủ động đặt điều kiện có tỷ lệ vi phạm cao lên đầu biểu thức `and` mang lại lợi ích gì về hiệu năng?
> **Gợi ý trả lời & Định hướng đáp án:**
> 1. Quy tắc cơ chế Short-circuit Evaluation:
>    - Đối với toán tử `and`: Nếu vế trái đánh giá ra `False`, toàn bộ biểu thức chắc chắn là `False`, Python dừng tính toán ngay và không đánh giá vế phải.
>    - Đối với toán tử `or`: Nếu vế trái ra `True`, toàn bộ biểu thức chắc chắn `True`, Python dừng đánh giá ngay.
> 2. Lợi ích hệ thống: Việc đặt điều kiện lọc thất bại lên trước giúp kích hoạt ngắn mạch sớm, tiết kiệm tài nguyên CPU và tăng tốc độ xử lý Boolean khi duyệt lượng đơn hàng lớn.

---

### Câu 3: Hãy viết câu lệnh Python sử dụng toán tử so sánh và toán tử logic để thiết lập cờ hiệu `is_discounted` thỏa mãn 2 điều kiện: giá trị đơn hàng `order_amount` từ 150.000 VNĐ trở lên VÀ người dùng có mã `has_voucher` hoặc là thành viên `is_vip_member`.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Câu lệnh Python chuẩn:
>   `is_discounted = (order_amount >= 150000) and (has_voucher or is_vip_member)`
