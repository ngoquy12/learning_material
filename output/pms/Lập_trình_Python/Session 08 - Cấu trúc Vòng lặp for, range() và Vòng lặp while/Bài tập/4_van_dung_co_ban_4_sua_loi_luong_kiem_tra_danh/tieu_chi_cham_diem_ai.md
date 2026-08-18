### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi luồng kiểm tra danh mục mượn sách theo lô — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
* **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ các dòng mã (dòng 12-13 trong mã legacy) thực thi lệnh in thành công và tăng biến đếm `processed_count` trước các câu lệnh rẽ nhánh `if`.
* **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ các dòng 2 và 3 trong bảng Test Case với đầy đủ thông tin: Input, Buggy Output, Expected Output, Dòng code gây lỗi và Giải thích nguyên nhân.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
* **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Đặt các khối điều kiện `if book_id == 104:` (chứa `continue`) và `if book_id == 107:` (chứa `break`) lên trước hành động in phê duyệt và tăng biến đếm.
* **[20 điểm] Vận dụng chuẩn xác khối else của vòng lặp for:** Đảm bảo khối `else` hiển thị tổng số `processed_count` chỉ chạy khi không chạm phải câu lệnh `break` (ví dụ: quét dải 101-105 sẽ chạy `else`, quét dải 101-108 gặp 107 sẽ bị ngắt và không chạy `else`).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
* **[10 điểm] Validate dải mã số hợp lệ:** Đảm bảo `start_id <= end_id` trước khi chạy vòng lặp `range()`.
* **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp nếu `start_id` hoặc `end_id` truyền vào là số âm hoặc không phải số nguyên.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
* **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích tại sao trong lập trình nghiệp vụ, nguyên tắc "Guard Clauses / Fail-Fast" (kiểm tra và loại bỏ ngoại lệ/lỗi trước) lại cực kỳ quan trọng so với việc ghi nhận dữ liệu trước.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết đúng tiêu chuẩn Python PEP 8 (thụt lề 4 dấu cách, tên biến dạng `snake_case`, chú thích rõ ràng bằng tiếng Việt).
* **[5 điểm] Tuân thủ nộp bài GitHub:** Nộp bài lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
* **[10 điểm] Viết Kịch bản Kiểm thử tự động:** Đóng gói đoạn mã kiểm tra thành một kịch bản chạy thử nghiệm nhiều dải `start_id`, `end_id` khác nhau và so sánh đầu ra tự động.