## <center>[Vận dụng cơ bản 4] Sửa lỗi tính phụ thu check-in sớm trong tổng chi phí đặt phòng</center>

### **1. Mục tiêu**
*   **Kỹ năng truy vết mã nguồn (Code Tracing):** Thực hành đọc hiểu, chạy tay (dry-run) và truy vết mã nguồn Python 3.12 để tìm lỗi tính toán logic số học trong nghiệp vụ đặt phòng.
*   **Khắc phục lỗi logic ưu tiên & đại lượng:** Sửa đổi công thức số học tính toán phụ thu dịch vụ check-in sớm dựa trên giá phòng 1 đêm tiêu chuẩn thay vì áp dụng sai trên toàn bộ số đêm lưu trú.
*   **Tuân thủ quy chuẩn mã nguồn:** Viết mã nguồn đạt chuẩn PEP 8, khai báo Type Hints đầy đủ và tạo báo cáo kiểm thử (Test Case Report) mô tả chi tiết nguyên nhân gây lỗi.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ tính toán hóa đơn (`BookingReservation`) của ứng dụng đặt phòng khách sạn Traveloka / Agoda, hệ thống áp dụng chính sách phụ thu đối với khách hàng có nhu cầu check-in sớm trước 12:00 trưa. Quy tắc niêm yết nêu rõ: Phụ thu check-in sớm bằng 30% giá phòng tiêu chuẩn của 1 đêm.

Tuy nhiên, bộ phận Chăm sóc Khách hàng liên tục nhận được phản ánh từ những khách hàng đặt phòng lưu trú dài ngày (từ 3 đến 5 đêm trở lên) và có đăng ký dịch vụ check-in sớm. Khách hàng khiếu nại rằng số tiền phụ thu trên hóa đơn bị chênh lệch cao bất thường so với mức 30% niêm yết trên ứng dụng. Hệ thống cần được truy vết mã nguồn legacy để xác định nguyên nhân và cập nhật lại công thức tính toán.### **3. Mã nguồn hiện tại**
Dưới đây là đoạn mã nguồn Python 3.12 legacy đang chạy trên hệ thống tính toán đơn đặt phòng:

```python
def calculate_booking_total(
    room_rate: float,
    num_nights: int,
    cleaning_fee: float,
    is_early_checkin: bool,
    is_long_stay: bool,
) -> float:
    """
    Tính tổng chi phí thanh toán cho đơn đặt phòng khách sạn.
    """
    # Tính tiền phòng cơ bản theo số đêm lưu trú
    base_room_cost: float = room_rate * num_nights

    # Tính số tiền được giảm giá cho khách lưu trú dài ngày (10%)
    discount_amount: float = base_room_cost * 0.10 * is_long_stay

    # Tính phụ thu check-in sớm (30% giá phòng)
    early_checkin_surcharge: float = base_room_cost * 0.30 * is_early_checkin

    # Tính tổng tiền thanh toán cuối cùng
    total_payment: float = (
        base_room_cost - discount_amount + early_checkin_surcharge + cleaning_fee
    )

    return total_payment


# --- CHƯƠNG TRÌNH CHÍNH (ĐỂ TRUY VẾT LỖI) ---
if __name__ == "__main__":
    # Kịch bản kiểm thử: Khách đặt 5 đêm, giá 1,000,000 VNĐ/đêm, phí vệ sinh 200,000 VNĐ
    rate: float = 1000000.0
    nights: int = 5
    cleaning: float = 200000.0
    early_flag: bool = True
    long_stay_flag: bool = True

    result: float = calculate_booking_total(
        room_rate=rate,
        num_nights=nights,
        cleaning_fee=cleaning,
        is_early_checkin=early_flag,
        is_long_stay=long_stay_flag,
    )

    print(f"Tổng tiền thanh toán tính toán hiện tại: {result:,.0f} VNĐ")
```

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Truy vết Code & Phát hiện lỗi (Test Case Report Table)**
Học viên tiến hành thực thi và truy vết mã nguồn legacy, phát hiện dòng code tính toán sai nghiệp vụ và hoàn thành bảng báo cáo kiểm thử dưới đây.

[REQUIREMENT] Bảng báo cáo bắt buộc phải sử dụng mẫu HTML bên dưới. Dòng 1 (STT 1) đã được hoàn thành mẫu, học viên cần tính toán và điền đầy đủ thông tin vào dòng 2 và 3 (thay thế các dấu `...`).

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%" border="1">
  <thead>
    <tr style="background-color: #f2f2f2;">
      <th style="padding: 8px; text-align: center;">STT</th>
      <th style="padding: 8px; text-align: left;">Dữ liệu đầu vào (Input)</th>
      <th style="padding: 8px; text-align: left;">Kết quả thực tế (Buggy Output)</th>
      <th style="padding: 8px; text-align: left;">Kết quả kỳ vọng (Expected Output)</th>
      <th style="padding: 8px; text-align: left;">Dòng code gây lỗi (Failing Line)</th>
      <th style="padding: 8px; text-align: left;">Giải thích nguyên nhân (Logic Note)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; text-align: center;">1</td>
      <td style="padding: 8px;">room_rate = 1,000,000<br>num_nights = 5<br>cleaning_fee = 200,000<br>is_early_checkin = True<br>is_long_stay = True</td>
      <td style="padding: 8px;">6,200,000 VNĐ</td>
      <td style="padding: 8px;">5,000,000 VNĐ</td>
      <td style="padding: 8px;">Dòng 17: <code>early_checkin_surcharge = base_room_cost * 0.30 * is_early_checkin</code></td>
      <td style="padding: 8px;">Hàm sử dụng <code>base_room_cost</code> (tổng tiền 5 đêm) để nhân 30% thay vì lấy <code>room_rate</code> (giá 1 đêm tiêu chuẩn), dẫn đến tính thừa phụ thu.</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">2</td>
      <td style="padding: 8px;">room_rate = 2,000,000<br>num_nights = 3<br>cleaning_fee = 300,000<br>is_early_checkin = True<br>is_long_stay = False</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
    <tr>
      <td style="padding: 8px; text-align: center;">3</td>
      <td style="padding: 8px;">room_rate = 1,500,000<br>num_nights = 4<br>cleaning_fee = 150,000<br>is_early_checkin = True<br>is_long_stay = True</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
      <td style="padding: 8px;">...</td>
    </tr>
  </tbody>
</table>

#### **Phần 2: Sửa lỗi mã nguồn (Source Code Correction)**
Học viên sửa lại mã nguồn của hàm `calculate_booking_total` trong đoạn mã legacy để đảm bảo:
1. Phụ thu check-in sớm được tính đúng 30% dựa trên đơn giá 1 đêm `room_rate`.
2. Giữ nguyên cấu trúc mã nguồn, không sử dụng các từ khóa hoặc cấu trúc thuộc phạm vi chưa học (Tuyệt đối không dùng `if/else`, không dùng toán tử logic `and/or/not`, không dùng vòng lặp hay danh sách).
3. Đảm bảo toàn bộ mã nguồn tuân thủ Type Hints và định dạng chuẩn PEP 8.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex4`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 04_Ex4`