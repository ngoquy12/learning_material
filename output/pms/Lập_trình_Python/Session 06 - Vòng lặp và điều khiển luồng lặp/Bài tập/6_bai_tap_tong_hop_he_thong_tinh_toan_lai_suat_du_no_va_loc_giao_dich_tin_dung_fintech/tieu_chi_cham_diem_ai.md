### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Hệ thống tính toán lãi suất dư nợ và lọc giao dịch tín dụng Fintech — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Tạo file mã nguồn sạch, cấu trúc dự án rõ ràng, định nghĩa đúng kiểu dữ liệu đầu vào và các hằng số cấu hình (lãi suất, hạn mức giao dịch đơn).
*   **[10 điểm] Xây dựng Cấu trúc dữ liệu:** Khai báo chính xác Type Hints cho hàm và biến theo tiêu chuẩn Python 3.10+ (sử dụng `list[float]`, `tuple[int, float]`, `dict[str, float | int]`).

#### **2. Hiện thực hóa các Chức năng cơ bản — 40 điểm**
*   **[20 điểm] Chức năng Lọc giao dịch và tính dư nợ gốc:** Sử dụng đúng vòng lặp `for` để duyệt danh sách giao dịch, tính toán chính xác tổng dư nợ gốc ban đầu từ các giao dịch hợp lệ.
*   **[20 điểm] Chức năng Tính toán lãi suất tích lũy:** Sử dụng đúng vòng lặp `for` với `range(1, months + 1)` để tính tiền lãi phát sinh và tổng dư nợ tích lũy qua $N$ tháng theo công thức tài chính.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Xử lý lọc bỏ bản ghi bằng `continue`:** Áp dụng thành công câu lệnh `continue` để bỏ qua các giá trị $\le 0$ hoặc vượt quá hạn mức $50,000,000$ VNĐ mà không làm gián đoạn vòng lặp.
*   **[10 điểm] Xử lý danh sách rỗng / Không có giao dịch hợp lệ:** Đảm bảo hệ thống hoạt động an toàn, không phát sinh lỗi khi danh sách giao dịch thô bị rỗng hoặc toàn bộ giao dịch bị lọc bỏ.

#### **4. Chất lượng mã nguồn và Đóng gói Response — 10 điểm**
*   **[10 điểm] Định dạng dữ liệu đầu ra sạch:** Đóng gói kết quả dạng Dictionary đúng cấu trúc yêu cầu; mã nguồn đặt tên biến/hàm 100% bằng tiếng Anh chuẩn PEP 8, comment logic bằng tiếng Việt có dấu.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Nộp bài GitHub:** Đẩy mã nguồn lên repository GitHub đúng theo định dạng thư mục quy định: `[Tên Lớp]_[Môn Học]_Session06_Ex06`.