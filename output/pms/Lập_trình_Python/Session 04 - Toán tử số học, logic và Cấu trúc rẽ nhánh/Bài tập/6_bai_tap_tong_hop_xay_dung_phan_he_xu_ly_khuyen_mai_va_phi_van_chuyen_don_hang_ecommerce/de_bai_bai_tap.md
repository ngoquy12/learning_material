## <center>[Bài tập tổng hợp] Xây dựng phân hệ xử lý khuyến mãi và phí vận chuyển đơn hàng E-commerce</center>

### **1. Mục tiêu**
*   **Vận dụng toán tử số học và logic:** Sử dụng thành thạo các toán tử số học (`+`, `-`, `*`, `/`), toán tử so sánh (`>`, `<`, `>=`, `<=`, `==`, `!=`) và toán tử logic (`and`, `or`, `not`) để giải quyết bài toán nghiệp vụ thương mại điện tử thực tế.
*   **Phẳng hóa cấu trúc rẽ nhánh (Flattening Conditions):** Loại bỏ bẫy lập trình "Arrow Anti-Pattern" (lồng ghép câu lệnh `if-else` quá sâu) bằng cách kết hợp hợp lý các mệnh đề logic và cấu trúc `if-elif-else`.
*   **Tuân thủ chuẩn mã nguồn PEP 8:** Viết mã nguồn Python chuẩn mực với thụt lề 4 khoảng trắng, tên biến và hàm theo kiểu `snake_case`, bổ sung chú thích kiểu dữ liệu (Type Hints).

### **2. Bối cảnh & Vấn đề**
Sàn thương mại điện tử EcoMart đang gặp vấn đề nghiêm trọng với phân hệ tính toán khuyến mãi và phí vận chuyển. Mã nguồn hiện tại được viết bởi nhiều lập trình viên khác nhau, dẫn đến tình trạng các câu lệnh `if-else` bị lồng nhau tới 5-6 tầng. Điều này làm cho hệ thống chạy chậm, khó đọc, dễ phát sinh lỗi khi thêm tính năng mới và vi phạm nghiêm trọng quy chuẩn PEP 8.

Ban kỹ thuật yêu cầu bạn thiết kế lại toàn bộ mô-đun tính toán ưu đãi đơn hàng cho EcoMart. Bạn cần áp dụng tư duy phẳng hóa điều kiện bằng toán tử logic, kiểm tra tính hợp lệ của dữ liệu đầu vào và xuất ra báo cáo chi phí minh bạch cho khách hàng.



### **3. Quy tắc nghiệp vụ**
Hệ thống tiếp nhận thông tin đơn hàng đầu vào gồm 4 thông số:
*   `order_value` (float): Tổng giá trị hàng hóa ban đầu (VNĐ).
*   `customer_tier` (str): Hạng thành viên (`"STANDARD"`, `"GOLD"`, `"DIAMOND"`).
*   `is_first_order` (bool): Đánh dấu có phải đơn hàng đầu tiên của tài khoản hay không.
*   `payment_method` (str): Phương thức thanh toán (`"COD"`, `"E_WALLET"`, `"CREDIT_CARD"`).

Bảng chi tiết quy tắc tính toán khuyến mãi và phí vận chuyển:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: left;">Hạng mục</th>
      <th style="padding: 8px; text-align: left;">Điều kiện áp dụng (Logic phẳng)</th>
      <th style="padding: 8px; text-align: left;">Mức tính toán</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px;">Giảm giá Loại 1 (Ưu tiên 1)</td>
      <td style="padding: 8px;">Khách hàng <code>DIAMOND</code> <strong>HOẶC</strong> giá trị đơn <code>order_value</code> &gt;= 2,000,000 VNĐ</td>
      <td style="padding: 8px;">Giảm 15% đơn hàng (Tối đa 500,000 VNĐ)</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Giảm giá Loại 2 (Ưu tiên 2)</td>
      <td style="padding: 8px;">Khách hàng <code>GOLD</code> <strong>VÀ</strong> phương thức thanh toán là <code>E_WALLET</code> hoặc <code>CREDIT_CARD</code></td>
      <td style="padding: 8px;">Giảm 10% đơn hàng (Tối đa 300,000 VNĐ)</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Giảm giá Loại 3 (Ưu tiên 3)</td>
      <td style="padding: 8px;"><code>is_first_order</code> là True <strong>VÀ</strong> <code>order_value</code> &gt;= 500,000 VNĐ</td>
      <td style="padding: 8px;">Giảm 5% đơn hàng (Tối đa 100,000 VNĐ)</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Không giảm giá</td>
      <td style="padding: 8px;">Các trường hợp còn lại không thỏa mãn các điều kiện trên</td>
      <td style="padding: 8px;">Giảm 0 VNĐ</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Phí vận chuyển (Shipping Fee)</td>
      <td style="padding: 8px;"><code>order_value</code> &gt;= 1,000,000 VNĐ <strong>HOẶC</strong> hạng thành viên là <code>GOLD</code> hoặc <code>DIAMOND</code></td>
      <td style="padding: 8px;">Miễn phí (0 VNĐ). Nếu không thỏa mãn: 30,000 VNĐ</td>
    </tr>
    <tr>
      <td style="padding: 8px;">Quà tặng kèm (Bonus Gift)</td>
      <td style="padding: 8px;">(<code>order_value</code> &gt;= 1,500,000 VNĐ <strong>VÀ</strong> hạng <code>DIAMOND</code>) <strong>HOẶC</strong> (<code>is_first_order</code> là True <strong>VÀ</strong> <code>order_value</code> &gt;= 3,000,000 VNĐ)</td>
      <td style="padding: 8px;">Được tặng "Voucher Quà Tặng Premium"</td>
    </tr>
  </tbody>
</table>

### **4. Yêu cầu bài toán**
1. **Kiểm tra tính hợp lệ của dữ liệu (Input Validation):**
   *   Nếu `order_value` <= 0, phát sinh ngoại lệ `ValueError("Giá trị đơn hàng phải lớn hơn 0")`.
   *   Nếu `customer_tier` không thuộc danh sách `("STANDARD", "GOLD", "DIAMOND")`, phát sinh ngoại lệ `ValueError("Hạng thành viên không hợp lệ")`.
   *   Nếu `payment_method` không thuộc danh sách `("COD", "E_WALLET", "CREDIT_CARD")`, phát sinh ngoại lệ `ValueError("Phương thức thanh toán không hợp lệ")`.

2. **Xây dựng hàm xử lý logic:**
   *   Định nghĩa hàm `calculate_order_summary(order_value: float, customer_tier: str, is_first_order: bool, payment_method: str) -> dict` sử dụng đầy đủ Type Hints.
   *   Sử dụng toán tử logic `and`, `or`, `not` để phẳng hóa mã nguồn. Không lồng câu lệnh `if` quá 2 tầng.
   *   Tính toán số tiền được giảm giá (áp dụng mức trần giảm giá tối đa nếu tiền giảm vượt mức trần).

3. **Tính tổng tiền thanh toán cuối cùng:**
   *   Công thức: `final_payment = order_value - discount_amount + shipping_fee`.

4. **Trả về kết quả và kiểm thử:**
   *   Hàm trả về một dictionary lưu giữ thông tin chi tiết: `original_price`, `discount_amount`, `shipping_fee`, `final_payment`, `has_gift`.
   *   Viết mã kiểm thử trong chương trình chính để gọi hàm với ít nhất 3 bộ dữ liệu đầu vào khác nhau (bao gồm 1 trường hợp biên và 1 trường hợp hợp lệ hoàn hảo) và in kết quả ra màn hình.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex06`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex06`