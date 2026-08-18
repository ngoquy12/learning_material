## <center>[Sáng tạo 2] Thiết kế Mô hình Kiểm tra và Xử lý Chuỗi Mượn Trả Sách Tự động</center>

### **1. Mục tiêu**
*   **Tư duy thiết kế hệ thống:** Tự chủ phân tích bài toán thực tế trong Hệ thống Quản lý Mượn trả Sách Thư viện Trường học (LIBRARY_WMS), thiết kế cấu trúc dữ liệu và quy trình kiểm duyệt chuỗi giao dịch mượn/trả sách tự động.
*   **Vận dụng cú pháp nâng cao:** Áp dụng thành thạo cấu trúc vòng lặp `for` kết hợp với hàm `range()`, các câu lệnh điều khiển luồng `break`, `continue` và khối lệnh `else` của vòng lặp để giải quyết bài toán nghiệp vụ xử lý danh sách giao dịch.
*   **Tư duy phòng ngừa rủi ro:** Tự phát hiện các sai sót dữ liệu (edge cases), xây dựng sơ đồ luồng dữ liệu (Data Flow) chuẩn hóa và hiện thực hóa chương trình chạy chuẩn xác theo tiêu chuẩn mã nguồn PEP 8.

---

### **2. Bối cảnh & Vấn đề**
Hệ thống LIBRARY_WMS đang vận hành tính năng kiểm tra tự động chuỗi giao dịch mượn/trả sách trong ca làm việc. Mỗi ca làm việc, hệ thống sẽ duyệt qua một dải mã giao dịch (được đại diện bởi dãy số nguyên liên tiếp sinh ra từ hàm `range()`).

Trong quá trình duyệt danh sách mã giao dịch mượn/trả:
1.  **Giao dịch vi phạm nhẹ (ví dụ: phiếu mượn thiếu mã barcode cuốn sách hoặc thiếu thông tin lớp học):** Hệ thống cần bỏ qua giao dịch lỗi này bằng câu lệnh `continue` để không gián đoạn tiến trình kiểm tra các giao dịch tiếp theo.
2.  **Giao dịch phát sinh sự cố nghiêm trọng (ví dụ: phát hiện thẻ sinh viên bị khóa do nợ phạt quá hạn chưa thanh toán hoặc sách bị mất/hại nghiêm trọng):** Hệ thống phải dừng khẩn cấp toàn bộ tiến trình kiểm duyệt bằng câu lệnh `break` và phát tín hiệu cảnh báo an ninh.
3.  **Trường hợp tất cả giao dịch đều diễn ra an toàn (không bị ngắt bởi `break`):** Khối `else` đính kèm vòng lặp `for` sẽ được thực thi để xác nhận toàn bộ đợt kiểm duyệt đã hoàn tất thành công và ghi nhận báo cáo tổng hợp.

Ban quản lý thư viện yêu cầu bạn tự thiết kế một kịch bản kiểm duyệt chi tiết, xác định quy tắc phân loại giao dịch và lập trình mô phỏng toàn bộ tiến trình này.---

### **3. Quy tắc nghiệp vụ**
Học viên tự thiết kế kịch bản chi tiết dựa trên các quy định chung của hệ thống LIBRARY_WMS:
*   **Quy định mượn sách:** Mỗi sinh viên mượn tối đa 3 quyển sách trong thời hạn 14 ngày.
*   **Quy định phí phạt:** Phí phạt mượn quá hạn là 5.000 VNĐ/quyển/ngày. Sinh viên chưa hoàn thành phí phạt sẽ bị khóa quyền mượn mới.
*   **Phạm vi duyệt giao dịch:** Sử dụng vòng lặp `for` với `range(start_id, end_id)` để duyệt dải mã giao dịch mượn/trả trong đợt kiểm tra.
*   **Luồng xử lý bằng từ khóa điều khiển:**
    *   Dùng `continue`: Bỏ qua các mã giao dịch gặp sự cố kỹ thuật nhẹ (ví dụ: tem barcode mờ, thiếu ngày hẹn trả).
    *   Dùng `break`: Dừng khẩn cấp toàn bộ ca kiểm duyệt khi gặp lỗi an ninh/nghiệp vụ nghiêm trọng (ví dụ: tài khoản bị khóa do nợ tiền phạt quá hạn, sách bị hủy hoại).
    *   Dùng khối `else` của vòng lặp `for`: Chỉ kích hoạt khi vòng lặp duyệt hết toàn bộ dải `range()` mà không bị ngắt giữa chừng bởi `break`.

