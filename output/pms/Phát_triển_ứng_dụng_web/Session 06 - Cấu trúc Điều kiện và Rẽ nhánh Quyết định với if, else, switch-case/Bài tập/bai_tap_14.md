# <center>[Sáng tạo 2] Thiết kế Động cơ Phân loại và Tự động hóa Check-in Hàng không</center>

### **1. Mục tiêu**
*   **Tư duy kiến trúc hệ thống:** Tự thiết kế mô hình dữ liệu (Schema) đầu vào/đầu ra và chủ động phát hiện các xung đột nghiệp vụ, lỗi biên trong hệ thống thủ tục bay.
*   **Vận dụng tổng hợp cấu trúc điều kiện:** Kết hợp linh hoạt `if...else`, `switch-case`, và toán tử ba ngôi (`?:`) trong JavaScript (ES6+) để xử lý logic rẽ nhánh phức tạp.
*   **Mô hình hóa quy trình:** Trực quan hóa luồng dữ liệu quyết định (Data Flow Diagram) bằng sơ đồ Mermaid đạt chuẩn công nghiệp.
*   **Hiện thực hóa giải pháp:** Viết mã nguồn sạch, tự bảo vệ trước dữ liệu bất hợp lệ và đáp ứng đầy đủ yêu cầu nghiệp vụ thực tế.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống làm thủ tục chuyến bay (Check-in System) của hãng hàng không Vietjet / Vietnam Airlines, việc xác định điều kiện duyệt check-in, tính phí phụ thu hành lý quá cước, và phân luồng lối đi ưu tiên đòi hỏi xử lý đồng thời nhiều tham số: hạng vé (`ticketClass`), trọng lượng hành lý ký gửi (`baggageWeight`), trạng thái đặt chỗ (`bookingStatus`), và thẻ hội viên (`isVip`).

Hiện tại, quy trình tại các quầy thủ tục và Kiosk tự động đang gặp sự cố ùn tắc do logic rẽ nhánh bị chồng chéo. Hệ thống cũ thiếu cơ chế phân loại tập trung, dẫn đến tình trạng hành khách bị tính sai phí hành lý hoặc được cấp nhãn ưu tiên không đúng với hạng vé.

Bộ phận Kiến trúc Phần mềm yêu cầu bạn thiết kế và phát triển một **"Động cơ Phân loại & Tự động hóa Check-in"** độc lập bằng JavaScript. Động cơ này phải tự động tiếp nhận dữ liệu hành khách, kiểm tra tính hợp lệ của mã đặt chỗ, tính toán chính xác chi phí phát sinh, và quyết định cấp thẻ lên máy bay (Boarding Pass) kèm theo hướng dẫn luồng di chuyển phù hợp.

### **3. Quy tắc nghiệp vụ**
Động cơ của bạn phải bao quát được 3 khối quyết định cốt lõi sau:

1.  **Phân loại Trạng thái Đặt chỗ (`switch-case`):**
    *   Mã trạng thái `1`: "Đã xác nhận thanh toán - Sẵn sàng check-in".
    *   Mã trạng thái `2`: "Đã check-in thành công - Chờ ra cửa khởi hành".
    *   Mã trạng thái `3`: "Vé thuộc danh sách kiểm tra an ninh tăng cường (SSSS)".
    *   Mã trạng thái `4`: "Vé đã hủy hoặc yêu cầu hoàn tiền".
    *   Mã trạng thái khác: "Mã trạng thái đặt chỗ không hợp lệ".

2.  **Tính Phí Hành lý Quá cước (`if...else` / `if` lồng ghép):**
    *   Hạng `Business`: Miễn phí hành lý ký gửi tối đa 30 kg. Mỗi kg vượt quá tính phí 50.000 VNĐ/kg.
    *   Hạng `Deluxe`: Miễn phí hành lý ký gửi tối đa 20 kg. Mỗi kg vượt quá tính phí 60.000 VNĐ/kg.
    *   Hạng `Eco`: Miễn phí hành lý ký gửi 0 kg (chỉ có 7 kg xách tay). Nếu ký gửi, toàn bộ trọng lượng hành lý ký gửi tính 70.000 VNĐ/kg.
    *   [LƯU Ý]: Trọng lượng hành lý nhập vào không được phép là số âm.

