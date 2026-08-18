#

# <center>[Sáng tạo 1] Thiết kế Module Đóng gói và Xử lý Payload Đặt phòng Khách sạn</center>

### **1. Mục tiêu**
*   **Vận dụng tư duy thiết kế cấu trúc dữ liệu linh hoạt**: Tự định hình và khởi tạo các đối tượng Object Literal phức tạp biểu diễn thông tin đặt phòng, phụ phí động và thông tin khách hàng.
*   **Thành thạo thao tác CRUD trên Object trong JavaScript**: Thực hiện truy cập thuộc tính tĩnh và động (Dot Notation, Bracket Notation), thêm mới dịch vụ đi kèm, cập nhật giá trị phụ phí, và loại bỏ các trường thông tin nhạy cảm/tạm thời bằng từ khóa `delete`.
*   **Làm chủ chu trình chuẩn hóa JSON Payload**: Thực thi việc đóng gói đối tượng (Object Serialization) thành chuỗi JSON và giải mã ngược lại (JSON Parsing) để phục vụ việc truyền nhận dữ liệu an toàn.
*   **Phát triển năng lực phát hiện bẫy dữ liệu và tư duy kiến trúc**: Tự đề xuất các trường hợp biên (Edge Cases), vẽ sơ đồ luồng dữ liệu (Data Flow Diagram) chuẩn kỹ thuật và hiện thực mã nguồn sạch.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng khách sạn và homestay trực tuyến (như Agoda hay Traveloka), mỗi đơn đặt phòng (`BookingReservation`) trải qua nhiều giai đoạn xử lý dữ liệu trước khi được hoàn tất. Khi khách hàng thao tác trên giao diện, hệ thống sinh ra một đối tượng dữ liệu tạm thời chứa mã token xác thực ngắn hạn (`temp-token`), thông tin phòng gốc, thông tin khách hàng và danh sách các dịch vụ phụ thu (check-in sớm, phụ thu người ở thêm, dịch vụ dọn phòng).

Trước khi truyền payload này về hệ thống lưu trữ hoặc xuất hóa đơn, bộ phận kỹ thuật cần xử lý clean dữ liệu:
1.  Bổ sung các trường tính toán phụ thu theo thời gian check-in và độ tuổi của khách.
2.  Cập nhật giá phòng thực tế dựa trên thuộc tính key linh hoạt (Dynamic Key Access).
3.  Xóa bỏ các trường dữ liệu nhạy cảm hoặc trường tạm thời (như `temp-token`, `payment-secret`) để tránh rò rỉ an ninh thông tin.
4.  Đóng gói toàn bộ đối tượng đã làm sạch thành chuỗi JSON hợp lệ để truyền tải, đồng thời có khả năng khôi phục lại đối tượng khi nhận được JSON payload từ máy chủ.

[GHI CHÚ]: Bài tập yêu cầu học viên tự chủ hoàn toàn trong việc thiết kế cấu trúc dữ liệu, đề xuất kịch bản lỗi và triển khai giải pháp lập trình JavaScript nguyên bản (Vanilla JS).

### **3. Quy tắc nghiệp vụ**
Hệ thống cần tuân thủ các quy định tính toán và xử lý thuộc tính đối tượng như sau:
*   **Phụ thu Check-in sớm**: Nếu khách nhận phòng trước 12:00 trưa, hệ thống tự động thêm thuộc tính phụ thu `early-checkin-fee` bằng 30% giá phòng cơ bản một đêm.
*   **Chính sách trẻ em**: Trẻ em dưới 6 tuổi được miễn phí lưu trú. Nếu có người phát sinh từ 6 tuổi trở lên vượt quá số lượng tiêu chuẩn của phòng, hệ thống bổ sung thuộc tính phụ thu `extra-guest-fee`.
*   **Đặt tên Key chứa ký tự đặc biệt**: Các thuộc tính mở rộng có dấu gạch ngang (như `unit-price`, `early-checkin-fee`, `shipping-address`) bắt buộc phải truy cập và khởi tạo bằng Bracket Notation (`obj["key-name"]`).
*   **Làm sạch dữ liệu nhạy cảm**: Các trường dữ liệu bảo mật hoặc thẻ tạm thời (`temp-token`, `raw-password`) bắt buộc phải được xóa hoàn toàn khỏi đối tượng bằng lệnh `delete` (không được gán bằng `undefined` hay `null`).
*   **Đóng gói và Giải mã JSON**: Đối tượng hoàn chỉnh phải được chuyển đổi thành chuỗi JSON bằng `JSON.stringify()`. Khi giải mã chuỗi JSON ngược lại bằng `JSON.parse()`, dữ liệu khôi phục phải đảm bảo nguyên vẹn và cho phép truy cập đúng thuộc tính.

### **4. Yêu cầu bài toán**
Học viên trình bày bài giải theo 4 phần chi tiết trong báo cáo và file mã nguồn:

#### **Phần 1: Tự thiết kế I/O Schema (Cấu trúc Dữ liệu)**
*   Tự thiết kế cấu trúc đối tượng JavaScript ban đầu lưu thông tin đặt phòng (`BookingReservation`) bao gồm các thuộc tính tiêu chuẩn và các thuộc tính có ký tự đặc biệt trong tên key.
*   Tự định nghĩa định dạng chuỗi JSON Payload sau khi đã được đóng gói và làm sạch.

#### **Phần 2: Tự phát hiện bẫy dữ liệu (Edge Cases)**
*   Liệt kê tối thiểu 3 kịch bản lỗi hoặc xung đột dữ liệu có thể xảy ra trong quá trình thao tác trên Object và JSON (Ví dụ: Lỗi ReferenceError khi dùng ngoặc vuông quên ngoặc nháy, lỗi SyntaxError khi dùng Dot Notation cho key chứa gạch ngang, lỗi lãng phí bộ nhớ khi gán `undefined` thay vì `delete`, hoặc lỗi parse chuỗi JSON sai định dạng).

#### **Phần 3: Sơ đồ luồng dữ liệu (Mermaid Data Flow Diagram)**
*   Vẽ sơ đồ luồng dữ liệu minh họa toàn bộ vòng đời từ lúc khởi tạo đối tượng đặt phòng -> cập nhật phụ phí động -> xóa key nhạy cảm -> serialization ra JSON -> deserialization khôi phục Object.
*   *Yêu cầu hình dạng sơ đồ Mermaid*:
    *   HÌNH OVAL `([Bắt đầu / Kết thúc])` cho điểm khởi đầu và kết thúc quy trình.
    *   HÌNH BÌNH HÀNH `[/Nhận dữ liệu / Xuất chuỗi JSON/]` CHO ĐẦU VÀO VÀ ĐẦU RA.
    *   HÌNH CHỮ NHẬT `["Thực hiện cập nhật / Tính phụ thu / Xóa key"]` CHO TẤT CẢ CÁC THAO TÁC XỬ LÝ VÀ TÍNH TOÁN.
    *   HÌNH THOI `Kiểm tra điều kiện?` cho các điểm rẽ nhánh logic.

#### **Phần 4: Mã nguồn triển khai (JavaScript Vanilla ES6+)**
*   Viết đoạn mã JavaScript độc lập (CLI/Script) thực hiện đầy đủ luồng xử lý theo thiết kế ở các phần trên.
*   Mã nguồn phải bao gồm các hàm/đoạn xử lý chuyên biệt cho từng bước: thêm thuộc tính động, cập nhật giá trị bằng biến dynamic key, xóa key nhạy cảm bằng `delete`, kiểm tra `JSON.stringify` và `JSON.parse`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 12_Ex13`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 12_Ex13`