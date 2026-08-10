# Bài thực hành: Khởi tạo Repository và Quản lý Nhánh theo chuẩn Git Flow với Git CLI 2.45+ trên GitHub Cloud

## 1. Mục tiêu
- Phân biệt và chứng minh cơ chế quản lý mã nguồn phân tán (DVCS) so với VCS tập trung thông qua việc tương tác giữa Local Repository và GitHub Cloud.
- Thực thi thành thạo các câu lệnh Git CLI 2.45+ để phân tích cơ chế lưu trữ Snapshot và áp dụng quy tắc Semantic Branching, Conventional Commits.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Máy tính phát triển đã cài đặt Git CLI phiên bản 2.45 trở lên, tài khoản GitHub Cloud khả dụng và terminal bash/zsh.

### Các bước thực hiện:
1. Bước 1: Cấu hình danh tính và khởi tạo kho lưu trữ local: Sử dụng Git CLI 2.45+ thiết lập thông tin người dùng (user.name, user.email) ở phạm vi global/local và khởi tạo repository với nhánh chính đặt tên theo quy chuẩn `main` (`git init -b main`).
2. Bước 2: Phân tích cơ chế Snapshot và tạo commit theo chuẩn Conventional Commits: Tạo tệp `README.md` mô tả sự khác biệt giữa Centralized VCS và DVCS, tệp `SNAPSHOT_NOTE.md` giải thích nguyên lý snapshot của Git. Đưa các tệp vào Staging Area và thực hiện commit với thông điệp theo chuẩn Conventional Commits (`docs: add initial VCS concepts and snapshot architecture`).
3. Bước 3: Triển khai nhánh theo mô hình Git Flow và Semantic Branching: Khởi tạo nhánh `develop` từ `main`, sau đó rẽ nhánh tính năng `feature/vcs-comparison`. Cập nhật nội dung so sánh chi tiết và commit với cấu trúc `feat(vcs): analyze centralized vs distributed vcs`.
4. Bước 4: Kết nối GitHub Cloud và kiểm tra lịch sử Snapshot: Tạo một repository mới trên GitHub Cloud. Kết nối remote origin với kho lưu trữ local (`git remote add origin <URL>`), đẩy toàn bộ các nhánh (`main`, `develop`, `feature/vcs-comparison`) lên cloud. Sử dụng lệnh `git log --oneline --graph` và `git cat-file -p` để kiểm tra cây commit cùng các đối tượng snapshot (blob, tree, commit).

## 3. Checklist đánh giá
- [ ] Khởi tạo thành công Local Repository sử dụng Git CLI 2.45+ với nhánh mặc định là `main`.
- [ ] Tuân thủ chính xác quy tắc Conventional Commits cho toàn bộ các thông điệp commit (sử dụng đúng tiền tố feat, docs, chore).
- [ ] Xây dựng cấu trúc nhánh đúng chuẩn Git Flow và Semantic Branching (phân định rõ main, develop, feature/*).
- [ ] Đẩy thành công các nhánh lên GitHub Cloud và kiểm tra được sự đồng bộ dữ liệu giữa Local và Remote.
- [ ] Thao tác kiểm tra đối tượng snapshot bằng `git cat-file` và hiển thị lịch sử nhánh bằng `git log` đạt kết quả chính xác.