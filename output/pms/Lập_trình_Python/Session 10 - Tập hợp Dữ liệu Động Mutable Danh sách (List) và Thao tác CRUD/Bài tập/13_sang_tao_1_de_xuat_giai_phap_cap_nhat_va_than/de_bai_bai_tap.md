# <center>[Sáng tạo 1] Đề xuất Giải pháp Cập nhật và Thanh lọc Dữ liệu Chuyến đi GrabRide</center>

### **1. Mục tiêu**
*   **Tư duy thiết kế hệ thống dữ liệu động:** Vận dụng linh hoạt các thao tác cơ bản trên danh sách Mutable (List) trong Python để giải quyết bài toán quản lý cước phí chuyến đi theo thời gian thực.
*   **Thao tác Cập nhật và Xóa dữ liệu chuẩn mực:** Làm chủ kỹ thuật điều chỉnh giá trị phần tử qua chỉ số (`list[index] = new_value`), loại bỏ phần tử dư thừa/hủy bỏ bằng từ khóa `del`, và truy xuất quy mô dữ liệu bằng hàm `len()`.
*   **Phát hiện lỗi thường gặp biên (Edge Cases):** Chủ động nhận diện các rủi ro tràn chỉ số (`IndexError`), sự dịch chuyển chỉ số sau khi xóa, và xây dựng cơ chế kiểm soát dữ liệu an toàn.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt xe công nghệ GrabRide, ca làm việc của mỗi tài xế lưu trữ danh sách giá cước của các chuyến đi đã và đang thực hiện dưới dạng một danh sách số nguyên (`list[int]`). Tuy nhiên, trong quá trình vận hành thực tế, dữ liệu này thường xuyên xuất hiện sự cố do hai nguyên nhân:
1.  **Tính sai phụ phí thời tiết/GPS:** Một chuyến đi bị tính thiếu phụ phí giờ cao điểm hoặc hệ thống GPS định vị sai khoảng cách, đòi hỏi nhân viên điều hành phải cập nhật lại giá cước chuẩn xác cho chuyến đi tại vị trí chỉ định.
2.  **Khách hàng hủy chuyến:** Một chuyến đi đã ghi nhận trong danh sách nhưng sau đó bị khách hàng hủy, bắt buộc phải xóa hoàn toàn khỏi danh sách ca làm việc để không ảnh hưởng đến doanh thu thực tế.

Người quản trị hệ thống GrabRide yêu cầu bạn tự thiết kế một kịch bản dữ liệu ca làm việc, sau đó xây dựng chương trình Python thực hiện cập nhật cước phí bị sai, xóa bỏ chuyến đi bị hủy, và thống kê lại chính xác số lượng chuyến đi còn hiệu lực trong ca.

### **3. Quy tắc nghiệp vụ**
*   **Khởi tạo dữ liệu ca làm việc:** Khai báo danh sách cước phí chuyến đi ban đầu `trip_fares` kiểu `list[int]` với danh sách các giá trị cước phí ngẫu nhiên (đơn vị: VNĐ).
*   **Cập nhật cước phí (Update):** Thực hiện thay đổi giá trị cước phí tại một vị trí chỉ số `target_update_index` xác định bằng cú pháp gán trực tiếp: `trip_fares[target_update_index] = new_fare`.
*   **Xóa chuyến đi bị hủy (Delete):** Loại bỏ phần tử chuyến đi bị hủy tại vị trí chỉ số `target_delete_index` bằng từ khóa `del trip_fares[target_delete_index]`.
*   **Thống kê độ dài (Read Length):** Sử dụng hàm `len(trip_fares)` để tính toán tổng số chuyến đi còn lại sau khi đã dọn dẹp dữ liệu.
*   **Giới hạn phạm vi công nghệ:**
    *   TUYỆT ĐỐI KHÔNG sử dụng các phương thức biến đổi danh sách chưa học như `.append()`, `.pop()`, `.remove()`, `.insert()`, `.extend()`.
    *   TUYỆT ĐỐI KHÔNG sử dụng Dictionary, Set, Tuple, hàm tự định nghĩa `def`, hoặc Lớp OOP.
    *   Chỉ sử dụng cú pháp truy cập chỉ số `[]`, từ khóa `del`, hàm `len()`, câu lệnh điều kiện `if/elif/else`, biến đơn và các kiểu dữ liệu cơ bản của Python 3.12.

### **4. Yêu cầu bài toán**

Học viên đóng vai trò là Lập trình viên Backend phụ trách mô-đun dữ liệu chuyến đi GrabRide, thực hiện đầy đủ 3 phần công việc sau:

#### **Phần 1: Thiết kế I/O Schema và lỗi thường gặp (Edge Cases)**
*   Tự xây dựng kịch bản dữ liệu đầu vào cho danh sách `trip_fares`, chỉ số cần cập nhật `target_update_index`, giá trị cước mới `new_fare`, và chỉ số chuyến đi bị hủy `target_delete_index`.
*   Phát hiện và phân tích tối thiểu 3 lỗi thường gặp biên (Edge Cases) có thể làm văng lỗi chương trình (ví dụ: chỉ số vượt quá phạm vi danh sách, chỉ số âm không hợp lệ, thao tác xóa trên danh sách rỗng, tác động của thao tác xóa đến vị trí của các phần tử đứng sau).

#### **Phần 2: Thiết kế Sơ đồ luồng dữ liệu (Data Flow Diagram)**
*   Vẽ sơ đồ luồng dữ liệu bằng định dạng Mermaid mô tả toàn bộ vòng đời xử lý từ lúc khởi tạo danh sách chuyến đi ban đầu đến khi xuất ra kết quả ca làm việc đã thanh lọc.
*   Bắt buộc tuân thủ 5 dạng hình chuẩn Mermaid:
    1.  Hình bo tròn Oval `([ ])`: Bắt đầu / Kết thúc quy trình.
    2.  Hình bình hành `[/ /]`: Đầu vào (Input) / Đầu ra (Output).
    3.  Hình thoi `?`: Kiểm tra điều kiện (chỉ số hợp lệ).
    4.  Hình chữ nhật `[" "]`: Tiến trình xử lý (Cập nhật `list[i] = val`, Xóa `del list[i]`, Tính `len()`).
    5.  Mũi tên `-->`: Luồng thực thi.

#### **Phần 3: Hiện thực hóa Mã nguồn Python (Implementation)**
*   Viết mã nguồn hoàn chỉnh trong tệp `main.py` triển khai giải pháp đã thiết kế.
*   Mã nguồn phải đạt chuẩn PEP 8, sử dụng Type Hints đầy đủ (`trip_fares: list[int] = [...]`).
*   Tên biến 100% bằng Tiếng Anh (`trip_fares`, `target_update_index`, `new_fare`, `target_delete_index`, `remaining_trips`).
*   Viết chú thích (comments) giải thích logic xử lý bằng Tiếng Việt có dấu.
*   Sử dụng câu lệnh `if/else` để tự bảo vệ chương trình trước các chỉ số truy cập không hợp lệ.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Sơ đồ Mermaid) và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex13`.
    Ví dụ: `HNKS25CNTT1_Core_Session10_Ex13`
