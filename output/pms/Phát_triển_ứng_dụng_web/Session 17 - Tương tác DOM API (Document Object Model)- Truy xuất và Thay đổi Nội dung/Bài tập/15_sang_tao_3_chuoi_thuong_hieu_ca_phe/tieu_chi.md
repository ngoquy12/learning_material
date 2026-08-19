### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **Cấu trúc & Phong cách mã nguồn** | **20đ** | - Mã nguồn được tổ chức sạch sẽ theo dạng Module Object (`POSReceiptEngine`).<br>- Đặt tên biến, hàm theo chuẩn CamelCase (rõ nghĩa, đúng tiếng Anh chuyên ngành).<br>- Có comment giải thích logic rõ ràng cho từng phương thức DOM. |
| **Xử lý Logic đúng nghiệp vụ** | **40đ** | - Tính đúng phụ thu Size món: M (+6.000đ), L (+10.000đ), S (+0đ).<br>- Tính đúng phụ thu Topping (8.000đ / phần).<br>- Tính đúng 10% giảm giá cho Gold Member.<br>- Định dạng chuẩn tiền tệ VNĐ (có phân cách hàng nghìn). |
| **Thao tác DOM API & Rendering** | **20đ** | - Truy xuất chính xác các phần tử bằng `getElementById` hoặc `querySelector`.<br>- Sử dụng linh hoạt `textContent`, `innerHTML` để chèn nội dung.<br>- Thao tác class thành thạo với `classList.add()` / `classList.remove()`.<br>- Cập nhật thuộc tính thành công qua `setAttribute()`. |
| **Xử lý Biên & Tối ưu hiệu năng** | **20đ** | - Kiểm soát trường hợp mảng `drinks` hoặc `toppings` rỗng (hiển thị thông báo phù hợp thay vì để trắng hoặc lỗi JS).<br>- Kiểm tra sự tồn tại của phần tử DOM trước khi thao tác để tránh lỗi Null Reference.<br>- Thuật toán duyệt mảng và tạo chuỗi DOM tối ưu, không gọi DOM API lặp đi lặp lại trong vòng lặp lớn. |