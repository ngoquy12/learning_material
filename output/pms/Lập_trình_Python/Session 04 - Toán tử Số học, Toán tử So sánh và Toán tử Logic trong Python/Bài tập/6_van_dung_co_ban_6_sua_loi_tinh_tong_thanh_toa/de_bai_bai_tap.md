# <center>[Vận dụng cơ bản 6] Sửa lỗi tính tổng thanh toán hóa đơn đặt phòng</center>

### **1. Mục tiêu**
*   Đọc hiểu mã nguồn Python hiện tại xử lý tính toán tổng tiền thanh toán đơn đặt phòng khách sạn.
*   Phát hiện và phân tích lỗi logic trong biểu thức tính chiết khấu hội viên và phụ phí lưu trú.
*   Lập bảng trace Test Case để so sánh kết quả tính sai của hệ thống cũ và kết quả kỳ vọng đúng.
*   Sửa mã nguồn để tính toán chính xác theo đúng quy tắc nghiệp vụ trong phạm vi kiến thức toán tử số học và so sánh đã học.

### **2. Bối cảnh & Vấn đề**
Hệ thống đặt phòng khách sạn trực tuyến (HOTEL_BOOKING) đang nhận phản ánh từ bộ phận Kế toán và Khách hàng về việc số tiền thanh toán bị tính sai đối với các đơn đặt phòng có dịch vụ bổ sung.

Phản ánh thực tế: Khách hàng là thành viên thân thiết (hội viên) khi đặt phòng có đăng ký check-in sớm (trước 12h trưa) và dịch vụ vệ sinh phòng nhận thấy tổng tiền thanh toán hiển thị bị lệch so với chính sách niêm yết. Theo quy định, chính sách giảm giá 10% dành cho hội viên **chỉ áp dụng trên tiền phòng cơ bản**, không áp dụng giảm giá cho các khoản phụ thu check-in sớm và phí dịch vụ vệ sinh. Tuy nhiên, hệ thống hiện tại đang tính giảm giá lên toàn bộ tổng chi phí khiến doanh thu thu về bị thất thoát.

### **3. Mã nguồn hiện tại**

```python
def calculate_booking_invoice(
    room_price: float,
    nights: int,
    is_early_checkin: bool,
    cleaning_fee: float,
    is_member: bool
) -> float:
    """
    Tính tổng tiền thanh toán cho đơn đặt phòng khách sạn.
    """
    base_cost: float = room_price * nights
    early_surcharge: float = room_price * 0.3 * is_early_checkin

# Tính tổng thanh toán hóa đơn
    total_payment: float = (base_cost + early_surcharge + cleaning_fee) * (1.0 - 0.10 * is_member)
    return total_payment

# Chạy thử nghiệm hệ thống
if __name__ == "__main__":
    price = 1000000.0

# Giá phòng 1,000,000 VNĐ / đêm
    num_nights = 2

# Lưu trú 2 đêm
    early = True

# Có check-in sớm
    cleaning = 200000.0

# Phí vệ sinh 200,000 VNĐ
    member = True

# Khách hàng là hội viên

    result = calculate_booking_invoice(price, num_nights, early, cleaning, member)
    print("Tổng tiền thanh toán tính được:", result)
```

# **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Lập Báo cáo Test Case (Trace lỗi)**
Học viên tiến hành kiểm tra mã nguồn, xác định chính xác dòng code gây ra lỗi logic và hoàn thiện Bảng Test Case dưới đây vào báo cáo (Dòng 1 là ví dụ mẫu đã hoàn thành, học viên thực hiện tiếp cho dòng 2 và dòng 3):

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #ccc; padding: 8px; text-align: center;">STT</th>
      <th style="border: 1px solid #ccc; padding: 8px; text-align: center;">Mã kiểm thử (Input)</th>
      <th style="border: 1px solid #ccc; padding: 8px; text-align: center;">Kết quả hiện tại (Buggy Output)</th>
      <th style="border: 1px solid #ccc; padding: 8px; text-align: center;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="border: 1px solid #ccc; padding: 8px; text-align: center;">Dòng code gây lỗi (Failing Line)</th>
      <th style="border: 1px solid #ccc; padding: 8px; text-align: center;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">1</td>
      <td style="border: 1px solid #ccc; padding: 8px;">room_price = 1000000.0<br/>nights = 2<br/>is_early_checkin = True<br/>cleaning_fee = 200000.0<br/>is_member = True</td>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">2250000.0</td>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">2300000.0</td>
      <td style="border: 1px solid #ccc; padding: 8px;"><code>total_payment = (base_cost + early_surcharge + cleaning_fee) * (1.0 - 0.10 * is_member)</code></td>
      <td style="border: 1px solid #ccc; padding: 8px;">Mã nguồn cũ nhân tỷ lệ giảm giá 10% trên tổng toàn bộ chi phí bao gồm cả phụ thu check-in sớm (300,000) và phí vệ sinh (200,000), khiến giảm giá vượt quá quy định.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">2</td>
      <td style="border: 1px solid #ccc; padding: 8px;">room_price = 2000000.0<br/>nights = 1<br/>is_early_checkin = False<br/>cleaning_fee = 100000.0<br/>is_member = True</td>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">3</td>
      <td style="border: 1px solid #ccc; padding: 8px;">room_price = 1500000.0<br/>nights = 3<br/>is_early_checkin = True<br/>cleaning_fee = 300000.0<br/>is_member = True</td>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px; text-align: center;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
      <td style="border: 1px solid #ccc; padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa mã nguồn nghiệp vụ**
Viết lại hàm `calculate_booking_invoice` sao cho đảm bảo các quy tắc nghiệp vụ sau:
1.  **Tiền phòng cơ bản**: `room_price * nights`
2.  **Phụ thu check-in sớm**: Tính 30% giá phòng 1 đêm (`room_price * 0.3`) khi `is_early_checkin` là `True`.
3.  **Chiết khấu hội viên**: Giảm 10% **chỉ tính trên tiền phòng cơ bản** (`base_cost * 0.10`) khi `is_member` là `True`.
4.  **Tổng tiền thanh toán cuối cùng**: `(Tiền phòng cơ bản - Chiết khấu hội viên) + Phụ thu check-in sớm + Phí vệ sinh`.
5.  [REQUIREMENT]: Tuyệt đối KHÔNG sử dụng câu lệnh rẽ nhánh (`if`/`else`), vòng lặp (`for`/`while`), danh sách (`list`/`dict`), hoặc các toán tử logic `and`/`or`/`not`. Chỉ sử dụng biểu thức số học và ép kiểu/nhân bản giá trị Boolean đã được học.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_SessionSession 04_Ex6.
    Ví dụ: HNKS25CNTT1_Core_Session_Session 04_Ex6
