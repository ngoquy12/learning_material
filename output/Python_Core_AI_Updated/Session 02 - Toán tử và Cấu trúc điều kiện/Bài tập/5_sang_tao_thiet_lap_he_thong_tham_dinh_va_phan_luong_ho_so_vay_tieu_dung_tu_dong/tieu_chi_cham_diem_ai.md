### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết lập hệ thống thẩm định và phân luồng hồ sơ vay tiêu dùng tự động — Tổng điểm: 100 điểm**

#### **1. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 30 điểm**
*   **[15 điểm] Thiết kế luồng dữ liệu (Data Flow):** Vẽ hoặc mô tả chính xác luồng di chuyển dữ liệu từ lúc nhận Input Dict, chạy qua bộ validate dữ liệu thô, thực hiện các phép logic toán tử để tính DTI, cho tới khi phân luồng thông qua bộ lọc.
*   **[15 điểm] Thiết kế vòng đời tính năng (Feature Lifecycle):** Mô tả rõ ràng cơ chế phân trạng thái của hồ sơ (Ví dụ: từ lúc nhận hồ sơ -> Kiểm tra điều kiện -> Chuyển luồng `match-case` -> Trạng thái cuối cùng: `APPROVED`, `REJECTED`, hay `MANUAL_REVIEW`).

#### **2. Hiện thực hóa logic nghiệp vụ sáng tạo — 40 điểm**
*   **[20 điểm] Ứng dụng cấu trúc match-case nâng cao:** Sử dụng chuẩn xác cấu trúc `match-case` để phân loại xử lý dựa trên trường dữ liệu `loan_purpose`, bao gồm cả trường hợp mặc định `case _` để bẫy các mục đích vay không hợp lệ.
*   **[20 điểm] Tính toán chỉ số tài chính chính xác:** Triển khai đúng công thức toán học tính DTI, tính toán lãi suất ưu đãi giảm trừ theo từng điều kiện lồng nhau, và tự động thu hẹp hạn mức phê duyệt theo giới hạn thu nhập hoặc số tiền yêu cầu.

#### **3. Kiểm chuẩn dữ liệu, Chặn lỗi dị biệt nâng cao — 20 điểm**
*   **[10 điểm] Xử lý ngoại lệ nghiệp vụ và chặn biên:** Kiểm tra các điều kiện đầu vào của khách hàng để tránh dữ liệu bị lỗi logic (ví dụ: tuổi âm, thu nhập âm, điểm tín dụng nằm ngoài khoảng 300 - 850).
*   **[10 điểm] Xử lý logic chia cho 0:** Thiết kế hàm tính toán an toàn đề phòng trường hợp thu nhập đầu vào được truyền vào bằng 0 (`monthly_income = 0`), đảm bảo hệ thống không bị crash đột ngột mà sẽ ném ra lỗi hoặc chuyển sang trạng thái từ chối phù hợp.

#### **4. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Phép toán trực quan:** Đặt tên biến tường minh, phân tách hàm kiểm tra điều kiện thô và hàm xử lý nghiệp vụ chính rõ ràng. Các toán tử so sánh lồng nhau được viết rõ ràng kèm chú thích.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc Git repo đúng định dạng, commit có thông điệp rõ nghĩa, có file README hướng dẫn cách chạy thực nghiệm các bộ dữ liệu thử nghiệm.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế thẩm định đồng bảo lãnh (Co-signer):** Phát triển thêm tính năng cho phép hồ sơ không đủ điểm tự động duyệt (ở trạng thái `MANUAL_REVIEW` hoặc `REJECTED` nhẹ) được tái đánh giá nếu bổ sung thông tin của người đồng bảo lãnh (Co-signer) có điểm tín dụng tốt, giúp hồ sơ nâng hạng lên phê duyệt.