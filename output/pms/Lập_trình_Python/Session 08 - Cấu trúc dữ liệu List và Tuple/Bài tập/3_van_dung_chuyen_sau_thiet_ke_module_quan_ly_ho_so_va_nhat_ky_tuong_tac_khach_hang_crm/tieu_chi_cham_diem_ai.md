### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Thiết kế Module Quản lý Hồ sơ và Nhật ký Tương tác Khách hàng CRM — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Mô tả chi tiết kiểu dữ liệu của tham số đầu vào và kết quả trả về của các hàm (`tuple[float, float]`, `list[int]`, `str`).
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Viết Pseudocode hoặc sơ đồ luồng minh họa rõ ràng các bước Unpacking Tuple, Swap trực tiếp biến, truy cập gán Index và Cắt lát List Slicing.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo cấu trúc danh sách nhật ký tương tác CRM và Tuple tọa độ GPS đúng kiểu dữ liệu, tuân thủ nguyên tắc không biến đổi Tuple ban đầu.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Triển khai chính xác logic hoán đổi biến (Swap), giải nén dữ liệu (Unpacking), cập nhật vị trí Index 0 và trích xuất phân đoạn Slicing `[1:3]`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Bắt chính xác bẫy tọa độ ngoài phạm vi địa lý (Vĩ độ ngoài `[-90.0, 90.0]` hoặc Kinh độ ngoài `[-180.0, 180.0]`) và kích hoạt `ValueError`.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Kiểm tra độ dài danh sách nhật ký tương tác trước khi truy cập Index 0 và Slicing; chủ động kích hoạt `IndexError` nếu danh sách có dưới 4 phần tử. Tuân thủ tuyệt đối KHÔNG dùng vòng lặp và phương thức thêm/xóa phần tử.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xử lý và hiển thị thông điệp lỗi bằng tiếng Việt rõ ràng khi gặp ngoại lệ dữ liệu không hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tuân thủ PEP 8 (khai báo 4-space indentation, đặt tên biến/hàm kiểu `snake_case`, tên định danh tiếng Anh, chú thích bằng tiếng Việt có dấu).
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên kho lưu trữ GitHub đúng cấu trúc thư mục yêu cầu (`[Tên Lớp]_[Môn Học]_Session08_Ex03`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Triển khai hoán đổi biến ngắn gọn bằng cú pháp mã hóa Pythonic `a, b = b, a` và tái tạo Tuple mới tối ưu không dùng biến trung gian dư thừa.