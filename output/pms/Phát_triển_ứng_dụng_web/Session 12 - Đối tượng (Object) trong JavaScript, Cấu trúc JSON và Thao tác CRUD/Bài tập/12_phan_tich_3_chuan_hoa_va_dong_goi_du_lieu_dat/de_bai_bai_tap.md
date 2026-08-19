# <center>[Phân tích 3] Chuẩn hóa và đóng gói dữ liệu đặt phòng khách sạn</center>

### **1. Mục tiêu**
*   **Vận dụng kiến thức**: Thao tác cập nhật thuộc tính động trong JavaScript (Dot Notation, Bracket Notation), xóa bỏ thông tin nhạy cảm bằng từ khóa `delete`, đóng gói và phục hồi đối tượng bằng `JSON.stringify()` và `JSON.parse()`.
*   **Tư duy phân tích**: Đánh giá các phương án xử lý đối tượng (Object mutation trực tiếp vs Đóng gói đối tượng sạch mới), xây dựng ma trận so sánh đánh đổi (Trade-off) về bộ nhớ và hiệu năng.
*   **Thiết kế hệ thống**: Biểu diễn luồng chuẩn hóa dữ liệu đặt phòng (`BookingReservation`) bằng lưu đồ thuật toán (Flowchart) đúng quy chuẩn thiết kế.

### **2. Bối cảnh & Vấn đề**
Trong ứng dụng đặt phòng du lịch (Agoda / Traveloka), hệ thống tiếp nhận dữ liệu phiếu đặt phòng từ giao diện người dùng dưới dạng một Object JavaScript chứa các trường thông tin thô. Trước khi lưu trữ thông tin vào bộ nhớ tạm hoặc truyền tải qua mạng dưới dạng chuỗi JSON, dữ liệu cần trải qua quá trình tính toán phụ phí check-in sớm, gắn thẻ ưu đãi cho khách đi cùng, xóa bỏ các mã xác thực tạm thời nhạy cảm và chuyển đổi sang định dạng chuỗi JSON chuẩn.

### **3. Quy tắc nghiệp vụ**
Hệ thống cần xử lý đối tượng phiếu đặt phòng (`bookingData`) dựa trên các quy tắc sau:
1.  **Phụ thu check-in sớm**: Nếu giờ nhận phòng (`checkInHour`) nhỏ hơn 12 (trước 12h trưa), hệ thống tính phụ thu 30% trên giá phòng 1 đêm (`roomPricePerNight`). Thuộc tính này phải được ghi vào Object với tên key chứa ký tự gạch ngang: `"early-checkin-fee"`. Nếu check-in từ 12h trưa trở đi, giá trị thuộc tính này bằng 0.
2.  **Ưu đãi trẻ em**: Trẻ em dưới 6 tuổi (`guestAge < 6`) được miễn phí phụ thu người đi cùng. Hệ thống bổ sung thuộc tính `isChildExempt` có giá trị `true` vào Object. Ngược lại, giá trị là `false`.
3.  **Tính tổng chi phí tạm tính (`totalAmount`)**: Cập nhật thuộc tính `totalAmount` cho Object theo công thức:
    `totalAmount = (roomPricePerNight * stayNights) + earlyCheckInFee`.
4.  **Bảo mật dữ liệu (Sanitization)**: Xóa hoàn toàn các trường thông tin nhạy cảm và tạm thời khỏi Object trước khi lưu trữ/truyền tải, bao gồm: `creditCardCVV` và `tempAuthToken`.
5.  **Chuẩn hóa và Đóng gói JSON**: Chuyển đổi toàn bộ đối tượng sau khi chuẩn hóa thành chuỗi JSON chuẩn (`jsonPayload`). Sau đó, kiểm tra việc khôi phục chuỗi JSON này ngược lại thành Object (`restoredBooking`) để truy xuất thuộc tính `"early-checkin-fee"`.

### **4. Yêu cầu bài toán**

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Học viên tự nghiên cứu và tự đề xuất ít nhất **02 phương án kỹ thuật khác nhau** để thực hiện việc cập nhật, xóa thuộc tính nhạy cảm và đóng gói JSON cho đối tượng đặt phòng.
*   Xây dựng bảng so sánh Trade-off giữa các phương án dựa trên 5 tiêu chí bắt buộc:
    *   Tốc độ xử lý (Time Complexity)
    *   Mức độ tiêu tốn bộ nhớ (Memory Footprint)
    *   Khả năng bảo trì (Maintainability)
    *   Độ dễ đọc của mã nguồn (Readability)
    *   Ngữ cảnh áp dụng phù hợp (Suitability)

#### **Phần 2: Giải trình Lựa chọn và Mã giả / Lưu đồ luồng**
*   Lý giải khoa học phương án tối ưu được chọn dựa trên ngữ cảnh hệ thống đặt phòng xử lý lượng lớn phiếu đặt phòng theo thời gian thực.
*   Vẽ lưu đồ thuật toán (Flowchart dạng Mermaid) hoặc mã giả (Pseudocode) cho giải pháp tối ưu đã chọn.
*   [YÊU CẦU CHUẨN HÓA MERMAID]: Lưu đồ Mermaid phải sử dụng đúng 5 hình dạng tiêu chuẩn:
    *   Start/End: Oval `([Bắt đầu])` / `([Kết thúc])`
    *   Input/Output: Parallelogram `[/Nhận bookingData/]` / `[/Xuất jsonPayload/]`
    *   Decision: Diamond `Kiểm tra checkInHour < 12?`
    *   Process: Rectangle `["Tính early-checkin-fee và totalAmount"]`
    *   Flowline: Mũi tên `-->` kèm nhãn `-->|Đúng|` hoặc `-->|Sai|`
    *   *Lưu ý*: KHÔNG dùng ngoặc song song `[/ /]` cho các bước xử lý/tính toán.

#### **Phần 3: Triển khai Mã nguồn & Xử lý lỗi biên**
*   Viết mã nguồn JavaScript (ES6+) triển khai phương án tối ưu đã chọn.
*   Xử lý triệt để các trường hợp biên: tên key chứa dấu gạch ngang (`"early-checkin-fee"`), giờ check-in âm hoặc không hợp lệ, dữ liệu nhạy cảm cần xóa sạch sẽ khỏi bộ nhớ Object trước khi JSON stringify.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session12_Ex12`.
    Ví dụ: `HNKS25CNTT1_Core_Session12_Ex12`
