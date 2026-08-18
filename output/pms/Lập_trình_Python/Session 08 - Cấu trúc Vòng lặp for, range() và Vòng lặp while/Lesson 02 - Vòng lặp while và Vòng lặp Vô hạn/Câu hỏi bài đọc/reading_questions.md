# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ lập tích lũy tài chính tự động cho khách hàng ngân hàng số được trích dẫn từ bài thực hành:

```python
# Khởi tạo số dư hiện tại, số dư mục tiêu và số tiền gửi định kỳ
current_balance = 10000000
target_balance = 50000000
monthly_deposit = 5000000
months = 0

# Vòng lặp tích lũy tài chính đến khi đạt mục tiêu
while current_balance < target_balance:
    current_balance += monthly_deposit
    months += 1

print(f"Tổng số tháng cần tích lũy: {months} tháng")
print(f"Số dư cuối cùng đạt được: {current_balance:,} VNĐ")
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X): Sau khi kết thúc vòng lặp `while` trong đoạn mã trên, biến `months` nhận giá trị cuối cùng là bao nhiêu và số dư tài khoản `current_balance` đạt mức cụ thể là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Số tiền cần tích lũy thêm để đạt mục tiêu là: `50.000.000 - 10.000.000 = 40.000.000 VNĐ`.
> - Mỗi tháng gửi thêm `5.000.000 VNĐ`, do đó vòng lặp sẽ chạy: `40.000.000 / 5.000.000 = 8` lần.
> - Sau 8 lần lặp, điều kiện `current_balance < target_balance` (50.000.000 < 50.000.000) trả về `False` và vòng lặp kết thúc.
> - Vậy biến `months` nhận giá trị cuối cùng là `8` tháng và số dư cuối cùng là `50.000.000` VNĐ.

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y): Nếu thay đổi mục tiêu tiết kiệm thành `target_balance = 52000000` (giữ nguyên các giá trị khác), số lần lặp và giá trị của `current_balance` khi kết thúc chương trình sẽ thay đổi thế nào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Khi `target_balance = 52.000.000 VNĐ`:
>   - Sau 8 tháng lặp, số dư là `50.000.000 VNĐ` (nhỏ hơn 52.000.000 nên điều kiện lặp vẫn đúng).
>   - Vòng lặp chạy tiếp tháng thứ 9: số dư tăng lên `55.000.000 VNĐ`. Điều kiện `55.000.000 < 52.000.000` trả về `False` và dừng lại.
>   - Kết quả: Vòng lặp chạy tổng cộng `9` lần (`months = 9`) và số dư cuối cùng đạt được là `55.000.000` VNĐ.

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z): Giả sử khách hàng muốn rút ngắn thời gian tích lũy xuống còn đúng `4` tháng để đạt mục tiêu tiết kiệm ban đầu (`target_balance = 50000000`, bắt đầu từ `current_balance = 10000000`). Số tiền gửi hàng tháng `monthly_deposit` tối thiểu phải là bao nhiêu?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Số tiền tích lũy cần đạt được là `40.000.000 VNĐ`.
> - Để số lần lặp (`months`) kết thúc sau đúng 4 chu kỳ lặp, ta cần: `monthly_deposit * 4 >= 40.000.000 VNĐ`.
> - Do đó, số tiền gửi hàng tháng `monthly_deposit` tối thiểu phải là: `40.000.000 / 4 = 10.000.000` VNĐ.

---

### Câu 4 (Phân tích lỗi thường gặp & Trường hợp biên): Tại sao việc cập nhật số dư `current_balance += monthly_deposit` bên trong khối lệnh `while` là bắt buộc? Điều gì sẽ xảy ra nếu lập trình viên quên viết dòng lệnh này?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Câu lệnh cập nhật `current_balance += monthly_deposit` làm tăng giá trị của `current_balance` sau mỗi chu kỳ, hướng nó tới cột mốc dừng là `target_balance`.
> - Nếu quên cập nhật, giá trị của `current_balance` sẽ giữ nguyên bằng `10.000.000` mãi mãi, điều kiện `current_balance < target_balance` (10.000.000 < 50.000.000) luôn luôn nhận giá trị `True`.
> - Hậu quả là chương trình sẽ rơi vào vòng lặp vô hạn (Infinite Loop), liên tục in ra màn hình hoặc tiêu tốn tài nguyên xử lý của CPU khiến hệ thống bị treo.