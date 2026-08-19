### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc Module & DOM Selection** | **20đ** | - Sử dụng đúng các phương thức DOM API (`getElementById`, `querySelector`, `querySelectorAll`).<br>- Tổ chức mã nguồn thành Module/Object rõ ràng (`SaaSSubscriptionManager`).<br>- Không vi phạm phạm vi cấm (Không dùng Event Listener, Fetch, LocalStorage). |
| **Logic Nghiệp vụ SaaS & Định giá** | **40đ** | - Tính toán chính xác giá chu kỳ Năm (giảm 20% trên 12 tháng) và render thẻ `<del>`, `.discount-tag` đúng DOM.<br>- Xử lý đúng quy tắc hạ cấp về gói `FREE` khi `paymentStatus === 'FAILED_OVER_3_DAYS'`.<br>- Render đúng số lượng tối đa 5 sub-profiles cho gói `FAMILY` và ẩn phần này khi ở gói `INDIVIDUAL`/`FREE`. |
| **Feature Gate & Biến đổi Giao diện** | **20đ** | - Duyệt qua tất cả `.feature-item` bằng `querySelectorAll`.<br>- Thêm/xóa class `.feature-active` / `.feature-disabled` chính xác theo `allowedFeatures`.<br>- Cập nhật nội dung text và icon (`✔️` / `❌`) khớp với từng quyền. |
| **Xử lý Biên & Phòng vệ Mã nguồn** | **20đ** | - Kiểm tra null/undefined trước khi thao tác với DOM element.<br>- Sử dụng `textContent` thay cho `innerHTML` đối với dữ liệu từ người dùng (tránh lỗi bảo mật XSS).<br>- Cắt mảng sub-profiles an toàn khi dữ liệu lớn hơn 5 và ghi log cảnh báo (`console.warn`). |