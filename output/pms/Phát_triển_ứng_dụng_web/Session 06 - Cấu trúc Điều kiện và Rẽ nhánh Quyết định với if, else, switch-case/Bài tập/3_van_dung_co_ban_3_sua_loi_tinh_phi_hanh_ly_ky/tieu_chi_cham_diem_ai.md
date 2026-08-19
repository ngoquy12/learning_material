# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi tính phí hành lý ký gửi khi Check-in máy bay — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác 2 lỗi logic lớn:
    1. Lỗi thứ tự điều kiện trong khối `if...else if` (kiểm tra `baggageWeight > 7` trước nên các giá trị > 15 kg và > 25 kg không bao giờ chạm tới).
    2. Lỗi trôi lệnh (fall-through) do thiếu từ khóa `break` trong `case "DELUXE"` của câu lệnh `switch-case`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác 100% các giá trị còn thiếu (`...`) trong Bảng Test Case ở Phần 1 (bao gồm Buggy Output, Expected Output, Dòng code gây lỗi, và Giải thích nguyên nhân).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công khối `if...else if` (đặt điều kiện `> 25` lên đầu, hoặc đảo chiều so sánh tăng dần hợp lý) và thêm `break` đầy đủ vào câu lệnh `switch-case`.
*   **[20 điểm] Tính toán chính xác các trường hợp cước hành lý:**
    *   Hành lý <= 7kg: Phí cơ bản 0 VNĐ.
    *   Hành lý 8kg - 15kg: Phí 150.000 VNĐ.
    *   Hành lý 16kg - 25kg: Phí 300.000 VNĐ.
    *   Hành lý > 25kg: Tính đúng 500.000 VNĐ + 50.000 VNĐ/kg quá cước.
    *   Áp dụng chuẩn xác giảm giá theo hạng vé `BUSINESS` (giảm 100%), `DELUXE` (giảm 50%), `ECO` (giảm 0%).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra khối lượng hành lý `baggageWeight` không được âm (`< 0`) hoặc là `NaN`/không phải kiểu số (`typeof baggageWeight !== 'number'`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp `ticketClass` không hợp lệ thông qua nhánh `default` trong `switch-case` mà không làm ứng dụng bị văng lỗi runtime.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn cơ chế Fall-through trong `switch-case` (khi nào là tính năng có lợi, khi nào là lỗi lập trình) và tại sao thứ tự kiểm tra điều kiện lại vô cùng quan trọng trong chuỗi `if...else if`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng bằng Tiếng Anh (`ticketClass`, `baggageWeight`, `baseFee`, `discountRate`), thụt lề chuẩn 2 spaces, ghi chú thích giải thích logic bằng Tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu bằng Toán tử Ba ngôi (Ternary Operator):** Sử dụng toán tử ba ngôi để tính nhanh mức phí hành lý cho các trường hợp đơn giản hoặc tính tỷ lệ giảm giá một cách ngắn gọn, sạch đẹp nhưng vẫn đảm bảo tính dễ đọc của mã nguồn.
