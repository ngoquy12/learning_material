### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Thiết kế Subsystem Validate và Xử lý Ngoại lệ trong Module CRM Lead Management — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Mô tả rõ ràng cơ chế hoạt động của Giải pháp 1 (Return Flag / Error Accumulator Pattern) và Giải pháp 2 (Custom Exception Hierarchy & Fail-Fast Pattern với `raise`).
    *   Nêu rõ điểm khác biệt về mặt kiến trúc xử lý luồng (Control Flow) giữa hai phương pháp.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** 
    *   Tạo bảng so sánh HTML đáp ứng thuộc tính `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.
    *   Đánh giá đầy đủ 5 tiêu chí bắt buộc: Thời gian thực thi, Mức tiêu tốn bộ nhớ, Tính đọc hiểu mã nguồn, Khả năng mở rộng/bảo trì, và Khả năng tích hợp kiểm thử Pytest.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** 
    *   Đưa ra lý giải thuyết phục vì sao chọn Custom Exception Hierarchy cho bài toán CRM Enterprise (giúp tách biệt nghiệp vụ xử lý lỗi khỏi luồng chạy chính, tường minh loại lỗi, dễ dàng ghi log tự động).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** 
    *   Trình bày mã giả (Pseudocode) sạch vẽ rõ các bước kiểm định dữ liệu và cấu trúc xử lý `try-except-else-finally` trong tiến trình xử lý hàng loạt.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** 
    *   Xây dựng hệ thống lớp Ngoại lệ tự định nghĩa chuẩn xác (`CRMBaseException` làm lớp cha, các lớp con chuyên biệt như `InvalidLeadIDError`, `InvalidContactInfoError`, v.v.).
    *   Viết hàm kiểm tra và xử lý batch dữ liệu áp dụng khối `try-except-else-finally` để phân loại và đếm số lượng bản ghi đã xử lý.
*   **[15 điểm] Xây dựng bộ kiểm thử tự động với Pytest 8.3:** 
    *   Hiện thực đầy đủ các test case bằng Pytest 8.3 trong file `test_crm_lead.py`.
    *   Sử dụng đúng `pytest.raises(...)` để kiểm tra toàn bộ các trường hợp ngoại lệ nghiệp vụ theo yêu cầu.
    *   Đảm bảo tất cả các test case đều vượt qua (PASSED) khi chạy lệnh `pytest`.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** 
    *   Hàm xử lý batch trả về đúng cấu trúc gồm danh sách các Lead thành công đã chuẩn hóa và danh sách nhật ký lỗi (Error Audit Log) chứa thông tin chi tiết: Lead ID (nếu có), loại lỗi, và thông điệp lỗi (error message).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** 
    *   Mã nguồn tuân thủ nghiêm ngặt PEP 8, đặt tên hàm/biến dạng `snake_case`, tên lớp ngoại lệ dạng `PascalCase`.
    *   Sử dụng Type Hints chuẩn Python 3.12 (ví dụ: `str | None`, `int | float`).
    *   Chú thích mã nguồn bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** 
    *   Đường dẫn GitHub hợp lệ, cấu trúc thư mục chuẩn `[Tên Lớp]_[Môn Học]_Session14_Ex04`, lịch sử commit rõ ràng.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** 
    *   Viết thêm tệp kịch bản đo thời gian thực thi (sử dụng module `time` hoặc `timeit`) để thực nghiệm so sánh tốc độ xử lý 10.000 bản ghi dữ liệu giữa Giải pháp 1 và Giải pháp 2, đưa ra kết luận thực nghiệm.