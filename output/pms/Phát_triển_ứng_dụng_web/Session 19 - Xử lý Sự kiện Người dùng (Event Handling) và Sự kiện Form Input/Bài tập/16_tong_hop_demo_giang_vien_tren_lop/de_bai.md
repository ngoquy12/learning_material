# Bài tập tổng hợp trên lớp: Hệ Thống Kiểm Duyệt Form Đặt Hàng Nhanh E-Commerce


## 1. Mục tiêu bài tập
- Lắng nghe và xử lý sự kiện `submit` trên Form, áp dụng phương thức ngăn chặn hành vi mặc định của trình duyệt khi gửi dữ liệu.
- Truy xuất, kiểm tra và xác thực dữ liệu đầu vào từ các phần tử Form Input (`text`, `select`) thông qua việc đăng ký sự kiện bằng `addEventListener`.
- Thực hiện cập nhật giao diện người dùng (DOM Manipulation) linh hoạt: hiển thị thông báo lỗi chi tiết khi dữ liệu không hợp lệ hoặc xuất khối xác nhận đơn hàng thành công khi dữ liệu hợp lệ.


## 2. Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)
- **Bối cảnh doanh nghiệp**: Trong các nền tảng thương mại điện tử (E-Commerce), tính năng "Đặt hàng nhanh" (Quick Checkout) đóng vai trò quan trọng giúp tối ưu tỷ lệ chuyển đổi. Hệ thống yêu cầu xây dựng một mô-đun kiểm duyệt Form đặt hàng ngay tại phía trình duyệt (Client-side validation). Mô-đun này phải lắng nghe các sự kiện tương tác của người dùng, thực hiện kiểm tra định dạng dữ liệu đầu vào, áp dụng mã ưu đãi phù hợp và hiển thị kết quả đặt hàng ngay trên giao diện mà không làm tải lại trang.

- **Dữ liệu đầu vào (Input)**:
  - Sự kiện người dùng tương tác với Form qua các ô nhập liệu:
    - Họ và tên (`fullName`): Chuỗi ký tự.
    - Số điện thoại (`phoneNumber`): Chuỗi ký tự số.
    - Mã giảm giá (`promoCode`): Chuỗi ký tự (Ví dụ: `RIKKAECOM10`, `RIKKAECOM20` hoặc mã bất kỳ).
    - Phương thức thanh toán (`paymentMethod`): Giá trị lựa chọn từ thẻ `<select>` (Giá trị: `COD`, `BANKING`).
  - Sự kiện nhấn nút "Xác nhận đặt hàng" (`submit`).

- **Kết quả đầu ra (Output)**:
  - **Trường hợp dữ liệu không hợp lệ**:
    - Ngăn chặn việc gửi form.
    - Hiển thị thông báo lỗi tương ứng ngay dưới từng ô nhập liệu vi phạm quy tắc.
    - Không hiển thị khối thông tin đơn hàng thành công.
  - **Trường hợp dữ liệu hợp lệ**:
    - Xóa toàn bộ các thông báo lỗi hiện có.
    - Hiển thị một khối thẻ (Card) chứa thông tin tóm tắt đơn hàng thành công gồm: Họ tên, Số điện thoại, Mức ưu đãi được áp dụng (`10%`, `20%` hoặc `0%`), và Phương thức thanh toán đã chọn.
    - Xóa sạch dữ liệu nhập trên form (Reset form) về trạng thái ban đầu.


### Bảng ví dụ minh họa Input/Output:

| Trường hợp (Case) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Ghi chú nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **Trường hợp 1 (Chuẩn)** | `fullName`: "Nguyen Van A"<br>`phoneNumber`: "0987654321"<br>`promoCode`: "RIKKAECOM10"<br>`paymentMethod`: "COD" | - Xóa các thông báo lỗi.<br>- Hiển thị khối đơn hàng:<br>  + Khách hàng: Nguyen Van A<br>  + Số điện thoại: 0987654321<br>  + Mức giảm giá: Giảm 10%<br>  + Thanh toán: COD<br>- Form được reset trống. | Luồng thành công bình thường. Mã `RIKKAECOM10` áp dụng mức giảm 10%. |
| **Trường hợp 2 (Chuẩn)** | `fullName`: "Tran Thi B"<br>`phoneNumber`: "0912345678"<br>`promoCode`: "RIKKAECOM20"<br>`paymentMethod`: "BANKING" | - Xóa các thông báo lỗi.<br>- Hiển thị khối đơn hàng:<br>  + Khách hàng: Tran Thi B<br>  + Số điện thoại: 0912345678<br>  + Mức giảm giá: Giảm 20%<br>  + Thanh toán: BANKING<br>- Form được reset trống. | Luồng thành công với mã giảm 20%. |
| **Trường hợp 3 (Ngoại lệ)** | `fullName`: "An"<br>`phoneNumber`: "12345"<br>`promoCode`: "ABC"<br>`paymentMethod`: "" | - Lỗi Họ tên: "Họ tên phải từ 3 ký tự trở lên".<br>- Lỗi SĐT: "Số điện thoại phải bắt đầu bằng 0 và có đúng 10 chữ số".<br>- Lỗi Thanh toán: "Vui lòng chọn phương thức thanh toán".<br>- Không hiển thị khối đơn hàng. | Xử lý lỗi nhập liệu không đủ độ dài, sai định dạng số điện thoại và bỏ trống thẻ select. |


