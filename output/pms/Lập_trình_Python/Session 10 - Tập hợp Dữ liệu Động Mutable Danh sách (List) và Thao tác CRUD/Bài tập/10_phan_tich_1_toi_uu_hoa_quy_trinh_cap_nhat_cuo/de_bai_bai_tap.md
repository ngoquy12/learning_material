## <center>[Phân tích 1] Tối ưu hóa quy trình cập nhật cước phí và xóa chuyến xe GrabRide</center>

### **1. Mục tiêu**
*   **Kiến thức:** Hiểu và áp dụng thành thạo thao tác truy xuất, ghi đè cập nhật giá trị (Update) và xóa phần tử (Delete) theo vị trí chỉ số (index) trên danh sách Python `list`.
*   **Kỹ năng phân tích:** Đánh giá ưu và nhược điểm của các phương án xử lý danh sách động mutable khi thao tác trực tiếp trên bộ nhớ mà không sử dụng các phương thức mở rộng bị cấm.
*   **Chuẩn hóa mã nguồn:** Viết mã Python 3.12 tuân thủ quy chuẩn PEP 8, áp dụng Type Hints rõ ràng, xử lý an toàn các trường hợp biên và không sử dụng kiến thức ngoài phạm vi cho phép.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt xe công nghệ GrabRide, danh sách cước phí của các chuyến xe trong một ca làm việc của tài xế được quản lý dưới dạng một tập hợp dữ liệu động kiểu `list`. Thiết bị máy tính bảng gắn trên xe nhận một danh sách gồm 5 cước phí chuyến xe ban đầu (đơn vị: VNĐ).

Trong quá trình vận hành thực tế tại ca làm việc:
1. Một chuyến xe tại vị trí chỉ số xác định cần điều chỉnh lại cước phí do phát sinh hệ số phụ phí thời tiết (mưa lớn).
2. Một chuyến xe khác bị hành khách hủy chuyến đột xuất, hệ thống bắt buộc phải loại bỏ dữ liệu chuyến xe này khỏi danh sách và cập nhật lại tổng số chuyến xe còn lại trong ca.

Do thiết bị nhúng IoT trên xe có cấu hình phần cứng tối giản, mã nguồn chạy trên hệ điều hành nhúng chỉ cho phép thao tác trực tiếp bằng chỉ số index, từ khóa `del` và hàm `len()`. [REQUIREMENT] Học viên cần thực hiện phân tích chuyên sâu các phương án kỹ thuật để cập nhật và loại bỏ phần tử ra khỏi danh sách, đồng thời triển khai mã nguồn tối ưu nhất cho hệ thống GrabRide.### **3. Quy tắc nghiệp vụ**
1.  **Dữ liệu đầu vào:** Danh sách cước phí khởi tạo gồm 5 chuyến xe có kiểu dữ liệu `list[int]`. Ví dụ: `[12000, 25500, 45000, 15000, 60000]`.
2.  **Quy tắc cập nhật (Update):** Khi có thông báo điều chỉnh cước phí cho chuyến xe tại chỉ số index chỉ định, giá trị mới (kiểu `int`) phải được ghi đè trực tiếp vào vị trí index đó.
3.  **Quy tắc xóa (Delete):** Khi chuyến xe tại vị trí index chỉ định bị hủy, phần tử tại index đó phải bị xóa hoàn toàn khỏi danh sách bằng từ khóa `del`.
4.  **Quy tắc thống kê:** Ngay sau khi xóa, hệ thống phải xác định lại độ dài của danh sách bằng hàm `len()` để báo cáo số lượng chuyến xe thực tế còn hiệu lực.
5.  **Giới hạn kỹ thuật strict scope:** TUYỆT ĐỐI CẤM sử dụng các phương thức `append()`, `pop()`, kiểu dữ liệu `dict`, `set`, `tuple`, từ khóa khai báo hàm `def`, khai báo lớp `class`, hoặc các thư viện bên ngoài.

### **4. Yêu cầu bài toán**

#### **Phần 1 - Báo cáo Đề xuất Đa giải pháp & So sánh Trade-off**
1.  Tự đề xuất ít nhất **02 phương án kỹ thuật** khác nhau để thực hiện yêu cầu cập nhật và xóa chuyến xe trong danh sách `list[int]` dựa trên nền tảng kiến thức đã học.
2.  Xây dựng bảng so sánh Trade-off chi tiết giữa các phương án đã đề xuất theo đúng 5 tiêu chí bắt buộc (Tốc độ thực thi, Dung lượng bộ nhớ, Khả năng bảo trì, Độ rõ ràng của mã nguồn, Kịch bản áp dụng phù hợp). Bảng so sánh HTML phải chèn thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **Phần 2 - Giải trình Lựa chọn và Thiết kế Sơ đồ luồng**
1.  Đưa ra lý giải khoa học thuyết phục về lý do lựa chọn phương án tối ưu nhất cho thiết bị GrabRide.
2.  Vẽ sơ đồ luồng Mermaid (Flowchart) mô tả chi tiết từng bước xử lý logic của phương án tối ưu.
    *   [NOTE] Bắt buộc tuân thủ đúng 5 dạng hình quy chuẩn Mermaid:
        *   Terminator (Bắt đầu/Kết thúc): `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`
        *   Input/Output (Nhập/Xuất dữ liệu): `[/Đầu vào: .../]` / `[/Đầu ra: .../]`
        *   Decision (Kiểm tra điều kiện): `Kiểm tra điều kiện?` kèm nhánh `-->|Đúng|` / `-->|Sai|`
        *   Process (Thực hiện hành động/Tính toán): `["Thực hiện hành động / Tính toán"]`
        *   Flowline (Đường dẫn luồng): Mũi tên `-->`

#### **Phần 3 - Triển khai Mã nguồn & Phòng chống Lỗi biên**
1.  Triển khai mã nguồn Python 3.12 cho phương án tối ưu đã chọn trong tệp `main.py`.
2.  Khởi tạo danh sách cước phí ban đầu: `trip_fares: list[int] = [12000, 25500, 45000, 15000, 60000]`.
3.  Thực hiện cập nhật cước phí tại index 2 thành `54000` (giá cước mới sau khi cộng phụ phí mưa).
4.  Thực hiện xóa chuyến xe bị hủy tại index 1 bằng từ khóa `del`.
5.  In danh sách sau khi cập nhật/xóa và in tổng số lượng chuyến xe còn lại bằng hàm `len()`.
6.  Phân tích và giải thích phương án ngăn ngừa lỗi biên `IndexError` khi người dùng nhập index nằm ngoài phạm vi danh sách.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex10`.
    Ví dụ: `HNKS25CNTT1_Core_Session10_Ex10`