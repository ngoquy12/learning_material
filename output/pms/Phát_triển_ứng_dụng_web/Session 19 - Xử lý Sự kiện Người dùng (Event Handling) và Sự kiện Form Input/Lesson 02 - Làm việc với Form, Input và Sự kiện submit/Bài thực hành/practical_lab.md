# Bài thực hành: Xây dựng Tính năng Đăng ký Tài khoản Khách hàng Nền tảng E-commerce

## 1. Mục tiêu bài học
- Cấu hình giao diện HTML chứa biểu mẫu đăng ký với các ID định danh cho trường thông tin và thông báo
- Triển khai sự kiện submit trong JavaScript, áp dụng event.preventDefault() để ngăn chặn trang reload và thu thập dữ liệu từ ô nhập liệu
- Thực hiện kiểm tra tính hợp lệ dữ liệu (validation) nhiều cấp độ, hiển thị phản hồi chi tiết và reset form khi đăng ký thành công

## 2. Yêu cầu bài toán
Trong các ứng dụng thương mại điện tử (E-commerce), tính năng đăng ký tài khoản là điểm chạm đầu tiên để thu thập thông tin khách hàng. Mặc định khi người dùng bấm nút gửi dữ liệu trên form, trình duyệt sẽ gửi request và tải lại (reload) toàn bộ trang web ngay lập tức. Điều này khiến cho các xử lý hiển thị thông báo lỗi hoặc phản hồi phía giao diện bằng JavaScript không kịp thực thi hoặc bị xóa mất.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển bao gồm trình duyệt web (Chrome, Firefox, Edge) và trình soạn thảo mã nguồn VS Code. Dữ liệu đầu vào gồm các giá trị chuỗi người dùng nhập tại Form: Họ và tên, Email, Mật khẩu, và Mật khẩu xác nhận.

### Các bước thực hiện:
1. Bước 1: Khởi tạo cấu trúc giao diện HTML bao gồm form đăng ký (id: registration-form), các ô nhập liệu (id: fullname, email, password, confirm-password), nút đăng ký (type: submit) và thẻ div hiển thị thông báo (id: status-message).
2. Bước 2: Lấy tham chiếu các phần tử DOM trong JavaScript và gắn sự kiện submit cho form đăng ký thông qua phương thức addEventListener.
3. Bước 3: Gọi hàm event.preventDefault() ngay tại dòng đầu tiên của hàm xử lý sự kiện để ngăn reload trang. Tiến hành lấy giá trị các ô input bằng thuộc tính .value và dùng .trim() loại bỏ khoảng trắng dư thừa.
4. Bước 4: Viết các câu lệnh điều kiện validation kiểm tra: các trường không được rỗng, email chứa ký tự '@', mật khẩu có độ dài tối thiểu 6 ký tự và mật khẩu xác nhận trùng khớp. Kiểm thử phản hồi trên từng trường hợp và reset form sau khi đăng ký thành công.

## 4. Mã nguồn tham khảo (Code Demo)

```text
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Đăng ký Tài khoản E-commerce</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 300px; padding: 8px; box-sizing: border-box; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        #status-message { margin-top: 15px; font-weight: bold; }
    </style>
</head>
<body>

    <h2>Đăng Ký Tài Khoản Khách Hàng</h2>
    <form id="registration-form">
        <div class="form-group">
            <label for="fullname">Họ và tên:</label>
            <input type="text" id="fullname" placeholder="Nhập họ và tên">
        </div>
        <div class="form-group">
            <label for="email">Địa chỉ Email:</label>
            <input type="text" id="email" placeholder="example@domain.com">
        </div>
        <div class="form-group">
            <label for="password">Mật khẩu:</label>
            <input type="password" id="password" placeholder="Tối thiểu 6 ký tự">
        </div>
        <div class="form-group">
            <label for="confirm-password">Xác nhận mật khẩu:</label>
            <input type="password" id="confirm-password" placeholder="Nhập lại mật khẩu">
        </div>
        <button type="submit">Đăng Ký</button>
    </form>

    <div id="status-message"></div>

    <script>
        // 1. Lấy tham chiếu đến các phần tử DOM
        const registrationForm = document.getElementById('registration-form');
        const fullnameInput = document.getElementById('fullname');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirm-password');
        const statusMessage = document.getElementById('status-message');

        // 2. Đăng ký sự kiện submit cho biểu mẫu
        registrationForm.addEventListener('submit', function(event) {
            // BẮT BUỘC: Ngăn chặn hành vi nạp lại trang mặc định
            event.preventDefault();

            // 3. Lấy giá trị từ các ô input ngay tại thời điểm submit
            const fullname = fullnameInput.value.trim();
            const email = emailInput.value.trim();
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;

            // 4. Kiểm tra Validation từng cấp độ
            // Kiểm tra trường rỗng
            if (!fullname || !email || !password || !confirmPassword) {
                statusMessage.textContent = 'Lỗi: Tất cả các trường thông tin đều là bắt buộc!';
                statusMessage.style.color = 'red';
                return;
            }

            // Kiểm tra định dạng email cơ bản
            if (!email.includes('@')) {
                statusMessage.textContent = 'Lỗi: Địa chỉ email không đúng định dạng (thiếu ký tự @)!';
                statusMessage.style.color = 'red';
                return;
            }

            // Kiểm tra độ dài mật khẩu
            if (password.length < 6) {
                statusMessage.textContent = 'Lỗi: Mật khẩu phải có độ dài từ 6 ký tự trở lên!';
                statusMessage.style.color = 'red';
                return;
            }

            // Kiểm tra mật khẩu xác nhận trùng khớp
            if (password !== confirmPassword) {
                statusMessage.textContent = 'Lỗi: Mật khẩu xác nhận không trùng khớp với mật khẩu đã nhập!';
                statusMessage.style.color = 'red';
                return;
            }

            // 5. Xử lý khi tất cả dữ liệu hợp lệ
            statusMessage.textContent = 'Thành công: Tài khoản của ' + fullname + ' đã được tạo thành công!';
            statusMessage.style.color = 'green';

            // Làm sạch toàn bộ nội dung đã nhập trên biểu mẫu
            registrationForm.reset();
        });
    </script>
</body>
</html>
```

## 5. Checklist đánh giá kết quả
- [ ] Xây dựng đúng cấu trúc HTML Form đăng ký với các ID tương ứng cho các phần tử DOM
- [ ] Sử dụng hàm event.preventDefault() chính xác để ngăn sự kiện submit reload trang
- [ ] Lấy được giá trị input (.value) đúng cách bên trong lắng nghe sự kiện submit
- [ ] Triển khai đầy đủ logic validate (bắt rỗng, kiểm tra @, kiểm tra độ dài mật khẩu, khớp mật khẩu) và gọi form.reset() thành công