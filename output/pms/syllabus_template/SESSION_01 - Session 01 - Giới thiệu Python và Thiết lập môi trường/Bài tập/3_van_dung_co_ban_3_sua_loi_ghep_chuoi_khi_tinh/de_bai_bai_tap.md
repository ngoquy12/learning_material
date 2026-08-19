# <center>[Vận dụng cơ bản 3] Sửa lỗi ghép chuỗi khi tính hóa đơn bán hàng POS</center>

### **1. Mục tiêu**
* Hiểu và vận dụng đúng các kiểu dữ liệu cơ bản trong Python (`str`, `int`, `float`).
* Nhận biết và khắc phục lỗi logic liên quan đến phép toán giữa các kiểu dữ liệu khi xử lý dữ liệu nhập từ người dùng (`input()`).
* Thực hành phương pháp theo vết mã nguồn (code tracing) và lập bảng báo cáo Test Case để kiểm chứng lỗi phần mềm.

### **2. Bối cảnh & Vấn đề**
Hệ thống Quản lý Bán hàng Quán Cà phê (Highlands POS) đang được triển khai tại quầy thu ngân. Khi khách hàng gọi đồ uống, thu ngân sẽ nhập giá niêm yết cơ bản của món, số lượng ly và số lượng topping gọi thêm (mỗi phần topping có giá cố định 8.000 VNĐ).

Bộ phận vận hành nhận được phản ánh từ thu ngân tại cửa hàng: Hệ thống POS xuất hóa đơn với số tiền thanh toán bất thường. Cụ thể, khi nhập 2 ly Trà sen vàng giá 45.000 VNĐ/ly và 2 phần topping củ năng (8.000 VNĐ/phần), thay vì tính tổng tiền là 106.000 VNĐ, trên màn hình và hóa đơn in ra lại hiển thị con số 9000016000 VNĐ.

### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn Python hiện tại đang chạy trên thiết bị POS của quầy thu ngân:

```python

# Hệ thống Quản lý Bán hàng Quán Cà phê (Highlands POS)

# Tệp mã nguồn: pos_receipt_calculator.py

# Nhập thông tin đơn hàng từ thu ngân
base_price_input = input("Nhập giá cơ bản của món (VNĐ): ")
quantity_input = input("Nhập số lượng ly: ")
topping_count_input = input("Nhập số lượng topping: ")

# Xử lý tính toán hóa đơn
base_price = int(base_price_input)
quantity = int(quantity_input)

# Tính thành tiền món uống
drink_subtotal = base_price * quantity

# Tính thành tiền topping (đồng giá 8.000 VNĐ/topping)
topping_subtotal = int(topping_count_input) * 8000

# Tính tổng tiền hóa đơn thanh toán
total_payment = str(drink_subtotal) + str(topping_subtotal)

# In hóa đơn ra màn hình quầy POS
print("\n=== HÓA ĐƠN THU NGÂN ===")
print("Tiền nước:", drink_subtotal, "VNĐ")
print("Tiền topping:", topping_subtotal, "VNĐ")
print("Tổng tiền thanh toán:", total_payment, "VNĐ")
```

# **4. Yêu cầu bài toán**

#### **Phần 1: Code Tracing & Báo cáo Test Case (Lập bảng phân tích lỗi)**
Học viên đọc hiểu mã nguồn, chạy thử chương trình với các trường hợp đầu vào khác nhau để tìm ra vị trí dòng code gây lỗi. Sau đó, hoàn thành bảng báo cáo Test Case dưới đây (Dòng STT 1 đã được thực hiện mẫu, học viên cần suy luận và hoàn thành STT 2 và STT 3):

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="6" cellSpacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; text-align: center;">STT</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Kết quả thực tế lỗi (Buggy Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Dòng code gây lỗi (Failing Line)</th>
      <th style="border: 1px solid #dddddd; text-align: left;">Giải thích nguyên nhân logic (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">1</td>
      <td style="border: 1px solid #dddddd;">Giá món: 45000<br/>Số lượng: 2<br/>Topping: 2</td>
      <td style="border: 1px solid #dddddd;">Tổng tiền thanh toán: 9000016000 VNĐ</td>
      <td style="border: 1px solid #dddddd;">Tổng tiền thanh toán: 106000 VNĐ</td>
      <td style="border: 1px solid #dddddd;"><code>total_payment = str(drink_subtotal) + str(topping_subtotal)</code></td>
      <td style="border: 1px solid #dddddd;">Mã nguồn chuyển các biến số thành kiểu chuỗi (<code>str</code>) trước khi cộng, làm cho toán tử <code>+</code> thực hiện ghép hai chuỗi kí tự <code>"90000"</code> và <code>"16000"</code> thay vì thực hiện phép cộng số học.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">2</td>
      <td style="border: 1px solid #dddddd;">Giá món: 50000<br/>Số lượng: 1<br/>Topping: 3</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; text-align: center;">3</td>
      <td style="border: 1px solid #dddddd;">Giá món: 35000<br/>Số lượng: 3<br/>Topping: 1</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
      <td style="border: 1px solid #dddddd;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa mã nguồn nghiệp vụ**
* Tiến hành sửa đổi mã nguồn Python sao cho chương trình thực hiện đúng phép tính số học giữa tiền nước và tiền topping.
* Đảm bảo dữ liệu đầu ra hiển thị chuẩn xác số tiền tổng thanh toán theo yêu cầu nghiệp vụ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
* Phần phân tích/báo cáo và mã nguồn triển khai.
* Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex3.
  Ví dụ: HNKS25CNTT1_Core_Session_SESSION_01_Ex3
