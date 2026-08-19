### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Cấu trúc HTML/CSS/JS tách biệt rõ ràng.<br>- Đặt tên biến, hàm theo chuẩn `camelCase`, danh xưng tiếng Anh chuẩn nghiệp vụ EdTech (`staffId`, `calculatePayroll`, `renderRow`).<br>- Code sạch, có comment giải thích các bước xử lý sự kiện. |
| **Xử lý Sự kiện Form & Validation** | **40đ** | - Sử dụng đúng sự kiện `submit` trên Form và ngăn tải lại trang bằng `event.preventDefault()` (**10đ**).<br>- Thu thập và chuẩn hóa dữ liệu bằng `.trim()`, kiểm tra định dạng Mã nhân sự `ET-xxxx` (**15đ**).<br>- Lắng nghe sự kiện `input`/`change` để tính toán và hiển thị preview đi muộn live mượt mà (**15đ**). |
| **Xử lý Logic Nghiệp vụ & DOM Dynamic** | **20đ** | - Tính đúng 100% công thức thù lao ca, thù lao OT, hệ số ngày Lễ/Tết và tiền phạt đi muộn (**10đ**).<br>- Thêm dòng mới vào DOM, cập nhật chính xác tổng chi trả `#totalBudget` thời gian thực (**10đ**). |
| **Xử lý Sự kiện Tương tác Nâng cao** | **20đ** | - Đăng ký thành công sự kiện `click` để xóa dòng và trừ tiền tổng chi trả (**10đ**).<br>- Đăng ký sự kiện `dblclick` để toggle class `.approved` đổi trạng thái dòng (**5đ**).<br>- Đăng ký sự kiện `mouseover`/`mouseleave` hiển thị tooltip chi tiết lương (**5đ**). |