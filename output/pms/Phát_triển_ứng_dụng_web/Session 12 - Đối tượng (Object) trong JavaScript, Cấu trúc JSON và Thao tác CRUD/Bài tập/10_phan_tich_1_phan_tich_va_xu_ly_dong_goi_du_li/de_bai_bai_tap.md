# <center>[Phân tích 1] Phân tích và Xử lý Đóng gói Dữ liệu Đặt phòng Khách sạn</center>

### **1. Mục tiêu**
*   **Hiểu sâu cấu trúc Object Literal và JSON**: Nắm vững cơ chế lưu trữ dữ liệu đối tượng theo dạng key-value, phân biệt sự khác nhau giữa đối tượng trong bộ nhớ RAM và chuỗi dữ liệu JSON trong bài toán đặt phòng trực tuyến.
*   **Thao tác linh hoạt với thuộc tính đối tượng**: Thành thạo việc truy cập thuộc tính bằng Dot Notation và Bracket Notation (đặc biệt là Dynamic Key Access khi tên thuộc tính chứa ký tự đặc biệt hoặc được truyền qua biến).
*   **Thao tác CRUD thuộc tính và bảo vệ dữ liệu**: Biết cách thêm mới, cập nhật và xóa bỏ hoàn toàn thuộc tính thừa/nhạy cảm bằng từ khóa `delete` trước khi đóng gói dữ liệu gửi lên server.
*   **Năng lực phân tích bài toán (Analysis 1)**: Đánh giá ưu/nhược điểm giữa các phương án xử lý cấu trúc đối tượng, lựa chọn giải pháp tối ưu về hiệu năng và tính an toàn dữ liệu.

---

### **2. Bối cảnh & Vấn đề**
Trong phân hệ quản lý thông tin đặt phòng (`HOTEL_BOOKING`) của các ứng dụng như Traveloka hay Agoda, mỗi khi khách hàng thực hiện thay đổi thông tin hoặc tiến hành thanh toán, hệ thống sẽ khởi tạo một đối tượng dữ liệu lưu trữ tạm thời (`BookingReservation`). 

Đối tượng này lưu giữ nhiều trường dữ liệu quan trọng như mã đặt phòng, giá phòng ban đầu, giờ check-in dự kiến, tuổi của trẻ em đi kèm, cùng các mã xác nhận giao dịch tạm thời (ví dụ: `tempAuthToken`, `draftDiscountCode`).

Vấn đề đặt ra là hệ thống cần phải xử lý cập nhật các khoản phụ phí phát sinh (như phụ thu check-in sớm, phụ thu trẻ em), bổ sung thông tin liên lạc động do khách hàng điền vào, đồng thời bắt buộc phải **loại bỏ sạch sẽ các mã xác nhận tạm thời** trước khi đóng gói đối tượng thành chuỗi JSON (`JSON.stringify`) để lưu vào cơ sở dữ liệu hoặc truyền qua mạng. Nếu lập trình viên xử lý sai (ví dụ: chỉ gán giá trị `undefined`/`null` thay vì dùng `delete`, hoặc truy cập sai cú pháp key động chứa dấu gạch ngang), dữ liệu gửi đi sẽ bị phình to, lộ thông tin nhạy cảm hoặc gây ra lỗi dừng chương trình đột ngột (`ReferenceError` / `SyntaxError`).---

### **3. Quy tắc nghiệp vụ**
Hệ thống xử lý đối tượng đặt phòng `bookingData` phải tuân thủ nghiêm ngặt các quy tắc sau:

1.  **Phụ thu Check-in sớm**: 
    *   Nếu giờ check-in thực tế (`checkInHour`) nhỏ hơn 12 (12h trưa), tính thêm phụ thu 30% trên giá phòng gốc (`basePrice`).
    *   Tạo thuộc tính mới `earlyCheckInFee` trên đối tượng để lưu số tiền phụ thu này. Nếu không check-in sớm, giá trị phụ thu là `0`.
2.  **Phụ thu Trẻ em đi kèm**:
    *   Trẻ em dưới 6 tuổi (tuổi `< 6`) được miễn phí lưu trú.
    *   Trẻ em từ 6 tuổi trở lên tính phụ thu `childSurcharge` là `150000` VNĐ/trẻ.
3.  **Cập nhật trường dữ liệu động (Dynamic Property)**:
    *   Khách hàng có thể gửi bổ sung thông tin liên hệ khẩn cấp hoặc yêu cầu đặc biệt với tên thuộc tính chứa ký tự đặc biệt như `"emergency-contact"` hoặc `"special-request"`.
    *   Phải sử dụng Bracket Notation (`obj[key]`) với biến động để gán dữ liệu này vào đối tượng.
