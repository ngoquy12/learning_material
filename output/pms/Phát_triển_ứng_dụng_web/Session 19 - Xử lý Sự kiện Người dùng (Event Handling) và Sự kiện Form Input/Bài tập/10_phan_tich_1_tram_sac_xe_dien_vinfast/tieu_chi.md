### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết đánh giá |
| :--- | :--- | :--- |
| **Phân tích Legacy & Cấu trúc Mã nguồn** | **20đ** | - Phân tích chính xác các điểm yếu của code cũ (Memory leak, tight coupling).<br>- Tổ chức mã nguồn sạch đẹp, đặt tên biến/hàm rõ nghĩa theo quy chuẩn Clean Code.<br>- Tách biệt rõ ràng Logic nghiệp vụ, Event Handlers và DOM Rendering. |
| **Kỹ thuật Event Handling & Delegation** | **30đ** | - Sử dụng **Event Delegation** chính xác trên Container chung, không gán event listener trong hàm loop/render.<br>- Xử lý sự kiện Form submit chuẩn mực với `preventDefault()`.<br>- Lắng nghe sự kiện `input`/`blur` để phản hồi validation real-time chuyên nghiệp. |
| **Xử lý Logic Nghiệp vụ Trạm sạc** | **30đ** | - Tính chính xác phí điện sạc theo loại cổng (Regular: 3.850đ, Super Fast: 4.500đ).<br>- Áp dụng đúng quy tắc ngắt sạc an toàn (Pin = 100% hoặc Nhiệt độ > 70°C).<br>- Tính chính xác phí phạt quá giờ (Miễn phí 30p đầu khi pin 100%, từ phút 31 phạt 1.000đ/phút; Không phạt nếu ngắt do quá nhiệt). |
| **Xử lý Biên, Ngoại lệ & Tối ưu Giao diện** | **20đ** | - Validate chặt chẽ dữ liệu đầu vào (kWh, nhiệt độ, thời gian đỗ xe).<br>- Giao diện cập nhật mượt mà, không bị giật lag, hiển thị hóa đơn chi tiết, rõ ràng.<br>- Không vi phạm các phạm vi cấm (Không Async/Fetch/LocalStorage). |