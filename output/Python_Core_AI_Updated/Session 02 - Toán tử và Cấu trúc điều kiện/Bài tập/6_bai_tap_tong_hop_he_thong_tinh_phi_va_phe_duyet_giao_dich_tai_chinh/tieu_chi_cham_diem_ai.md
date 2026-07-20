### **Tiêu chí chấm điểm (AI)**
**[Bài tập tổng hợp] Hệ thống tính phí và phê duyệt giao dịch tài chính — Tổng điểm: 100 điểm**

#### **1. Khởi tạo Dự án & Schema dữ liệu — 20 điểm**
*   **[10 điểm] Thiết lập môi trường và cấu trúc dự án:** Khởi tạo thành công môi trường ảo `.venv`, cài đặt được các thư viện `fastapi` và `uintcorn`, thiết lập tệp tin chính khởi chạy API đúng chuẩn mà không phát sinh lỗi.
*   **[10 điểm] Xây dựng Pydantic Schemas:** Định nghĩa chính xác cấu trúc dữ liệu đầu vào cho yêu cầu tạo giao dịch (chứa `account_type` giới hạn trong các giá trị hợp lệ, số tiền `amount` kiểu số) và các cấu trúc phản hồi đầu ra chứa đầy đủ các trường thông tin theo mô tả.

#### **2. Hiện thực hóa các API chức năng cơ bản — 40 điểm**
*   **[10 điểm] API Lấy số dư hiện tại (GET `/balance`):** Trả về chính xác số dư hiện tại của tài khoản hệ thống.
*   **[15 điểm] API Xem danh sách giao dịch (GET `/transactions`):** Trả về đầy đủ lịch sử của tất cả các giao dịch đã thực hiện trong phiên làm việc.
*   **[15 điểm] API Xóa giao dịch (DELETE `/transactions/{transaction_id}`):** Xóa đúng bản ghi giao dịch được chỉ định khỏi RAM dựa trên ID truyền vào.

#### **3. Kiểm chuẩn logic & Chặn bẫy dữ liệu cơ bản — 20 điểm**
*   **[10 điểm] Cơ chế tính toán phí và phê duyệt giao dịch (POST `/transactions`):** 
    *   Áp dụng chính xác mô hình tính toán số học và các cấu trúc logic (`match-case`, `if-elif-else`) để tính ra chi phí giao dịch dựa trên từng loại hạng tài khoản hệ thống.
    *   Trừ số dư tài khoản thành công theo đúng tổng chi phí khi giao dịch được chấp thuận.
*   **[10 điểm] Xử lý ngoại lệ và lỗi nghiệp vụ:**
    *   Trả về mã lỗi HTTP 400 Bad Request kèm thông báo chi tiết khi giao dịch bị từ chối do số dư không đủ hoặc số tiền giao dịch không hợp lệ (nhỏ hơn hoặc bằng 0).
    *   Trả về mã lỗi HTTP 404 Not Found khi thực hiện xóa giao dịch với ID không tồn tại.

#### **4. Chất lượng mã nguồn và Đóng gói API Response — 10 điểm**
*   **[5 điểm] Định dạng dữ liệu và quy chuẩn ngôn ngữ:** Định nghĩa đúng tên các trường dữ liệu bằng tiếng Anh kỹ thuật, giữ code sạch sẽ, có giải thích chú thích cơ bản về logic nghiệp vụ.
*   **[5 điểm] Quy chuẩn thiết kế API:** Sử dụng đúng các HTTP Method (GET, POST, DELETE) phù hợp với mục đích xử lý của từng chức năng.

#### **5. Quy chuẩn nộp bài GitHub — 10 điểm**
*   **[10 điểm] Quy chuẩn lưu trữ:** Cam kết mã nguồn chạy ổn định lên GitHub với cấu trúc tên thư mục đặt đúng quy cách: `[Tên Lớp]_[Môn Học]_Session02_Tong_hop`.