## <center>[Vận dụng cơ bản 2] Sửa lỗi tính phụ phí và xác thực ưu đãi đặt phòng</center>

### **1. Mục tiêu**

- Hiểu và áp dụng đúng thứ tự ưu tiên của các toán tử số học, so sánh và toán tử logic (`and`, `or`) trong Python 3.12.
- Rèn luyện kỹ năng đọc kiểm mã nguồn (code tracing) để phát hiện lỗi sai lệch kết quả do thiếu dấu ngoặc đơn đóng/mở nhóm biểu thức logic.
- Thực hiện sửa lỗi mã nguồn theo đúng quy tắc nghiệp vụ tính phụ phí check-in và duyệt Voucher ưu đãi của hệ thống đặt phòng khách sạn.

### **2. Bối cảnh & Vấn đề**

Trong hệ thống Đặt phòng Khách sạn & Homestay (HOTEL_BOOKING), phân hệ xử lý đơn hàng chịu trách nhiệm tự động tính tổng tiền thanh toán và kiểm tra điều kiện phê duyệt ưu đãi Voucher cho khách hàng.

**Quy tắc nghiệp vụ của hệ thống:**

1.  **Tính tổng tiền thanh toán:**
    - `Giá phòng gốc` = `room_rate` \* `num_nights`.
    - `Phụ thu check-in sớm`: Nếu khách check-in trước 12h trưa (`checkin_hour < 12`), phụ thu bằng 30% giá phòng của 1 đêm (`room_rate * 0.3`). Nếu không check-in sớm, phụ thu bằng 0.
    - `Tổng tiền thanh toán` = `Giá phòng gốc` + `Phụ thu check-in sớm`.
2.  **Điều kiện phê duyệt ưu đãi Voucher:** Khách hàng chỉ được cấp Voucher khi thỏa mãn đồng thời hai điều kiện:
    - _Nhóm điều kiện khách hàng:_ Có điểm tích lũy `loyalty_points >= 500` HOẶC đặt phòng vào đợt khuyến mãi (`is_promo_event == True`).
    - _Bắt buộc về thời gian:_ Số đêm lưu trú phải từ 2 đêm trở lên (`num_nights >= 2`).

**Sự cố ghi nhận:**
Bộ phận Vận hành phản ánh rằng nhiều đơn đặt phòng 1 đêm (`num_nights = 1`) mặc dù không đủ điều kiện tối thiểu 2 đêm nhưng vẫn được hệ thống tự động phê duyệt Voucher ưu đãi nếu khách hàng có điểm tích lũy trên 500 điểm.###

**3. Mã nguồn hiện tại**
Dưới đây là đoạn mã Python đang vận hành bị phản ánh có lỗi logic:

```python
# Thông tin từ đơn đặt phòng khách hàng
room_rate: int = 1200000
num_nights: int = 1
checkin_hour: int = 10
loyalty_points: int = 600
is_promo_event: bool = False

# Kiểm tra điều kiện check-in sớm
is_early_checkin: bool = checkin_hour < 12

# Tính phụ thu check-in sớm (30% giá 1 đêm nếu check-in sớm)
early_surcharge: float = is_early_checkin * room_rate * 0.3

# Tính tổng tiền thanh toán
total_payment: float = room_rate * num_nights + early_surcharge

# Kiểm tra điều kiện phê duyệt Voucher ưu đãi
# Biểu thức kiểm tra bị phản ánh sai sót kết quả:
is_discount_approved: bool = loyalty_points >= 500 or is_promo_event and num_nights >= 2

# In kết quả kiểm tra hệ thống
print(f"Trạng thái check-in sớm: {is_early_checkin}")
print(f"Phụ thu check-in sớm: {early_surcharge} VNĐ")
print(f"Tổng tiền thanh toán: {total_payment} VNĐ")
print(f"Kết quả duyệt Voucher: {is_discount_approved}")
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Phát hiện lỗi logic (Báo cáo Test Case)**

Học viên thực hiện chạy thử mã nguồn (code tracing) với các bộ dữ liệu khác nhau, xác định dòng mã gây ra lỗi logic và hoàn thành Bảng Báo cáo Test Case theo mẫu dưới đây vào báo cáo cá nhân:

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1" cellPadding="6" cellSpacing="0">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="border: 1px solid #dddddd; padding: 8px;">STT</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Dữ liệu đầu vào (Input)</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Kết quả thực tế (Buggy Output)</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Dòng code gây lỗi (Failing Line)</th>
      <th style="border: 1px solid #dddddd; padding: 8px;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">1</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">loyalty_points = 600<br/>is_promo_event = False<br/>num_nights = 1</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">is_discount_approved = True</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">is_discount_approved = False</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Dòng 17</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">Do toán tử 'and' có độ ưu tiên cao hơn 'or', biểu thức bị tách thành `loyalty_points >= 500` OR `(is_promo_event and num_nights >= 2)`. Khách có 600 điểm nên vế trái trả về True.</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">2</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">loyalty_points = 400<br/>is_promo_event = True<br/>num_nights = 1</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="border: 1px solid #dddddd; padding: 8px; text-align: center;">3</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">loyalty_points = 550<br/>is_promo_event = False<br/>num_nights = 3</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
      <td style="border: 1px solid #dddddd; padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn (Source Code Correction)**

- Tiến hành cập nhật lại biểu thức kiểm tra điều kiện `is_discount_approved` trong tệp mã nguồn Python để đảm bảo ưu tiên gom nhóm điều kiện khách hàng trước khi kết hợp với điều kiện số đêm lưu trú tối thiểu.
- Đảm bảo toàn bộ biến khai báo có type hints chuẩn xác và tuân thủ định dạng PEP 8.

### **5. Yêu cầu nộp bài**

Học viên cần nộp:

- Phần phân tích/báo cáo và mã nguồn triển khai.
- Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex2`.
  Ví dụ: `HNKS25CNTT1_Core_Session_Session 04_Ex2`
