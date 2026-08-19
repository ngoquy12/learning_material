### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Đăng ký & Xử lý Sự kiện DOM** | **25đ** | - Đăng ký đúng sự kiện `submit` cho Form, dùng `event.preventDefault()` chính xác.<br>- Lắng nghe đúng sự kiện `input`/`change` trên các thẻ input để tính tiền realtime.<br>- Không sử dụng thuộc tính `onclick`/`onsubmit` trực tiếp trong thẻ HTML. |
| **2. Validation Dữ liệu & Xử lý Biên** | **20đ** | - Kiểm tra đầy đủ điều kiện: Họ tên rỗng/quá ngắn, Số điện thoại không đủ 10 chữ số hoặc không bắt đầu bằng số 0, Tuổi không hợp lệ.<br>- Làm sạch chuỗi đầu vào bằng `.trim()`. Hiển thị lỗi rõ ràng trên UI. |
| **3. Logic Nghiệp vụ FinTech & Hạn mức Slot** | **25đ** | - Tính đúng tiền khám khi có BHYT (giảm 80%) và không có BHYT.<br>- Nhận diện đúng diện ưu tiên (Tuổi $\ge 70$ hoặc Mang thai) để miễn phí dịch vụ và cấp mã `PRIO-`.<br>- Chặn chính xác khi Bác sĩ đã đầy chỗ (`bookedSlot >= maxSlot`). |
| **4. Cập nhật Giao diện (DOM Manipulation)** | **20đ** | - Cập nhật thông tin tạm tính realtime mượt mà.<br>- Render hóa đơn thanh toán chi tiết (Số STT, Họ tên, Bác sĩ, Số tiền) đẹp mắt vào `#receiptContainer`.<br>- Cập nhật hiển thị số slot còn lại của Bác sĩ sau khi đặt thành công. |
| **5. Cấu trúc Mã nguồn & Reset Form** | **10đ** | - Mã nguồn tổ chức sạch sẻ, chia hàm rõ ràng (`render`, `validate`, `calculate`).<br>- Reset Form đúng cách về trạng thái ban đầu sau khi đăng ký thành công. |