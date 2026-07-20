### **Tiêu chí chấm điểm (AI)**
**[Khắc phục lỗi logic giao dịch ví điện tử] — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:**
    *   Chỉ ra cụ thể dòng tính phí giao dịch của tài khoản `STANDARD` dùng sai hàm `min` và `max` làm sai lệch số phí.
    *   Chỉ ra cụ thể dòng so sánh điều kiện số dư của người gửi (`sender["balance"] < request.amount`) bị thiếu biến `fee`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Standard Markdown Table tối thiểu 3 dòng ứng với 3 lỗi khác nhau (ví dụ: chuyển khoản tự thân, chuyển tiền âm, số dư không đủ thanh toán cả phí). Mỗi kịch bản có đủ Input, Actual Output (lỗi) và Expected Output.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:**
    *   Sửa chính xác logic tính phí `STANDARD`: Phí nằm trong đoạn $[2,000, 50,000]$. Gợi ý thuật toán: `fee = max(2000.0, min(50000.0, request.amount * 0.015))`.
    *   Sắp xếp lại trình tự xử lý: Tính phí trước, sau đó so sánh tổng tiền trừ (`amount + fee`) với số dư hiện có.
*   **[20 điểm] Trả về chính xác HTTP Status Code và Exception:**
    *   Ném ra `HTTPException` với trạng thái `status_code=400` kèm thông báo lỗi cụ thể khi số dư không đủ.
    *   Trả về mã lỗi hợp lý khi xảy ra các ngoại lệ nghiệp vụ khác.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:**
    *   Chặn giao dịch nếu số tiền chuyển từ `0` trở xuống (Ví dụ: `amount <= 0`).
    *   Chặn giao dịch nếu `sender_id` trùng khớp với `receiver_id`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kiểm tra sự tồn tại của tài khoản người gửi và tài khoản nhận trước khi xử lý các phép toán số học để tránh lỗi crash hệ thống `KeyError`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Sinh viên giải thích được tác hại của việc thực hiện trừ tiền trước khi kiểm tra số dư và cách ứng dụng độ ưu tiên của các toán tử logic, so sánh để giảm thiểu thời gian xử lý của CPU.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ quy chuẩn viết code PEP 8 (đặt tên biến rõ ràng, căn lề, thụt dòng nhất quán).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session02_Ex01`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Học viên cung cấp file kiểm thử độc lập (sử dụng thư viện `pytest` hoặc `unittest`) chạy được và tự động xác thực thành công các hành vi lỗi và sau khi sửa lỗi của API.