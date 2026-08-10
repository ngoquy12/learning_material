# Bài thực hành: Xây dựng hệ thống thẩm định điều kiện vay vốn và tối ưu hóa logic đánh giá ngắn mạch

## 1. Mục tiêu
- Vận dụng kiến thức Python về toán tử so sánh và toán tử logic để xây dựng các biểu thức điều kiện trả về kiểu Boolean chính xác.
- Phân tích và vận dụng cơ chế đánh giá ngắn mạch (Short-circuit Evaluation) để tối ưu hóa hiệu năng chương trình và phòng ngừa lỗi runtime.
- Thành thạo thao tác thực hành kiểm thử các kịch bản kiểm tra điều kiện phức tạp dựa trên bảng giá trị chân lý.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x, trình soạn thảo mã nguồn và tập dữ liệu mô phỏng hồ sơ tín dụng của khách hàng.

### Các bước thực hiện:
1. Bước 1: Khởi tạo không gian làm việc, tạo tệp main.py và khai báo các biến mô phỏng thông tin khách hàng như tuổi, thu nhập hàng tháng, điểm tín dụng và trạng thái nợ xấu.
2. Bước 2: Xây dựng các biểu thức điều kiện sử dụng toán tử so sánh (==, !=, >, <, >=, <=) kết hợp toán tử logic (and, or, not) để đánh giá tiêu chuẩn phê duyệt khoản vay.
3. Bước 3: Thiết lập tình huống thử nghiệm cơ chế Short-circuit Evaluation bằng cách kết hợp biểu thức logic với hàm kiểm tra kiểm soát thứ tự thực thi nhằm tránh lỗi chia cho 0 hoặc truy xuất dữ liệu không hợp lệ.
4. Bước 4: Chạy kiểm thử trên nhiều bộ dữ liệu thử nghiệm khác nhau, in kết quả Boolean và đối chiếu với bảng giá trị chân lý để hoàn tất bài thực hành.

## 3. Checklist đánh giá
- [ ] Xây dựng chính xác các biểu thức điều kiện trả về kiểu Boolean theo đúng yêu cầu nghiệp vụ.
- [ ] Giải thích và chứng minh được cơ chế Short-circuit Evaluation thông qua kết quả chạy chương trình.
- [ ] Tuân thủ quy chuẩn mã nguồn Python PEP 8 và khai báo biến rõ ràng.
- [ ] Kết quả kiểm thử đạt 100% yêu cầu trên tất cả các bộ dữ liệu đầu vào.