### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Xây dựng Module Quản lý Lead CRM và Bộ Kiểm thử Pytest — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Báo cáo liệt kê đầy đủ kiểu dữ liệu input/output, mô tả rõ danh mục dữ liệu đầu vào và đầu ra của từng phương thức kiểm chuẩn và lưu trữ.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Vẽ sơ đồ khối (Flowchart) hoặc viết mã giả (Pseudocode) thể hiện chính xác thứ tự kiểm tra: Kiểm tra định dạng -> Kiểm tra trùng lặp -> Kiểm tra khoảng điểm -> Phân hạng -> Lưu bộ nhớ.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Thiết kế đúng cây hệ thống Exception (`CRMBaseException`, `InvalidLeadDataError`, `LeadScoreOutOfRangeError`, `DuplicateLeadError`) kế thừa đúng từ `Exception`.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Triển khai hàm đăng ký Lead và hàm tự động phân hạng (`BRONZE`, `SILVER`, `GOLD`, `PLATINUM`) chính xác theo từng mốc điểm.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu trùng lặp / Vượt ngưỡng:** Bắt chính xác lỗi trùng lặp Email/Mã số thuế trong bộ nhớ RAM và kích hoạt `DuplicateLeadError`; kiểm tra đúng biên điểm `score` (< 0 hoặc > 100) để ném `LeadScoreOutOfRangeError`.
*   **[15 điểm] Validate dữ liệu đầu vào nâng cao:** Kiểm tra chính xác định dạng Email (`@`, tên miền `.com`/`.vn`), định dạng Số điện thoại (10 chữ số, bắt đầu bằng `0`), và Mã số thuế (10-13 chữ số số học nếu khác `None`). Ném `InvalidLeadDataError` kèm thông điệp rõ ràng.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Sử dụng khối lệnh `try-except-else-finally` chuẩn xác trong module chính. Viết đầy đủ bộ test trong `test_crm_system.py` sử dụng `pytest.fixture` và `pytest.raises` bắt thành công tất cả ngoại lệ tùy chỉnh.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tuân thủ PEP 8, đặt tên biến/hàm/lớp chuẩn Tiếng Anh, sử dụng Type Hints chuẩn Python 3.12 (`str | None`), không dùng mã khung (Skeleton Code).
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session14_Ex03`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Sử dụng `@pytest.mark.parametrize` trong Pytest để kiểm thử hàng loạt các dữ liệu đầu vào sai quy chuẩn một cách gọn gàng và tối ưu bộ nhớ.