## 3. Các bước thực hiện & Quy định kỹ thuật
- **Tài nguyên & Môi trường**: Thực thi trên môi trường Browser Standard (HTML5 / Modern JavaScript).
- **Yêu cầu kỹ thuật**:
  - **Sự kiện & Form**: 
    - Bắt buộc dùng `addEventListener` để lắng nghe sự kiện `submit` của Form và sự kiện `input` hoặc `change` nếu muốn kiểm tra dữ liệu theo thời gian thực.
    - Phải sử dụng phương thức hủy hành vi gửi form mặc định để phục vụ xử lý trên Client.
  - **Quy tắc xác thực (Validation Rules)**:
    - `fullName`: Không được để trống, độ dài sau khi loại bỏ khoảng trắng thừa (trim) phải >= 3 ký tự.
    - `phoneNumber`: Không được để trống, phải bắt đầu bằng chữ số `0`, chỉ chứa chữ số và có chính xác 10 ký tự.
    - `promoCode`: Nếu nhập `RIKKAECOM10` -> Giảm 10%; nếu nhập `RIKKAECOM20` -> Giảm 20%; các trường hợp còn lại (hoặc để trống) -> Không giảm (0%).
    - `paymentMethod`: Phải chọn một trong các giá trị hợp lệ (`COD` hoặc `BANKING`), không được để giá trị rỗng.
  - **Giới hạn phạm vi kỹ thuật**:
    - Tuyệt đối KHÔNG sử dụng Fetch API, Async/Await, Promise.
    - Tuyệt đối KHÔNG sử dụng LocalStorage / SessionStorage.
    - Tất cả việc lưu giữ trạng thái và hiển thị dữ liệu được thực hiện trực tiếp trên DOM của trang hiện tại.
  - **Tự chủ thuật toán & Clean Code**:
    - Học viên tự thiết kế cấu trúc hàm (phân tách rõ hàm xử lý kiểm tra validation và hàm cập nhật DOM).
    - Đặt tên biến và hàm theo chuẩn `camelCase`, phản ánh đúng ngữ nghĩa nghiệp vụ.
    - Mã nguồn gọn gàng, có ghi chú (comments) giải thích các bước xử lý chính.


## 4. Checklist đánh giá kết quả (Nghiệm thu)
- [ ] Xây dựng giao diện Form Đặt Hàng Nhanh và Khối Tóm Tắt Đơn Hàng đáp ứng đúng bối cảnh nghiệp vụ E-Commerce.
- [ ] Đăng ký thành công sự kiện `submit` cho Form bằng `addEventListener` và ngăn chặn được hành vi reload trang mặc định.
- [ ] Kiểm tra chính xác tất cả các điều kiện ràng buộc của dữ liệu đầu vào (`fullName`, `phoneNumber`, `paymentMethod`).
- [ ] Xử lý chính xác logic quy đổi mã giảm giá (`promoCode`) theo đúng yêu cầu nghiệp vụ.
- [ ] Hiển thị chính xác các thông báo lỗi bên dưới ô nhập liệu khi dữ liệu không hợp lệ (Trường hợp ngoại lệ).
- [ ] Cập nhật và hiển thị thành công khối tóm tắt đơn hàng, đồng thời reset Form về trạng thái ban đầu khi dữ liệu hợp lệ (Trường hợp chuẩn).
- [ ] Tuyệt đối không sử dụng các công nghệ nằm trong phạm vi bị cấm (Fetch API, Async/Await, LocalStorage).
- [ ] Mã nguồn đạt chuẩn Clean Code, đặt tên biến/hàm theo đúng quy chuẩn `camelCase` và có chú thích rõ ràng.