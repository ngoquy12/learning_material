### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Sử dụng đúng cú pháp DOM API (`getElementById`, `querySelector`).<br>- Đặt tên biến/hàm theo chuẩn `camelCase` (ví dụ: `calculateGrabFare`, `tripCard`).<br>- Định dạng code rõ ràng, có comment giải thích các bước thực hiện. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính chuẩn cước phí 2 km đầu (12.000 VNĐ) và các km tiếp theo (4.500 VNĐ/km) (20đ).<br>- Áp dụng chính xác hệ số 1.2x khi `data-is-surge="true"` (10đ).<br>- Làm tròn số tiền chính xác và định dạng chuỗi VNĐ đúng quy định (10đ). |
| **Xử lý Biên & Ngoại lệ (I/O Validation)** | **20đ** | - Bắt lỗi thành công trường hợp `distance <= 0`, `NaN`, hoặc chuỗi không hợp lệ (10đ).<br>- Cập nhật đúng thông điệp lỗi và thay đổi style/class tương ứng trên DOM khi gặp dữ liệu lỗi (10đ). |
| **Tác động & Cập nhật DOM** | **20đ** | - Đọc dữ liệu đúng từ `dataset` của DOM (5đ).<br>- Cập nhật chính xác `textContent` / `innerHTML` cho thẻ `#total-fare` và `#fare-detail` (10đ).<br>- Thay đổi `style.color` hoặc `classList` đúng mô tả cho thẻ `#status-badge` (5đ). |