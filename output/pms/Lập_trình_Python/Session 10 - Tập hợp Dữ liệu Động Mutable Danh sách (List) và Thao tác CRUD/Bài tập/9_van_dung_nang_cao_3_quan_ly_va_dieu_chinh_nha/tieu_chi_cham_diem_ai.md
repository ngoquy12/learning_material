# **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 3] Quản lý và Điều chỉnh Nhật ký Cước phí Chuyến đi GrabRide — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Xác định đúng kiểu dữ liệu của danh sách cước phí (`list[float]`), chỉ số cập nhật/xóa (`int`), hệ số phụ phí (`float`) và biến tổng thu nhập (`float`).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế sơ đồ luồng Mermaid:** Vẽ đúng sơ đồ luồng Mermaid tuân thủ nghiêm ngặt 5 hình dạng chuẩn (Oval cho Bắt đầu/Kết thúc, Bình hành cho Input/Output, Chữ nhật cho Process cập nhật/xóa/tính toán, Hình thoi cho Decision kiểm tra chỉ số).

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM:** Khởi tạo danh sách cước phí ban đầu chuẩn PEP 8 và có gán Type Hints đầy đủ (ví dụ: `danh_sach_cuoc_phi: list[float] = [...]`).
*   **[15 điểm] Cập nhật và Xóa phần tử List:** Thực hiện cập nhật giá trị đúng chỉ số (`danh_sach_cuoc_phi[index] = new_value`), xóa đúng vị trí bằng `del danh_sach_cuoc_phi[index]` và truy xuất độ dài bằng `len()`.

#### **3. Kiểm chuẩn dữ liệu và Chặn sai sót biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Kiểm soát chỉ số index hợp lệ:** Viết điều kiện kiểm tra chỉ số $0 \le \text{index} < \text{len(danh\_sach)}$ trước khi truy cập hoặc xóa phần tử để ngăn ngừa lỗi `IndexError`.
*   **[15 điểm] Validate dữ liệu đầu vào:** Kiểm tra khoảng cách km hoặc cước phí cập nhật không được âm ($\ge 0.0$).

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Thông điệp cảnh báo rõ ràng:** Xuất thông báo lỗi mô tả đúng bản chất sự cố khi chỉ số `index` vượt quá phạm vi danh sách (ví dụ: `"[LỖI] Chỉ số chuyến đi không tồn tại trong hệ thống!"`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch & Chuẩn PEP 8:** Tên biến bằng tiếng Anh chuẩn snake_case (`trip_fares`, `updated_index`), comment tiếng Việt rõ ràng, thụt lề 4 space.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục yêu cầu (`HNKS25CNTT1_Core_Session_Session 10_Ex9`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý thống kê tối ưu:** Tính toán tổng doanh thu và cước phí trung bình mỗi chuyến đi chỉ bằng vòng lặp duyệt qua danh sách sau khi đã xóa phần tử rác mà không cần khởi tạo danh sách phụ.
