# <center>[Vận dụng cơ bản 1] Sửa lỗi tính phụ thu check-in sớm hệ thống đặt phòng</center>

### **1. Mục tiêu**
*   **Kiến thức:** Hiểu và vận dụng đúng thứ tự ưu tiên của các toán tử số học (`*`, `/`, `+`, `-`) và dấu ngoặc đơn `()` trong Python 3.12.
*   **Kỹ năng:** Phân tích mã nguồn (Code Tracing), phát hiện sai sót trong công thức tính toán tài chính của hệ thống đặt phòng, và sửa lại mã nguồn đúng quy tắc nghiệp vụ.
*   **Thực tế nghiệp vụ:** Đảm bảo hệ thống tính chính xác tổng chi phí hóa đơn cho đơn đặt phòng (`BookingReservation`) bao gồm tiền phòng theo đêm, phụ thu nhận phòng sớm (Early Check-in Surcharge) và phí dịch vụ dọn dẹp cố định.

### **2. Bối cảnh & Vấn đề**
Bộ phận Chăm sóc khách hàng của ứng dụng đặt phòng khách sạn Agoda / Traveloka vừa tiếp nhận phản ánh từ người dùng: Hệ thống tự động tính sai tổng tiền thanh toán của các đơn đặt phòng. 

Cụ thể, đối với khách hàng đặt phòng thông thường (không đăng ký check-in sớm), hóa đơn thanh toán hiển thị số tiền thấp một cách bất thường, gần như chỉ tính tiền phí dịch vụ dọn dẹp mà bỏ quên toàn bộ tiền phòng lưu trú. Trong khi đó, khách hàng chọn check-in sớm lại bị tính sai giá trị phụ thu khiến tổng tiền biến động không chính xác.

Ví dụ: Khách hàng đặt 2 đêm với giá 1,000,000 VND/đêm, phí dọn dẹp 100,000 VND và không check-in sớm. Tổng tiền đúng phải thanh toán là 2,100,000 VND, nhưng hệ thống hiện tại lại kết xuất hóa đơn chỉ có 100,000 VND.

### **3. Mã nguồn hiện tại**
Dưới đây là mã nguồn Python đang chạy trên môi trường thử nghiệm bị phản ánh tính toán sai:

```python

# Khai báo thông tin đơn đặt phòng khách sạn (BookingReservation)
room_price_per_night: float = 1200000.0

# Giá phòng tiêu chuẩn 1 đêm (VND)
nights_count: int = 3

# Số đêm lưu trú
early_checkin_rate: float = 0.30

# Tỷ lệ phụ thu check-in sớm (30% giá của 1 đêm)
has_early_checkin: int = 0

# 1: Có check-in sớm, 0: Không check-in sớm
cleaning_fee: float = 150000.0

# Phí dịch vụ dọn dẹp phòng cố định (VND)

# Biểu thức tính tổng tiền thanh toán đơn đặt phòng bị khiếu nại
total_payment: float = (room_price_per_night * nights_count + early_checkin_rate) * has_early_checkin + cleaning_fee

# Hiển thị hóa đơn chi tiết
print("Giá phòng mỗi đêm (VND):", room_price_per_night)
print("Số đêm lưu trú:", nights_count)
print("Trạng thái check-in sớm (1=Có, 0=Không):", has_early_checkin)
print("Phí dịch vụ dọn dẹp (VND):", cleaning_fee)
print("Tổng tiền thanh toán tính toán bởi hệ thống (VND):", total_payment)
```

# **4. Yêu cầu bài toán**

#### **Phần 1: Phân tích & Tracing mã nguồn (Báo cáo Test Case)**
Học viên tiến hành trace mã nguồn, tìm dòng code bị lỗi và hoàn thành bảng báo cáo kiểm thử dưới đây. Hàng đầu tiên đã được điền mẫu làm căn cứ thực hiện.

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: center;">STT</th>
      <th style="padding: 8px; text-align: left;">Input (Dữ liệu đầu vào)</th>
      <th style="padding: 8px; text-align: left;">Buggy Output (Đầu ra lỗi hiện tại)</th>
      <th style="padding: 8px; text-align: left;">Expected Output (Đầu ra kỳ vọng)</th>
      <th style="padding: 8px; text-align: left;">Failing Line of Code (Dòng gây lỗi)</th>
      <th style="padding: 8px; text-align: left;">Logic Note (Giải thích nguyên nhân)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; text-align: center;">1</td>
      <td style="padding: 8px;">room_price = 1000000.0<br>nights_count = 2<br>has_early_checkin = 0<br>cleaning_fee = 100000.0</td>
      <td style="padding: 8px;">100000.0</td>
      <td style="padding: 8px;">2100000.0</td>
      <td style="padding: 8px;">Dòng 9</td>
      <td style="padding: 8px;">Dấu ngoặc đơn bao phủ toàn bộ tiền phòng khiến phép nhân với <code>has_early_checkin = 0</code> triệt tiêu toàn bộ tiền phòng 2 đêm thành 0.</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">2</td>
      <td style="padding: 8px;">room_price = 1200000.0<br>nights_count = 3<br>has_early_checkin = 1<br>cleaning_fee = 150000.0</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">3</td>
      <td style="padding: 8px;">room_price = 2000000.0<br>nights_count = 1<br>has_early_checkin = 1<br>cleaning_fee = 200000.0</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn (Source Code Correction)**
*   Viết lại biểu thức tính tổng tiền `total_payment` trong Python 3.12 đảm bảo đúng nghiệp vụ:
    *   Tiền phòng gốc = `room_price_per_night * nights_count`
    *   Phí check-in sớm = `room_price_per_night * early_checkin_rate * has_early_checkin`
    *   Tổng thanh toán = Tiền phòng gốc + Phí check-in sớm + `cleaning_fee`
*   Áp dụng đúng thứ tự ưu tiên toán tử số học và sử dụng ngoặc đơn `()` hợp lý.
*   Tuân thủ nghiêm ngặt chuẩn PEP 8 và bổ sung Type Hints đầy đủ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex1`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 04_Ex1`
