### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân tích logic tính tiền hóa đơn và kiểm tra điều kiện tặng voucher tại Highlands POS — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Đề xuất Giải pháp A (vd: Dùng biểu thức toán tử so sánh nhân với hệ số giá trị: `(size_code == 1) * 6000 + (size_code == 2) * 10000`).
    *   Đề xuất Giải pháp B (vd: Tách riêng các biến Boolean trung gian để thực hiện nhân logic số học từng bước).
    *   Phân tích rõ sự khác biệt về mặt cấu trúc tính toán giữa 2 phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng HTML đúng định dạng chứa đầy đủ 5 tiêu chí: Tốc độ thực thi, Bộ nhớ, Khả năng bảo trì, Độ dễ đọc, Mức độ phù hợp.
    *   Có nhận xét phân tích phản biện sâu sắc, không chép lại lý thuyết suông.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lập luận thuyết phục lý do chọn phương án tối ưu (ví dụ chọn phương án tách biến trung gian để tối ưu độ dễ đọc và dễ bảo trì trong môi trường làm việc nhóm).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu (Mermaid):**
    *   Sử dụng đúng 100% chuẩn Mermaid 5 hình dạng: Oval `([ ])` cho Start/End, Parallelogram `[/ /]` cho Input/Output, Rectangle `[" "]` cho Process, Diamond cho Decision.
    *   Tuyệt đối KHÔNG dùng Parallelogram cho các bước tính toán toán tử.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code Python:**
    *   Viết code chạy đúng, tính toán chính xác tổng tiền phụ thu size, phụ thu topping, tiền giảm giá và tổng tiền thanh toán cuối cùng.
    *   Tính chính xác giá trị Boolean `is_eligible_voucher` bằng kết hợp toán tử so sánh và toán tử logic (`and`, `or`).
*   **[15 điểm] Tuân thủ phạm vi kiến thức & Chặn lỗi logic biên:**
    *   TUYỆT ĐỐI KHÔNG sử dụng `if/else/elif`, `for/while`, `list`, `dict`, `def`, `class`. (Nếu vi phạm trừ toàn bộ 15 điểm mục này).
    *   Xử lý chính xác dữ liệu biên: `size_code = 0` (Size S không bị phụ thu), `topping_count = 0`, ép kiểu dữ liệu `input()` đầu vào chính xác (`int`, `float`).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   In rõ ràng các thông tin theo từng dòng: Tổng tiền tạm tính, Số tiền giảm giá, Tổng thanh toán, Trạng thái nhận Voucher (`True`/`False`).
    *   Định dạng số tiền hiển thị rõ ràng, không bị lỗi làm tròn số thực kỳ quặc.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Biến số bằng tiếng Anh chuẩn PEP 8 (như `base_price`, `size_extra`, `topping_extra`, `subtotal`, `discount_amount`, `final_total`, `is_eligible_voucher`).
    *   Chú thích mã nguồn bằng tiếng Việt có dấu, giải thích rõ các phép tính số học Boolean.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn repository GitHub hợp lệ, đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_SessionSession 04_Ex10`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Kịch bản kiểm thử độc lập (Test Suite Manual):**
    *   Viết thêm bộ dữ liệu mẫu gồm 3-4 kịch bản test case đầu vào (ví dụ: Đơn Size L, 4 topping, Khách Vàng vs Đơn Size S, 0 topping, Khách Thường) kèm giá trị đầu ra mong đợi (Expected Output) để tự kiểm chứng mã nguồn.