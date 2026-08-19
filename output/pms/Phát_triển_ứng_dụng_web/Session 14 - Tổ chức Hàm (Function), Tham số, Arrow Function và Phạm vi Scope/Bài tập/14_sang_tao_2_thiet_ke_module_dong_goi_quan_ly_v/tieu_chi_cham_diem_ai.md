### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Module Đóng gói Quản lý Vé & Đặt chỗ Concert bằng Closure — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc tham số đầu vào và dữ liệu trả về cho hàm khởi tạo Closure và các hàm thao tác con (đơn hàng vé, mã QR, giá trị chiết khấu) đầy đủ kiểu dữ liệu và mô tả rõ ràng.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 bẫy bối cảnh nghiệp vụ thực tế (ví dụ: mua vé vượt hạn ngạch 4 vé/tài khoản, kho hết vé, chiết khấu âm, quét mã QR trùng lặp) và đề xuất cách xử lý mạch lạc.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid mô tả chính xác vòng đời dữ liệu từ khởi tạo Closure đến check-in. Tuân thủ 100% quy chuẩn 5 dạng hình khối (Terminator, Input/Output, Decision, Process, Flowline).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ cơ chế chuyển đổi trạng thái của mã QR check-in (từ Chưa sử dụng -> Đã check-in) và cơ chế đóng gói bảo vệ biến private bằng Lexical Scope.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Xây dựng hàm tạo bộ quản lý vé bằng Closure + Arrow Function; tính đúng chiết khấu Early Bird (15%), xử lý phí xuất vé mặc định (20.000 VNĐ) qua Default Parameter.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Triển khai các phương thức truy xuất báo cáo (ví dụ: danh sách vé đã quét check-in, tổng doanh thu thực thu) từ dữ liệu private đóng gói trong Closure.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các điều kiện kiểm tra (guards) để chặn ngay khi người dùng cố tình mua > 4 vé/tài khoản, mua khi hết vé kho, hoặc quét check-in lại mã QR đã dùng với thông báo lỗi cụ thể.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết bằng ES6+, đặt tên biến/hàm bằng tiếng Anh theo chuẩn camelCase, chú thích tiếng Việt có dấu rõ ràng, tuyệt đối không lạm dụng biến toàn cục `var` hay `class`.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc thư mục repository đúng quy định (`[Tên Lớp]_[Môn Học]_Session14_Ex14`), file README trình bày mạch lạc kịch bản chạy thử nghiệm.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Triển khai thêm tính năng hủy vé đặt trước thời hạn (hoàn lại hạn ngạch cho kho và cho tài khoản) hoặc ghi vết nhật ký quét QR check-in kèm mốc thời gian thực thi (Timestamp log).