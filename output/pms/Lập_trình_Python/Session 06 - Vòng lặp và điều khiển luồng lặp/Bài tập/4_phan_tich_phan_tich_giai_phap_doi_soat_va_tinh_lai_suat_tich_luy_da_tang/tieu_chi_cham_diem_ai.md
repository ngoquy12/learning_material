### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Phân tích giải pháp đối soát và tính lãi suất tích lũy đa tầng — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   **10-15 điểm:** Phân tích chi tiết, phân biệt rõ cấu trúc lồng lề sâu (Nested code) của Phương án A và cấu trúc phẳng loại trừ sớm (Guard clause with `continue`) của Phương án B. Trình bày được bản chất hoạt động của từng phương án trên tập dữ liệu lớn.
    *   **5-9 điểm:** Mô tả được 2 phương án nhưng sơ sài, chưa chỉ ra được sự khác biệt cốt lõi về mặt kiến trúc điều khiển luồng.
    *   **0-4 điểm:** Chỉ trình bày 1 phương án hoặc mô tả sai logic nghiệp vụ.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   **10-15 điểm:** Điền đầy đủ 5 tiêu chí vào bảng HTML đúng cấu trúc. Phân tích chính xác Độ phức tạp thời gian $O(N)$, Bộ nhớ $O(1)$, và đánh giá khách quan về khả năng đọc hiểu/bảo trì của việc dùng `continue` bỏ qua các ngày `"SUSPENDED"`.
    *   **5-9 điểm:** Bảng so sánh thiếu tiêu chí hoặc lập luận so sánh chưa có tính thuyết phục kỹ thuật.
    *   **0-4 điểm:** Không có bảng so sánh hoặc bảng so sánh thiếu chuẩn HTML quy định.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   **8-10 điểm:** Đưa ra lập luận logic tài chính sắc bén, chỉ ra lý do Phương án B giúp giảm rủi ro phát sinh lỗi khi bổ sung các quy tắc nghiệp vụ mới và nâng cao hiệu suất xử lý luồng lặp.
    *   **4-7 điểm:** Lý giải chung chung, chưa gắn kết với đặc thù xử lý giao dịch Fintech.
    *   **0-3 điểm:** Không có phần lý giải hoặc lựa chọn phương án không phù hợp với yêu cầu tối ưu.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   **8-10 điểm:** Trình bày mã giả (Pseudocode) hoặc Flowchart mạch lạc, thể hiện rõ luồng duyệt `for`, bước kiểm tra `status == "SUSPENDED"` để thực hiện `continue`, và các nấc tính lãi suất bậc thang.
    *   **4-7 điểm:** Mã giả thiếu chi tiết hoặc chưa thể hiện đúng logic phân nhánh lãi suất.
    *   **0-3 điểm:** Mã giả sai logic nghiêm trọng hoặc dùng các câu lệnh bị cấm (`while`, `break`).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   **11-15 điểm:** Viết mã Python hoàn chỉnh, sử dụng chính xác vòng lặp `for` và từ khóa `continue`. Tính toán chính xác tổng tiền tích lũy và tổng tiền lãi phát sinh qua `N` chu kỳ theo đúng 3 mức lãi suất bậc thang.
    *   **6-10 điểm:** Viết được code nhưng tính sai công thức lãi suất bậc thang hoặc áp dụng sai tỷ lệ lãi suất ngày.
    *   **0-5 điểm:** Mã nguồn vi phạm ràng buộc cấm (sử dụng `while` hoặc `break`), hoặc code không chạy được.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   **11-15 điểm:** Xử lý triệt để các trường hợp đặc biệt: `deposit` nhỏ hơn 0 (bỏ qua hoặc cảnh báo), số dư không đủ điều kiện nâng nấc lãi suất, danh sách chu kỳ rỗng, dữ liệu có trạng thái không hợp lệ.
    *   **6-10 điểm:** Có kiểm tra biên nhưng chưa bao quát hết các trường hợp dữ liệu rác.
    *   **0-5 điểm:** Không có kiểm tra dữ liệu biên, chương trình dễ bị crash khi gặp input sai định dạng.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   **8-10 điểm:** Trả về kết quả dưới dạng `dict` chứa các thông tin tài chính sạch sẽ (`initial_balance`, `final_balance`, `total_interest_earned`, `active_cycles_count`), định dạng số thực chính xác đến 2 chữ số thập phân nếu cần.
    *   **4-7 điểm:** Đã trả về kết quả nhưng định dạng dữ liệu còn thừa/thiếu các trường thông tin chính.
    *   **0-3 điểm:** Không trả về đúng cấu trúc dữ liệu yêu cầu.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   **4-5 điểm:** Tuân thủ chuẩn PEP 8, sử dụng Type Hints Python 3.10+ (ví dụ: `str | float`), tên hàm/biến bằng tiếng Anh theo `snake_case`, chú thích giải trình bằng Tiếng Việt có dấu rõ ràng.
    *   **2-3 điểm:** Tên biến/hàm chưa chuẩn tiếng Anh hoặc thiếu chú thích Tiếng Việt.
    *   **0-1 điểm:** Vi phạm PEP 8, mã nguồn viết cẩu thả, đặt tên biến viết tắt khó hiểu.
*   **[5 điểm] Nộp bài GitHub:**
    *   **5 điểm:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session06_Ex04`), commit message rõ ràng.
    *   **0 điểm:** Không nộp link GitHub hoặc sai cấu trúc thư mục.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Thực hiện viết một đoạn script đo thời gian thực thi (sử dụng thư viện chuẩn `time`) so sánh hiệu năng chạy giữa Phương án A và Phương án B trên tập dữ liệu giả lập $100,000$ chu kỳ tài chính để minh chứng sự tối ưu của Guard Clause.