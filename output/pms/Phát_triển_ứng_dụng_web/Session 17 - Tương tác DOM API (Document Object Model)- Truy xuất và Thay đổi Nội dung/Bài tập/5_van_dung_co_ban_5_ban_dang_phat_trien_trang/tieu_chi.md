### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Đặt tên biến/hàm đúng chuẩn camelCase, có ý nghĩa nghiệp vụ CRM (`planType`, `overdueDays`, `accountItems`).<br>- Thụt lề chuẩn (2 hoặc 4 spaces), mã nguồn sạch sẻ, có comment giải thích từng bước xử lý DOM.<br>- Không thừa code rác hoặc console.log dư thừa. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Truy xuất chính xác thông tin từ `data-* attributes` (10đ).<br>- Xử lý đúng logic hạ cấp gói xuống "Free" khi trễ hạn > 3 ngày, hiển thị thông báo warning chính xác (15đ).<br>- Render chính xác HTML tính năng (`#feature-list`) dựa trên loại gói sau cùng (15đ). |
| **Xử lý Biên & Ngoại lệ** | **20đ** | - Đánh dấu đúng các phần tử tài khoản dư thừa bằng `classList.add('account-error')` theo từng loại gói (`family`: >5, `individual`/`free`: >1) (15đ).<br>- Cập nhật chính xác tổng số tài khoản lên `#account-count` (5đ). |
| **Tối ưu hiệu năng & DOM Manipulation** | **20đ** | - Chọn đúng phương thức truy xuất DOM (`getElementById` cho ID đơn lẻ, `querySelectorAll` cho danh sách phần tử) (10đ).<br>- Thao tác với class thông qua `classList` thay vì nối chuỗi `className` thủ công; hiển thị/ẩn element bằng thuộc tính `hidden` hoặc `classList` hợp lý (10đ). |