### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Khắc phục sự cố cấu hình danh tính và quản lý loại trừ tệp trong kho chứa E-Commerce — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi vận hành (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác lỗi:** Chỉ ra tối thiểu 3 lỗi gồm: (1) Cú pháp `user.name` thiếu ngoặc kép và email sai chuẩn doanh nghiệp; (2) Trình soạn thảo `core.editor` thiếu cờ `--wait`; (3) Tệp `.gitignore` viết sai mẫu pattern làm lọt tệp `.env` và `node_modules/`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện bảng HTML tối thiểu 3 test cases phân tích rõ thao tác lỗi, hậu quả hệ thống và kết quả sửa đổi kỳ vọng.

#### **2. Thao tác khắc phục sự cố & Lệnh thực thi — 40 điểm**
*   **[20 điểm] Thao tác đúng lệnh nghiệp vụ:**
    *   Cấu hình đúng danh tính toàn cục: `git config --global user.name "Nguyen Van Dev"`, `git config --global user.email "dinh.nguyen@shopmall.com"`, `git config --global core.editor "code --wait"`, `git config --global core.autocrlf true`.
    *   Tạo/Sửa tệp `.gitignore` khai báo chính xác `node_modules/`, `dist/`, `.env`, `.env.*.local`, `*.log`.
*   **[20 điểm] Xử lý tình huống hệ thống:** Loại bỏ các tệp nhạy cảm/tệp rác khỏi Staging Area, kiểm tra trạng thái bằng `git status` trước khi tiến hành commit.

#### **3. Kiểm chuẩn quy trình & Trạng thái hệ thống — 20 điểm**
*   **[10 điểm] Validate cấu hình cơ bản:** Sử dụng `git config --global --list` kiểm tra chính xác toàn bộ danh tính và thuộc tính cấu hình đã được lưu trữ thành công.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo tệp chứa mật khẩu `.env` và thư mục `node_modules/` không còn nằm trong danh sách theo dõi (Tracked Files) hay Staging Area. Commit lịch sử đúng định dạng Conventional Commits (`chore(...)`, `feat(...)`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao tham số `--wait` lại bắt buộc khi dùng VS Code làm editor trong Git CLI, và hậu quả của việc lọt tệp `.env` lên kho chứa là gì.

#### **5. Chất lượng quy trình và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Nhật ký thao tác sạch:** Thao tác các câu lệnh Git CLI chính xác, không phát sinh lỗi cú pháp hệ thống.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy báo cáo và mã nguồn lên GitHub theo đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session02_Ex01`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tự động hóa quy trình:** Viết một đoạn kịch bản Shell (`setup_env.sh` hoặc `setup_env.ps1`) tự động kiểm tra và cài đặt lại toàn bộ `git config` chuẩn cho nhân viên mới chỉ bằng 1 cú nhấp lệnh.