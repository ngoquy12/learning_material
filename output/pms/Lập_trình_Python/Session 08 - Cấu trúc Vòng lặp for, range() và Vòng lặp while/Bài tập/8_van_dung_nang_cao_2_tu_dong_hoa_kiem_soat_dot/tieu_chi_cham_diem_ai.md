### **Tiêu chí chấm điểm (AI)**
**[Vận dụng nâng cao 2] Tự động hóa kiểm soát đợt mượn sách bằng luồng vòng lặp — Tổng điểm: 100 điểm**

#### **1. Báo cáo Phân tích I/O & Đề xuất giải pháp — 20 điểm**
*   **[10 điểm] Phân tích I/O chi tiết:** Đơn định rõ ràng tên biến, kiểu dữ liệu (`int`, `str`, `float`), phạm vi sử dụng của dữ liệu đầu vào (ví dụ: `start_id`, `end_id`, `overdue_days`) và dữ liệu đầu ra (ví dụ: `total_fine`, thông điệp cảnh báo).
*   **[10 điểm] Tự đề xuất giải pháp & Thiết kế các bước:** Vẽ sơ đồ luồng Mermaid đầy đủ, chính xác chuẩn 5 hình dạng (Oval, Parallelogram, Diamond, Rectangle, Flowline). Giải thích logic điều khiển luồng với `break`, `continue`, `else` mạch lạc, đúng bản chất ngôn ngữ.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Cấu trúc vòng lặp:** Sử dụng chính xác vòng lặp `for record_id in range(start_id, end_id + 1)` để duyệt đúng phạm vi bản ghi được yêu cầu. Khởi tạo biến tích lũy tổng tiền phạt chính xác.
*   **[15 điểm] Xử lý rẽ nhánh nghiệp vụ & Điều khiển luồng:**
    *   Sử dụng đúng `continue` để bỏ qua bản ghi lỗi nhẹ (mã chia hết cho 5) trước khi nhập dữ liệu hoặc tính toán.
    *   Sử dụng đúng `break` để thoát vòng lặp lập tức khi phát hiện mã vi phạm an ninh (mã chia hết cho 13).
    *   Tính chính xác tiền phạt mượn quá hạn (5.000 VNĐ/ngày khi `overdue_days > 0`) cho bản ghi hợp lệ.

#### **3. Kiểm chuẩn dữ liệu và Chặn sai sót biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Vận dụng chính xác khối `else` của vòng lặp `for`:** Khối `else` chỉ chạy khi vòng lặp duyệt hết toàn bộ phạm vi mà không chạm phải lệnh `break`. In báo cáo tổng kết thành công chính xác trong khối `else`.
*   **[15 điểm] Tuân thủ triệt để pham vi kiến thức:** 
    *   Không sử dụng vòng lặp `while`.
    *   Không khai báo hàm (`def`), không tạo `class`, không sử dụng `list`, `dict`, `tuple`, `set`.
    *   Xử lý đúng biên dữ liệu khi `end_id < start_id` hoặc khi `overdue_days <= 0`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Thông báo xuất ra màn hình CLI rõ ràng, phân biệt được thông báo Bỏ qua (Skip/Continue), Thông báo Cảnh báo dừng khẩn cấp (Emergency Break), và Thông báo hoàn thành an toàn (Else Success).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Tên biến bằng tiếng Anh theo chuẩn `snake_case`, chú thích mã nguồn bằng tiếng Việt chuẩn xác, rõ ràng, không chứa emoji.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc cây thư mục yêu cầu (`[Tên Lớp]_[Môn Học]_SessionSession 08_Ex8`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Phân tích & Tối ưu logic kiểm soát:** Phân tích chi tiết trường hợp thứ tự kiểm tra điều kiện `break` và `continue` để tránh sai sót logic khi một mã thỏa mãn đồng thời hai điều kiện (nếu có), viết mã giải thích dễ hiểu trong báo cáo.