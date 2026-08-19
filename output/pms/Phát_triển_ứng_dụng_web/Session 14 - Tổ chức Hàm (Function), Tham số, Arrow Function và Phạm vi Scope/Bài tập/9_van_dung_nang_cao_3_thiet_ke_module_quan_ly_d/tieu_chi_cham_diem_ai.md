### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Thiết kế Module Quản lý Đặt vé và Hạn ngạch Sự kiện bằng Closure & Arrow Function — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê đầy đủ tên tham số, kiểu dữ liệu (number, string, object, function...) và mô tả ý nghĩa dữ liệu đầu vào/đầu ra cho hàm tạo session và các phương thức con.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Giải thích rõ ràng nguyên lý Closure trong việc giấu biến `availableStock` và `userPurchasedCount`. Vẽ đúng sơ đồ luồng/các bước xử lý kiểm tra 2 lớp ràng buộc (Tồn kho & Hạn ngạch 4 vé).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Đóng gói State bằng Closure:** Khởi tạo biến private đúng cách trong hàm cha, trả về một đối tượng chứa các phương thức (Arrow Functions) có khả năng đọc/ghi các biến private đó mà không rò rỉ ra biến toàn cục.
*   **[15 điểm] Tính toán tài chính chuẩn xác:** Sử dụng đúng cú pháp Arrow Function và Tham số mặc định (Default Parameters) cho tỷ lệ chiết khấu (15%) và phí phát hành (20,000 VNĐ). Đảm bảo công thức tính giá sau chiết khấu và tổng thanh toán hoàn toàn chính xác.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy vượt hạn ngạch 4 vé:** Kiểm tra chính xác số vé đã tích lũy qua nhiều lần mua của một phiên giao dịch. Bắt lỗi và từ chối nếu `lượt_mua_mới + đã_mua > 4`.
*   **[15 điểm] Validate dữ liệu đầu vào & Tồn kho:** Kiểm tra số lượng mua phải là số nguyên dương (`Number.isInteger(qty) && qty > 0`), giá vé không âm, và số lượng mua không được vượt quá số vé khả dụng còn lại trong kho.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi rõ ràng:** Khi giao dịch bị từ chối (do vượt hạn ngạch, hết vé, dữ liệu sai format), hàm xử lý phải trả về đối tượng báo lỗi hoặc ném ra exception với thông điệp định danh tiếng Việt rõ ràng, giữ nguyên trạng thái kho vé trước đó.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch & Chuẩn ES6+:** Tên biến/hàm đặt bằng tiếng Anh chuẩn camelCase (`reserveTicket`, `getRemainingStock`, `calculateTotalPrice`), comment giải thích logic bằng tiếng Việt có dấu đầy đủ, tuyệt đối không dùng từ khóa `var` hoặc biến Global để lưu trữ state.
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đẩy mã nguồn lên GitHub đúng quy cách đặt tên thư mục theo hướng dẫn.

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ & Trả về Chi tiết Hóa đơn:** Phương thức đặt vé trả về thông tin hóa đơn chi tiết (bao gồm mã giao dịch duy nhất, giá gốc, tiền giảm giá, phí dịch vụ và số hạn ngạch còn lại được phép mua tiếp) dưới dạng Immutable Object.