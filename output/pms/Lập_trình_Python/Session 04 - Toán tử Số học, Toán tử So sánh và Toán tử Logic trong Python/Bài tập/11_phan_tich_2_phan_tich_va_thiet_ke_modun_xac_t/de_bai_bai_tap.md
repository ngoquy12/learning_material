## <center>[Phân tích 2] Phân tích và Thiết kế Mô-đun Xác thực Điều kiện Ưu đãi VIP Đặt phòng Khách sạn</center>

### **1. Mục tiêu**
*   **Kiến thức:** Hiểu sâu về cách thức hoạt động của toán tử số học, toán tử so sánh và bản chất của kiểu dữ liệu Boolean trong Python mà không phụ thuộc vào câu lệnh rẽ nhánh hay các toán tử logic mặc định.
*   **Kỹ năng:** Phân tích bài toán thực tế, độc lập đề xuất ít nhất 2 giải pháp kỹ thuật, đánh giá ưu/nhược điểm (Trade-off), thiết kế lưu đồ thuật toán Mermaid chuẩn hóa và cài đặt mã nguồn Python 3.12 đáp ứng chuẩn PEP 8.
*   **Tư duy:** Phát triển tư duy tối ưu hóa logic trong xử lý dữ liệu đơn đặt phòng với khối lượng giao dịch lớn.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng trực tuyến (HOTEL_BOOKING) như Agoda hoặc Traveloka, việc kiểm tra điều kiện áp dụng các chương trình ưu đãi cao cấp (VIP Booking Privilege) diễn ra liên tục trên hàng triệu yêu cầu mỗi giờ. Để đảm bảo tốc độ phản hồi tối đa và tránh việc lạm dụng tài nguyên bộ nhớ cho các cấu trúc rẽ nhánh phức tạp, đội ngũ kiến trúc sư phần mềm yêu cầu thiết kế một mô-đun xác thực điều kiện tự động dựa trên đại số số học và toán tử so sánh thuần túy.

Nhiệm vụ của bạn là nghiên cứu cơ chế đại số Boole tích hợp trong số học Python để xây dựng bộ xử lý logic kiểm tra điều kiện nhận ưu đãi VIP cho đơn đặt phòng mà không sử dụng các từ khóa rẽ nhánh hay các toán tử logic nâng cao bị cấm trong phân hệ này.### **3. Quy tắc nghiệp vụ**
Hệ thống tiếp nhận thông tin đơn đặt phòng qua các thông số đầu vào:
*   `nights_stayed` (kiểu `int`): Số đêm khách đăng ký lưu trú.
*   `total_raw_cost` (kiểu `int`): Tổng chi phí nguyên giá của đơn phòng (đơn vị: VNĐ).
*   `has_valid_referral_code` (kiểu `bool`): Xác định khách hàng có nhập mã giới thiệu hợp lệ hay không.
*   `is_vip_member` (kiểu `bool`): Xác định khách hàng có phải là thành viên VIP của hệ thống hay không.

Một đơn đặt phòng được phê duyệt nhận **Ưu đãi VIP** (`is_eligible_for_vip` nhận giá trị `True`) khi thỏa mãn ĐỒNG THỜI các điều kiện sau:
1.  **Điều kiện thời lượng:** Số đêm lưu trú phải từ 3 đêm trở lên (`nights_stayed >= 3`).
2.  **Điều kiện giá trị:** Tổng chi phí nguyên giá phòng phải đạt tối thiểu 5,000,000 VNĐ (`total_raw_cost >= 5000000`).
3.  **Điều kiện đối tượng:** Khách hàng có mã giới thiệu hợp lệ HOẶC là thành viên VIP của hệ thống (tối thiểu 1 trong 2 yếu tố này là `True`).

[GIỚI HẠN KỸ THUẬT NGHIÊM NGẶT]:
*   TUYỆT ĐỐI CẤM sử dụng các câu lệnh rẽ nhánh (`if`, `else`, `elif`).
*   TUYỆT ĐỐI CẤM sử dụng các toán tử logic: `and`, `or`, `not`.
*   TUYỆT ĐỐI CẤM sử dụng các vòng lặp (`for`, `while`) và cấu trúc dữ liệu nâng cao (`list`, `dict`, `set`, `tuple`).
*   Bắt buộc chỉ sử dụng toán tử số học (`+`, `-`, `*`, `//`, `%`, v.v.), toán tử so sánh (`>=`, `>`, `<=`, `<`, `==`, `!=`) và chuyển đổi kiểu `bool()`.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
1.  Độc lập nghiên cứu và đề xuất **ít nhất 2 giải pháp kỹ thuật khác nhau** để giải quyết bài toán kiểm tra điều kiện ghép nối (thỏa mãn cả 3 điều kiện nghiệp vụ) mà không sử dụng `if/else` và toán tử `and/or/not`.
2.  Lập bảng so sánh Trade-off trực quan giữa các giải pháp dựa trên 5 tiêu chí:
    *   Tốc độ thực thi (Execution Speed)
    *   Dung lượng bộ nhớ tiêu tốn (Memory Footprint)
    *   Khả năng bảo trì (Maintainability)
    *   Độ dễ đọc mã nguồn (Readability)
    *   Mức độ phù hợp thực tế (Practical Suitability)

#### **Phần 2: Giải trình Lựa chọn và Mã giả / Lưu đồ luồng**
1.  Đưa ra lý giải khoa học và thuyết phục để chọn ra 1 phương án tối ưu nhất.
2.  Xây dựng mã giả (Pseudocode) và vẽ lưu đồ thuật toán (Flowchart) bằng cú pháp **Mermaid** mô tả chi tiết từng bước xử lý dữ liệu của phương án được chọn.
    *   *Yêu cầu Mermaid:* Bắt buộc tuân thủ 5 dạng hình chuẩn: Oval cho Start/End `([ ... ])`, Hình bình hành cho Input/Output `[/ ... /]`, Hình chữ nhật cho Process `[" ... "]`, Hình thoi cho Decision (Kiểm tra điều kiện), Mũi tên cho luồng thực thi `-->`.

#### **Phần 3: Triển khai mã nguồn & Kiểm thử**
1.  Hiện thực hóa giải pháp tối ưu bằng ngôn ngữ Python 3.12.
2.  Viết hàm `verify_vip_eligibility(nights_stayed: int, total_raw_cost: int, has_valid_referral_code: bool, is_vip_member: bool) -> bool` có đầy đủ Type Hints và chú thích mã nguồn bằng tiếng Việt có dấu.
3.  Kiểm thử mã nguồn với các bộ dữ liệu thử nghiệm để xác nhận tính chính xác của kết quả logic.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex11`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex11`