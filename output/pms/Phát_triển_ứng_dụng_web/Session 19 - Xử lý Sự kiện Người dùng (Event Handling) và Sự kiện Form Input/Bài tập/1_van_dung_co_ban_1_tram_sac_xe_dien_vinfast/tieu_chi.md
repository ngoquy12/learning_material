### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Debug Report** | **20đ** | - Tổ chức thư mục chuẩn theo yêu cầu.<br>- Viết file `debug_report.md` liệt kê chính xác nguyên nhân và giải pháp sửa ít nhất 4 lỗi trong bài gốc. |
| **Sự kiện DOM & Prevent Default** | **25đ** | - Sử dụng `addEventListener('submit', ...)` chuẩn xác.<br>- Gọi `e.preventDefault()` để chặn hành vi reload trang.<br>- Đăng ký đúng sự kiện `input` và `change` trên các phần tử DOM. |
| **Xử lý Logic Nghiệp vụ** | **25đ** | - Ép kiểu số chuẩn xác cho `kwh` và `minutes`.<br>- Tính đúng phí đỗ quá giờ (Miễn phí 30p đầu, không bị âm tiền).<br>- Tính đúng tiền điện theo cổng sạc `STANDARD` (3.850đ) và `FAST` (4.500đ). |
| **Xử lý Biên & Validation** | **15đ** | - Catch lỗi đầu vào: số kWh $\le 0$, số phút $< 0$ hoặc để trống.<br>- Hiển thị/Ẩn thông báo lỗi trên UI phù hợp với trạng thái người dùng nhập. |
| **Trải nghiệm người dùng (UX) & Format** | **15đ** | - Tính toán real-time mượt mà khi gõ phím/thay đổi option.<br>- Định dạng số tiền có dấu phân cách hàng nghìn (ví dụ: `150,000 VNĐ` hoặc `150.000 VNĐ`). |