### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế Module Đóng gói Quản lý Vé và Check-in Sự kiện Concert — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa rõ ràng mô hình dữ liệu cho từng thao tác (Phát hành vé, Tính tiền, Check-in, Báo cáo Stats). Cấu trúc dữ liệu có tính mở rộng cao và thể hiện đầy đủ các trường thông tin cần thiết.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê ít nhất 3 bẫy lỗi nghiệp vụ thực tế (Ví dụ: `discountRate` truyền giá trị `0`, vượt quá số lượng 4 vé/lần mua, mã vé trùng lặp, check-in mã chưa phát hành hoặc đã check-in trước đó).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện đầy đủ luồng xử lý từ lúc khách chọn vé -> tính tiền -> lưu trữ vé vào Closure -> thực hiện check-in tại cổng. Tuân thủ 100% quy chuẩn hình dạng chuẩn (Oval cho Start/End, Song song cho Input/Output, Chữ nhật cho Process, Thoi cho Decision).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ cơ chế đóng gói phạm vi (Scope isolation) bằng Closure giúp bảo vệ dữ liệu vé không bị can thiệp bởi biến toàn cục như thế nào.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công Closure & Arrow Functions:** Sử dụng đúng cú pháp ES6 Arrow Functions, xây dựng thành công factory function trả về object chứa các hàm thao tác truy cập biến private qua Lexical Scope.
*   **[15 điểm] Xử lý tham số mặc định chuẩn xác:** Áp dụng Tham số mặc định (Default Parameters) cho thuế VAT và mức giảm giá. Không vi phạm lỗi logic của toán tử `||` khi đối số truyền vào có giá trị bằng `0`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết code validation chặt chẽ cho các lỗi biên đã nêu ở Phần 1, trả về thông báo lỗi rõ ràng và không làm sập chương trình.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn đặt tên:** Mã nguồn tổ chức mô-đun hóa tốt, tên biến/hàm đặt bằng tiếng Anh chuẩn `camelCase`, comment giải thích logic rõ ràng bằng tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc thư mục đúng quy định `[Tên Lớp]_[Môn Học]_Session14_Ex13`, file README mô tả chi tiết kịch bản chạy thử nghiệm.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung hàm ghi nhật ký thao tác (Audit Log) theo thời gian thực khép kín bên trong Closure hoặc hàm hủy/hoàn vé (Cancel Ticket) khôi phục lại hạn ngạch chưa bán của khu vực.