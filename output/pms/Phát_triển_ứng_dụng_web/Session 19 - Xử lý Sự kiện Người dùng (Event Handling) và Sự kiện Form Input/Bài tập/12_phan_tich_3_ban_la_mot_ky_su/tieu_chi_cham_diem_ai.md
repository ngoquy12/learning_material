### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc Code & Refactoring (Phân tích & Tối ưu)** | **20đ** | - Chỉ ra chính xác lỗi Memory Leak & Code duplication của legacy code.<br>- Áp dụng triệt để **Event Delegation** (không gán listener trực tiếp lên thẻ dynamic).<br>- Tách biệt hàm logic nghiệp vụ (pure function) và hàm thao tác DOM rõ ràng. |
| **Xử lý Logic Nghiệp vụ & Live Preview** | **40đ** | - Tính toán đúng 100% tổng tiền cho tất cả kết hợp (Gói x Chu kỳ x Giảm giá 20% cho Yearly).<br>- Toggle ẩn/hiện danh sách tài khoản con chính xác khi chọn Gói (Family vs Personal/Free).<br>- Quản lý chuẩn số lượng Sub-accounts (tối thiểu 1, tối đa 5 đối với gói Family). |
| **Xử lý Sự kiện Form & Realtime Validation** | **20đ** | - Sử dụng chuẩn xác các event `input`, `change`, `blur`, `submit`.<br>- Validate chính xác định dạng Email, lỗi bỏ trống.<br>- Validate lỗi trùng lặp Email (Email con trùng nhau hoặc trùng với Email chính).<br>- Sử dụng `preventDefault()` chuẩn xác khi Submit. |
| **Xử lý Biên & Trải nghiệm Người dùng (UX)** | **20đ** | - Vô hiệu hóa (Disable) nút "Thêm" khi đạt tối đa 5 tài khoản con.<br>- Hiển thị thông báo lỗi chi tiết bên dưới từng ô input lỗi.<br>- Tự động Focus vào ô input vi phạm đầu tiên khi submit không thành công.<br>- Định dạng tiền tệ đẹp mắt (`2.400.000 VNĐ`). |