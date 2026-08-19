### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Đã sửa xong lỗi Reload Trang & Sự kiện Form** | 20đ | - Sử dụng chính xác `event.preventDefault()` trong callback sự kiện `submit`.<br>- Lắng nghe đúng sự kiện `submit` trên thẻ `<form>`. |
| **2. Đã sửa lỗi Phản hồi Thời gian thực (Real-time Input)** | 20đ | - Đổi sự kiện trên `portTemp` từ `change` sang `input`.<br>- Cảnh báo ẩn/hiện tức thì theo giá trị nhiệt độ nhập vào.<br>- Chặn không cho phép tính toán hóa đơn nếu nhiệt độ > 70°C. |
| **3. Xử lý Đúng Logic Nghiệp vụ & Ép kiểu** | 40đ | - Ép kiểu số (`parseFloat`/`Number`) chính xác cho các giá trị từ input.<br>- Tính đúng tiền điện theo từng loại cổng sạc (3.850đ hoặc 4.500đ).<br>- Tính đúng phí đỗ xe theo quy tắc miễn phí 30 phút đầu.<br>- Hiển thị đúng tổng tiền hóa đơn (`ChargingInvoice`). |
| **4. Xử lý Biên & Validation dữ liệu đầu vào** | 10đ | - Kiểm tra số kWh phải là số dương lớn hơn 0.<br>- Xử lý trường hợp người dùng nhập chữ hoặc để trống thông tin. |
| **5. Cấu trúc mã nguồn & Comment Debug** | 10đ | - Mã nguồn trình bày sạch sẻ, thụt lề chuẩn.<br>- Đặt tên biến rõ ràng, có ghi chú (comment) giải thích những điểm bị lỗi và cách khắc phục. |