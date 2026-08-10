# Bài thực hành: Xây dựng công cụ thu thập thông tin hệ thống và tính toán chi phí máy chủ enterprise

## 1. Mục tiêu
- Vận dụng cú pháp Python 3.12 Core để nhập, xuất dữ liệu và tương tác với người dùng qua giao diện dòng lệnh CLI.
- Thực hành khai báo biến, ép kiểu dữ liệu tường minh và xử lý các kiểu dữ liệu cơ bản như integer, float, string, boolean.
- Ứng dụng chuỗi định dạng f-string để xuất báo cáo chi phí vận hành máy chủ đạt chuẩn định dạng doanh nghiệp.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Dữ liệu nhập từ Terminal/CLI bao gồm: Tên máy chủ (string), Số lượng nhân CPU (integer), Dung lượng RAM tính bằng GB (float), Chi phí điện năng theo giờ (float), và Trạng thái kích hoạt máy chủ (boolean/string).

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp mã nguồn main.py và kiểm tra phiên bản môi trường thực thi Python 3.12 bằng thư viện sys.
2. Bước 2: Sử dụng hàm input() kết hợp ép kiểu dữ liệu tường minh để thu thập thông tin cấu hình máy chủ từ người dùng.
3. Bước 3: Thực hiện các phép toán đại số tính tổng dung lượng tài nguyên và dự toán chi phí vận hành theo tháng (30 ngày).
4. Bước 4: Sử dụng f-string và các quy tắc căn chỉnh chuỗi để in báo cáo tổng quan thông số hệ thống ra màn hình CLI.

## 3. Checklist đánh giá
- [ ] Mã nguồn thực thi thành công trên môi trường Python 3.12 không gặp lỗi cú pháp SyntaxError hoặc lỗi kiểu dữ liệu TypeError.
- [ ] Thực hiện ép kiểu dữ liệu tường minh chính xác cho các giá trị số nguyên (int) và số thực (float) khi nhận dữ liệu từ hàm input().
- [ ] Tính toán đúng tổng chi phí vận hành máy chủ theo công thức với độ chính xác lấy 2 chữ số thập phân.
- [ ] Định dạng đầu ra hiển thị đầy đủ thông tin báo cáo hệ thống, sử dụng f-string căn chỉnh đẹp mắt đúng yêu cầu bài tập.