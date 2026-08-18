## <center>[Phân tích 2] Cập nhật và Xóa cước phí chuyến xe GrabRide</center>

### **1. Mục tiêu**
*   **Kiến thức:** Nắm vững và áp dụng thuần thục thao tác truy cập chỉ số (indexing), cập nhật giá trị trực tiếp và xóa phần tử bằng câu lệnh `del` trên kiểu dữ liệu danh sách động (`list`) trong Python 3.12.
*   **Kỹ năng phân tích:** Đánh giá, so sánh các phương án kỹ thuật xử lý biến đổi danh sách dữ liệu chuyến xe khi có yêu cầu thay đổi nghiệp vụ (cập nhật cước phí, xóa chuyến xe bị hủy).
*   **Tư duy tối ưu:** Xây dựng báo cáo phân tích trade-off, vẽ lưu đồ thuật toán (flowchart) và hiện thực hóa mã nguồn tuân thủ nghiêm ngặt chuẩn PEP 8 và Type Hints.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống GrabRide, danh sách cước phí của các chuyến xe được ghi nhận trong một ca làm việc của tài xế được lưu trữ dưới dạng một danh sách động `list[int]`. Giả sử hệ thống đang quản lý danh sách cước phí của 6 chuyến xe liên tiếp trong ca trực: `[35000, 12000, 85000, 45000, 12000, 150000]` (đơn vị: VNĐ).

Trong quá trình vận hành ca trực, hai sự kiện nghiệp vụ phát sinh đồng thời:
1. Chuyến xe ở vị trí thứ 3 (tương ứng với chỉ số 2 trong danh sách) được áp dụng mã khuyến mãi theo chương trình ưu đãi, giá cước cần được cập nhật lại thành `60000` VNĐ.
2. Chuyến xe ở vị trí thứ 2 (tương ứng với chỉ số 1 trong danh sách) bị khách hàng hủy chuyến do thời gian chờ quá lâu, cần được xóa bỏ hoàn toàn khỏi hệ thống để tránh tính toán doanh thu sai lệch.

Bộ phận kỹ thuật yêu cầu lập báo cáo phân tích kiến trúc dữ liệu và triển khai mã nguồn Python xử lý danh sách trên, đảm bảo kiểm tra độ dài danh sách sau khi thao tác và in ra kết quả chính xác.### **3. Quy tắc nghiệp vụ**
1. **Dữ liệu khởi tạo:** Danh sách cước phí ban đầu gồm 6 phần tử `[35000, 12000, 85000, 45000, 12000, 150000]`.
2. **Cập nhật giá cước:**
   * Thay đổi giá trị phần tử tại chỉ số (index) 2 thành `60000`.
   * Việc cập nhật phải diễn ra theo đúng trình tự nghiệp vụ đã đề ra.
3. **Xóa chuyến xe hủy:**
   * Xóa phần tử tại chỉ số (index) 1 khỏi danh sách.
   * Chú ý đến sự thay đổi về vị trí chỉ số và độ dài danh sách sau khi xóa phần tử.
4. **Kiểm tra và truy xuất:**
   * Sử dụng hàm `len()` để xác định tổng số chuyến xe còn lại.
   * In danh sách ban đầu, danh sách sau khi xử lý và tổng số chuyến xe còn lại ra màn hình.
5. **Ràng buộc công nghệ:** Chỉ được phép sử dụng cú pháp cập nhật gán chỉ số `list[index] = value`, câu lệnh xóa `del list[index]`, hàm `len()` và các câu lệnh điều kiện/vòng lặp cơ bản. Tuyệt đối không sử dụng các phương thức `append()`, `pop()`, `remove()`, `insert()`, hàm tự định nghĩa `def`, lớp `class` hoặc các kiểu dữ liệu nâng cao như `dict`, `set`, `tuple`.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Đề xuất & So sánh Đa giải pháp (Multi-Solution Report)**
*   Tự đề xuất ít nhất 2 phương án kỹ thuật khác nhau từ đầu để giải quyết bài toán cập nhật và xóa phần tử trong danh sách (Ví dụ: Thao tác biến đổi trực tiếp trên danh sách gốc bằng câu lệnh `del` và gán chỉ số VS. Tạo danh sách mới hoặc dịch chuyển vị trí các phần tử thủ công).
*   Lập bảng so sánh Trade-off giữa các phương án dựa trên 5 tiêu chí bắt buộc:
    *   Độ phức tạp thời gian (Time Complexity).
    *   Độ phức tạp bộ nhớ (Space Complexity).
    *   Khả năng bảo trì (Maintainability).
    *   Độ rõ ràng / Dễ đọc (Readability).
    *   Mức độ phù hợp với quy định công nghệ hiện tại (Suitability).

#### **Phần 2: Giải trình Lựa chọn & Thiết kế Lưu đồ Thuật toán (Flowchart)**
*   Giải trình chi tiết lý do lựa chọn phương án tối ưu nhất dựa trên kết quả phân tích.
*   Vẽ lưu đồ thuật toán (Mermaid Flowchart) mô tả chi tiết các bước xử lý của phương án đã chọn.
*   *Yêu cầu bắt buộc về ký hiệu Mermaid:*
    *   Bắt đầu / Kết thúc: Hình bo tròn `([Bắt đầu])` / `([Kết thúc])`.
    *   Nhập / Xuất dữ liệu: Hình bình hành `[/In kết quả.../]` (Tuyệt đối không dùng cho câu lệnh tính toán/gán).
    *   Xử lý / Gán / Tính toán: Hình chữ nhật `["Gán trip_fares[2] = 60000"]` hoặc `["Xóa del trip_fares[1]"]`.
    *   Ràng buộc kiểm tra: Hình thoi `Kiểm tra chỉ số hợp lệ?`.

#### **Phần 3: Triển khai Mã nguồn Python & lỗi thường gặp Biên**
*   Viết mã nguồn Python 3.12 đầy đủ trong tệp `main.py`.
*   Khai báo biến có Type Hints chuẩn PEP 8 (sử dụng tên biến tiếng Anh).
*   Xử lý lỗi thường gặp biên (ví dụ: kiểm tra độ dài danh sách trước khi truy cập chỉ số để tránh lỗi `IndexError`).
*   In ra màn hình kết quả theo đúng định dạng đầu ra.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session10_Ex11`.
    Ví dụ: `HNKS25CNTT1_Core_Session10_Ex11`