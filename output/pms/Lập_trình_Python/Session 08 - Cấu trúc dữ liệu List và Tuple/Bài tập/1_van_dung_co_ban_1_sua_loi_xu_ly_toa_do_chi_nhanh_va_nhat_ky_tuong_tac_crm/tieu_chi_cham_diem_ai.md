### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi xử lý tọa độ chi nhánh và nhật ký tương tác CRM — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra đúng dòng mã nguồn gây ra lỗi sụp đổ ứng dụng `TypeError` khi ghi đè Tuple và các dòng mã dùng sai Index / Slicing trong danh sách `List`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp đầy đủ bảng phân tích tối thiểu 3 Test Cases đúng cấu trúc (Mã TC, Mô tả đầu vào, Buggy Output, Expected Output) và áp dụng chuẩn HTML table styling theo quy định.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    *   Ghi đè đúng vị trí Index `0` của `recent_logs` thành `9001`.
    *   Thực hiện Slicing đúng phạm vi `[1:3]` để trích xuất 2 phần tử nhật ký trung gian.
    *   Tạo thành công Tuple mới `updated_geo` chứa tọa độ đã hoán đổi.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Loại bỏ hoàn toàn thao tác gán trực tiếp phần tử Tuple, tôn trọng tính bất biến của Tuple và ngăn chặn ngoại lệ `TypeError` khi thực thi.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Sử dụng kỹ thuật Tuple Unpacking và Swap chuẩn:** Giải nén biến `latitude, longitude = branch_geo` và hoán đổi trực tiếp `latitude, longitude = longitude, latitude` đúng cú pháp Python.
*   **[10 điểm] Không dùng biến trung gian:** Loại bỏ hoàn toàn việc khai báo biến phụ `temp` gây lãng phí bộ nhớ và tiềm ẩn nguy cơ sai lệch dữ liệu.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn (qua comment trong code hoặc file báo cáo) lý do tại sao hệ thống lại chọn lưu tọa độ GPS bằng `Tuple` thay vì `List` trong các ứng dụng doanh nghiệp CRM thực tế (Tính an toàn dữ liệu, phòng ngừa lỗi vô tình ghi đè tọa độ cố định).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến bằng tiếng Anh chuẩn snake_case (`recent_logs`, `branch_geo`, `updated_geo`), comment giải thích logic bằng Tiếng Việt có dấu chuẩn sản xuất, thụt lề 4 dấu cách theo chuẩn PEP 8.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub repository theo đúng cấu trúc tên thư mục quy định (`[Tên Lớp]_[Môn Học]_Session08_Ex01`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết kiểm thử tự động cơ bản:** Khai báo hàm kiểm tra dữ liệu đầu ra tự động bằng câu lệnh assertion đơn giản (`assert updated_geo == (106.66017, 10.76262)` và `assert recent_logs[0] == 9001`) để đảm bảo tính toàn vẹn của mã nguồn sau khi sửa.