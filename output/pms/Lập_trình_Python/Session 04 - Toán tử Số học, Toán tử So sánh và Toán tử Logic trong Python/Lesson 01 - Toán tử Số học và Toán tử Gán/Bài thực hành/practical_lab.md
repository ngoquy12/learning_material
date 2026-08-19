# Bài thực hành: Xây dựng Mô-đun Tính toán Hóa đơn và Quản lý Điểm thưởng Siêu thị

## 1. Mục tiêu bài học
- Vận dụng kiến thức Python để viết các biểu thức số học phức tạp sử dụng các toán tử +, -, *, /, //, %, **.
- Thành thạo việc tối ưu hóa và cập nhật biến trong mã nguồn bằng các toán tử gán gộp +=, -=, *=, /=.
- Thành thạo thao tác thực hành, kiểm tra loại dữ liệu số và kiểm chuẩn kết quả đầu ra đúng với nghiệp vụ thực tế.

## 2. Yêu cầu bài toán
Một hệ thống bán lẻ siêu thị cần phát triển mô-đun xử lý thanh toán hóa đơn tự động. Bạn được giao nhiệm vụ viết chương trình Python thực hiện các quy tắc logic nghiệp vụ sau:
1. Khai báo các thông tin đầu vào gồm: đơn giá sản phẩm, số lượng mua, tỷ lệ chiết khấu (%), thuế VAT (%), cấp độ thành viên của khách hàng (tier_level), số lượng hàng trong kho và số dư ví điện tử.
2. Thực hiện tính toán chi tiết bằng các toán tử số học:
   - Tính tổng tiền hàng chưa giảm giá (*).
   - Tính số tiền giảm giá và số tiền chịu thuế (*, /).
   - Tính tổng thanh toán cuối cùng bao gồm thuế VAT (+, -).
   - Tính hệ số nhân điểm thưởng dựa trên cấp độ thành viên bằng toán tử lũy thừa (**).
   - Tính số điểm thưởng tích lũy (mỗi 100,000 VNĐ tính 1 điểm gốc) bằng toán tử chia lấy nguyên (//).
   - Xác định số tiền dư chưa đủ quy đổi thành điểm thưởng bằng toán tử chia lấy dư (%).
3. Cập nhật dữ liệu hệ thống bằng toán tử gán gộp:
   - Giảm số lượng tồn kho tương ứng với số lượng đã bán (-=).
   - Trừ số tiền thanh toán vào ví điện tử của khách hàng (-=).
   - Cộng bù số tiền voucher khuyến mãi vào ví điện tử (+=).
   - Tính số tiền dư nợ sau khi áp dụng chính sách hỗ trợ giảm một nửa (/=).
4. Xuất báo cáo hóa đơn rõ ràng, chính xác ra màn hình console.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x (VS Code hoặc PyCharm) và tệp kịch bản pos_calculator.py.

### Các bước thực hiện:
1. Bước 1: Khởi tạo không gian làm việc, tạo tệp pos_calculator.py và khai báo các biến số ban đầu mô phỏng đơn hàng.
2. Bước 2: Viết các biểu thức số học tính toán tổng tiền, chiết khấu, thuế VAT và hệ số điểm thưởng theo quy tắc nghiệp vụ.
3. Bước 3: Thực hiện cập nhật số lượng tồn kho, tài khoản ví điện tử và dư nợ bằng các toán tử gán gộp +=, -=, *=, /=.
4. Bước 4: Sử dụng hàm print() định dạng kết quả hiển thị báo cáo thanh toán và tiến hành chạy kiểm thử kịch bản.

## 4. Mã nguồn tham khảo (Code Demo)

```text

# pos_calculator.py

# Mô-đun tính toán hóa đơn và quản lý điểm thưởng siêu thị

# 1. Khai báo dữ liệu đầu vào
unit_price = 150000

# Đơn giá một sản phẩm (VNĐ)
quantity = 8

# Số lượng mua
discount_percent = 10

# Tỷ lệ chiết khấu (%)
vat_percent = 8

# Tỷ lệ thuế VAT (%)
customer_tier = 2

# Cấp độ thành viên VIP
stock_quantity = 50

# Số lượng tồn kho ban đầu
customer_wallet = 2000000

# Số dư ví điện tử khách hàng (VNĐ)

# 2. Xử lý các phép tính số học (+, -, *, /, //, %, **)

# Tính tổng tiền hàng trước chiết khấu
subtotal = unit_price * quantity

# Tính số tiền chiết khấu được giảm
discount_amount = subtotal * (discount_percent / 100)

# Tổng tiền sau chiết khấu
amount_after_discount = subtotal - discount_amount

# Tính tiền thuế VAT
vat_amount = amount_after_discount * (vat_percent / 100)

# Tổng số tiền thanh toán cuối cùng
final_total = amount_after_discount + vat_amount

# Tính hệ số nhân điểm thưởng dựa trên cấp độ thành viên (2^tier)
reward_multiplier = 2 ** customer_tier

# Tính số điểm thưởng cơ bản (mỗi 100,000 VNĐ = 1 điểm)
base_points = final_total // 100000
total_reward_points = base_points * reward_multiplier

# Số tiền lẻ dư ra chưa đủ điều kiện đổi điểm tiếp theo
remaining_for_next_point = final_total % 100000

# 3. Thực thi cập nhật trạng thái với toán tử gán gộp (+=, -=, *=, /=)

# Trừ số lượng tồn kho theo hàng đã bán
stock_quantity -= quantity

# Trừ tiền hóa đơn vào số dư ví khách hàng
customer_wallet -= final_total

# Khách hàng nhận quà tặng voucher trị giá 50,000 VNĐ cộng vào ví
voucher_bonus = 50000
customer_wallet += voucher_bonus

# Khai báo một khoản phí dịch vụ và nhân đôi khoản phí này
service_fee = 15000.0
service_fee *= 2

# Khai báo dư nợ và giảm một nửa dư nợ cho khách hàng
debt_balance = 300000.0
debt_balance /= 2

# 4. Hiển thị báo cáo chi tiết hóa đơn
print("=== HÓA ĐƠN THANH TOÁN SIÊU THỊ ===")
print(f"Đơn giá sản phẩm: {unit_price:,.0f} VNĐ")
print(f"Số lượng mua: {quantity}")
print(f"Tổng tiền hàng: {subtotal:,.0f} VNĐ")
print(f"Chiết khấu ({discount_percent}%): -{discount_amount:,.0f} VNĐ")
print(f"Thuế VAT ({vat_percent}%): +{vat_amount:,.0f} VNĐ")
print(f"TỔNG THANH TOÁN: {final_total:,.0f} VNĐ")
print("-----------------------------------")
print(f"Hệ số nhân điểm thưởng (2^{customer_tier}): {reward_multiplier}")
print(f"Điểm thưởng tích lũy: {total_reward_points:.0f} điểm")
print(f"Số tiền dư chưa quy đổi điểm: {remaining_for_next_point:,.0f} VNĐ")
print("-----------------------------------")
print(f"Tồn kho còn lại: {stock_quantity} sản phẩm")
print(f"Phí dịch vụ áp dụng: {service_fee:,.0f} VNĐ")
print(f"Dư nợ còn lại sau ưu đãi: {debt_balance:,.0f} VNĐ")
print(f"Số dư ví điện tử hiện tại: {customer_wallet:,.0f} VNĐ")
```

# 5. Checklist đánh giá kết quả
- [ ] Viết đúng và chính xác các biểu thức số học có chứa toán tử +, -, *, /, //, %, **.
- [ ] Sử dụng chuẩn xác các toán tử gán gộp +=, -=, *=, /= để cập nhật giá trị biến.
- [ ] Mã nguồn Python tuân thủ quy chuẩn PEP 8, có giải thích chú thích đầy đủ và chạy thành công không có lỗi syntax/runtime.
- [ ] Kết quả đầu ra tính toán số tiền, thuế, điểm thưởng và số dư chính xác theo logic nghiệp vụ bài toán.
