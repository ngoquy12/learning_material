## <center>[Vận dụng cơ bản 1] Sửa lỗi tính tổng tiền hóa đơn đơn hàng Highlands POS</center>

### **1. Mục tiêu**
*   **Kiến thức:** Hiểu và vận dụng thành thạo thứ tự ưu tiên của các toán tử số học (`+`, `-`, `*`, `/`), toán tử so sánh (`==`) và toán tử logic trong Python mà không cần sử dụng câu lệnh rẽ nhánh (`if/else`).
*   **Kỹ năng:** Phân tích mã nguồn hiện có (code tracing), phát hiện lỗi tính toán sai quy cách do thứ tự ưu tiên toán tử, và thực hiện sửa lỗi để đảm bảo tính đúng đắn cho hệ thống tính tiền POS.
*   **Thái độ:** Tỉ mỉ kiểm tra logic nghiệp vụ tài chính, đảm bảo tính chính xác từng đồng trên hóa đơn của khách hàng.

### **2. Bối cảnh & Vấn đề**
Chuỗi quán cà phê Highlands đang vận hành hệ thống POS (Point of Sale) để thu ngân thực hiện order tại quầy. Hệ thống cho phép nhập giá của thức uống cơ bản, số lượng topping đi kèm (mỗi topping đồng giá 8.000 VNĐ) và xác nhận khách hàng có phải là thành viên Vàng (Gold Member) hay không. Khách hàng sở hữu thẻ Vàng sẽ được giảm 10% trên tổng giá trị hóa đơn (bao gồm cả tiền nước và tiền topping).

Tuy nhiên, bộ phận kế toán vừa ghi nhận phản ánh từ các thu ngân: Khi thanh toán cho khách hàng có thẻ Vàng mua kèm topping, số tiền tính ra bị chênh lệch cao hơn so với thực tế. Khách hàng phàn nàn rằng mức giảm giá 10% dường như chỉ được áp dụng cho tiền topping chứ không giảm cho giá món uống cơ bản.### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn hiện tại của mô-đun tính tiền trên hệ thống POS:

```python
# Highlands POS - Hệ thống tính tiền tại quầy (Phiên bản v1.0)

# Nhập thông tin đơn hàng từ thu ngân
base_price_str = input("Nhập giá tiền món uống cơ bản (VNĐ): ")
topping_count_str = input("Nhập số lượng topping đi kèm: ")
is_gold_member_str = input("Khách hàng có thẻ Vàng không? (True/False): ")

# Ép kiểu dữ liệu đầu vào
base_price = float(base_price_str)
topping_count = int(topping_count_str)
is_gold_member = is_gold_member_str.strip().lower() == "true"

# Khai báo đơn giá topping và tỷ lệ giảm giá
topping_price = 8000
discount_rate = 0.10

# Tính toán tổng số tiền thanh toán cuối cùng
final_total = base_price + topping_count * topping_price * (1 - is_gold_member * discount_rate)

# In kết quả hóa đơn
print("--- HÓA ĐƠN THU NGÂN ---")
print("Tổng tiền thanh toán cuối cùng:", final_total, "VNĐ")
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Báo cáo lỗi (Test Case Report Table)**
Học viên chạy thử đoạn mã nguồn trên, tiến hành truy vết biểu thức tính toán và hoàn thành Bảng báo cáo Test Case dưới đây vào báo cáo cá nhân. 

[NOTE] Hàng đầu tiên (STT 1) là ví dụ mẫu đã hoàn chỉnh. Học viên cần thực hiện tính toán và điền tiếp thông tin cho Hàng 2 và Hàng 3 (thay thế dấu `...`).

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellpadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="text-align: left;">Kết quả từ mã hiện tại (Buggy Output)</th>
      <th style="text-align: left;">Kết quả kỳ vọng đúng (Expected Output)</th>
      <th style="text-align: left;">Ghi chú phân tích logic (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td>base_price = 45000<br>topping_count = 2<br>is_gold_member = True</td>
      <td>59400.0 VNĐ</td>
      <td>54900.0 VNĐ</td>
      <td>Do thiếu dấu ngoặc đóng mở để nhóm tổng tiền trước, toán tử nhân `*` thực hiện tính discount trên giá topping (16.000 * 0.9 = 14.400) rồi mới cộng tiền nước (45.000 + 14.400 = 59.400). Giá trị món nước 45.000 VNĐ bị bỏ sót không giảm 10%.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td>base_price = 60000<br>topping_count = 1<br>is_gold_member = True</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td>base_price = 35000<br>topping_count = 3<br>is_gold_member = False</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn (Source Code Correction)**
*   [REQUIREMENT] Hiệu chỉnh duy nhất biểu thức tính toán `final_total` trong mã nguồn Python để áp dụng tỷ lệ giảm giá 10% cho TOÀN BỘ tổng giá trị đơn hàng (bao gồm tiền món uống cơ bản và tiền topping) khi `is_gold_member` là `True`.
*   [WARNING] TUYỆT ĐỐI KHÔNG sử dụng các câu lệnh rẽ nhánh (`if`, `else`, `elif`), vòng lặp (`for`, `while`), hoặc các kiểu dữ liệu nâng cao (`list`, `dict`, `tuple`, `set`). Bài tập chỉ cho phép sử dụng các toán tử số học, toán tử logic, toán tử so sánh và thứ tự ưu tiên của dấu ngoặc đơn `()`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo kết quả Test Case (điền đầy đủ vào bảng ở Phần 1).
*   Đẩy mã nguồn đã sửa lỗi lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex1`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex1`