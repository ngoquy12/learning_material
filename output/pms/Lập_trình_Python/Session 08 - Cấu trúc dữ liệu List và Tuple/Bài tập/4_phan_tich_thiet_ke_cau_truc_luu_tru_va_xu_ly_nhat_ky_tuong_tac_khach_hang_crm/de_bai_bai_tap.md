## <center>[Phân tích] Thiết kế cấu trúc lưu trữ và xử lý nhật ký tương tác khách hàng CRM</center>

### **1. Mục tiêu**
*   **Phân tích chuyên sâu:** Đánh giá ưu và nhược điểm giữa phương pháp sửa đổi trực tiếp dữ liệu List qua Index so với phương pháp tái tạo List mới bằng kỹ thuật cắt lát (Slicing).
*   **Bảo toàn an toàn dữ liệu:** Hiểu rõ và ứng dụng tính bất biến (Immutability) của Tuple để bảo vệ dữ liệu tọa độ địa lý GPS cố định của các điểm tương tác CRM.
*   **Kỹ thuật xử lý Pythonic:** Áp dụng kỹ thuật Tuple Unpacking và hoán đổi biến trực tiếp (Variable Swap) để chuẩn hóa thứ tự kinh vĩ độ mà không dùng biến trung gian.
*   **Tư duy tối ưu hóa:** Đưa ra quyết định kiến trúc dữ liệu phù hợp với hệ thống CRM cập nhật theo thời gian thực mà không vi phạm các quy định giới hạn cú pháp.

### **2. Vấn đề**
Trong phân hệ Quản lý Quan hệ Khách hàng (CRM), hệ thống ghi nhận nhật ký của một chuyên viên chăm sóc khách hàng tại hiện trường. Mỗi bản ghi tương tác bao gồm hai thành phần dữ liệu chính:
1. Danh sách ID mã phiên tương tác gần nhất: `session_log = [5001, 5002, 5003, 5004]` (Cấu trúc dữ liệu List có tính thay đổi được - Mutable).
2. Tọa độ địa lý GPS vị trí gặp mặt khách hàng: `geo_location = (106.66017, 10.76262)` (Cấu trúc dữ liệu Tuple bất biến - Immutable).

Do lỗi ghi nhận dữ liệu đầu vào từ thiết bị di động:
*   Mã phiên tương tác đầu tiên (`index 0`) bị sai sót và cần được cập nhật ngay thành mã phiên ưu tiên `9999`.
*   Bộ phận phân tích dữ liệu CRM yêu cầu trích xuất một phân đoạn nhật ký gồm 2 mã phiên ở giữa (từ index 1 đến index 2) để làm báo cáo nhanh.
*   Tọa độ GPS bị ghi ngược thứ tự: Kinh độ (`longitude = 106.66017`) lại nằm trước Vĩ độ (`latitude = 10.76262`). Quy chuẩn hệ thống CRM bắt buộc phải lưu dưới dạng `(vĩ_độ, kinh_độ)`.



### **3. Quy tắc nghiệp vụ**
*   **Bảo vệ tính bất biến:** Không được tìm cách ghi đè trực tiếp các phần tử bên trong Tuple `geo_location` (vì thao tác này gây ra lỗi runtime `TypeError`). Dữ liệu tọa độ mới phải được khởi tạo thành một Tuple mới dựa trên giá trị đã chuẩn hóa.
*   **Chuẩn hóa tọa độ:** Sử dụng kỹ thuật giải nén Tuple (Tuple Unpacking) và hoán đổi biến (Swap) trực tiếp để đưa tọa độ về dạng `(latitude, longitude)`.
*   **Phân đoạn dữ liệu:** Sử dụng kỹ thuật Slicing `[1:3]` để trích xuất đúng sub-list chứa 2 phần tử ở giữa.
*   **Giới hạn kỹ thuật nghiêm ngặt:** 
    *   [REQUIREMENT] TUYỆT ĐỐI CẤM sử dụng các vòng lặp (`for`, `while`).
    *   [REQUIREMENT] TUYỆT ĐỐI CẤM sử dụng các phương thức thêm/xóa phần tử của List như `append()`, `insert()`, `pop()`, `remove()`, `del`, `clear()`.
    *   [REQUIREMENT] Mã nguồn phải tuân thủ chuẩn PEP 8, có Type Hints đầy đủ cho các khai báo dữ liệu trong Python 3.12.

### **4. Yêu cầu bài toán**

#### **Nhiệm vụ 1: Báo cáo Đề xuất & So sánh Trade-off (Báo cáo văn bản)**
Học viên cần đề xuất 2 giải pháp kỹ thuật khác nhau để giải quyết bài toán nghiệp vụ trên và lập bảng so sánh Trade-off chi tiết:
*   **Giải pháp A (Cập nhật In-place & Pythonic Swap):** Sửa đổi trực tiếp giá trị index 0 của List hiện tại `session_log[0] = 9999`, sử dụng Slicing `[1:3]` để lấy sub-list, và dùng Unpacking kết hợp Pythonic Swap (`lat, lng = lng, lat`) để đảo thứ tự tọa độ.
*   **Giải pháp B (Tái tạo List mới & Variable Swap thủ công):** Tạo một List hoàn toàn mới bằng phép cộng Slicing `[9999] + session_log[1:]`, trích xuất sub-list, và hoán đổi giá trị tọa độ qua biến trung gian `temp`.

Yêu cầu lập bảng so sánh HTML theo 5 tiêu chí:
1. Độ phức tạp bộ nhớ (Memory Allocation).
2. Tốc độ thực thi (Execution Speed).
3. Độ rõ ràng & Dễ bảo trì (Readability & Maintainability).
4. Tính an toàn dữ liệu (Data Integrity).
5. Ngữ cảnh áp dụng tối ưu trong hệ thống CRM.

#### **Nhiệm vụ 2: Biện luận Lựa chọn & Thiết kế Mã giả/Lưu đồ**
*   Đưa ra lập luận kỹ thuật để chọn ra 1 giải pháp tối ưu nhất cho hệ thống CRM xử lý dữ liệu lớn.
*   Trình bày mã giả (Pseudocode) hoặc các bước logic từng dòng cho phương án tối ưu đã chọn.

#### **Nhiệm vụ 3: Triển khai Mã nguồn Python 3.12**
*   Viết chương trình Python 3.12 hoàn chỉnh thực thi giải pháp tối ưu đã chọn.
*   In ra màn hình theo định dạng chuẩn:
    *   Dòng 1: Mã phiên đầu tiên trước và sau khi cập nhật.
    *   Dòng 2: Danh sách nhật ký phiên CRM đầy đủ sau khi sửa.
    *   Dòng 3: Danh sách phân đoạn nhật ký đã trích xuất `[1:3]`.
    *   Dòng 4: Tuple tọa độ GPS chuẩn hóa ban đầu và sau khi swap.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai trong một tập tin duy nhất hoặc báo cáo kèm tệp code `.py`.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex04`.
    Ví dụ: `HNKS25CNTT1_Core_Session08_Ex04`