### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi tính tổng tiền hóa đơn POS tại quầy Highlands Coffee — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng các dòng mã nguồn xảy ra lỗi chuyển đổi kiểu dữ liệu (`item_price`, `quantity`, `cash_given` đang ở dạng `str`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác thông tin 2 kịch bản kiểm thử còn thiếu (STT 2 và STT 3) trong bảng báo cáo Test Case theo đúng định dạng mẫu.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Ép kiểu dữ liệu đầu vào thành công từ chuỗi `str` sang `int` hoặc `float` trước khi thực hiện phép toán `*` và `-`.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Xuất ra kết quả tính toán chính xác tổng tiền hóa đơn và tiền thừa trả lại cho khách hàng theo đúng ngữ cảnh thực tế của quầy thu ngân Highlands POS.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Đảm bảo dữ liệu số lượng (`quantity`) là số nguyên dương và đơn giá (`item_price`) không bị lỗi khi người dùng nhập số lẻ/số nguyên.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Chương trình không bị ngắt đột ngột (crash) trong quá trình thực thi tính toán và in ra thông tin định dạng hóa đơn rõ ràng.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao hàm `input()` trong Python 3 luôn mặc định trả về kiểu chuỗi (`str`), và nêu tác hại của việc quên ép kiểu dữ liệu trong các phần mềm tài chính/POS bán hàng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến bằng tiếng Anh đúng chuẩn (snake_case), trình bày mã nguồn thụt lùi dòng sạch sẽ, chú thích mã nguồn bằng tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub theo đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex1`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Định dạng lại số tiền hiển thị có dấu phân cách hàng nghìn (ví dụ: `78,000 VNĐ` hoặc `78.000 VNĐ`) để tăng trải nghiệm người dùng trên hóa đơn POS.