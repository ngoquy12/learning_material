# <center>[Phân tích 3] Thiết kế Module Quản lý Hạn ngạch và Tính giá Vé Sự kiện Ca nhạc</center>

### **1. Mục tiêu**
*   **Tổ chức kiến trúc hàm chuyên nghiệp:** Phân tích và vận dụng linh hoạt giữa Khai báo hàm truyền thống (Function Declaration) và Cú pháp hàm mũi tên (Arrow Function) kết hợp Tham số mặc định (Default Parameters).
*   **Quản lý phạm vi biến và đóng gói dữ liệu (Scope & Closure):** Triển khai kỹ thuật Closure để bảo toàn trạng thái hạn ngạch mua vé của từng khách hàng, ngăn chặn việc biến bị ghi đè hoặc truy cập trái phép từ Scope toàn cục (Global Scope).
*   **Tư duy phân tích đa giải pháp:** So sánh các phương án thiết kế phần mềm dựa trên các tiêu chí kỹ thuật (Hiệu năng, Bộ nhớ, Tính đóng gói, Độ đọc hiểu và Khả năng bảo trì) để lựa chọn kiến trúc tối ưu cho hệ thống bán vé trực tuyến.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống bán vé sự kiện âm nhạc Ticketbox, việc kiểm soát hạn ngạch mua vé của mỗi tài khoản và tính toán tổng tiền thanh toán là hai chức năng cốt lõi. Mỗi đêm diễn ca nhạc có quy định nghiêm ngặt: một tài khoản chỉ được phép mua tối đa **4 vé** để tránh tình trạng "phe vé" (gồm cả các giao dịch mua thành công trước đó).

Đội ngũ kỹ thuật hiện tại đang gặp phải thách thức lớn khi xây dựng module này:
1. **Lỗi đè dữ liệu phạm vi toàn cục (Global State Collision):** Sử dụng các biến toàn cục để lưu số lượng vé đã mua dẫn đến việc khi nhiều khách hàng cùng thực hiện giao dịch, dữ liệu đếm bị ghi đè lẫn nhau.
2. **Lặp lại logic tính toán và sai lệch tham số:** Công thức tính tổng tiền vé (bao gồm giá gốc, chiết khấu vé Early Bird 15%, thuế VAT mặc định 8%, phí dịch vụ mặc định 20.000 VNĐ) chưa được đóng gói chuẩn xác, dẫn đến lỗi tính toán khi người dùng không truyền đủ tham số đầu vào.

Bạn được giao nhiệm vụ phân tích kiến trúc, đề xuất ít nhất 2 phương án kỹ thuật và triển khai giải pháp tối ưu bằng JavaScript (ES6+).

### **3. Quy tắc nghiệp vụ**
1. **Quy tắc hạn ngạch mua vé (Purchase Quota Rule):**
   * Giới hạn tối đa cho một tài khoản là **4 vé** (`MAX_LIMIT = 4`).
   * Khi khách hàng yêu cầu mua `N` vé: Nếu $(Số vé đã mua hiện tại + N) > 4$, hệ thống phải từ chối giao dịch, trả về thông báo lỗi và **không** cập nhật số lượng vé đã mua.
   * Nếu giao dịch hợp lệ, số vé đã mua hiện tại sẽ được cộng thêm `N` và trả về số vé còn lại có thể mua tiếp.
2. **Quy tắc tính toán giá vé (Pricing Rule):**
   * **Giá cơ bản sau giảm (Discounted Base Price):** Nếu là đợt bán Early Bird (`isEarlyBird = true`), giá mỗi vé giảm 15% so với giá niêm yết (`basePrice * 0.85`). Ngược lại giữ nguyên `basePrice`.
   * **Thuế VAT:** Áp dụng tỷ lệ thuế mặc định là `8%` (`taxRate = 0.08`) trên giá mỗi vé sau giảm.
   * **Phí dịch vụ:** Phí cố định mặc định là `20,000 VNĐ` (`serviceFee = 20000`) trên mỗi vé.
   * **Tổng thanh toán cho 1 đơn hàng:** $Tổng tiền = (Giá vé sau giảm + Thuế VAT trên 1 vé + Phí dịch vụ) * Số lượng vé$.
3. **Quy tắc an toàn dữ liệu (Encapsulation Rule):**
   * Biến lưu trữ số vé đã mua của mỗi tài khoản tuyệt đối không được truy cập hoặc chỉnh sửa trực tiếp từ Global Scope.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off (Độc lập đề xuất)**
1. Tự thiết kế và mô tả chi tiết ít nhất **2 giải pháp kỹ thuật khác nhau** để giải quyết bài toán trên (Ví dụ: Một giải pháp sử dụng biến toàn cục/hàm truyền thống và một giải pháp sử dụng Arrow Function kết hợp Closure & Default Parameters).
2. Xây dựng **Bảng so sánh Trade-off** giữa các giải pháp dựa trên 5 tiêu chí kỹ thuật:
   * Tốc độ thực thi (Speed / Execution Time).
   * Mức độ tiêu tốn bộ nhớ (Memory Overhead).
   * Tính đóng gói & Bảo mật biến (Encapsulation & Scope Safety).
   * Độ đọc hiểu và Chuẩn hóa cú pháp (Readability & ES6+ Standard).
   * Khả năng mở rộng & Tái sử dụng (Maintainability & Reusability).

#### **Phần 2: Lý giải lựa chọn và Mã giả / Lưu đồ luồng (Flowchart)**
1. Đưa ra lý giải khoa học thuyết phục lý do chọn phương án tối ưu nhất cho hệ thống Ticketbox.
2. Vẽ **Lưu đồ thuật toán (Mermaid Flowchart)** thể hiện chi tiết luồng xử lý mua vé và tính tiền của phương án tối ưu.
   * *Yêu cầu chuẩn hóa Mermaid shapes:*
     * Oval `([Bắt đầu / Kết thúc])` cho điểm khởi đầu và kết thúc.
     * Hình bình hành `[/Đầu vào / Đầu ra/]` cho thao tác nhận tham số hoặc trả về kết quả.
     * Hình chữ nhật `["Thực hiện tính toán / Cập nhật biến"]` cho các bước xử lý logic.
     * Hình thoi `Kiểm tra điều kiện?` cho các nhánh rẽ điều kiện.

#### **Phần 3: Triển khai mã nguồn và Chặn lỗi biên**
Triển khai mã nguồn JavaScript (ES6+) hoàn chỉnh cho phương án tối ưu đã chọn:
* Khai báo hàm tạo bộ quản lý vé cho khách hàng bằng Arrow Function và Closure.
* Sử dụng Default Parameters cho `taxRate = 0.08`, `serviceFee = 20000`, `isEarlyBird = false`.
* Viết logic tính tiền vé chính xác theo công thức nghiệp vụ.
* Bắt toàn bộ các trường hợp lỗi biên (Edge Cases): Số lượng vé mua $\le 0$, số lượng không phải số nguyên, đơn giá $\le 0$, vượt hạn ngạch 4 vé.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
* Phần phân tích/báo cáo và mã nguồn triển khai.
* Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex12`.
  * Ví dụ: `HNKS25CNTT1_Core_Session14_Ex12`
