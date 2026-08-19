### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc thư mục và đặt tên file chính xác theo quy định.<br>- Mã nguồn rõ ràng, đặt tên biến/hàm theo chuẩn `camelCase`. Có comment giải thích logic thao tác DOM trực quan. |
| **Thao tác DOM & Thay đổi Nội dung/Style** | **20đ** | - Sử dụng đúng các phương thức DOM API: `getElementById`, `querySelector`, `querySelectorAll`, `children`, `appendChild`.<br>- Thay đổi chính xác thuộc tính `textContent`, `innerHTML`, `dataset`, `classList` (add/remove) và inline `style.width` cho thanh progress bar. |
| **Xử lý Logic Nghiệp vụ (Business Rules)** | **40đ** | - Ràng buộc nhiệt độ kho lạnh ($-18^\circ\text{C}$ đến $5^\circ\text{C}$) đạt chuẩn 100%.<br>- Tính toán chính sở tỷ lệ lấp đầy %, chuyển đổi trạng thái CSS class (`status-normal`, `status-warning`, `status-full`) chính xác.<br>- Tính chính xác tổng tải trọng và tổng phí lưu kho toàn hệ thống theo loại kệ (`DRY`: 10.000, `COLD`: 25.000 VNĐ/kg/ngày). |
| **Xử lý Biên, Cảnh báo & Ngoại lệ** | **20đ** | - Chặn chính xác các trường hợp nhập pallet vượt mức $500\text{ kg}$.<br>- Render thông báo lỗi/thành công chuyên nghiệp lên `#alert-box` trên giao diện DOM.<br>- Xử lý an toàn khi truy xuất các thuộc tính dữ liệu `dataset` hoặc parse dữ liệu kiểu số từ DOM text. |