### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Xây dựng quy trình khởi tạo và kiểm soát phiên bản an toàn cho dự án E-commerce Marketplace — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc Repository & Config Schema:** Xây dựng bảng thiết lập cấu hình Git CLI đầy đủ các thông số (`user.name`, `user.email`, `core.editor`, `core.autocrlf`) kèm mô tả thư mục kiến trúc dự án E-commerce hợp lý.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Nhận diện đúng tối thiểu 3 rủi ro thực tế (rò rỉ secret key `.env`, xung đột `CRLF`/`LF` ảnh hưởng checksum mã nguồn, lọt tệp rác `node_modules` hay `.DS_Store`) và đưa ra giải pháp xử lý triệt để.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ thành công sơ đồ Mermaid thể hiện chuẩn xác luồng di chuyển tệp qua 3 vùng (Working Directory, Staging Area, Local Repository DAG) và vị trí can thiệp của bộ lọc `.gitignore`.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ cơ chế chuyển đổi trạng thái của tệp từ `Untracked` $\rightarrow$ `Staged` $\rightarrow$ `Committed (Unmodified)`.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công chuỗi lệnh Git CLI:** Viết và thực thi chính xác chuỗi câu lệnh khởi tạo (`git init`), cấu hình (`git config`), kiểm tra (`git status`), đưa vào staging (`git add`), commit (`git commit`) và truy vấn nhật ký (`git log --oneline`).
*   **[15 điểm] Triển khai tệp loại trừ .gitignore nâng cao:** Xây dựng tệp `.gitignore` chính xác cho dự án E-commerce Web Framework, chặn đủ các loại tệp nhạy cảm/tệp rác và cấu hình đúng cú pháp ngoại lệ `!/logs/system-audit.log`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Đảm bảo sau khi thực thi kịch bản, các tệp nhạy cảm và tệp rác không bị lọt vào vùng Staging Area hay Local Repository khi kiểm tra bằng `git status`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Chuẩn hóa thông điệp Conventional Commits:** 100% thông điệp commit tuân thủ đúng cú pháp `<type>(<scope>): <description>` bằng tiếng Việt có dấu chuẩn xác (hoặc tiếng Anh chuyên ngành).
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo cấu trúc thư mục nộp bài chuẩn theo đúng tên mẫu `[Tên Lớp]_[Môn Học]_Session02_Ex05` và trình bày báo cáo rõ ràng.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai kịch bản Automation CLI Verification:** Viết được kịch bản shell/bash tự động kiểm tra trạng thái kho chứa, kiểm tra giá trị danh tính `git config --list` và xuất ra báo cáo định dạng log hệ thống chuẩn mực.