# Bài thực hành: Khởi tạo và Chuẩn hóa Kho lưu trữ Mã nguồn Doanh nghiệp với Git CLI và GitHub Cloud

## 1. Mục tiêu
- Vận dụng kiến thức Git CLI 2.45+ và GitHub Cloud để khởi tạo cấu trúc kho lưu trữ mã nguồn chuẩn doanh nghiệp cho dự án Web Responsive JavaScript.
- Thực thi luồng làm việc Git Flow, thiết lập quy tắc đặt tên nhánh Semantic Branching (main, develop, feature/*) và chuẩn hóa lịch sử commit theo Conventional Commits.
- Thành thạo thao tác khởi tạo Pull Request, thực hiện Code Review và kiểm chuẩn cấu trúc kho lưu trữ đạt tiêu chuẩn đầu ra dự án.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Git CLI 2.45+, tài khoản GitHub Cloud, trình duyệt web và thư mục mã nguồn khởi tạo cho dự án Web Responsive JavaScript.

### Các bước thực hiện:
1. Bước 1: Khởi tạo repository cục bộ bằng lệnh git init -b main trên Git CLI 2.45+, cấu hình thông tin git user và thiết lập tệp .gitignore chuẩn cho dự án JavaScript.
2. Bước 2: Tạo commit khởi tạo tuân thủ Conventional Commits (feat: initial project setup) và đẩy mã nguồn lên GitHub Cloud qua lệnh git remote add origin và git push.
3. Bước 3: Thiết lập mô hình Git Flow bằng cách tạo nhánh develop từ main và khởi tạo nhánh tính năng Semantic Branching feature/responsive-header từ develop.
4. Bước 4: Thực thi các thao tác lập trình giao diện header, thực hiện các commit chi tiết tuân thủ Conventional Commits (feat(header): add navigation bar layout).
5. Bước 5: Đẩy nhánh tính năng lên GitHub Cloud, khởi tạo Pull Request vào nhánh develop, thực hiện quy trình Code Review giả định và hoàn tất Merge Pull Request.

## 3. Checklist đánh giá
- [ ] Kho lưu trữ trên GitHub Cloud có đầy đủ các nhánh cốt lõi (main, develop, feature/*) tuân thủ đúng quy tắc Git Flow và Semantic Branching.
- [ ] Tất cả các commit message đều tuân thủ 100% quy chuẩn Conventional Commits (feat, fix, docs, chore).
- [ ] Quy trình tạo Pull Request, Code Review và Merge PR trên GitHub Cloud được thực hiện chính xác, không có xung đột mã nguồn.
- [ ] Cấu trúc kho lưu trữ đạt chuẩn doanh nghiệp với đầy đủ tệp .gitignore, README.md mô tả rõ ràng kỳ vọng sản phẩm.