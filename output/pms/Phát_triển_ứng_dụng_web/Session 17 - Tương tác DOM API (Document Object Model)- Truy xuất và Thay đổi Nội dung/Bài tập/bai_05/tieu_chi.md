### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn `camelCase` có nghĩa (`distance`, `isSurge`, `totalFare`).<br>- Định dạng code thụt lề chuẩn 2/4 spaces.<br>- Thêm comment giải thích rõ ràng từng bước đọc DOM, tính toán và ghi DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính đúng giá sàn 12.000 VNĐ cho $\le 2$ km (10đ).<br>- Tính đúng giá lũy tiến 4.500 VNĐ/km cho $> 2$ km (15đ).<br>- Nhàn chính xác hệ số 1.2x khi `isSurge` là `true` và làm tròn số tiền (15đ). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Bắt lỗi khi khoảng cách $\le 0$ hoặc `NaN` (10đ).<br>- Đổi màu chữ thông báo lỗi thành màu đỏ (`red` / `#dc3545`) và thông báo hợp lệ thành màu xanh (`green` / `#28a745`) (10đ). |
| **Thao tác DOM & Kiểm thử I/O** | **20đ** | - Đọc dữ liệu chính xác từ DOM elements/attributes (`data-distance`, `data-surge`) (10đ).<br>- Cập nhật nội dung hiển thị chính xác vào `#fare-amount` và `#trip-status` với định dạng tiền tệ Việt Nam (`VNĐ`) (10đ).<br>- Tuyệt đối không vi phạm danh sách Forbidden Scope (Event Listeners, Fetch, LocalStorage). |