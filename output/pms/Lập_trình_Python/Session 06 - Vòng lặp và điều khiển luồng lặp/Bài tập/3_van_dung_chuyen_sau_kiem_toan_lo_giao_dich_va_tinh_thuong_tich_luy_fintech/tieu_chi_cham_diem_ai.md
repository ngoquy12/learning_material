### **Tiêu chí chấm điểm (AI)**
**[Vận dụng chuyên sâu] Kiểm Toán Lô Giao Dịch Và Tính Thưởng Tích Lũy Fintech — Tổng điểm: 100 điểm**

#### **1. Báo cáo phân tích và Thiết kế giải pháp — 20 điểm**
*   **[10 điểm] Xác định cấu trúc I/O:** Mô tả đầy đủ kiểu dữ liệu danh sách `list[dict[str, str | float]]` cho Input và `dict[str, int | float]` cho Output với đầy đủ diễn giải ý nghĩa từng thuộc tính.
*   **[10 điểm] Mô tả giải thuật xử lý nghiệp vụ:** Viết mã giả (Pseudocode) hoặc lưu đồ mô tả logic duyệt lặp `for`, điều kiện lọc bằng `continue`, logic phân tầng cashback và kiểm tra ngưỡng ngoại lệ trước khi cập nhật trạng thái.

#### **2. Lập trình logic nghiệp vụ cốt lõi — 30 điểm**
*   **[15 điểm] Khởi tạo dữ liệu RAM và Schema:** Khai báo cấu trúc hàm có Type Hints chuẩn Python 3.10+ (vd: `list[dict[str, str | float]]`), khởi tạo chính xác các biến tích lũy tổng số lượng, tổng tiền và tiền thưởng.
*   **[15 điểm] Hàm/Module xử lý nghiệp vụ tích hợp:** Triển khai chính xác vòng lặp `for` duyệt qua từng giao dịch, sử dụng đúng câu lệnh `continue` để bỏ qua giao dịch có `amount <= 0` hoặc `status != "SUCCESS"`.

#### **3. Kiểm chuẩn dữ liệu và Chặn bẫy biên (Edge Cases) — 30 điểm**
*   **[15 điểm] Chặn bẫy dữ liệu vượt ngưỡng & Phân tầng chuẩn:** Tính đúng các mức cashback Bronze (1%), Silver (2%), Gold (3%) và áp dụng đúng trần cashback tối đa 300,000 VNĐ cho từng giao dịch hạng Gold.
*   **[15 điểm] Tuân thủ ràng buộc kỹ thuật:** Tuyệt đối không sử dụng vòng lặp `while` và câu lệnh `break`. Mã nguồn hoạt động chính xác dựa trên sự phối hợp giữa `for` và `continue`.

#### **4. Xử lý ngoại lệ hệ thống và Thông điệp lỗi — 10 điểm**
*   **[10 điểm] Trả về thông điệp lỗi định danh:** Bẫy chính xác các trường hợp đầu vào rỗng (ném `ValueError("Danh sách giao dịch không được để rỗng")`) và trường hợp tổng cashback vượt hạn mức ngân sách lô 2,000,000 VNĐ (ném `ValueError("Tổng tiền cashback vượt quá hạn mức ngân sách lô")`).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Code sạch:** Đặt tên biến/hàm tiếng Anh chuẩn `snake_case`, chú thích logic bằng tiếng Việt có dấu, thụt lề 4 khoảng trắng chuẩn PEP 8.
*   **[5 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session06_Ex03`).

---

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý tối ưu bộ nhớ:** Sử dụng cú pháp `for...else` hợp lý để in thông báo hoàn tất kiểm toán tự động chỉ khi vòng lặp duyệt qua toàn bộ danh sách mà không bị gián đoạn bởi ngoại lệ.