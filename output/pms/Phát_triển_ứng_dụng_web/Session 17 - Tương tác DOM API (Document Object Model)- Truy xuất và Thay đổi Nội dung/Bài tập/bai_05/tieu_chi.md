### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Tối ưu hóa DOM (DOM Refactoring)** | **20đ** | - Áp dụng thành công caching cho các phần tử DOM, không để lặp lại việc truy xuất phần tử DOM.<br>- Sử dụng `DocumentFragment` hoặc gom chuỗi HTML để thao tác `innerHTML` đúng 1 lần.<br>- Sử dụng `textContent` hợp lý thay cho `innerHTML` cho các đoạn text tĩnh/tiền tệ. |
| **Xử lý Logic đúng Nghiệp vụ ShopeeFood** | **40đ** | - Tính đúng Subtotal (bỏ qua sản phẩm `stock === 0`).<br>- Áp dụng đúng quy tắc giảm 15k phí ship cho đơn $\ge 100\text{k}$ (phí ship không âm).<br>- Tính chuẩn phụ phí giờ cao điểm $10\text{k}$ (11h-13h, 18h-20h).<br>- Tính chính xác tổng thanh toán cuối cùng. |
| **Xử lý Trạng thái & Trường hợp Biên** | **20đ** | - Xử lý chuẩn xác khi quán đóng cửa (`isStoreOpen = false`): Hiển thị banner lỗi, ẩn khu vực checkout.<br>- Phân biệt rõ món còn hàng/hết hàng trên giao diện bằng class CSS và nhãn tương ứng.<br>- Xử lý an toàn trường hợp giỏ hàng rỗng (`cartItems = []`). |
| **Tái cấu trúc Mã nguồn & Clean Code** | **20đ** | - Tách biệt logic nghiệp vụ tính toán (Pure Functions) và logic thao tác DOM (Impure Functions).<br>- Đặt tên hàm, biến chuẩn CamelCase, tự giải thích (self-documenting).<br>- Định dạng tiền tệ chính xác (`xxx.xxxđ`). Mã nguồn không chứa Event Listeners hay API cấm. |