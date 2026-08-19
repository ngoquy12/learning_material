### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân Tích Và Thiết Kế Bộ Xử Lý Đặt Vé Sự Kiện Vấn Đề Phạm Vi Biến Và Hạn Ngạch Check-in — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Mô tả chi tiết giải pháp 1 (ví dụ: Sử dụng Function Declaration/Expression truyền thống kết hợp biến toàn cục hoặc kiểm tra tham số bằng toán tử logic `||`). Nêu rõ các lỗ hổng về Global Scope Pollution và falsy value (`serviceFee = 0`).
    *   Mô tả chi tiết giải pháp 2 (ví dụ: Sử dụng Arrow Functions, ES6 Default Parameters và mô hình Closure để đóng gói trạng thái biến cục bộ `remainingTickets`).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng so sánh hoàn chỉnh sử dụng thẻ HTML table đúng định dạng `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.
    *   Đánh giá chi tiết đủ 5 tiêu chí: Tốc độ xử lý (Speed), Chi phí bộ nhớ (Memory), Khả năng bảo trì (Maintainability), Độ rõ ràng (Readability), Mức độ phù hợp sản xuất (Suitability).

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Lý giải thuyết phục tại sao giải pháp sử dụng Closure và ES6 Default Parameters lại tối ưu vượt trội trong việc bảo vệ dữ liệu kho vé và tính toán chính xác hóa đơn dưới tải giao dịch cao.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ sơ đồ luồng Mermaid Flowchart hoặc viết Pseudocode chi tiết logic xử lý đặt vé.
    *   Nếu dùng Mermaid, bắt buộc tuân thủ đúng 5 chuẩn hình khối (Oval `([Bắt đầu/Kết thúc])`, Parallelogram `[/Đầu vào/Đầu ra/]`, Diamond `Kiểm tra điều kiện?`, Rectangle `["Tính toán/Xử lý"]`, Arrow `-->`). Không sử dụng Parallelogram cho khối xử lý tính toán.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Sử dụng cú pháp chuẩn ES6+ (Arrow Functions, `const`/`let`, Default Parameters).
    *   Tạo hàm Closure đóng gói an toàn biến `remainingTickets` (hoàn toàn không thể bị can thiệp từ bên ngoài).
    *   Viết hàm tính tổng chi phí thanh toán `calculateOrderTotal` chính xác theo công thức nghiệp vụ.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Kiểm tra số lượng vé hợp lệ (1 <= quantity <= 4), nếu sai trả về thông báo lỗi phù hợp.
    *   Xử lý chính xác tham số mặc định khi `serviceFee = 0` (không bị ghi đè thành 30,000).
    *   Từ chối đơn hàng và giữ nguyên số lượng tồn kho khi vé yêu cầu > vé còn lại trong Zone.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Hàm trả về đối tượng kết quả chứa đầy đủ thông tin: `success` (boolean), `message` (string), `totalAmount` (number), `remainingTickets` (number) mà không dư thừa các thuộc tính không cần thiết.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến, tên hàm sử dụng tiếng Anh chuẩn camelCase (ví dụ: `createTicketManager`, `calculateOrderTotal`, `discountRate`).
    *   Mã nguồn sạch rành mạch, có chú thích giải thích bằng tiếng Việt có dấu. Không sử dụng các từ ngữ cấm hoặc emoji trong mã nguồn.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn repository GitHub hợp lệ, đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session14_Ex10`).

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Viết đoạn mã thử nghiệm mô phỏng gọi liên tục 1,000 lượt đặt vé đồng thời để đo thời gian thực thi và xác nhận tính toàn vẹn dữ liệu kho vé không bị phá hỏng.