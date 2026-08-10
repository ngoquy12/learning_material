# Bài thực hành: Xây dựng hệ thống tính giá vé và phân loại ưu đãi tự động bằng Python

## 1. Mục tiêu
- Vận dụng cấu trúc rẽ nhánh if, if-else, if-elif-else trong Python để xử lý luồng điều khiển theo điều kiện thực tế.
- Thành thạo việc áp dụng quy tắc thụt lề (Indentation) chuẩn PEP 8 nhằm đảm bảo tính chính xác của khối lệnh trong Python.
- Thực hiện kiểm thử hệ thống với nhiều kịch bản dữ liệu khác nhau và xử lý các tình huống đầu vào không hợp lệ.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x (VS Code/PyCharm) và tệp mã nguồn main.py.

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp main.py, định nghĩa các biến chứa dữ liệu đầu vào bao gồm tuổi của khách hàng (age) và tổng giá trị đơn hàng (order_amount).
2. Bước 2: Triển khai câu lệnh rẽ nhánh đơn if để kiểm tra tính hợp lệ của dữ liệu đầu vào (tuổi phải lớn hơn 0 và giá trị đơn hàng không được âm).
3. Bước 3: Xây dựng cấu trúc rẽ nhánh nhiều trường hợp if-elif-else để phân loại mức giảm giá dựa trên độ tuổi (dưới 12 tuổi giảm 50%, từ 60 tuổi trở lên giảm 30%, các trường hợp còn lại giữ nguyên giá). Chú ý thụt lề 4 khoảng trắng cho mỗi khối lệnh.
4. Bước 4: Sử dụng cấu trúc rẽ nhánh nhị phân if-else để tính phí giao hàng (miễn phí giao hàng nếu đơn hàng trên 500,000 VND, ngược lại tính phí 30,000 VND).
5. Bước 5: Chạy chương trình với nhiều tập dữ liệu mẫu khác nhau, đối soát kết quả hiển thị trên terminal để đảm bảo luồng rẽ nhánh hoạt động đúng kỳ vọng.

## 3. Checklist đánh giá
- [ ] Mã nguồn thực thi thành công, không gặp lỗi IndentationError, TabError hay SyntaxError.
- [ ] Áp dụng chính xác cú pháp rẽ nhánh đơn if, nhị phân if-else và nhiều trường hợp if-elif-else theo đúng bài toán nghiệp vụ.
- [ ] Tuân thủ quy tắc thụt lề chuẩn 4 khoảng trắng của Python trong tất cả các khối lệnh rẽ nhánh.
- [ ] Kết quả tính toán giá vé, chiết khấu và phí giao hàng hiển thị chính xác theo từng kịch bản kiểm thử.