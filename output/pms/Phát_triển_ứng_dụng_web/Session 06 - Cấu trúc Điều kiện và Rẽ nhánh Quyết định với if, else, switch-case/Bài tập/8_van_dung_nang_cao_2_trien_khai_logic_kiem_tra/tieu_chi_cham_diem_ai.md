### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Triển khai logic kiểm tra check-in và tính toán phụ phí hành lý hàng không — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:**
    *   Xác định đúng và đầy đủ kiểu dữ liệu các tham số đầu vào (`ticketClass`: string, `passengerTier`: string, `handBaggageWeight`: number, `checkedBaggageWeight`: number, `isPriorityBoarding`: boolean).
    *   Xác định đúng kết quả đầu ra (tổng trọng lượng ký gửi thực tế, tổng phụ phí hành lý, phí ưu tiên, tổng chi phí thanh toán, trạng thái check-in).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:**
    *   Trình bày sơ đồ luồng quy trình xử lý logic bằng chuẩn Mermaid Flowchart.
    *   Tuân thủ nghiêm ngặt quy chuẩn hình dạng Mermaid (Hình thoi cho điều kiện, Hình chữ nhật cho tính toán, Hình bình hành cho I/O, Oval cho Start/End). Không dùng sai hình chữ nhật / hình bình hành.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Áp dụng đúng cấu trúc rẽ nhánh theo quy định:**
    *   Sử dụng `switch-case` chính xác để xác định hạn mức theo `ticketClass` có đầy đủ `break` và `default`.
    *   Sử dụng `if...else if...else` chính xác để tính toán dồn kg xách tay vượt mức và ưu đãi theo `passengerTier`.
    *   Sử dụng toán tử ba ngôi `ternary operator` đơn cho tính phí Boarding ưu tiên và gán trạng thái check-in.
*   **[15 điểm] Tính toán phụ phí và đơn giá cước lũy tiến:**
    *   Tính đúng logic chuyển kg dư thừa xách tay sang ký gửi.
    *   Áp dụng chuẩn đơn giá 50.000 VNĐ/kg hoặc đơn giá lũy tiến 75.000 VNĐ/kg khi tổng ký gửi vượt 40 kg.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy vượt ngưỡng an toàn quy định:**
    *   Bắt chính xác bẫy tổng hành lý ký gửi thực tế vượt quá 50 kg, đưa ra trạng thái `"REJECTED_OVERWEIGHT"` và cảnh báo an toàn.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:**
    *   Chặn các trường hợp cân nặng bị âm (`handBaggageWeight < 0` hoặc `checkedBaggageWeight < 0`).
    *   Xử lý trường hợp hạng vé hoặc hạng hội viên nhập không hợp lệ (không nằm trong danh sách chuẩn) bằng thông báo lỗi hệ thống.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:**
    *   In ra thông báo rõ ràng, chuyên nghiệp trên console về chi tiết hóa đơn check-in, phân rã từng khoản phí và nguyên nhân từ chối nếu bị quá cước an toàn.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:**
    *   Đặt tên biến/hằng số hoàn toàn bằng tiếng Anh rõ nghĩa (`ticketClass`, `allowanceWeight`, `excessFee`, `checkinStatus`).
    *   Chú thích giải thích bằng tiếng Việt có dấu đầy đủ, thụt lề 2 spaces chuẩn ES6+.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đẩy mã nguồn lên repository GitHub đúng cấu trúc tên thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:**
    *   Tổ chức code dưới dạng hàm ES6 hoàn chỉnh nhận tham số đầu vào và trả về đối tượng kết quả (`Object`) chứa đầy đủ thông tin hóa đơn phụ thu, tránh sử dụng biến toàn cục dư thừa.