### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Truy xuất DOM API** | **20 điểm** | - Sử dụng đúng các phương thức `document.getElementById`, `querySelector`, `querySelectorAll`.<br>- Cập nhật chính xác `dataset`, `setAttribute`, `classList` (thêm/xóa lớp `d-none`, `badge-surge`).<br>- Thụt lề chuẩn, comment giải thích code rõ ràng. |
| **Logic Nghiệp vụ & Công thức Cước phí** | **40 điểm** | - Tính đúng cước khoảng cách lũy tiến ($2\text{ km}$ đầu $12.000\text{đ}$, từ $\text{km}$ 3 tính $4.500\text{đ/km}$).<br>- Tính chính xác hệ số phụ phí khi mưa/giờ cao điểm ($1.2\text{x}$ hoặc $1.3\text{x}$).<br>- Tính chính xác giảm giá theo mã `GRABNEW` (tối đa $15.000\text{đ}$) hoặc `TIETKIEM` ($\ge 30.000\text{đ}$).<br>- Định dạng chuẩn tiền tệ VNĐ trên giao diện. |
| **Render Giao diện & Đổ Dữ liệu Động** | **20 điểm** | - Đổ đầy đủ thông tin chuyến đi vào các thẻ HTML tương ứng.<br>- Sử dụng `innerHTML` để render dynamic HTML cho thông tin tài xế đúng thiết kế.<br>- Cập nhật đúng các thuộc tính `data-*` trên container node. |
| **Xử lý Ngoại lệ & Kiểm soát Phạm vi** | **20 điểm** | - Hiển thị đúng thông báo lỗi trên DOM khi `distanceKm` không hợp lệ ($< 0.1\text{ km}$ hoặc sai kiểu dữ liệu).<br>- Không vi phạm vùng cấm: Không sử dụng `addEventListener`, không `fetch`, không `localStorage`. |