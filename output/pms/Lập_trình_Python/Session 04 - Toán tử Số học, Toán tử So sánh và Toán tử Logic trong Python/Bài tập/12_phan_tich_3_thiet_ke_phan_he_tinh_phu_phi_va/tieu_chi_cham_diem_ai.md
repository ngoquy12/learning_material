# **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Thiết Kế Phân Hệ Tính Phụ Phí Và Phê Duyệt Hoàn Tiền Đặt Phòng Khách Sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Đề xuất được ít nhất 2 phương án kỹ thuật tính toán phụ phí và cờ hoàn tiền độc lập.
    *   Cả 2 phương án phải tuân thủ nghiêm ngặt việc KHÔNG dùng `if/else`, KHÔNG dùng `and/or/not` (Ví dụ: Phương án 1 sử dụng trực tiếp tính chất Ép kiểu tự động của Boolean trong phép nhân số học `(check_in_hour < 12) * (nightly_rate * 0.3)`; Phương án 2 sử dụng phép chia lấy phần nguyên / công thức số học đại số).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Tạo bảng HTML/Markdown so sánh đầy đủ 5 tiêu chí: Tốc độ thực thi, Bộ nhớ, Khả năng bảo trì, Độ đọc hiểu mã nguồn, Ngữ cảnh áp dụng.
    *   Bảng HTML có thuộc tính CSS `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Giải trình thuyết phục lý do chọn phương án tối ưu dựa trên độ ngắn gọn, tính chuẩn hóa của Pythonic code và tốc độ xử lý CPU instructions.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ Mermaid Flowchart chính xác 100% quy chuẩn 5 hình dạng chuẩn: Oval cho Terminator, Hình bình hành `[/ /]` cho Input/Output, Hình chữ nhật `[" "]` cho Process tính toán số học, Hình thoi cho Decision check điều kiện số học.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Viết code Python 3.12 thực thi chính xác các công thức tính toán: `base_room_cost`, `early_surcharge`, `guest_surcharge`, `total_payment`, `is_full_refund_approved`.
    *   Sử dụng đúng Type Hints cho toàn bộ biến khai báo (e.g., `nightly_rate: float`, `num_nights: int`).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Logic xử lý đúng các trường hợp biên: `check_in_hour = 12` (không phụ thu), `guest_age = 6` (tính phụ thu), `cancellation_days = 3` (được hoàn tiền cọc).
    *   Tuyệt đối không vi phạm phạm vi kiến thức (Không chứa từ khóa `if`, `else`, `and`, `or`, `not`, `for`, `while`).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Chương trình in ra màn hình CLI kết quả tính toán chi tiết, minh bạch từng khoản phụ thu và tổng số tiền thanh toán dưới dạng số thực/số nguyên chuẩn định dạng.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Biến đặt tên tiếng Anh chuẩn danh định `snake_case` (e.g., `is_early_check_in`, `has_extra_guest_fee`). Chú thích code giải thích bằng tiếng Việt có dấu chuẩn sản xuất.
*   **[5 điểm] Nộp bài GitHub:**
    *   Cung cấp link GitHub repository hợp lệ theo cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session04_Ex12`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Tự viết thêm script benchmark đo thời gian thực thi (dùng module `time`) để so sánh hiệu năng chạy 1.000.000 phép tính giữa 2 phương án xử lý logic.
