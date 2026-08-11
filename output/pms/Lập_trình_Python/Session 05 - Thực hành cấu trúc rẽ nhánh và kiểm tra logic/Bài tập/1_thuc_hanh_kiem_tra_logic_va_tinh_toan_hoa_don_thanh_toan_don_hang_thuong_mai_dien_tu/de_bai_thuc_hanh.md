## <center>Thực Hành Kiểm Tra Logic Và Tính Toán Hóa Đơn Thanh Toán Đơn Hàng Thương Mại Điện Tử</center>

### **1. Mục tiêu**
- Vận dụng thành thạo cấu trúc rẽ nhánh điều khiển `if`, `if-else`, `if-elif-else` và các rẽ nhánh lồng nhau trong Python 3.12.
- Kết hợp linh hoạt các toán tử so sánh (`==`, `!=`, `>`, `<`, `>=`, `<=`) và toán tử logic (`and`, `or`, `not`) để giải quyết các điều kiện kinh doanh thực tế.
- Xử lý nhập/xuất dữ liệu qua Console, thực hiện ép kiểu dữ liệu ép buộc (`int()`, `float()`, `str()`) chính xác và an toàn.
- Áp dụng quy tắc đặt tên biến chuẩn PEP 8 (`snake_case`) và định dạng mã nguồn sạch, dễ bảo trì.

---

### **2. Vấn đề**
Trong phân hệ xử lý đơn hàng của một hệ thống thương mại điện tử (E-commerce Management Subsystem), khi khách hàng tiến hành thanh toán, hệ thống cần tính toán chính xác tổng tiền của hóa đơn. Số tiền cuối cùng phụ thuộc vào nhiều yếu tố bao gồm: hạng thành viên của khách hàng, điều kiện tính phí vận chuyển, và các chương trình khuyến mãi giảm giá áp dụng theo mã coupon.

Hệ thống yêu cầu phát triển một chương trình Python thực thi trên Console để nhận thông tin đơn hàng, kiểm tra tính hợp lệ của dữ liệu đầu vào, áp dụng quy tắc kinh doanh để tính toán các khoản chiết khấu, và in hóa đơn chi tiết cho người dùng.

Dưới đây là sơ đồ luồng xử lý dữ liệu của chương trình:

```mermaid

flowchart TD
    A[/ "Nhập dữ liệu đơn hàng (Tên, Hạng, Giá trị, Mã)" /] --> B{"Giá trị đơn hàng > 0?"}
    B -->|Không| C[/ "In thông báo lỗi: Giá trị đơn hàng không hợp lệ" /]
    B -->|Có| D[/"Tính phần trăm giảm giá theo Hạng thành viên"/]
    D --> E{"Giá trị >= 500.000 VNĐ hoặc Mã == 'FREESHIP'?"}
    E -->|Có| F[/"Phí vận chuyển = 0 VNĐ"/]
    E -->|Không| G[/"Phí vận chuyển = 30.000 VNĐ"/]
    F --> H{"Mã == 'SALE10' và Giá trị >= 200.000 VNĐ?"}
    G --> H
    H -->|Có| I[/"Giảm giá bổ sung = 10.000 VNĐ"/]
    H -->|Không| J[/"Giảm giá bổ sung = 0 VNĐ"/]
    I --> K[/"Tính Tổng thanh toán = Giá gốc - Giảm hạng - Giảm mã + Phí vận chuyển"/]
    J --> K
    K --> L[/ "In hóa đơn thanh toán chi tiết ra màn hình Console" /]

```

---

### **3. Yêu cầu bài toán**

Chương trình cần khai báo và xử lý các tham số đầu vào và đầu ra theo bảng cấu trúc dữ liệu bên dưới:

