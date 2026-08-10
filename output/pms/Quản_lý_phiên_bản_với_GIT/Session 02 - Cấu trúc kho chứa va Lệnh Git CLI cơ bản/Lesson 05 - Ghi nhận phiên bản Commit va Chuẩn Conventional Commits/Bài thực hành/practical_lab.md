# Bài thực hành: Ghi nhận lịch sử phát triển dự án E-Commerce với chuẩn Conventional Commits

## 1. Mục tiêu
- Vận dụng Git CLI 2.45+ để ghi nhận các phiên bản mã nguồn (commit) theo đúng quy chuẩn Conventional Commits (feat, fix, docs, style, refactor).
- Áp dụng trợ lý AI để sinh câu thông điệp commit chuẩn xác, phản ánh đúng bản chất thay đổi của mã nguồn.
- Thành thạo sử dụng các câu lệnh truy vấn lịch sử git log và git log --oneline để kiểm tra và đối soát các mốc phiên bản mã nguồn.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường máy tính đã cài đặt Git CLI 2.45+, tài khoản GitHub Cloud, thư mục dự án mã nguồn E-Commerce mẫu và công cụ AI hỗ trợ sinh thông điệp commit.

### Các bước thực hiện:
1. Bước 1: Khởi tạo và cấu hình không gian làm việc: Chuyển vào thư mục dự án E-Commerce, kiểm tra trạng thái Git CLI 2.45+ bằng câu lệnh `git status` và đảm bảo thông tin định danh `user.name`, `user.email` đã được cấu hình chính xác.
2. Bước 2: Thực hiện các thay đổi mã nguồn theo từng kịch bản tính năng và đưa tệp vào Staging Area (`git add`): Thêm file tính năng đăng nhập (`index.html`), sửa lỗi giao diện giỏ hàng (`cart.js`), bổ sung tài liệu hướng dẫn (`README.md`), điều chỉnh định dạng style (`style.css`), và tối ưu hóa hàm xử lý thanh toán (`payment.js`).
3. Bước 3: Ghi nhận phiên bản bằng lệnh `git commit -m` theo đúng quy chuẩn Conventional Commits cho từng bước: Sử dụng tiền tố `feat:` cho tính năng mới, `fix:` cho sửa lỗi, `docs:` cho tài liệu, `style:` cho định dạng mã nguồn và `refactor:` cho việc tái cấu trúc mã. Đưa diff đoạn mã vào trợ lý AI để tạo thông điệp chuẩn xác khi cần thiết.
4. Bước 4: Trực quan hóa và đối soát lịch sử commit: Sử dụng lệnh `git log` để xem chi tiết tác giả, thời gian và thông điệp commit; sau đó sử dụng `git log --oneline` để kiểm tra danh sách lịch sử ngắn gọn, đảm bảo các commit tuân thủ đúng chuẩn quy định.

## 3. Checklist đánh giá
- [ ] Thực hiện thành công việc đưa tệp vào Staging Area và commit mã nguồn mà không gặp lỗi lệnh Git CLI.
- [ ] Toàn bộ thông điệp commit tuân thủ nghiêm ngặt cấu trúc Conventional Commits với đầy đủ các loại tiền tố required (feat, fix, docs, style, refactor).
- [ ] Sử dụng AI hỗ trợ sinh được câu thông điệp commit ngắn gọn, rõ ràng, phản ánh đúng thay đổi trong mã nguồn.
- [ ] Truy vấn và hiển thị chính xác lịch sử commit bằng lệnh `git log` và `git log --oneline` theo đúng yêu cầu.