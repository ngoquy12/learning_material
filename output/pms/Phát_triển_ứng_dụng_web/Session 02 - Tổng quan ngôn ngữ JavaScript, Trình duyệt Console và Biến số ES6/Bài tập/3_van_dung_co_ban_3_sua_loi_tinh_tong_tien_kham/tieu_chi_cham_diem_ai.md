# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi tính tổng tiền khám bệnh và xuất phiếu thông báo — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code `var totalFee = consultationFee + testingFee;` thực hiện phép cộng trên hai chuỗi chưa ép kiểu.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ thông tin dòng 2 và dòng 3 trong bảng Test Case (đầu ra bị lỗi, đầu ra mong đợi, vị trí dòng lỗi và nguyên nhân logic về kiểu dữ liệu String).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Ép kiểu dữ liệu chính xác:** Áp dụng `Number()` ép kiểu thành công cho hai tham số chi phí đầu vào, tính toán chính xác tổng chi phí thanh toán (ví dụ: `200000 + 50000 = 250000`).
*   **[20 điểm] Chuẩn hóa biến ES6 và Naming Convention:**
    *   Loại bỏ 100% từ khóa `var`.
    *   Sử dụng đúng `const` cho các giá trị không bị gán lại và `let` cho các biến thay đổi.
    *   Đổi tên biến `Patient_Name` thành `patientName` chuẩn `camelCase`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Sử dụng Template Literals:** Đóng gói chuỗi thông báo kết quả sạch đẹp, dễ đọc bằng dấu backticks `` `...${}...` ``.
*   **[10 điểm] Hiển thị kết quả ra DOM & Console:** Xuất đúng thông tin thông báo phiếu khám ra Developer Console và gán thành công vào thuộc tính `textContent` của thẻ HTML có id `appointment-summary`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được cơ chế trả về dữ liệu của hàm `prompt()` trong trình duyệt luôn là kiểu `String` và sự khác biệt giữa phép toán `+` khi thao tác với String (nối chuỗi) so với Number (cộng số học).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn Javascript trình bày rõ ràng, thụt lùi dòng chuẩn, có chú thích bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tạo đúng cấu trúc tệp `index.html` và `app.js`, đẩy lên GitHub repository theo định dạng thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu hóa nhập liệu:** Thực hiện ép kiểu trực tiếp `Number(prompt(...))` gọn gàng ngay tại thời điểm khai báo biến.
