# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Sửa lỗi đóng gói và tính phụ phí đặt phòng khách sạn — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã chứa toán tử so sánh sai (`<= 12`) và dòng mã gán `undefined` thay vì sử dụng toán tử `delete`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện chính xác các cột Input, Buggy Output, Expected Output, Line of Code và Logic Note cho toàn bộ 3 testcase trong bảng báo cáo.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh điều kiện kiểm tra check-in sớm (`checkInHour < 12`) và tính đúng phụ phí 30% giá cơ bản.
*   **[20 điểm] Thao tác xóa và đóng gói Object chuẩn xác:** Sử dụng đúng toán tử `delete bookingObj.tempSecurityToken` để xóa thuộc tính khỏi bộ nhớ và thực hiện đóng gói chuỗi JSON bằng `JSON.stringify`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra giá phòng `basePrice > 0` và giờ check-in nằm trong khoảng từ `0` đến `23`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Ném ra `Error` với thông báo rõ ràng khi gặp dữ liệu không hợp lệ mà không làm dừng đột ngột chương trình.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được sự khác biệt giữa việc gán `obj.key = undefined` và dùng toán tử `delete obj.key` khi đóng gói dữ liệu sang chuỗi JSON (`JSON.stringify`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Đặt tên biến/hàm theo chuẩn camelCase, mã nguồn trình bày rõ ràng, bổ sung ghi chú bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session12_Ex5`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết hàm test kiểm thử tự động kiểm tra các trường hợp check-in lúc 11h, 12h và 13h để đảm bảo logic phụ phí làm việc chính xác 100%.
