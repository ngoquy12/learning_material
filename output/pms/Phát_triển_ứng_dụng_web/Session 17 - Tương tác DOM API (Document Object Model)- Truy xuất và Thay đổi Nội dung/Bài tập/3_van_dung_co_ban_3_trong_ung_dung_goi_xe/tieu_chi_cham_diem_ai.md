### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Phát hiện & Báo cáo lỗi (Debug Log)** | **20đ** | Liệt kê đầy đủ và chính xác ít nhất 4 lỗi có trong đoạn mã mẫu. Giải thích rõ nguyên nhân dẫn tới lỗi runtime hoặc lỗi hiển thị. |
| **Sửa lỗi DOM Selector & Thao tác thuộc tính** | **20đ** | - Sửa đúng `getElementById` không dùng dấu `#`.<br>- Dùng đúng `innerText` / `textContent` thay cho `.value` trên thẻ `<span>`.<br>- Gọi đúng phương thức `classList.add(...)`. |
| **Xử lý Ép kiểu & Logic Nghiệp vụ** | **30đ** | - Chuyển đổi đúng `data-distance` thành kiểu `Number` (`parseFloat`).<br>- Chuyển đổi/So sánh đúng `data-is-surge` (so sánh chuỗi `"true"` hoặc ép kiểu `Boolean`).<br>- Tính đúng công thức cước cơ bản: $12.000 + (5.5 - 2) \times 4.500 = 27.750$ VNĐ.<br>- Tính đúng phụ phí 1.2x: $27.750 \times 1.2 = 33.300$ VNĐ. |
| **Xử lý Biên & Chống lỗi Runtime (Null Check)** | **15đ** | - Kiểm tra null/undefined đối với phần tử DOM trước khi gán dữ liệu.<br>- Xử lý trường hợp `data-distance` bị rỗng hoặc không phải là số hợp lệ. |
| **Phong cách mã nguồn & Định dạng** | **15đ** | - Đặt tên biến rõ ràng, tuân thủ `camelCase`.<br>- Code trình bày sạch sẽ, có comment giải thích các bước fix lỗi.<br>- Định dạng tiền cước hiển thị đẹp mắt (VD: `33,300 VNĐ` hoặc `33.300 VNĐ`). |