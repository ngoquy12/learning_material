### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Tái cấu trúc Kiến trúc** | **20đ** | - File `README.md` chỉ ra chính xác 4 lỗi code smell của mã nguồn cũ.<br>- Mã nguồn mới được chia nhỏ thành các hàm có trách nhiệm riêng biệt (Pure Function tính cước, Function tạo Node, Function render, Function update summary). |
| **Thao tác DOM API & Tối ưu hiệu năng** | **20đ** | - Cache thành công các element DOM cố định.<br>- Sử dụng `DocumentFragment` để batching DOM node.<br>- Không gọi `document.getElementById/querySelector` bên trong vòng lặp.<br>- Sử dụng `textContent` thay cho `innerHTML` để chống XSS. |
| **Logic Nghiệp vụ & Chính xác dữ liệu** | **40đ** | - Tính đúng cước phí 2km đầu ($12.000$) và từ km thứ 3 ($4.500$/km).<br>- Tính đúng hệ số phụ phí `isSurge` ($1.2x$).<br>- Định dạng chuẩn tiền tệ VNĐ.<br>- Tính chính xác tổng doanh thu và tổng số chuyến VIP trên Dashboard. |
| **Xử lý Biên & Ngoại lệ** | **10đ** | - Xử lý an toàn khi mảng chuyến đi rỗng.<br>- Xử lý đúng dữ liệu `distance` không hợp lệ ($\le 0$, `null`, `undefined`, chuỗi không phải số).<br>- Xử lý dữ liệu chuỗi nguy hiểm (HTML injection) không bị thực thi script. |
| **Phong cách Mã nguồn & Quy chuẩn UI** | **10đ** | - Đặt tên biến/hàm theo chuẩn CamelCase rõ nghĩa (`calculateTripFare`, `createTripCardNode`).<br>- CSS phân định rõ các class (`trip-card`, `trip-card--vip`, `trip-card--standard`).<br>- Thụt lề chuẩn, comment giải thích logic rõ ràng. |