### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo] Thiết kế Hệ thống Phân bổ và Hiển thị Hồ sơ Khách hàng CRM trên Đa Thiết bị — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản bẫy lỗi — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Tự định nghĩa cấu trúc dữ liệu Request/Response rõ ràng, hợp lý, bao phủ đầy đủ các thuộc tính của thiết bị và hồ sơ khách hàng CRM mà không cần dựa vào template mẫu.
*   **[15 điểm] Chủ động phát hiện bẫy dữ liệu (Edge Cases):** Phát hiện và trình bày giải pháp cụ thể cho tối thiểu 3 trường hợp biên hoặc xung đột trạng thái dữ liệu thực tế.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ đúng cú pháp sơ đồ MermaidJS thể hiện chính xác đường đi của dữ liệu qua các bước xử lý responsive và phân hạng.
*   **[10 điểm] Thiết kế vòng đời tính năng:** Trình bày mạch lạc logic chuyển đổi trạng thái hồ sơ (Active, Archived/Soft Deleted) và cơ chế tính toán layout hiển thị.

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Mã nguồn Python chạy chính xác logic phân loại thiết bị, giới hạn trang và phân hạng hồ sơ theo đúng thiết kế đã đề xuất.
*   **[15 điểm] Xử lý lọc dữ liệu nâng cao:** Triển khai cơ chế lọc bỏ chính xác các bản ghi bị Soft Delete khỏi kết quả hiển thị mặc định nhưng vẫn giữ nguyên toàn vẹn dữ liệu gốc.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết đầy đủ mã kiểm tra (validation guard) và `raise` ngoại lệ cụ thể (`ValueError`, `KeyError`) đi kèm thông điệp mô tả lỗi bằng tiếng Việt khi dữ liệu đầu vào không hợp lệ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Hướng đối tượng:** Đạt 100% quy chuẩn PEP 8, bắt buộc có Type Hints (`int | str`), định danh hoàn toàn bằng tiếng Anh, ghi chú giải thích logic bằng Tiếng Việt có dấu.
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tạo đúng tên thư mục theo quy định `[Tên Lớp]_[Môn Học]_Session01_Ex05`, commit mã nguồn đầy đủ và có file `README.md` hướng dẫn chạy chương trình.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Bổ sung module ghi vết lịch sử thay đổi trạng thái Lead (Audit Log) hoặc chức năng khôi phục (Restore) cho các bản ghi đã xóa mềm.