### **Tiêu chí chấm điểm (AI)**
**Tính Cước và Phân Loại Đơn Hàng Logistics — Tổng điểm: 100 điểm**

#### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
*   **Kiểm soát vòng lặp (10 điểm):** Thiết lập được vòng lặp vô hạn `while True` để tiếp nhận dữ liệu nhập liên tục, có cơ chế kết thúc và thoát vòng lặp một cách chuẩn xác khi nhập mã đơn là `"EXIT"` (hoặc chuyển đổi thành viết hoa/thường).
*   **Cơ chế lưu trữ (10 điểm):** Khởi tạo thành công các biến tích lũy (ví dụ: đếm số đơn theo loại hình, tổng khối lượng, tổng tiền gốc) hoặc cấu trúc dữ liệu đơn giản (List) để lưu lại danh sách đơn hàng đã nhập hợp lệ trước khi tính toán tổng thể.

#### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
*   **Tính cước phí cơ bản (10 điểm):** Cài đặt đúng biểu phí động cho dịch vụ Standard (phân tầng khoảng cách dưới và trên 10km) cũng như cước phẳng cho Express và Overnight.
*   **Tính phụ phí tải trọng (10 điểm):** Áp dụng đúng công thức phụ phí cho gói hàng > 10 kg, phân tách chính xác phụ phí giữa nhóm Standard/Express (15,000đ/kg) và Overnight (25,000đ/kg).
*   **Chiết khấu tổng lô hàng (10 điểm):** Sử dụng các biểu thức logic so sánh kết hợp toán tử `and`/`or` để xác định chính xác mức chiết khấu áp dụng (10% hoặc 15%) mà không bị cộng dồn sai quy tắc.

#### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
*   **Kiểm tra kiểu dữ liệu và miền giá trị (15 điểm):** Kiểm soát lỗi khi người dùng nhập dữ liệu không phải số cho khối lượng, khoảng cách bằng cơ chế kiểm thử hoặc bẫy lỗi logic đơn giản. Kiểm tra đúng miền giá trị (Weight: 0 - 100 kg, Distance: 0 - 500 km).
*   **Kiểm chuẩn loại hình dịch vụ (10 điểm):** Bắt lỗi chính xác các trường hợp nhập sai tên loại hình dịch vụ (ví dụ: nhập `"standard"` viết thường hoặc nhập từ không thuộc danh mục quy định) và thông báo cụ thể.
*   **Yêu cầu nhập lại (5 điểm):** Chương trình không bị sập nguồn khi nhập sai, hiển thị rõ thông báo yêu cầu nhập lại thông tin đơn hàng bị lỗi.

#### **4. Kiểm thử hoặc câu hỏi lý thuyết bổ sung — 10 điểm**
*   **In kết quả trung gian và thống kê (10 điểm):** Hiển thị đầy đủ thông số tổng hợp sau khi dừng chương trình (EXIT). Kết quả hiển thị số thực được làm tròn chính xác 2 chữ số thập phân (format `.2f`). Dữ liệu tính toán mẫu phải khớp hoàn toàn với kịch bản test quy định ở phần yêu cầu bài toán.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **Đặt tên biến và comment (5 điểm):** Đặt tên biến rõ ràng bằng tiếng Anh theo chuẩn rắn (`snake_case`), cấu trúc chương trình tường minh bằng các đoạn comment giải thích logic thuật toán.
*   **Quy chuẩn nộp bài (5 điểm):** Tổ chức mã nguồn trong duy nhất một tập tin chạy trực tiếp, lưu trữ và đẩy lên repository GitHub đúng cấu trúc đường dẫn quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **Tối ưu hóa mã nguồn (5 điểm):** Tối ưu hóa cấu trúc rẽ nhánh, giảm thiểu tối đa các nhánh code trùng lặp (redundant code) khi tính phụ phí tải trọng.
*   **Xử lý định dạng đầu vào nâng cao (5 điểm):** Cho phép tự động loại bỏ khoảng trắng dư thừa trong chuỗi ký tự nhập vào hoặc tự động chuyển đổi chữ hoa/thường thông minh để tăng trải nghiệm người dùng.