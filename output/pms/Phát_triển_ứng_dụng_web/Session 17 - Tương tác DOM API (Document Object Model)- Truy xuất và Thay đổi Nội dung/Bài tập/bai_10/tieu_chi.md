### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Tái cấu trúc Mã nguồn** | **20đ** | - Tách biệt hoàn toàn Business Logic (hàm thuần khiết) và DOM Rendering Logic.<br>- Mã nguồn sạch, chuẩn ES6+, đặt tên biến/hàm thể hiện đúng ngữ nghĩa nghiệp vụ ShopeeFood. |
| **Xử lý Đúng Logic Nghiệp vụ** | **40đ** | - Tính chính xác subtotal các món.<br>- Tính đúng phí giao hàng cơ bản (20k), cộng phụ phí cao điểm 10k (khung 11h-13h, 18h-20h).<br>- Áp dụng chính xác giảm 15k phí ship cho đơn > 100k (không âm phí ship).<br>- Tính chính xác tổng thanh toán cuối cùng. |
| **Tối ưu hóa Hiệu năng DOM** | **20đ** | - Thực hiện DOM Caching hiệu quả, không gọi `querySelector`/`getElementById` dư thừa.<br>- Sử dụng `DocumentFragment` để gộp việc chèn phần tử vào DOM (tránh Layout Thrashing).<br>- Sử dụng `textContent` và `classList` đúng chuẩn thay cho `innerHTML` và direct `style`. |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Phát hiện chính xác trạng thái quán đóng cửa hoặc hết hàng (`stockQuantity <= 0` hoặc `isAvailable === false`).<br>- Khóa nút thanh toán đúng chuẩn (`disabled`, `aria-disabled`), hiển thị banner lỗi đúng định dạng CSS.<br>- Xử lý an toàn dữ liệu đầu vào rỗng hoặc không hợp lệ. |