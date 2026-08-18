## <center>[Sáng tạo 2] Thiết Kế Module Tính Toán Điều Kiện Đặt Phòng Khách Sạn</center>

### **1. Mục tiêu**
*   **Tự chủ thiết kế I/O Schema**: Xác định cấu trúc dữ liệu đầu vào và đầu ra cho module đánh giá điều kiện đặt phòng và tính toán phụ phí trong hệ thống Agoda/Traveloka.
*   **Vận dụng toán tử nâng cao**: Sử dụng kết hợp các toán tử số học, toán tử so sánh, toán tử logic và quy tắc ưu tiên tính toán trong Python để xác định cờ trạng thái (Boolean flags) và số tiền phụ thu mà không cần dùng câu lệnh điều khiển luồng (`if/else`).
*   **Trực quan hóa quy trình**: Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram) thể hiện quy trình xử lý logic bằng cú pháp Mermaid chuẩn hóa.
*   **Hiện thực hóa mã nguồn**: Viết chương trình Python 3.12 đạt chuẩn PEP 8, có Type Hints, tên biến tiếng Anh chỉn chu và ghi chú bằng tiếng Việt có dấu.

### **2. Bối cảnh & Vấn đề**
Hệ thống đặt phòng trực tuyến (Agoda/Traveloka) cần phát triển một tính năng nền tảng: **Booking Condition & Fee Evaluator Engine**. Module này xử lý dữ liệu từ yêu cầu đặt phòng của khách hàng (giờ check-in dự kiến, số ngày hủy phòng trước thời điểm nhận phòng, số lượng khách thực tế so với sức chứa tiêu chuẩn, tuổi của trẻ em đi cùng...).

Do yêu cầu hiệu năng cực cao ở tầng tính toán nhanh (In-Memory Evaluation), hệ thống không sử dụng các câu lệnh rẽ nhánh phức tạp mà tính toán trực tiếp thông qua các biểu thức số học và biểu thức logic đại số. Bài toán đặt ra cho học viên là tự thiết kế bài toán, định nghĩa tập dữ liệu, phát hiện các trường hợp biên nguy hiểm và hiện thực hóa module tính toán này hoàn toàn từ đầu.### **3. Quy tắc nghiệp vụ**
Hệ thống áp dụng các quy tắc kinh doanh lưu trú tiêu chuẩn sau:
*   **Giờ Check-in tiêu chuẩn**: Giờ check-in quy định là 14:00. Nếu khách check-in trước 12:00 (giờ check-in < 12), cờ phụ thu `is_early_checkin` sẽ kích hoạt (`True`) và chịu phụ phí 30% giá phòng một đêm.
*   **Chính sách hủy phòng**: Hủy phòng trước ngày nhận phòng từ 3 ngày trở lên (số ngày báo hủy >= 3), cờ hoàn tiền `is_full_refund_eligible` nhận giá trị `True` (hoàn 100% cọc).
*   **Chính sách trẻ em**: Trẻ em dưới 6 tuổi (tuổi trẻ em < 6) được cờ `is_child_free` xác nhận miễn phí lưu trú.
*   **Vượt sức chứa tiêu chuẩn**: Sức chứa tiêu chuẩn của phòng là 2 người lớn. Mỗi người vượt quá chịu phụ phí 200.000 VNĐ/người/đêm. Cờ `is_over_capacity` kích hoạt khi số khách lớn hơn 2.

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Software Architect tự chủ thực hiện 4 phần nhiệm vụ sau:

*   **Phần 1: Thiết kế I/O Schema (Đầu vào / Đầu ra)**
    *   Tự khai báo danh sách các biến đầu vào đại diện cho thông tin đặt phòng (`checkin_hour`, `days_before_cancellation`, `guest_count`, `child_age`, `room_rate_per_night`, `deposit_amount`).
    *   Tự khai báo danh sách các biến đầu ra biểu diễn kết quả tính toán (`is_early_checkin`, `is_full_refund_eligible`, `is_child_free`, `is_over_capacity`, `early_surcharge`, `extra_guest_surcharge`, `total_extra_fee`).

*   **Phần 2: Tự phát hiện bẫy dữ liệu (Edge Cases)**
    *   Liệt kê ít nhất 3 kịch bản dữ liệu bất thường hoặc điểm nghẽn nghiệp vụ (ví dụ: giờ check-in nhập số âm hoặc lớn hơn 24, số ngày báo hủy là số âm, số lượng khách bằng 0).
    *   Đề xuất hướng xử lý bằng biểu thức logic kiểm tra tính hợp lệ của dữ liệu.

*   **Phần 3: Sơ đồ luồng dữ liệu (Mermaid Data Flow Diagram)**
    *   Vẽ sơ đồ Mermaid diễn tả luồng dữ liệu từ lúc nhận Input -> Qua các bước tính toán đại số/logic -> Xuất ra Output.
    *   Tuân thủ nghiêm ngặt chuẩn hình dạng:
        *   Oval `([Bắt đầu / Kết thúc])`
        *   Hình bình hành `[/Đầu vào / Đầu ra/]`
        *   Hình chữ nhật `["Thực hiện hành động / Tính toán"]`
        *   Hình thoi `Kiểm tra điều kiện?`

*   **Phần 4: Triển khai mã nguồn Python**
    *   Viết chương trình Python 3.12 hoàn chỉnh thực hiện các tính toán logic và số học đã thiết kế.
    *   **Yêu cầu kỹ thuật**:
        *   Sử dụng Type Hints đầy đủ cho các biến.
        *   Tuân thủ chuẩn đặt tên `snake_case` cho biến theo chuẩn PEP 8.
        *   TUYỆT ĐỐI KHÔNG sử dụng: câu lệnh rẽ nhánh `if/else`, vòng lặp `for/while`, các kiểu dữ liệu nâng cao `list`, `dict`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex14`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex14`