# Bài thực hành: Xây dựng công cụ dự toán ngân sách dự án phần mềm

## 1. Mục tiêu
- Xây dựng kịch bản tương tác dữ liệu cơ bản qua giao diện dòng lệnh bằng Python 3.12.
- Thực hành chuyển đổi kiểu dữ liệu tường minh và định dạng chuỗi f-string xuất báo cáo tài chính doanh nghiệp.
- Nắm vững quy chuẩn mã nguồn và mô hình sản phẩm đầu ra theo yêu cầu doanh nghiệp.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Dữ liệu đầu vào thu thập qua giao diện dòng lệnh (CLI): Tên dự án, số lượng lập trình viên, tổng số giờ phát triển, đơn giá nhân công theo giờ và chi phí dự phòng.

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp mã nguồn main.py và định nghĩa thông báo chào mừng hệ thống quản lý dự án.
2. Bước 2: Thu thập thông tin dự toán từ người dùng và thực hiện ép kiểu dữ liệu tường minh (str, int, float).
3. Bước 3: Thực hiện tính toán tổng chi phí nhân sự, chi phí dự phòng rủi ro và tổng ngân sách dự án.
4. Bước 4: Định dạng và hiển thị bảng báo cáo dự toán ngân sách chi tiết ra màn hình dòng lệnh bằng f-string.

## 3. Checklist đánh giá
- [ ] Mã nguồn thực thi thành công không phát sinh lỗi cú pháp hoặc lỗi runtime trên Python 3.12.
- [ ] Thực hiện ép kiểu dữ liệu đầu vào chính xác từ chuỗi sang kiểu số nguyên và số thực.
- [ ] Đầu ra báo cáo hiển thị đầy đủ thông tin dự án và chỉ số tài chính được định dạng rõ ràng.
- [ ] Tên biến tuân thủ đúng quy tắc snake_case theo chuẩn PEP 8.