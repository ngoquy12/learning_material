### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Tổ chức mã nguồn sạch sẻ, chia nhỏ hàm xử lý rõ ràng (`calculateTripFare`, `updateSurgeUI`, `updateDriverUI`, `renderTripSummary`).<br>- Đặt tên biến và hàm chuẩn camelCase, có comment giải thích rõ các bước truy xuất DOM. |
| **Xử lý Logic nghiệp vụ (Business Logic)** | **40đ** | - Tính đúng cước cơ bản (2km đầu 12k, km sau 4.5k/km) (15đ).<br>- Tính chính xác phụ phí Surge x1.2 khi `isSurge = true` (10đ).<br>- Áp dụng đúng công thức giảm giá cho mã `GRABNEW` (-20%) và `SAIGONXANH` (-10k) (15đ). |
| **Thao tác DOM API & Định dạng** | **20đ** | - Sử dụng thành thạo `getElementById` / `querySelector` để đọc và ghi nội dung (8đ).<br>- Sử dụng đúng `textContent` / `innerHTML` cho thẻ text và badge (6đ).<br>- Cập nhật linh hoạt `classList` (`surge-active`, `vip-driver`) và thuộc tính CSS `style` (6đ). |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Xử lý trường hợp quãng đường $d \le 0$ hoặc không phải số hợp lệ (5đ).<br>- Xử lý trường hợp số tiền giảm giá lớn hơn tổng tiền sau surge (không để tổng tiền bị âm) (5đ).<br>- Xử lý mã giảm giá không tồn tại/rỗng (5đ).<br>- Định dạng tiền tệ VNĐ chính xác với dấu phân cách hàng nghìn (5đ). |