### **Tiêu chí chấm điểm (AI)**
**Hệ Thống Tính Phí Giao Dịch và Quét Giao Dịch Bất Thường Fintech — Tổng điểm: 100 điểm**

Chương trình sẽ được đánh giá tự động và thủ công dựa trên các tiêu chí nghiêm ngặt sau:

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
*   **10 điểm**: Khai báo và tổ chức mã nguồn đầy đủ 5 hàm theo đúng tên gọi, cấu trúc tham số đầu vào và kiểu dữ liệu đầu ra được chỉ định trong bảng mô tả yêu cầu.
*   **10 điểm**: Khởi tạo và theo dõi chính xác trạng thái biến tích lũy hạn mức chi tiêu ngày (`daily_accumulated`) và việc cập nhật số dư (`balance`) của tài khoản xuyên suốt quá trình lặp duyệt qua lô dữ liệu.

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
*   *Tính phí bậc thang (10 điểm)*: Triển khai chính xác logic tính phí bậc thang cho cả 3 nhóm tài khoản (Personal, Business, Premium), kiểm tra đầy đủ các điều kiện chặn trần (phí tối đa) và chặn sàn (phí tối thiểu).
*   *Phát hiện trùng lặp giao dịch (10 điểm)*: Viết đúng logic vòng lặp hoặc truy xuất chỉ mục để kiểm tra dấu vết giao dịch lịch sử nhằm phát hiện chính xác mẫu spam (chuỗi 3 giao dịch giống nhau liên tục thành công).
*   *Xử lý hạn mức (10 điểm)*: Áp dụng đúng quy tắc kiểm tra hạn mức giao dịch đơn lẻ của từng phân hạng tài khoản và tích lũy kiểm tra hạn mức ngày dồn tích. Các giao dịch bị từ chối không được tính cộng dồn hay trừ tiền khỏi số dư tài khoản.

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
*   *Kiểm chuẩn định dạng đầu vào (15 điểm)*: Nhận diện chính xác và phân loại trạng thái `"INVALID_DATA"` cho các giao dịch thiếu trường thông tin bắt buộc, số tiền không phải kiểu số (trừ các trường hợp chuỗi số hợp lệ có thể ép kiểu an toàn), hoặc có giá trị âm/bằng không.
*   *Xử lý cạn kiệt số dư (15 điểm)*: Kiểm tra điều kiện số dư tài khoản hiện tại có đủ để thực hiện giao dịch sau khi đã cộng thêm phí hay không (Số dư >= Số tiền giao dịch + Phí giao dịch). Nếu không đủ, giao dịch phải bị từ chối với nhãn trạng thái thích hợp (ví dụ: `"INSUFFICIENT_BALANCE"`).

#### **4. Kiểm thử hoặc câu hỏi lý thuyết bổ sung — 10 điểm**
*   **5 điểm**: Cung cấp hàm kiểm thử (kịch bản chạy thử nghiệm) chứa ít nhất 5 trường hợp giao dịch bao quát toàn bộ các trạng thái đầu ra mong muốn (`SUCCESS`, `DAILY_LIMIT_EXCEEDED`, `LIMIT_EXCEEDED`, `SUSPICIOUS_SPAM`, `INVALID_DATA`).
*   **5 điểm**: Thực thi thành công hàm lọc giao dịch `filter_transactions_by_status` và in ra bảng tổng hợp báo cáo trực quan cho người dùng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **5 điểm**: Mã nguồn trình bày sạch sẽ, đặt tên biến/hàm theo chuẩn `snake_case` khoa học bằng tiếng Anh, có chú thích bằng tiếng Việt làm rõ các đoạn mã logic phức tạp. Tuyệt đối không chứa các debug print dư thừa hoặc mã thừa không chạy.
*   **5 điểm**: Sinh viên nộp bài đúng hạn, cấu trúc Git đúng quy định và có file README.md mô tả cách vận hành chương trình.

#### **Điểm cộng khuyến khích (Bonus) — 5 điểm**
*   **5 điểm**: Tối ưu hóa thuật toán phát hiện spam trùng lặp liên tiếp sử dụng kỹ thuật trượt cửa sổ (sliding window) hoặc tối ưu hóa bộ nhớ khi xử lý các lô giao dịch cực lớn lên tới hàng chục nghìn phần tử mà không gây lag hệ thống.