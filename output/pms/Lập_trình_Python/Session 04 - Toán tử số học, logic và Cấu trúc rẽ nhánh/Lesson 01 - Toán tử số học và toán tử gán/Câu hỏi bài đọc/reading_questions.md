# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn tính toán đơn hàng ShopeeFood:

```python
unit_price = 45000
quantity = 3
shipping_fee = 20000
discount_voucher = 15000

subtotal = unit_price * quantity
total_payment = subtotal + shipping_fee - discount_voucher
reward_points = 120
reward_points += 50
```

---

### Câu 1 (Tính toán kết quả tài chính): Với dữ liệu đơn hàng 3 phần cơm tấm giá 45.000 VNĐ, hãy tính giá trị biến `subtotal` và tổng thanh toán `total_payment` thu được sau khi chạy đoạn mã trên.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Giá trị tiền hàng `subtotal = 45000 * 3` thu được là `135.000 VNĐ`.
> - Tổng tiền thanh toán `total_payment = 135000 + 20000 - 15000` thu được kết quả cuối cùng là `140.000 VNĐ`.

---

### Câu 2 (Phân tích toán tử gán phức hợp): Biến `reward_points` ban đầu khởi tạo là `120`. Sau câu lệnh `reward_points += 50`, giá trị mới lưu trữ trong bộ nhớ RAM của biến này thay đổi thành bao nhiêu và tương đương với cú pháp cơ bản nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Giá trị mới của biến `reward_points` thay đổi thành `170`.
> - Cú pháp `reward_points += 50` tương đương hoàn toàn với phép gán cơ bản `reward_points = reward_points + 50`.

---

### Câu 3 (Chia hóa đơn nhóm): Nếu nhóm 4 người ăn chung hóa đơn `total_payment = 140000 VNĐ`, câu lệnh `share_per_person = total_payment // 4` và `change = total_payment % 4` trả về kết quả số tiền mỗi người đóng và số tiền dư lẻ là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - `share_per_person` trả về `35000` (mỗi người đóng 35.000 VNĐ).
> - Phép chia hết cho 4 nên phần dư `change` trả về `0` VNĐ.

---

### Câu 4 (Phân tích sai sót số học): Nếu lập trình viên tính giá trị giảm giá bằng câu lệnh `discount = subtotal * 0.10`, vì sao kết quả số thực `float` thu được có thể gặp sai số số thực và cách khắc phục khi cần xử lý tiền tệ ngân hàng?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Do máy tính lưu trữ số thực `float` dưới dạng nhị phân, phép tính với `0.10` có thể tạo ra sai số phần thập phân dài (floating-point precision).
> - Để xử lý chính xác tài chính ngân hàng, lập trình viên nên ép kiểu số nguyên `int()` hoặc sử dụng thư viện `decimal`.
