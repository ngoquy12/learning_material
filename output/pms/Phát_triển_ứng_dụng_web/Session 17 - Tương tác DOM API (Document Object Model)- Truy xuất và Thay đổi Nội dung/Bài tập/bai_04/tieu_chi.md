### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc HTML/CSS sạch sẽ, đúng semantic.<br>- Mã nguồn JS tuân thủ quy tắc đặt tên `camelCase`, comment giải thích logic nghiệp vụ rõ ràng.<br>- Sử dụng chính xác APIs của Session 17 (`querySelector`, `getElementById`, `innerHTML`, `textContent`, `classList`). |
| **Xử lý Logic đúng Nghiệp vụ Fitness** | **40đ** | - Tính đúng logic tặng 2 tháng cho gói 12 tháng (tổng 14 tháng) (10đ).<br>- So sánh ngày hiện tại với ngày hết hạn chính xác để gắn nhãn `HẾT HẠN` / `HỢP LỆ` (10đ).<br>- Cảnh báo đúng trường hợp vượt quá lượt check-in trong ngày (10đ).<br>- Render đúng đặc quyền VIP (Tủ đồ & Khăn tắm) cho gói VIP (10đ). |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Xử lý an toàn dữ liệu `trainerAssigned` bị `null`/`undefined` (5đ).<br>- Kiểm soát dữ liệu số tháng tập không hợp lệ (5đ).<br>- Xử lý trường hợp mảng hội viên rỗng, hiển thị UI thay thế phù hợp (10đ). |
| **Tối ưu Hiệu năng & Cập nhật Summary DOM** | **20đ** | - Tính toán và cập nhật chính xác các chỉ số thống kê trên Summary Bar (`#total-checkins`, `#total-warnings`, `#total-vip`) (10đ).<br>- Tối ưu hóa các thao tác DOM, tránh việc truy xuất DOM lặp đi lặp lại không cần thiết trong vòng lặp (10đ). |