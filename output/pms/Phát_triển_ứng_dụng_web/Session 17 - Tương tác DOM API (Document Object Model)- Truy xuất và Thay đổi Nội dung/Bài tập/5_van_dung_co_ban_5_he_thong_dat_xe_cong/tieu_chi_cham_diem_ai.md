### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Sử dụng đúng các phương thức DOM API (`getElementById`, `querySelector`).<br>- Đặt tên biến rõ ràng, đúng chuẩn `camelCase`.<br>- Code sạch sẻ, có comment giải thích các bước truy xuất và cập nhật DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Đọc chính xác thuộc tính `data-distance` và `data-weather` từ DOM.<br>- Tính chính xác cước gốc cho $d \le 2$ km (12.000 VNĐ) và $d > 2$ km.<br>- Áp dụng chuẩn hệ số phụ phí thời tiết (1.2x cho `rain`, 1.0x cho `clear`).<br>- Tính đúng tổng cước cuối cùng và làm tròn hợp lý. |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Kiểm tra và xử lý thỏa đáng trường hợp $d \le 0$ hoặc `NaN`.<br>- Cập nhật giao diện cảnh báo lỗi đúng yêu cầu (class `text-danger`, thông báo lỗi). |
| **Thao tác DOM & Định dạng Output** | **20đ** | - Đổi class giao diện linh hoạt (`classList.add`/`classList.remove` hoặc `className`).<br>- Định dạng số tiền chính xác chuẩn Việt Nam (có hậu tố `VNĐ`).<br>- Không dùng các kỹ thuật cấm (Event Listener, Form Submit, LocalStorage). |