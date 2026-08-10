# Bài thực hành: Ứng dụng Prompt Engineering trong quản lý kho mã nguồn Git và xử lý lỗi Terminal

## 1. Mục tiêu
- Vận dụng kỹ thuật Prompt Engineering với LLM (ChatGPT/Claude) để sinh chính xác câu lệnh Git CLI 2.45+ và xử lý các lỗi terminal phát sinh.
- Thành thạo khởi tạo repository, áp dụng quy chuẩn Semantic Branching và Conventional Commits trên GitHub Cloud.
- Rèn luyện kỹ năng tự học chủ động và quản lý thời gian khi phối hợp làm việc nhóm với Git Workflow.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Máy tính đã cài đặt Git CLI 2.45+, tài khoản GitHub Cloud, truy cập công cụ LLM (ChatGPT/Claude) và tệp tài liệu bài học 'phuong-phap-hoc-tap.md'.

### Các bước thực hiện:
1. Bước 1: Khởi tạo kho lưu trữ Git local với Git CLI 2.45+. Soạn prompt cho AI để lấy chuỗi lệnh thiết lập thông tin user, khởi tạo nhánh chính 'main' và tạo nhánh tính năng mới theo quy chuẩn Semantic Branching ('feature/active-learning').
2. Bước 2: Tải tệp 'phuong-phap-hoc-tap.md' vào thư mục làm việc. Sử dụng prompt kỹ thuật để yêu cầu AI tóm tắt nội dung chính về phương pháp tự học chủ động và quản lý thời gian nhóm, sau đó ghi kết quả vào tệp.
3. Bước 3: Thực hiện lưu trữ thay đổi bằng Git CLI tuân thủ quy chuẩn Conventional Commits (ví dụ: 'docs: summarize active learning techniques'). Cố tình tạo một tình huống lỗi Terminal (như push sai tên nhánh hoặc thiếu thông tin remote) và dùng AI để giải thích nguyên nhân kèm câu lệnh sửa lỗi.
4. Bước 4: Đẩy (push) mã nguồn lên GitHub Cloud, tiến hành mở Pull Request (PR) từ nhánh 'feature/active-learning' vào nhánh 'main' và kiểm tra lịch sử commit hiển thị đúng chuẩn.

## 3. Checklist đánh giá
- [ ] Khởi tạo repository thành công bằng Git CLI 2.45+ và kết nối chính xác với kho lưu trữ từ xa trên GitHub Cloud.
- [ ] Thực hiện đúng quy chuẩn Semantic Branching (nhánh 'feature/active-learning') và ghi chú commit tuân thủ chuẩn Conventional Commits.
- [ ] Áp dụng hiệu quả Prompt Engineering để nhờ AI giải thích lỗi Terminal và sinh câu lệnh Git chính xác.
- [ ] Tệp tài liệu được tóm tắt đầy đủ nội dung bài học và Pull Request được tạo thành công trên GitHub Cloud mà không có xung đột.