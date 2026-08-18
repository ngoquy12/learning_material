### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Thiết kế Module Phụ thu Check-in sớm và Phê duyệt Đặt phòng Khách sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Đề xuất chi tiết ít nhất 2 phương án xử lý logic không dùng `if/else` và không dùng `and/or/not`. 
    *   *Ví dụ:* 
        *   *Phương án A:* Nhân trực tiếp biểu thức so sánh dạng Boolean với giá trị tính toán, ví dụ: `early_surcharge = (checkin_hour < 12) * (0.30 * base_price_per_night)`.
        *   *Phương án B:* Sử dụng hàm ép kiểu số `float(checkin_hour < 12)` hoặc `int(checkin_hour < 12)` làm hệ số tính toán trước khi thực hiện phép nhân.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** 
    *   Xây dựng bảng HTML table đầy đủ 5 tiêu chí (Speed, Memory, Maintainability, Readability, Suitability).
    *   Có phân tích ưu/nhược điểm sắc bén cho từng phương án dựa trên bản chất ngôn ngữ Python.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** 
    *   Giải thích rõ ràng lý do chọn phương án tối ưu (ví dụ: tối ưu cú pháp gọn nhẹ, đọc mã nguồn tự nhiên, phù hợp với kiến trúc tính toán nguyên tử).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** 
    *   Vẽ Mermaid Flowchart hoàn chỉnh, cú pháp hợp lệ.
    *   Tuân thủ đúng 5 hình dạng chuẩn: Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho Process/Calculation, Diamond cho Decision.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** 
    *   Viết mã nguồn Python 3.12 chạy thành công, không có lỗi cú pháp.
    *   Sử dụng chính xác toán tử số học và toán tử so sánh để tính toán phụ thu và xác định `is_instant_confirmed`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** 
    *   Logic phụ thu chính xác khi `checkin_hour = 11` (có phụ thu) và `checkin_hour = 12` (không phụ thu).
    *   Logic duyệt `is_instant_confirmed` chính xác khi tiền cọc vừa đủ 50% hoặc vượt quá 50%.
    *   Tuyệt đối không vi phạm phạm vi cấm (không xuất hiện `if`, `else`, `and`, `or`, `not`, `for`, `while`, `list`, `dict`).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** 
    *   Kết quả in ra Console minh bạch, định dạng số tiền rõ ràng, kèm giải thích cho từng mục tính toán.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** 
    *   Tên biến 100% bằng tiếng Anh chuẩn snake_case (ví dụ: `base_price_per_night`, `early_checkin_surcharge`, `is_instant_confirmed`).
    *   Khai báo Type Hints đầy đủ cho các biến đầu vào.
*   **[5 điểm] Nộp bài GitHub:** 
    *   Cấu trúc thư mục nộp bài chuẩn quy định: `[Tên Lớp]_[Môn Học]_Session04_Ex10`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** 
    *   Viết đoạn mã thử nghiệm đo thời gian thực thi (sử dụng module `time`) so sánh hiệu năng chạy 1.000.000 lượt tính toán giữa Phương án A và Phương án B.