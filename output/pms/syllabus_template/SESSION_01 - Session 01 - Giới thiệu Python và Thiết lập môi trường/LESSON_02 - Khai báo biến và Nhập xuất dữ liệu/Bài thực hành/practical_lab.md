# Bài thực hành: Xây dựng Mô-đun In Hóa đơn và Tính Tiền thừa cho Hệ thống POS Rikkei Mart

## 1. Mục tiêu bài học
- Vận dụng kiến thức về khai báo biến, nhập dữ liệu từ bàn phím và xuất thông tin ra màn hình trong lập trình ứng dụng.
- Thực hiện thành thạo kỹ thuật ép kiểu dữ liệu (int, float) từ đầu vào dạng chuỗi để đảm bảo tính toán số học chính xác.
- Sử dụng f-string để định dạng chuỗi kết quả nâng cao bao gồm căn chỉnh lề và phân tách hàng nghìn cho số tiền.
- Phát hiện và chủ động phòng ngừa các lỗi phổ biến như TypeError và ValueError khi xử lý dữ liệu nhập từ người dùng.

## 2. Yêu cầu bài toán
Ban quản lý Siêu thị Rikkei Mart yêu cầu xây dựng một mô-đun phần mềm cho hệ thống POS quầy thu ngân. Chương trình cần thu thập thông tin giao dịch bao gồm: tên thu ngân, tên khách hàng, tên sản phẩm, số lượng mua, đơn giá sản phẩm, tỷ lệ giảm giá (%) và số tiền khách hàng thanh toán. Hệ thống tiến hành xử lý ép kiểu dữ liệu đầu vào, tính toán tạm tính, tiền giảm giá, tiền sau giảm giá, thuế VAT (cố định 8%), tổng tiền thanh toán và tiền thối lại cho khách. Sau khi tính toán thành công, chương trình phải in ra hóa đơn bán hàng được căn chỉnh lề chuẩn giao diện POS quầy thu ngân (độ rộng khung 45 ký tự) và định dạng hiển thị tiền tệ rõ ràng.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển phần mềm (Visual Studio Code / PyCharm chạy Python 3.x) và tài liệu mô tả yêu cầu nghiệp vụ hóa đơn Rikkei Mart POS.

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp chương trình pos_invoice.py và khai báo các hằng số hệ thống như tên siêu thị STORE_NAME = 'SIÊU THỊ RIKKEI MART' và tỷ lệ thuế VAT_RATE = 0.08.
2. Bước 2: Thu thập thông tin giao dịch từ bàn phím bằng hàm input() và thực hiện ép kiểu ngay lập tức (dùng int() cho số lượng, float() cho đơn giá, phần trăm giảm giá và tiền khách đưa).
3. Bước 3: Lập trình các công thức tính toán nghiệp vụ: Tạm tính = Số lượng * Đơn giá; Tiền giảm giá = Tạm tính * (% Giảm giá / 100); Tiền sau giảm giá = Tạm tính - Tiền giảm giá; Thuế VAT = Tiền sau giảm giá * VAT_RATE; Tổng thanh toán = Tiền sau giảm giá + Thuế VAT; Tiền thối lại = Tiền khách đưa - Tổng thanh toán.
4. Bước 4: Định dạng cấu trúc hóa đơn POS bằng f-string với các ký tự căn chỉnh lề (^ cho căn giữa, < cho căn trái, > cho căn phải) và mã hóa số thực thành chuỗi có phân tách hàng nghìn, sau đó in kết quả kiểm chuẩn.

## 4. Mã nguồn tham khảo (Code Demo)

```text

# Hệ thống xử lý và in hóa đơn POS - Rikkei Mart POS

# Hằng số hệ thống
STORE_NAME = "SIÊU THỊ RIKKEI MART"
VAT_RATE = 0.08

# Thuế VAT ưu đãi 8%

# Bước 1: Thu thập dữ liệu và ép kiểu dữ liệu chính xác
cashier_name = input("Nhập tên thu ngân: ")
customer_name = input("Nhập tên khách hàng: ")
product_name = input("Nhập tên sản phẩm: ")

# Ép kiểu dữ liệu để tránh lỗi TypeError và Logic Error
quantity = int(input("Nhập số lượng: "))
unit_price = float(input("Nhập đơn giá (VNĐ): "))
discount_percent = float(input("Nhập % giảm giá: "))

# Bước 2: Xử lý tính toán nghiệp vụ hóa đơn
subtotal = quantity * unit_price
discount_amount = subtotal * (discount_percent / 100)
amount_after_discount = subtotal - discount_amount
vat_amount = amount_after_discount * VAT_RATE
final_amount = amount_after_discount + vat_amount

# Thu thập tiền khách đưa và tính tiền thối lại
cash_given = float(input("Nhập số tiền khách đưa (VNĐ): "))
change_due = cash_given - final_amount

# Bước 3: In hóa đơn POS định dạng chuẩn chuyên nghiệp
print("\n" + "=" * 45)
print(f"{STORE_NAME:^45}")
print(f"{'HÓA ĐƠN THANH TOÁN':^45}")
print("=" * 45)
print(f"Thu ngân: {cashier_name:<20} Khách: {customer_name}")
print("-" * 45)
print(f"Tên sản phẩm:      {product_name}")
print(f"Số lượng:          {quantity}")
print(f"Đơn giá:           {unit_price:>15,.0f} VNĐ")
print(f"Tạm tính:          {subtotal:>15,.0f} VNĐ")
print(f"Giảm giá ({discount_percent:.0f}%):    -{discount_amount:>15,.0f} VNĐ")
print(f"Thuế VAT (8%):     +{vat_amount:>15,.0f} VNĐ")
print("-" * 45)
print(f"TỔNG TỔNG CỘNG:    {final_amount:>15,.0f} VNĐ")
print(f"Tiền khách đưa:    {cash_given:>15,.0f} VNĐ")
print(f"Tiền thối lại:     {change_due:>15,.0f} VNĐ")
print("=" * 45)
print(f"{'CẢM ƠN QUÝ KHÁCH VÀ HẸN GẶP LẠI!':^45}")
print("=" * 45)
```

# 5. Checklist đánh giá kết quả
- [ ] Khai báo đầy đủ hằng số và các biến chứa thông tin giao dịch tuân thủ chuẩn đặt tên trong lập trình.
- [ ] Ép kiểu dữ liệu đầu vào đúng loại (int cho số lượng, float cho số tiền/tỷ lệ) để tránh lỗi lặp chuỗi hoặc lỗi sai phép toán số học.
- [ ] Tính toán chính xác các giá trị nghiệp vụ: tạm tính, tiền giảm giá, tiền sau giảm giá, thuế VAT 8%, tổng tiền thanh toán và tiền thối lại.
- [ ] Sử dụng f-string căn chỉnh lề khung 45 ký tự chuẩn xác và định dạng hiển thị tiền tệ có phân tách hàng nghìn.
- [ ] Mã nguồn chạy thành công không phát sinh lỗi ngoại lệ như TypeError hoặc ValueError.
