### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi tính tổng hóa đơn đặt phòng khách sạn khi có phụ thu check-in sớm và thuế VAT — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
* **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã nguồn thực hiện sai thứ tự ưu tiên toán tử và sử dụng sai biến khi tính tiền thuế VAT.
* **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác kết quả bị lỗi (Buggy Output), kết quả kỳ vọng (Expected Output) cùng lời giải thích nguyên nhân cho 2 testcase còn thiếu (STT 2 và STT 3).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
* **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa đúng biểu thức tính thuế VAT (`vat_amount = subtotal * 0.10`), trả về tổng thanh toán chính xác cho mọi trường hợp dữ liệu.
* **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Đảm bảo các phép toán thực hiện chính xác với kiểu dữ liệu số thực (`float`), không phát sinh lỗi ép kiểu dữ liệu.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
* **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra các giá trị đầu vào mang ý nghĩa thực tế (giá phòng >= 0, số đêm >= 1).
* **[10 điểm] Bắt lỗi an toàn hệ thống:** Hàm tính toán không bị treo hoặc crash khi gặp tham số biên.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
* **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được quy tắc thứ tự ưu tiên của toán tử số học trong Python (phép nhân `*` có độ ưu tiên cao hơn phép cộng `+`) và tầm quan trọng của việc sử dụng cặp dấu ngoặc `()` để nhóm các biểu thức đại số.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
* **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm rõ nghĩa theo chuẩn `snake_case`, khai báo type hints chuẩn PEP 8.
* **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository theo đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
* **[10 điểm] Viết Unit Test tự động:** Viết script kiểm thử tự động sử dụng `assert` để kiểm tra kết quả hàm `calculate_booking_invoice` trên nhiều kịch bản testcase khác nhau.