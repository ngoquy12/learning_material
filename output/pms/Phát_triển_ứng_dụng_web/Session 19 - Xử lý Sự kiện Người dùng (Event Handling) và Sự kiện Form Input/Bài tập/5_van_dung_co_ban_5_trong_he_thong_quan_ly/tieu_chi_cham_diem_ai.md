### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc HTML/CSS/JS tách biệt rõ ràng.<br>- Đặt tên biến, hàm theo chuẩn `camelCase` (ví dụ: `calculateTripFare`, `distanceInput`).<br>- Sử dụng `const`/`let` đúng phạm vi, không dùng `var`.<br>- Code được comment đầy đủ, thụt lề chuẩn. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Sử dụng đúng `event.preventDefault()` khi submit form (10đ).<br>- Tính toán chính xác Base Fare theo khoảng cách lũy tiến (10đ).<br>- Áp dụng chính xác hệ số phụ phí cao điểm / mưa (10đ).<br>- Xử lý chuẩn xác các trường hợp mã giảm giá `GRABNEW`, `TIETKIEM` và đưa tiền về tối thiểu 0 VNĐ (10đ). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Bắt chính xác lỗi khi khoảng cách trống, bằng 0 hoặc số âm (10đ).<br>- Hiển thị thông báo lỗi rõ ràng trên UI và ẩn khối kết quả khi gặp lỗi (10đ). |
| **Tối ưu hiệu năng & Thao tác DOM** | **20đ** | - Truy xuất phần tử DOM chính xác thông qua ID/Class.<br>- Render kết quả hiển thị mượt mà, định dạng tiền tệ Việt Nam (`VNĐ`) trực quan.<br>- Xử lý chuỗi mã giảm giá linh hoạt (loại bỏ khoảng trắng `trim()`, chuyển thành chữ hoa `toUpperCase()`). |