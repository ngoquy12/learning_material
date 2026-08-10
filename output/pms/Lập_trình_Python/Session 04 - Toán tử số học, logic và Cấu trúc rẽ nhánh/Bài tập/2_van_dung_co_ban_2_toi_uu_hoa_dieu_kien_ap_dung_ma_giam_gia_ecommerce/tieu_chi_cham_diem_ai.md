### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Tối ưu hóa điều kiện áp dụng mã giảm giá E-commerce — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi & vi phạm quy chuẩn:** Đánh giá đúng các vi phạm PEP 8 (tên biến viết tắt `v`, `val`, `a`, `cnt`, thụt lề 2 spaces, thiếu space quanh toán tử) và chỉ ra cấu trúc lồng nhau 5 cấp (Arrow Anti-Pattern).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp đầy đủ tối thiểu 3 test cases có đầu vào chi tiết, ghi rõ kết quả mã legacy và kết quả mong đợi chuẩn xác theo quy tắc nghiệp vụ.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng đúng logic rẽ nhánh để kiểm tra điều kiện độ tuổi (18 - 60), số lượng mặt hàng (>= 2) và điều kiện ưu đãi (`is_vip` hoặc `order_value >= 2000000`).
*   **[20 điểm] Phẳng hóa điều kiện thành công:** Loại bỏ tháp `if` lồng nhau, chuyển thành câu lệnh phẳng dạng `if / elif / else` sử dụng hợp lý các toán tử logic `and`, `or`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate thứ tự điều kiện ưu tiên:** Đặt các điều kiện vi phạm dừng sớm (Guard Clauses) hợp lý (ví dụ: kiểm tra độ tuổi hoặc số lượng sản phẩm trước).
*   **[10 điểm] Bắt lỗi thông báo chi tiết:** Xuất đúng các thông báo phản hồi tương ứng cho từng trường hợp từ chối (Độ tuổi không phù hợp, Số lượng không đủ, Không đủ điều kiện VIP/giá trị).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích chính xác ảnh hưởng tiêu cực của Arrow Anti-Pattern (khó đọc, khó test đầy đủ các nhánh branch coverage, dễ bỏ sót lỗi rò rỉ logic).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ tuyệt đối quy chuẩn PEP 8 (thụt lề 4 space, đặt tên biến `snake_case`, khoảng trắng quanh toán tử).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session04_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết kịch bản kiểm thử mở rộng:** Đưa ra đoạn mã thử nghiệm duyệt qua nhiều bộ dữ liệu thử nghiệm khác nhau mà không làm lặp mã.