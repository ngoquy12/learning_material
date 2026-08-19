# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết kế mô-đun tổng hợp phiếu đăng ký khám và tính chi phí phòng khám tự động — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự xây dựng bảng I/O Schema đầy đủ các trường thông tin (tên bệnh nhân, mã BHYT, tiền khám gốc, phí phụ thu, tỷ lệ giảm trừ BHYT, tổng tiền) với kiểu dữ liệu chính xác, phân định biến `const`/`let` và tên biến chuẩn `camelCase`.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phân tích và chỉ ra ít nhất 3 bẫy lỗi tiềm ẩn (lỗi nối chuỗi do thiếu `Number()`, lỗi `TypeError` khi reassign `const`, lỗi dữ liệu `NaN` khi tính toán số học, hoặc lỗi script chặn DOM loading nếu đặt sai vị trí thẻ `<script>`).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện đầy đủ vòng đời xử lý từ khi trình duyệt tải HTML, V8 Engine nạp `app.js`, thu thập `prompt()`, ép kiểu dữ liệu, tính toán chi phí, và xuất báo cáo.
*   **[10 điểm] Thiết kế chuẩn hình khối Mermaid:** Đảm bảo tuân thủ nghiêm ngặt quy tắc hình khối (Terminator `([ ])`, Input/Output `[/ /]`, Process `[" "]`, Decision `?`).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Viết mã lệnh thu thập thông tin qua `prompt()`, ép kiểu `Number()`, tính toán đúng logic chi phí khám (áp dụng giảm giá 80% BHYT cho tiền khám gốc + cộng phí dịch vụ).
*   **[15 điểm] Định dạng báo cáo chuyên nghiệp:** Đóng gói toàn bộ kết quả bằng Chuỗi mẫu (Template Literals) hiển thị thông tin phiếu khám sạch đẹp, trực quan ra `console.log()` và `alert()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xử lý ép kiểu an toàn và quản lý phạm vi biến chính xác, tránh các cạm bẫy ô nhiễm phạm vi toàn cục hoặc tính toán sai lệch do nối chuỗi `String`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn ES6:** Tách biệt rõ ràng tệp `index.html` và `app.js`. Đặt tên biến hoàn toàn bằng Tiếng Anh (`camelCase`), có chú thích bằng Tiếng Việt có dấu. Không dùng từ khóa `var`.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo repository theo đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session02_Ex15`), commit mã nguồn rõ ràng và kèm tệp README hướng dẫn chạy ứng dụng qua Live Server.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung đoạn mã ghi vết nhật ký kiểm toán (Audit Log) trên Console hiển thị thời gian khởi chạy phiếu khám và kiểm tra trạng thái bộ nhớ/phiên bản Node runtime.
