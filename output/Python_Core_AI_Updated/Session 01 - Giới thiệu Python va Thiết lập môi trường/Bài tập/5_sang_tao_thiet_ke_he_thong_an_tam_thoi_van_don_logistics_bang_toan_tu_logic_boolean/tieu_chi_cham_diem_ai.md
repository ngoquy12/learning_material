### **Tiêu chí chấm điểm (AI)**
**[Bài tập Sáng tạo - Ẩn tạm thời vận đơn Logistics] — Tổng điểm: 100 điểm**

#### **1. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 30 điểm**
*   **[15 điểm] Thiết kế luồng dữ liệu (Data Flow):**
    *   Có sơ đồ Mermaid mô tả rõ ràng dữ liệu từ thiết bị đầu cuối CLI đi vào các biến trung gian, chuyển đổi kiểu dữ liệu (Type-Casting) và xuất ra màn hình.
    *   Thể hiện rõ việc kiểm soát kiểu dữ liệu đầu vào.
*   **[15 điểm] Thiết kế vòng đời tính năng (Feature Lifecycle):**
    *   Giải thích logic và chứng minh được công thức toán học/boolean dùng để mô phỏng cơ chế Soft-Hide.
    *   Thể hiện nguyên lý chuyển đổi dữ liệu logic thành chuỗi văn bản giao diện mà không dùng cấu trúc kiểm soát luồng.

#### **2. Hiện thực hóa logic nghiệp vụ sáng tạo — 40 điểm**
*   **[20 điểm] Triển khai thành công logic nghiệp vụ đặc thù:**
    *   Tính chính xác của công thức tính "Chi phí vận chuyển gốc" và "Phụ phí trì hoãn" bằng phương pháp đại số Boolean (nhân giá trị boolean: `phu_phi * is_delayed`).
    *   Mã nguồn tuyệt đối không xuất hiện các từ khóa điều khiển: `if`, `else`, `elif`, `match`, `for`, `while`.
*   **[20 điểm] Xử lý lọc dữ liệu nâng cao:**
    *   Tính toán đúng trạng thái `Is Hidden` dựa trên điều kiện kết hợp (Admin yêu cầu ẩn HOẶC (Đơn hàng bị trễ VÀ khoảng cách vận chuyển > 500 km)) chỉ bằng toán tử logic: `or`, `and`.
    *   Xác định chính xác biến trung gian `Payment Rate` từ biến logic `Is Hidden`.

#### **3. Kiểm chuẩn dữ liệu, Chặn lỗi dị biệt nâng cao — 20 điểm**
*   **[10 điểm] Xử lý ngoại lệ nghiệp vụ lặp trạng thái:**
    *   Có phương án chuyển đổi dữ liệu đầu vào chuỗi `"True"`/`"False"` của người dùng sang kiểu `bool` chuẩn xác (lưu ý: hàm `bool("False")` trong Python mặc định trả về `True` vì chuỗi không rỗng, học viên cần sáng tạo ra cơ chế ép kiểu giá trị này như so sánh trực tiếp: `admin_hide_input == "True"`).
*   **[10 điểm] Validate dữ liệu và Chống tràn:**
    *   Sử dụng hàm toán học cơ bản như `abs()` hoặc xử lý chuỗi cơ bản để ngăn chặn việc nhập giá trị âm đối với khối lượng và khoảng cách.

#### **4. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code:**
    *   Đặt tên biến rõ ràng, mang tính gợi nhớ theo quy chuẩn PEP 8.
    *   Định dạng kết quả đầu ra rõ ràng, thẳng hàng, hiển thị số tiền có ngăn cách phần nghìn hoặc làm tròn hợp lý bằng toán tử định dạng f-string (như ví dụ `:,.2f`).
*   **[5 điểm] Quy chuẩn nộp bài GitHub:**
    *   Cấu trúc thư mục nộp bài chuẩn chỉnh theo cấu trúc: `[Tên Lớp]_[Môn Học]_Session01_Ex05`.
    *   Có file `README.md` mô tả bối cảnh bài toán, cách khởi chạy file Python và chụp ảnh kết quả kiểm thử.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore (Phục hồi) dữ liệu:**
    *   Thiết kế biểu thức logic đảo ngược để tính toán lại số tiền bồi hoàn bảo hiểm được hoàn lại khi khôi phục trạng thái đơn hàng về lại trạng thái hoạt động (Active). 
    *   Ý tưởng được triển khai liền mạch dưới dạng một dòng code tính giá trị phục hồi hoàn toàn bằng toán tử số học/boolean.