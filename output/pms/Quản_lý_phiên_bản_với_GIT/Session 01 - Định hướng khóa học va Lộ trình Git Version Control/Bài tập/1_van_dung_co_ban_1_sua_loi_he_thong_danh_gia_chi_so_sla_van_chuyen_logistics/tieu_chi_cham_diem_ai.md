### **Tiêu chí chấm điểm (AI)**
**[Vận dụng cơ bản 1] Sửa lỗi hệ thống đánh giá chỉ số SLA vận chuyển Logistics — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi vận hành (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác lỗi:** Chỉ ra đầy đủ 3 lỗi sai logic trong bài toán (tính sai trọng số 20%-30%-50%, bỏ qua tỷ lệ giám sát GPS 80%, không làm tròn 2 chữ số thập phân).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Xây dựng bảng HTML đủ 3 kịch bản kiểm thử (Input, Actual Buggy Output, Expected Output) dùng chuẩn định dạng `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;"`.

#### **2. Thao tác khắc phục sự cố & Lệnh thực thi — 40 điểm**
*   **[20 điểm] Thao tác đúng lệnh nghiệp vụ:** Khai báo chính xác cấu trúc Class `ShipmentEvaluationEngine` chứa thuộc tính `weights` đúng tỷ lệ trọng số doanh nghiệp.
*   **[20 điểm] Xử lý tình huống hệ thống:** Sửa thành công hàm `calculateFinalScore` và `verifySLACompletion`, tính toán đúng điểm tổng hợp và áp dụng toán tử logic `&&` kiểm tra điều kiện an toàn hành trình.

#### **3. Kiểm chuẩn quy trình & Trạng thái hệ thống — 20 điểm**
*   **[10 điểm] Validate cấu hình cơ bản:** Kiểm tra chính xác số checkpoint tối thiểu đạt $80\%$ tổng lộ trình (`monitoredCheckpoints >= totalRouteCheckpoints * 0.8`).
*   **[10 điểm] Bắt lỗi an toàn hệ thống:** Xử lý làm tròn điểm số bằng `Number(totalScore.toFixed(2))` đảm bảo không phát sinh lỗi số thực trong JS.

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Trả lời ngắn gọn lý do tại sao việc bỏ qua ràng buộc tỷ lệ giám sát GPS lại làm gia tăng rủi ro thất thoát hàng hóa và giảm uy tín doanh nghiệp Logistics.

#### **5. Chất lượng quy trình và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Nhật ký thao tác sạch:** Mã nguồn sạch đẹp, định dạng đúng chuẩn, tên biến tiếng Anh, comment tiếng Việt rõ ràng.
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Nộp bài và đẩy mã nguồn đúng thư mục quy định `[Tên Lớp]_[Môn Học]_Session01_Ex01`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Tự động hóa quy trình:** Viết thêm một hàm tự động chạy qua danh sách (array) gồm 5 đơn hàng mẫu để xuất kết quả báo cáo kiểm duyệt hàng loạt.