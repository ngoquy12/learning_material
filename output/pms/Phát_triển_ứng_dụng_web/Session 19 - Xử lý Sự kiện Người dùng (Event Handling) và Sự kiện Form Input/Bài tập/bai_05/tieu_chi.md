### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách Tái cấu trúc Mã nguồn** | **20đ** | - Loại bỏ hoàn toàn `onclick` và gán handler trực tiếp.<br>- Đăng ký sự kiện đúng chuẩn bằng `addEventListener`.<br>- Tách biệt hàm rõ ràng (`validate`, `calculate`, `render`).<br>- Đặt tên biến/hàm theo chuẩn camelCase, comment giải thích lý do refactor. |
| **Xử lý Sự kiện Form & Tương tác DOM** | **40đ** | - Bắt đúng sự kiện `'submit'` trên thẻ `<form>` và gọi `event.preventDefault()` thành công.<br>- Đọc giá trị `.value` động bên trong handler sự kiện, loại bỏ khoảng trắng bằng `.trim()`.<br>- Triển khai thành công tính năng preview tính phí thời gian thực bằng sự kiện `'input'` hoặc `'change'`. |
| **Tính đúng đắn của Logic Nghiệp vụ ShopeeFood** | **20đ** | - Chặn đặt đơn chính xác khi trạng thái cửa hàng là `CLOSED`.<br>- Tính chuẩn phí giao hàng gốc theo khoảng cách (15k cho 3km đầu, 5k/km tiếp theo).<br>- Tính chính xác phụ phí cao điểm 10k và giảm giá ship 15k cho đơn $\ge 100\text{k}$. |
| **Xử lý Biên & Validation Ngoại lệ** | **20đ** | - Kiểm tra định dạng số điện thoại (10 chữ số, bắt đầu bằng 0).<br>- Xử lý chuẩn các trường hợp nhập khoảng trắng, số âm, khoảng cách bằng 0.<br>- Hiển thị thông báo lỗi thân thiện trên giao diện UI (không dùng `alert()`), tự động xóa lỗi khi submit thành công. |