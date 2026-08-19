# **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Tối ưu hóa quy trình cập nhật cước phí và xóa chuyến xe GrabRide — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Nêu rõ cơ chế thực hiện của ít nhất 2 phương án kỹ thuật xử lý bài toán (ví dụ: Phương án 1 - Xóa phần tử trực tiếp bằng từ khóa `del` và ghi đè trực tiếp qua index; Phương án 2 - Gán giá trị cờ đánh dấu tạm thời tại index cần xóa rồi thực hiện tạo danh sách lọc mới thông qua vòng lặp duyệt index).
    *   Chỉ rõ sự khác biệt về cách thức quản lý vùng nhớ và chỉ số index của danh sách trong từng phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng so sánh HTML chứa đầy đủ thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.
    *   Đánh giá đầy đủ 5 tiêu chí: Tốc độ thực thi, Dung lượng bộ nhớ, Khả năng bảo trì (Maintainability), Độ rõ ràng (Readability), Kịch bản áp dụng phù hợp.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Lý giải nguyên nhân lựa chọn phương án tối ưu dựa trên điều kiện tài nguyên phần cứng giới hạn của thiết bị nhúng GrabRide (tối ưu số lần duyệt bộ nhớ, thao tác in-place).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ sơ đồ luồng Mermaid đầy đủ, chính xác.
    *   Sử dụng đúng 100% hình dạng Mermaid theo quy chuẩn: Oval `([ ])` cho Start/End, Parallelogram `[/ /]` cho Input/Output, Diamond `?` cho Decision, Rectangle `[" "]` cho Process. Không dùng Parallelogram cho các câu lệnh gán hay tính toán.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Viết mã Python 3.12 thực hiện chính xác các thao tác: khởi tạo `trip_fares: list[int]`, cập nhật giá trị `trip_fares[2] = 54000`, xóa phần tử bằng `del trip_fares[1]`, kiểm tra độ dài bằng `len(trip_fares)`.
    *   Tuân thủ nghiêm ngặt giới hạn kiến thức (KHÔNG dùng `append()`, `pop()`, `def`, `class`, `dict`, `set`, `tuple`).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Giải thích hoặc thể hiện logic kiểm tra phạm vi chỉ số `0 <= index < len(trip_fares)` trước khi thao tác truy xuất/xóa để tránh lỗi `IndexError`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Đầu ra màn hình hiển thị rõ ràng danh sách sau khi thao tác và số lượng chuyến xe còn lại đúng với dữ liệu mẫu (ví dụ: Danh sách còn 4 phần tử, các phần tử bị dịch chuyển chỉ số chính xác sau khi `del`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến bằng Tiếng Anh chuẩn snake_case (ví dụ: `trip_fares`, `remaining_trips`, `updated_fare`).
    *   Có ghi chú mã nguồn bằng Tiếng Việt có dấu đầy đủ, chuẩn PEP 8.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn repository GitHub hợp lệ, đúng cấu trúc thư mục `[Tên Lớp]_[Môn Học]_Session10_Ex10`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Viết đoạn mã đo lường thời gian thực thi (sử dụng thư viện chuẩn `time`) để so sánh hiệu năng giữa phương án gán cờ lọc và phương án xóa trực tiếp bằng `del` trên một danh sách kích thước lớn.
