### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phát hiện & Giải thích Lỗi (Debug Report)** | 20đ | Giải thích đúng nguyên nhân gây lỗi của cả 5 vị trí: Thứ tự load Script, HTMLCollection vs Element, `.value` trên Div, ép kiểu Attribute dữ liệu, ghi đè Class Attribute. |
| **Sửa lỗi Nhúng Script & Truy xuất DOM** | 20đ | Sử dụng đúng thuộc tính `defer` trên thẻ `<script>`. Truy xuất chính xác Element bằng `querySelector` hoặc truy cập đúng chỉ số `[0]` của `HTMLCollection`. |
| **Tính toán Nghiệp vụ BHYT & Chuyển đổi Dữ liệu** | 30đ | Ép kiểu dữ liệu `dataset` từ chuỗi sang số/boolean đúng chuẩn. Tính chính xác 80% giảm trừ BHYT (500,000 VNĐ -> 100,000 VNĐ). Cập nhật chuỗi kết quả có đơn vị "VNĐ". |
| **Thao tác Class & Cập nhật DOM Content** | 20đ | Dùng `classList.add("priority-badge")` giữ nguyên class `.badge`. Cập nhật đúng textContent cho nhãn ưu tiên và số thứ tự (`Q-008`). |
| **Cấu trúc Mã nguồn & Phong cách (Clean Code)** | 10đ | Code sạch vẽ đúng thụt lề, tên biến rõ nghĩa theo chuẩn camelCase, comment đầy đủ các bước xử lý. |