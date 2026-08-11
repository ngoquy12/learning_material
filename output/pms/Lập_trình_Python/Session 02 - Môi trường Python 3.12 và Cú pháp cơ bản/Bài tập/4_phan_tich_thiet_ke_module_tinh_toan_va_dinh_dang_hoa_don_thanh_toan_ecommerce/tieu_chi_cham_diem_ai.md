### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Thiết kế module tính toán và định dạng hóa đơn thanh toán E-Commerce — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Mô tả chi tiết bản chất kỹ thuật của Giải pháp A (Staged Variable Casting) và Giải pháp B (Inline Direct Evaluation) trong ngữ cảnh nhập xuất console và ép kiểu dữ liệu Python.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Hoàn thiện bảng so sánh đầy đủ 5 tiêu chí (Bộ nhớ, Tính dễ đọc, Bảo trì, Kiểm vết lỗi, Độ an toàn tài chính) theo định dạng bảng HTML có thuộc tính CSS `style` bắt buộc.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Trình bày lý do kỹ thuật thuyết phục cho việc chọn giải pháp tối ưu (ưu tiên tính rõ ràng, dễ bảo trì và kiểm soát lỗi dữ liệu số học trong ngành E-Commerce).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày mã giả (Pseudocode) rõ ràng, thể hiện chính xác thứ tự nhận dữ liệu chuỗi, ép kiểu sang `float`/`int`, tính toán tạm tính và tổng chi phí.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết hoàn chỉnh chương trình Python 3.12 thực hiện đúng bài toán tính hóa đơn E-Commerce từ dữ liệu nhập bàn phím.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Ép kiểu chính xác (`float` cho đơn giá/phí ship/voucher, `int` cho số lượng), tuyệt đối không để xảy ra lỗi ghép chuỗi tài chính (ví dụ cộng chuỗi `"15000" + "5000"` thành `"150005000"`).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** Sử dụng đúng tham số `sep=" - "` cho dòng tiêu đề và tham số `end=" VNĐ\n"` (hoặc định dạng kết thúc tương đương) cho dòng kết xuất tổng tiền theo đúng yêu cầu nghiệp vụ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến bằng tiếng Anh chuẩn `snake_case` (ví dụ `unit_price`, `quantity`, `shipping_fee`), mã nguồn có ghi chú giải thích logic bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** Đường dẫn repository GitHub hợp lệ, đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session02_Ex04`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Phân tích bộ dữ liệu kiểm thử (Test Cases Report):** Xây dựng báo cáo kiểm thử chi tiết minh họa kết quả chạy của chương trình với ít nhất 3 bộ dữ liệu đầu vào khác nhau (bao gồm trường hợp số tiền lẻ, số lượng lớn và voucher vượt phí vận chuyển).