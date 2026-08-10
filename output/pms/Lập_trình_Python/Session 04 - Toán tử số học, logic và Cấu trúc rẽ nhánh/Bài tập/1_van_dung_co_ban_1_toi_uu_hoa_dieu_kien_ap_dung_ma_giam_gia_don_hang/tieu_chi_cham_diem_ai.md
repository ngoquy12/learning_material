### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Tối ưu hóa điều kiện áp dụng mã giảm giá đơn hàng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng lệnh chứa toán tử `or` sai lầm (`orderValue >= 500000 or totalOrders >= 10`) gây ra việc duyệt sai đơn hàng chưa đủ giá trị.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện bảng tối thiểu 3 test case chỉ rõ Input, Buggy Output hiện tại và Expected Output chính xác theo yêu cầu nghiệp vụ.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa triệt để điều kiện để đơn hàng chỉ được chấp nhận khi đạt ĐỒNG THỜI 3 điều kiện (`order_value >= 500000` AND `total_orders >= 5` AND `location in ("HANOI", "HCM")` hoặc `(location == "HANOI" or location == "HCM")`).
*   **[20 điểm] Phẳng hóa điều kiện (Anti-Arrow Pattern):** Loại bỏ cấu trúc `if` lồng 5 cấp cũ, chuyển thành cấu trúc phẳng sử dụng `if - elif - else` rõ ràng, dễ đọc.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra và phản hồi chính xác khi giá trị đơn hàng `<= 0` hoặc số lượng đơn hàng `< 0`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý chuẩn hóa chuỗi `location` (ví dụ chuyển về viết hoa `.upper()` hoặc `.strip()`) để tránh lỗi do người dùng nhập `"hanoi"` hoặc `"hcm "`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tác hại của mã nguồn lồng nhau quá sâu (Arrow Anti-Pattern) đối với khả năng đọc hiểu và bảo trì phần mềm trong môi trường thực tế.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đạt 100% chuẩn PEP 8 (thụt lề 4 spaces, đặt tên biến `snake_case`, bổ sung Type Hints đầy đủ).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session04_Ex01`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết các câu lệnh `assert` hoặc file test kiểm thử tự động các trường hợp biên của hàm đã refactor.