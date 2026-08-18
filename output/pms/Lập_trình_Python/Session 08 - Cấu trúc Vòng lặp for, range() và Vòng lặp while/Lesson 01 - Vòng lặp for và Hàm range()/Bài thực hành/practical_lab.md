# Bài thực hành: Xây dựng Hệ thống In Hóa đơn & Phân tích Mã giảm giá Siêu thị MartX

## 1. Mục tiêu bài học
- Vận dụng kiến thức cú pháp vòng lặp for và hàm range(start, stop, step) trong Python để xử lý các bài toán duyệt số thứ tự và đếm ngược thời gian.
- Thành thạo kỹ thuật duyệt chuỗi ký tự kết hợp phương thức isdigit() để trích xuất và tính toán dữ liệu ưu đãi từ mã coupon.
- Nhận biết và khắc phục các lỗi thường gặp phổ biến như lỗi thiếu giá trị cuối (Off-by-one Error) và lỗi chọn sai tham số step khi lặp lùi.

## 2. Yêu cầu bài toán
Bộ phận kỹ thuật của Siêu thị MartX cần xây dựng module xử lý hóa đơn tự động tại quầy thu ngân với 3 yêu cầu logic chính:
1. In danh sách số thứ tự mặt hàng từ 1 đến N (ví dụ N = 5) và tính giá trị minh họa cho từng item. Cần đảm bảo in đủ N mặt hàng, không bị ngắt sớm do đặc tính của hàm range().
2. Đếm ngược thời gian chờ xử lý quầy thanh toán từ 5 giây về 1 giây trước khi chốt giao dịch bằng cách sử dụng bước nhảy step âm trong hàm range().
3. Kiểm tra mã voucher discount (ví dụ: 'MARTX2025') bằng cách duyệt từng ký tự trong chuỗi. Nếu ký tự là chữ số, hệ thống sẽ chuyển thành số nguyên và cộng dồn để xác định tổng phần trăm giảm giá thực tế dành cho khách hàng.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x (IDLE, VS Code hoặc PyCharm) và tệp mã nguồn martx_invoice.py.

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp mã nguồn martx_invoice.py, khai báo các biến chứa tổng số mặt hàng total_items = 5, chuỗi mã giảm giá coupon_code = 'MARTX2025' và biến tích lũy total_discount = 0.
2. Bước 2: Sử dụng vòng lặp for kết hợp với hàm range(1, total_items + 1) để in số thứ tự sản phẩm từ 1 đến 5. Lưu ý tham số stop phải bằng total_items + 1 để tránh lỗi Off-by-one.
3. Bước 3: Cài đặt logic đếm ngược thời gian giữ quầy bằng vòng lặp for và hàm range(5, 0, -1) để in ra các mức thời gian giảm dần từ 5 giây đến 1 giây.
4. Bước 4: Duyệt từng ký tự char trong chuỗi coupon_code bằng vòng lặp for. Dùng hàm char.isdigit() để kiểm tra ký tự số, ép kiểu thành int và cộng dồn vào biến total_discount.
5. Bước 5: Chạy kiểm thử chương trình, đối chiếu kết quả hiển thị với yêu cầu nghiệp vụ và đảm bảo mã nguồn tuân thủ quy chuẩn mã hóa Python.

## 4. Mã nguồn tham khảo (Code Demo)

```text
# martx_invoice.py
# Hệ thống In Hóa đơn & Phân tích Mã giảm giá Siêu thị MartX

# Khai báo dữ liệu đầu vào
total_items = 5
coupon_code = "MARTX2025"
total_discount = 0

print("=== CHƯƠNG TRÌNH XỬ LÝ HÓA ĐƠN SIÊU THỊ MARTX ===")

# Nhiệm vụ 1: In danh sách thứ tự mặt hàng (Khắc phục lỗi Off-by-one với total_items + 1)
print("\n--- 1. DANH SÁCH MẶT HÀNG TRÊN HÓA ĐƠN ---")
for item_id in range(1, total_items + 1):
    item_price = item_id * 50000  # Đơn giá minh họa
    print(f"Mặt hàng số {item_id}: Đơn giá {item_price:,} VNĐ")

# Nhiệm vụ 2: Đếm ngược thời gian chờ giữ quầy thanh toán (Dùng range với step = -1)
print("\n--- 2. ĐẾM NGƯỢC THỜI GIAN XỬ LÝ THANH TOÁN ---")
for seconds in range(5, 0, -1):
    print(f"Hệ thống sẽ chốt hóa đơn sau: {seconds} giây")

# Nhiệm vụ 3: Phân tích mã voucher và tính % giảm giá tích lũy
print(f"\n--- 3. PHÂN TÍCH MÃ GIẢM GIÁ: {coupon_code} ---")
for char in coupon_code:
    if char.isdigit():
        digit_value = int(char)
        total_discount += digit_value
        print(f"Phát hiện chữ số ưu đãi: {digit_value}")
    else:
        print(f"Ký tự định danh phân loại: {char}")

print("--------------------------------------------------")
print(f"TỔNG XÁC NHẬN: Phần trăm giảm giá nhận được là {total_discount}%")
```

## 5. Checklist đánh giá kết quả
- [ ] Sử dụng đúng cú pháp range(1, total_items + 1) để in đủ danh sách mặt hàng, không bị lỗi thiếu phần tử cuối cùng.
- [ ] Áp dụng chính xác bước nhảy âm range(5, 0, -1) cho bài toán đếm ngược thời gian mà không bị bỏ qua vòng lặp.
- [ ] Duyệt thành công từng ký tự trong chuỗi mã giảm giá và sử dụng phương thức char.isdigit() để tính chính xác tổng phần trăm giảm giá.
- [ ] Mã nguồn được trình bày rõ ràng, có chú thích đầy đủ các bước xử lý và thực thi thành công không phát sinh lỗi cú pháp hay lỗi logic.