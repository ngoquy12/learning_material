## <center>[Sáng tạo] Thiết kế Hệ thống Console Điều hướng và Quản lý Đơn hàng E-commerce</center>

### **1. Mục tiêu**
*   **Thiết kế hệ thống giao diện dòng lệnh (CLI Menu):** Xây dựng giải pháp điều hướng menu tương tác quản lý đơn hàng thương mại điện tử linh hoạt và mở rộng.
*   **Tư duy thiết kế kiến trúc phần mềm độc lập:** Tự định nghĩa mô hình dữ liệu (Schema I/O), phát hiện và kiểm soát các tình huống lỗi biên nghiệp vụ (Edge Cases).
*   **Mô hình hóa luồng dữ liệu:** Vẽ và giải thích sơ đồ luồng dữ liệu (Data Flow Diagram) hiển thị vòng đời giao dịch thương mại điện tử.
*   **Tuân thủ tiêu chuẩn lập trình enterprise:** Áp dụng nghiêm ngặt chuẩn PEP 8, Type Hints của Python 3.10+ và không sử dụng các từ khóa lặp bị cấm trong phạm vi bài học.

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quản trị vận hành của một sàn thương mại điện tử (E-commerce Platform), nhân viên hỗ trợ khách hàng cần một công cụ Console CLI điều hướng tương tác để tra cứu, duyệt đơn hàng, áp dụng mã giảm giá (Voucher), cập nhật trạng thái vận chuyển và tính toán doanh thu giao dịch.

Hệ thống đòi hỏi khả năng điều hướng tương tác menu liên tục mà không làm gián đoạn trải nghiệm người dùng, đồng thời phải đảm bảo tính toàn vẹn dữ liệu khi có các thao tác thay đổi trạng thái đơn hàng.



### **3. Quy tắc nghiệp vụ**
*   **Quy trình chuyển đổi trạng thái đơn hàng (Order Workflow):** Đơn hàng chỉ được phép chuyển trạng thái theo đúng thứ tự logic nghiệp vụ (ví dụ: `PENDING` -> `CONFIRMED` -> `SHIPPING` -> `COMPLETED`). Đơn hàng đã ở trạng thái `COMPLETED` hoặc `CANCELLED` thì không được phép thay đổi trạng thái hoặc chỉnh sửa dữ liệu.
*   **Tính toán tổng tiền giao dịch:** Mã giảm giá chỉ được áp dụng hợp lệ nếu giá trị đơn hàng tối thiểu đáp ứng điều kiện nghiệp vụ và mã chưa bị quá hạn sử dụng.
*   **Ràng buộc cú pháp lập trình:** 
    *   [CẤM] Tuyệt đối KHÔNG sử dụng vòng lặp `while`, lệnh `break` hoặc lệnh `continue` trong toàn bộ chương trình (sử dụng giải pháp gọi hàm đệ quy hoặc duy trì luồng điều phối menu thông qua hàm điều hướng tương tác).
    *   [YÊU CẦU] Mã nguồn phải sử dụng Python 3.10+, có Type Hints đầy đủ cho các chữ ký hàm (`def function_name(param: type) -> return_type:`).

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kiến trúc sư phần mềm, tự chủ động thực hiện 4 phần nhiệm vụ sau từ đầu:

*   **Phần 1 - Tự thiết kế I/O Schema chuẩn nghiệp vụ:**
    *   Tự xây dựng cấu trúc dữ liệu lưu trữ danh sách đơn hàng (sử dụng `dict` hoặc `list[dict]`).
    *   Định nghĩa dữ liệu đầu vào (Input Request) và dữ liệu hiển thị (Output Response) cho từng tính năng trong Menu quản trị.

*   **Phần 2 - Chủ động phát hiện Bẫy dữ liệu (Edge Cases):**
    *   Liệt kê ít nhất 03 bẫy dữ liệu hoặc xung đột trạng thái nghiệp vụ (ví dụ: người dùng nhập lựa chọn menu nằm ngoài dải phím cho phép, cố tình áp dụng mã giảm giá cho đơn hàng đã hủy, cập nhật trạng thái ngược quy trình).

*   **Phần 3 - Vẽ Sơ đồ Luồng dữ liệu (Data Flow Diagram):**
    *   Sử dụng cú pháp Mermaid để vẽ sơ đồ luồng dữ liệu mô tả hành trình dữ liệu từ bước hiển thị Menu Console đến logic xử lý và lưu trữ dữ liệu trong bộ nhớ.

*   **Phần 4 - Hiện thực hóa mã nguồn Python:**
    *   Viết mã nguồn Python hoàn chỉnh triển khai toàn bộ giao diện Console Menu và logic quản lý đơn hàng dựa trên bản thiết kế ở 3 phần trên.
    *   Mã nguồn tuân thủ đặt tên biến/hàm bằng tiếng Anh (`snake_case`), chú thích code bằng tiếng Việt có dấu.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex05`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex05`