### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi tính phí dịch vụ check-in và chọn vị trí ghế máy bay — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ vị trí dòng lệnh thiếu từ khóa `break;` trong khối `case 3` của câu lệnh `switch-case`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác thông tin cho các dòng STT 2 và STT 3 trong bảng báo cáo kiểm thử (Input, Buggy Output, Expected Output, Failing Line, Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Bổ sung đầy đủ lệnh `break;` vào cuối tất cả các trường hợp `case` trong cấu trúc `switch-case`, đảm bảo không bị lỗi trôi lệnh (fall-through).
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng cấu trúc rẽ nhánh chính xác để xử lý trường hợp mã hạng vé không hợp lệ (`default`), gán đúng tên hạng và tính tổng phí bằng 0 VNĐ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra số cân hành lý không được là số âm (`baggageWeight >= 0`). Nếu âm thì thông báo dữ liệu không hợp lệ.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo khi `ticketClass` nhận giá trị bất kỳ nằm ngoài tập {1, 2, 3}, chương trình vẫn chạy an toàn, không sinh lỗi Runtime hoặc kết quả NaN.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích bản chất hiện tượng trôi lệnh (fall-through) trong `switch-case` của JavaScript và nêu rõ trường hợp nào trong thực tế lập trình chủ động áp dụng kỹ thuật fall-through có mục đích.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến rõ ràng theo tiếng Anh (`ticketClass`, `baggageWeight`, `seatFee`), thụt lề chuẩn 2 spaces, ghi chú rõ ràng bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub theo đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết đoạn mã kịch bản tự động kiểm thử cả 3 trường hợp hạng vé (Eco, Deluxe, Business) và in ra kết quả thông qua console (PASSED / FAILED).