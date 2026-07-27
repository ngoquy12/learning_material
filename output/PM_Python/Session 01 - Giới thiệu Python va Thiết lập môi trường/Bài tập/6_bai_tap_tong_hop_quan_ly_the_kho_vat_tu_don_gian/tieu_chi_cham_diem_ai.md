### **Tiêu chí chấm điểm (AI)**
**[Quản lý thẻ kho vật tư đơn giản] — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Môi trường — 20 điểm**
*   **[10 điểm] Thiết lập môi trường ảo:** Thư mục dự án có chứa dấu vết thiết lập môi trường ảo `.venv` hoặc học viên mô tả được bước kích hoạt `.venv` (ví dụ thông qua ảnh chụp hoặc cấu trúc thư mục).
*   **[10 điểm] Cấu trúc tệp:** Tạo đúng file mã nguồn `warehouse_card.py` chạy độc lập, không bị lỗi import hệ thống hoặc lỗi cấu hình thông dịch viên.

#### **2. Nhập liệu & Làm sạch chuỗi — 20 điểm**
*   **[10 điểm] Tương tác nhập liệu:** Viết đúng các câu lệnh `input()` để người dùng nhập lần lượt 5 thông tin yêu cầu.
*   **[10 điểm] Chuẩn hóa chuỗi:** Sử dụng các phương thức xử lý chuỗi cơ bản của Python để biến đổi mã vật tư thành chữ hoa (`.upper()`) và loại bỏ khoảng trắng dư thừa trong tên vật tư (`.strip()`).

#### **3. Ép kiểu & Tính toán logic — 30 điểm**
*   **[15 điểm] Ép kiểu dữ liệu:** Thực hiện ép kiểu chuỗi nhập vào sang kiểu số nguyên (`int()`) đối với số lượng đầu kỳ, số lượng xuất và kiểu số thực (`float()`) đối với đơn giá.
*   **[15 điểm] Logic tính toán:** Thực hiện đúng phép toán cơ bản xác định:
    *   Tồn cuối kỳ = Tồn đầu kỳ - Số lượng xuất.
    *   Giá trị tồn = Tồn cuối kỳ * Đơn giá.

#### **4. Định dạng đầu ra với f-string — 20 điểm**
*   **[10 điểm] Căn chỉnh lề văn bản:** In dữ liệu thẻ kho hiển thị thẳng hàng, các tiêu đề cân đối bằng cách căn chỉnh thủ công hoặc dùng các cú pháp định dạng khoảng trắng của f-string.
*   **[10 điểm] Định dạng số:** Áp dụng f-string định dạng hiển thị đơn giá và giá trị tồn cuối kỳ hiển thị đúng phần thập phân (ví dụ: `:,.2f`).

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Đặt tên thư mục:** Thư mục nộp bài trên GitHub đặt đúng cấu hình quy định: `[Tên Lớp]_[Môn Học]_Session01_Tong_hop`.