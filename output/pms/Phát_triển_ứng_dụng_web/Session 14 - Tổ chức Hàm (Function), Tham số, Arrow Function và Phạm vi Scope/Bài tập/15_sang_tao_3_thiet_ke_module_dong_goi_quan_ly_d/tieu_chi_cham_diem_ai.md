### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết kế Module Đóng gói Quản lý Đặt vé và Kiểm soát QR Check-in Sự kiện Ca nhạc — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ, rõ ràng các thuộc tính đầu vào/đầu ra cho hàm đặt vé và hàm kiểm soát check-in QR mà không cần gợi ý mã.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phân tích và mô tả chi tiết tối thiểu 3 kịch bản lỗi biên thực tế (ví dụ: cộng dồn số vé quá 4 vé/tài khoản qua nhiều lần mua, truyền giá trị phí dịch vụ bằng 0, quét mã QR trùng lặp, mã sự kiện không tồn tại).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid đúng cú pháp, thể hiện rõ các bước xử lý từ khởi tạo Closure, tính toán giá trị, đóng gói trạng thái private đến xác thực check-in.
*   **[10 điểm] Tuân thủ quy chuẩn hình họa Mermaid:** Sử dụng đúng 5 dạng hình chuẩn theo yêu cầu (Terminator `([ ])`, Input/Output `[/ /]`, Process `[" "]`, Decision Diamond, Flowline).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai Closure & Arrow Functions đóng gói dữ liệu:** Sử dụng hàm tạo Closure (`createTicketManager` hoặc tương đương) để giấu kín biến trạng thái `tickets`, trả về các phương thức dạng Arrow Function nhằm thao tác với dữ liệu mà không bị rò rỉ scope.
*   **[15 điểm] Triển khai đúng các quy tắc nghiệp vụ:**
    *   Tính đúng chiết khấu Early Bird (giảm 15%).
    *   Áp dụng tham số mặc định cho phí dịch vụ (20.000 VNĐ) một cách an toàn.
    *   Kiểm soát hạn ngạch tối đa 4 vé/tài khoản.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xây dựng mã nguồn kiểm tra dữ liệu chặt chẽ (Guard Clauses), trả về thông báo lỗi rõ ràng khi phát hiện vi phạm hạn ngạch hoặc quét trùng mã QR.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Standard Naming:** Đặt tên biến và hàm bằng tiếng Anh chuẩn camelCase, comment giải thích bằng Tiếng Việt có dấu đầy đủ, tuyệt đối không sử dụng biến toàn cục hoặc từ khóa bị cấm.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo cấu trúc thư mục đúng định dạng quy định `[Tên Lớp]_[Môn Học]_Session14_Ex15`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Auditing / Nhật ký thao tác:** Triển khai thêm phương thức private ghi lại lịch sử các lượt quét QR thất bại (mã không tồn tại, mã đã dùng) hoặc phương thức thống kê tổng doanh thu thực tế được đóng gói an toàn trong Closure.