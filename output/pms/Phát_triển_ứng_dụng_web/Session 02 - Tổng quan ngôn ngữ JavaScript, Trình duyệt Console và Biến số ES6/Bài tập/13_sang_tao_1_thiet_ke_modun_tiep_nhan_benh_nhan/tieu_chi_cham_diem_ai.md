# **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Thiết kế mô-đun tiếp nhận bệnh nhân và dự tính chi phí khám — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa đầy đủ bảng biến Input/Output chuẩn ES6 (`camelCase`), xác định rõ kiểu dữ liệu (`String`, `Number`) và mô tả mục đích nghiệp vụ.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Liệt kê ít nhất 3 bẫy dữ liệu thực tế (nhập chuỗi không hợp lệ vào prompt số, bấm hủy prompt trả về null, cộng chuỗi do quên ép kiểu `Number()`).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid đúng chuẩn kỹ thuật 5 hình khối (Oval `([ ])`, Bình hành `[/ /]`, Thoi `?`, Chữ nhật `[" "]`), thể hiện đúng luồng dữ liệu từ Kiosk nhập vào đến khi xuất thông báo.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ ràng các bước chuyển đổi dữ liệu từ dạng Chuỗi (`String`) sang Số (`Number`) và đóng gói thành Chuỗi kết quả (`Template Literals`).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Khai báo biến `const`/`let` chuẩn xác, thực hiện các phép tính số học (tổng phí, giảm trừ BHYT, tiền thanh toán) đúng công thức nghiệp vụ.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Đóng gói thông tin phiếu đăng ký chuyên nghiệp bằng Template Literals (`${}`), hiển thị chính xác kết quả qua `console.log()` và `alert()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Xử lý ép kiểu an toàn với `Number()`, có lời nhắn hướng dẫn rõ ràng trên giao diện prompt/alert khi dữ liệu chưa hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Mã nguồn viết bằng ES6+, phân tách HTML và JS chuyên nghiệp qua thẻ `<script src="app.js"></script>`, tên biến tiếng Anh rõ nghĩa (`patientName`, `baseFee`, `totalPayment`).
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy đủ file `index.html`, `app.js` và báo cáo thiết kế lên GitHub đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Trình bày chi tiết log kiểm toán (audit log) định dạng đẹp mắt trong `console.log` sử dụng định dạng chuỗi nhiều dòng bằng Template Literals.
