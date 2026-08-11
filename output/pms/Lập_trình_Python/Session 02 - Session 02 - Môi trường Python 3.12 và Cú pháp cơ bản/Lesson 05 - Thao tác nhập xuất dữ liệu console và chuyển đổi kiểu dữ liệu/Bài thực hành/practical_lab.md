# Bài thực hành: Xây dựng chương trình tính hóa đơn bán hàng và định dạng dữ liệu console

## 1. Mục tiêu
- Sử dụng thành thạo hàm input() để nhận dữ liệu từ người dùng và hàm print() kết hợp với các tham số sep, end để định dạng đầu ra console.
- Thực hiện chính xác các thao tác ép kiểu dữ liệu ép buộc (Explicit Type Casting) bằng các hàm int(), float(), str() phục vụ tính toán số liệu.
- Thành thạo thao tác thực hành, phát hiện lỗi ép kiểu sai định dạng và kiểm chuẩn kết quả đầu ra trên màn hình console.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x (VS Code, PyCharm hoặc IDLE) và tệp mã nguồn main.py.

### Các bước thực hiện:
1. Bước 1: Khởi tạo không gian làm việc và chuẩn bị tệp mã nguồn main.py.
2. Bước 2: Sử dụng hàm input() để nhận tên sản phẩm (chuỗi), số lượng (chuỗi) và đơn giá (chuỗi) từ bàn phím.
3. Bước 3: Thực hiện ép kiểu số lượng từ str sang int, đơn giá từ str sang float và tính tổng tiền thanh toán.
4. Bước 4: Sử dụng hàm print() với tham số sep và end để xuất thông tin hóa đơn chi tiết ra console theo định dạng chuẩn và hoàn tất bài thực hành.

## 3. Checklist đánh giá
- [ ] Nhận thành công dữ liệu đầu vào bằng input() và chuyển đổi đúng kiểu dữ liệu bằng int() và float().
- [ ] Sử dụng đúng cấu hình tham số sep và end trong hàm print() để định dạng thông tin console theo yêu cầu.
- [ ] Kết quả tính toán thành tiền chính xác, mã nguồn chạy mượt mà và không phát sinh lỗi cú pháp hay lỗi kiểu dữ liệu.