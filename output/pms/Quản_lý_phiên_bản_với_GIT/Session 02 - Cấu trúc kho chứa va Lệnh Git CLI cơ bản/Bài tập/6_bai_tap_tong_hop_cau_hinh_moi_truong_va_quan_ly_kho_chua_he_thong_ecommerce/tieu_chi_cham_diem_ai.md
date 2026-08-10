### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Cấu hình môi trường và quản lý kho chứa hệ thống E-Commerce — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu hình Git CLI:** Thực hiện đầy đủ các câu lệnh thiết lập danh tính `user.name="Dev ECommerce"`, `user.email="dev.ecommerce@scart.vn"`, trình soạn thảo `core.editor="code --wait"`, và cấu hình `core.autocrlf` chính xác trên hệ điều hành tương ứng.
*   **[10 điểm] Xây dựng Cấu trúc thư mục kho chứa dự án E-Commerce:** Khởi tạo kho chứa cục bộ hợp lệ tại thư mục `ecommerce-order-system` và tạo đầy đủ các thư mục/tệp tin theo yêu cầu (`src/`, `docs/`, `logs/`, `dist/`, `.env`, `.env.production`).

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Chức năng Đọc/Xem trạng thái và Lịch sử kho chứa:** Thực thi đúng cú pháp các lệnh kiểm tra trạng thái `git status` và câu lệnh truy vấn nhật ký một dòng `git log --oneline` để xác minh dữ liệu.
*   **[20 điểm] Chức năng Ghi/Thêm mới phiên bản Commit:** Thực hiện thành công 4 lượt commit riêng biệt tương ứng với từng giai đoạn phát triển, ghi nhận đúng snapshot các tệp vào Local Repository.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Xử lý loại trừ tệp nhạy cảm và tệp rác (.gitignore):** Định nghĩa chính xác các quy tắc loại trừ trong `.gitignore` để ngăn chặn việc theo dõi các tệp chứa bí mật dịch vụ (`.env*`), tệp đóng gói (`dist/`), và tệp tạm hệ thống.
*   **[10 điểm] Xử lý ngoại lệ trong .gitignore:** Cấu hình chuẩn xác cú pháp phủ định `!logs/audit_trail.log` để đảm bảo tệp nhật ký kiểm toán không bị chặn bởi quy tắc `logs/*.log`.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra và tuân thủ chuẩn Conventional Commits:** Toàn bộ 4 thông điệp commit phải tuân thủ nghiêm ngặt cấu trúc `type(scope): description` với các tiền tố `chore(config)`, `docs(api)`, `feat(order)`, `fix(payment)`, không chứa ký tự emoji hay từ ngữ không chuẩn mực.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub tuân thủ đúng tên thư mục quy định `[Tên Lớp]_[Môn Học]_Session02_Ex06`.