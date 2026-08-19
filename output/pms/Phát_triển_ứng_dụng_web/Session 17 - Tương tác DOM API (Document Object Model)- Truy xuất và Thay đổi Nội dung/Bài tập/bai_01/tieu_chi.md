### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Phát hiện Lỗi (Debug Report)** | **20đ** | - Phát hiện đầy đủ và chính xác ít nhất 5 lỗi trong file `script.js`.<br>- Giải thích rõ ràng bản chất kỹ thuật của lỗi (VD: `getElementById` truyền dư `#`, `getElementsByClassName` trả về `HTMLCollection` chứ không phải 1 element, thẻ `span`/`strong` không có thuộc tính `.value`...). |
| **Xử lý Logic đúng Nghiệp vụ GrabRide** | **40đ** | - Tính chuẩn cước phí gốc cho 2km đầu ($12.000$ VNĐ) và các km tiếp theo ($4.500$ VNĐ/km).<br>- Áp dụng đúng công thức nhân hệ số $1.2$ khi `isSurge = true`.<br>- Kết quả tính toán chính xác tuyệt đối với các bộ test cases (ví dụ 1.5km, 5.5km, 10km). |
| **Thao tác DOM API & Chuẩn hóa UI** | **20đ** | - Truy xuất đúng DOM element mà không gây lỗi `null` hoặc `undefined`.<br>- Sử dụng đúng `innerText`/`textContent` để cập nhật văn bản.<br>- Đặt thuộc tính `src` cho ảnh thành công.<br>- Thay đổi style/class hiển thị đúng bằng `classList.add()` mà không làm phá vỡ CSS nền. |
| **Cấu trúc Mã nguồn & Quy chuẩn Nộp bài** | **20đ** | - Mã nguồn viết sạch sẻ, có comment giải thích rõ ràng.<br>- Đặt tên biến/hàm theo chuẩn camelCase (`calculateTripFare`, `totalFareEl`).<br>- Tuân thủ đúng cấu trúc thư mục nộp bài và các ràng buộc phạm vi kỹ thuật (không dùng event/fetch). |