### **Tiêu chí chấm điểm (AI)**
**[Sáng tạo 3] Thiết kế Module Quản lý và Điều chỉnh Cước phí Chuyến đi GrabRide — Tổng điểm: 100 điểm**

#### **1. Tự thiết kế I/O Schema và Kịch bản lỗi thường gặp — 30 điểm**
*   **[15 điểm] Tự thiết kế cấu trúc I/O Schema:** Định nghĩa rõ ràng, đầy đủ kiểu dữ liệu của đầu vào (Input) và đầu ra (Output) phù hợp với nghiệp vụ quản lý cước phí chuyến đi GrabRide.
*   **[15 điểm] Chủ động phát hiện sai sót dữ liệu (Edge Cases):** Liệt kê chính xác tối thiểu 3 kịch bản lỗi thực tế (chỉ số index out of range, giá trị cước phí âm/không hợp lệ, thao tác khi danh sách rỗng, v.v.) và nêu giải pháp xử lý logic.

#### **2. Thiết kế kiến trúc và Sơ đồ luồng dữ liệu — 20 điểm**
*   **[10 điểm] Sơ đồ luồng dữ liệu (Data Flow):** Vẽ sơ đồ Mermaid thể hiện đầy đủ các bước xử lý dữ liệu. Tuân thủ 100% quy chuẩn 5 hình khối (Stadium cho Bắt đầu/Kết thúc, Parallelogram cho I/O, Diamond cho Decision, Rectangle cho Process).
*   **[10 điểm] Thiết kế vòng đời tính năng:** Giải thích rõ ràng sự thay đổi trạng thái của danh sách dữ liệu qua từng bước (khởi tạo -> cập nhật index -> xóa phần tử với `del` -> tính số lượng với `len()`).

#### **3. Hiện thực hóa logic nghiệp vụ sáng tạo — 30 điểm**
*   **[15 điểm] Triển khai thành công logic nghiệp vụ đặc thù:** Tính toán chuẩn xác cước phí GrabRide theo quy tắc 2km đầu, các km tiếp theo và nhân hệ số thời tiết `1.2x` khi cần cập nhật.
*   **[15 điểm] Thao tác List Mutable chính xác:** Thực hiện đúng thao tác cập nhật giá trị qua index (`list[index] = new_value`), xóa phần tử chính xác bằng câu lệnh `del list[index]`, và đếm đúng số phần tử còn lại bằng `len()`.

#### **4. Chặn lỗi biên và Validate dữ liệu — 10 điểm**
*   **[10 điểm] Tự chặn các lỗi biên đã đề xuất:** Viết đầy đủ các cấu trúc điều kiện `if/else` để kiểm tra tính hợp lệ của index và dữ liệu trước khi truy cập hoặc thực thi câu lệnh `del`, tránh gây tràn chỉ số hoặc sập chương trình.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Clean Code & Chuẩn Python 3.12:** Mã nguồn tuân thủ PEP 8, sử dụng Type Hints cho tất cả các biến, tên biến bằng tiếng Anh mang ý nghĩa rõ ràng, comment bằng tiếng Việt có dấu. Không vi phạm phạm vi cấm (không dùng `append`, `pop`, `def`, `class`, `dict`...).
*   **[5 điểm] Quy chuẩn nộp bài GitHub:** Tệp mã nguồn tổ chức sạch sẽ, thông tin commit rõ ràng và tuân thủ đúng tên thư mục theo mẫu quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Triển khai cơ chế Restore / Auditing dữ liệu:** Xây dựng thêm cơ chế sao lưu danh sách cước phí trước khi xóa (bằng cách gán danh sách lưu trữ song song trước thời điểm `del`) hoặc in nhật ký audit trail chi tiết thông số thay đổi cước phí theo đúng phạm vi kiến thức cho phép.