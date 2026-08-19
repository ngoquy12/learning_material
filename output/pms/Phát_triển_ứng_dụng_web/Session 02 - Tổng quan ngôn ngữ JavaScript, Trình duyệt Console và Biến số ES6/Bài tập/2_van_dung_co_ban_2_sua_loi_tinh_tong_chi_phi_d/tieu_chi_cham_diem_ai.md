# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi tính tổng chi phí đăng ký khám bệnh ban đầu — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng code thực hiện phép cộng biến chưa qua ép kiểu dữ liệu làm sai lệch logic.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành chính xác các ô còn trống (`...`) trong bảng Test Case với dữ liệu thực tế và kỳ vọng chính xác.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Tính chính xác tổng tiền thanh toán là phép cộng số học của phí khám và phí sổ khám (`consultationFee + cardFee`).
*   **[20 điểm] Ép kiểu dữ liệu an toàn:** Áp dụng đúng hàm `Number()` ngay sau khi nhận dữ liệu từ `prompt()` hoặc trước khi tính toán.

#### **3. Kiểm chuẩn dữ liệu & Xử lý xuất kết quả — 20 điểm**
*   **[10 điểm] Sử dụng Template Literals:** Định dạng câu thông báo kết quả bằng cú pháp `` `${...}` `` sạch đẹp, dễ đọc, không dùng nối chuỗi rườm rà.
*   **[10 điểm] Hiển thị kết quả đa kênh:** Xuất thông báo đầy đủ ra Developer Console (`console.log`) và cửa sổ thông báo (`alert`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ lý do hàm `prompt()` luôn trả về kiểu dữ liệu String và lý do từ khóa `var` không còn được khuyến khích trong ES6.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Áp dụng đúng quy tắc đặt tên `camelCase`, khai báo chuẩn `const`/`let`, có chú thích bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tải mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex2`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý giá trị mặc định:** Bổ sung logic gán giá trị mặc định bằng `0` nếu người dùng bấm Cancel hoặc để trống ô nhập phí sổ khám.
