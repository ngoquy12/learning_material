# Xử lý Sự kiện Người dùng và Sự kiện Form Input

## Lesson 01 — Đăng ký Sự kiện với addEventListener
### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Cơ chế lắng nghe và phản hồi thao tác tương tác người dùng trên DOM.
- Vai trò: Tách rời HTML và JavaScript, cho phép gán nhiều trình xử lý sự kiện độc lập.
### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:
  ```javascript
  targetElement.addEventListener(eventType, handlerFunction);
  ```
- Giải thích thành phần:
  - targetElement: Phần tử DOM chịu tác động của hành vi tương tác.
  - eventType: Tên sự kiện dạng chuỗi như click, dblclick, mouseover.
  - handlerFunction: Hàm thực thi khi sự kiện tương ứng được kích hoạt.
### Ví dụ thực hành
- Kịch bản áp dụng: Cập nhật văn bản và màu nền nút bấm khi người dùng nhấn lưu.
  ```javascript
  const saveButton = document.querySelector("#btn-save-task");

  function updateButtonUI() {
    saveButton.innerText = "Đã lưu thành công!";
    saveButton.style.backgroundColor = "#22c55e";
  }

  saveButton.addEventListener("click", updateButtonUI);
  ```
- Giải thích ví dụ: Đăng ký hàm updateButtonUI vào sự kiện click của nút bấm an toàn.
### Lưu ý triển khai
- **Ghi đè logic**: Tránh gán trực tiếp thuộc tính onclick vì sẽ đè mất logic xử lý cũ.
- **Quy chuẩn đặt tên**: Tên sự kiện viết chữ thường, không chứa tiền tố on như click hoặc mouseover.

## Lesson 02 — Làm việc với Form, Input và Sự kiện submit
### Khái niệm & Vai trò
- Định nghĩa ngắn gọn: Quy trình kiểm soát và xử lý dữ liệu biểu mẫu HTML khi gửi.
- Vai trò: Ngăn trang web tải lại mặc định, thu thập và kiểm tra dữ liệu trước khi gửi.
### Cú pháp & Giải nghĩa
- Khai báo cú pháp chuẩn:
  ```javascript
  formElement.addEventListener("submit", function (event) {
    event.preventDefault();
    const inputValue = inputElement.value.trim();
  });
  ```
- Giải thích thành phần:
  - formElement: Thẻ form chứa các ô nhập liệu của biểu mẫu.
  - event.preventDefault(): Phương thức hủy bỏ hành vi tải lại trang mặc định.
  - inputElement.value.trim(): Lấy chuỗi đầu vào và loại bỏ khoảng trắng hai đầu.
### Ví dụ thực hành
- Kịch bản áp dụng: Xử lý submit form đăng ký và kiểm tra ô họ tên không được rỗng.
  ```javascript
  const bookingForm = document.querySelector("#booking-form");
  const fullnameInput = document.querySelector("#fullname-input");
  const statusMessage = document.querySelector("#status-message");

  bookingForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const cleanFullname = fullnameInput.value.trim();
    if (cleanFullname === "") {
      statusMessage.innerText = "Vui lòng nhập họ tên!";
      return;
    }
    statusMessage.innerText = "Đặt lịch thành công: " + cleanFullname;
  });
  ```
- Giải thích ví dụ: Chặn reload trang, đọc và làm sạch dữ liệu nhập, hiển thị thông báo.
### Lưu ý triển khai
- **Đọc dữ liệu sai thời điểm**: Không truy xuất thuộc tính value bên ngoài callback vì dữ liệu luôn bị rỗng.
- **Đăng ký sai phần tử**: Đăng ký sự kiện submit trên thẻ form thay vì bắt click trên button.

## Liên kết hệ thống
- Mối quan hệ logic: addEventListener của Lesson 01 cung cấp nền tảng gán sự kiện submit cho Lesson 02.
- Luồng dữ liệu xuyên suốt: Tương tác submit -> Hủy reload trang -> Đọc và cắt khoảng trắng value -> Cập nhật UI.
- Ứng dụng tổng hợp: Thiết kế form tương tác động, xác thực dữ liệu phía client và xử lý giao diện linh hoạt.