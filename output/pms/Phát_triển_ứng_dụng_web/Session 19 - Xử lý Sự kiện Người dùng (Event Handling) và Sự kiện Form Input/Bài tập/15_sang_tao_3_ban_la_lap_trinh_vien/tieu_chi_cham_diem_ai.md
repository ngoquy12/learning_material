### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Áp dụng đúng mô hình Class/Module tách biệt logic DOM và Business.<br>- Đặt tên biến/hàm theo chuẩn `camelCase`, mã nguồn sạch sẽ, có comment giải thích rõ ràng. |
| **Xử lý Sự kiện & Real-time Calculation** | **40đ** | - Sử dụng chính xác các sự kiện `input`, `change`, `submit`.<br>- Tính toán chính xác 100% các công thức phụ phí (check-in sớm, trẻ em, người lớn thứ 3, dịch vụ đi kèm).<br>- Giao diện cập nhật tiền tức thì ngay khi đổi input. |
| **Form Validation & Ngoại lệ** | **20đ** | - Sử dụng `event.preventDefault()` chính xác.<br>- Validate đầy đủ logic ngày tháng (check-out > check-in), định dạng SĐT, Email, Họ tên.<br>- Hiển thị/ẩn các thông báo lỗi chi tiết ngay bên dưới các ô input (không dùng `alert`). |
| **Trải nghiệm UI & Hiển thị Hóa đơn** | **20đ** | - Render hóa đơn (`ServiceInvoice`) đẹp mắt, rõ ràng từng khoản mục tiền sau khi submit thành công.<br>- Reset form và dữ liệu hóa đơn đúng chuẩn khi đặt lại. |