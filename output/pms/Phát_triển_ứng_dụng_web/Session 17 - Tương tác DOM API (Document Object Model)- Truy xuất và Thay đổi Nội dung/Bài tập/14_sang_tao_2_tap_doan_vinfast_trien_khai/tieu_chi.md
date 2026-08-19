### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Cấu trúc Architecture & Phong cách Code** | **20 điểm** | - Đóng gói đúng mô hình Mini-Module/Class sạch sẽ.<br>- Đặt tên biến, hàm theo chuẩn `camelCase`, hằng số `UPPER_SNAKE_CASE`.<br>- Comment mã nguồn rõ ràng, cấu trúc HTML/CSS mạch lạc. |
| **2. Xử lý Logic Nghiệp vụ FinTech** | **40 điểm** | - Tính chính xác đơn giá sạc theo loại `STANDARD` (3.850đ) và `SUPER_FAST` (4.500đ).<br>- Tính chính xác phí phạt đỗ xe (Miễn phí 30 phút đầu, từ phút 31 tính 1.000đ/phút).<br>- Kiểm soát chính xác logic ngắt sạc khi `Pin = 100%` hoặc `Nhiệt độ > 70°C`.<br>- Format đúng định dạng tiền tệ Việt Nam (`VNĐ`). |
| **3. Thao tác DOM API (Phạm vi Session 17)** | **20 điểm** | - Truy xuất phần tử DOM chính xác bằng `querySelector`/`getElementById`.<br>- Sử dụng thành thạo `createElement`, `appendChild`, `textContent`, `classList`.<br>- Tuân thủ quy định: Không dùng Event Listener, Form submit, Fetch API hay LocalStorage. |
| **4. Xử lý Biên & Ngoại lệ DOM** | **20 điểm** | - Kiểm tra và xử lý khi `portId` không tồn tại trên DOM.<br>- Tránh nhân bản (duplicate) phần tử Hóa đơn nếu hóa đơn đó đã tồn tại.<br>- Xử lý an toàn dữ liệu đầu vào bị thiếu hoặc bị sai kiểu dữ liệu (vd: `temperature` bị âm, `currentKwh` không phải là số). |