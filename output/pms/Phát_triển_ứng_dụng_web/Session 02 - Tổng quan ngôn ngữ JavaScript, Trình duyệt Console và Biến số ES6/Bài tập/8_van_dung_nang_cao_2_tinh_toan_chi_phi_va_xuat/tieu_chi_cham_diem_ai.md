### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Tính toán Chi phí và Xuất Phiếu Đăng ký Khám bệnh Tự động — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Liệt kê đầy đủ các tham số đầu vào (`patientId`, `patientName`, `patientAge`, `baseFee`, `labFee`, `insuranceDiscountRate`) cùng kiểu dữ liệu ban đầu (`string`) và kiểu dữ liệu sau ép kiểu (`number`), đầu ra xuất ra Console & Alert.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Trình bày rõ phương án ép kiểu dữ liệu bằng `Number()`, quy tắc dùng `const`/`let` và sơ đồ luồng Mermaid đầy đủ các bước thực hiện.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo chính xác các biến và hằng số theo chuẩn ES6 `camelCase`, phân định hợp lý giữa `const` (đơn giá cố định, kết quả tính toán) và `let` (biến có thể thay đổi).
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán chính xác tổng chi phí dịch vụ, số tiền BHYT chi trả, tổng thanh toán thực tế và biểu thức kiểm tra ưu tiên cao tuổi.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Ép kiểu minh bạch toàn bộ các tham số tài chính số (`Number(...)`), triệt tiêu hoàn toàn lỗi nối chuỗi `string + string` của `prompt()`.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Đảm bảo thứ tự nhận dữ liệu logic, xử lý dữ liệu đầu vào an toàn, đúng kiểu dữ liệu mục tiêu trước khi thực hiện phép tính số học.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất dữ liệu phiếu tiếp nhận bằng Template Literals với định dạng đẹp mắt, bố cục rõ ràng trên Console và thông báo Alert súc tích.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Mã nguồn viết hoàn toàn bằng tên Tiếng Anh (`camelCase`), ghi chú giải thích bằng Tiếng Việt có dấu, cấu trúc HTML/JS tách biệt chuẩn V8 Engine (`script` đặt trước `</body>`).
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đẩy mã nguồn lên GitHub đúng định dạng tên thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex8`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Trình bày sơ đồ luồng Mermaid minh họa chính xác 5 dạng hình khối tiêu chuẩn (Oval, Parallelogram, Rectangle, Diamond, Arrow) và giải thích được cơ chế V8 Engine biên dịch Bytecode tối ưu khi tách riêng file `.js`.