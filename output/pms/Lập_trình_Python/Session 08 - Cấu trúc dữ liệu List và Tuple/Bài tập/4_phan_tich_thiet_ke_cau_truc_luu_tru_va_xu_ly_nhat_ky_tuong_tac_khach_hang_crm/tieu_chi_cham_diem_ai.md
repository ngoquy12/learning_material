### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Thiết kế cấu trúc lưu trữ và xử lý nhật ký tương tác khách hàng CRM — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Phân tích chi tiết Giải pháp A (Sửa List in-place + Pythonic Swap Tuple).
    *   Phân tích chi tiết Giải pháp B (Khởi tạo List mới bằng Slicing + Swap biến trung gian `temp`).
    *   Giải thích rõ cơ chế quản lý bộ nhớ của List (mutable) và Tuple (immutable) trong từng giải pháp.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** 
    *   Tạo bảng so sánh HTML đầy đủ 5 tiêu chí (Độ phức tạp bộ nhớ, Tốc độ execution, Readability, Data Integrity, Phù hợp ngữ cảnh CRM).
    *   Bảng sử dụng đúng thẻ HTML và attribute `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Giải trình thuyết phục tại sao Giải pháp A tối ưu hơn về hiệu năng bộ nhớ khi xử lý List dữ liệu CRM kích thước lớn (tránh tạo bản sao danh sách không cần thiết).
    *   Lý giải tính gọn gàng, an toàn và đúng chuẩn PEP 8 của cú pháp hoán đổi `lat, lng = lng, lat`.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Trình bày đầy đủ các bước thuật toán mã giả từ bước khởi tạo, cập nhật index, trích xuất slice đến giải nén và đảo vị trí Tuple.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Khai báo đúng danh sách `session_log = [5001, 5002, 5003, 5004]` và Tuple `geo_location = (106.66017, 10.76262)`.
    *   Cập nhật thành công phần tử index 0: `session_log[0] = 9999`.
    *   Trích xuất đúng phân đoạn sub-list bằng Slicing: `sub_log = session_log[1:3]`.
    *   Giải nén và Swap thành công tọa độ thành Tuple mới: `lat, lng = geo_location` -> `updated_geo = (lat, lng)`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Không cố tình thực hiện thao tác ghi đè vào Tuple (`geo_location[0] = ...`).
    *   TUYỆT ĐỐI KHÔNG vi phạm các vùng cấm: Không sử dụng vòng lặp (`for`/`while`), không sử dụng các phương thức `append`, `pop`, `remove`, `del`, `insert`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Đầu ra `print()` hiển thị chính xác kết quả danh sách sau cập nhật `[9999, 5002, 5003, 5004]`.
    *   Kết quả phân đoạn sub-list chính xác `[5002, 5003]`.
    *   Tọa độ chuẩn hóa chính xác dạng Tuple `(10.76262, 106.66017)`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến 100% bằng tiếng Anh (`session_log`, `geo_location`, `updated_geo`, `sub_log`).
    *   Ghi chú giải thích bằng Tiếng Việt có dấu. Sử dụng Type Hints chuẩn Python 3.12 (ví dụ: `session_log: list[int]`, `geo_location: tuple[float, float]`).
*   **[5 điểm] Nộp bài GitHub:**
    *   Cung cấp link GitHub repository hợp lệ theo đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session08_Ex04`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script mô phỏng:**
    *   Viết mã so sánh dung lượng bộ nhớ (dùng thư viện `sys.getsizeof`) hoặc chứng minh trực quan sự khác biệt giữa việc tạo mới List bằng Slicing và sửa đổi List In-place.