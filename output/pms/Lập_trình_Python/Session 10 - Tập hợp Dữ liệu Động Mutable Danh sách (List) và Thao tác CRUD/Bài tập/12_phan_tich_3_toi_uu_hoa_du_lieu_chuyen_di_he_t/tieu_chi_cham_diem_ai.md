### **Tiêu chí chấm điểm (AI)**
**[Phân Tích 3] Tối Ưu Hóa Dữ Liệu Chuyến Đi Hệ Thống GrabRide Bằng Thao Tác Cập Nhật Và Xóa Danh Sách — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Học viên tự phát hiện và trình bày rõ ràng ít nhất 2 phương án xử lý duyệt chỉ số index khi dùng `del` (ví dụ: Phương án điều khiển biến đếm index chủ động trong vòng lặp `while` không tăng `i` khi xóa vs. Phương án duyệt ngược danh sách từ cuối về đầu `range(len - 1, -1, -1)`).
    *   Mô tả đúng khác biệt mặt cấu trúc logic giữa 2 phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** 
    *   Điền đầy đủ nội dung phân tích vào bảng HTML theo chuẩn 5 tiêu chí: Độ phức tạp thời gian, Bộ nhớ, Khả năng bảo trì, Độ đọc hiểu, Rủi ro lỗi chỉ số.
    *   Phân tích chính xác ưu điểm và nhược điểm của từng phương án.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Trình bày lý do thuyết phục chọn phương án tối ưu dựa trên tiêu chí tính đúng đắn khi thay đổi độ dài danh sách (`len()`) và sự đơn giản, rõ ràng trong việc kiểm soát index.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** 
    *   Vẽ sơ đồ Mermaid Flowchart đúng chuẩn 5 dạng hình (Oval cho Start/End, Bình hành cho I/O, Hình thoi cho Decision, Chữ nhật cho Process).
    *   Diễn tả chính xác logic duyệt, kiểm tra điều kiện `< 0.0` để cập nhật và `== 0.0` để xóa bằng `del`.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** 
    *   Triển khai đúng mã nguồn Python 3.12 thực hiện cập nhật `danh_sach[i] = 2.0` cho khoảng cách âm và xóa phần tử bằng `del danh_sach[i]` khi khoảng cách bằng `0.0`.
    *   Tuyệt đối tuân thủ phạm vi kiến thức: Không dùng `append()`, `pop()`, `def`, `class`, `dict`, `set`, `tuple`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** 
    *   Xử lý chính xác trường hợp danh sách chứa nhiều số `0.0` liên tiếp mà không bị bỏ sót phần tử (do dồn index).
    *   Xử lý đúng khi danh sách rỗng hoặc chứa 100% phần tử `0.0` mà không gây ra lỗi `IndexError`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** 
    *   In ra màn hình rõ ràng: Danh sách chuyến đi ban đầu, Danh sách chuyến đi sau khi xử lý cập nhật/xóa, và Tổng số chuyến đi hợp lệ còn lại bằng lệnh `len()`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến bằng tiếng Anh chuẩn snake_case (ví dụ: `trip_distances`, `current_index`, `valid_trip_count`), có ghi chú thích logic bằng tiếng Việt có dấu. Khai báo Type Hints đầy đủ (`list[float]`, `int`).
*   **[5 điểm] Nộp bài GitHub:** Cung cấp link repository GitHub đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session10_Ex12`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Kịch bản Kiểm thử mở rộng:** Học viên chủ động bổ sung bộ dữ liệu thử nghiệm mở rộng kiểm thử với 4 kịch bản dữ liệu biên khác nhau trong cùng một file script để chứng minh thuật toán hoạt động hoàn hảo trong mọi tình huống.