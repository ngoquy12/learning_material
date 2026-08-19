# <center>[Phân tích 1] Phân Tích Và Thiết Kế Bộ Xử Lý Đặt Vé Sự Kiện Vấn Đề Phạm Vi Biến Và Hạn Ngạch Check-in</center>

### **1. Mục tiêu**
*   **Đánh giá và so sánh kiến trúc hàm trong JavaScript ES6+**: Phân tích sự khác biệt về khả năng đóng gói dữ liệu, phạm vi biến (Scope) và hiệu năng giữa các kỹ thuật tổ chức hàm (Function Declaration, Arrow Function, Closure).
*   **Áp dụng Tham số mặc định (Default Parameters)**: Thiết kế các hàm tính toán chiết khấu và tổng chi phí đặt vé an toàn, loại bỏ triệt để các lỗi logic do thiếu dữ liệu đầu vào hoặc lỗi ép kiểu từ toán tử logic cũ.
*   **Xây dựng bộ quản lý hạn ngạch vé an toàn (State Encapsulation)**: Triển khai mô hình Closure đóng gói trạng thái vé tồn kho và hạn ngạch lượt mua cho hệ thống bán vé Ticketbox, ngăn chặn việc biến bị ghi đè ngẫu nhiên từ Global Scope.

### **2. Bối cảnh & Vấn đề**
Hệ thống bán vé sự kiện ca nhạc trực tuyến **Ticketbox** vừa mở bán vé cho đêm diễn âm nhạc quy mô lớn. Trong đợt cao điểm mở bán vé Zone VIP, hệ thống liên tục gặp phải các sự cố nghiêm trọng:

1.  **Sự cố ghi đè dữ liệu kho vé (Global Scope Pollution)**: Số lượng vé còn lại của Zone VIP được lưu dưới dạng một biến toàn cục. Khi tích hợp một thư viện tiện ích từ bên thứ ba, thư viện này vô tình khai báo trùng tên biến và ghi đè giá trị về 0, làm cho hàng ngàn khách hàng không thể tiếp tục đặt vé mặc dù thực tế kho vé vẫn còn.
2.  **Sự cố sai lệch tính tiền hóa đơn (Default Parameter Logic Error)**: Hàm tính toán tổng tiền đặt vé sử dụng cách kiểm tra tham số mặc định cũ dạng `serviceFee = serviceFee || 20000`. Khi ban tổ chức tung ra chương trình "Miễn phí dịch vụ xuất vé" bằng cách truyền `serviceFee = 0`, toán tử `||` đã hiểu sai giá trị `0` là *falsy* và tự động ép về giá trị mặc định `20000`, dẫn đến việc khách hàng bị tính thừa tiền.
3.  **Vi phạm quy tắc hạn ngạch đơn hàng**: Mỗi tài khoản chỉ được phép mua tối đa 4 vé cho một lượt giao dịch. Tuy nhiên, logic kiểm tra trước đây nằm phân rải ở nhiều nơi và không có cơ chế khóa trạng thái (encapsulation), khiến nhiều truy vấn đồng thời vượt qua được hàng rào kiểm tra.

### **3. Quy tắc nghiệp vụ**
Hệ thống quản lý đặt vé sự kiện phải tuân thủ nghiêm ngặt các quy định nghiệp vụ sau:

*   **Quy tắc 1: Giới hạn hạn ngạch vé mua/lượt giao dịch**:
    *   Mỗi đơn đặt vé (`CustomerOrder`) chỉ cho phép mua từ **1 đến 4 vé**.
    *   Tham số `ticketQuantity` nếu bị khuyết (không truyền) sẽ tự động nhận giá trị mặc định là `1`.
    *   Nếu số lượng vé yêu cầu nhỏ hơn 1 hoặc lớn hơn 4, hàm xử lý phải từ chối giao dịch và trả về thông báo lỗi cụ thể.
