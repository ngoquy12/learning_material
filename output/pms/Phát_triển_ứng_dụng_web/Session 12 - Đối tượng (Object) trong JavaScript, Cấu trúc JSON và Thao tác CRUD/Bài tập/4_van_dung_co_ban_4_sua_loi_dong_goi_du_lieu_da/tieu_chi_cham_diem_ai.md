# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 4] Sửa lỗi đóng gói dữ liệu đặt phòng và chuẩn hóa JSON — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác các dòng mã nguồn chứa lỗi logic (Lỗi gán `undefined` giữ lại key trong Object ở dòng 16; Lỗi đọc thuộc tính trực tiếp trên chuỗi JSON chưa giải mã ở dòng 22-23).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện 100% thông tin bị thiếu trong bảng Test Case (cột Buggy Output, Expected Output, Dòng code gây lỗi và Nguyên nhân giải thích).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    * Sử dụng cú pháp ngoặc vuông `bookingReservation[surchargeKey] = 250000` để cập nhật đúng thuộc tính động.
    * Sử dụng toán tử `delete bookingReservation.tempAuthToken` để loại bỏ sạch key nhạy cảm khỏi bộ nhớ.
    * Sử dụng `JSON.parse(jsonPayload)` để chuyển chuỗi JSON thành Object trước khi truy xuất dữ liệu `guestName` và `extra-services`.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Mã nguồn JavaScript ES6+ chạy thành công không phát sinh lỗi cú pháp hay lỗi tham chiếu Runtime.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Đảm bảo đối tượng ban đầu có đầy đủ cấu trúc thuộc tính theo yêu cầu và kiểm tra tính hợp lệ của biến key động.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Chuỗi JSON đầu ra (`jsonPayload`) đảm bảo hợp lệ, không chứa thuộc tính `tempAuthToken` và không chứa thuộc tính thừa `surchargeKey`.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích rõ sự khác biệt giữa việc gán giá trị `undefined` cho thuộc tính và việc sử dụng toán tử `delete`, đồng thời nêu rõ lý do tại sao không thể truy cập thuộc tính trực tiếp từ một chuỗi JSON (String type).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn đặt tên biến rõ ràng, thụt lùi dòng chuẩn mực, chú thích giải thích logic bằng tiếng Việt đầy đủ dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_SessionSession 12_Ex4`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết thêm đoạn mã kiểm thử tự động sử dụng `console.assert()` để kiểm tra thuộc tính `tempAuthToken` không còn tồn tại trong `bookingReservation` sau khi xóa (`console.assert(bookingReservation.tempAuthToken === undefined && !('tempAuthToken' in bookingReservation))`).
