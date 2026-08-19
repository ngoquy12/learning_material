# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế Tiến trình Kiểm duyệt Danh mục Sách Trả Tự động — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản lỗi thường gặp — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa rõ ràng các biến đầu vào, đầu ra, quy tắc phân loại mã tài liệu (hợp lệ, lỗi nhẹ, vi phạm nghiêm trọng) mang tính thực tế và sáng tạo.
*   **[15 điểm] Chủ động phát hiện sai sót dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 kịch bản lỗi biên thực tế (dải mã không hợp lệ, lỗi xảy ra ở biên bắt đầu/kết thúc, lô sách toàn bộ bị skipped...) và đưa ra phương án xử lý thỏa đáng.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ đúng cú pháp Mermaid Flowchart thể hiện trọn vẹn vòng lặp `for`, các nhánh rẽ `break`, `continue` và khối `else`. Sử dụng chuẩn 5 dạng hình khối (Oval cho Start/End, Parallelogram cho I/O, Rectangle cho Process, Diamond cho Decision).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày mạch lạc luồng chuyển đổi trạng thái của hệ thống từ lúc khởi chạy quét lô sách đến khi kết thúc an toàn hoặc ngắt khẩn cấp.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Viết mã nguồn Python chạy đúng logic thiết kế, khai thác chính xác sức mạnh của `for`, `range()`, `break`, `continue` và khối `else`. Tuyệt đối không vi phạm phạm vi kiến thức bị cấm (`while`, `list`, `dict`, `def`, `class`...).
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Tính toán và thống kê chính xác các chỉ số nghiệp vụ (ví dụ: số sách hợp lệ, số sách bị bỏ qua, tổng tiền phạt tích lũy) thông qua các biến đếm/biến dồn trong quá trình lặp.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Triển khai đầy đủ các câu lệnh điều kiện guard-clause để xử lý các sai sót dữ liệu đã liệt kê tại Phần 2, in ra thông báo hướng dẫn rõ ràng cho người dùng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & PEP 8:** Mã nguồn trình bày sạch sẻ, thụt lề 4 dấu cách chuẩn PEP 8, tên biến bằng tiếng Anh chuẩn ngữ nghĩa (`snake_case`), chú thích tiếng Việt rõ ràng.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex13`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Audit / Thống kê nâng cao:** Thiết kế thêm biến theo dõi tỉ lệ phần trăm sách bị bỏ qua hoặc cơ chế đề xuất phương án xử lý thủ công cho từng mã sách bị `continue` sau khi kết thúc chương trình.
