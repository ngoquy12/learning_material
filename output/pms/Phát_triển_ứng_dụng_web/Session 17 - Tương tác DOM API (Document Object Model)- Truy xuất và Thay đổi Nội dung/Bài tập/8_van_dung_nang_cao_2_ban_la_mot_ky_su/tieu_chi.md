### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Tổ chức mã nguồn sạch sẽ, tách hàm rõ ràng theo đúng yêu cầu.<br>- Đặt tên biến/hàm chuẩn camelCase, theo ngữ cảnh GrabRide (`calculateTripFare`, `renderDriverCard`).<br>- Thụt lề chuẩn 2 spaces, có comment giải thích cho từng đoạn xử lý DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - **Cước cơ bản (15đ)**: Tính đúng $2\text{ km}$ đầu 12k, các km sau 4.5k/km.<br>- **Phụ phí Surge (15đ)**: Đúng hệ số $1.2\text{x}$ (mưa hoặc cao điểm) và $1.4\text{x}$ (cả hai).<br>- **Mã giảm giá (10đ)**: Tính đúng giảm $20\%$ max 15k cho `GRABDIWUI` và giảm 10k cho `CHAOXINCHAO`. |
| **Thao tác DOM API & Xử lý Biên** | **20đ** | - Sử dụng chính xác `getElementById`, `querySelector`, `classList`, `setAttribute`.<br>- Định dạng số tiền chính xác (thêm chấm phân cách hàng nghìn và đuôi `"VNĐ"`).<br>- Kiểm soát biên: Khoảng cách âm hoặc $= 0$, mã giảm giá không hợp lệ không làm crash script. |
| **Tối ưu UI & Ẩn/Hiện trạng thái** | **20đ** | - Hiển thị đúng Badge trạng thái tài xế theo từng màu tương ứng.<br>- Thao tác class `d-none` thành công để bật/tắt `#surge-alert`.<br>- Thay đổi màu sắc đánh giá sao (`#driver-rating`) linh hoạt theo điều kiện điểm số. |