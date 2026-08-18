### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 3] Sửa lỗi cập nhật thuộc tính và đóng gói JSON hồ sơ đặt phòng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác dòng code gán `undefined` thay vì dùng `delete` và dòng code cố gắng truy cập trực tiếp thuộc tính từ chuỗi JSON mà chưa parse.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 100% các ô trống (`...`) ở hàng 2 và 3 trong bảng Test Case với đầy đủ Input, Buggy Output, Expected Output, Failing Line và Logic Note giải thích cơ chế chuỗi JSON và toán tử `delete`.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Sử dụng toán tử delete đúng cách:** Sử dụng cú pháp `delete bookingObj.tempAuthToken;` hoặc `delete bookingObj["tempAuthToken"];` để loại bỏ hẳn key khỏi Object trước khi serialize.
*   **[20 điểm] Chuyển đổi và giải mã JSON chuẩn xác:** Thực hiện đúng `JSON.stringify()` khi đóng gói và `JSON.parse()` khi muốn khôi phục chuỗi JSON thành Object để truy cập thuộc tính `"early-checkin-fee"`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate đối tượng đầu vào cơ bản:** Kiểm tra `bookingObj` hợp lệ (không null/undefined và là kiểu Object) trước khi thao tác thuộc tính.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp tính phụ phí an toàn nếu `basePrice` thiếu hoặc không phải là số hợp lệ.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Phân tích lý thuyết chuyên sâu:** Giải thích được sự khác biệt giữa việc gán `obj.key = undefined` (vẫn còn key trong `Object.keys()`) và dùng `delete obj.key` (loại bỏ hoàn toàn key khỏi bộ nhớ).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo chuẩn camelCase trong JavaScript, định dạng mã nguồn thụt lùi rõ ràng, comment tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 12_Ex3`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xây dựng hàm kiểm định tự động:** Viết thêm đoạn mã kiểm thử tự động (Assertion / Console check) so sánh `JSON.parse(resultPayload)["tempAuthToken"] === undefined` và xác nhận key không tồn tại trong chuỗi JSON.