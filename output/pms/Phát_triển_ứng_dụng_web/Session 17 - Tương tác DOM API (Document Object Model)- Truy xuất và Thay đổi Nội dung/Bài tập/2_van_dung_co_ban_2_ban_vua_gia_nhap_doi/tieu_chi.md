### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phát hiện & Fix lỗi Selector** | 20đ | - Sửa đúng `getElementById("pnr-code")` (bỏ `#`) (10đ).<br>- Sử dụng đúng `getElementsByClassName("passenger-name")[0]` hoặc đổi sang `querySelector` (10đ). |
| **Phát hiện & Fix lỗi Nội dung DOM** | 20đ | - Sửa thuộc tính `.value` thành `textContent` / `innerText` cho thẻ `span#ticket-class` (10đ).<br>- Sửa lỗi gọi hàm `innerHTML(...)` thành gán giá trị `innerHTML = ...` hoặc `textContent = ...` (10đ). |
| **Xử lý Logic Nghiệp vụ & Class** | 40đ | - Tính toán đúng phí hành lý theo hạng vé `Business` (0 VNĐ) và `Eco` (40đ).<br>- Thao tác class đúng kỹ thuật với `classList.remove()` và `classList.add()` (hoặc `className`) thay vì gán vào `.style`.<br>- Cập nhật đúng nội dung văn bản cho `#status-badge`. |
| **Thao tác Attribute & Trạng thái Nút** | 20đ | - Kiểm tra điều kiện phí quá cước để gỡ bỏ thuộc tính `disabled` bằng `removeAttribute("disabled")` hoặc `.disabled = false` khi hợp lệ.<br>- Mã nguồn sạch đẹp, có comment giải thích rõ ràng các điểm lỗi đã sửa. |
| **Tổng điểm** | **100đ** | **Đạt từ 80đ trở lên là ĐẠT (PASS)** |