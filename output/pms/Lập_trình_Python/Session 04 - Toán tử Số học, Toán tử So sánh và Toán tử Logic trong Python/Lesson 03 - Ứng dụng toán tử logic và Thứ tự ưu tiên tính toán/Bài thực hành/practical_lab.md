# Bài thực hành: Xây dựng Mô-đun Thẩm định Khuyến mãi và Phê duyệt Đơn hàng ShopeeFood

## 1. Mục tiêu bài học
- Vận dụng các toán tử logic phức hợp `and`, `or`, `not` để xây dựng biểu thức điều kiện.
- Hiểu và ứng dụng thứ tự ưu tiên tính toán (PEMDAS) bằng cách sử dụng dấu ngoặc đơn `()` để nhóm các điều kiện logic rõ ràng.
- Phân tích và kiểm chứng cơ chế đánh giá ngắn mạch (Short-circuit evaluation) của Python trong môi trường thực tế.

## 2. Yêu cầu bài toán
Hệ thống thanh toán tự động của **ShopeeFood** cần lọc và phê duyệt đơn hàng được miễn phí giao hàng, được tặng voucher khuyến mãi và tự động gửi đơn đến nhà hàng. Bạn hãy viết một chương trình Python để thực hiện kiểm tra và xuất ra kết quả kiểm tra logic (True/False) cho các quy tắc nghiệp vụ sau:

1. **Đơn hàng được miễn phí giao hàng (`is_freeship`):** 
   - Đơn hàng có khoảng cách giao hàng ngắn dưới hoặc bằng 3.0 km (`distance_km <= 3.0`).
   - HOẶC đơn hàng có giá trị từ 250,000 VNĐ trở lên (`order_amount >= 250000.0`) VÀ đồng thời khách hàng là tài khoản VIP (`is_vip == 1`).
   - *Công thức:* `is_freeship = (distance_km <= 3.0) or ((order_amount >= 250000.0) and (is_vip == 1))`

2. **Đơn hàng được tặng voucher tri ân (`is_eligible_for_voucher`):**
   - Khách hàng không có lịch sử hủy đơn gần đây (`has_recent_cancel == 0`).
   - VÀ đồng thời thỏa mãn một trong hai điều kiện: Giá trị đơn hàng lớn hơn hoặc bằng 500,000 VNĐ (`order_amount >= 500000.0`) HOẶC là tài khoản VIP (`is_vip == 1`).
   - *Công thức:* `is_eligible_for_voucher = (has_recent_cancel == 0) and ((order_amount >= 500000.0) or (is_vip == 1))`

3. **Phê duyệt đơn hàng gửi đến nhà hàng tự động (`is_approved`):**
   - Nhà hàng đang trong khung giờ mở cửa hoạt động (`is_restaurant_open == 1`).
   - VÀ tài khoản không bị cảnh báo rủi ro gian lận (`is_fraud_warning == 0`).
   - *Công thức:* `is_approved = (is_restaurant_open == 1) and (is_fraud_warning == 0)`

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x (VS Code hoặc PyCharm) và tệp kịch bản `shopee_checkout.py`.

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp `shopee_checkout.py` và khai báo các biến chứa thông số đơn hàng.
2. Bước 2: Viết các biểu thức logic kết hợp `and`, `or`, `not` cùng dấu ngoặc đơn `()` để định vị thứ tự ưu tiên tính toán theo quy tắc nghiệp vụ.
3. Bước 3: Gán kết quả của các biểu thức so sánh và logic phức hợp vào các biến Boolean tương ứng.
4. Bước 4: Sử dụng hàm `print()` để xuất báo cáo trạng thái đơn hàng ra màn hình console và chạy thử nghiệm.

## 4. Mã nguồn tham khảo (Code Demo)

```python

# shopee_checkout.py

# Khai báo các thông tin đầu vào của khách đặt hàng
order_amount = 280000

# Giá trị đơn hàng (VNĐ)
distance_km = 4.5

# Khoảng cách giao hàng (km)
is_vip = 1

# Trạng thái VIP (1: Có, 0: Không)
has_recent_cancel = 0

# Lịch sử hủy đơn gần đây (1: Có, 0: Không)
is_restaurant_open = 1

# Nhà hàng đang mở cửa (1: Đúng, 0: Sai)
is_fraud_warning = 0

# Cảnh báo gian lận tài khoản (1: Có, 0: Không)

# 1. Đánh giá điều kiện miễn phí giao hàng (Freeship)

# Khoảng cách <= 3.0 km HOẶC (Đơn hàng >= 250k AND là VIP)
is_freeship = (distance_km <= 3.0) or ((order_amount >= 250000.0) and (is_vip == 1))

# 2. Đánh giá điều kiện được tặng voucher tri ân

# Không hủy đơn gần đây AND (Đơn hàng >= 500k OR là VIP)
is_eligible_for_voucher = (has_recent_cancel == 0) and ((order_amount >= 500000.0) or (is_vip == 1))

# 3. Đánh giá điều kiện phê duyệt đơn hàng tự động gửi nhà hàng

# Nhà hàng mở cửa AND tài khoản không bị cảnh báo gian lận
is_approved = (is_restaurant_open == 1) and (is_fraud_warning == 0)

# Hiển thị báo cáo chi tiết xét duyệt
print("=== KẾT QUẢ XÉT DUYỆT ĐƠN HÀNG SHOPEEFOOD ===")
print(f"Giá trị đơn hàng: {order_amount:,} VNĐ")
print(f"Khoảng cách: {distance_km} km")
print(f"Khách hàng miễn phí vận chuyển: {is_freeship}")
print(f"Được tặng voucher tri ân: {is_eligible_for_voucher}")
print(f"Phê duyệt đơn hàng tự động gửi nhà hàng: {is_approved}")
```

# 5. Checklist đánh giá kết quả
- [ ] Khai báo đầy đủ các biến đầu vào theo đúng kiểu dữ liệu yêu cầu.
- [ ] Vận dụng chính xác toán tử logic `and`, `or`, `not` kết hợp toán tử so sánh.
- [ ] Sử dụng đúng dấu ngoặc đơn `()` để định rõ thứ tự ưu tiên thực thi cho các cụm điều kiện logic.
- [ ] Chương trình chạy ổn định, trả về kết quả đúng luận lý Boolean (True/False) ra màn hình.
