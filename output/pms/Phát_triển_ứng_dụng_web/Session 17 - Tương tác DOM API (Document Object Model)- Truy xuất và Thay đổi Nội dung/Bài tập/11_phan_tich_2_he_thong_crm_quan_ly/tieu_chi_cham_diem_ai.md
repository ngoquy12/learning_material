### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phân tích & Tái cấu trúc (Clean Code)** | **20đ** | - Tách biệt rõ ràng hàm `calculateTripFare`, `formatCurrencyVND` và `renderTripTable`.<br>- Đặt tên biến/hàm theo chuẩn CamelCase, có comment giải thích rõ ràng các bước xử lý. |
| **Xử lý Logic Nghiệp vụ Cước phí** | **40đ** | - Tính đúng giá $2\text{ km}$ đầu ($12.000\text{ VNĐ}$) và các km tiếp theo ($4.500\text{ VNĐ/km}$).<br>- Nhân đúng hệ số $1.2x$ khi `isSurge === true` và làm tròn số (`Math.round`).<br>- Định dạng chuẩn tiền tệ VNĐ (ví dụ `30.600 VNĐ`). |
| **Xử lý Biên & Dữ liệu Ngoại lệ** | **20đ** | - Bắt lỗi `distanceKm <= 0` hoặc không phải số: Không sập chương trình, hiển thị cước `$0\text{ VNĐ}$` và cảnh báo giao diện.<br>- Xử lý tên hành khách rỗng/null thành `"Khách ẩn danh"`. |
| **Tối ưu Hiệu năng DOM API** | **20đ** | - Tuyệt đối **không** dùng `innerHTML` trong vòng lặp.<br>- Sử dụng `DocumentFragment` để gom thao tác DOM và chỉ append vào tbody 1 lần duy nhất.<br>- Dùng `createElement`, `textContent`, và `classList.add` đúng tiêu chuẩn bảo mật & hiệu năng. |