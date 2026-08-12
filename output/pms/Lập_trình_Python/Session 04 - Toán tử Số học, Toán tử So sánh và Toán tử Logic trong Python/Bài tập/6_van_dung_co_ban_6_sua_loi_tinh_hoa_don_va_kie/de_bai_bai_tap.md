## <center>[Vận dụng cơ bản 6] Sửa lỗi tính hóa đơn và kiểm tra ưu đãi thẻ thành viên POS</center>

### **1. Mục tiêu**
*   **Kiến thức:** Đánh giá và củng cố hiểu biết về thứ tự ưu tiên của toán tử số học (`+`, `-`, `*`), toán tử so sánh (`>=`) và toán tử logic (`and`, `or`, `not`) trong Python.
*   **Kỹ năng:** Rèn luyện kỹ năng đọc hiểu mã nguồn (Code Tracing), phát hiện các sai sót logic ẩn (subtle logic bugs) liên quan đến đóng mở ngoặc đơn và kết hợp toán tử logic mà không làm gián đoạn cú pháp chương trình.
*   **Thực tiễn:** Áp dụng vào module tính hóa đơn tự động và xét duyệt voucher ưu đãi trong Hệ thống Quản lý Bán hàng Quán Cà phê / Trà sữa (Highlands POS).

### **2. Bối cảnh & Vấn đề**
Chuỗi cửa hàng Highlands POS áp dụng quy tắc tính tiền đơn hàng và chương trình ưu đãi dành cho khách hàng như sau:
*   Mỗi ly nước cơ bản có giá tiền gốc `base_price` (VNĐ).
*   Khách hàng có thể gọi thêm các loại topping với giá cố định 8.000 VNĐ/topping.
*   Nếu khách hàng sở hữu **Thẻ thành viên Vàng** (`is_gold = True`), tổng chi phí hóa đơn (gồm nước và topping) sẽ được **giảm 10%** (tương đương nhân với `0.9`). Thành viên thường không được giảm giá (giảm 0%).
*   Khách hàng được nhận **Voucher sinh nhật** khi đơn hàng thỏa mãn đồng thời hai điều kiện: Tổng tiền thanh toán sau giảm giá đạt từ **100.000 VNĐ trở lên** VÀ số lượng topping đi kèm đạt từ **2 topping trở lên**.

Bộ phận vận hành Highlands POS ghi nhận sự cố: Thu ngân phản ánh rằng khi nhập thông tin order của khách hàng có thẻ Vàng, tổng số tiền thanh toán thực tế bị sai lệch nghiêm trọng (tiền thanh toán chỉ giảm đi 0.1 VNĐ thay vì 10%). Đồng thời, hệ thống tự động xác nhận tặng Voucher sinh nhật cho các đơn hàng không đủ điều kiện theo quy định.### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn hiện tại của hệ thống POS đang gặp lỗi logic:

```python
# Hệ thống Highlands POS - Module tính tổng đơn hàng và kiểm tra voucher ưu đãi
base_price = int(input("Nhập giá tiền nước cơ bản (VNĐ): "))
num_toppings = int(input("Nhập số lượng topping: "))
is_gold = input("Khách hàng có thẻ Vàng (True/False): ") == "True"

# Tính tỷ lệ giảm giá áp dụng (10% cho thẻ Vàng, 0% cho thẻ thường)
discount_rate = 0.1 * is_gold

# Tính tổng tiền thanh toán của đơn hàng sau giảm giá
final_amount = base_price + num_toppings * 8000 * 1 - discount_rate

# Kiểm tra điều kiện nhận Voucher quà tặng sinh nhật
eligible_voucher = final_amount >= 100000 or num_toppings >= 2

# Hiển thị kết quả ra màn hình POS
print("Tổng tiền thanh toán:", final_amount, "VNĐ")
print("Được nhận Voucher quà tặng:", eligible_voucher)
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Tracing mã nguồn (Báo cáo Test Case)**
Học viên thực hiện chạy tay (Code Tracing) mã nguồn hiện tại, xác định chính xác nguyên nhân lỗi logic và hoàn thành bảng báo cáo Test Case dưới đây.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="6" cellSpacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center; width: 5%;">STT</th>
      <th style="text-align: left; width: 25%;">Dữ liệu đầu vào (Input)</th>
      <th style="text-align: left; width: 20%;">Kết quả hiện tại (Buggy Output)</th>
      <th style="text-align: left; width: 20%;">Kết quả mong đợi (Expected Output)</th>
      <th style="text-align: left; width: 30%;">Ghi chú phân tích logic lỗi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td><code>base_price = 90000</code><br><code>num_toppings = 2</code><br><code>is_gold = True</code></td>
      <td><code>final_amount = 105999.9</code><br><code>eligible_voucher = True</code></td>
      <td><code>final_amount = 95400.0</code><br><code>eligible_voucher = False</code></td>
      <td>Do thiếu dấu ngoặc đơn xác định thứ tự ưu tiên, phép nhân thực hiện trước phép cộng làm cho <code>base_price</code> không được giảm giá, đồng thời dùng nhầm toán tử <code>or</code> thay vì <code>and</code>.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td><code>base_price = 50000</code><br><code>num_toppings = 1</code><br><code>is_gold = False</code></td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td><code>base_price = 80000</code><br><code>num_toppings = 3</code><br><code>is_gold = True</code></td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa đổi và Hoàn thiện Mã nguồn**
*   Sửa lỗi biểu thức tính toán `final_amount` để đảm bảo áp dụng mức giảm giá `discount_rate` chính xác trên toàn bộ tổng tiền order (gồm giá nước và topping).
*   Sửa biểu thức logic `eligible_voucher` để kiểm tra chính xác điều kiện nhận Voucher sinh nhật.
*   **Ràng buộc phạm vi kỹ thuật:** KHÔNG sử dụng câu lệnh rẽ nhánh `if/else`, không dùng vòng lặp, không khai báo hàm `def` hay sử dụng cấu trúc dữ liệu nâng cao. Chỉ sử dụng các toán tử số học, toán tử so sánh và toán tử logic trong phạm vi bài học.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex6`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 04_Ex6`