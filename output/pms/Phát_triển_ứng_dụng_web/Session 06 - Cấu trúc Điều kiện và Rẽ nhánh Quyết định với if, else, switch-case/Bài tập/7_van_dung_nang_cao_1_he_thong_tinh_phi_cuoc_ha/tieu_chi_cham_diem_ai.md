### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Hệ thống tính phí cước hành lý sân bay tự động — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định đầy đủ danh sách biến đầu vào (`ticketClass`, `baggageWeight`, `passengerType`, `isVipMember`) và đầu ra (`freeAllowance`, `excessWeight`, `totalPenalty`), gán đúng kiểu dữ liệu.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Vẽ sơ đồ luồng Mermaid đầy đủ logic nghiệp vụ, sử dụng chuẩn xác 5 dạng hình (Oval cho Start/End, Parallelogram cho I/O, Diamond cho điều kiện, Rectangle cho tính toán).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo hằng số và biến bằng `const`/`let` chuẩn ES6+, thiết lập bộ dữ liệu test case minh bạch.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Kết hợp chính xác `if-else` (tính hạn mức miễn cước cơ bản và ưu đãi), `switch-case` (tra cứu đơn giá phạt theo hạng vé) và toán tử ba ngôi (tính phụ phí quá tải > 15 kg).

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Xử lý chính xác trường hợp hành lý không quá cước (`excessWeight <= 0` thì phí phạt bằng 0) và tính phụ phí 200.000 VNĐ khi `excessWeight > 15`.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Bắt bẫy trọng lượng âm (`baggageWeight < 0`) và xử lý hạng vé không tồn tại bằng nhánh `default` trong `switch-case`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Hiển thị thông báo lỗi rõ ràng, chuyên nghiệp ra console khi phát hiện dữ liệu đầu vào không hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Đặt tên biến hoàn toàn bằng tiếng Anh theo quy tắc camelCase, căn lề chuẩn 2 spaces, ghi chú thích giải thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Tạo repository và đặt tên thư mục đúng định dạng quy định `[Tên Lớp]_[Môn Học]_Session06_Ex7`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Viết mã nguồn ngắn gọn, tối ưu luồng kiểm tra logic không bị lặp dư thừa, áp dụng nguyên lý DRY (Don't Repeat Yourself).