*   **Quy tắc 2: Công thức tính toán tổng giá trị hóa đơn**:
    *   Công thức: `Tổng tiền = (Số lượng vé * Giá vé niêm yết * (1 - Tỷ lệ chiết khấu)) + Phí dịch vụ`.
    *   Giá vé niêm yết Zone VIP (`basePrice`) mặc định là `2,000,000 VND`.
    *   Tỷ lệ chiết khấu Early Bird (`discountRate`): Mặc định là `0.15` (giảm 15%) nếu khách hàng đặt vé trong thời gian ưu đãi (`isEarlyBird = true`). Nếu không áp dụng Early Bird (`isEarlyBird = false`), tỷ lệ chiết khấu mặc định là `0`.
    *   Phí dịch vụ xuất vé (`serviceFee`): Mặc định là `30,000 VND`. Trường hợp truyền giá trị `0`, hệ thống phải giữ nguyên giá trị `0` (không được tự động ép về `30,000`).
*   **Quy tắc 3: Đóng gói và bảo vệ trạng thái kho vé (State Encapsulation)**:
    *   Biến lưu trữ số lượng vé còn lại (`remainingTickets`) của một Zone sự kiện phải được cô lập hoàn toàn trong Lexical Scope (không xuất lộ ra Global Scope).
    *   Bên ngoài chỉ có thể tương tác với kho vé thông qua các phương thức được cung cấp từ Closure (ví dụ: đặt vé, kiểm tra số vé còn lại).
    *   Nếu số vé yêu cầu mua vượt quá số vé hiện có trong kho, giao dịch phải bị hủy bỏ và số lượng vé kho không được thay đổi.

### **4. Yêu cầu bài toán**
Với vai trò là Kiến trúc sư phần mềm Frontend, bạn hãy thực hiện đầy đủ 3 phần công việc sau:

#### **Phần 1: Báo cáo Đề xuất Đa Giải pháp & Phân tích Trade-off**
*   Tự đề xuất ít nhất **2 giải pháp kỹ thuật khác nhau** từ sơ khai đến tối ưu để tổ chức hàm tính toán chiết khấu và quản lý trạng thái kho vé.
*   Phân tích ưu/nhược điểm cấu trúc của từng giải pháp (nêu rõ việc xử lý Scope, Hoisting, Arrow Function và Tham số mặc định).
*   Xây dựng bảng so sánh Trade-off trực quan giữa các giải pháp dựa trên **5 tiêu chí**:
    1. Tốc độ xử lý thực thi (Speed).
    2. Chi phí tiêu tốn bộ nhớ Stack/Heap (Memory).
    3. Khả năng bảo trì & mở rộng mã nguồn (Maintainability).
    4. Độ rõ ràng và dễ đọc của code (Readability).
    5. Mức độ phù hợp với môi trường sản xuất tải cao (Suitability).

#### **Phần 2: Giải trình Lựa chọn & Thiết kế Mã giả / Lưu đồ**
*   Đưa ra lý giải khoa học thuyết phục về việc lựa chọn giải pháp tối ưu nhất cho hệ thống Ticketbox.
*   Vẽ lưu đồ thuật toán (Mermaid Flowchart) hoặc viết mã giả (Pseudocode) mô tả chi tiết luồng xử lý từ khi nhận yêu cầu đặt vé, kiểm tra hạn ngạch, tính chiết khấu Early Bird đến khi trừ kho vé an toàn.
*   *Lưu ý đối với Mermaid Flowchart*: Phải tuân thủ đúng 5 hình khối chuẩn (Hình thoi cho điều kiện `Kiểm tra?`, Hình chữ nhật `["Thực hiện hành động"]` cho tính toán, Hình bo tròn `([Bắt đầu/Kết thúc])`, Hình bình hành `[/Đầu vào/Đầu ra/]`).

#### **Phần 3: Triển khai Mã nguồn & Chặn Lỗi Biên**
*   Viết mã nguồn JavaScript ES6+ hoàn chỉnh hiện thực hóa giải pháp tối ưu đã chọn.
*   Sử dụng Arrow Function, ES6 Default Parameters và Closure để đóng gói biến.
*   Chặn toàn bộ các lỗi biên (Edge Cases): truyền số lượng vé âm/vượt quá 4, truyền thiếu tham số, số vé yêu cầu vượt quá tồn kho, truyền `serviceFee = 0`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex10`.
    Ví dụ: `HNKS25CNTT1_Core_Session14_Ex10`
