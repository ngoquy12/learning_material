### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Tính Phí Hành Lý Quá Cước Và Phụ Phí Chọn Ghế Máy Bay — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định chính xác các biến đầu vào (`ticketClassCode`, `carryOnWeight`, `checkedWeight`, `seatSelectionType`, `isPriorityCheckin`) kèm kiểu dữ liệu và các biến đầu ra (`excessCarryOn`, `totalCalculatedCheckedWeight`, `overweightKg`, `baggageFee`, `bulkyBaggageFee`, `seatFee`, `priorityFee`, `totalSurcharge`, `checkinStatus`).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Vẽ sơ đồ luồng Mermaid Flowchart đúng quy chuẩn hình khối (Terminator `([ ])`, I/O `[/ /]`, Decision `Kiểm tra?`, Process `[" "]`) mô tả chính xác quy trình xử lý dữ liệu và các điểm rẽ nhánh.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo biến/hằng số chuẩn xác trong ES6 (`const`, `let`), lưu trữ các hằng số hạn mức (7kg xách tay; 0kg, 20kg, 40kg ký gửi) và mức phạt cồng kềnh (500.000 VNĐ).
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** 
    *   Tính toán chuẩn xác phần dồn cước xách tay quá hạn sang ký gửi.
    *   Sử dụng cấu trúc `switch-case` chính xác cho 3 mã hạng vé để tính phụ phí ghế ngồi đúng bảng giá.
    *   Sử dụng toán tử ba ngôi để gán trạng thái `checkinStatus`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu vượt ngưỡng & cộng dồn:** Xử lý đúng trường hợp tổng hành lý ký gửi tính toán vượt ngưỡng `50 kg` (cộng thêm 500.000 VNĐ) và không phụ thu phí ưu tiên với Hạng Business.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Kiểm tra và chặn các trường hợp trọng lượng âm (`carryOnWeight < 0`, `checkedWeight < 0`), mã hạng vé khác {1, 2, 3} và mã ghế khác {1, 2, 3}.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất thông báo lỗi rõ ràng khi phát hiện dữ liệu không hợp lệ (ví dụ: `[ERROR] Mã hạng vé không hợp lệ`) và in hóa đơn thanh toán chi tiết khi dữ liệu hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Đặt tên biến/hằng số hoàn toàn bằng tiếng Anh theo chuẩn camelCase, viết ghi chú tiếng Việt có dấu rõ ràng, căn lề chuẩn 2 spaces.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session06_Ex9`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Tối ưu hóa cấu trúc rẽ nhánh, tránh lặp lại các đoạn mã thừa, viết mã nguồn theo phong cách Clean Code dễ đọc và có tính mở rộng cao.