### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Thiết kế Quy trình Kiểm soát Phiên bản và Bảo mật Kho chứa Subsystem Đơn hàng E-Commerce — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Trình bày rõ ràng cơ chế vận hành của Phương án A (Staging gộp hàng loạt) và Phương án B (Staging phân tách nguyên tử & cấu hình `.gitignore` đa tầng).
    *   Nêu bật sự khác biệt về cách thức tương tác với 3 vùng dữ liệu Git.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** 
    *   Sử dụng đúng thẻ HTML Table có thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.
    *   So sánh đầy đủ 5 tiêu chí: An toàn bảo mật, Tính nguyên tử lịch sử, Khả năng truy vết lỗi, Dung lượng kho chứa, Chi phí bảo trì.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** 
    *   Đưa ra lý do thuyết phục chọn Phương án B dựa trên đặc thù bảo mật API Key thanh toán và tính kiểm toán dữ liệu E-Commerce.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** 
    *   Trình bày sơ đồ luồng dữ liệu (Flowchart/Pseudocode) mô tả chính xác đường đi của các tệp từ *Working Directory* qua *Staging Area* đến *Local Repository* đối với từng commit cụ thể.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Cấu hình tệp `.gitignore` chuẩn xác:** 
    *   Chặn thành công các tệp bí mật: `.env`, `.env.production.local`.
    *   Chặn thư mục nặng và tệp rác: `node_modules/`, `dist/`, `*.log`.
    *   Sử dụng cú pháp ngoại lệ (Negation Pattern `!/logs/payment-audit.log` hoặc `!logs/payment-audit.log`) để giữ lại tệp audit log chính xác.
*   **[15 điểm] Thực thi chuỗi lệnh Git CLI 2.45+:** 
    *   Cấu hình danh tính global chuẩn xác (`user.name`, `user.email`, `core.editor`, `core.autocrlf`).
    *   Khởi tạo repo (`git init`) và kiểm tra trạng thái (`git status`).
    *   Thực hiện staging từng phần (`git add <path>`) kết hợp ghi nhận commit nguyên tử.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Tuân thủ chuẩn Conventional Commits & Log Output:** 
    *   Tất cả thông điệp commit phải tuân thủ đúng định dạng: `feat(order): ...`, `feat(payment): ...`, `docs(api): ...`.
    *   Kết quả lệnh `git log --oneline` hiển thị lịch sử sạch vẽ thành chuỗi commit rõ ràng, không chứa tệp rác hoặc tệp nhạy cảm.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Chuẩn hóa danh tính & Clean Command workflow:** 
    *   Lệnh CLI được tổ chức mạch lạc, có chú thích giải thích rõ mục đích từng bước bằng Tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài:** 
    *   Tạo đường dẫn thư mục nộp bài chuẩn định dạng: `[Tên Lớp]_[Môn Học]_Session02_Ex04`.

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản Tự động hóa Kiểm chuẩn (Automation Shell Script):** 
    *   Viết kịch bản Bash/Shell tự động kiểm tra xem tệp `.env` hoặc thư mục `node_modules/` có vô tình bị theo dõi bởi Git hay không thông qua kết quả của `git status --porcelain`.