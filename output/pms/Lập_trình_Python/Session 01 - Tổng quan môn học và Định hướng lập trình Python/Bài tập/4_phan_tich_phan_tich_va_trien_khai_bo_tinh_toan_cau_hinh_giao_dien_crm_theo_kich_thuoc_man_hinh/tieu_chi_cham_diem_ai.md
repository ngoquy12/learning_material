### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Phân tích và Triển khai Bộ tính toán Cấu hình Giao diện CRM theo Kích thước Màn hình — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Phân tích làm rõ bản chất cấu trúc và cơ chế vận hành của Phương án A (Hardcoded conditional logic `if-elif-else`) và Phương án B (Data-driven configuration lookup mapping).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Trình bày đầy đủ bảng so sánh 5 tiêu chí (Độ phức tạp thời gian/bộ nhớ, Khả năng đọc, Khả năng bảo trì, Độ linh hoạt, Bối cảnh áp dụng phù hợp) với lập luận sắc bén, chính xác về mặt kỹ thuật.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Đưa ra lý do thuyết phục dựa trên tính chất mở rộng của sản phẩm CRM (ví dụ: dễ dàng thêm breakpoint mới cho màn hình Ultra-Wide hoặc Foldable mà không phải sửa logic mã nguồn chính).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày mã giả hoặc sơ đồ luồng rõ ràng, bao phủ cả các trường hợp kiểm tra lỗi dữ liệu và các nhánh tính toán layout.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết mã nguồn Python hoạt động chính xác theo kiến trúc đã chọn, tuân thủ chuẩn PEP 8, đặt tên dạng `snake_case`, sử dụng Type Hints đầy đủ.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Sử dụng `raise ValueError` xử lý triệt để các trường hợp `viewport_width <= 0` hoặc sai kiểu dữ liệu đầu vào.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Đầu ra thu được là một `dict` chứa chính xác 3 thuộc tính `device_category`, `max_cards_per_page`, `layout_columns` với giá trị tương ứng chính xác theo quy tắc nghiệp vụ đề ra.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Mã nguồn sạch, không thừa mã rác, các hàm rõ trách nhiệm, ghi chú bằng Tiếng Việt có dấu chuẩn sản xuất.
*   **[5 điểm] Nộp bài GitHub:** Đường dẫn repository GitHub hợp lệ, cấu trúc thư mục nộp bài chuẩn định dạng `[Tên Lớp]_[Môn Học]_Session01_Ex04`.

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Triển khai thêm đoạn mã script sử dụng thư viện `time` hoặc `timeit` để đo đạc và so sánh thời gian thực thi (Performance Benchmark) giữa 2 phương án khi chạy thử nghiệm trên tập dữ liệu 100,000 lượt yêu cầu giả lập.