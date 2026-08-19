# Bài thực hành: Kiểm tra điều kiện xét duyệt đơn hàng và ưu đãi bán hàng

## 1. Mục tiêu bài học
- Vận dụng thành thạo các toán tử so sánh (==, !=, >, <, >=, <=) trong Python để so sánh dữ liệu số và chuỗi.
- Xây dựng và đánh giá các biểu thức logic Boolean trả về kết quả True hoặc False.
- Thành thạo thao tác thực hành, kiểm chuẩn kết quả đầu ra và xử lý các trường hợp biên trên môi trường Python.

## 2. Yêu cầu bài toán
Một hệ thống thương mại điện tử cần tự động đánh giá các điều kiện áp dụng ưu đãi cho đơn hàng dựa trên các thông số của khách hàng. Bạn hãy viết một chương trình Python để thực hiện kiểm tra và xuất ra kết quả kiểm tra logic (True/False) cho các quy tắc sau:
1. Đơn hàng được miễn phí giao hàng nếu tổng tiền hàng (`order_amount`) từ 500,000 VNĐ trở lên hoặc khách hàng là tài khoản VIP (`is_vip` là True).
2. Đơn hàng được tặng quà cao cấp nếu số lượng sản phẩm (`items_count`) lớn hơn 5 và tổng tiền hàng từ 1,000,000 VNĐ trở lên.
3. Mã giảm giá áp dụng (`discount_code`) là hợp lệ nếu mã khác chuỗi rỗng và trùng khớp chính xác với chuỗi "SALE2024".
4. Kiểm tra xem tổng giá trị đơn hàng có đạt đúng mức hạn ngạch chuẩn 500,000 VNĐ hay không.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x (VS Code, PyCharm hoặc Jupyter Notebook) và tệp mã nguồn Python `order_check.py`.

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp `order_check.py` và khai báo các biến chứa thông tin mẫu của đơn hàng bao gồm `order_amount`, `items_count`, `is_vip`, và `discount_code`.
2. Bước 2: Sử dụng các toán tử so sánh thích hợp (>=, >, ==, !=) để viết biểu thức kiểm tra cho từng quy tắc nghiệp vụ đã đề ra.
3. Bước 3: Gán kết quả của các biểu thức so sánh vào các biến chứa giá trị Boolean tương ứng (`is_free_shipping`, `is_eligible_for_gift`, `has_valid_discount`, `is_exact_threshold`).
4. Bước 4: Sử dụng hàm `print()` để xuất kết quả đánh giá kiểu Boolean ra màn hình console và kiểm tra tính đúng đắn với các bộ dữ liệu thử nghiệm khác nhau.

## 4. Mã nguồn tham khảo (Code Demo)

```text

# Khai báo các thông tin đầu vào của đơn hàng
order_amount = 650000
items_count = 6
is_vip = False
discount_code = "SALE2024"

# Bước 1: Kiểm tra điều kiện miễn phí vận chuyển

# Đơn hàng >= 500,000 VNĐ hoặc là tài khoản VIP
is_free_shipping = (order_amount >= 500000) or (is_vip == True)

# Bước 2: Kiểm tra điều kiện tặng quà cao cấp

# Số lượng > 5 sản phẩm và Tổng tiền >= 1,000,000 VNĐ
is_eligible_for_gift = (items_count > 5) and (order_amount >= 1000000)

# Bước 3: Kiểm tra tính hợp lệ của mã giảm giá

# Mã không được rỗng và phải chính xác là "SALE2024"
has_valid_discount = (discount_code != "") and (discount_code == "SALE2024")

# Bước 4: Kiểm tra xem đơn hàng có khớp chính xác mức hạn ngạch 500,000 VNĐ không
is_exact_threshold = (order_amount == 500000)

# In kết quả kiểm tra logic ra màn hình
print("=== KẾT QUẢ XÉT DUYỆT ĐƠN HÀNG ===")
print("Miễn phí vận chuyển:", is_free_shipping)
print("Đủ điều kiện nhận quà cao cấp:", is_eligible_for_gift)
print("Mã giảm giá hợp lệ:", has_valid_discount)
print("Đơn hàng bằng đúng 500,000 VNĐ:", is_exact_threshold)
print("Kiểu dữ liệu của kết quả kiểm tra:", type(is_free_shipping))
```

# 5. Checklist đánh giá kết quả
- [ ] Khai báo đầy đủ các biến đầu vào theo đúng kiểu dữ liệu yêu cầu.
- [ ] Sử dụng chính xác các toán tử so sánh (==, !=, >, >=, <=, <) trong biểu thức.
- [ ] Kết quả đầu ra của các biểu thức so sánh trả về chuẩn kiểu dữ liệu Boolean (True/False).
- [ ] Mã nguồn chạy thành công không phát sinh lỗi cú pháp và được trình bày sạch đẹp.
