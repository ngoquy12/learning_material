### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi xử lý hóa đơn đặt phòng và đóng gói JSON — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng code gán `undefined` thay vì `delete` (Dòng 16) và dòng đọc thuộc tính trực tiếp trên chuỗi JSON string (Dòng 22).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Đã hoàn thành chính xác 2 dòng Test Case còn thiếu (STT 2, STT 3) với các thông số dữ liệu đầu vào, đầu ra bị lỗi thực tế và đầu ra mong đợi chuẩn xác.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    - Dùng đúng cú pháp `delete bookingObj.tempSecurityCode` để loại bỏ thuộc tính khỏi đối tượng.
    - Chuyển đổi thành chuỗi JSON bằng `JSON.stringify()`.
    - Giải mã chuỗi JSON về Object bằng `JSON.parse()` và lấy đúng giá trị `totalAmount` cho `confirmedTotal`.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Sử dụng câu lệnh `throw new Error(...)` để báo lỗi khi dữ liệu đầu vào không hợp lệ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Bắt được các trường hợp `bookingObj` là `null`, `undefined` hoặc không phải đối tượng.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kiểm tra `roomPrice` hợp lệ (kiểu `number` và `> 0`), tránh tính toán ra kết quả `NaN`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ lý do tại sao gán `obj.key = undefined` vẫn làm cho `key` tồn tại trong đối tượng (vẫn xuất hiện trong `Object.keys()` hoặc `hasOwnProperty()`) và phân biệt sự khác nhau về bản chất giữa Chuỗi JSON và JS Object.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến/hàm đặt theo chuẩn camelCase bằng tiếng Anh, viết chú thích mã nguồn rõ ràng, thụt lùi dòng đúng chuẩn ES6+.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository đúng tên thư mục yêu cầu: `[Tên Lớp]_[Môn Học]_Session12_Ex6`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết một đoạn mã tự động kiểm thử (script test automation đơn giản) để gọi hàm `processBookingInvoice` với các tham số hợp lệ và bất hợp lệ, tự động in ra màn hình thông báo `PASS` hoặc `FAIL`.