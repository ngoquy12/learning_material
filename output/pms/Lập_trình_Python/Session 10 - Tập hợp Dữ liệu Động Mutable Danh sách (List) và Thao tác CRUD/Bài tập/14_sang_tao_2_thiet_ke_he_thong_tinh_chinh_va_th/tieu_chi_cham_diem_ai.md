### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 2] Thiết kế Hệ thống Tinh chỉnh và Thanh lọc Dữ liệu Cước phí GrabRide — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản lỗi thường gặp — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa rõ ràng, hợp lý cấu trúc dữ liệu List đầu vào (các chuyến đi ban đầu) và dữ liệu đầu ra sau khi điều chỉnh/xóa, phản ánh đúng nghiệp vụ GrabRide.
*   **[15 điểm] Chủ động phát hiện sai sót dữ liệu (Edge Cases):** Phát hiện tối thiểu 3 kịch bản lỗi biên thực tế (như truy cập index vượt quá độ dài danh sách, thao tác trên List rỗng, giá trị nhập vào không hợp lệ).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow Diagram - Mermaid):** Sơ đồ Mermaid vẽ chính xác luồng dữ liệu, sử dụng đúng 100% chuẩn 5 dạng hình (Terminator `([ ])`, Input/Output `[/ /]`, Decision `?`, Process `[" "]`, Flowline `-->`).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Diễn giải mạch lạc các bước chuyển đổi trạng thái của danh sách dữ liệu từ lúc khởi tạo đến khi hoàn tất thanh lọc.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Cập nhật giá trị phần tử chính xác qua chỉ số index (`list[index] = new_value`) và xóa đúng chuyến đi bị hủy bằng câu lệnh `del list[index]`.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Đếm và thống kê chính số lượng phần tử hợp lệ còn lại trong danh sách bằng hàm `len()`, phản ánh đúng sự thay đổi độ dài danh sách sau khi xóa.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết các điều kiện kiểm tra (dùng `if/else` và `len()`) để ngăn ngừa lỗi `IndexError` trước khi cập nhật hoặc xóa phần tử khỏi List.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn Python 3.12:** Mã nguồn viết sạch sẻ, đặt tên biến chuẩn `snake_case` bằng tiếng Anh, có Type Hints (`list[float]`, `int`), giải thích bằng tiếng Việt có dấu. Tuân thủ tuyệt đối phạm vi cấm (không dùng `def`, `class`, dict, tuple, set, `append`, `pop`).
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Đẩy tệp mã nguồn lên GitHub đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Auditing dữ liệu:** Thiết lập thêm một danh sách lưu lại vết (log) các chỉ số hoặc giá trị cước phí bị xóa/điều chỉnh trong suốt ca làm việc.