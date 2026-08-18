#

# <center>[Sáng tạo 3] Sáng tạo hệ thống làm thủ tục check-in và tính phí hành lý hàng không</center>

### **1. Mục tiêu**
*   Vận dụng linh hoạt và sáng tạo các cấu trúc rẽ nhánh rẽ nhánh điều kiện đã học (`if-else`, `switch-case`, toán tử ba ngôi `ternary operator`) để thiết kế logic giải quyết bài toán phức tạp trong thực tế.
*   Rèn luyện tư duy thiết kế kiến trúc phần mềm: tự định nghĩa cấu trúc dữ liệu I/O, chủ động phát hiện các kịch bản lỗi biên (edge cases) và mô hình hóa luồng dữ liệu bằng sơ đồ Mermaid.
*   Viết mã nguồn JavaScript (ES6+) chuẩn sạch, độc lập, tối ưu logic rẽ nhánh và tuân thủ tuyệt đối các quy định thiết kế hệ thống.

---

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quản lý làm thủ tục chuyến bay (Airline Check-in System) của hãng hàng không, quy trình xác minh thông tin hành khách và tính toán chi phí phát sinh trước khi cấp thẻ lên máy bay (Boarding Pass) đóng vai trò cốt lõi. Khi hành khách đến quầy check-in hoặc thực hiện kịch bản tự check-in, hệ thống phải xử lý đồng thời nhiều biến số: mã phân hạng vé (`Eco`, `Deluxe`, `Business`), trọng lượng hành lý mang theo, mã vị trí ghế muốn chọn và trạng thái vé trên hệ thống.

Một vấn đề lớn đặt ra cho các lập trình viên hệ thống là sự đa dạng của các quy tắc phụ thu và bẫy dữ liệu phát sinh. Ví dụ: hành khách hạng vé phổ thông mang hành lý quá cước nhưng lại yêu cầu chọn ghế ưu tiên của hạng thương gia, hoặc hành khách có mã trạng thái vé bị treo nhưng vẫn cố gắng hoàn tất check-in. Nếu logic rẽ nhánh không được thiết kế chặt chẽ, hệ thống có thể tính sai chi phí, cấp thẻ sai quyền hạn hoặc gây thất thoát doanh thu dịch vụ của hãng hàng không.---

### **3. Quy tắc nghiệp vụ**
Hệ thống cần vận hành dựa trên các quy tắc nghiệp vụ cốt lõi sau:

1.  **Quy tắc định trọng lượng hành lý:**
    *   Hành lý xách tay tiêu chuẩn được miễn phí tối đa 7 kg cho tất cả các phân hạng vé.
    *   Đối với trọng lượng quá cước (trên 7 kg), mỗi kg vượt hạn mức sẽ tính phí phụ thu tại sân bay là 50.000 VNĐ/kg.
2.  **Quy tắc phân hạng vé & ghế ngồi:**
    *   Hạng `Business`: Được miễn phí 100% chi phí chọn vị trí ghế ngồi trước.
    *   Hạng `Deluxe` và `Eco`: Nếu chọn vị trí ghế ngồi thuộc hàng ghế đặc biệt (ví dụ: ghế gần cửa thoát hiểm hoặc ghế hàng đầu), hệ thống sẽ áp dụng mức phí chọn ghế tương ứng theo mã quy định.
3.  **Quy tắc xử lý trạng thái Check-in:**
    *   Trạng thái làm thủ tục được quản lý thông qua các mã số (ví dụ: `1` - Chờ làm thủ tục, `2` - Đã làm thủ tục thành công, `3` - Đã lên tàu bay, `4` - Vé bị hủy hoặc từ chối).
    *   Chương trình chỉ cho phép xử lý và xuất thẻ lên tàu bay khi mã trạng thái ở mức hợp lệ (`1`).

---

### **4. Yêu cầu bài toán**
Học viên đóng vai trò là Kiến trúc sư Phần mềm (Software Architect), tự thực hiện toàn bộ 4 phần nhiệm vụ dưới đây:

#### **Phần 1: Tự thiết kế I/O Schema**
Học viên tự định nghĩa danh sách các biến dữ liệu đầu vào (Input) và đầu ra (Output) cần thiết để mô phỏng hoàn chỉnh một lượt check-in. Trình bày rõ ràng tên biến (bằng tiếng Anh), kiểu dữ liệu và giải thích ý nghĩa nghiệp vụ.

#### **Phần 2: Chủ động phát hiện bẫy dữ liệu (Edge Cases)**
Liệt kê tối thiểu 3 trường hợp biên hoặc xung đột dữ liệu có thể xảy ra trong thực tế khai thác (ví dụ: số kg hành lý nhập vào là số âm, mã hạng vé nhập không đúng quy chuẩn, hoặc hành khách đã ở trạng thái đã bay nhưng lại thực hiện check-in lần 2). Giải thích hướng xử lý logic cho từng trường hợp.

#### **Phần 3: Thiết kế Sơ đồ luồng dữ liệu (Data Flow Diagram)**
Vẽ sơ đồ quy trình xử lý check-in bằng cú pháp Mermaid. Sơ đồ phải tuân thủ nghiêm ngặt quy chuẩn 5 dạng hình khối:
*   **Terminator (Bắt đầu/Kết thúc):** Khối bo tròn `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`.
*   **Input / Output:** Khối hình bình hành `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
*   **Decision (Kiểm tra điều kiện):** Khối hình thoi `{Kiểm tra ...}` kèm nhãn rẽ nhánh `-->|Đúng|` và `-->|Sai|`.
*   **Process (Xử lý / Tính toán):** Khối hình chữ nhật `["Tính toán / Thực hiện ..."]`.
*   **Flowline (Đường dòng chảy):** Mũi tên chỉ hướng `-->`.

#### **Phần 4: Triển khai mã nguồn JavaScript (ES6+)**
Xây dựng chương trình JavaScript hoàn chỉnh xử lý logic từ đầu đến cuối:
*   Sử dụng các cấu trúc rẽ nhánh `if-else`, `switch-case` và toán tử ba ngôi `? :` một cách tối ưu, tránh lặp mã (DRY).
*   In ra màn hình console báo cáo kết quả check-in chi tiết bao gồm: Thông tin hành khách, Phí hành lý quá cước, Phí chọn ghế, Tổng chi phí phụ thu và Trạng thái thẻ lên tàu bay.
*   Mã nguồn sử dụng tên biến/hằng số hoàn toàn bằng tiếng Anh, ghi chú giải thích logic bằng Tiếng Việt có dấu.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Sơ đồ Mermaid) và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 06_Ex15`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 06_Ex15`