### **Tiêu chí chấm điểm (AI)**
**[Sửa lỗi tính toán sức chứa kệ hàng trong kho] — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:**
    *   Chỉ ra cụ thể lỗi chuyển đổi diện tích pallet từ cm2 sang m2 ở dòng tính `dien_tich_pallet` (lỗi chia cho 100 thay vì chia cho 10000). (7.5 điểm)
    *   Chỉ ra lỗi phép toán hiệu số bị ngược ở dòng tính `dien_tich_con_trong` (chiếm dụng trừ đi ban đầu thay vì ban đầu trừ đi chiếm dụng). (7.5 điểm)
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:**
    *   Hoàn thành chính xác 3 test cases yêu cầu với đầy đủ dữ liệu thử nghiệm, chỉ rõ giá trị Output lỗi thực tế và Output mong muốn tương ứng. (15 điểm)

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Sửa đổi công thức toán học và đơn vị:**
    *   Quy đổi đúng diện tích từ centimet vuông (cm2) sang mét vuông (m2): diện tích pallet = (dài_pallet * rộng_pallet) / 10000 (hoặc quy đổi từng chiều dài, rộng sang mét trước khi nhân). (10 điểm)
    *   Chỉnh sửa đúng chiều của biểu thức trừ: `dien_tich_con_trong = dien_tich_ke - tong_dien_tich_chiem_dung`. (10 điểm)
*   **[20 điểm] Sử dụng f-string định dạng hiển thị:**
    *   Định dạng chuẩn xác hai chữ số thập phân cho tất cả các thông số đầu ra bằng cú pháp `{gia_tri:.2f}` trong f-string. (20 điểm)

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Ép kiểu dữ liệu an toàn:**
    *   Ép kiểu đúng các tham số đầu vào kích thước sang kiểu số thực (`float()`) và số lượng pallet sang kiểu số nguyên (`int()`). (10 điểm)
*   **[10 điểm] Phân tích kịch bản dữ liệu dị biệt:**
    *   Trong báo cáo, học viên giải thích được hiện tượng crash chương trình (ValueError) khi người dùng nhập chuỗi ký tự không thể ép kiểu sang số và đề xuất được hạn chế của chương trình ở Session 01 khi chưa học các kỹ thuật xử lý ngoại lệ nâng cao. (10 điểm)

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Giải thích nguyên nhân thực tế:**
    *   Trả lời được câu hỏi thảo luận: Tại sao việc nhầm lẫn đơn vị đo lường (m và cm) thường xuyên xảy ra trong phát triển phần mềm nghiệp vụ (ví dụ: do thiếu sự thống nhất tài liệu nghiệp vụ, thiếu kiểm chuẩn đơn vị) và các biện pháp giảm thiểu lỗi này (ví dụ: đặt tên biến có kèm hậu tố đơn vị đo như `chieu_dai_m`, `chieu_dai_cm`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:**
    *   Viết code sạch sẽ, thụt lề chuẩn PEP 8. Tên biến trực quan và có chú thích rõ ràng bằng tiếng Việt không chứa emoji. (5 điểm)
*   **[5 điểm] Tuân thủ nộp bài GitHub:**
    *   Nộp link và cấu trúc cây thư mục GitHub đúng định dạng `[Tên Lớp]_[Môn Học]_Session01_Ex02`. (5 điểm)

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Đề xuất cải tiến giao diện CLI:**
    *   Tự thiết kế giao diện hiển thị CLI rõ ràng hơn bằng cách sử dụng các dòng phân cách, hiển thị rõ ràng đơn vị đo lường (m, cm, m2) ở từng dòng kết quả để người dùng kho không bị nhầm lẫn. (10 điểm)