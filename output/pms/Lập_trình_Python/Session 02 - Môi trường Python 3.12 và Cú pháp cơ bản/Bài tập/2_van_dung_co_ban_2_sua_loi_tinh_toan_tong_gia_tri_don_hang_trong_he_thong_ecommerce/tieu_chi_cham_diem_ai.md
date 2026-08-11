### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi tính toán tổng giá trị đơn hàng trong hệ thống E-Commerce — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ rõ dòng mã nguồn thực hiện phép cộng chuỗi do chưa gọi các hàm ép kiểu `float()` và `int()` trên biến thu được từ `input()`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện bảng báo cáo kiểm thử tối thiểu 3 test case theo đúng mẫu HTML, so sánh rõ ràng giữa kết quả thực tế bị lỗi ghép chuỗi và kết quả kỳ vọng đúng số học.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Ép kiểu chính xác các biến đầu vào (`float` cho đơn giá và phí ship, `int` cho số lượng), thực hiện đúng công thức nhân số lượng và cộng phí vận chuyển.
*   **[20 điểm] Xử lý xuất dữ liệu chuẩn dòng lệnh:** Cấu hình chính xác các tham số `sep` và `end` trong các lệnh `print()` theo đúng yêu cầu hiển thị hóa đơn E-Commerce.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ép kiểu ngay sau khi nhận dữ liệu từ `input()` để tránh việc lan truyền dữ liệu kiểu `str` sang các bước tính toán tiếp theo.
*   **[10 điểm] An toàn dữ liệu số học:** Đảm bảo các tính toán tài chính giữ nguyên giá trị kiểu số thực (`float`) mà không làm mất phần thập phân của tiền tệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn nguyên nhân vì sao hàm `input()` trong Python luôn trả về kiểu `str` và tác hại nghiêm trọng của toán tử `+` khi thao tác trên kiểu chuỗi trong các phần mềm thương mại điện tử.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ chuẩn PEP 8 (thụt lề 4 spaces, tên biến `snake_case`, ghi chú tiếng Việt có dấu rõ ràng).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session02_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Kiểm thử giá trị biên:** Thực hiện thêm kịch bản kiểm thử cho các trường hợp đặc biệt như đơn giá chứa số thập phân lẻ, số lượng bằng 1, hoặc phí giao hàng bằng 0 VNĐ và trình bày kết quả sạch đẹp trong báo cáo.