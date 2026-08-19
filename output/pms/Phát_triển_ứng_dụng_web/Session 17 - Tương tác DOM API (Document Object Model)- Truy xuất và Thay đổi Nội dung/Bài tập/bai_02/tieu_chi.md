### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn `camelCase`, rõ nghĩa.<br>- Thụt lề đồng nhất (2 hoặc 4 spaces).<br>- Có comment giải thích các đoạn xử lý DOM quan trọng. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Xử lý hạ cấp gói cước chính xác khi `paymentOverdueDays > 3` (15đ).<br>- Cập nhật đúng thông tin gói cước, số thiết bị & danh sách tính năng tương ứng với `PERSONAL`, `FAMILY`, `FREE` (15đ).<br>- Hiển thị/Ẩn cảnh báo tài khoản con (`#warning-badge`) chính xác theo điều kiện số lượng (10đ). |
| **Thao tác DOM API & Chuẩn I/O** | **20đ** | - Sử dụng đúng `document.getElementById` hoặc `document.querySelector` (5đ).<br>- Cập nhật nội dung bằng `textContent` và danh sách bằng `innerHTML` hợp lý (10đ).<br>- Thao tác class (`classList.add`, `classList.remove`) và ẩn/hiện element (`style.display`) đúng quy định (5đ). |
| **Kiểm thử Biên & Ngoại lệ** | **20đ** | - Xử lý đúng khi `activeSubAccounts` chạm mốc biên (= 5 thì ẩn warning, > 5 mới hiện).<br>- Xử lý đúng khi `paymentOverdueDays` chạm mốc 3 (chưa phạt) và 4 (bắt đầu phạt hạ cấp).<br>- Không để phát sinh lỗi JavaScript Runtime khi gọi hàm với dữ liệu hợp lệ. |