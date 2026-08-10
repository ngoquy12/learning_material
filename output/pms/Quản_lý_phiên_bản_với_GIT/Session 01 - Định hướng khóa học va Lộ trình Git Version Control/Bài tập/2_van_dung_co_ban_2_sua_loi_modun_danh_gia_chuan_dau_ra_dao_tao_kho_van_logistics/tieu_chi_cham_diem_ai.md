### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 2] Sửa lỗi mô-đun đánh giá chuẩn đầu ra đào tạo kho vận Logistics — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi vận hành (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác lỗi:** Chỉ ra đầy đủ 2 lỗi sai nghiệp vụ cốt lõi (không tính đúng trọng số 20-30-50 và bỏ qua kiểm tra điều kiện chuyên cần 80%).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Hoàn thành bảng HTML Table chứa tối thiểu 03 kịch bản kiểm thử (Test Cases) phân biệt rõ Dữ liệu đầu vào, Kết quả lỗi hiện tại và Kết quả kỳ vọng.

#### **2. Thao tác khắc phục sự cố & Lệnh thực thi — 40 điểm**
*   **[20 điểm] Thao tác đúng lệnh nghiệp vụ:** Xây dựng lại lớp `CourseEvaluationEngine` với cấu trúc constructor chứa thuộc tính trọng số `weights` đúng tỷ trọng (0.20, 0.30, 0.50).
*   **[20 điểm] Xử lý tình huống hệ thống:** Triển khai chính xác thuật toán tính toán `calculateFinalScore` và làm tròn số chuẩn `Number(totalScore.toFixed(2))`.

#### **3. Kiểm chuẩn quy trình & Trạng thái hệ thống — 20 điểm**
*   **[10 điểm] Validate cấu hình cơ bản:** Kiểm tra chính xác điều kiện số buổi tham gia tối thiểu `attendedSessions >= totalSessions * 0.8` trong `verifyCLOCompletion`.
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Kết hợp logic điều kiện `isPassed` bằng toán tử logic `&&` đảm bảo cả 2 điều kiện (chuyên cần và điểm tổng kết) đều phải thỏa mãn mới trả về trạng thái "ĐẠT CHUẨN ĐẦU RA (CLO/PLO)".

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Giải thích được tác hại của việc cào bằng trọng số hoặc bỏ qua kiểm tra chuyên cần trong các hệ thống phần mềm quản trị doanh nghiệp/kho vận thực tế.

#### **5. Chất lượng quy trình và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Nhật ký thao tác sạch:** Mã nguồn viết sạch sẻ, tên biến/hàm 100% tiếng Anh, chú thích Tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session01_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tự động hóa quy trình:** Viết thêm đoạn mã tự động duyệt qua danh sách (array) nhiều nhân viên kho và in ra bảng tổng hợp kết quả đạt/không đạt CLO/PLO.