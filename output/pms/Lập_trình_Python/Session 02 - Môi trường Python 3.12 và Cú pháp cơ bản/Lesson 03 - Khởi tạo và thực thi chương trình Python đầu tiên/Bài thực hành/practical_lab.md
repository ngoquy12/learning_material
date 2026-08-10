# Bài thực hành: Xây dựng Kịch bản Khởi động và Hiển thị Báo cáo Trạng thái Hệ thống Rikkei Digital

## 1. Mục tiêu
- Vận dụng môi trường Python 3.12 Core để khởi tạo tệp mã nguồn và thực thi kịch bản hệ thống thông qua giao diện dòng lệnh CLI.
- Thực hành thu thập dữ liệu đầu vào từ bàn phím bằng hàm input() và định dạng thông điệp báo cáo bằng f-string.
- Áp dụng quy chuẩn khai báo biến và cấu trúc mã nguồn tiêu chuẩn trong dự án phần mềm doanh nghiệp.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Dữ liệu thông tin vận hành hệ thống (tên dịch vụ, phiên bản phần mềm, mã kỹ thuật viên, số lượng máy chủ) được nhập từ Terminal/CLI.

### Các bước thực hiện:
1. Bước 1: Khởi tạo tệp mã nguồn main.py và khai báo thông tin tiêu đề kịch bản theo chuẩn Python 3.12 Core.
2. Bước 2: Thu thập dữ liệu đầu vào từ giao diện dòng lệnh bao gồm tên dịch vụ, phiên bản, mã kỹ thuật viên và số lượng máy chủ.
3. Bước 3: Thực hiện chuyển đổi kiểu dữ liệu tường minh cho số lượng máy chủ từ chuỗi ký tự sang số nguyên.
4. Bước 4: Định dạng và hiển thị bảng báo cáo khởi tạo trạng thái hệ thống ra màn hình Terminal bằng f-string.

## 3. Checklist đánh giá
- [ ] Tệp mã nguồn thực thi thành công từ giao diện Terminal trên môi trường Python 3.12 mà không phát sinh lỗi cú pháp hay lỗi runtime.
- [ ] Thực hiện ép kiểu dữ liệu tường minh chính xác cho biến số lượng máy chủ từ kiểu chuỗi sang kiểu số nguyên.
- [ ] Đầu ra báo cáo hiển thị đầy đủ thông tin hệ thống đúng cấu trúc định dạng khung thông báo đã yêu cầu.