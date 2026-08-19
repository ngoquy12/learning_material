# <center>[Sáng tạo 2] Thiết kế Hệ thống Tinh chỉnh và Thanh lọc Dữ liệu Cước phí GrabRide</center>

### **1. Mục tiêu**
*   **Vận dụng kỹ năng xử lý Danh sách (List):** Thực thi thành thạo thao tác truy xuất, cập nhật giá trị phần tử qua chỉ số (`list[index] = value`), loại bỏ phần tử bị hủy (`del list[index]`), và đo đạc quy mô dữ liệu bằng hàm `len()`.
*   **Tư duy thiết kế hệ thống độc lập:** Tự xây dựng sơ đồ luồng dữ liệu (Data Flow Diagram), tự quy định kịch bản dữ liệu đầu vào/đầu ra (I/O Schema), và chủ động nhận diện các lỗi biên (Edge Cases) trong nghiệp vụ vận tải GrabRide.
*   **Quy chuẩn lập trình chuyên nghiệp:** Viết mã nguồn Python 3.12 hoàn chỉnh không phụ thuộc vào mã mẫu (skeleton code), tuân thủ PEP 8 và Type Hints trong phạm vi kiến thức đã được duyệt.

---

### **2. Bối cảnh & Vấn đề**
Trong hệ thống quản lý ca trực của tài xế GrabRide, mỗi danh sách List đóng vai trò lưu trữ chuỗi dữ liệu giao dịch nối tiếp theo thời gian (như khoảng cách di chuyển của từng chuyến đi, cước phí gốc tạm tính). 

Tuy nhiên, trong thực tế vận hành luôn xuất hiện các biến cố dữ liệu:
1. **Lỗi tính thiếu cước:** Do hệ thống định vị GPS bị mất tín hiệu tạm thời hoặc chưa kịp áp dụng hệ số phụ phí thời tiết xấu (mưa bão/giờ cao điểm), cước phí của một số chuyến đi tại chỉ số chỉ định bị tính sai và cần được điều chỉnh lại giá trị chính xác.
2. **Chuyến đi không hợp lệ:** Một số chuyến đi bị hành khách hủy giữa chừng hoặc bị phát hiện vi phạm quy định gian lận. Các chuyến đi này phải bị xóa hoàn toàn khỏi danh sách ca trực để đảm bảo tính minh bạch cho báo cáo doanh thu.---

### **3. Quy tắc nghiệp vụ**
Hệ thống GrabRide áp dụng các công thức và quy định nghiệp vụ sau:
*   **Cước phí cơ bản:**
    *   2 km đầu tiên: Giá cố định **12.000 VNĐ**.
    *   Từ km thứ 3 trở đi: Tính thêm **4.500 VNĐ/km** cho phần khoảng cách vượt quá 2 km.
*   **Phụ phí đặc biệt:**
    *   Khi có mưa lớn hoặc giờ cao điểm, tổng cước phí của chuyến đi sẽ được nhân với hệ số điều chỉnh **1.2x**.
*   **Quy tắc cập nhật và xóa phần tử:**
    *   Cập nhật cước phí: Tiến hành gán lại giá trị cước mới cho phần tử tại vị trí chỉ số `index` tương ứng: `danh_sach_cuoc[index] = gia_tri_moi`.
    *   Xóa phần tử: Loại bỏ chuyến đi bị hủy khỏi danh sách bằng câu lệnh `del danh_sach_cuoc[index]`. Lưu ý: Khi thực hiện xóa, chỉ số của các phần tử đứng sau sẽ tự động dịch chuyển lùi 1 vị trí.
    *   Thống kê quy mô: Sử dụng hàm `len(danh_sach_cuoc)` để tính toán chính xác tổng số chuyến đi hợp lệ còn lại trong ca trực.

---

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Lập trình Hệ thống tại GrabRide, hãy thực hiện bài nộp gồm 4 phần sau:

*   **Phần 1: Tự thiết kế I/O Schema (Cấu trúc đầu vào / đầu ra)**
    *   Tự xác định danh sách dữ liệu đầu vào đại diện cho ca làm việc của tài xế (bao gồm danh sách khoảng cách hoặc cước phí ban đầu).
    *   Mô tả rõ dạng dữ liệu và giá trị của kết quả đầu ra sau khi đã thực hiện các thao tác cập nhật và xóa.

*   **Phần 2: Tự phát hiện & Liệt kê sai sót dữ liệu (Edge Cases)**
    *   Tự liệt kê ít nhất 3 sai sót dữ liệu có thể làm nảy sinh lỗi hệ thống (Ví dụ: Thao tác xóa trên danh sách rỗng, cập nhật chỉ số `index` nằm ngoài phạm vi danh sách `IndexError`, cập nhật khoảng cách di chuyển thành số âm, v.v.).

*   **Phần 3: Thiết kế Sơ đồ luồng dữ liệu (Data Flow Diagram)**
    *   Vẽ sơ đồ luồng dữ liệu bằng định dạng Mermaid minh họa toàn bộ quá trình: Nhận danh sách ban đầu -> Kiểm tra và cập nhật cước phí tại index -> Xóa chuyến đi bị hủy tại index -> Thống kê độ dài danh sách bằng `len()`.
    *   **Quy định bắt buộc về hình dạng trong Mermaid:**
        *   Terminator (Bắt đầu/Kết thúc): Dùng hình viên thuốc `([Bắt đầu])` / `([Kết thúc])`.
        *   Input/Output (Nhận/Xuất dữ liệu): Dùng hình hình bình hành `[/Đầu vào/]` / `[/Đầu ra/]`.
        *   Decision (Kiểm tra điều kiện): Dùng hình thoi `Điều kiện?`.
        *   Process (Thao tác/Tính toán): Dùng hình chữ nhật `["Thực hiện tính toán/Gán giá trị"]`.
        *   Flowline (Luồng dịch chuyển): Dùng mũi tên `-->`.

*   **Phần 4: Viết mã nguồn chương trình Python hoàn chỉnh (`main.py`)**
    *   Khởi tạo danh sách ca trực.
    *   Thực hiện việc tính toán lại cước phí và cập nhật trực tiếp vào chỉ số cụ thể trong List.
    *   Thực hiện xóa chuyến đi bị hủy khỏi List bằng câu lệnh `del`.
    *   In ra màn hình thông tin chi tiết danh sách trước và sau khi xử lý, cùng số lượng chuyến đi hợp lệ còn lại.
    *   *Giới hạn kỹ thuật:* Chỉ sử dụng kiến thức đã học (List, chỉ số index, `del`, `len()`, kiểu dữ liệu cơ bản, câu lệnh điều khiển `if/else`, vòng lặp). **Tuyệt đối không sử dụng:** hàm `def`, lớp `class`, Dictionary, Set, Tuple, các phương thức biến đổi danh sách (`append`, `pop`, `remove`, `insert`...).

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Sơ đồ Mermaid) và mã nguồn triển khai trong tệp `main.py`.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 10_Ex14`.
    *   *Ví dụ:* `HNKS25CNTT1_Core_Session_Session 10_Ex14`
