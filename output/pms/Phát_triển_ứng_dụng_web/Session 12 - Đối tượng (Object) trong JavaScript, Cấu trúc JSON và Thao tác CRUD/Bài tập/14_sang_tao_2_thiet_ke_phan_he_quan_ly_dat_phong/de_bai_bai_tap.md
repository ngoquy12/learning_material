# <center>[Sáng tạo 2] Thiết kế Phân hệ Quản lý Đặt phòng Động và Chuẩn hóa JSON Payload</center>

### **1. Mục tiêu**
*   **Về kiến thức:** Nắm vững và vận dụng linh hoạt kỹ thuật khởi tạo Object Literal, truy cập thuộc tính tĩnh/động bằng Dot Notation và Bracket Notation (`obj[key]`), các thao tác CRUD thuộc tính đối tượng (`delete`, thêm mới, cập nhật) và mã hóa/giải mã cấu trúc JSON (`JSON.stringify`, `JSON.parse`).
*   **Về kỹ năng:** Tự thiết kế mô hình dữ liệu (I/O Schema), phân tích các điểm nghẽn nghiệp vụ và lỗi biên liên quan đến bảo mật thông tin nhạy cảm trong payload, xây dựng sơ đồ luồng xử lý bằng Mermaid chuẩn hóa và hiện thực hóa mã nguồn JavaScript ES6+ hoàn chỉnh từ đầu.
*   **Về tư duy:** Hình thành tư duy đóng gói dữ liệu an toàn trong các hệ thống Thương mại Điện tử và Đặt phòng Trực tuyến (Enterprise Travel & Hospitality Platform).

---

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đại lý du lịch trực tuyến (OTA) cho nền tảng đặt phòng khách sạn và homestay, đối tượng đơn đặt phòng (`BookingReservation`) luôn biến động liên tục trong suốt quá trình khách hàng tương tác. Ban đầu, một đơn đặt phòng chỉ chứa thông tin cơ bản (mã đơn, mã phòng, thông tin khách, mã bảo mật tạm thời `tempToken`, số thẻ thanh toán thử nghiệm `paymentGatewayPin`). Trong quá trình hoàn tất đặt phòng, hệ thống phải thực hiện nhiều phép tính phụ phí động như: phụ thu check-in sớm, phụ phí giường phụ, dịch vụ ăn uống.

Trước khi gửi dữ liệu hóa đơn giao dịch về máy chủ trung tâm hoặc truyền qua mạng, hệ thống bắt buộc phải thực hiện bước chuẩn hóa dữ liệu: thêm các trường thông tin phụ phí theo dynamic key (chứa ký tự đặc biệt như `early-checkin-fee`, `extra-guest-charge`), xóa bỏ toàn bộ các thuộc tính nhạy cảm hoặc lưu vết nội bộ (`tempToken`, `paymentGatewayPin`, `internalNote`) bằng từ khóa `delete` nhằm đảm bảo an toàn thông tin, sau đó đóng gói đối tượng thành chuỗi JSON hợp lệ. Ở chiều ngược lại, khi nhận dữ liệu JSON phản hồi từ gateway, hệ thống cần parse trở lại dạng Object và giải mã dynamic property để phục vụ tra cứu.

Hệ thống hiện tại đang gặp bài toán dữ liệu bị rò rỉ các key nhạy cảm do lập trình viên chỉ gán giá trị `undefined` hoặc `null` thay vì xóa bỏ hoàn toàn thuộc tính bằng `delete`, dẫn đến chuỗi JSON đóng gói bị phình to và không đáp ứng tiêu chuẩn an toàn thông tin. Bạn được giao nhiệm vụ thiết kế và hiện thực phân hệ đóng gói payload đặt phòng động này.---

### **3. Quy tắc nghiệp vụ**
Hệ thống tính toán phụ thu và đóng gói đơn đặt phòng phải tuân thủ các quy tắc nghiệp vụ thực tế sau:
1.  **Phụ thu Check-in sớm:** Khách hàng check-in trước 12:00 PM sẽ chịu phụ thu 30% giá phòng trị giá 1 đêm. Trường phụ thu này được thêm vào đối tượng đặt phòng với dynamic key tên là `"early-checkin-fee"`.
2.  **Miễn phí trẻ em:** Trẻ em dưới 6 tuổi đi cùng được miễn phí lưu trú hoàn toàn. Nếu trẻ em từ 6 tuổi trở lên hoặc số lượng người vượt chuẩn phòng, hệ thống áp dụng phụ thu người phát sinh với key `"extra-guest-charge"`.
3.  **Chính sách Bảo mật Dữ liệu Payload:** Trước khi chuyển đối tượng đơn đặt phòng (`BookingReservation`) thành chuỗi đại diện JSON, bắt buộc phải loại bỏ triệt để các thuộc tính bảo mật tạm thời (`tempToken`, `paymentGatewayPin`, `internalNote`). Việc gán `undefined` hay `null` bị nghiêm cấm vì vẫn lưu lại dấu vết key trong bộ nhớ đối tượng.
4.  **Chuẩn hóa JSON:** Chuỗi dữ liệu JSON sau khi đóng gói (`JSON.stringify`) phải có khả năng phục hồi hoàn hảo về dạng JS Object (`JSON.parse`) và truy xuất chính xác các thuộc tính bằng cả Dot Notation và Bracket Notation.

