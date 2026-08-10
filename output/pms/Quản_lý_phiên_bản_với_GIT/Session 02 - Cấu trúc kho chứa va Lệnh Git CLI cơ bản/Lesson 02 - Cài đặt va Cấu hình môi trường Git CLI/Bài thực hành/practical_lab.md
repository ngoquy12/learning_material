# Bài thực hành: Cài đặt, Cấu hình Danh tính chuẩn và Tích hợp Git CLI 2.45+ trên VS Code

## 1. Mục tiêu
- Cài đặt và kiểm tra phiên bản Git CLI 2.45+ trên môi trường máy tính cá nhân.
- Thiết lập thành thạo danh tính toàn cục (user.name, user.email), nhánh mặc định main và trình biên tập mã nguồn VS Code.
- Tích hợp thành công Git Terminal vào VS Code và kiểm thử tính hợp lệ của hệ thống cấu hình Git CLI.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Máy tính cá nhân (Windows/macOS/Linux), phần mềm VS Code đã cài đặt, kết nối Internet để tải bản cài Git CLI 2.45+.

### Các bước thực hiện:
1. Bước 1: Tải về và tiến hành cài đặt Git CLI phiên bản 2.45+ từ trang chủ git-scm.com. Kiểm tra cài đặt thành công qua câu lệnh git --version trên Terminal/Command Prompt.
2. Bước 2: Cấu hình thông tin danh tính lập trình viên toàn cục (Global Config) sử dụng các lệnh: git config --global user.name "[Họ và Tên]" và git config --global user.email "[Email GitHub]".
3. Bước 3: Đặt tên nhánh mặc định khi khởi tạo kho lưu trữ là main qua lệnh git config --global init.defaultBranch main, đồng thời thiết lập VS Code làm trình biên tập mặc định với git config --global core.editor "code --wait".
4. Bước 4: Mở VS Code, cấu hình Git Bash/Terminal mặc định trong không gian làm việc. Chạy câu lệnh git config --list --show-origin để kiểm tra toàn bộ cấu hình và thực thi lệnh git init trên một thư mục mẫu để xác nhận kết quả.

## 3. Checklist đánh giá
- [ ] Kết xuất câu lệnh git --version xác nhận phiên bản Git CLI từ 2.45 trở lên.
- [ ] Cấu hình user.name và user.email chính xác, sẵn sàng cho quy chuẩn Commit trên GitHub Cloud.
- [ ] Nhánh khởi tạo mặc định được ghi nhận là main và core.editor được gán thành công cho VS Code.
- [ ] Tích hợp và thực thi trơn tru câu lệnh Git CLI trong Terminal của VS Code mà không phát sinh lỗi.