4.  **Làm sạch dữ liệu nhạy cảm/tạm thời**:
    *   Trước khi chuyển đổi sang JSON, phải dùng từ khóa `delete` để xóa bỏ hoàn toàn 2 trường tạm thời: `tempAuthToken` và `draftDiscountCode`.
    *   [WARNING] CẤM gán `undefined` hoặc `null` vì gán `undefined` vẫn giữ lại tên key trong đối tượng gốc, gây lãng phí bộ nhớ.
5.  **Đóng gói và Đọc dữ liệu JSON**:
    *   Đóng gói đối tượng đã làm sạch thành chuỗi JSON bằng `JSON.stringify()`.
    *   Thực hiện giải mã ngược lại thành đối tượng JavaScript bằng `JSON.parse()` và in ra màn hình thông tin cập nhật cuối cùng để xác nhận dữ liệu vẹn toàn.

---

### **4. Yêu cầu bài toán**

Học viên đóng vai trò là Lập trình viên JavaScript Senior, thực hiện bài nộp gồm 3 phần:

#### **Phần 1: Đề xuất & Báo cáo Phân tích Trade-off (Multi-Solution Proposal & Analysis Report)**
*   Tự nghiên cứu, tự đề xuất ít nhất **2 phương án kỹ thuật khác nhau** để giải quyết bài toán: tiếp nhận đối tượng đặt phòng, tính toán phụ phí, gán thuộc tính động, làm sạch trường tạm thời và đóng gói JSON.
*   *Lưu ý: Học viên tự đưa ra các giải pháp dựa trên tư duy lập trình (ví dụ: Biến đổi trực tiếp trên đối tượng gốc vs Tạo đối tượng mới trung gian; hoặc Thao tác thủ công từng thuộc tính vs Đóng gói hàm helper).*
*   Xây dựng bảng so sánh Trade-off trực quan giữa 2 phương án theo 5 tiêu chí:
    1.  **Tốc độ xử lý (Speed)**
    2.  **Dung lượng bộ nhớ (Memory)**
    3.  **Khả năng bảo trì (Maintainability)**
    4.  **Độ rõ ràng của mã nguồn (Readability)**
    5.  **Độ phù hợp thực tế (Suitability)**
*   *Bảng so sánh phải sử dụng định dạng HTML chuẩn:*
    `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`

#### **Phần 2: Giải trình Lựa chọn & Thiết kế Mã giả/Lưu đồ (Trade-off Justification & Flowchart Design)**
*   Đưa ra lý giải khoa học thuyết minh lý do lựa chọn 1 phương án tối ưu nhất cho hệ thống đặt phòng trực tuyến.
*   Thiết kế **Lưu đồ thuật toán (Mermaid Flowchart)** hoặc **Mã giả (Pseudocode)** cho phương án tối ưu đã chọn.
*   *Quy tắc bắt buộc khi vẽ Mermaid Flowchart:*
    *   Khối Bắt đầu / Kết thúc: Dùng Oval `([Bắt đầu])` / `([Kết thúc])`.
    *   Khối Đầu vào / Đầu ra: Dùng Hình bình hành `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
    *   Khối Kiểm tra điều kiện: Dùng Hình thoi `Kiểm tra...?`.
    *   Khối Thực hiện hành động / Tính toán: Dùng Hình chữ nhật `["Tính toán phụ thu..."]`. Tuyệt đối không dùng hình bình hành cho hành động tính toán.

#### **Phần 3: Triển khai Mã nguồn & Xử lý Lỗi biên (Implementation & Bug Prevention)**
*   Viết mã nguồn JavaScript (ES6+) hoàn chỉnh triển khai phương án tối ưu đã chọn.
*   Khai báo đối tượng ban đầu `bookingReservation` với đầy đủ các trường dữ liệu theo mô tả.
*   Thực hiện đầy đủ logic nghiệp vụ ở Mục 3 (tính phụ thu check-in sớm, phụ thu trẻ em, gán dynamic key có chứa ký tự đặc biệt, xóa token tạm bằng `delete`, chuyển thành JSON payload và khôi phục bằng `JSON.parse`).
*   Bắt bẫy lỗi logic biên:
    *   Bẫy lỗi quên ngoặc nháy khi dùng ngoặc vuông khiến JS hiểu nhầm tên key là biến chưa khai báo (`ReferenceError`).
    *   Bẫy lỗi cố tình dùng Dot Notation cho key có chứa dấu gạch ngang (`SyntaxError`).
    *   Bẫy lỗi cố tình truy cập thuộc tính trực tiếp trên chuỗi JSON chưa được `JSON.parse`.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex10`.
    Ví dụ: `HNKS25CNTT1_Core_Session12_Ex10`
