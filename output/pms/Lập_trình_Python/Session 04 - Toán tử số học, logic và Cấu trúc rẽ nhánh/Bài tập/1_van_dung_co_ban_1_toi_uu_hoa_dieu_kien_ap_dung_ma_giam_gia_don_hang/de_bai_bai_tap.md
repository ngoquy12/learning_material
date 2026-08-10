## <center>[Sửa lỗi mã nguồn] Tối ưu hóa điều kiện áp dụng mã giảm giá đơn hàng</center>

### **1. Mục tiêu**
*   **Phát hiện lỗi logic và vi phạm quy chuẩn:** Nhận biết các lỗi câu lệnh điều kiện sai lệch so với yêu cầu nghiệp vụ E-commerce và tác hại của chống-mẫu lập trình dạng hình mũi tên (Arrow Anti-Pattern).
*   **Phẳng hóa cấu trúc rẽ nhánh:** Áp dụng kết hợp các toán tử logic (`and`, `or`, `not`) để tái cấu trúc mã nguồn lồng nhau phức tạp thành luồng xử lý phẳng, tuân thủ chuẩn PEP 8.
*   **Chuẩn hóa mã nguồn Python:** Áp dụng ghi chú kiểu dữ liệu (Type Hints), đặt tên chuẩn `snake_case`, thụt lề 4 khoảng trắng (4 spaces) và xử lý ngoại lệ đầu vào cơ bản.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống quản lý đơn hàng của sàn thương mại điện tử, bộ phận Marketing triển khai chương trình khuyến mãi "VIP Super Sale". Một đơn hàng chỉ được chấp nhận áp dụng mã giảm giá `VIP_SUPER_SALE` khi thỏa mãn đồng thời tất cả các quy tắc nghiệp vụ sau:
1. Giá trị đơn hàng (`order_value`) phải đạt tối thiểu **500,000 VNĐ**.
2. Tài khoản mua hàng đã hoàn thành tối thiểu **5 đơn hàng thành công** (`total_orders >= 5`).
3. Địa chỉ giao hàng (`location`) thuộc khu vực được hỗ trợ ưu đãi, bao gồm **"HANOI"** hoặc **"HCM"**.

Đoạn mã nguồn legacy hiện tại được bàn giao lại từ một lập trình viên cũ. Chương trình đang gặp phải các vấn đề nghiêm trọng:
*   **Lỗi logic nghiệp vụ:** Một số khách hàng mua đơn chỉ 200,000 VNĐ nhưng vẫn được giảm giá do câu lệnh logic bị viết sai toán tử.
*   **Vi phạm quy chuẩn PEP 8:** Sử dụng thụt lề 2 spaces không đồng nhất, tên biến đặt theo kiểu `camelCase`, thiếu khoảng trắng xung quanh toán tử và cấu trúc câu lệnh `if` lồng nhau quá 4 cấp gây khó đọc, khó bảo trì.
*   **Thừa thiếu kiểm soát dữ liệu:** Không chặn các trường hợp dữ liệu đầu vào bị âm hoặc không hợp lệ.



### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn Python legacy tồn tại lỗi logic và vi phạm chuẩn định dạng:

```python
# Mã nguồn LEGACY: Vi phạm quy chuẩn PEP 8 & chứa lỗi logic nghiệp vụ
def evaluate_voucher_eligibility(orderValue, totalOrders, location):
  if orderValue > 0:
    if totalOrders >= 0:
      if location == "HANOI" or location == "HCM":
        if totalOrders >= 5:
          if orderValue >= 500000 or totalOrders >= 10:
            return "Phe duyet: Ap dung thanh cong ma VIP_SUPER_SALE"
          else:
            return "Tu choi: Don hang chua dat gia tri toi thieu 500.000 VND"
        else:
          return "Tu choi: Khach hang chua dat toi thieu 5 don hang"
      else:
        return "Tu choi: Khu vuc giao hang khong duoc ho tro"
    else:
      return "Loi: So luong don hang khong duoc am"
  else:
    return "Loi: Gia tri don hang phai lon hon 0"
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Lập báo cáo kiểm thử (Test Case Report)**
Học viên chạy thử đoạn mã trên với các bộ dữ liệu đầu vào, phát hiện điểm sai và hoàn thiện bảng báo cáo theo mẫu sau vào file nộp bài:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="text-align: left;">Kết quả đoạn mã cũ (Buggy Output)</th>
      <th style="text-align: left;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="text-align: left;">Ghi chú lỗi</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td>orderValue = 300000<br/>totalOrders = 12<br/>location = "HANOI"</td>
      <td>Phe duyet: Ap dung thanh cong ma VIP_SUPER_SALE</td>
      <td>Tu choi: Don hang chua dat gia tri toi thieu 500.000 VND</td>
      <td>Lỗi toán tử logical `or` làm lọt đơn hàng dưới 500k.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td>orderValue = 600000<br/>totalOrders = 3<br/>location = "HCM"</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td>orderValue = -50000<br/>totalOrders = 5<br/>location = "DANANG"</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Tái cấu trúc và sửa lỗi mã nguồn**
Viết lại hàm `evaluate_voucher_eligibility` tuân thủ các chuẩn sau:
1. **Phẳng hóa cấu trúc logic:** Sử dụng các toán tử kết hợp `and`, `or` để đưa câu lệnh kiểm tra điều kiện phê duyệt về dạng phẳng (tối đa 1 cấp `if/elif/else`), loại bỏ triệt để Arrow Anti-Pattern.
2. **Tuân thủ chuẩn PEP 8:**
   * Thụt lề chuẩn 4 khoảng trắng (4 spaces).
   * Đặt tên hàm và tên biến theo chuẩn `snake_case` (ví dụ: `order_value`, `total_orders`).
   * Sử dụng bổ sung khoảng trắng chuẩn xác quanh các toán tử so sánh và gán.
3. **Bổ sung Type Hints & Xử lý lỗi:**
   * Khai báo rõ kiểu dữ liệu tham số đầu vào (`order_value: float`, `total_orders: int`, `location: str`) và kiểu trả về `-> str`.
   * Bổ sung kiểm soát dữ liệu không hợp lệ (nếu `order_value <= 0` hoặc `total_orders < 0` thì chủ động trả về thông báo lỗi hợp lệ hoặc ném ngoại lệ `ValueError`).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex01`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex01`