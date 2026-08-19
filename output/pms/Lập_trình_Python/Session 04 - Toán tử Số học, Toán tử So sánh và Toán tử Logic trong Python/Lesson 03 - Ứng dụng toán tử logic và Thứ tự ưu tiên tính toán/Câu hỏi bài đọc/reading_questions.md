# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions) - Lesson 03

## Tình huống & Mã nguồn kiểm tra

Dựa trên mã nguồn nghiệp vụ thẩm định hồ sơ đăng ký đối tác tài xế giao hàng ShopeeFood:

```python

# Thông số hồ sơ ứng viên
age = 22
has_motorbike = True
has_criminal_record = False

# Thẩm định điều kiện tuyển dụng
is_eligible = (age >= 18 and age <= 60) and has_motorbike and (not has_criminal_record)
```

---

### Câu 1: Xác định giá trị Boolean của biến `is_eligible` và giải thích vai trò của toán tử `not`.

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Biểu thức tuổi `(age >= 18 and age <= 60)` trả về `True`.
> - Biểu thức xe máy `has_motorbike` là `True`.
> - Biểu thức lịch sử tư pháp `not has_criminal_record` (not False) trả về `True`.
> - Kết hợp toàn bộ bằng toán tử `and` trả về kết quả cuối cùng `is_eligible = True`.
> - Toán tử `not` đảo ngược giá trị Boolean, giúp phát biểu nghiệp vụ "không có tiền án tiền sự" trở thành điều kiện hợp lệ `True` khi giá trị biến đầu vào là `False`.

---

### Câu 2: Nếu một ứng viên có tuổi là `17` nhưng có xe máy và lý lịch sạch, chương trình sẽ đánh giá ngắn mạch như thế nào?

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Phép so sánh tuổi đầu tiên `age >= 18` (17 >= 18) trả về `False`.
> - Vì vế đầu tiên của phép toán `and` là `False`, Python dừng ngay toàn bộ việc đánh giá các vế còn lại (`age <= 60`, `has_motorbike`, `not has_criminal_record`) và gán ngay `is_eligible = False`. Đây là cơ chế đánh giá ngắn mạch giúp tiết kiệm tài nguyên hệ thống.

---

### Câu 3: Hãy chỉ ra thứ tự ưu tiên thực thi của các toán tử trong biểu thức gán của `is_eligible`.

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Thứ tự ưu tiên thực thi từ cao đến thấp trong biểu thức này là:
>   1. Dấu ngoặc đơn `(age >= 18 and age <= 60)` được ưu tiên tính toán trước.
>   2. Toán tử logic phủ định `not` (`not has_criminal_record`).
>   3. Toán tử so sánh số học (`>=`, `<=`).
>   4. Toán tử logic `and` kết hợp các mệnh đề lại với nhau.

---

### Câu 4: Tại sao việc thiếu dấu ngoặc đơn `()` khi viết các biểu thức kết hợp giữa toán tử so sánh và toán tử logic có thể dẫn đến kết quả sai lệch hoặc lỗi đọc mã nguồn?

> **Gợi ý trả lời & Định hướng đáp án:**
>
> - Khi không có ngoặc đơn, Python sẽ áp dụng thứ tự ưu tiên mặc định (toán tử so sánh thực hiện trước toán tử logic).
> - Đối với các biểu thức dài hoặc phức tạp, việc thiếu dấu ngoặc đơn dễ khiến lập trình viên hiểu lầm thứ tự đánh giá các điều kiện hoặc làm giảm khả năng đọc hiểu (Readability) của mã nguồn theo chuẩn PEP 8.
