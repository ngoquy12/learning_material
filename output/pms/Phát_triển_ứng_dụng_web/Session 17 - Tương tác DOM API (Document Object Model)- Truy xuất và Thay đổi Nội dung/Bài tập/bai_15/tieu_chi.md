### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Architecture Module** | 20đ | - Thiết kế Module/Class rõ ràng, encapsulated tốt.<br>- Sử dụng DOM Caching (truy xuất DOM 1 lần trong `init`, lưu biến references).<br>- Không vi phạm scope cấm (Không dùng Event Listeners, Fetch API, LocalStorage). |
| **Xử lý Logic Nghiệp vụ & Giá vé** | 40đ | - Tính chính xác giá ghế VIP (+15k), Ghế Đôi (x2 + 30k).<br>- Tính chuẩn 20% giảm giá cho HS/SV trong ngày thường.<br>- Định dạng tiền tệ VND chuẩn xác (ví dụ: `150.000 VNĐ`). |
| **Thao tác DOM & Kiểm soát T18** | 20đ | - Render đúng cấu trúc sơ đồ ghế kèm theo `dataset` (`data-seat-id`, `data-seat-type`, `data-price`).<br>- Xử lý kiểm soát tuổi T18 đúng yêu cầu (thêm class `restricted-mode`, cập nhật banner cảnh báo, đặt thuộc tính `aria-disabled`). |
| **Xử lý Biên & Mã nguồn Clean Code** | 20đ | - Đọc/ghi thuộc tính DOM an toàn, xử lý danh sách ghế trống hoặc ID không tồn tại.<br>- Đặt tên biến/hàm chuẩn CamelCase, mã nguồn viết bằng tiếng Anh/Việt sạch đẹp, comment giải thích logic đầy đủ. |