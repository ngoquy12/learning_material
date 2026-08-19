# **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Kiểm tra Luồng Xử lý Phiếu Mượn và Phí Phạt Thư viện — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:** Chỉ ra chính xác hai dòng lệnh cập nhật giá trị `success_count += 1` và `total_fine += 5000` được đặt sai vị trí (nằm trước các câu lệnh `if ... continue` và `if ... break`).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thiện đầy đủ và chính xác dữ liệu 3 Test Case trong bảng báo cáo (STT 1 đã mẫu, STT 2 và STT 3 tính đúng các tham số `Buggy Output` và `Expected Output`).

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** Đẩy các câu lệnh tích lũy `success_count` và `total_fine` xuống sau khối lệnh kiểm tra `continue` và `break`. Kết quả đầu ra khớp 100% với yêu cầu nghiệp vụ (chỉ cộng phí cho phiếu xử lý thành công).
*   **[20 điểm] Điều khiển luồng lặp chính xác:** Sử dụng đúng vòng lặp `for ... in range()` cùng các lệnh `continue`, `break` và khối `else` của vòng lặp để thông báo khi tiến trình chạy không bị ngắt giữa chừng.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate tham số khoảng quét:** Đảm bảo giá trị `start_id` nhỏ hơn `end_id` và phạm vi duyệt `range(start_id, end_id)` chính xác.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Đảm bảo chương trình không bị lỗi gián đoạn hoặc in ra kết quả sai lệch khi gặp mã phiếu rủi ro.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích ngắn gọn tại sao việc đặt câu lệnh thay đổi trạng thái biến trước lệnh `continue` / `break` lại là lỗi lập trình thường gặp phổ biến (side-effect bug) và cách phòng ngừa trong thực tế sản xuất.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tên biến chuẩn `snake_case`, thụt lề 4 dấu cách đúng chuẩn PEP 8, chú thích bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_SessionSession 08_Ex1`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Mở rộng kịch bản kiểm thử:** Viết thêm kịch bản chạy thử với các khoảng `range` khác nhau (ví dụ trường hợp chạy hoàn toàn không có phiếu lỗi để kiểm chứng khối `else` được kích hoạt).
