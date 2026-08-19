### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20 điểm** | - Đặt tên biến, hàm theo chuẩn `camelCase`, thể hiện rõ ngữ nghĩa.<br>- Tổ chức code sạch sẻ, tách biệt giữa phần xử lý Logic (State) và Render UI.<br>- Có comment giải thích chi tiết logic nghiệp vụ phức tạp (Công thức tính phí ship, giờ cao điểm). |
| **Xử lý Sự kiện & Form (DOM Events)** | **20 điểm** | - Lắng nghe đúng và đủ các sự kiện `input`, `change`, `click`, `submit` bằng `addEventListener`.<br>- Sử dụng `e.preventDefault()` chuẩn xác khi submit Form.<br>- Truy xuất và cập nhật các phần tử DOM mượt mà, đúng kỹ thuật. |
| **Tính đúng đắn Logic Nghiệp vụ** | **40 điểm** | - Tính đúng phí giao hàng theo khoảng cách làm tròn ($15k$ cho $2km$ đầu, $+5k/km$ tiếp theo).<br>- Cộng đúng phụ phí $10k$ khi chọn khung giờ cao điểm.<br>- Giảm đúng $15k$ phí ship cho đơn từ $100k$ (không âm phí ship).<br>- Áp dụng chính xác voucher `SHOPEEFOOD50` (tối đa $30k$) và `FREESHIP`.<br>- Khóa nút/chặn đặt hàng chuẩn xác khi cửa hàng đóng cửa (`isOpen = false`). |
| **Xử lý Biên & Ngoại lệ (Edge Cases)** | **10 điểm** | - Giới hạn số lượng món theo tồn kho (`stock`), không cho chọn quá stock hoặc âm số lượng.<br>- Báo lỗi rõ ràng khi khoảng cách nhập vào $\le 0$ hoặc giỏ hàng $0$ món.<br>- Xử lý đúng khi nhập mã voucher sai/không tồn tại. |
| **Giao diện & Tương tác UX** | **10 điểm** | - Hiển thị giá tiền dạng định dạng chuẩn VND (VD: `45,000 VNĐ`).<br>- Vô hiệu hóa (disabled) trực quan các nút tăng/giảm số lượng hoặc nút Submit khi không đủ điều kiện. |
| **TỔNG ĐIỂM** | **100 điểm** | **Đạt yêu cầu khi tổng điểm $\ge 70$ điểm.** |