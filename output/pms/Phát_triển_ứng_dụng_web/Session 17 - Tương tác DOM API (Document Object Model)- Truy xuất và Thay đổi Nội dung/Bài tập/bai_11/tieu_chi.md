### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Tái cấu trúc Mã nguồn (Refactoring Quality)** | **20đ** | - Tách biệt hoàn toàn logic đọc DOM, tính toán và ghi DOM.<br>- Loại bỏ triệt để đoạn mã lặp lại (Spaghetti/Duplicate DOM queries).<br>- Tổ chức hàm mô đun hóa (Clean Code, DRY principle). |
| **Xử lý Logic Nghiệp vụ Tính Cước** | **40đ** | - Tính đúng cước cơ bản (2km đầu 12k, từ km thứ 3 là 4.5k/km) (15đ).<br>- Tính đúng hệ số Surge 1.2x khi `data-surge="true"` (10đ).<br>- Tính đúng KM (`GRABNEW` giảm 20% max 20k, `VIPRIDE` giảm 10% max 50k) (10đ).<br>- Làm tròn tiền và không âm (5đ). |
| **Thao tác DOM API & An toàn** | **20đ** | - Sử dụng `dataset` đúng chuẩn để đọc dữ liệu thuộc tính `data-*` (5đ).<br>- Sử dụng `textContent` để cập nhật văn bản thay cho `innerHTML` (5đ).<br>- Thao tác với `classList` (`add`, `remove`, `toggle`) và thuộc tính `setAttribute`/`title` chính xác (10đ). |
| **Xử lý Biên & Dữ liệu Ngoại lệ (Edge Cases)** | **20đ** | - Khoảng cách âm ($\le 0$) hoặc không phải là số (`NaN`): Đánh dấu card lỗi `.card-error`, hiển thị `-- VNĐ` (10đ).<br>- Thuộc tính `data-surge` bị thiếu hoặc mang giá trị bất thường (5đ).<br>- Mã giảm giá không hợp lệ/đã hết hạn (5đ). |