### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm chuẩn `camelCase`, mang ý nghĩa nghiệp vụ (5đ).<br>- Tổ chức mã nguồn sạch sẽ, tách biệt logic tính toán và logic thao tác DOM (10đ).<br>- Có comment giải thích các bước xử lý dữ liệu và DOM API (5đ). |
| **Thao tác DOM API & Dataset** | **30đ** | - Truy xuất chính xác phần tử bằng `getElementById`, `querySelector` (10đ).<br>- Trích xuất và ép kiểu đúng dữ liệu từ `dataset` ( distance, boolean flags) (10đ).<br>- Cập nhật chuẩn xác `textContent`, `innerHTML`, thao tác class qua `classList` (`add`, `remove`, `toggle`) (10đ). |
| **Xử lý Logic nghiệp vụ (Business Logic)** | **30đ** | - Tính Cước phí nền chuẩn xác theo quy tắc 2km đầu và các km tiếp theo (10đ).<br>- Tính đúng hệ số nhân phụ phí khi xảy ra đồng thời hoặc đơn lẻ (trời mưa / giờ cao điểm) (10đ).<br>- Tính chính xác mức giảm giá của các mã `GRAB20` (có giới hạn max 20k) và `TIETKIEM` (10đ). |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Kiểm soát khoảng cách không hợp lệ ($0$, số âm, `NaN`): hiển thị trạng thái lỗi trên DOM (10đ).<br>- Xử lý trường hợp không có mã giảm giá hoặc mã giảm giá không tồn tại trong hệ thống (5đ).<br>- Đảm bảo cước thanh toán không bao giờ bị âm ($Total \ge 0$) (5đ). |