<table width="100%" border="1" cellSpacing="0" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th width="20%">Tên biến (Python)</th>
      <th width="15%">Kiểu dữ liệu</th>
      <th width="25%">Giá trị / Định dạng</th>
      <th width="40%">Mô tả chi tiết</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>customer_name</code></td>
      <td><code>str</code></td>
      <td>Chuỗi văn bản bất kỳ</td>
      <td>Họ và tên của khách hàng mua hàng.</td>
    </tr>
    <tr>
      <td><code>member_tier</code></td>
      <td><code>str</code></td>
      <td><code>BRONZE</code>, <code>SILVER</code>, <code>GOLD</code></td>
      <td>Hạng thành viên hiện tại của khách hàng.</td>
    </tr>
    <tr>
      <td><code>order_amount</code></td>
      <td><code>float</code></td>
      <td>Số thực lớn hơn 0</td>
      <td>Tổng giá trị đơn hàng ban đầu (chưa tính giảm giá và phí ship).</td>
    </tr>
    <tr>
      <td><code>promo_code</code></td>
      <td><code>str</code></td>
      <td><code>FREESHIP</code>, <code>SALE10</code>, <code>NONE</code></td>
      <td>Mã giảm giá do người dùng nhập vào.</td>
    </tr>
    <tr>
      <td><code>tier_discount_rate</code></td>
      <td><code>float</code></td>
      <td>0.0, 0.05, 0.10</td>
      <td>Tỷ lệ giảm giá dựa trên hạng thành viên.</td>
    </tr>
    <tr>
      <td><code>shipping_fee</code></td>
      <td><code>float</code></td>
      <td>0.0 hoặc 30000.0</td>
      <td>Phí vận chuyển đơn hàng.</td>
    </tr>
    <tr>
      <td><code>promo_discount</code></td>
      <td><code>float</code></td>
      <td>0.0 hoặc 10000.0</td>
      <td>Số tiền giảm thêm từ mã khuyến mãi.</td>
    </tr>
    <tr>
      <td><code>final_total</code></td>
      <td><code>float</code></td>
      <td>Số thực >= 0</td>
      <td>Số tiền cuối cùng khách hàng phải thanh toán.</td>
    </tr>
  </tbody>
</table>

---

### **4. Quy tắc xử lý**

Yêu cầu 1: Kiểm tra tính hợp lệ của giá trị đơn hàng
- Nhập dữ liệu từ bàn phím bằng hàm `input()` và ép kiểu giá trị đơn hàng sang `float`.
- Nếu `order_amount <= 0`, hiển thị thông báo: `[LỖI] Giá trị đơn hàng không hợp lệ. Giá trị phải lớn hơn 0.` và kết thúc xử lý (không thực hiện các bước tính toán bên dưới).

Yêu cầu 2: Xác định chiết khấu theo Hạng thành viên (`member_tier`)
- Nếu `member_tier` là `"GOLD"`: Tỷ lệ giảm giá `tier_discount_rate = 0.10` (Giảm 10%).
- Nếu `member_tier` là `"SILVER"`: Tỷ lệ giảm giá `tier_discount_rate = 0.05` (Giảm 5%).
- Nếu `member_tier` là `"BRONZE"` hoặc các giá trị khác: Tỷ lệ giảm giá `tier_discount_rate = 0.0` (Giảm 0%).
- Công thức tính số tiền giảm hạng thành viên: `tier_discount_amount = order_amount * tier_discount_rate`.

Yêu cầu 3: Tính Phí vận chuyển (`shipping_fee`)
- Đơn hàng được miễn phí vận chuyển (`shipping_fee = 0.0`) nếu thỏa mãn MỘT TRONG HAI điều kiện sau:
  + Tổng giá trị đơn hàng gốc `order_amount >= 500000.0`
  + Hoặc mã giảm giá `promo_code == "FREESHIP"`
- Trường hợp không thỏa mãn cả hai điều kiện trên, phí vận chuyển mặc định là: `shipping_fee = 30000.0`.

