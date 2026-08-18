### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Tính Toán Chi Phí Khám Bệnh Và Xác Nhận Đặt Lịch Phòng Khám — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định chính xác các tham số đầu vào (`patientName`, `patientAge`, `baseExamFee`, `insuranceDiscountRate`), hằng số (`serviceFee`) và đầu ra (`totalPayment`, phiếu xác nhận) cùng kiểu dữ liệu tương ứng (`String`, `Number`, `Boolean`).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Trình bày giải pháp logic mạch lạc và vẽ sơ đồ Mermaid tuân thủ đúng 5 dạng hình tiêu chuẩn (Terminator, Input/Output, Decision, Process, Flowline).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo đúng phạm vi biến ES6 (`const` cho hằng số cố định như phí dịch vụ, `let` cho giá trị tính toán), đặt tên biến chuẩn `camelCase` bằng tiếng Anh rõ nghĩa.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán chính xác số tiền BHYT chi trả, giá khám thực tế và tổng chi phí thanh toán theo quy tắc nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Thực hiện ép kiểu minh bạch với `Number()` cho các dữ liệu số từ `prompt()`, phòng ngừa tuyệt đối lỗi cộng chuỗi ngoài ý muốn (ví dụ: `"150000" + "30000"` thành `"15000030000"`).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Xử lý dữ liệu nhập vào hợp lý, tránh các trường hợp tính toán sai lệch khi giá trị BHYT hoặc chi phí khám không phải số hợp lệ.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Định dạng chuỗi Template Literals đa dòng đầy đủ thông tin hóa đơn xác nhận và xuất đồng thời ra cả `console.log()` lẫn `alert()`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Mã nguồn sạch đẹp, định dạng thụt lề chuẩn xác, tách biệt HTML và JavaScript (`<script src="app.js"></script>`), có chú thích Tiếng Việt rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** Đẩy toàn bộ mã nguồn lên thư mục GitHub theo đúng cấu trúc tên bài tập quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Trình bày thông tin xác nhận hóa đơn dưới dạng bảng kết quả chuyên nghiệp trong Developer Console bằng `console.table()` bên cạnh dạng chuỗi văn bản thông thường.