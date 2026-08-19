### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | 20đ | - Thư mục và file đặt đúng quy chuẩn bài nộp.<br>- Mã nguồn JS tuân thủ mô hình Module (`CoffeePosEngine`), khai báo biến rõ ràng (`const`/`let`).<br>- Thụt lề chuẩn, comment giải thích đầy đủ các bước thao tác DOM API. |
| **Xử lý Logic đúng nghiệp vụ** | 40đ | - Tính chính xác giá từng món (Base price + Size Fee + Toppings Fee).<br>- Tính đúng Subtotal, Chiết khấu hội viên (0%, 5%, 10%) và Thuế VAT (8%).<br>- Cập nhật đầy đủ và chính xác tất cả thông tin Header, Table Rows và Summary lên DOM.<br>- Định dạng chuẩn tiền tệ VNĐ cho tất cả hiển thị số tiền. |
| **Xử lý Biên & Ngoại lệ** | 20đ | - Xử lý mảng order rỗng/null: Ẩn receipt card, hiển thị error banner đúng yêu cầu.<br>- Xử lý đúng món có giá âm hoặc size không hợp lệ (gán giá 0 và thêm suffix danh xưng lỗi). |
| **Tối ưu DOM & Thuộc tính động** | 20đ | - Sử dụng hiệu quả các API DOM (`querySelector`, `getElementById`, `classList`, `setAttribute`, `style`).<br>- Gán đúng class badge hội viên (`badge-gold`, `badge-silver`, ...).<br>- Thêm thuộc tính `data-vip-order="true"` và đổi style nền `#final-total-box` khi tổng hóa đơn > 200.000 VNĐ. |