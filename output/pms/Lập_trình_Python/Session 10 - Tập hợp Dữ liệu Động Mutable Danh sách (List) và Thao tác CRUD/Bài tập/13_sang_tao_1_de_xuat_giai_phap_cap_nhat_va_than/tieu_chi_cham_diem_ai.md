### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 1] Đề xuất Giải pháp Cập nhật và Thanh lọc Dữ liệu Chuyến đi GrabRide — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản lỗi thường gặp — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Khai báo và mô tả rõ ràng kiểu dữ liệu của danh sách chuyến đi `trip_fares` (`list[int]`), các biến chứa chỉ số và giá trị cước mới, cùng kết quả đầu ra dự kiến.
*   **[15 điểm] Chủ động phát hiện sai sót dữ liệu (Edge Cases):** Phân tích chính xác ít nhất 3 kịch bản lỗi biên thực tế (như chỉ số `target_update_index` hoặc `target_delete_index` nằm ngoài khoảng `0` đến `len(trip_fares) - 1`, danh sách rỗng, hoặc sự thay đổi chỉ số của các phần tử đứng sau khi xóa bằng `del`).

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid chính xác, hiển thị rõ luồng dữ liệu từ khi khởi tạo, qua các bước kiểm tra điều kiện chỉ số, cập nhật phần tử, xóa phần tử đến khi tính độ dài còn lại. Sử dụng đúng 5 dạng hình tiêu chuẩn (Oval, Parallelogram, Diamond, Rectangle, Flowline).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày logic rõ ràng về việc thay đổi trạng thái của danh sách động Mutable trong bộ nhớ sau từng thao tác gán `[index]` và xóa `del`.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Thực hiện đúng thao tác cập nhật cước phí chuyến đi bị sai bằng cú pháp `trip_fares[i] = val` và xóa chuyến đi bị hủy bằng từ khóa `del trip_fares[i]`. TUYỆT ĐỐI KHÔNG dùng các phương thức bị cấm như `append()`, `pop()`, `remove()`, hoặc hàm `def`.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Tính toán chính xác số lượng chuyến đi thực tế còn lại sau khi thanh lọc bằng hàm `len(trip_fares)` và in ra báo cáo rõ ràng.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết mã nguồn chứa các câu lệnh kiểm tra điều kiện `if 0 <= target_index < len(trip_fares):` trước khi can thiệp vào danh sách, có thông báo lỗi mô tả rõ ràng nếu chỉ số không hợp lệ để ngăn ngừa ném lỗi `IndexError`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn Python:** Mã nguồn tuân thủ PEP 8, thụt lề 4 dấu cách, đặt tên biến 100% bằng Tiếng Anh theo chuẩn `snake_case`, sử dụng Type Hints đầy đủ (`list[int]`, `int`), chú thích logic bằng Tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Cấu trúc thư mục nộp bài chuẩn xác theo định dạng `[Tên Lớp]_[Môn Học]_Session10_Ex13`, có tệp `main.py` hoàn chỉnh và tệp báo cáo/phân tích đính kèm.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Auditing / Lưu vết dữ liệu:** Tự thiết kế thêm biến lưu trữ doanh thu ban đầu hoặc ghi nhận độ chênh lệch tổng tiền cước trước và sau khi cập nhật/xóa dữ liệu mà chỉ dùng các kiến thức đã học.