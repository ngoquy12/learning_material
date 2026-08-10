### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Khắc phục lỗi kiểm chuẩn dữ liệu và xử lý ngoại lệ trong hệ thống CRM — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác các dòng mã nguồn trong `update_spend` thiếu sót về kiểm chuẩn dữ liệu và chưa chủ động kích hoạt ngoại lệ.
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Trình bày đầy đủ bảng Test Case (tối thiểu 03 trường hợp) phân tích rõ Input, Buggy Output hiện tại và Expected Output chính xác.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Cập nhật chính xác `total_spend` và chuyển đổi hạng thành viên `BRONZE`, `SILVER`, `GOLD` tương ứng với doanh số tích lũy mới.
*   **[20 điểm] Xử lý ngoại lệ chuẩn ngôn ngữ:** Kích hoạt chủ động các ngoại lệ `KeyError`, `ValueError`, `TypeError` bằng câu lệnh `raise` kèm thông báo tiếng Việt rõ ràng, đúng ngữ cảnh.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Chặn thành công các trường hợp `amount` không phải là số nguyên (bao gồm việc chặn kiểu `bool`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo hệ thống không bị crash đột ngột khi tra cứu mã khách hàng không hợp lệ mà báo lỗi có kiểm soát.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được tại sao trong các ứng dụng doanh nghiệp (CRM/Fintech) cần chủ động ném ngoại lệ (`raise`) ở tầng xử lý nghiệp vụ thay vì âm thầm trả về giá trị `None` hoặc `False`.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Mã nguồn viết sạch đẹp, đúng chuẩn PEP 8, có Type Hints đầy đủ, sử dụng tên biến/phương thức tiếng Anh chuẩn `snake_case`.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Tạo đúng thư mục `[Tên Lớp]_[Môn Học]_Session14_Ex01` và commit đầy đủ file báo cáo + mã nguồn Python đã sửa.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Unit Test tự động:** Viết file script kiểm thử đơn vị với thư viện `pytest` để kiểm tra tự động các trường hợp `pytest.raises(ValueError)` và `pytest.raises(KeyError)`.