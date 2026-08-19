# **Tiêu chí chấm điểm (AI)**
**Hệ Thống Phân Loại Lô Hàng Và Kiểm Tra Điều Kiện Thông Quan Logistics — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
*   **10 điểm:** Khai báo cấu trúc thư mục chuẩn, tệp `index.html` liên kết đúng với `script.js`. Tất cả các biến đầu vào được khai báo đúng từ khóa ES6 (`const`/`let`), chuẩn đặt tên `camelCase`, ghi chú mã nguồn rõ ràng.
*   **5 điểm:** Khai báo đúng các biến nhưng dùng sai từ khóa (`var` tràn lan) hoặc đặt tên chưa tuân thủ quy tắc `camelCase`.
*   **0 điểm:** Không khởi tạo được dự án hoặc sai cấu trúc tệp cơ bản.

#### **2. Logic nghiệp vụ (30 điểm)**
*   **30 điểm:** Thực hiện chính xác toàn bộ logic nghiệp vụ:
    *   Tính cước cơ bản chính xác theo 3 khung trọng lượng bằng `if-else`.
    *   Tính phụ phí loại hàng chính xác bằng `switch-case` có đầy đủ các `case` và `default`.
    *   Sử dụng toán tử ba ngôi Ternary để tính phí hỏa tốc và đánh giá mức ưu tiên ngắn gọn, đúng logic.
    *   Xác định chính xác trạng thái thông quan bằng sự kết hợp toán tử logic (`&&`, `||`, `!`).
*   **20 điểm:** Tính đúng cước cơ bản và phụ phí nhưng xử lý sai logic thông quan hoặc không dùng `switch-case`/`ternary operator` theo yêu cầu.
*   **10 điểm:** Sai kết quả tính toán chi phí ở 2 công thức trở lên.
*   **0 điểm:** Không triển khai logic nghiệp vụ hoặc mã nguồn bị lỗi cú pháp làm dừng chương trình.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
*   **30 điểm:** Kiểm soát đầy đủ 3 điều kiện ràng buộc dữ liệu đầu vào (mã lô hàng rỗng, trọng lượng `<= 0` hoặc `isNaN`, mã loại hàng nằm ngoài khoảng `1-4`). In thông báo lỗi rõ ràng và dừng chương trình bằng cơ chế luồng rẽ nhánh chuẩn.
*   **15 điểm:** Có kiểm tra dữ liệu đầu vào nhưng thiếu điều kiện `isNaN` hoặc chưa chặn được mã loại hàng không hợp lệ.
*   **0 điểm:** Không có bước Validation dữ liệu đầu vào.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
*   **20 điểm:** Sử dụng cơ chế rẽ nhánh hợp lý, không lặp lại các phép tính trùng lặp, dùng biểu thức điều kiện ngắn gọn, ứng dụng tối đa tính năng Short-circuit evaluation và toán tử ba ngôi để mã nguồn tối ưu.
*   **10 điểm:** Mã nguồn bị lặp đoạn logic điều kiện (redundant `if` blocks), lạm dụng nhiều câu lệnh `if` thay vì `switch-case`.
*   **0 điểm:** Code rối rắm, lặp logic nghiêm trọng gây ảnh hưởng tới hiệu năng chạy của chương trình.

#### **5. Chất lượng mã nguồn (10 điểm)**
*   **10 điểm:** Mã nguồn trình bày sạch đẹp, thụt lề chuẩn xác (2 hoặc 4 spaces), đặt tên biến minh bạch theo đúng ngữ cảnh domain Logistics. Trình bày output Console bằng Template Literals đúng định dạng mẫu.
*   **5 điểm:** Thiếu thụt lề hoặc trình bày console output sơ sài, cộng chuỗi thủ công thay vì dùng Template Literals.
*   **0 điểm:** Mã nguồn cẩu thả, không tuân thủ bất kỳ quy chuẩn Clean Code nào.

#### **Điểm cộng (5-10 điểm)**
*   **+5 điểm:** Tích hợp thành công `prompt()` để người dùng nhập động dữ liệu lô hàng trực tiếp từ màn hình trình duyệt kèm ép kiểu dữ liệu `parseFloat()` / `parseInt()` an toàn.
*   **+5 điểm:** Định dạng tiền tệ VNĐ chuyên nghiệp sử dụng hàm chuẩn JavaScript `Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' })`.
