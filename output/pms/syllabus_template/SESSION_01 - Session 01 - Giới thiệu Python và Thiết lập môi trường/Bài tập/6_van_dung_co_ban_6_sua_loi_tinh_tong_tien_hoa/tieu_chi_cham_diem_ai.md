# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính tổng tiền hóa đơn order tại quầy Highlands POS — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng 8 trong đoạn mã mẫu là nơi xảy ra phép cộng hai chuỗi kí tự chưa được ép kiểu số.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành chính xác các giá trị thiếu trong Bảng Báo cáo Kịch bản Kiểm thử cho STT 2 và STT 3 (tính đúng kết quả lỗi và kết quả mong đợi).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa lỗi ép kiểu dữ liệu thành công (`float(unit_price)`, `float(topping_fee)`, `int(quantity)`), đảm bảo tổng hóa đơn và tiền thừa trả khách được tính toán chính xác 100%.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Thực hiện chuyển đổi kiểu dữ liệu phù hợp với quy chuẩn xử lý nhập xuất chuẩn CLI của Python, không làm ứng dụng phát sinh lỗi ngầm.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Ép kiểu chính xác các biến nhập vào thành `float` cho số tiền và `int` cho số lượng ly.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo xuất ra kết quả minh bạch, format đẹp mắt, hiển thị rõ đơn vị tính `VNĐ`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn lý do tại sao hàm `input()` trong Python mặc định trả về kiểu dữ liệu `str` và tầm quan trọng của việc ép kiểu dữ liệu trước khi thực hiện các toán tử đại số (`+`, `-`, `*`, `/`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến bằng tiếng Anh chuẩn nghiệp vụ (`unit_price`, `topping_fee`, `total_bill`), chú thích bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex6`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] ĐỊnh dạng đầu ra số tiền:** Sử dụng hàm định dạng chuỗi (String Formatting) để hiển thị số tiền có khoảng cách phân cách hoặc làm tròn số tiền lẻ đẹp mắt khi in hóa đơn.
