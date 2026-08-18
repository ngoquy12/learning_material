### **Tiêu chí chấm điểm (AI)**
**[Phân tích 1] Phân tích và Xử lý Đóng gói Dữ liệu Đặt phòng Khách sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Trình bày độc lập, chi tiết ít nhất 2 phương án kỹ thuật xử lý dữ liệu đối tượng (ví dụ: Thao tác biến đổi trực tiếp trên đối tượng gốc `Mutation` vs Tạo đối tượng clone mới làm sạch `Immutability`/`Helper Function`).
    *   Phân tích cơ chế bộ nhớ và cách truy cập thuộc tính của từng phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** 
    *   Xây dựng bảng HTML đầy đủ 5 tiêu chí: Tốc độ xử lý, Dung lượng bộ nhớ, Khả năng bảo trì, Độ rõ ràng, Độ phù hợp.
    *   Bảng HTML có sử dụng attribute bắt buộc: `style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%"`.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** 
    *   Lập luận chặt chẽ vì sao phương án được chọn phù hợp với hệ thống đặt phòng trực tuyến (đảm bảo tính an toàn dữ liệu nhạy cảm, tối ưu RAM, mã nguồn sạch).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** 
    *   Vẽ Mermaid Flowchart hoặc viết mã giả chính xác logic xử lý.
    *   Tuân thủ 100% chuẩn hình dạng Mermaid: Terminator `([ ])`, Input/Output `[/ /]`, Decision `?`, Process `[" "]`. Tuyệt đối không dùng sai ký hiệu khối.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** 
    *   Viết code JavaScript Vanilla (ES6+) chạy đúng yêu cầu nghiệp vụ.
    *   Sử dụng đúng Dot Notation cho key tiêu chuẩn và Bracket Notation cho key chứa dấu gạch ngang/biến động.
    *   Tính chính xác phụ thu check-in sớm (30% `basePrice`) và phụ thu trẻ em (`150000`).
    *   Dùng đúng từ khóa `delete` để loại bỏ `tempAuthToken` và `draftDiscountCode`.
    *   Sử dụng đúng `JSON.stringify()` và `JSON.parse()`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** 
    *   Không để xảy ra lỗi `ReferenceError` khi dùng ngoặc vuông.
    *   Không gán `undefined`/`null` thay cho `delete`.
    *   Không cố tình truy cập thuộc tính trên chuỗi JSON chưa parse.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** 
    *   Chuỗi JSON thu được hoàn toàn sạch sẽ, không chứa các token nhạy cảm tạm thời.
    *   Đối tượng khôi phục sau khi parse truy xuất chính xác các thuộc tính động và phụ phí.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** 
    *   Đặt tên biến/thuộc tính bằng tiếng Anh chuẩn chuẩn camelCase (`bookingReservation`, `checkInHour`, `basePrice`, `earlyCheckInFee`).
    *   Chú thích giải thích bằng tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:** 
    *   Đường link GitHub hợp lệ, đúng cấu trúc thư mục yêu cầu `[Tên Lớp]_[Môn Học]_Session12_Ex10`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** 
    *   Viết đoạn mã đo lường thời gian xử lý (dùng `console.time`/`console.timeEnd`) để so sánh hiệu năng giữa phương án xóa trực tiếp (`delete`) và phương án tạo bản sao đối tượng mới trước khi chuyển sang JSON.