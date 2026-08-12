# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn phân hạng giảm giá đơn hàng ShopeeFood:

```python
order_amount = 1500000

if order_amount >= 2000000:
    discount_rate = 0.20
elif order_amount >= 1000000:
    discount_rate = 0.10
elif order_amount >= 500000:
    discount_rate = 0.05
else:
    discount_rate = 0.0

final_payment = order_amount * (1 - discount_rate)
```

---

### Câu 1: Với giá trị đơn hàng đầu vào `order_amount = 1500000`, hãy giải thích tuần tự từng bước kiểm tra điều kiện của chuỗi `if-elif-else` và xác định giá trị cuối cùng của biến `discount_rate`.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Bước 1: Điều kiện `order_amount >= 2000000` (1.500.000 >= 2.000.000) trả về `False` ➔ Chuyển sang nhánh `elif` tiếp theo.
> - Bước 2: Điều kiện `order_amount >= 1000000` (1.500.000 >= 1.000.000) trả về `True` ➔ Thực thi gán `discount_rate = 0.10` (10%).
> - Python lập tức thoát khỏi toàn bộ cấu trúc rẽ nhánh, bỏ qua nhánh `elif >= 500000` và nhánh `else`.

---

### Câu 2: Nếu sửa giá trị biến đầu vào thành `order_amount = 400000`, nhánh điều khiển nào sẽ được kích hoạt và số tiền thanh toán cuối cùng `final_payment` nhận kết quả là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Các điều kiện `>= 2000000`, `>= 1000000`, `>= 500000` đều trả về `False`.
> - Nhánh mặc định `else` được kích hoạt, gán `discount_rate = 0.0` (0%).
> - Giá trị `final_payment = 400000 * (1 - 0) = 400.000 VNĐ`.

---

### Câu 3: Hãy phân tích vì sao việc đặt sai thứ tự điều kiện (ví dụ đưa nhánh `elif order_amount >= 500000:` lên trước nhánh `elif order_amount >= 2000000:`) sẽ gây ra sai sót logic nghiêm trọng cho hệ thống ShopeeFood.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Khi đơn hàng đạt 2.500.000 VNĐ, do điều kiện `>= 500000` đứng trước trả về `True` ngay lập tức, Python sẽ thực thi gán `discount_rate = 0.05` (5%) và thoát nhánh.
> - Khách hàng bị mất quyền lợi giảm 20% vì nhánh `>= 2000000` đứng phía sau không bao giờ được chạm tới.
