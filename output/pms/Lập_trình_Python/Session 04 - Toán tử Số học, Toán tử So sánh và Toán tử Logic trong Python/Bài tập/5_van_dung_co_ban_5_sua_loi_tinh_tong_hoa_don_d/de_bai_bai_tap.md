# <center>[Vận dụng cơ bản 5] Sửa lỗi tính tổng hóa đơn đặt phòng khách sạn khi có phụ thu check-in sớm và thuế VAT</center>

### **1. Mục tiêu**
* **Kiến thức:** Củng cố kiến thức về thứ tự ưu tiên của toán tử số học (`*`, `/`, `+`, `-`) và toán tử so sánh trong ngôn ngữ lập trình Python.
* **Kỹ năng:** Phân tích mã nguồn kế thừa (legacy code), thực hiện truy vết mã nguồn (code tracing) để phát hiện và sửa các lỗi sai lệch thứ tự ưu tiên toán tử trong biểu thức tính toán hóa đơn.
* **Thực tiễn:** Đảm bảo tính chính xác cho module quyết toán hóa đơn đặt phòng (`BookingReservation`) thuộc hệ thống đặt phòng trực tuyến (Agoda / Traveloka).

### **2. Bối cảnh & Vấn đề**
Hệ thống Đặt phòng Khách sạn & Homestay đang vận hành module tự động tính hóa đơn cho khách hàng khi thực hiện thủ tục nhận phòng (check-in). Theo quy trình, hóa đơn bao gồm tiền phòng cơ bản, phụ thu nhận phòng sớm (nếu check-in trước 12h trưa), phụ thu khách vượt định mức và thuế giá trị gia tăng (VAT 10%).

Tuy nhiên, đội ngũ hỗ trợ khách hàng liên tục nhận được phản ánh: Tổng số tiền thanh toán hiển thị trên ứng dụng bị dội lên cao bất thường (gần gấp đôi so với thực tế) đối với các đơn đặt phòng có phát sinh nhận phòng sớm và có thêm người lưu trú.

### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn Python đang chạy thực tế trên hệ thống bị ghi nhận lỗi:

```python
def calculate_booking_invoice(
    room_rate_per_night: float,
    num_nights: int,
    checkin_hour: int,
    extra_guest_count: int,
    extra_guest_fee_per_person: float
) -> float:
    """
    Tính tổng hóa đơn thanh toán cho đơn đặt phòng khách sạn.
    
    Quy tắc nghiệp vụ:
    1. Tiền phòng cơ bản = room_rate_per_night * num_nights
    2. Check-in sớm (< 12h) phụ thu 30% giá 1 đêm phòng.
    3. Phụ thu khách phát sinh = extra_guest_count * extra_guest_fee_per_person
    4. Tổng tiền dịch vụ trước thuế (subtotal) = tiền phòng + phụ thu check-in + phụ thu khách
    5. Thuế VAT 10% tính trên tổng tiền dịch vụ trước thuế (subtotal).
    6. Tổng thanh toán = subtotal + tiền thuế VAT.
    """

# 1. Tính tổng tiền phòng cơ bản
    base_room_cost: float = room_rate_per_night * num_nights

# 2. Kiểm tra điều kiện nhận phòng sớm (trước 12h trưa)
    is_early_checkin: bool = checkin_hour < 12
    early_surcharge: float = room_rate_per_night * 0.30 * is_early_checkin

# 3. Tính phụ thu số lượng khách đi kèm vượt quy định
    extra_guest_cost: float = extra_guest_count * extra_guest_fee_per_person

# 4. Tính tổng tiền chi phí trước thuế (Subtotal)
    subtotal: float = base_room_cost + early_surcharge + extra_guest_cost

# 5. Tính số tiền thuế VAT 10%
    vat_amount: float = base_room_cost + early_surcharge * 0.10

# 6. Tính tổng thanh toán cuối cùng
    total_payment: float = subtotal + vat_amount
    
    return total_payment

# Chạy thử nghiệm hệ thống
if __name__ == "__main__":
    test_total: float = calculate_booking_invoice(
        room_rate_per_night=1000000.0,
        num_nights=2,
        checkin_hour=10,
        extra_guest_count=1,
        extra_guest_fee_per_person=150000.0
    )
    print(f"Tổng hóa đơn thanh toán tính được: {test_total:,.0f} VNĐ")
```

# **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Báo cáo Test Case (Code Tracing)**
Học viên thực hiện truy vết mã nguồn (Code Tracing), xác định dòng code gây lỗi và hoàn thành Báo cáo Test Case theo bảng mẫu dưới đây:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="8">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="text-align: center;">STT</th>
      <th style="text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="text-align: center;">Kết quả bị lỗi (Buggy Output)</th>
      <th style="text-align: center;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="text-align: center;">Dòng code gây lỗi</th>
      <th style="text-align: left;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">1</td>
      <td>
        room_rate = 1,000,000<br/>
        num_nights = 2<br/>
        checkin_hour = 10<br/>
        extra_guest_count = 1<br/>
        extra_guest_fee = 150,000
      </td>
      <td style="text-align: center;">4,480,000 VNĐ</td>
      <td style="text-align: center;">2,695,000 VNĐ</td>
      <td style="text-align: center;">Dòng 28</td>
      <td>Do thiếu ngoặc nhóm <code>subtotal</code> và sử dụng sai biến tính VAT, phép nhân <code>0.10</code> thực hiện trước phép cộng, làm số tiền VAT bị cộng thừa toàn bộ tiền phòng cơ bản 2,000,000 VNĐ.</td>
    </tr>
    <tr>
      <td style="text-align: center;">2</td>
      <td>
        room_rate = 2,000,000<br/>
        num_nights = 1<br/>
        checkin_hour = 14<br/>
        extra_guest_count = 0<br/>
        extra_guest_fee = 150,000
      </td>
      <td style="text-align: center;">...</td>
      <td style="text-align: center;">...</td>
      <td style="text-align: center;">...</td>
      <td>...</td>
    </tr>
    <tr>
      <td style="text-align: center;">3</td>
      <td>
        room_rate = 1,500,000<br/>
        num_nights = 3<br/>
        checkin_hour = 9<br/>
        extra_guest_count = 2<br/>
        extra_guest_fee = 200,000
      </td>
      <td style="text-align: center;">...</td>
      <td style="text-align: center;">...</td>
      <td style="text-align: center;">...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Mã nguồn khắc phục**
* Tiến hành sửa trực tiếp mã nguồn trong file Python để tính chính xác thuế VAT 10% dựa trên tổng số tiền trước thuế `subtotal`.
* Tuân thủ chuẩn định dạng Python PEP 8, thêm đầy đủ `type hints` cho tham số và kiểu trả về của hàm.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
* Phần phân tích/báo cáo và mã nguồn triển khai.
* Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex5`.
  Ví dụ: `HNKS25CNTT1_Core_Session_Session 04_Ex5`
