# <center>[Sáng tạo 3] Thiết kế Module Đóng gói Quản lý Đặt vé và Kiểm soát QR Check-in Sự kiện Ca nhạc</center>

### **1. Mục tiêu**
*   Vận dụng sáng tạo cú pháp **Arrow Function ES6**, **Tham số mặc định (Default Parameters)** và cơ chế **Closure / Lexical Scope** để thiết kế module đóng gói trạng thái dữ liệu an toàn (Private State).
*   Chủ động phân tích và giải quyết bài toán quản lý đặt vé sự kiện âm nhạc thuộc hệ thống Ticketbox, áp dụng đúng các quy tắc nghiệp vụ thực tế như chiết khấu vé Early Bird, giới hạn số lượng vé mua trên mỗi tài khoản và kiểm soát mã QR check-in 1 lần.
*   Tự thiết kế cấu trúc dữ liệu I/O, dự báo các kịch bản lỗi biên (Edge Cases), vẽ sơ đồ luồng dữ liệu bằng Mermaid và viết mã nguồn hoàn chỉnh không sử dụng biến toàn cục.

### **2. Bối cảnh & Vấn đề**
Hệ thống bán vé sự kiện ca nhạc và hội thảo Ticketbox đang gặp sự cố nghiêm trọng trong quá trình vận hành đêm diễn concert lớn: danh sách vé đặt và trạng thái mã QR check-in đang lưu trữ bằng các biến toàn cục (Global Variables). Điều này khiến lập trình viên ở các phân hệ khác dễ dàng can thiệp, làm thay đổi dữ liệu vé hoặc cho phép 1 mã QR có thể quét check-in nhiều lần tại cổng soát vé.

Ban tổ chức yêu cầu tái cấu trúc toàn bộ logic đặt vé và soát vé thành một module độc lập. Module này phải đóng gói dữ liệu vé bên trong Scope của một Closure, chỉ cung cấp các phương thức thao tác an toàn thông qua Arrow Functions, tự động áp dụng giá trị mặc định cho phí dịch vụ và ngăn chặn tuyệt đối các hành vi truy cập hoặc sửa đổi trái phép từ bên ngoài.

### **3. Quy tắc nghiệp vụ**
1.  **Đóng gói trạng thái (State Encapsulation):** Danh sách vé (`tickets`) và trạng thái doanh thu phải được bảo mật hoàn toàn bên trong Closure. Không biến toàn cục nào được phép truy cập trực tiếp vào mảng dữ liệu này.
2.  **Hạn ngạch đặt vé (Ticket Quota):** Mỗi khách hàng (xác định qua `customerId`) chỉ được mua tối đa 4 vé cho 1 sự kiện. Nếu tổng số vé mua đăng ký cộng với số vé đã mua trước đó vượt quá 4, hệ thống phải từ chối đơn hàng.
3.  **Chiết khấu & Phí mặc định (Early Bird & Default Service Fee):**
    *   Vé thuộc đợt mở bán sớm (`isEarlyBird = true`) được chiết khấu 15% trên giá vé niêm yết của khu vực (Zone A, VIP, GA).
    *   Hàm tính toán tổng tiền phải hỗ trợ phí dịch vụ mặc định là 20.000 VNĐ/vé nếu người gọi hàm không truyền giá trị này.
4.  **Kiểm soát check-in 1 lần (Single-use QR Verification):** Mã QR check-in được tạo ra khi đặt vé thành công có trạng thái ban đầu là `PENDING`. Khi quét check-in tại cổng, trạng thái đổi thành `CHECKED_IN`. Nếu cùng một mã QR được quét lần thứ 2, hệ thống phải cảnh báo mã không hợp lệ hoặc đã qua cổng.

### **4. Yêu cầu bài toán**
Học viên đóng vai trò là Kiến trúc sư phần mềm (Lead Architect) để tự xây dựng giải pháp từ đầu theo 4 phần bắt buộc sau:

*   **Phần 1: Tự thiết kế I/O Schema (Request / Response Data Structures)**
    *   Tự xác định cấu trúc dữ liệu đầu vào cho thao tác đặt vé `purchaseTickets(...)` và thao tác check-in `scanQrCode(...)`.
    *   Định hình cấu trúc dữ liệu trả về (Response Object) cho từng hành động bao gồm trạng thái thành công, thông báo lỗi, mã QR generated và chi tiết số tiền.
*   **Phần 2: Phân tích Kịch bản lỗi biên (Edge Cases)**
    *   Tự liệt kê tối thiểu 3 bẫy dữ liệu hoặc kịch bản xung đột trạng thái (ví dụ: mua vé vượt hạn ngạch 4 vé, quét mã QR chưa tồn tại, quét lại mã QR đã check-in, truyền phí dịch vụ bằng 0).
*   **Phần 3: Sơ đồ luồng dữ liệu (Data Flow Diagram với Mermaid)**
    *   Vẽ sơ đồ Mermaid minh họa toàn bộ vòng đời từ lúc khách hàng khởi tạo đơn hàng, tính tiền (áp dụng Early Bird & phí dịch vụ mặc định), lưu vào Closure state, phát hành mã QR cho đến khi quét check-in thành công tại cổng soát vé.
    *   *Yêu cầu tuân thủ đúng 5 dạng hình chuẩn:* Terminator `([ ])`, Input/Output `[/ /]`, Decision `{ }` hoặc `Kiểm tra?`, Process `[" "]`, Flowline `-->`.
*   **Phần 4: Hiện thực hóa mã nguồn (Implementation)**
    *   Viết chương trình JavaScript Vanilla (ES6+) hoàn chỉnh từ đầu.
    *   Sử dụng Closure kết hợp Arrow Functions và Default Parameters để đóng gói và quản lý logic.
    *   Tự tạo dữ liệu thử nghiệm để chứng minh module hoạt động chính xác theo đúng các quy tắc nghiệp vụ và các bẫy lỗi biên đã đề xuất.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Mermaid Diagram) và mã nguồn triển khai trong file giải bài tập.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex15`.
    Ví dụ: `HNKS25CNTT1_Core_Session14_Ex15`
