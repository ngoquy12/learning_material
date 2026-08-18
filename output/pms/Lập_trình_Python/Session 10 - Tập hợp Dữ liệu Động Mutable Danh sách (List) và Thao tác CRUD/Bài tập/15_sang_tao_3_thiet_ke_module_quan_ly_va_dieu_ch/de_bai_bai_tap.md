## <center>[Sáng tạo 3] Thiết kế Module Quản lý và Điều chỉnh Cước phí Chuyến đi GrabRide</center>

### **1. Mục tiêu**
*   **Tư duy hệ thống & Kiến trúc dữ liệu:** Vận dụng linh hoạt các thao tác cơ bản trên danh sách dữ liệu động Mutable (cập nhật phần tử qua vị trí index, xóa phần tử bằng câu lệnh `del`, và truy xuất kích thước danh sách bằng `len()`) để xây dựng module quản lý cước phí chuyến đi trong ca làm việc của tài xế.
*   **Phân tích & Tự thiết kế:** Tự thiết kế cấu trúc I/O Schema, chủ động phát hiện các sai sót dữ liệu/lỗi biên (Edge Cases), và biểu diễn luồng vận hành dữ liệu bằng sơ đồ Mermaid đúng chuẩn kỹ thuật.
*   **Quy chuẩn lập trình:** Tuân thủ chuẩn PEP 8, Type Hints trong Python 3.12, và giới hạn phạm vi kiến thức đã học (tuyệt đối không sử dụng các phương thức hoặc cấu trúc dữ liệu chưa được đề cập).

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt xe công nghệ **GrabRide**, các chuyến đi được khởi tạo và lưu giữ dưới dạng một danh sách giá cước tạm tính trong ca làm việc của tài xế. Tuy nhiên, dữ liệu này liên tục biến động do các yếu tố thực tế phát sinh:
1.  **Cập nhật giá cước (Update):** Khách hàng thay đổi điểm đến khiến quãng đường di chuyển tăng/giảm, hoặc thời tiết đột ngột chuyển sang mưa lớn làm kích hoạt phụ phí `1.2x`. Hệ thống cần ghi đè cước phí mới trực tiếp tại chỉ số index của chuyến đi tương ứng.
2.  **Hủy chuyến đi (Delete):** Hành khách hoặc tài xế chủ động hủy chuyến đi do sự cố ngoài ý muốn, yêu cầu hệ thống loại bỏ hoàn toàn giá cước của chuyến đi đó khỏi danh sách bằng câu lệnh `del`.
3.  **Thống kê chỉ tiêu (Length Check):** Điều phối viên cần kiểm tra số lượng chuyến đi thực tế còn lại trong danh sách thông qua hàm `len()` để đánh giá hiệu suất ca làm việc.

Hệ thống đang cần một Kỹ sư Phần mềm Backend chịu trách nhiệm phân tích toàn bộ quy trình, thiết kế cấu trúc dữ liệu và triển khai mã nguồn hoàn chỉnh từ đầu.### **3. Quy tắc nghiệp vụ**
*   **Cơ chế tính giá cước chuyến đi GrabRide:**
    *   2 km đầu tiên: Tính giá cố định `12.000 VNĐ`.
    *   Từ km thứ 3 trở đi: Tính `4.500 VNĐ/km` cho phần quãng đường vượt quá 2 km.
    *   Trường hợp thời tiết xấu (mưa lớn) hoặc giờ cao điểm: Giá cước toàn chuyến đi được nhân hệ số phụ phí `1.2x`.
*   **Quy tắc cập nhật và xóa trên List mutable:**
    *   Cập nhật phần tử: Sử dụng cú pháp gán qua chỉ số `danh_sach[index] = cuoc_phi_moi`.
    *   Xóa phần tử: Sử dụng lệnh `del danh_sach[index]` để xóa phần tử tại vị trí được chọn.
    *   Kiểm tra số lượng: Sử dụng hàm `len(danh_sach)` để lấy tổng số chuyến đi còn lại.
*   **Giới hạn phạm vi kĩ thuật:**
    *   Sử dụng Python 3.12, PEP 8 và Type Hints cho các biến (ví dụ: `danh_sach_cuoc_phi: list[int] = [...]`).
    *   **CẤM CÁC TỪ KHÓA/KIẾN THỨC:** Tuyệt đối không sử dụng phương thức biến đổi List như `append()`, `pop()`, `insert()`, `remove()`; không dùng `dict`, `tuple`, `set`; không dùng hàm tự định nghĩa `def`, lớp `class` hoặc thư viện ngoài.

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Phần mềm tại GrabRide, hoàn thành 4 phần bài tập sau:

*   **Phần 1 - Tự thiết kế I/O Schema:** Tự định nghĩa cấu trúc dữ liệu đầu vào (danh sách cước phí ban đầu, chỉ số cập nhật, giá trị cập nhật, chỉ số xóa) và đầu ra dự kiến của chương trình.
*   **Phần 2 - Tự phát hiện sai sót dữ liệu (Edge Cases):** Liệt kê ít nhất 3 kịch bản lỗi hoặc xung đột dữ liệu có thể xảy ra khi thao tác với danh sách (ví dụ: truy cập chỉ số index vượt quá phạm vi `len()`, cập nhật cước phí bằng giá trị âm, hoặc thao tác trên danh sách rỗng) và nêu phương án xử lý bằng các câu điều kiện `if/else`.
*   **Phần 3 - Thiết kế Sơ đồ luồng dữ liệu (Data Flow Diagram):** Vẽ sơ đồ Mermaid mô tả toàn bộ vòng đời xử lý dữ liệu từ lúc khởi tạo danh sách chuyến đi -> kiểm tra điều kiện hợp lệ -> cập nhật cước phí -> xóa chuyến đi bị hủy -> xuất báo cáo tổng hợp.
    *   *Yêu cầu hình khối Mermaid:*
        *   Terminator (Bắt đầu/Kết thúc): Hình oval `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`.
        *   Input/Output (Nhập/Xuất): Hình bình hành `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
        *   Decision (Kiểm tra): Hình thoi `Kiểm tra điều kiện?`.
        *   Process (Xử lý/Tính toán): Hình chữ nhật `["Thực hiện tính toán / Cập nhật"]`.
        *   Flowline: Mũi tên `-->` hoặc `-->|Đúng|`.
*   **Phần 4 - Hiện thực hóa mã nguồn Python:** Viết chương trình hoàn chỉnh bằng Python 3.12 tuân thủ thiết kế từ Phần 1 đến Phần 3 và nằm trong giới hạn kiến thức cho phép.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 10_Ex15`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 10_Ex15`