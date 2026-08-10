# Bài thực hành: Xây dựng Kịch bản Kiểm tra Môi trường và Tích hợp AI Assistant Doanh nghiệp

## 1. Mục tiêu
- Vận dụng kiến thức Python 3.12 Core để tạo lập và quản lý môi trường làm việc ảo venv chuẩn doanh nghiệp.
- Thực hành cấu hình và xác chuẩn các biến môi trường cho công cụ AI hỗ trợ phát triển phần mềm.
- Xây dựng kịch bản Python kiểm tra tự động thông số hệ thống và trạng thái sẵn sàng của môi trường phát triển.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Thông tin phiên bản Python, đường dẫn thư mục làm việc và mã khóa API của công cụ AI thu thập từ CLI hoặc tệp cấu hình biến môi trường.

### Các bước thực hiện:
1. Bước 1: Khởi tạo môi trường làm việc ảo venv bằng Python 3.12 và tạo tệp cấu hình môi trường cho dự án.
2. Bước 2: Viết mã Python đọc thông số phiên bản hệ thống và đường dẫn thực thi bằng các thư viện chuẩn sys và os.
3. Bước 3: Thực hiện kiểm tra ràng buộc logic đối với biến môi trường chứa khóa API của công cụ AI.
4. Bước 4: Tổng hợp dữ liệu kiểm tra và định dạng xuất báo cáo trạng thái môi trường phát triển ra màn hình dòng lệnh.

## 3. Checklist đánh giá
- [ ] Môi trường ảo venv được khởi tạo chính xác và kịch bản thực thi thành công trên Python 3.12.
- [ ] Truy xuất và kiểm chuẩn thành công giá trị biến môi trường API Key không gây phát sinh lỗi runtime.
- [ ] Báo cáo kết quả kiểm tra môi trường xuất ra Terminal đúng định dạng chuẩn doanh nghiệp.