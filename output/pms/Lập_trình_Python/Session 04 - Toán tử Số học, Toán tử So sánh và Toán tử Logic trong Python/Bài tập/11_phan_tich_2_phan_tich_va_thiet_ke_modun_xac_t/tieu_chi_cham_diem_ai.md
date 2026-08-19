# **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Phân tích và Thiết kế Mô-đun Xác thực Điều kiện Ưu đãi VIP Đặt phòng — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Đề xuất đầy đủ và phân tích rõ cơ chế hoạt động của từ 2 phương án trở lên (ví dụ: Phương án 1 dùng phép nhân số học/đại số Boole tích số; Phương án 2 dùng phép cộng số học kết hợp so sánh ngưỡng lớn hơn 0, v.v.).
    *   Không vi phạm danh mục từ khóa bị cấm (`if/else`, `and/or/not`, vòng lặp, list/dict).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Tạo bảng so sánh đầy đủ 5 tiêu chí: Tốc độ execution, Bộ nhớ memory, Tính bảo trì, Độ dễ đọc, Mức độ phù hợp.
    *   Bảng HTML sử dụng đúng thuộc tính style: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Giải trình rõ ràng lý do chọn phương án tối ưu dựa trên độ rõ ràng của logic và tốc độ tính toán trong Python.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ biểu đồ Mermaid chính xác. Bắt buộc dùng Oval `([ ])` cho Bắt đầu/Kết thúc, Hình bình hành `[/ /]` cho Đầu vào/Đầu ra, Hình chữ nhật `[" "]` cho Tính toán/Số học. Không dùng Hình bình hành cho thao tác tính toán.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Khhai báo và định nghĩa hàm `verify_vip_eligibility` đúng signature, có type hints đầy đủ.
    *   Tính toán chính xác logic nghiệp vụ mà không vi phạm phạm vi cấm.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Đảm bảo giá trị trả về đạt chuẩn `True`/`False` cho các trường hợp biên: số đêm = 3, số tiền = 5,000,000, hoặc trường hợp có cả mã giới thiệu lẫn thành viên VIP.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Kết quả trả về chính xác kiểu `bool`, không in thừa các chuỗi không cần thiết trong hàm xử lý logic.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tuân thủ PEP 8 (snake_case cho tên biến và tên hàm), chú thích tiếng Việt có dấu chuẩn sản xuất. Không có từ ngữ suồng sã.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub hợp lệ, cấu trúc thư mục đúng định dạng `[Tên Lớp]_[Môn Học]_Session04_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Viết đoạn mã script đo thời gian thực thi (sử dụng thư viện `time` hoặc `timeit`) so sánh tốc độ thực tế của 2 giải pháp trên 1,000,000 lần lặp.
