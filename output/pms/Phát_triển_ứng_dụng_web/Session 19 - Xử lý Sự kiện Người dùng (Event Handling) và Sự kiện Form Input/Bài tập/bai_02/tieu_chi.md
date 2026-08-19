### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đăng ký sự kiện chuẩn xác bằng `addEventListener('submit', ...)` (không dùng `onclick` hay gán inline).<br>- Tên biến rõ ràng, tuân thủ chuẩn `camelCase`.<br>- Mã nguồn trình bày sạch sẽ, thụt lề chuẩn xác, có comment giải thích logic rõ ràng. |
| **Xử lý Logic nghiệp vụ & I/O** | **40đ** | - Gọi `event.preventDefault()` để chống reload trang (10đ).<br>- Tính chính xác giá theo Size và số lượng Topping (10đ).<br>- Tính chính xác giảm giá thành viên 10% khi mã là `GOLD` (10đ).<br>- Vượt qua toàn bộ 5 Test Cases trong bảng Kiểm thử I/O (10đ). |
| **Xử lý Biên & Ngoại lệ (Validation)** | **20đ** | - Xử lý làm sạch chuỗi đầu vào bằng `.trim()` trước khi kiểm tra (5đ).<br>- Bắt đúng các trường hợp tên rỗng, số lượng ly $\le 0$, số lượng topping $< 0$ (10đ).<br>- Đưa thông báo lỗi và xóa kết quả cũ đúng yêu cầu (5đ). |
| **Tối ưu giao diện & Trải nghiệm** | **20đ** | - Cập nhật chính xác nội dung hiển thị trên DOM (`#error-msg` và `#result-msg`).<br>- Định dạng chuỗi tiền tệ đầu ra đẹp mắt, rõ ràng (có dấu chấm phân cách hàng nghìn và đơn vị VNĐ). |