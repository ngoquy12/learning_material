# Xây dựng module tính toán chu kỳ tích lũy tài chính tự động cho khách hàng ngân hàng số

## 1. Mục tiêu bài học
- Vận dụng vòng lặp while với điều kiện động để xác định chính xác số tháng tích lũy.
- Kiểm soát biến trạng thái nhằm tránh hiện tượng vòng lặp vô hạn trong xử lý tài chính.

## 2. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển python và tệp tài nguyên thực hành.

### Các bước thực hiện:
1. Bước 1: Khai báo biến current_balance đại diện cho số dư ban đầu (ví dụ: 10000000) và target_balance đại diện cho mục tiêu (ví dụ: 50000000).
2. Bước 2: Khai báo biến monthly_deposit đại diện số tiền gửi hàng tháng (ví dụ: 5000000) và biến đếm months = 0.
3. Bước 3: Viết vòng lặp while với điều kiện current_balance < target_balance.
4. Bước 4: Bên trong thân vòng lặp, cộng thêm monthly_deposit vào current_balance và tăng biến count months thêm 1 đơn vị.
5. Bước 5: In ra màn hình kết quả tổng số tháng tích lũy và số dư tài khoản cuối cùng sau khi kết thúc vòng lặp.

## 3. Mã nguồn tham khảo (Code Demo)

```python
# Tệp mã nguồn: main.py
# Bài thực hành: Vòng lặp while và Vòng lặp Vô hạn

print("=== HỆ THỐNG TÍNH TOÁN TÍCH LŨY TÀI CHÍNH ===")

# Khởi tạo thông tin số dư ban đầu và mục tiêu
current_balance = 10000000  # 10 triệu VNĐ
target_balance = 50000000   # 50 triệu VNĐ
monthly_deposit = 5000000   # 5 triệu VNĐ gửi thêm hàng tháng
months = 0

print(f"Số dư ban đầu: {current_balance:,} VNĐ")
print(f"Số tiền gửi hàng tháng: {monthly_deposit:,} VNĐ")
print(f"Mục tiêu tích lũy: {target_balance:,} VNĐ\n")

# Vòng lặp while kiểm tra điều kiện tích lũy
while current_balance < target_balance:
    current_balance += monthly_deposit
    months += 1
    print(f"- Tháng {months:02d}: Số dư hiện tại = {current_balance:,} VNĐ")

# Kết xuất thông tin kết quả
print(f"\n--> Kết quả: Hoàn thành mục tiêu sau {months} tháng.")
print(f"--> Số dư cuối kỳ đạt được: {current_balance:,} VNĐ")
```

## 4. Checklist đánh giá kết quả
- [ ] Vòng lặp while dừng chính xác khi current_balance đạt hoặc vượt mốc target_balance.
- [ ] Khai báo và tăng biến đếm số tháng months chính xác sau từng chu kỳ lặp.
- [ ] Biến trạng thái current_balance được cập nhật trong thân lặp để đảm bảo không xảy ra vòng lặp vô hạn.