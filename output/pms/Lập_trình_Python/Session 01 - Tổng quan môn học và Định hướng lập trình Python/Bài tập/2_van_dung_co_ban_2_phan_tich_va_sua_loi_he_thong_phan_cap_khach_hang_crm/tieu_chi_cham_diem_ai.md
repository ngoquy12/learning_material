### **Tiêu chí chấm điểm (AI)**
**[Phân tích và sửa lỗi hệ thống phân cấp khách hàng CRM] — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng các điểm yếu trong mã nguồn legacy bao gồm lỗi bỏ sót trường hợp `total_spent == 1000`, lỗi không xử lý số âm `< 0` và lỗi thiếu kiểm tra kiểu dữ liệu đầu vào.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp tối thiểu 3 trường hợp kiểm thử cụ thể trình bày đúng cấu trúc bảng (Input, Buggy Output, Expected Output) phản ánh đúng các lỗi logic thực tế.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa triệt để các điều kiện biên `0 <= total_spent < 1000`, `1000 <= total_spent < 5000`, và `total_spent >= 5000`, trả về đúng dictionary chỉ số SLA và Reps.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng `raise ValueError` cho dữ liệu chi tiêu âm và `raise TypeError` cho kiểu dữ liệu không hợp lệ với thông điệp rõ ràng.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Đảm bảo chặn thành công các giá trị rỗng, kiểu dữ liệu sai (string, list, None) trước khi thực hiện phép so sánh.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Hàm xử lý mượt mà, không làm đứt gãy chương trình khi gọi thử nghiệm với dữ liệu lỗi bằng khối `try...except` ngoài hàm.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tác hại của lỗi sai biên (Off-by-one boundary error) trong các hệ thống doanh nghiệp thực tế và đề xuất giải pháp phòng ngừa.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết đúng chuẩn PEP 8, đặt tên biến/hàm tiếng Anh chuẩn CRM domain (`total_spent`, `calculate_customer_tier_metrics`), chú thích tiếng Việt đầy đủ.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tạo repository và đẩy mã nguồn đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session01_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết các hàm/đoạn mã kiểm thử tự động (sử dụng câu lệnh `assert` hoặc khối kiểm thử) xác minh tự động tất cả các kịch bản biên và ngoại lệ.