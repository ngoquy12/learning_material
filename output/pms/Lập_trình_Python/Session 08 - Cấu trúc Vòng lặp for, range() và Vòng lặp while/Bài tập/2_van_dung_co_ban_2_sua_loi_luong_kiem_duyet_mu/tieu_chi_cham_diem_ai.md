### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi luồng kiểm duyệt mượn sách trong LIBRARY_WMS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code `print("Đã xác nhận mượn thành công...")` nằm sai thứ tự so với các khối `if ... continue` và `if ... break`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác các dòng STT 2 và STT 3 trong Bảng phân tích Test Case (mô tả đúng Buggy Output, Expected Output và nguyên nhân tại `book_id = 8` và khi vòng lặp dừng khẩn cấp).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh thứ tự thực thi câu lệnh sao cho sách mã 4 bị bỏ qua chính xác, sách mã 8 ngắt vòng lặp lập tức mà không ghi nhận mượn thành công.
*   **[20 điểm] Cấu trúc điều khiển chuẩn xác:** Sử dụng đúng cú pháp `for book_id in range(1, 11)`, câu lệnh `continue`, `break` và khối `else` ứng với vòng lặp `for`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Kiểm soát phạm vi dữ liệu (range):** Sử dụng chính xác `range(1, 11)` để duyệt đúng 10 mã sách từ 1 tới 10 theo yêu cầu.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo khi gặp mã rủi ro (8), tiến trình dừng ngay lập tức và khối `else` của vòng lặp không bị kích hoạt ngoài ý muốn.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Trả lời câu hỏi tự luận:** Trả lời rõ ràng bản chất cơ chế hoạt động của khối `else` đi kèm vòng lặp `for` (chỉ chạy khi vòng lặp kết thúc bình thường, bị bỏ qua nếu vòng lặp thoát bằng `break`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến chuẩn `snake_case` (ví dụ: `book_id`), thụt lề 4 khoảng trắng đúng chuẩn PEP 8, có chú thích bằng tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session08_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Mở rộng kịch bản kiểm thử:** Viết thêm khối lệnh kiểm thử độc lập cho trường hợp danh sách sách không chứa mã rủi ro (ví dụ `range(1, 4)`) để chứng minh khối `else` hoạt động chính xác khi hoàn thành 100% quy trình.