---

### **4. Yêu cầu bài toán**

Học viên đóng vai trò là Lập trình viên Frontend Senior, thực hiện hoàn chỉnh 4 phần yêu cầu độc lập dưới đây (không sử dụng khung mã nguồn mẫu, tự thiết kế hoàn toàn):

#### **Phần 1: Tự thiết kế I/O Schema & Mô tả Cấu trúc Dữ liệu**
*   Tự đề xuất cấu trúc Object ban đầu đại diện cho `BookingReservation` chứa các thông tin tĩnh và các thuộc tính nhạy cảm cần loại bỏ.
*   Tự xác định cấu trúc Object sau khi bổ sung các key tính năng phụ thu động và cấu trúc chuỗi JSON đầu ra mong muốn.

#### **Phần 2: Chủ động phát hiện Bẫy dữ liệu (Edge Cases)**
*   Liệt kê ít nhất 3 kịch bản bẫy dữ liệu/lỗi biên có thể phát sinh trong quá trình thao tác với Object và JSON (Ví dụ: Cố tình truy cập key chứa ký tự đặc biệt bằng Dot Notation, gán `undefined` thay vì dùng `delete`, lỗi `SyntaxError` khi parse chuỗi JSON hỏng, hoặc lỗi truy cập thuộc tính trên chuỗi JSON chưa được `JSON.parse`).
*   Mô tả giải pháp xử lý tương ứng cho từng bẫy dữ liệu.

#### **Phần 3: Vẽ Sơ đồ luồng dữ liệu (Data Flow Diagram với Mermaid)**
*   Vẽ sơ đồ Mermaid biểu diễn trọn vẹn vòng đời xử lý của đơn đặt phòng:
    `[Khởi tạo Object ban đầu]` `\rightarrow` `[Thêm/Cập nhật phụ thu bằng Dynamic Key/Bracket Notation]` `\rightarrow` `[Xóa thuộc tính nhạy cảm bằng delete]` `\rightarrow` `[Mã hóa JSON.stringify]` `\rightarrow` `[Giải mã JSON.parse & Kiểm tra thuộc tính]`.
*   Tuân thủ nghiêm ngặt quy chuẩn hình dạng node Mermaid:
    *   Node Bắt đầu / Kết thúc: Hình bo tròn `([Bắt đầu quy trình])`.
    *   Node Kiểm tra điều kiện: Hình thoi `Kiểm tra điều kiện?`.
    *   Node Hành động / Xử lý: Hình chữ nhật `["Thực hiện thao tác"]`.
    *   Node Đầu vào / Đầu ra dữ liệu: Hình bình hành `[/Nhận/Xuất dữ liệu/]`.

#### **Phần 4: Triển khai Mã nguồn JavaScript ES6+**
*   Viết chương trình JavaScript hoàn chỉnh thực hiện toàn bộ luồng nghiệp vụ trên.
*   Đảm bảo mã nguồn thể hiện rõ:
    *   Khai báo Object Literal ban đầu với key chuẩn và key chứa nhãn nhạy cảm.
    *   Sử dụng Bracket Notation để thêm động các trường phụ thu (`"early-checkin-fee"`, `"extra-guest-charge"`).
    *   Sử dụng từ khóa `delete` để làm sạch đối tượng.
    *   Sử dụng `JSON.stringify` để đóng gói dữ liệu thành JSON String.
    *   Sử dụng `JSON.parse` để tái tạo đối tượng và dùng biến động (Dynamic Key Access) để kiểm tra dữ liệu sau khi phục hồi.

---

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (I/O Schema, Edge Cases, Sơ đồ Mermaid) và mã nguồn triển khai trong tệp `main.js` hoặc `app.js`.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex14`.
    *   Ví dụ: `HNKS25CNTT1_Core_Session12_Ex14`
