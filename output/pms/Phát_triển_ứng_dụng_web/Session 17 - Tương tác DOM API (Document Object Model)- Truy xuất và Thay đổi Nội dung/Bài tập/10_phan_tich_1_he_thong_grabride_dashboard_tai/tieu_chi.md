### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Nhận diện Code Smell** | 15đ | - Trích xuất đúng 4 điểm yếu chính của đoạn mã Legacy (Hiệu năng DOM query, Reflow do `innerHTML`, tính toán sai nghiệp vụ km, thiếu validation). |
| **Cấu trúc & Phong cách mã nguồn** | 15đ | - Áp dụng mô hình thiết kế rõ ràng (Object Literal / Class / Module Pattern).<br>- Đặt tên hàm/biến chuẩn Clean Code (camelCase), comment giải thích logic đầy đủ. |
| **Xử lý Logic Nghiệp vụ (GrabRide Rules)** | 35đ | - Tính chính xác cước 2km đầu ($12.000\text{đ}$) và km thứ 3 trở đi ($4.500\text{đ/km}$).<br>- Áp dụng chính xác phụ phí $1.2\text{x}$ khi mưa/giờ cao điểm.<br>- Tính chính xác giảm giá cho mã `"GRAB20"` và `"GRAB50"` đúng trần max discount.<br>- Trả về kết quả tính toán chính xác với dữ liệu mẫu. |
| **Tối ưu DOM API & An toàn** | 20đ | - Thực hiện Cache DOM Node thành công (không gọi lại `querySelector`/`getElementById` trong hàm render).<br>- Tuyệt đối sử dụng `textContent` thay cho `innerHTML` khi hiển thị chuỗi văn bản.<br>- Sử dụng thành thạo `classList.add/remove/toggle` và `dataset`. |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | 15đ | - Kiểm soát tốt dữ liệu đầu vào bị âm, `NaN`, hoặc `null/undefined`.<br>- Hiển thị trạng thái lỗi trực quan lên UI khi dữ liệu không hợp lệ.<br>- Không làm sập chương trình khi thiếu tham số mã giảm giá. |