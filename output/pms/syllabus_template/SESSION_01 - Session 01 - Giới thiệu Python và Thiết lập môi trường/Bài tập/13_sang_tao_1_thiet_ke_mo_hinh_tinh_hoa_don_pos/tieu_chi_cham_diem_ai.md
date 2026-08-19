# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế mô hình tính hóa đơn POS tích hợp ưu đãi và VAT linh hoạt — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Lập bảng mô tả đầy đủ các biến đầu vào và đầu ra, quy định rõ ràng kiểu dữ liệu (`int`, `float`, `str`, `bool`) phù hợp với nghiệp vụ hóa đơn Highlands POS.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê tối thiểu 3 kịch bản bẫy dữ liệu đầu vào bất thường (như nhập sai kiểu dữ liệu số, nhập số âm, giảm giá lớn hơn 100%) và mô tả hướng guards/xử lý logic tương ứng.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Trình bày sơ đồ luồng dữ liệu bằng Mermaid tuân thủ chính xác chuẩn hình học (Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho Process, Diamond cho Decision).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ ràng trình tự các bước biến đổi dữ liệu từ dạng chuỗi (`str`) nhập từ CLI sang số học (`int`/`float`) để thực hiện các phép toán tổng tiền, chiết khấu và thuế.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Mã nguồn Python thực hiện chính xác phép tính nâng size, cộng phí topping, trừ chiết khấu thành viên và cộng thuế VAT theo đúng thiết kế đã đề xuất.
*   **[15 điểm] Định dạng hiển thị hóa đơn POS chuyên nghiệp:** Sử dụng f-string hoặc các phương thức định dạng chuỗi để in ra hóa đơn CLI đẹp mắt, căn chỉnh lề rõ ràng, hiển thị số tiền có phân tách hoặc ghi chú đơn vị tính VNĐ.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Triển khai các câu lệnh kiểm tra dữ liệu hoặc thông báo hướng dẫn lại khi nhân viên nhập sai dữ liệu biên đã xác định trong Phần 2.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn định danh:** Đặt tên biến và hàm hoàn toàn bằng tiếng Anh có ý nghĩa (ví dụ: `base_price`, `topping_fee`, `discount_rate`, `vat_rate`). Chú thích giải thích mã nguồn bằng 100% tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc thư mục chuẩn `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex13`, có tệp README.md hướng dẫn chạy chương trình và mô tả thiết kế.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung đoạn mã mô phỏng việc tạo chuỗi mã hóa đơn duy nhất (Invoice ID) dựa trên thời gian/thông tin đơn hàng và xuất lịch sử nhật ký (Audit Log) tóm tắt hóa đơn phục vụ đối soát ca làm việc của thu ngân.
