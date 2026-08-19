# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi cập nhật và xóa chuyến đi trong danh sách cước phí GrabRide — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng thực thi bị lệch chỉ số do thứ tự thực hiện lệnh `del` trước khi gán cập nhật phần tử.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác các giá trị tương ứng ở dòng 2 và dòng 3 trong bảng Test Case (Input, Buggy Output, Expected Output, Dòng code gây lỗi, Logic Note).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Sửa thành công mã nguồn sao cho chuyến đi thứ 3 được cập nhật lên 18.000 VNĐ và chuyến đi thứ 2 bị xóa khỏi danh sách đúng theo chỉ số ban đầu.
*   **[20 điểm] Tuân thủ giới hạn kiến thức:** Sử dụng chính xác thao tác gán chỉ số `list[i] = val` và xóa `del list[i]`, tuyệt đối không dùng `def`, `class`, `append()`, `pop()`, `remove()`.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate chỉ số hợp lệ:** Đảm bảo chỉ số thao tác nằm trong phạm vi chiều dài danh sách (`0 <= index < len(list)`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo danh sách không bị rỗng trước khi thực hiện truy cập hoặc xóa phần tử.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn bản chất hiện tượng Index Shift trong danh sách động khi thực hiện thao tác xóa phần tử (`del`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến bằng tiếng Anh chuẩn `snake_case`, comment giải thích bằng tiếng Việt có dấu, tuân thủ PEP 8 và Type Hints (`list[int]`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tối ưu thứ tự thao tác:** Giải thích rõ hai phương án sửa lỗi (Phương án 1: Cập nhật trước rồi xóa sau; Phương án 2: Tính toán lại chỉ số mới sau khi xóa) và chọn phương án tối ưu nhất.
