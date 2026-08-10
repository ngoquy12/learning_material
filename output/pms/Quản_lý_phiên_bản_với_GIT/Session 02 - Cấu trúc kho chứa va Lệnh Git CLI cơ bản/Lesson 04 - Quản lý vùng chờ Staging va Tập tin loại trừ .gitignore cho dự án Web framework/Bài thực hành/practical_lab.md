# Bài thực hành: Quản lý Staging Area và Cấu hình .gitignore Bỏ qua Tệp tin Nhạy cảm trong Dự án Web Framework

## 1. Mục tiêu
- Vận dụng kiến thức Git CLI 2.45+ để thao tác chuyển tệp tin vào Staging Area và kiểm soát trạng thái vùng chờ bằng các lệnh git add, git status.
- Thành thạo kỹ năng khởi tạo và cấu hình tệp .gitignore để loại trừ thư mục node_modules, tệp môi trường nhạy cảm .env và các tệp build artifacts khỏi lịch sử quản lý phiên bản.
- Thực hành quy trình Git Flow / Semantic Branching và viết thông điệp commit tuân thủ quy chuẩn Conventional Commits khi làm việc với GitHub Cloud.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển gồm Git CLI 2.45+, tài khoản GitHub Cloud, dự án Web framework (JavaScript/Node.js) chứa thư mục node_modules, tệp cấu hình môi trường .env, mã nguồn trong thư mục src/ và kết quả đóng gói trong thư mục dist/.

### Các bước thực hiện:
1. Bước 1: Tạo và chuyển sang nhánh tính năng mới theo quy chuẩn Semantic Branching (ví dụ: feature/staging-gitignore) từ nhánh develop. Khởi tạo cấu trúc dự án mẫu gồm tệp .env, thư mục node_modules/, thư mục dist/ và tệp src/app.js.
2. Bước 2: Soạn thảo tệp .gitignore theo đúng cú pháp để loại trừ tệp môi trường (.env, .env.local), thư mục phụ thuộc (node_modules/), sản phẩm đóng gói (dist/, build/) và tệp hệ điều hành (.DS_Store, Thumbs.db).
3. Bước 3: Sử dụng các lệnh Git CLI 2.45+ (git status, git add) để kiểm tra trạng thái và đưa các tệp hợp lệ vào Staging Area. Thực hành xử lý tình huống vô tình đưa tệp nhạy cảm vào Staging Area bằng lệnh git restore --staged <file> để đưa tệp trở lại Working Directory.
4. Bước 4: Kiểm tra lại toàn bộ danh sách tệp trong Staging Area, thực hiện commit với thông điệp chuẩn Conventional Commits (ví dụ: feat(config): add .gitignore and setup staging rules) và đẩy nhánh feature/staging-gitignore lên GitHub Cloud.

## 3. Checklist đánh giá
- [ ] Thao tác tạo và đặt tên nhánh đúng quy chuẩn Semantic Branching trên Git CLI 2.45+.
- [ ] Cấu hình tệp .gitignore hoàn chỉnh, loại bỏ chính xác các tệp/thư mục nhạy cảm (.env, node_modules/, dist/) khỏi danh sách theo dõi của Git.
- [ ] Sử dụng thành thạo các lệnh git add, git restore --staged và git status để kiểm soát vùng chờ Staging Area không chứa tệp rác hay tệp bảo mật.
- [ ] Thông điệp commit tuân thủ định dạng Conventional Commits và nhánh được đẩy lên GitHub Cloud không phát sinh xung đột hay lỗi hệ thống.