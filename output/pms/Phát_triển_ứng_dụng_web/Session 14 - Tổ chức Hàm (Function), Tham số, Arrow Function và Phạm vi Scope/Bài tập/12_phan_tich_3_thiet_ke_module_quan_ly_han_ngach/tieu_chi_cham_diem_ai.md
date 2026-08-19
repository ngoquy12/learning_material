### **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Thiết kế Module Quản lý Hạn ngạch và Tính giá Vé Sự kiện Ca nhạc — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Tự đề xuất 2 giải pháp khác biệt về mặt cấu trúc lưu trữ trạng thái và cú pháp khai báo hàm (ví dụ: Giải pháp 1 dùng Global Variables + Function Declaration; Giải pháp 2 dùng Closure Scope + Arrow Functions + ES6 Default Parameters).
    *   Phân tích ưu/nhược điểm kiến trúc của từng giải pháp rõ ràng, không trùng lặp.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Tạo bảng HTML/Markdown đầy đủ 5 tiêu chí: Tốc độ thực thi, Bộ nhớ, Tính đóng gói, Độ đọc hiểu, Khả năng mở rộng.
    *   Bảng HTML phải chứa thuộc tính chuẩn: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lập luận thuyết phục vì sao chọn giải pháp Closure + Arrow Function + Default Parameters cho môi trường Production của hệ thống Ticketbox (tránh race condition, an toàn bộ nhớ, cú pháp hiện đại).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu (Mermaid):**
    *   Vẽ sơ đồ Mermaid đúng chuẩn 5 hình khối: Oval `([...])` cho Start/End, Hình bình hành `[/.../]` cho Input/Output, Hình chữ nhật `["..."]` cho Process, Hình thoi `...` cho Decision.
    *   Luồng logic thể hiện đầy đủ các bước kiểm tra hạn ngạch $N + \text{vé đã mua} \le 4$, tính giảm giá Early Bird, tính thuế VAT và phí dịch vụ.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code JavaScript:**
    *   Khởi tạo hàm đóng gói bằng Closure (ví dụ `createTicketManager(maxQuota = 4)`), chứa biến private đếm số vé đã mua.
    *   Áp dụng Arrow Function và ES6 Default Parameters đúng cú pháp cho logic tính toán thanh toán (`taxRate = 0.08`, `serviceFee = 20000`, `isEarlyBird = false`).
    *   Thực hiện return đúng đối tượng chứa các phương thức xử lý (như `buyTickets`, `getPurchasedCount`).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Từ chối và báo lỗi nếu `quantity` không phải số nguyên dương ($N \le 0$ hoặc `!Number.isInteger(quantity)`).
    *   Từ chối và báo lỗi nếu `basePrice` $\le 0$.
    *   Từ chối giao dịch và giữ nguyên số vé đã mua nếu vượt quá hạn ngạch 4 vé.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Kết quả trả về khi mua vé thành công phải dạng Object hoặc chuỗi thông báo rõ ràng gồm: Số vé vừa mua, Số tiền thanh toán thực tế, Số vé còn lại được phép mua.
    *   Định dạng dữ liệu chính xác, không thừa hoặc thiếu trường thông tin.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Sử dụng tên biến/hàm 100% bằng tiếng Anh chuẩn camelCase (ví dụ: `calculateTicketPrice`, `purchasedCount`, `remainingQuota`).
    *   Mã nguồn sạch đẹp, có chú thích bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đúng cấu trúc thư mục GitHub: `[Tên Lớp]_[Môn Học]_Session14_Ex12`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script / Kịch bản kiểm thử độc lập:**
    *   Viết kịch bản khởi tạo 2 instance khách hàng độc lập từ Closure để chứng minh tính cô lập dữ liệu (Scope Isolation) giữa 2 tài khoản mua vé khác nhau.