#

# <center>[Phân tích 2] Thiết kế và tối ưu logic tính phí dịch vụ làm thủ tục chuyến bay</center>

### **1. Mục tiêu**
- **Về mặt kỹ thuật**: Phân tích, so sánh và lựa chọn mô hình rẽ nhánh tối ưu (Guard Clauses / `if-else` lồng nhau / `switch-case` kết hợp toán tử ba ngôi) để xử lý cây quyết định điều kiện phức tạp trong JavaScript (ES6+).
- **Về mặt tư duy**: Đánh giá các đánh đổi (trade-offs) về tính đọc hiểu (Readability), bảo trì (Maintainability) và khả năng mở rộng khi triển khai luồng nghiệp vụ kiểm tra hành lý quá cước và phí chọn vị trí ngồi.
- **Về mặt nghiệp vụ**: Làm quen với quy trình check-in tự động của hệ thống hàng không Vietjet / Vietnam Airlines, tính toán chính xác chi phí phát sinh cho từng phân khúc hành khách theo hạng vé và đặc quyền hội viên.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống check-in tự động tại kiosk sân bay hoặc website của hãng hàng không Vietjet / Vietnam Airlines, giai đoạn xác nhận hành lý và chọn vị trí ngồi thường phát sinh các chi phí bổ sung tùy thuộc vào hạng vé và trạng thái tài khoản của khách hàng. Mã nguồn xử lý hiện tại của hệ thống đang gặp tình trạng điều kiện rẽ nhánh chồng chéo phức tạp, dễ gây ra sai sót khi áp dụng chính sách ưu đãi mới.

Hệ thống cần tiếp nhận thông tin làm thủ tục bao gồm: Hạng vé (`ticketClass`), Trọng lượng hành lý ký gửi thực tế (`baggageWeight`), Khu vực ghế ngồi đăng ký (`seatZone`) và Trạng thái hội viên thân thiết (`isVipMember`). Nhiệm vụ của lập trình viên là thiết kế một giải pháp cấu trúc rẽ nhánh tối ưu để tính tổng phí phát sinh (bao gồm Phí hành lý quá cước + Phí chọn chỗ ngồi), đồng thời xử lý triệt để các trường hợp dữ liệu đầu vào không hợp lệ.

### **3. Quy tắc nghiệp vụ**
1. **Mã hóa dữ liệu đầu vào**:
   - `ticketClass` (Số nguyên): `1` - Eco (Phổ thông), `2` - Deluxe (Đặc biệt), `3` - Business (Thương gia).
   - `baggageWeight` (Số thực/nguyên): Trọng lượng hành lý ký gửi thực tế (tính bằng kg).
   - `seatZone` (Số nguyên): `1` - Ghế tiêu chuẩn (Standard), `2` - Ghế hàng đầu (Front Row), `3` - Ghế lối thoát hiểm / Rộng chân (Emergency Exit).
   - `isVipMember` (Boolean): `true` (Hội viên VIP) hoặc `false` (Khách hàng thường).

2. **Quy tắc tính Phí hành lý quá cước (Baggage Fee)**:
   - **Hạng Eco (`1`)**: Miễn phí tối đa 7 kg. Mỗi kg vượt quá tính 50.000 VNĐ/kg.
   - **Hạng Deluxe (`2`)**: Miễn phí tối đa 20 kg. Mỗi kg vượt quá tính 50.000 VNĐ/kg.
   - **Hạng Business (`3`)**: Miễn phí tối đa 30 kg. Mỗi kg vượt quá tính 40.000 VNĐ/kg.
   - **Ưu đãi VIP**: Nếu `isVipMember === true`, tổng phí hành lý quá cước sẽ được giảm 10%. (Lưu ý: Chỉ áp dụng giảm giá trên phí hành lý quá cước, không giảm trên phí chọn ghế).

3. **Quy tắc tính Phí chọn chỗ ngồi (Seat Fee)**:
   - **Hạng Business (`3`)**: Miễn phí 100% cho tất cả vị trí ghế (`seatZone` 1, 2, 3 đều tính 0 VNĐ).
   - **Hạng Deluxe (`2`)**: Miễn phí `seatZone` 1 và 2 (0 VNĐ); `seatZone` 3 thu phí 100.000 VNĐ.
   - **Hạng Eco (`1`)**: `seatZone` 1 tính 30.000 VNĐ; `seatZone` 2 tính 80.000 VNĐ; `seatZone` 3 tính 150.000 VNĐ.

4. **Xử lý dữ liệu không hợp lệ (Edge Cases)**:
   - Nếu `ticketClass` không thuộc {1, 2, 3} hoặc `seatZone` không thuộc {1, 2, 3} hoặc `baggageWeight < 0`: Đánh dấu dữ liệu không hợp lệ, trả về tổng phí bằng `-1` và hiển thị thông báo lỗi tương ứng.

### **4. Yêu cầu bài toán**
Học viên hoàn thành bài tập theo 3 phần nội dung sau:

#### **Phần 1: Báo cáo Đề xuất Đa giải pháp & Phân tích Đánh đổi (Trade-off Report)**
- Tự đề xuất ít nhất **2 phương án kỹ thuật độc lập** để triển khai luồng rẽ nhánh điều kiện cho bài toán trên (ví dụ: mô hình rẽ nhánh lồng nhau `if-else`, mô hình điều kiện bảo vệ `Guard Clauses`, hoặc kết hợp `switch-case` tách biệt theo phân khúc hạng vé).
- Lập bảng so sánh Đánh đổi (Trade-off) theo 5 tiêu chí:
  1. Độ phức tạp thời gian (Time Complexity).
  2. Dung lượng bộ nhớ duy trì (Memory Footprint).
  3. Khả năng bảo trì & mở rộng (Maintainability & Extensibility).
  4. Độ sạch và dễ đọc của mã nguồn (Code Readability).
  5. Bối cảnh áp dụng phù hợp (Suitability).

#### **Phần 2: Lựa chọn Phương án Tối ưu & Thiết kế Mã giả/Lưu đồ**
- Lý giải khoa học lý do chọn phương án tối ưu nhất dưới góc độ kiến trúc mã nguồn Clean Code.
- Trình bày các bước xử lý logic bằng **Mã giả (Pseudocode)** hoặc **Lưu đồ thuật toán (Mermaid Flowchart)** chuẩn hóa.

#### **Phần 3: Triển khai Mã nguồn & Kiểm chuẩn Logic**
- Viết mã nguồn hoàn chỉnh bằng JavaScript (ES6+) thực thi phương án đã lựa chọn.
- Kiểm thử mã nguồn với nhiều kịch bản dữ liệu khác nhau (bao gồm dữ liệu hợp lệ và dữ liệu lỗi biên).

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session 06_Ex11`.
    Ví dụ: `HNKS25CNTT1_Core_Session 06_Ex11`