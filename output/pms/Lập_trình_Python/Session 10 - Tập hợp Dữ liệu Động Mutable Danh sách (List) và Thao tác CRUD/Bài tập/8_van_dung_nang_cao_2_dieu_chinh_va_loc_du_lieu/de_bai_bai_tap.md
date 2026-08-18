## <center>[Vận dụng nâng cao 2] Điều chỉnh và Lọc dữ liệu Cước phí Chuyến xe GrabRide</center>

### **1. Mục tiêu**
*   **Kỹ năng lập trình**: Vận dụng các thao tác cập nhật phần tử danh sách qua chỉ số (`list[index] = new_value`), xóa phần tử theo vị trí chỉ số bằng lệnh `del`, và truy xuất kích thước danh sách với hàm `len()`.
*   **Tư duy phân tích**: Độc lập phân tích bài toán thực tế từ bối cảnh nghiệp vụ GrabRide, tự thiết kế giải pháp kỹ thuật, xây dựng sơ đồ luồng Mermaid chuẩn hóa và thiết lập rào chắn dữ liệu (edge case guards) cho các chỉ số ngoài phạm vi.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống quản lý đặt xe công nghệ GrabRide (GRAB_RIDE), cuối ca làm việc của mỗi đối tác tài xế, trung tâm điều hành sẽ tiến hành quy trình đối soát dữ liệu cước phí các chuyến xe (`trip_fares`).Trong quá trình vận hành thực tế, hai sự cố thường phát sinh:
1. **Chuyến xe bị tính thiếu cước**: Do GPS mất tín hiệu gián đoạn, cước phí một chuyến xe bị ghi nhận thấp hơn thực tế và cần được điều chỉnh lại giá trị chuẩn xác tại chỉ số tương ứng.
2. **Chuyến xe bị hủy/ảo**: Một chuyến xe bị hệ thống ghi nhận nhầm dù khách hàng đã hủy, cần phải xóa bỏ hoàn toàn khỏi danh sách đối soát theo chỉ số vị trí để tránh làm sai lệch doanh thu.

Hệ thống yêu cầu bạn thực hiện cập nhật giá trị cước mới, xóa chuyến xe không hợp lệ, đồng thời tính toán số lượng chuyến xe hợp lệ còn lại trong danh sách để sẵn sàng chốt ca.

### **3. Quy tắc nghiệp vụ**
1. **Dữ liệu cước phí ban đầu**: Danh sách `trip_fares` chứa các số nguyên đại diện cho cước phí từng chuyến xe (đơn vị: VNĐ). Ví dụ: `[15000, 45000, 12000, 85000, 30000]`.
2. **Điều kiện Cập nhật (Update)**:
   *   Vị trí cần cập nhật (`update_index`) phải nằm trong khoảng chỉ số hợp lệ của danh sách: `0 <= update_index < len(trip_fares)`.
   *   Cước phí mới (`new_fare`) phải đạt tối thiểu **12.000 VNĐ** (giá cước cố định cho 2 km đầu tiên). Nếu nhỏ hơn 12.000 VNĐ, từ chối cập nhật và báo lỗi nghiệp vụ.
3. **Điều kiện Xóa (Delete)**:
   *   Vị trí cần xóa (`delete_index`) phải nằm trong khoảng chỉ số hợp lệ hiện tại của danh sách: `0 <= delete_index < len(trip_fares)`.
   *   Thực hiện xóa phần tử bằng câu lệnh `del`.
4. **Kiểm tra biên (Edge Cases Guard)**:
   *   Nếu chỉ số `update_index` hoặc `delete_index` nằm ngoài phạm vi danh sách (chỉ số âm hoặc `>= len()`), chương trình phải cảnh báo lỗi và hủy thao tác tương ứng để đảm bảo tính toàn vẹn dữ liệu.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Phân tích & Thiết kế Giải pháp (Solution Analysis & Design Report)**
Học viên cần trình bày báo cáo phân tích trước khi viết mã nguồn:
1. **Phân tích I/O**:
   *   Xác định kiểu dữ liệu của danh sách cước phí ban đầu, các chỉ số thao tác và các biến kiểm tra.
2. **Đề xuất giải pháp & Các bước thực hiện**:
   *   Tự đề xuất chuỗi logic xử lý kiểm tra điều kiện chỉ số trước khi cập nhật hoặc xóa.
3. **Sơ đồ luồng (Mermaid Flowchart)**:
   *   Vẽ sơ đồ luồng biểu diễn quy trình kiểm tra và thao tác trên danh sách. Tuân thủ nghiêm ngặt 5 hình dạng chuẩn:
     - **Start/End**: Hình bo tròn `([Bắt đầu...])`, `([Kết thúc...])`.
     - **Input/Output**: Hình bình hành `[/Đầu vào.../]`, `[/Đầu ra.../]`.
     - **Condition Check**: Hình thoi `Kiểm tra điều kiện?`.
     - **Process/Action**: Hình chữ nhật `["Thực hiện tính toán / gán / xóa"]`.
     - **Flowline**: Mũi tên `-->` kèm nhãn `-->|Đúng|` hoặc `-->|Sai|`.

#### **Phần 2: Triển khai Mã nguồn (Implementation)**
Triển khai chương trình Python đáp ứng các yêu cầu sau:
*   Sử dụng Python 3.12, tuân thủ chuẩn PEP 8 và ghi rõ Type Hints.
*   Chỉ sử dụng các cú pháp đã học: gán chỉ số `list[i] = val`, xóa `del list[i]`, kiểm tra độ dài `len()`, câu lệnh điều kiện `if/else`.
*   **CẤM SỬ DỤNG**: Các phương thức biến đổi List như `append()`, `pop()`, `insert()`, `remove()`, hoặc các kiểu dữ liệu `dict`, `set`, `tuple`, từ khóa tạo hàm `def`, lớp `class`.
*   Hiển thị rõ ràng danh sách ban đầu, danh sách sau cập nhật, danh sách sau khi xóa và số lượng chuyến xe hợp lệ còn lại.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (bao gồm sơ đồ luồng Mermaid) và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex8`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session10_Ex8`