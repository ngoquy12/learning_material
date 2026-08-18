### **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Thiết kế Hệ thống Phân luồng Check-in và Tính phí Phụ thu Hành lý Máy bay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Học viên đề xuất đủ 2 phương án kỹ thuật rẽ nhánh rõ ràng (Ví dụ: Phương án 1 dùng các khối `if-else if` lồng nhau truyền thống; Phương án 2 kết hợp Guard Clauses loại bỏ case lỗi sớm, sau đó phân tách việc tính phí hành lý bằng `switch-case` và phân làn check-in bằng biểu thức logic điều kiện).
    *   Phân tích cụ thể sự khác biệt về mặt cấu trúc điều kiện giữa 2 phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng so sánh đủ 5 tiêu chí (Tốc độ xử lý, Bộ nhớ, Khả năng bảo trì, Độ dễ đọc, Mức độ phù hợp quy mô) sử dụng đúng thẻ HTML `<table>` có thuộc tính inline style theo yêu cầu.
    *   Nội dung phân tích trong từng ô sắc bén, có căn cứ kỹ thuật lập trình thực tế, không viết chung chung.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lập luận thuyết phục lý giải vì sao phương án được chọn giúp hệ thống chạy nhanh hơn, giảm rủi ro bug khi bổ sung thêm hạng vé mới trong tương lai.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Trình bày mã giả hoặc lưu đồ Mermaid chính xác.
    *   Nếu dùng Mermaid, phải tuân thủ đúng 100% chuẩn hình dạng: Oval `([...])` cho Terminator, Rectangle `["..."]` cho Process, Diamond `?` cho Decision, Parallelogram `[/.../]` cho Input/Output.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Sử dụng đúng cú pháp JavaScript ES6+ (`const`, `let`, `if-else`, `switch-case`, ternary).
    *   Tính chính xác 100% cước phí hành lý quá cân cho 3 hạng vé (Eco 7kg/50k, Deluxe 20kg/40k, Business 40kg/30k).
    *   Tính chính xác phí trễ giờ làm thủ tục (Eco 200k, Deluxe 100k, Business 0k).
    *   Gán đúng 100% làn check-in (Priority Counter nếu VIP hoặc Business; Fast-track Counter nếu Deluxe; Standard Counter cho các trường hợp còn lại).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Bắt trọn vẹn trường hợp `ticketClass` không thuộc {1, 2, 3} và `baggageWeight < 0`.
    *   Xử lý đúng trường hợp hành lý không quá cân (`baggageWeight <= freeAllowance`) thì cước phí quá cân phải bằng `0`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   In ra màn hình console đầy đủ thông tin báo cáo check-in: Hạng vé, Trọng lượng hành lý, Phí hành lý quá cước, Phí trễ giờ, Tổng phụ thu, Làn phục vụ.
    *   Kết quả tính toán với các Test Case mẫu khớp hoàn toàn với quy tắc nghiệp vụ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Biến và hằng số đặt bằng tiếng Anh theo chuẩn camelCase (`ticketClass`, `baggageWeight`, `excessBaggageFee`, `lateCheckinFee`, `counterLane`).
    *   Mã nguồn thụt lề chuẩn 2 spaces, không dư thừa mã rác, có comment giải thích bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub repository hợp lệ, đặt tên thư mục đúng chuẩn format: `[Tên Lớp]_[Môn Học]_Session06_Ex12`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản Kiểm thử Tự động (Benchmark/Test Runner Script):**
    *   Tự thiết kế một chuỗi các lệnh gán đầu vào liên tiếp đại diện cho 5+ trường hợp thực tế khác nhau và in ra bảng tổng hợp kết quả tự động để kiểm tra tính toàn vẹn của logic.