Yêu cầu 4: Tính Giảm giá bổ sung từ Mã khuyến mãi (`promo_discount`)
- Nếu mã giảm giá `promo_code == "SALE10"` ĐỒNG THỜI tổng giá trị đơn hàng gốc `order_amount >= 200000.0`, khách hàng được giảm thêm `promo_discount = 10000.0`.
- Các trường hợp còn lại: `promo_discount = 0.0`.

Yêu cầu 5: Tính Tổng tiền thanh toán (`final_total`)
- Công thức tính tổng tiền thanh toán: `final_total = order_amount - tier_discount_amount - promo_discount + shipping_fee`.

Yêu cầu 6: Hiển thị hóa đơn thanh toán chi tiết
- In ra màn hình thông tin chi tiết hóa đơn theo mẫu định dạng trong ví dụ bên dưới.

---

### **Ví dụ minh họa Input / Output**

#### **Kịch bản 1: Đơn hàng hợp lệ - Hạng GOLD có mã FREESHIP**
Input:
```text
Nhập tên khách hàng: Nguyễn Văn A
Nhập hạng thành viên (BRONZE/SILVER/GOLD): GOLD
Nhập tổng giá trị đơn hàng (VNĐ): 600000
Nhập mã giảm giá (FREESHIP/SALE10/NONE): FREESHIP
```

Output:
```text
================ HÓA ĐƠN THANH TOÁN ================
Khách hàng: Nguyễn Văn A
Hạng thành viên: GOLD (Giảm 10%)
----------------------------------------------------
Giá trị đơn hàng gốc: 600000.0 VNĐ
Giảm giá hạng thành viên: -60000.0 VNĐ
Giảm giá từ mã khuyến mãi: -0.0 VNĐ
Phí vận chuyển: 0.0 VNĐ
----------------------------------------------------
TỔNG TIỀN THANH TOÁN: 540000.0 VNĐ
====================================================
```

#### **Kịch bản 2: Đơn hàng hợp lệ - Hạng SILVER sử dụng mã SALE10**
Input:
```text
Nhập tên khách hàng: Lê Thị B
Nhập hạng thành viên (BRONZE/SILVER/GOLD): SILVER
Nhập tổng giá trị đơn hàng (VNĐ): 300000
Nhập mã giảm giá (FREESHIP/SALE10/NONE): SALE10
```

Output:
```text
================ HÓA ĐƠN THANH TOÁN ================
Khách hàng: Lê Thị B
Hạng thành viên: SILVER (Giảm 5%)
----------------------------------------------------
Giá trị đơn hàng gốc: 300000.0 VNĐ
Giảm giá hạng thành viên: -15000.0 VNĐ
Giảm giá từ mã khuyến mãi: -10000.0 VNĐ
Phí vận chuyển: 30000.0 VNĐ
----------------------------------------------------
TỔNG TIỀN THANH TOÁN: 305000.0 VNĐ
====================================================
```

#### **Kịch bản 3: Đơn hàng không hợp lệ (Giá trị <= 0)**
Input:
```text
Nhập tên khách hàng: Phạm Văn C
Nhập hạng thành viên (BRONZE/SILVER/GOLD): BRONZE
Nhập tổng giá trị đơn hàng (VNĐ): -50000
Nhập mã giảm giá (FREESHIP/SALE10/NONE): NONE
```

Output:
```text
[LỖI] Giá trị đơn hàng không hợp lệ. Giá trị phải lớn hơn 0.
```

---

### **5. Yêu cầu nộp bài**
- Cấu trúc thư mục dự án nộp bài:
  ```text
  session05_lab/
  └── main.py
  ```
- File mã nguồn duy nhất đặt tên là `main.py`.
- Thực thi chương trình qua Terminal bằng lệnh:
  `python main.py`
- Đẩy mã nguồn lên kho chứa GitHub cá nhân và nộp liên kết kho chứa (Repository URL) lên hệ thống quản lý học tập.