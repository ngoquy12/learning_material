### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi tính toán chiết khấu và phạm vi biến trong module bán vé Ticketbox — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code gán mặc định sai bằng toán tử `||` (`discountRate || 0.15`) và dòng code rò rỉ biến toàn cục `orderTotalAmount`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành đầy đủ 3 dòng trong bảng Test Case, mô tả chi tiết đầu vào (Input), đầu ra thực tế lỗi (Buggy Output), đầu ra kỳ vọng (Expected Output) và giải thích nguyên nhân logic.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sử dụng đúng tham số mặc định ES6 `(quantity, baseUnitPrice, discountRate = 0.15, serviceFee = 30000) => ...`, đảm bảo khi truyền `discountRate = 0` thì tỷ lệ tính toán chính xác là 0%.
*   **[20 điểm] Đóng gói phạm vi biến (Local Scope):** Xóa bỏ biến toàn cục `orderTotalAmount`, khai báo biến tính toán cục bộ bằng `const`/`let` bên trong hàm và trả về trực tiếp giá trị hợp lệ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate điều kiện nghiệp vụ:** Kiểm tra chính xác điều kiện số lượng vé `quantity > 4` hoặc `quantity <= 0`, đơn giá `baseUnitPrice <= 0`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Ném lỗi chuẩn bằng `throw new Error(...)` với thông báo tiếng Việt rõ ràng và bọc lời gọi hàm trong khối `try...catch` ở chương trình chính.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Phân tích lý thuyết Falsy Values và Scope:** Trả lời rõ ràng lý do tại sao toán tử `||` thất bại với giá trị `0` trong JavaScript và giải thích nguy cơ gây ra lỗi dữ liệu khi sử dụng biến toàn cục cho các luồng xử lý đơn hàng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết bằng ES6+ chuẩn mực, thụt lùi dòng nhất quán, đặt tên biến/hàm theo chuẩn camelCase bằng tiếng Anh có ý nghĩa (`calculateTicketOrder`, `appliedDiscount`, `totalAmount`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tạo đúng thư mục và đẩy bài làm lên GitHub theo đúng cấu trúc yêu cầu: `[Tên Lớp]_[Môn Học]_Session14_Ex6`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết hàm kiểm thử tự động (Automated Test Suite):** Viết thêm một đoạn mã ngắn tự động chạy 4-5 test case khác nhau và in ra màn hình `PASS`/`FAIL` tương ứng với mỗi kịch bản.