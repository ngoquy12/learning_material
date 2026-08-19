# <center>[Phân tích 2] Đóng Gói Mô-đun Tính Giá Vé và Quản Lý Hạn Ngạch Đặt Vé Concert</center>

### **1. Mục tiêu**

*   **Về kiến thức**: Trình bày và vận dụng sâu sắc cơ chế phạm vi biến (Global Scope, Local Scope) và Closure trong JavaScript ES6+ để bảo vệ dữ liệu nghiệp vụ nhạy cảm khỏi các thao tác can thiệp trái phép.
*   **Về kỹ năng**: Áp dụng thành thạo cú pháp Arrow Function kết hợp với Tham số mặc định (Default Parameters) để tối ưu hóa mã nguồn, thiết lập giao diện lập trình logic rõ ràng và ngăn ngừa lỗi dữ liệu đầu vào khuyết thiếu.
*   **Về tư duy phân tích**: Thực hiện so sánh Trade-off giữa các hướng thiết kế hàm khác nhau trong ứng dụng bán vé sự kiện, đánh giá tính an toàn, bộ nhớ và khả năng bảo trì của hệ thống.

### **2. Bối cảnh & Vấn đề**

Trong ứng dụng quản lý vé sự kiện ca nhạc **Ticketbox**, khi hệ thống mở bán các đêm nhạc quy mô lớn, việc xử lý tính toán giá đơn hàng và kiểm soát hạn ngạch vé mua của từng tài khoản khách hàng đóng vai trò cốt lõi. Mỗi tài khoản người dùng chỉ được phép mua một số lượng vé nhất định nhằm hạn chế tình trạng "gầu vé" (seat scalping).

Hệ thống legacy hiện tại đang lưu trữ số vé đã mua của người dùng và các thông số giá ở dạng biến toàn cục (Global Scope). Điều này gây ra những rủi ro nghiêm trọng:
1.  Bất kỳ đoạn mã script nào khác trong phiên chạy cũng có thể ghi đè biến toàn cục, làm mất tính chính xác của số vé đã đặt.
2.  Khi không truyền đủ các tham số tính toán (như phí xuất vé hay tỷ lệ thuế VAT), hàm cũ trả về kết quả `NaN` hoặc tính toán sai lệch do xử lý tham số mặc định bằng các toán tử hoán đổi không an toàn.

Để chuẩn hóa kiến trúc mã nguồn cho đợt mở bán sắp tới, nhóm phát triển yêu cầu bạn nghiên cứu và tái cấu trúc toàn bộ mô-đun tính toán đơn hàng và quản lý hạn ngạch mua vé bằng cách áp dụng các nguyên lý nâng cao về tổ chức hàm, Scope và Closure.

### **3. Quy tắc nghiệp vụ**

1.  **Quy định hạn ngạch mua vé (Quota Limit)**:
    *   Mỗi tài khoản chỉ được phép mua **tối đa 4 vé** cho một đêm diễn trong toàn bộ phiên hoạt động.
    *   Nếu số lượng vé đăng ký mua thêm vượt quá hạn ngạch khả dụng còn lại của tài khoản, hệ thống phải chặn giao dịch và trả về thông báo lỗi chi tiết.

2.  **Công thức tính toán tổng giá trị đơn hàng**:
    *   `Giá vé gốc = số lượng vé * đơn giá vé`.
    *   **Ưu đãi Early Bird**: Nếu đơn hàng thuộc đợt bán vé sớm, áp dụng mức chiết khấu **15%** trên tổng giá vé gốc.
    *   **Phí dịch vụ xuất vé (Service Fee)**: Mặc định là **30,000 VNĐ / đơn hàng** (nếu hệ thống không truyền đối số phí cụ thể).
    *   **Thuế VAT**: Mặc định là **8% (0.08)** tính trên số tiền sau chiết khấu (nếu hệ thống không truyền đối số thuế cụ thể).
    *   `Tổng thanh toán = (Giá vé gốc - Chiết khấu) + Thuế VAT + Phí dịch vụ xuất vé`.

3.  **Đóng gói dữ liệu an toàn (Scope & Closure Isolation)**:
    *   Trạng thái tích lũy tổng số vé người dùng đã đặt thành công phải được lưu giữ private bên trong phạm vi Lexical Scope của Closure.
    *   Tuyệt đối không sử dụng biến toàn cục (Global Scope) để lưu trạng thái này nhằm tránh nguy cơ bị ghi đè dữ liệu từ bên ngoài.

