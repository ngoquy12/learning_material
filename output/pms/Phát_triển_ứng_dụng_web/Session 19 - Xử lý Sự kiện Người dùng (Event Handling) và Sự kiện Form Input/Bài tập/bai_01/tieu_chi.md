### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Phát hiện Lỗi (Debug Analysis)** | 20đ | - Chỉ ra chính xác từ 4 lỗi trở lên có trong đoạn mã mẫu.<br>- Giải thích nguyên nhân rõ ràng (VD: Đọc `.value` ngoài Handler, thiếu `preventDefault`, truy cập `.value` thay vì `.checked` của checkbox, công thức tính sai). |
| **Xử lý Sự kiện Form chuẩn chuẩn JS** | 20đ | - Đăng ký sự kiện `'submit'` trên thẻ `<form>` thông qua `addEventListener`.<br>- Gọi `event.preventDefault()` ngăn làm làm mới trang thành công.<br>- Đọc và xử lý `.value` đúng thời điểm bên trong Callback function. |
| **Xử lý Logic Nghiệp vụ (GrabRide Fare)** | 30đ | - Tính đúng cước gốc $d \le 2$ km (12.000 VNĐ).<br>- Tính đúng cước $d > 2$ km ($12.000 + (d-2) \times 4.500$).<br>- Áp dụng chính xác hệ số 1.2x khi `isPeakHourInput.checked === true`. |
| **Xử lý Biên & Validation dữ liệu** | 15đ | - Gọi `.trim()` loại bỏ khoảng trắng thừa.<br>- Ép kiểu sang số chính xác bằng `parseFloat` hoặc `Number`.<br>- Bắt lỗi đầu vào rỗng, không phải số (`isNaN`), hoặc số âm/bằng 0 và hiển thị thông báo lỗi màu đỏ. |
| **Cấu trúc & Phong cách mã nguồn** | 15đ | - Mã nguồn viết sạch sẻ, đặt tên biến có ý nghĩa (`distanceVal`, `totalFare`, `resultMsg`).<br>- Định dạng giao diện kết quả đẹp mắt, hiển thị giá tiền kèm đơn vị VNĐ rõ ràng. |