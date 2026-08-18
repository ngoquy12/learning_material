## <center>[Vận dụng nâng cao 2] Tính phụ phí check-in sớm và xác nhận hóa đơn đặt phòng</center>

### **1. Mục tiêu**
*   **Vận dụng toán tử số học và so sánh trong Python**: Thực hiện các phép tính toán tài chính phức tạp (tính phụ thu nhận phòng sớm, tổng tiền hóa đơn) và xác minh điều kiện phê duyệt đơn đặt phòng mà không sử dụng câu lệnh rẽ nhánh hay các từ khóa logic bị cấm.
*   **Thực hành nguyên tắc Closed How - Open What & Why**: Tự phân tích bài toán nghiệp vụ thực tế trong ngành quản lý khách sạn, tự thiết kế cấu trúc dữ liệu đầu vào/đầu ra và giải thuật số học tương ứng.
*   **Áp dụng quy chuẩn lập trình chuyên nghiệp**: Đảm bảo mã nguồn tuân thủ nghiêm ngặt quy chuẩn PEP 8, khai báo Type Hints đầy đủ và quản lý mã nguồn trên GitHub.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng trực tuyến Agoda / Traveloka, quy trình tự động tính toán hóa đơn thanh toán và xác minh cờ phê duyệt nhận phòng (Check-in Validation Engine) đóng vai trò then chốt giúp tối ưu hóa thời gian vận hành tại quầy lễ tân. 

Khi khách hàng thực hiện đặt phòng, hệ thống cần tính toán chính xác tổng số tiền hóa đơn bao gồm tiền phòng cơ bản và phụ phí nhận phòng sớm (early check-in). Đồng thời, hệ thống phải tự động kiểm tra cờ ưu tiên phê duyệt đơn đặt phòng dựa trên các hạn mức kinh doanh mà khách sạn thiết lập.### **3. Quy tắc nghiệp vụ**
Hệ thống xử lý thông tin dựa trên các thông số đầu vào cơ bản:
*   `room_price` (`float`): Giá niêm yết của phòng cho 1 đêm (đơn vị: VNĐ).
*   `num_nights` (`int`): Số đêm khách lưu trú.
*   `checkin_hour` (`int`): Giờ dự kiến nhận phòng của khách (từ 0 đến 23 giờ).
*   `vip_points` (`int`): Điểm thưởng tích lũy VIP của tài khoản khách hàng.

Các quy tắc tính toán tài chính và kiểm tra điều kiện được định nghĩa như sau:
1.  **Tiền phòng cơ bản (`base_amount`)**: Bằng giá phòng 1 đêm nhân với tổng số đêm lưu trú.
2.  **Định mức phụ phí nhận phòng sớm**:
    *   Khách nhận phòng trước 12 giờ trưa (`checkin_hour < 12`) được xác định là nhận phòng sớm.
    *   Phụ phí nhận phòng sớm tiêu chuẩn bằng 30% giá phòng của 1 đêm (`room_price * 0.3`).
3.  **Chính sách miễn trừ phụ phí VIP**:
    *   Nếu khách hàng có điểm tích lũy VIP từ 1000 điểm trở lên (`vip_points >= 1000`), khách hàng sẽ được miễn 100% phụ phí nhận phòng sớm.
    *   Phụ phí thực tế chỉ áp dụng khi khách nhận phòng sớm VÀ không thuộc diện miễn trừ VIP.
4.  **Tổng tiền hóa đơn (`total_invoice`)**: Bằng tiền phòng cơ bản cộng với phụ phí nhận phòng sớm thực tế phải trả.
5.  **Xác nhận cờ duyệt ưu tiên (`is_priority_approved`)**:
    *   Đơn đặt phòng được đánh dấu ưu tiên nếu thỏa mãn ít nhất một trong hai tiêu chuẩn: Tổng tiền hóa đơn từ 15,000,000 VNĐ trở lên HOẶC giờ nhận phòng nằm trong khung giờ chuẩn từ 14 giờ đến 22 giờ.

[NOTE] Lưu ý quan trọng: Toàn bộ quá trình tính toán và kiểm tra điều kiện phải được thực hiện thuần túy bằng toán tử số học và toán tử so sánh (chuyển đổi biểu thức boolean thành số nguyên 0 và 1 nếu cần). Tuyệt đối KHÔNG sử dụng các từ khóa rẽ nhánh (`if`, `else`), vòng lặp (`for`, `while`), cấu trúc danh sách (`list`, `dict`), hoặc các toán tử logic `and`, `or`, `not`.

### **4. Yêu cầu bài toán**

Bài tập yêu cầu học viên hoàn thiện 2 phần báo cáo và lập trình độc lập:

#### **Phần 1: Báo cáo Phân tích & Thiết kế giải pháp (Analysis & Design Report)**
Học viên trình bày báo cáo bằng Markdown (hoặc vẽ sơ đồ luồng):
1.  **Phân tích Input / Output**: Liệt kê chi tiết tên biến, kiểu dữ liệu, phạm vi hợp lệ và ý nghĩa nghiệp vụ của tất cả dữ liệu đầu vào và đầu ra.
2.  **Đề xuất giải pháp số học**: Giải thích giải thuật tính toán phụ phí và cờ phê duyệt mà không dùng câu lệnh điều kiện rẽ nhánh.
3.  **Thiết kế sơ đồ luồng xử lý (Flowchart)**: Sử dụng cú pháp Mermaid chuẩn để vẽ sơ đồ quy trình tính toán (tuân thủ đúng 5 hình dạng chuẩn: Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho tính toán/xử lý, Diamond cho so sánh kiểm tra).

#### **Phần 2: Cài đặt mã nguồn Python (Implementation)**
Xây dựng chương trình Python 3.12 thỏa mãn các yêu cầu:
*   Khai báo hàm xử lý có Type Hints chuẩn xác cho tất cả tham số và kết quả trả về.
*   Đặt tên biến, tên hàm bằng tiếng Anh theo đúng quy chuẩn PEP 8 (snake_case).
*   Tính toán chính xác tổng hóa đơn và trả về kết quả dưới dạng thông báo rõ ràng ra màn hình Console.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: [Tên Lớp]_[Môn Học]_SessionSession 04_Ex8.
    Ví dụ: HNKS25CNTT1_Core_Session_Session 04_Ex8