3.  **Gán Nhãn Ưu tiên & Lựa chọn Ghế ngồi (Toán tử ba ngôi `?:`):**
    *   Nhãn luồng di chuyển (`boardingZone`): Hành khách có thẻ `isVip === true` hoặc đi hạng `Business` được gán nhãn `"Priority Fast-Track"`, ngược lại gán nhãn `"Standard Zone"`.
    *   Quyền chọn ghế (`seatSelectionFee`): Hạng `Business` hoặc `Deluxe` được miễn phí chọn ghế (`0 VNĐ`), hạng `Eco` tính phí chọn ghế trước (`50.000 VNĐ`).

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Phần mềm độc lập triển khai 4 phần nhiệm vụ sau:

*   **Phần 1 - Tự thiết kế I/O Schema:**
    *   Khai báo bộ dữ liệu kiểm thử (dạng các biến `const`/`let`) đại diện cho thông tin lượt check-in của một hành khách.
    *   Thiết kế cấu trúc đầu ra chứa thông tin đầy đủ: Trạng thái check-in (Đạt/Từ chối), Nhãn thông báo, Tổng chi phí phụ thu (Phí hành lý + Phí chọn ghế), và Luồng di chuyển áp dụng.

*   **Phần 2 - Chủ động phát hiện Bẫy dữ liệu (Edge Cases):**
    *   Liệt kê ít nhất 3 trường hợp dữ liệu biên hoặc xung đột logic có thể xảy ra trong thực tế (Ví dụ: Trọng lượng hành lý là số âm, hạng vé nhập sai chính tả, mã trạng thái vé đã hủy nhưng vẫn cố tình check-in hành lý quá cước...).
    *   Đề xuất giải pháp xử lý ngắn gọn bằng câu lệnh điều kiện cho từng kịch bản.

*   **Phần 3 - Vẽ Sơ đồ luồng dữ liệu (Mermaid Data Flow Diagram):**
    *   Vẽ sơ đồ Mermaid thể hiện toàn bộ luồng ra quyết định của động cơ check-in.
    *   Tuân thủ nghiêm ngặt quy chuẩn hình khối:
        *   Khối Bắt đầu / Kết thúc: Hình bo tròn `([Bắt đầu quy trình])` / `([Kết thúc quy trình])`.
        *   Khối Đầu vào / Đầu ra: Hình bình hành `[/Đầu vào: .../]` / `[/Đầu ra: .../]`.
        *   Khối Kiểm tra điều kiện: Hình thoi `Kiểm tra điều kiện?` kèm nhãn mũi tên `-->|Đúng|` / `-->|Sai|`.
        *   Khối Hành động / Tính toán: Hình chữ nhật `["Tính phí hành lý"]`.

*   **Phần 4 - Hiện thực hóa Mã nguồn JavaScript (ES6+):**
    *   Viết chương trình hoàn chỉnh thực thi toàn bộ logic trên.
    *   Tên biến, tên hằng số bắt buộc bằng **Tiếng Anh** (Ví dụ: `passengerName`, `ticketClass`, `baggageWeight`, `bookingStatusCode`, `extraBaggageFee`).
    *   Chú thích giải thích logic bắt buộc bằng **Tiếng Việt có dấu**.
    *   Sử dụng đúng các cấu trúc đã học (`if/else`, `switch-case`, `?:`), tuyệt đối **KHÔNG** sử dụng hàm nâng cao, vòng lặp, hoặc thư viện ngoài chưa học.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo (mô tả I/O schema, danh sách edge cases, sơ đồ Mermaid) và mã nguồn JS hoàn chỉnh.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session06_Ex14`.
    Ví dụ: `HNKS25CNTT1_Core_Session06_Ex14`
