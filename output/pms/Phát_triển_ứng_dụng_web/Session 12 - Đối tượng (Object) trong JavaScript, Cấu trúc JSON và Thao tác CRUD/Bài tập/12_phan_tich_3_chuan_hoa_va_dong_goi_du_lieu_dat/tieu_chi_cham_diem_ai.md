# **Tiêu chí chấm điểm (AI)**
**[Phân tích 3] Chuẩn hóa và đóng gói dữ liệu đặt phòng khách sạn — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Trình bày rõ ràng cấu trúc tư duy của 2 phương án (Ví dụ: Phương án thao tác trực tiếp trên Object ban đầu - Direct Mutation; Phương án khởi tạo Object sạch mới và trích xuất trường - Object Transformation).
    *   Nêu rõ sự khác biệt về cú pháp truy cập thuộc tính tĩnh (Dot Notation) và thuộc tính động có ký tự đặc biệt (Bracket Notation).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Khởi tạo bảng so sánh đúng cấu trúc HTML style: `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`.
    *   So sánh đầy đủ 5 tiêu chí: Tốc độ xử lý, Tiêu tốn bộ nhớ, Khả năng bảo trì, Độ dễ đọc, Ngữ cảnh áp dụng.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Phân tích lý do chọn phương án tối ưu dựa trên việc tránh rò rỉ dữ liệu nhạy cảm (`creditCardCVV`) và tối ưu vùng nhớ cho ứng dụng Hotel Booking.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:**
    *   Vẽ Mermaid Flowchart chính xác theo chuẩn 5 hình dạng (Oval cho Start/End, Parallelogram cho In/Out, Rectangle cho Process, Diamond cho Decision).
    *   Tuyệt đối không vi phạm bẫy lỗi dùng Parallelogram cho khối tính toán.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Khai báo Object `bookingData` ban đầu đầy đủ thuộc tính nghiệp vụ.
    *   Sử dụng Bracket Notation đúng cách để thêm/cập nhật thuộc tính `"early-checkin-fee"`.
    *   Tính toán chính xác `totalAmount` và gắn trường `isChildExempt`.
    *   Sử dụng đúng từ khóa `delete` để loại bỏ `creditCardCVV` và `tempAuthToken`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Bắt lỗi nếu `checkInHour` không hợp lệ (nhỏ hơn 0 hoặc lớn hơn 23).
    *   Đảm bảo thuộc tính bị `delete` không còn xuất hiện trong chuỗi JSON thu được.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   Sử dụng `JSON.stringify()` để tạo chuỗi JSON hợp lệ.
    *   Sử dụng `JSON.parse()` để giải mã và truy xuất thành công thuộc tính `"early-checkin-fee"` từ Object đã khôi phục.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến/hàm 100% bằng tiếng Anh chuẩn camelCase (ví dụ: `roomPricePerNight`, `earlyCheckInFee`, `sanitizedBooking`).
    *   Chú thích mã nguồn bằng Tiếng Việt có dấu rõ ràng.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub hợp lệ, thư mục đặt tên đúng định dạng quy định.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Xây dựng đoạn mã đo lường thời gian thực thi (sử dụng `console.time` / `console.timeEnd`) để so sánh hiệu năng xử lý 10,000 lượt đặt phòng giữa 2 phương án kỹ thuật.
