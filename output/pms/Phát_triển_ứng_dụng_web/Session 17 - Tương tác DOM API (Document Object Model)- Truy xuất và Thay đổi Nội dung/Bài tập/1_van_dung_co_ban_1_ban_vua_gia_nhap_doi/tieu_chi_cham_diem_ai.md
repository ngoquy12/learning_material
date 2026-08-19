### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Debug Code** | 20đ | - Tìm đủ và giải thích đúng nguyên nhân gây ra 5 lỗi trong code ban đầu.<br>- Mã nguồn sạch đẹp, tuân thủ chuẩn đặt tên biến CamelCase. |
| **Truy xuất DOM API chuẩn xác** | 25đ | - Sử dụng đúng `document.getElementById()` hoặc `document.querySelector()` đúng cú pháp selector (`#` cho ID, `.` cho Class).<br>- Phân biệt rõ đối tượng đơn lẻ và HTMLCollection/NodeList. |
| **Thao tác Thay đổi Nội dung DOM** | 25đ | - Dùng đúng `textContent` cho văn bản thuần (Text node).<br>- Dùng đúng `innerHTML` khi cần chèn chuỗi HTML có chứa các thẻ element (`<span>`, `<ul>`, `<li>`).<br>- Không dùng thuộc tính `.value` cho các thẻ không phải Form Input (`<h2>`, `<p>`). |
| **Xử lý Logic Nghiệp vụ SaaS** | 20đ | - Cập nhật chính xác các thông tin: Tên gói, Trạng thái quá hạn, Giới hạn thiết bị, Giới hạn tài khoản con.<br>- Render danh sách tính năng dạng danh sách HTML đầy đủ. |
| **Xử lý Biên & Mã an toàn** | 10đ | - Đảm bảo script thực thi không bắn lỗi Uncaught TypeError trên Console trình duyệt.<br>- Kiểm tra trường hợp dữ liệu danh sách `features` bị rỗng. |