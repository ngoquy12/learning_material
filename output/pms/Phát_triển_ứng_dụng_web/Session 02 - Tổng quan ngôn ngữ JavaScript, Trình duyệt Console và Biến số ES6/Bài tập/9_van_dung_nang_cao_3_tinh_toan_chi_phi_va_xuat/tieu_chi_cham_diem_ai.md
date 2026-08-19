# **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Tính toán Chi phí và Xuất Phiếu Khám Bệnh Tự động — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Phân tích đầy đủ tất cả các tham số đầu vào (`patientName`, `birthYear`, `baseFee`, `hasInsurance`, `serviceFee`) và đầu ra (`patientAge`, `insuranceDiscount`, `totalPayment`, `isPriority`), xác định đúng kiểu dữ liệu nguyên thủy cho từng biến.
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Vẽ sơ đồ Mermaid Flowchart thể hiện chính xác luồng xử lý từ nhập liệu, ép kiểu `Number`, tính toán tài chính đến đóng gói chuỗi Template Literals. Tuân thủ 100% quy tắc 5 hình dạng chuẩn (không dùng sai hình bình hành cho bước tính toán).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo hằng số hệ thống (`currentYear = 2026`, `insuranceDiscountRate = 0.8`, `priorityAgeThreshold = 70`) bằng từ khóa `const`. Khai báo biến lưu giữ kết quả tính toán bằng `let`. Đặt tên biến 100% chuẩn `camelCase` bằng tiếng Anh.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Tính toán chính xác tuổi bệnh nhân, tiền giảm trừ BHYT (80% nếu `hasInsurance = 1`, 0% nếu `hasInsurance = 0`), phụ phí và tổng chi phí thanh toán cuối cùng.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Thực hiện ép kiểu dữ liệu đầu vào minh bạch ngay khi nhận dữ liệu từ `prompt()` bằng `Number()`, ngăn ngừa tuyệt đối lỗi cộng nối chuỗi ngầm định (ví dụ: `"150000" + "30000" = "15000030000"`).
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Xử lý chính xác trường hợp năm sinh hoặc chi phí bị nhập sai định dạng thành `NaN`, đảm bảo kết quả phép tính toán học không bị sai lệch dữ liệu.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất báo cáo phiếu xác nhận khám đầy đủ, chuyên nghiệp thông qua chuỗi Template Literals với định dạng rõ ràng, hiển thị đồng thời ở `console.log()` và `alert()`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Mã nguồn viết sạch sẻ, có chú thích giải thích logic bằng tiếng Việt có dấu, nhúng tệp script ngoài ở trước thẻ đóng `</body>` trong file `index.html`.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên kho lưu trữ GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex9`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Trình bày mã nguồn tối ưu, đóng gói biểu thức logic kiểm tra điều kiện ưu tiên trực tiếp trong chuỗi nội dung xuất mà không tạo thêm các biến trung gian thừa thải.
