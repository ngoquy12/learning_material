### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | 20đ | - Đặt tên biến, tên hàm rõ nghĩa theo chuẩn camelCase.<br>- Sử dụng đúng phương thức truy xuất DOM (`getElementById`, `querySelector`).<br>- Thụt lề chuẩn xác, mã nguồn sạch sẽ, có comment giải thích logic. |
| **Xử lý Logic đúng nghiệp vụ** | 40đ | - Tính chính xác phụ thu VIP (15.000 VNĐ) và ưu đãi HSSV ngày thường (20%).<br>- Cập nhật chuẩn xác nội dung text và HTML tương ứng vào DOM (`textContent`, `innerHTML`).<br>- Định dạng chuẩn chuỗi hiển thị giá tiền (có dấu chấm phân cách hàng nghìn và đơn vị `VNĐ`). |
| **Xử lý Biên & Ngoại lệ** | 20đ | - Kiểm tra điều kiện giới hạn tuổi (dưới 18 tuổi đăng ký dịch vụ `isRestricted18Plus = true`).<br>- Reset đầy đủ trạng thái các phần tử DOM về giá trị mặc định `"--"` khi vi phạm điều kiện.<br>- Cập nhật chính xác danh sách lớp CSS (`status-success`, `status-error`). |
| **Tối ưu hiệu năng & Phạm vi cho phép** | 20đ | - Tuyệt đối không dùng Event Listener hay Form Submit (đúng yêu cầu Session 17).<br>- Tránh truy xuất lặp đi lặp lại cùng một phần tử DOM nhiều lần (nên lưu vào biến tạm).<br>- Không làm thừa/dư thuộc tính trên cây DOM. |