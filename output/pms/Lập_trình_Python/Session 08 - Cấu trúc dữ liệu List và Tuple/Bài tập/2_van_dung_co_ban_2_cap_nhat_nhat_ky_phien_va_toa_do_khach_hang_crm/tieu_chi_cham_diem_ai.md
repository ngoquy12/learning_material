### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Cập nhật nhật ký phiên và tọa độ khách hàng CRM — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Giải thích rõ ràng nguyên nhân tính bất biến (Immutability) của Tuple khiến thao tác gán `geo_location[0] = ...` gây lỗi `TypeError`.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Cung cấp bảng báo cáo Test Case đầy đủ tối thiểu 3 kịch bản kiểm thử (Input, Buggy Output, Expected Output) đúng định dạng HTML/Markdown.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Thao tác List & Tuple chuẩn:** Cập nhật thành công phần tử `index 0`, cắt lát Slicing `[1:3]` chính xác, giải nén Tuple Unpacking và hoán đổi Swap `lat, lng = lng, lat` không dùng biến trung gian.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Ném ngoại lệ `ValueError` với thông điệp rõ ràng khi dữ liệu đầu vào không thỏa mãn quy tắc nghiệp vụ.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Kiểm tra chính xác kiểu dữ liệu và điều kiện `new_session_id > 0`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kiểm tra độ dài `len(session_logs) >= 4` trước khi thực hiện truy cập index và slicing để tránh lỗi chỉ số.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Trả lời câu hỏi lý thuyết:** Trình bày được ưu điểm về mặt hiệu năng và tính an toàn dữ liệu của `Tuple` so với `List` trong các bài toán lưu trữ dữ liệu hằng số (như tọa độ địa lý, cấu hình hệ thống).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến/hàm chuẩn `snake_case` bằng tiếng Anh, có chú thích code bằng Tiếng Việt có dấu, tuân thủ chuẩn PEP 8 và Python 3.12 Type Hints.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session08_Ex02`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết đoạn mã kiểm thử tự động:** Viết khối lệnh kiểm thử `try...except` chạy thử nghiệm cả 3 kịch bản Test Case và in ra báo cáo kết quả đẹp mắt trên màn hình CLI.