### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm theo chuẩn `camelCase`, đúng ngữ nghĩa nghiệp vụ HRM.<br>- Code định dạng sạch sẽ, thụt lề chuẩn xác, có comment giải thích các khối xử lý DOM.<br>- Sử dụng ES6 (Template Literals, Arrow Functions, Destructuring). |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính chính xác lương giờ cơ bản, tiền phạt đi muộn (chỉ phạt khi `lateMinutes > 15`).<br>- Tính chuẩn hệ số OT 150% và ngày lễ 300%.<br>- Tính đúng tổng lương thực nhận `netSalary` theo từng nhân viên.<br>- Tính chính xác các chỉ số tổng quan: Tổng quỹ lương, Tổng tiền phạt, Nhân viên lương cao nhất. |
| **Thao tác DOM & Dynamic Styling** | **20đ** | - Truy xuất chính xác các phần tử bằng `getElementById`, `querySelector`.<br>- Thay đổi nội dung thẻ bằng `textContent` và `innerHTML` hợp lý.<br>- Dynamic Styling đúng điều kiện: Thêm class `row-warning`, `row-highlight`, thuộc tính `data-salary-level` và render đúng badge trạng thái. |
| **Xử lý Biên & Ràng buộc Kỹ thuật** | **20đ** | - Định dạng tiền tệ chính xác (`x.xxx.xxx VNĐ`).<br>- Kiểm soát trường hợp mảng dữ liệu rỗng (không bị lỗi runtime JS).<br>- Tuân thủ 100% ràng buộc: Không dùng `addEventListener`, `fetch`, `localStorage`, `form submit`. |