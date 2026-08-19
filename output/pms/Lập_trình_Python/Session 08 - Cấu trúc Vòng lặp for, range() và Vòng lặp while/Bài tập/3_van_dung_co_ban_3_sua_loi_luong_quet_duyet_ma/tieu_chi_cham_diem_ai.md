# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi luồng quét duyệt mã tài liệu thư viện — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code chứa câu lệnh `break` sai mục đích tại vị trí kiểm tra mã `104` (dòng 10).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ thông tin cho STT 2 và STT 3 trong bảng Test Case, mô tả rõ Buggy Output vs Expected Output và giải thích nguyên nhân logic làm ngắt luồng xử lý.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Thay thế đúng câu lệnh `break` thành `continue` tại trường hợp mã `104`, giữ nguyên `break` tại mã `108`.
*   **[20 điểm] Hoạt động chính xác của khối else trong vòng lặp:** Khối `else` hoạt động chuẩn xác (chỉ in thông báo thành công khi không chạm phải từ khóa `break` ở mã `108`).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate dải dữ liệu quét:** Sử dụng đúng tham số hàm `range(101, 110)` để quét đủ dải mã sách từ 101 đến 109.
*   **[10 điểm] Kiểm tra điều kiện chính xác:** Viết đúng câu lệnh điều kiện `if book_id == 104:` và `if book_id == 108:`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Trả lời câu hỏi phân tích:** Nêu được sự khác biệt cốt lõi giữa `break` (ngắt toàn bộ vòng lặp) và `continue` (bỏ qua lượt lặp hiện tại), đồng thời giải thích được điều kiện để khối `else` của vòng lặp `for` được thực thi.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng (`book_id`), tuân thủ chuẩn PEP 8 (thụt lề 4 khoảng trắng, câu lệnh rõ ràng, chú thích Tiếng Việt có dấu).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tạo đúng thư mục theo cấu trúc `[Tên Lớp]_[Môn Học]_Session08_Ex3` và đẩy code lên repository công khai.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Mở rộng luồng quét linh hoạt:** Cho phép người dùng nhập dải mã bắt đầu và dải mã kết thúc từ bàn phím qua hàm `input()` và thực hiện quét kiểm tra với các quy tắc nghiệp vụ tương tự.