4.  **Ràng buộc kiểm chuẩn dữ liệu (Input Validation)**:
    *   Số lượng vé mua thêm mỗi lần phải là số nguyên dương lớn hơn 0 (`ticketQuantity > 0` và là số nguyên).
    *   Đơn giá vé phải là số lớn hơn hoặc bằng 0 (`unitPrice >= 0`).

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Kỹ sư Phần mềm Frontend/Backend Core, thực hiện đầy đủ 3 phần công việc sau:

#### **Phần 1: Báo cáo Đề xuất Giải pháp & Phân tích Trade-off**
*   Tự đề xuất ít nhất **2 giải pháp kỹ thuật khác nhau** để thiết kế mô-đun quản lý hạn ngạch vé và engine tính giá tiền đơn hàng (với các cách tổ chức hàm, quản lý scope, và khởi tạo closure khác nhau).
*   Lập bảng so sánh Trade-off chi tiết giữa 2 giải pháp dựa trên 5 tiêu chí bắt buộc:
    1.  Tốc độ thực thi (Performance / Execution Speed).
    2.  Mức tiêu thụ bộ nhớ (Memory Allocation & Scope Lifecycle).
    3.  Khả năng bảo trì và mở rộng (Maintainability & Extensibility).
    4.  Độ rõ ràng và chuẩn mực mã nguồn (Readability & Code Style).
    5.  Mức độ phù hợp với yêu cầu đóng gói dữ liệu (Security & Encapsulation Suitability).

[NOTE] Yêu cầu trình bày bảng so sánh bằng bảng HTML có thuộc tính CSS: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **Phần 2: Giải trình Lựa chọn & Thiết kế Lưu đồ Thuật toán**
*   Đưa ra lý giải khoa học và lập luận kỹ thuật cho việc chọn lựa 1 giải pháp tối ưu nhất từ 2 phương án đã đề xuất.
*   Xây dựng sơ đồ quy trình xử lý (**Mermaid Flowchart**) cho phương án tối ưu đã chọn.
*   [REQUIREMENT] Sơ đồ Mermaid bắt buộc phải tuân thủ chính xác 5 dạng hình chuẩn theo quy định:
    - Terminator (Start/End): `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`
    - Input/Output: `[/Đầu vào: .../]` / `[/Đầu ra: .../]`
    - Decision: `Kiểm tra điều kiện?` kết hợp nhánh `-->|Đúng|` và `-->|Sai|`
    - Process: `["Thực hiện tính toán / Cập nhật dữ liệu"]`
    - Flowline: Mũi tên kết nối `-->`

#### **Phần 3: Triển khai Mã nguồn & Bắt lỗi Biên (Edge Cases)**
*   Viết mã nguồn JavaScript chuẩn ES6+ triển khai trọn vẹn phương án tối ưu.
*   Sử dụng Arrow Function, Default Parameters và Closure để đóng gói biến trạng thái đếm vé private.
*   Xử lý triệt để các trường hợp lỗi biên (Edge Cases):
    - Người dùng nhập số vé âm, bằng 0, hoặc số thực.
    - Đặt vé vượt quá hạn ngạch 4 vé.
    - Không truyền đối số phí dịch vụ hoặc đối số thuế VAT (hệ thống tự áp dụng tham số mặc định).
    - Truyền tỷ lệ chiết khấu hoặc thuế bằng 0 (đảm bảo giá trị 0 không bị coi là falsy để rồi tự lấy lại giá trị mặc định sai logic).
*   Tạo các kịch bản gọi thử nghiệm (console.log) minh họa cho 3 trường hợp:
    - Kịch bản A: Đặt thành công vé đợt Early Bird sử dụng toàn bộ tham số mặc định.
    - Kịch bản B: Tiếp tục đặt thêm vé đợt chính thức và bị từ chối do vượt hạn ngạch 4 vé.
    - Kịch bản C: Truyền dữ liệu đầu vào vi phạm rào chắn dữ liệu.

### **5. Yêu cầu nộp bài**

Học viên cần nộp:
*   Phần báo cáo phân tích kiến trúc, bảng so sánh trade-off, lưu đồ Mermaid và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session14_Ex11`.
    Ví dụ: `HNKS25CNTT1_Core_Session14_Ex11`
