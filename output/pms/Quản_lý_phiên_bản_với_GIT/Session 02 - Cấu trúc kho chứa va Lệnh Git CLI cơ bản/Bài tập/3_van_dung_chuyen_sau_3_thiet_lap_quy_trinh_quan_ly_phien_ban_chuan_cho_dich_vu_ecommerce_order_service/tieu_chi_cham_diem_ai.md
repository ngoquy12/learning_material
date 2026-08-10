### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu 3] Thiết lập quy trình quản lý phiên bản chuẩn cho dịch vụ E-commerce Order Service — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Trình bày chi tiết bảng tham số đầu vào (cờ lệnh, tên tệp, cấu hình) và kết quả hiển thị mong đợi (Output status, log hash) cho từng bước trong quy trình Git CLI.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Vẽ sơ đồ hoặc viết giả mã phân tích rõ sự dịch chuyển dữ liệu qua 3 vùng (Working Directory, Staging Area, Local Repository) và cơ chế đánh giá tệp của `.gitignore` trước khi thực hiện `git add`.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khởi tạo kho chứa cục bộ thành công bằng `git init`, dựng đầy đủ cây cấu trúc tệp mô phỏng dự án thương mại điện tử đúng yêu cầu bài toán.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Cấu hình danh tính toàn cục (`user.name`, `user.email`, `core.editor`, `core.autocrlf`) chuẩn xác và kiểm tra thành công bằng `git config --global --list`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Viết tệp `.gitignore` chính xác, chặn thành công các tệp nhạy cảm (`.env.production`), tệp biên dịch trung gian (`dist/`) và thư mục phụ thuộc nặng (`node_modules/`).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Xử lý thành công quy tắc ngoại lệ phức tạp `!/logs/audit-transactions.log` để giữ lại tệp nhật ký kiểm toán giao dịch trong khi vẫn loại trừ tất cả tệp `*.log` khác. Kiểm tra và xác minh trạng thái bằng `git status`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Ghi nhận đủ 4 commit độc lập tuân thủ 100% quy chuẩn Conventional Commits (`chore`, `feat`, `fix`, `docs`) bằng tiếng Việt có dấu, không bị vi phạm cú pháp hay thiếu phạm vi (scope). Kiểm tra khớp bằng `git log --oneline`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tổ chức thư mục dự án gọn gàng, đặt tên tệp tiếng Anh chuẩn mực, cấu trúc tệp `.gitignore` có nhóm dòng và ghi chú phân loại rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** Nộp bài đúng thời hạn, cấu hình thư mục lưu trữ mã nguồn chuẩn định dạng `[Tên Lớp]_[Môn Học]_Session02_Ex03`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Phân tích được sự khác biệt giữa cấu hình Local Scope (`git config --local`) và Global Scope (`git config --global`) khi quản lý nhiều dự án e-commerce trên cùng một máy trạm phát triển.