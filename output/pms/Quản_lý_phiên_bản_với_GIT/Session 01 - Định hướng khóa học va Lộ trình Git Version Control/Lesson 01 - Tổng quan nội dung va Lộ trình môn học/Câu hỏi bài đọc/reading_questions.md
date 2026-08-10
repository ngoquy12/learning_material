# Bộ câu hỏi tự luận kiểm tra bài đọc (Reading Comprehension Essay Questions)

### Câu 1: Trong kịch bản khởi tạo và quản lý kho lưu trữ ở bài đọc môn git cli 2.45+, github cloud (conventional commits, git flow, semantic branching), hãy phân tích hậu quả xảy ra khi lập trình viên thực thi lệnh mà quên sử dụng cờ `--global` và nêu cách kiểm tra lại file cấu hình.
> **Gợi ý trả lời & Định hướng đáp án:** Khi không có cờ `--global`, cấu hình chỉ áp dụng cho local repository hiện tại. Cần kiểm tra lại bằng lệnh `git cli 2.45+, github cloud (conventional commits, git flow, semantic branching) config --list` hoặc xem file `.git/config` để xác nhận phạm vi.

---

### Câu 2: Phân tích lý do tại sao việc sử dụng lệnh gom toàn bộ tệp vào Staging Area mà không kiểm tra trạng thái lại vô tình đưa cả các tệp nhạy cảm (như `.env` hoặc tệp nhật ký tạm) vào mốc snapshot và đề xuất giải pháp cách ly.
> **Gợi ý trả lời & Định hướng đáp án:** Việc gom toàn bộ tệp không kiểm tra dễ đưa các tệp chứa thông tin bảo mật vào kho lưu trữ. Giải pháp là thiết lập tệp cấu hình loại trừ `.gitignore` và rà soát kỹ bằng lệnh kiểm tra trạng thái trước khi commit.

---

### Câu 3: Trích dẫn kịch bản thực thi bị lỗi trong bài đọc, hãy chỉ ra điểm không an toàn khi sử dụng giao thức HTTP cho địa chỉ Remote và viết lại câu lệnh chuyển sang giao thức HTTPS/SSH chuẩn.
> **Gợi ý trả lời & Định hướng đáp án:** Giao thức HTTP không mã hóa dữ liệu truyền tải trên đường truyền. Cần đổi sang giao thức HTTPS hoặc SSH bằng câu lệnh cập nhật URL remote chuẩn doanh nghiệp.

---