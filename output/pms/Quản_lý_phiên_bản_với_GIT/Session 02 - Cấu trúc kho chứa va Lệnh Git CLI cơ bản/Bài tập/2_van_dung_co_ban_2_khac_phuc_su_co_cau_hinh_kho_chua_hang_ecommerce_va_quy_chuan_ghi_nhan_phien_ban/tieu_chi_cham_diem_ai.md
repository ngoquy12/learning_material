### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Khắc Phục Sự Cố Cấu Hình Kho Chứa Hàng E-Commerce Và Quy Chuẩn Ghi Nhận Phiên Bản — Tổng điểm: 100 điểm**

---

#### **1. Phân tích & Phát hiện lỗi vận hành (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác lỗi:**
    *   Chỉ ra chính xác 3 nhóm lỗi: (1) Cấu hình danh tính & Editor sai cú pháp; (2) Tệp `.gitignore` viết sai dẫn đến rò rỉ `.env` và đẩy `node_modules/` vào Staging Area; (3) Commit message tùy tiện vi phạm Conventional Commits.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:**
    *   Lập bảng báo cáo kiểm thử đủ 3 cột theo yêu cầu, mô tả rõ Input, Buggy Output và Expected Output cho tối thiểu 3 trường hợp lỗi cụ thể.

---

#### **2. Thao tác khắc phục sự cố & Lệnh thực thi — 40 điểm**
*   **[20 điểm] Thao tác đúng lệnh nghiệp vụ:**
    *   Thực hiện đúng chuỗi lệnh cấu hình danh tính toàn cục:
        *   `git config --global user.name "Tran Van Dev"`
        *   `git config --global user.email "dev.tran@company.com"`
        *   `git config --global core.editor "code --wait"`
        *   `git config --global core.autocrlf true`
*   **[20 điểm] Xử lý tình huống hệ thống:**
    *   Chỉnh sửa tệp `.gitignore` chuẩn hóa với đầy đủ các mẫu loại trừ: `node_modules/`, `.env`, `dist/`, `*.log`, `.DS_Store`, `.vscode/`.
    *   Đưa các tệp rác và tệp nhạy cảm ra khỏi Staging Area an toàn, chỉ giữ lại các tệp mã nguồn chuẩn (`.gitignore`, `package.json`, `src/order/checkout.js`).

---

#### **3. Kiểm chuẩn quy trình & Trạng thái hệ thống — 20 điểm**
*   **[10 điểm] Validate cấu hình cơ bản:**
    *   Truy vấn danh sách cấu hình toàn cục bằng `git config --global --list` và xác nhận tất cả các tham số đều đạt chuẩn.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:**
    *   Thực hiện lệnh ghi nhận commit tuân thủ đúng chuẩn Conventional Commits với tiền tố hợp lệ (`feat(order): ...` hoặc `feat(checkout): ...`).
    *   Kiểm tra nhật ký bằng `git log --oneline` để xác thực mã commit và thông điệp lưu vết chuẩn mực.

---

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:**
    *   Giải thích ngắn gọn hậu quả của việc đưa tệp `.env` chứa bí mật thanh toán vào kho chứa mã nguồn sản xuất và tại sao cần tham số `--wait` khi cấu hình `core.editor`.

---

#### **5. Chất lượng quy trình và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Nhật ký thao tác sạch:**
    *   Các câu lệnh Git CLI trình bày rõ ràng, không thừa lệnh lỗi, định dạng mã lệnh chuẩn xác.
*   **[5 điểm] Tuân thủ nộp bài GitHub:**
    *   Đẩy mã nguồn lên kho chứa GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session02_Ex02`.

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tự động hóa quy trình:**
    *   Viết kịch bản Bash shell (`check_git_env.sh`) tự động kiểm tra xem cấu hình `user.name`, `user.email`, `core.editor` đã đúng và tệp `.env` đã được loại trừ bởi `.gitignore` hay chưa.