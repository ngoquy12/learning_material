# <center>[Phân tích 3] Thiết kế Luồng Xử lý và Quét Nhật ký Mượn Trả Sách Thư viện Hàng ngày</center>

### **1. Mục tiêu**
*   **Phân tích bài toán kiểm soát chất lượng dữ liệu**: Rèn luyện kỹ năng phân tích luồng xử lý và phát hiện điểm tắc nghẽn khi duyệt dải dữ liệu giao dịch mượn/trả sách thư viện.
*   **Đề xuất chiến lược điều khiển luồng lặp**: So sánh và đánh giá ưu/nhược điểm của việc ứng dụng các câu lệnh điều khiển luồng lặp `for`, `range()`, `break`, `continue` và khối `else` kết hợp.
*   **Thiết kế lưu đồ thuật toán chuẩn hóa**: Chuyển đổi yêu cầu nghiệp vụ thực tế thành sơ đồ Mermaid sử dụng đúng ký hiệu chuẩn.
*   **Triển khai mã nguồn an toàn**: Viết chương trình Python hoàn chỉnh tuân thủ chuẩn PEP 8, xử lý đầy đủ các quy tắc nghiệp vụ và các trường hợp lỗi dữ liệu đầu vào.

---

### **2. Bối cảnh & Vấn đề**
Trong phân hệ Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS), cuối mỗi ngày làm việc, hệ thống tự động tiến hành một tiến trình quét đối soát (Batch Audit Scan) trên dải mã giao dịch phát sinh từ mã bắt đầu `start_id` đến mã kết thúc `end_id`.

Trong quá trình tiến hành đối soát từng mã giao dịch `tx_id`, hệ thống phát sinh các tình huống nghiệp vụ cần xử lý khác nhau:
1. Có những giao dịch bị lỗi dữ liệu nhẹ (như thiếu thông tin sinh viên) cần được bỏ qua để tiếp tục đối soát các mã giao dịch kế tiếp.
2. Có những giao dịch vi phạm quy định an toàn nghiêm trọng (như phát hiện thẻ mượn bị giả mạo hoặc sách bị báo mất đột ngột) đòi hỏi tiến trình quét phải lập tức dừng dừng khẩn cấp để đảm bảo an toàn cho dữ liệu hệ thống.
3. Các giao dịch hợp lệ còn lại cần được ghi nhận, kiểm tra ngày quá hạn và cộng dồn phí phạt (nếu có).

Nếu tiến trình quét hết toàn bộ dải mã mà không gặp bất kỳ vi phạm an toàn nghiêm trọng nào, hệ thống cần đưa ra xác nhận hoàn tất thành công ca trực.---

### **3. Quy tắc nghiệp vụ**

1.  **Dải dữ liệu đầu vào**:
    *   Người dùng nhập vào mã giao dịch bắt đầu (`start_id`) và mã giao dịch kết thúc (`end_id`).
    *   Điều kiện hợp lệ: `start_id > 0` và `end_id >= start_id`.

2.  **Quy định phân loại và xử lý từng mã giao dịch `tx_id` trong dải `[start_id, end_id]`**:
    *   **Trường hợp bỏ qua (`continue`)**: Nếu mã giao dịch `tx_id` chia hết cho 5 (ví dụ: 5, 10, 15...), đây là giao dịch thiếu thông tin. Hệ thống in thông báo bỏ qua và chuyển ngay sang giao dịch tiếp theo mà không cộng dồn thống kê.
    *   **Trường hợp dừng khẩn cấp (`break`)**: Nếu mã giao dịch `tx_id` chia hết cho 13 (ví dụ: 13, 26...), đây là giao dịch vi phạm an ninh nghiêm trọng. Hệ thống in cảnh báo đỏ và lập tức ngắt toàn bộ tiến trình quét lô.
    *   **Trường hợp xử lý hợp lệ**: Các giao dịch còn lại được xem là hợp lệ:
        *   Tăng số lượng giao dịch xử lý thành công lên `1`.
        *   Kiểm tra tính phí phạt quá hạn: Nếu `tx_id` chia hết cho 3, giao dịch này bị quá hạn 2 ngày. Phí phạt áp dụng theo quy định thư viện là 5.000 VNĐ/quyển/ngày (tổng phạt = `2 * 5000 = 10000` VNĐ). Ngược lại, phí phạt bằng 0 VNĐ.

