## <center>[Sáng tạo] Thiết kế hệ thống đánh giá điều kiện khuyến mãi và phân hạng đơn hàng E-Commerce</center>

### **1. Mục tiêu**
*   **Vận dụng sáng tạo cấu trúc rẽ nhánh:** Sử dụng linh hoạt biểu thức điều kiện `if-elif-else` kết hợp các toán tử logic (`and`, `or`, `not`) để xây dựng phân hệ thẩm định điều kiện ưu đãi tự động cho nền tảng thương mại điện tử.
*   **Chuẩn hóa mã nguồn theo quy chuẩn PEP 8:** Xóa bỏ triệt để anti-pattern "Arrow Code" (lồng ghép câu lệnh điều kiện quá sâu), thực thi thụt lề 4 khoảng trắng chuẩn mực và đặt tên biến/hàm chuẩn `snake_case`.
*   **Tự chủ trong thiết kế giải pháp:** Tự định nghĩa cấu trúc dữ liệu đầu vào/đầu ra, chủ động phát hiện các bẫy dữ liệu giao dịch và biểu diễn tiến trình bằng sơ đồ luồng dữ liệu (Data Flow Diagram).

### **2. Bối cảnh & Vấn đề**
Trong các chiến dịch mua sắm lớn (Mega Sale), hệ thống xử lý đơn hàng của một sàn thương mại điện tử gặp tình trạng quá tải và phản hồi sai logic khuyến mãi. Nguyên nhân xuất phát từ đoạn mã nguồn cũ lồng ghép quá nhiều cấp điều kiện (`if` lồng `if` 5-6 tầng), dẫn đến việc kiểm tra chéo giữa hạng hội viên (Bronze, Silver, Gold, Diamond), tổng giá trị đơn hàng, khoảng cách giao hàng và mã giảm giá bị xung đột.

Ban công nghệ yêu cầu bạn tái thiết kế lại mô-đun thẩm định điều kiện khuyến mãi và tính toán chi phí vận chuyển. Mô-đun mới phải đạt tiêu chuẩn phẳng hóa điều kiện bằng toán tử logic, tối ưu hiệu năng đọc mã và dễ dàng mở rộng các chính sách bán hàng trong tương lai.



### **3. Quy tắc nghiệp vụ**
Hệ thống cần đưa ra quyết định duyệt mức giảm giá chính xác và xác định phí giao hàng dựa trên các nhóm tiêu chuẩn nghiệp vụ sau:
1.  **Thẩm định điều kiện hội viên & Khuyến mãi:** Mỗi hạng hội viên yêu cầu một ngưỡng giá trị đơn hàng tối thiểu khác nhau để kích hoạt ưu đãi. Khách hàng đạt hạng cao (như Gold hoặc Diamond) có thể nhận ưu đãi đặc biệt ngay cả khi giá trị đơn hàng chưa đạt ngưỡng tối đa nếu thời gian gắn bó đạt tiêu chuẩn.
2.  **Chính sách miễn phí vận chuyển (Free Shipping):** Phí vận chuyển phụ thuộc vào khoảng cách giao hàng và tổng tiền đơn. Đơn hàng đạt giá trị cao hoặc thuộc khách hàng VIP ở khu vực nội thành sẽ được miễn phí vận chuyển.
3.  **Cơ chế cảnh báo đơn hàng bất thường (Fraud / Risk Flag):** Nếu đơn hàng có sự bất hợp lý về thông số (ví dụ: áp mã giảm giá cao cấp nhưng điểm uy tín tài khoản thấp, hoặc tổng giá trị tiền âm/bằng 0), hệ thống phải từ chối phê duyệt và trả về trạng thái cảnh báo.

### **4. Yêu cầu bài toán**
Học viên đóng vai trò Kỹ sư Phần mềm chính triển khai tính năng này và cần thực hiện đầy đủ 4 phần công việc sau:

*   **Phần 1 - Tự thiết kế I/O Schema (Self-Designed I/O Schema):** Tự định nghĩa cấu trúc dữ liệu đầu vào (Request Input) và kết quả trả về (Response Output) dạng biến/dict trong Python để đại diện cho thông tin đơn hàng và kết quả thẩm định.
*   **Phần 2 - Chủ động phát hiện kịch bản biên (Self-Discovered Edge Cases):** Liệt kê ít nhất 3 kịch bản bẫy dữ liệu hoặc xung đột trạng thái có thể xảy ra trong giao dịch thực tế và đề xuất cách xử lý rẽ nhánh cho từng trường hợp.
*   **Phần 3 - Vẽ sơ đồ luồng dữ liệu (Data Flow Diagram):** Sử dụng biểu đồ Mermaid (sơ đồ luồng `graph TD` hoặc `flowchart TD`) để mô tả tiến trình xử lý từ khi tiếp nhận dữ liệu đơn hàng đến khi ra quyết định phê duyệt.
*   **Phần 4 - Triển khai mã nguồn Python chuẩn PEP 8:** Viết chương trình Python hoàn chỉnh hiện thực hóa toàn bộ logic trên. Mã nguồn tuyệt đối không được vi phạm anti-pattern lồng lề quá sâu; phải phẳng hóa các câu lệnh điều kiện bằng toán tử `and`, `or`.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex05`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex05`