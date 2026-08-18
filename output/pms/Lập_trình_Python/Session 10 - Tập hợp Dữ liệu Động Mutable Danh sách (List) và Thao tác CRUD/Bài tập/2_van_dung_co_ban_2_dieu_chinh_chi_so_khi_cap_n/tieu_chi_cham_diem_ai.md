### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Điều chỉnh chỉ số khi cập nhật và xóa chuyến đi trong Hệ thống GrabRide — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác lỗi nằm ở thứ tự thực hiện lệnh `del` gây ra hiện tượng dịch chuyển chỉ số (index shift) trước khi gán `trip_distances[2] = 5.5`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền đầy đủ và chính xác dữ liệu 2 trường hợp Test Case còn lại trong bảng HTML (Input, Buggy Output, Expected Output và giải thích nguyên nhân).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Điều chỉnh lại thứ tự thao tác (cập nhật trước khi xóa, hoặc tính toán lại chỉ số sau khi xóa) để danh sách cuối cùng đúng giá trị `[4.0, 5.5, 8.2, 0.5]`.
*   **[20 điểm] Sử dụng chính xác cú pháp danh sách được phép:** Áp dụng đúng cú pháp cập nhật theo index `list[i] = val`, xóa phần tử bằng `del list[i]` và đếm bằng `len()`. Không vi phạm phạm vi kiến thức cấm.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Bảo toàn định dạng dữ liệu:** Đảm bảo kiểu dữ liệu trong danh sách là `float` cho quãng đường và `int` cho số lượng chuyến đi.
*   **[10 điểm] Kiểm tra biên danh sách:** Đảm bảo chỉ số truy cập nằm trong phạm vi hợp lệ của danh sách (`0 <= index < len(list)`).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được tác động của các câu lệnh làm thay đổi kích thước/thứ tự danh sách (như `del`) đối với các chỉ số phía sau trong bộ nhớ Python.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết theo đúng chuẩn PEP 8, biến đặt tên tiếng Anh dạng `snake_case`, chú thích làm rõ logic bằng tiếng Việt có dấu.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session10_Ex2`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Giải pháp tối ưu:** Trình bày 2 cách sửa lỗi khác nhau (Cách 1: Đổi thứ tự thực hiện; Cách 2: Điều chỉnh chỉ số index sau khi xóa) và phân tích ưu/nhược điểm của từng cách.