3.  **Báo cáo hoàn tất lô (Khối `else` của vòng lặp `for`)**:
    *   Nếu vòng lặp quét qua toàn bộ dải giao dịch thành công mà **không bị dừng khẩn cấp bởi câu lệnh `break`**, khối `else` của vòng lặp `for` phải được kích hoạt để xuất thông báo: `"Báo cáo ca trực: Toàn bộ lô giao dịch đã được quét an toàn!"`.

---

### **4. Yêu cầu bài toán**

Học viên đóng vai trò là Lập trình viên Hệ thống (Backend Developer) thực hiện 3 phần việc sau:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Đề xuất độc lập **ít nhất 2 giải pháp kỹ thuật khác nhau** để giải quyết bài toán kiểm soát luồng lặp và ghi nhận trạng thái hoàn thành lô giao dịch (Ví dụ: Giải pháp dùng trực tiếp cấu trúc `for...else` kết hợp `break`/`continue` vs Giải pháp dùng biến cờ hiệu `flag_status` kết hợp điều kiện `if` truyền thống).
*   Lập bảng so sánh Trade-off giữa các giải pháp theo 5 tiêu chí:
    *   Tốc độ thực thi (Time Complexity).
    *   Dung lượng bộ nhớ (Memory Overhead).
    *   Khả năng bảo trì và mở rộng (Maintainability).
    *   Độ đọc hiểu mã nguồn (Readability).
    *   Mức độ phù hợp với bài toán thực tế LIBRARY_WMS.
*   *Lưu ý*: Bảng so sánh bắt buộc sử dụng thẻ HTML `<table>` với thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **Phần 2: Lý giải Lựa chọn & Thiết kế Lưu đồ thuật toán (Flowchart)**
*   Đưa ra lý giải khoa học thuyết phục lý do lựa chọn phương án tối ưu nhất.
*   Vẽ lưu đồ thuật toán (Flowchart) thể hiện tiến trình xử lý bằng Mermaid. Sơ đồ phải tuân thủ nghiêm ngặt 5 dạng hình tiêu chuẩn:
    1.  **Start/End**: Hình bầu dục `([Bắt đầu])`, `([Kết thúc])`.
    2.  **Input/Output**: Hình bình hành `[/Đầu vào: .../]`, `[/Đầu ra: .../]`.
    3.  **Process (Thao tác/Tính toán)**: Hình chữ nhật `["Tính tổng phí phạt..."]`.
    4.  **Decision (Điều kiện)**: Hình thoi `Kiểm tra điều kiện?`.
    5.  **Flowline**: Mũi tên chỉ hướng `-->` hoặc `-->|Đúng|`.
*   *Chú ý*: Tuyệt đối không dùng hình bình hành cho các hành động tính toán/gán biến!

#### **Phần 3: Triển khai Mã nguồn & Chặn Lỗi biên**
*   Viết chương trình Python hoàn chỉnh thực thi phương án tối ưu đã chọn.
*   **Phạm vi kiến thức cho phép**: Chỉ sử dụng vòng lặp `for`, hàm `range()`, điều kiện `if/elif/else`, từ khóa `break`, `continue`, khối `else` của vòng lặp `for`, câu lệnh xuất nhập `input()`, `print()` và các kiểu dữ liệu cơ bản (`int`, `str`, `float`, `bool`).
*   **Phạm vi cấm**: Tuyệt đối KHÔNG sử dụng vòng lặp `while`, định nghĩa hàm (`def`), lớp (`class`), danh sách (`list`), từ điển (`dict`), `tuple`, `set` hay bất kỳ thư viện ngoài nào.
*   Xử lý triệt để lỗi biên: Thông báo lỗi nếu người dùng nhập `start_id <= 0` hoặc `end_id < start_id`.

---

### **5. Yêu cầu nộp bài**

Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex12`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 08_Ex12`
