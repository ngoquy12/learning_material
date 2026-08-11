## <center>[Sáng tạo] Thiết kế Hệ thống Nhật ký Kiểm toán Check-in và Điều phối Khách hàng CRM</center>

### **1. Mục tiêu**
*   **Ứng dụng thực tế tính bất biến của Tuple:** Thiết kế cơ chế đóng gói dữ liệu tọa độ check-in và cấu hình hệ thống cố định nhằm chống gian lận và đảm bảo tính toàn vẹn dữ liệu kiểm toán (Audit Trail) trong CRM.
*   **Vận dụng kỹ thuật xử lý List nâng cao:** Sử dụng kỹ thuật truy cập Index, cập nhật phần tử trực tiếp và cắt lát danh sách (List Slicing) để quản lý lịch sử tương tác khách hàng theo thời gian thực mà không làm thay đổi cấu trúc bộ nhớ ban đầu.
*   **Tối ưu hóa thao tác hoán đổi dữ liệu:** Áp dụng kỹ thuật Tuple Unpacking và hoán đổi biến trực tiếp (Variable Swap) để xử lý luồng luân chuyển nhân viên chăm sóc khách hàng chuyên nghiệp.
*   **Nâng cao tư duy kiến trúc:** Tự định nghĩa lược đồ I/O, dự báo bẫy dữ liệu biên và xây dựng sơ đồ luồng dữ liệu (Mermaid) cho bài toán quản trị quan hệ khách hàng.

### **2. Bối cảnh & Vấn đề**
Trong một hệ thống CRM quản lý đội ngũ kinh doanh đi thị trường (Field Sales), mỗi nhân viên khi đến gặp khách hàng phải thực hiện thao tác check-in. Hệ thống cần ghi nhận tọa độ vị trí (Latitude, Longitude) dưới dạng dữ liệu kiểm toán cố định không thể sửa đổi sau khi đã khởi tạo. Đồng thời, danh sách mã phiên làm việc với khách hàng trong ngày (Customer Session Logs) cần được theo dõi và cập nhật trạng thái liên tục.

Hệ thống hiện tại đang gặp hai sự cố nghiêm trọng:
1. Thông tin vị trí check-in ban đầu bị sửa đổi trái phép trên bộ nhớ do dùng sai cấu trúc dữ liệu, dẫn đến sai lệch dữ liệu kiểm toán doanh số.
2. Thao tác bàn giao khách hàng giữa hai nhân viên tư vấn bị lỗi lệch dữ liệu khi sử dụng các biến trung gian thủ công không an toàn.

Hệ thống CRM mới yêu cầu một kiến trúc xử lý dữ liệu bộ nhớ an toàn: bảo vệ dữ liệu nhạy cảm bằng Tuple bất biến, quản lý nhật ký phiên bằng List và xử lý hoán đổi quyền chăm sóc bằng kỹ thuật Swap chuẩn mực của Python 3.12.



### **3. Quy tắc nghiệp vụ**
*   **Quy tắc 1 (Bảo vệ dữ liệu kiểm toán):** Thông tin định vị GPS cố định gồm (Latitude, Longitude) phải được lưu trữ dưới dạng Tuple. Mọi hành vi cố tình thay đổi trực tiếp giá trị phần tử của Tuple này phải bị hệ thống chặn lại và báo lỗi bất biến.
*   **Quy tắc 2 (Hoán đổi điều phối an toàn):** Việc chuyển giao quyền quản lý hồ sơ khách hàng giữa hai nhân viên tư vấn (Lead Primary Rep và Lead Secondary Rep) phải thực hiện bằng kỹ thuật hoán đổi trực tiếp (Variable Swap) và giải nén dữ liệu (Tuple Unpacking), tuyệt đối không dùng biến trung gian tạm thời.
*   **Quy tắc 3 (Quản lý nhật ký phiên tương tác):** Lịch sử các mã phiên CRM trong ngày được lưu dưới dạng List. Hệ thống cho phép:
    *   Cập nhật mã phiên mới nhất tại một chỉ số Index xác định.
    *   Trích xuất phân đoạn lịch sử tương tác trọng tâm (Sub-log) bằng kỹ thuật cắt lát danh sách `[start:end]`.
*   **Ràng buộc kỹ thuật nghiêm ngặt:** 
    *   TUYỆT ĐỐI KHÔNG sử dụng vòng lặp (`for`, `while`).
    *   TUYỆT ĐỐI KHÔNG sử dụng các phương thức thêm/xóa phần tử của List (`append`, `pop`, `remove`, `insert`, `extend`...).
    *   Chỉ áp dụng các kiến thức đã học: Indexing, Slicing, Tuple Unpacking, Variable Swap, cập nhật giá trị List theo Index.

### **4. Yêu cầu bài toán**

[REQUIREMENT] Học viên đóng vai trò Kỹ sư Kiến trúc Phần mềm CRM và thực hiện đầy đủ 4 phần công việc sau:

*   **Phần 1 - Tự thiết kế I/O Schema (Input/Output Schema):**
    *   Tự khai báo cấu trúc dữ liệu đầu vào (bao gồm Tuple chứa tọa độ GPS CRM, List chứa mã phiên tương tác khách hàng, Tuple chứa thông tin cặp nhân viên tư vấn).
    *   Tự xác định và mô tả rõ ràng định dạng dữ liệu kết quả đầu ra sau khi xử lý.
*   **Phần 2 - Tự phát hiện bẫy dữ liệu (Edge Cases):**
    *   Liệt kê ít nhất 03 kịch bản lỗi hoặc xung đột dữ liệu có thể xảy ra trong nghiệp vụ CRM (Ví dụ: Thao tác cố tình ghi đè Tuple kiểm toán, vi phạm chỉ số Slicing ngoài phạm vi List, lỗi lệch số lượng biến khi Unpacking).
    *   Đề xuất phương án xử lý chặn lỗi tương ứng cho từng kịch bản.
*   **Phần 3 - Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram):**
    *   Vẽ 01 sơ đồ luồng bằng mã Mermaid (`graph TD` hoặc `sequenceDiagram`) mô tả toàn bộ vòng đời xử lý dữ liệu: Khởi tạo Tuple GPS & List CRM -> Giải nén Unpacking -> Swap nhân viên -> Cập nhật Index List -> Cắt lát Slicing -> Đóng gói báo cáo đầu ra.
*   **Phần 4 - Triển khai mã nguồn Python 3.12:**
    *   Viết chương trình Python 3.12 hoàn chỉnh từ đầu dựa trên thiết kế cá nhân.
    *   Đảm bảo có Type Hints đầy đủ (`tuple[float, float]`, `list[int]`, v.v.).
    *   Đặt tên biến, hàm 100% bằng tiếng Anh theo chuẩn PEP 8. Viết ghi chú giải thích logic bằng tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex05`.
    Ví dụ: `HNKS25CNTT1_Core_Session08_Ex05`