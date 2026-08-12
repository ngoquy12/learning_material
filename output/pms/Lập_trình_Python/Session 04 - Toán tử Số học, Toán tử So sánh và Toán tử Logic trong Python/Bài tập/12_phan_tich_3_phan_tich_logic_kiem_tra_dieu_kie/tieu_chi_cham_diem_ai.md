### **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Phân Tích Logic Kiểm Tra Điều Kiện Đơn Hàng và Áp Dụng Ưu Đãi POS Highlands — Tổng điểm: 100 điểm**

---

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Đề xuất độc lập tối thiểu 2 phương án tính toán và đánh giá điều kiện nghiệp vụ không dùng `if/else` (Ví dụ: Phương án gộp biểu thức đại số boolean trực tiếp trên 1 dòng duy nhất vs. Phương án phân tách các bước tính giá trị trung gian và chuyển đổi boolean sang số nguyên float/int).
    *   Mô tả rõ cơ chế hoạt động của từng phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Xây dựng bảng so sánh đầy đủ 5 tiêu chí: Thời gian thực thi, Bộ nhớ tiêu tốn, Khả năng bảo trì, Độ dễ đọc, Ngữ cảnh áp dụng.
    *   Thẻ HTML của bảng phải chứa thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

---

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lý do thuyết phục chọn phương án tối ưu dựa trên tiêu chí cân bằng giữa tính dễ đọc (Readability) và khả năng hạn chế lỗi khi bảo trì trong môi trường POS.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Cung cấp lưu đồ Mermaid thể hiện đúng luồng dữ liệu của bài toán.
    *   Tuân thủ nghiêm ngặt quy chuẩn 5 dạng hình dạng Mermaid: Oval `([Start/End])`, Hình bình hành `[/Input/Output/]`, Hình chữ nhật `["Process/Calculation"]`, Hình thoi `Kiểm tra?`, Mũi tên `-->`.

---

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Nhập liệu từ bàn phím và ép kiểu dữ liệu chuẩn xác (`float`, `int`, `bool`).
    *   Tính toán đúng `subtotal`, `discount_amount`, `final_total` và 2 cờ logic `is_vip_order`, `is_eligible_free_ship`.
    *   Tuyệt đối KHÔNG chứa câu lệnh `if/else/elif` hoặc các cấu trúc bị cấm.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Xử lý đúng phép nhân Boolean (`True` tính là 1, `False` tính là 0) để không làm sai lệch kết quả số tiền.
    *   Đảm bảo thứ tự ưu tiên của toán tử số học và toán tử logic (`and`, `or`, `not`) chính xác tuyệt đối bằng cách dùng đóng mở ngoặc `()` hợp lý.

---

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Màn hình console hiển thị rõ ràng thông tin chi tiết hóa đơn: Giá phụ thu, Tạm tính, Tiền giảm giá, Tổng tiền thanh toán và kết quả đánh giá 2 cờ ưu đãi (`True`/`False`).

---

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến đúng chuẩn Python `snake_case`, ghi chú giải thích bằng tiếng Việt có dấu.
    *   Không chứa ký tự emoji trong mã nguồn và câu văn báo cáo.
*   **[5 điểm] Nộp bài GitHub:**
    *   Link repository GitHub hợp lệ, đặt tên thư mục đúng định dạng quy định: `[Tên Lớp]_[Môn Học]_Session04_Ex12`.

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Báo cáo Phân tích Chuyện biệt về Ép kiểu ngầm định:**
    *   Viết đoạn phân tích sâu sắc về cơ chế ép kiểu ngầm định (Implicit Type Conversion) từ `bool` sang `int`/`float` trong Python khi thực hiện các toán tử số học và cảnh báo rủi ro về độ rõ ràng mã nguồn.