### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 1] Tính toán chi phí đặt phòng phức hợp và Đánh giá điều kiện xác thực giao dịch — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Đưa ra bảng phân tích đầu vào (Input) và đầu ra (Output) đầy đủ tên biến `snake_case` Tiếng Anh, mô tả nghiệp vụ và kiểu dữ liệu chuẩn Python (`int`, `float`, `bool`).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Vẽ được sơ đồ luồng Mermaid đầy đủ, sử dụng chuẩn xác 5 hình khối theo quy định kỹ thuật (Oval cho Start/End, Parallelogram cho Input/Output, Rectangle cho Process, Diamond cho Decision).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo đầy đủ các biến đầu vào mô phỏng giao dịch với Type Hints rõ ràng (`base_price_per_night: int`, `nights_count: int`, `paid_deposit: float`, ...), đúng quy chuẩn PEP 8.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Thực hiện chính xác các công thức tính phụ thu check-in sớm, phụ thu vượt số lượng khách, tổng tiền trước thuế, thuế VAT 10%, tổng tiền thanh toán và mức cọc yêu cầu 50%.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Thực hiện chính xác phép so sánh kiểm tra tiền cọc `paid_deposit >= required_deposit` và ngưỡng nâng hạng VIP `total_amount >= 15000000` mà không vi phạm phạm phạm vi kiến thức cấm.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Áp dụng phép chia lấy phần nguyên `//` để tính toán chi phí trung bình trên mỗi khách (`total_amount // total_guests`) và thực hiện phép so sánh `<=` ngưỡng 2,500,000 VND một cách chính xác.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Xuất báo cáo tài chính ra màn hình console bằng các câu lệnh `print()` chuyên nghiệp, mô tả đúng ý nghĩa kinh doanh của từng chỉ số tài chính và giá trị trạng thái `True`/`False`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tên biến và hằng số hoàn toàn bằng Tiếng Anh, câu lệnh rõ ràng, có chú thích giải thích logic bằng Tiếng Việt có dấu, tuân thủ thụt lề 4 khoảng trắng.
*   **[5 điểm] Nộp bài GitHub:** Đẩy toàn bộ báo cáo và mã nguồn lên GitHub đúng cấu trúc thư mục quy định: `[Tên Lớp]_[Môn Học]_Session04_Ex7`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Thực hiện làm tròn tiền thuế VAT bằng hàm `round()` hoặc ép kiểu tường minh `int()` để tránh hiện tượng sai số số thực trong Python khi hiển thị tiền tệ VND.