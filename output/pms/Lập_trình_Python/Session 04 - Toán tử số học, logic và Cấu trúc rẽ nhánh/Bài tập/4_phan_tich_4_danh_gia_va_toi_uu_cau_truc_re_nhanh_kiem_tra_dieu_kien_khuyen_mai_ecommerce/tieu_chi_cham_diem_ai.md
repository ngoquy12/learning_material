### **Tiêu chí chấm điểm (AI)**
**[Phân tích 4] Đánh giá và tối ưu cấu trúc rẽ nhánh kiểm tra điều kiện khuyến mãi E-Commerce — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Mô tả rõ ràng cơ chế hoạt động của Phương án A (Cấu trúc rẽ nhánh lồng nhau - Arrow Anti-Pattern). (7.5 điểm)
    *   Mô tả rõ ràng cơ chế hoạt động của Phương án B (Phẳng hóa điều kiện với toán tử logic `and`, `or` theo chuẩn PEP 8). (7.5 điểm)
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Hoàn thiện đầy đủ bảng so sánh HTML với 5 tiêu chí: Thời gian xử lý, Bộ nhớ, Độ đọc hiểu, Khả năng bảo trì, và Mức độ phù hợp. (10 điểm)
    *   Phân tích chính xác ưu/nhược điểm kỹ thuật của từng tiêu chí (không phán đoán cảm tính). (5 điểm)

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lý luận thuyết phục về lý do chọn Phương án B dựa trên khả năng bảo trì, giảm độ phức tạp cyclomatic complexity và tuân thủ nguyên lý Clean Code. (10 điểm)
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Mã giả hoặc sơ đồ luồng mô tả đúng các bước kiểm tra dữ liệu đầu vào và các nhánh điều kiện phẳng hóa. (10 điểm)

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Viết hàm bằng Python thực hiện đúng quy tắc nghiệp vụ Mức 1 (Giảm 20% + Freeship), Mức 2 (Giảm 10%), và Mức 3 (Giảm 0%). (15 điểm)
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Kiểm tra chính xác các điều kiện dữ liệu không hợp lệ: `cart_value <= 0`, `customer_age < 0`, `shipping_distance < 0`, `total_past_orders < 0` và trả về thông báo lỗi thích hợp. (15 điểm)

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Hàm trả về chuỗi thông báo kết quả rõ ràng, chính xác với từng trường hợp thử nghiệm mà không làm gián đoạn chương trình. (10 điểm)

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Đạt chuẩn PEP 8: thụt lề 4 space, đặt tên hàm/biến theo `snake_case`, có Type Hints đầy đủ (`cart_value: float`, ...). (5 điểm)
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub hợp lệ, đúng cấu trúc thư mục quy định `[Tên Lớp]_[Môn Học]_Session04_Ex04`. (5 điểm)

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Viết đoạn mã đo lường thời gian thực thi (dùng thư viện `time` hoặc `timeit`) chạy thử 100.000 lượt đánh giá để chứng minh hiệu năng thực tế của Phương án B so với Phương án A. (10 điểm)