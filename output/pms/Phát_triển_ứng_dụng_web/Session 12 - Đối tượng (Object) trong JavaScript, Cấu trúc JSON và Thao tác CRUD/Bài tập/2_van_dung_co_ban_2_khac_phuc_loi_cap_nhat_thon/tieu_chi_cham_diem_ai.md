### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Khắc phục lỗi cập nhật thông tin và đóng gói JSON đơn đặt phòng — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Pinpoint chính xác 2 điểm lỗi trong mã nguồn ban đầu (dòng gán `undefined` thay vì dùng từ khóa `delete` và dòng truy cập trực tiếp thuộc tính trên chuỗi JSON).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ và chính xác dữ liệu 3 trường hợp thử nghiệm trong bảng báo cáo (STT 2 và STT 3).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    *   Sử dụng đúng cú pháp `delete rawBookingData.internalStaffNote` hoặc `delete rawBookingData["internalStaffNote"]`.
    *   Sử dụng `JSON.parse(jsonPayload)` để chuyển đổi chuỗi JSON về lại Object trước khi đọc giá trị `"early-checkin-fee"`.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Trả về đối tượng kết quả chính xác bao gồm chuỗi `jsonPayload` hợp lệ và giá trị `extractedFee` là một số thực tế.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra `rawBookingData` phải là Object hợp lệ (không bị `null` hoặc `undefined`), giá trị `earlyFee` phải là kiểu số (Number) không âm.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý trường hợp chuỗi JSON bị lỗi cấu trúc khi parse bằng khối `try...catch` an toàn.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Trả lời rõ ràng sự khác biệt giữa việc gán `undefined` cho thuộc tính và việc dùng từ khóa `delete`, đồng thời giải thích tại sao không thể lấy thuộc tính trực tiếp từ một String dạng JSON.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến theo chuẩn `camelCase`, thụt lề đồng nhất 2 hoặc 4 khoảng trắng, ghi chú mã nguồn bằng tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session12_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm các hàm kiểm thử tự động (sử dụng `console.assert` hoặc câu lệnh điều kiện) để kiểm tra thuộc tính `internalStaffNote` hoàn toàn không còn tồn tại trong Object sau khi xử lý.