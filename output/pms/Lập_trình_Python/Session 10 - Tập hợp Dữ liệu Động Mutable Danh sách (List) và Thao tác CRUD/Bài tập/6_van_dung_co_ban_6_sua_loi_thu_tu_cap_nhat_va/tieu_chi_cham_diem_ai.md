### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 6] Sửa lỗi thứ tự cập nhật và xóa chuyến xe GrabRide — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác nguyên nhân dòng lệnh `del danh_sach_cuoc_phi[1]` bị đặt trước dòng cập nhật `danh_sach_cuoc_phi[2] = 45000` dẫn đến sự cố trượt chỉ số (Index Drift).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Điền hoàn chỉnh bảng Test Case (tối thiểu 3 kịch bản kiểm thử) mô tả rõ kết quả sai (Buggy Output) và kết quả kỳ vọng (Expected Output).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Đảo lại thứ tự thực hiện: cập nhật phần tử tại `index 2` lên `45000` trước, sau đó mới gọi câu lệnh `del` xóa phần tử tại `index 1`. Output danh sách đạt `[35000, 45000, 85000, 25000]`.
*   **[20 điểm] Truy xuất độ dài chuẩn xác:** Sử dụng đúng hàm `len(danh_sach_cuoc_phi)` để tính toán tổng số chuyến xe còn lại sau khi đã hoàn tất cả thao tác cập nhật và xóa (`so_luong_con_lai == 4`).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate điều kiện biên chỉ số:** Đảm bảo danh sách kiểm thử có đủ số lượng phần tử tối thiểu (ít nhất 3 phần tử) để tránh truy cập vượt quá chỉ số (`IndexError`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Mã nguồn thực thi độc lập không làm treo chương trình, hiển thị kết quả trực quan trên CLI.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao thao tác xóa (`del`) lại làm thay đổi vị trí index của tất cả phần tử đứng phía sau trong một List động của Python.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết đúng chuẩn PEP 8, sử dụng 4 khoảng trắng để thụt lùi dòng, đặt tên biến `snake_case` minh bạch (`danh_sach_cuoc_phi`, `so_luong_con_lai`) và có Type Hints (`list[int]`).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session10_Ex6`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Phân tích giải pháp thay thế:** Đề xuất phương án 2 (Nếu bắt buộc phải xóa trước thì phải điều chỉnh chỉ số cập nhật từ `index 2` thành `index 1`) và so sánh ưu/nhược điểm về độ rõ ràng mã nguồn của 2 cách làm.