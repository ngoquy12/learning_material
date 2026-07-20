### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Xây dựng hệ thống quản lý đơn vận chuyển Logistics — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Khởi tạo thành công môi trường ảo `.venv`, tạo cấu trúc thư mục sạch sẽ, tệp `main.py` hoạt động bình thường mà không phát sinh lỗi thiết lập.
*   **[10 điểm] Xây dựng Cấu trúc Dữ liệu mô phỏng (Schemas):** Định nghĩa cấu trúc dữ liệu lưu giữ thông tin vận đơn dưới dạng từ điển (`dict`) đúng và đầy đủ các trường yêu cầu: `Shipment ID` (str), `Origin` (str), `Destination` (str), `Weight` (float), `Base Rate` (float), `Is Express` (bool).

#### **2. Hiện thực hóa các API chức năng cơ bản — 40 điểm**
*   **[20 điểm] API Đọc/Xem danh sách đơn vận chuyển (Chức năng Xem danh sách):** Truy xuất thông tin từ danh sách in-memory và trình bày toàn bộ số liệu dưới dạng bảng danh mục rõ ràng trên console.
*   **[20 điểm] API Ghi/Thêm mới đơn vận chuyển (Chức năng Thêm mới):** Cho phép nhập liệu đầy đủ từ bàn phím, tiếp nhận và ghi nhận thành công thực thể vận đơn mới vào danh sách bộ nhớ tạm thời, tính toán đúng Tổng chi phí vận hành (bao gồm cả hệ số nhân 1.2 khi đơn hàng chọn hỏa tốc).

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Xử lý trùng lặp:** Hệ thống phát hiện được trường hợp trùng lặp mã vận đơn (`Shipment ID`) và in thông báo cảnh báo ra console thay vì lưu đè hoặc gây lỗi runtime.
*   **[10 điểm] Xử lý lỗi chuyển đổi kiểu dữ liệu:** Sử dụng kỹ thuật xử lý lỗi ngoại lệ (`try-except` hoặc so sánh dữ liệu đầu vào) chặn các lỗi nhập sai định dạng số đối với trường `Weight` và `Base Rate` một cách mượt mà.

#### **4. Chất lượng mã nguồn và Đóng gói API Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra và Quy chuẩn lập trình:** 
    *   Trình bày giao diện kết quả trả về sạch sẽ, thẳng đều các cột nhờ sử dụng định dạng nâng cao của `f-string`.
    *   Đặt tên biến, hàm rõ nghĩa bằng tiếng Anh chuyên ngành. Không sử dụng thư viện cấm ngoài danh mục học tập của Session 01.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy toàn bộ mã nguồn chương trình lên kho lưu trữ GitHub theo đúng định dạng được hướng dẫn (`[Tên Lớp]_[Môn Học]_Session01_Tong_hop`).