## <center>[Vận dụng nâng cao 3] Tính toán Tổng Phí Đặt Phòng và Kiểm Soát Điều Kiện Đặt Cọc Homestay</center>

### **1. Mục tiêu**
Vận dụng linh hoạt các toán tử số học, toán tử so sánh và phép toán biểu thức logic trong Python 3.12 để giải quyết bài toán tính toán chi phí đặt phòng homestay, kiểm tra điều kiện hoàn cọc và xác thực tính hợp lệ của giao dịch mà không sử dụng các cấu trúc điều khiển nâng cao (câu lệnh rẽ nhánh `if/else`, vòng lặp, danh sách). Học viên rèn luyện tư duy phân tích I/O, tự thiết kế luồng xử lý và viết mã chuẩn PEP 8 kèm Type Hints.

### **2. Bối cảnh & Vấn đề**
Trong nền tảng ứng dụng đặt phòng khách sạn & homestay (như Agoda hay Traveloka), phân hệ quản lý thanh toán và đặt phòng (BookingReservation Subsystem) cần một module tự động tính toán tổng số tiền phòng, phụ phí người phát sinh, phụ phí check-in sớm, số tiền cọc bắt buộc (50%) và xác định điều kiện hoàn cọc 100% khi khách hàng yêu cầu hủy đơn.### **3. Quy tắc nghiệp vụ**
1. **Chi phí phòng cơ bản**: Giá phòng tiêu chuẩn 1 đêm là `price_per_night` (VNĐ). Tổng chi phí tiền phòng = `price_per_night * num_nights`.
2. **Phụ thu Check-in sớm**: Nếu khách check-in sớm trước 12h trưa (`is_early_checkin = True`), hệ thống tính phụ thu thêm 30% giá phòng của 1 đêm.
3. **Phụ thu số lượng khách**: 
   - Phòng tiêu chuẩn áp dụng cho tối đa 2 khách. 
   - Từ khách thứ 3 trở đi, tính phụ thu `200,000` VNĐ/người/đêm. 
   - Số khách vượt quá được xác định bằng công thức số học không bị âm khi số khách <= 2: `extra_guests = (num_guests - 2) * (num_guests > 2)`.
   - Tổng phụ thu người phát sinh = `extra_guests * 200000 * num_nights`.
4. **Tổng thanh toán & Tiền cọc**:
   - Tổng chi phí booking = `Tổng tiền phòng + Phụ thu check-in sớm + Phụ thu người phát sinh`.
   - Tiền cọc tối thiểu để hoàn tất giữ phòng = 50% Tổng chi phí booking.
5. **Ràng buộc tính hợp lệ của đơn hàng (Valid Booking)**:
   - Số đêm lưu trú `num_nights` phải hợp lệ: lớn hơn 0 và nhỏ hơn hoặc bằng 30 đêm (`1 <= num_nights <= 30`).
   - Số lượng khách `num_guests` phải hợp lệ: lớn hơn 0 và nhỏ hơn hoặc bằng 6 người (`1 <= num_guests <= 6`).
   - Đơn đặt phòng hợp lệ khi cả 2 điều kiện về số đêm và số khách đồng thời thỏa mãn.
6. **Chính sách hoàn cọc 100% (Full Refund Eligibility)**:
   - Khách hủy phòng trước thời điểm nhận phòng từ 3 ngày trở lên (`days_before_cancel >= 3`).
   - Đơn đặt phòng ban đầu phải là đơn hợp lệ (`is_valid_booking == True`).

### **4. Yêu cầu bài toán**
Học viên thực hiện bài tập gồm 2 phần độc lập:

**Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp**
- Phân tích và định nghĩa rõ ràng các thông số đầu vào (Input) và đầu ra (Output) kèm theo kiểu dữ liệu (Data types) phù hợp theo chuẩn Type Hints trong Python.
- Tự đề xuất mô hình giải pháp logic để giải quyết các quy tắc nghiệp vụ trên bằng toán tử số học và toán tử so sánh (tuyệt đối không sử dụng câu lệnh rẽ nhánh `if/else`, từ khóa `and`/`or`/`not` hay vòng lặp).
- Thiết kế các bước thực hiện chi tiết dưới dạng sơ đồ luồng (Mermaid Flowchart) tuân thủ đúng 5 dạng hình chuẩn:
  + Oval: Bắt đầu / Kết thúc quy trình.
  + Hình bình hành (Parallelogram): Nhập dữ liệu / Xuất dữ liệu.
  + Hình chữ nhật (Rectangle): Xử lý tính toán / Gán biến.
  + Hình thoi (Diamond): Kiểm tra điều kiện so sánh.
  + Mũi tên (Flowline): Mối liên kết luồng thực thi.

**Phần 2: Triển khai Mã nguồn & Xử lý Ràng buộc**
- Viết chương trình Python 3.12 thực hiện chính xác logic đã thiết kế ở Phần 1.
- Khai báo biến có gắn Type Hints đầy đủ, tuân thủ nghiêm ngặt quy chuẩn PEP 8 (tên biến dùng kiểu `snake_case` bằng tiếng Anh, ghi chú mã nguồn bằng tiếng Việt có dấu).
- In kết quả tính toán chi tiết ra màn hình CLI (Tổng tiền phòng, Phụ thu check-in sớm, Phụ thu người phát sinh, Tổng thanh toán, Tiền cọc yêu cầu, Trạng thái đơn hợp lệ, Trạng thái đủ điều kiện hoàn cọc 100%).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 04_Ex9`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 04_Ex9`