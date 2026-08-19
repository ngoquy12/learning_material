# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 5] Cập nhật và Xóa cước phí chuyến đi GrabRide — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác thứ tự thực thi thao tác `del` gây ra hiệu ứng dịch chuyển chỉ số (Index Shift Bug) dẫn đến việc cập nhật sai phần tử mục tiêu.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác thông tin 2 dòng còn lại (`...`) trong bảng Test Case (chỉ ra đúng kết quả lỗi và kết quả kỳ vọng).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa lại thứ tự thực hiện (cập nhật trước khi xóa, hoặc điều chỉnh lại chỉ số truy cập sau khi xóa) để kết quả danh sách cước phí cuối cùng hoàn toàn chính xác.
*   **[20 điểm] Xử lý thao tác Danh sách đúng cú pháp:** Sử dụng chính xác thao tác gán chỉ số `list[index] = new_value`, câu lệnh `del` và hàm `len()` đúng chuẩn Python 3.12.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate chỉ số hợp lệ:** Kiểm tra điều kiện chỉ số cần truy cập/xóa nằm trong phạm vi hợp lệ của danh sách (`0 <= index < len(trip_fares)`) trước khi thao tác.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo chương trình không bị văng lỗi `IndexError` khi xử lý danh sách có số lượng phần tử thay đổi.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Phân tích hiện tượng Index Shift:** Giải thích được bản chất vì sao danh sách kiểu List trong Python là Mutable và làm thế nào các thao tác xóa (`del`) ảnh hưởng tới vị trí của các phần tử đứng phía sau.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tuân thủ chuẩn PEP 8 (đặt tên biến dạng `snake_case`, comment bằng tiếng Việt rõ ràng, khai báo Type Hints `list[int]`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session10_Ex5`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Đóng gói kiểm thử linh hoạt:** Viết thêm kịch bản in ra trạng thái danh sách tại từng bước trung gian (trước cập nhật, sau cập nhật, sau khi xóa) để minh họa trực quan tiến trình biến đổi của danh sách.