[REQUIREMENT] Lưu ý phạm vi kiến thức: Chỉ sử dụng biến cơ bản, câu lệnh `input()`, `print()`, phép toán cơ bản, cấu trúc rẽ nhánh `if/elif/else`, vòng lặp `for` kết hợp `range()`, `break`, `continue` và khối `else`. tuyệt đối CẤM sử dụng: vòng lặp `while`, kiểu dữ liệu danh sách (`list`, `dict`, `tuple`, `set`), định nghĩa hàm (`def`), và lớp đối tượng (`class`).

---

### **4. Yêu cầu đầu ra**

Học viên phải chủ động thực hiện 4 phần nội dung sau trong bài nộp:

#### **Phần 1: Thiết kế I/O Schema & Kịch bản nghiệp vụ tự chọn**
*   Tự định nghĩa dải mã giao dịch mượn trả (ví dụ: từ `101` đến `110`).
*   Tự quy định mã giao dịch nào sẽ bị lỗi nhẹ (dùng `continue`), mã nào bị sự cố nghiêm trọng (dùng `break`).
*   Mô tả rõ ràng kết quả mong đợi tương ứng với kịch bản bạn tự xây dựng.

#### **Phần 2: Phân tích sai sót dữ liệu (Edge Cases)**
Liệt kê và giải thích cách xử lý đối với ít nhất 3 sai sót dữ liệu/trường hợp biên thực tế, ví dụ:
*   Mã bắt đầu lớn hơn hoặc bằng mã kết thúc trong `range()`.
*   Mã sự cố nghiêm trọng trùng ngay ở vị trí giao dịch đầu tiên (`start_id`).
*   Tất cả các mã trong dải đều thuộc dạng bị lỗi nhẹ (liên tục `continue`).

#### **Phần 3: Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram)**
Vẽ sơ đồ quy trình kiểm duyệt bằng cú pháp Mermaid Flowchart. Quy chuẩn hình dạng bắt buộc:
*   Hình bo tròn `([Bắt đầu / Kết thúc])`: Điểm bắt đầu và kết thúc quy trình.
*   Hình bình hành `[/Đầu vào / Đầu ra/]` : Nhập dải mã giao dịch hoặc in thông báo kết quả.
*   Hình thoi `Kiểm tra điều kiện?`: Kiểm tra loại lỗi của mã giao dịch (lỗi nhẹ, lỗi nghiêm trọng, hoặc giao dịch hợp lệ).
*   Hình chữ nhật `["Thực hiện hành động / Tính toán"]`: Tiến hành cập nhật trạng thái, bỏ qua (`continue`), ngắt luồng (`break`).

#### **Phần 4: Triển khai mã nguồn Python**
*   Viết chương trình hoàn chỉnh bằng Python thực thi kịch bản đã thiết kế.
*   Đặt tên biến bằng tiếng Anh theo chuẩn `snake_case` (ví dụ: `start_borrow_id`, `end_borrow_id`, `has_security_issue`).
*   Thêm chú thích tiếng Việt có dấu rõ ràng giải thích từng khối logic.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (Phần 1, 2, 3) và mã nguồn triển khai (Phần 4) vào file báo cáo.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session08_Ex14`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session08_Ex14`