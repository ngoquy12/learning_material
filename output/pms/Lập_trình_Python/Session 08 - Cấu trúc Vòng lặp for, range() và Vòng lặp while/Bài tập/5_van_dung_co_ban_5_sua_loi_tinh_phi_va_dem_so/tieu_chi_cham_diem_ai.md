### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi tính phí và đếm số lượng trong vòng lặp quét sách thư viện — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ lỗi nằm ở việc đặt câu lệnh tăng `scanned_count += 1` và `total_processing_fee += 5000` trước điều kiện kiểm tra `if book_id == 4: continue`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ thông tin cho các dòng STT 2 và STT 3 trong bảng Test Case với giá trị đầu ra thực tế (lỗi), đầu ra kỳ vọng (đúng) và giải thích nguyên nhân rõ ràng.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh vị trí cộng tiền và biến đếm xuống sau các câu lệnh kiểm tra điều kiện `continue` và `break`, đảm bảo mã sách `4` không bị tính phí.
*   **[20 điểm] Xử lý đúng luồng điều khiển:** Sử dụng chính xác cấu trúc `for...in range()`, `continue`, `break` và khối `else` của vòng lặp để in báo cáo tổng kết khi kết thúc thành công.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Kiểm soát phạm vi giá trị:** Đảm bảo mã nguồn hoạt động chính xác với các khoảng `range(start_id, end_id)` khác nhau.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý đúng trường hợp vòng lặp bị dừng đột ngột bởi `break` (mã 8) thì khối `else` không được phép thực thi.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn về rủi ro của việc "thực hiện tác động side-effect (tăng biến, cập nhật dữ liệu) trước khi kiểm tra điều kiện lọc dữ liệu" trong lập trình phần mềm.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến rõ ràng bằng tiếng Anh (`book_id`, `scanned_count`, `total_processing_fee`), thụt lề 4 khoảng trắng chuẩn PEP 8.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Mở rộng kịch bản kiểm thử:** Thêm thông báo tổng số mã sách đã bị bỏ qua (đếm số sách lỗi mã 4) mà không dùng đến danh sách (List).