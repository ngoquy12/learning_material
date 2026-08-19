### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Kiến trúc Mã nguồn** | 20đ | - Chỉ ra chính xác ít nhất 4 lỗi trong đoạn mã legacy (Reflow/Repaint, DOM Query in Loop, Coupling Logic & UI, Lack of Validation).<br>- Tách biệt hoàn toàn hàm pure logic (`calculateTripFare`) và hàm thao tác DOM (`renderTripDashboard`). |
| **Xử lý Logic đúng nghiệp vụ** | 40đ | - Tính chính xác cước 2km đầu (12.000đ) và từ km thứ 3 (4.500đ/km).<br>- Tính chính xác hệ số phụ phí 1.2x khi `isSurge = true` và làm tròn số (`Math.round`).<br>- Thống kê chính xác tổng doanh thu và đếm đúng số chuyến đường dài ($\ge 10\text{ km}$). |
| **Xử lý Biên & Ngoại lệ** | 20đ | - Xử lý an toàn các trường hợp `distance <= 0`, dữ liệu rỗng hoặc không phải dạng số.<br>- Đánh dấu giao diện trực quan cho chuyến đi không hợp lệ (class `.trip-invalid`).<br>- Định dạng số tiền hiển thị chuẩn tiếng Việt (dùng `toLocaleString('vi-VN')` hoặc hàm tự viết). |
| **Tối ưu Hiệu năng DOM API** | 20đ | - **Bắt buộc:** Cache các DOM element references bên ngoài vòng lặp.<br>- **Bắt buộc:** Gom nhóm thao tác DOM (chèn danh sách chuyến đi bằng 1 lệnh DOM update duy nhất).<br>- Sử dụng `textContent` thay cho `innerHTML` tại các vị trí hiển thị text thuần túy. Không sử dụng các Event Listeners hay API bị cấm. |