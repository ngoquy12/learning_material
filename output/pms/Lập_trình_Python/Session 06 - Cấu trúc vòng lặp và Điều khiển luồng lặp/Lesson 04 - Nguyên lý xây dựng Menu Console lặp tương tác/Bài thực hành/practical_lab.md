# Bài thực hành: Xây dựng hệ thống Menu CLI quản lý thông tin điều khiển lặp tương tác bằng Python

## 1. Mục tiêu
- Vận dụng vòng lặp while True trong Python để khởi tạo luồng điều khiển lặp vô hạn cho ứng dụng console.
- Thành thạo cấu trúc rẽ nhánh để xử lý chính xác các lựa chọn chức năng từ bàn phím người dùng.
- Triển khai cơ chế thoát chương trình an toàn và xử lý ngoại lệ đầu vào không hợp lệ nhằm đảm bảo ứng dụng hoạt động ổn định.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x, trình soạn thảo mã nguồn (VS Code hoặc PyCharm) và tệp khởi tạo main.py.

### Các bước thực hiện:
1. Bước 1: Khởi tạo cấu trúc tệp mã nguồn main.py và định nghĩa hàm hiển thị giao diện menu console chứa danh sách các tính năng cùng tùy chọn thoát.
2. Bước 2: Xây dựng luồng điều khiển chính sử dụng vòng lặp while True, tiếp nhận dữ liệu nhập vào từ người dùng thông qua hàm input() và rẽ nhánh thực thi chức năng tương ứng.
3. Bước 3: Tích hợp khối lệnh try-except để bắt bẫy lỗi khi người dùng nhập dữ liệu sai định dạng hoặc lựa chọn nằm ngoài danh mục hệ thống.
4. Bước 4: Thiết lập cơ chế thoát chương trình an toàn bằng câu lệnh break khi người dùng chọn lệnh thoát, kiểm thử toàn bộ luồng tương tác và hoàn tất bài thực hành.

## 3. Checklist đánh giá
- [ ] Chương trình duy trì được vòng lặp tương tác liên tục và chỉ kết thúc đúng thời điểm người dùng chọn lệnh thoát.
- [ ] Xử lý chính xác tất cả các lựa chọn hợp lệ và bắt lỗi thành công các đầu vào không hợp lệ mà không làm dừng đột ngột ứng dụng.
- [ ] Mã nguồn tuân thủ quy chuẩn PEP 8 của Python, phân chia hàm xử lý rõ ràng và tối ưu luồng điều khiển.