# Bài thực hành: Xây dựng ứng dụng tính toán chỉ số hiệu quả học tập Python cá nhân hóa

## 1. Mục tiêu
- Vận dụng kiến thức ép kiểu và khai báo biến trong Python 3.12 Core để thu thập và xử lý các chỉ số học tập.
- Thực hiện các phép toán số học để tính toán phân bổ thời gian học tập theo phương pháp thực hành chủ động.
- Định dạng đầu ra báo cáo tổng quan lộ trình học tập chuyên nghiệp bằng f-string.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Dữ liệu thông tin học viên, số giờ học dự kiến mỗi tuần và thời lượng dành cho thực hành thu thập từ Terminal (CLI).

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp mã nguồn study_plan.py và thiết lập khai báo thông tin ban đầu của khóa học.
2. Bước 2: Sử dụng hàm input() thu thập số giờ học lý thuyết, thực hành và số tuần cam kết từ người dùng.
3. Bước 3: Chuyển đổi kiểu dữ liệu tường minh (int, float) và tính toán tỷ lệ phần trăm thời lượng thực hành thực tế.
4. Bước 4: Tính toán tổng số giờ tích lũy dự kiến và kiểm tra chỉ số đạt chuẩn phương pháp Active Learning.
5. Bước 5: Định dạng và hiển thị bảng báo cáo chỉ số học tập cá nhân hóa ra giao diện dòng lệnh.

## 3. Checklist đánh giá
- [ ] Mã nguồn thực thi thành công không phát sinh lỗi cú pháp trên Python 3.12.
- [ ] Thực hiện ép kiểu dữ liệu int và float tường minh chính xác cho dữ liệu đầu vào.
- [ ] Tính toán đúng tỷ lệ phần trăm phân bổ thời gian thực hành theo công thức nghiệp vụ.
- [ ] Định dạng đầu ra hiển thị chuẩn báo cáo thông số học tập theo mẫu yêu cầu.