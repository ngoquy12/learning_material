### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Đề xuất phương án bóc tách mã Pallet nhập kho tự động — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** 
    *   Giải trình rõ ràng bản chất kỹ thuật của việc cắt chuỗi (Tạo các vùng nhớ mới cho chuỗi con, thao tác trên String pool của Python) ở giải pháp 1.
    *   Giải trình bản chất kỹ thuật của phép toán số học (Thực hiện trực tiếp bằng thanh ghi số học của CPU, không tạo thêm chuỗi con trung gian) ở giải pháp 2.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** 
    *   Lập bảng đầy đủ 5 tiêu chí so sánh (RAM, Tốc độ, Dễ đọc, Dễ bảo trì, Bối cảnh phù hợp).
    *   Đánh giá đúng đắn: Xử lý số học (Giải pháp 2) tiết kiệm bộ nhớ RAM và chạy nhanh hơn so với xử lý cắt chuỗi (Giải pháp 1) nhưng kém linh hoạt hơn nếu cấu trúc số lượng ký tự thay đổi (ví dụ: chuyển từ 8 chữ số thành 10 chữ số).

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Đưa ra lập luận thuyết phục bảo vệ giải pháp tối ưu dựa trên điều kiện tài nguyên hạn chế của thiết bị IoT Gateway (ưu tiên tiết kiệm RAM và chu kỳ CPU).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** 
    *   Trình bày mã giả rõ ràng các bước thực hiện tuần tự.
    *   Mã giả không chứa các cấu trúc ngoài phạm vi học (không dùng hàm hoặc vòng lặp).

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** 
    *   Nhập dữ liệu với `input()` và ép kiểu chính xác.
    *   Thực hiện các toán tử đúng logic (Ví dụ: `sku = pallet_id // 10000` và `quantity = pallet_id % 10000`).
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Tự tính toán được khoảng trống tối đa của kệ (`500 - quantity`) chính xác thông qua phép toán trừ.
    *   Chương trình hoạt động trơn tru không phát sinh lỗi cú pháp.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Response — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc hiển thị:**
    *   Sử dụng f-string xuất ra đúng định dạng yêu cầu ở Mục 3.
    *   Hiển thị đúng giá trị số nguyên SKU và Số lượng (không hiển thị dạng float hoặc hiển thị sai chuỗi log).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến tuân thủ snake_case (ví dụ: `pallet_id`, `product_sku`, `empty_space`).
    *   Có comment giải thích các bước tính toán rõ ràng.
*   **[5 điểm] Nộp bài GitHub:**
    *   Nộp đúng thư mục cấu trúc yêu cầu: `[Tên Lớp]_[Môn Học]_Session01_Ex04`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Script So sánh Kết quả chéo:**
    *   Học viên tự viết thêm một script Python chạy cả hai giải pháp song song với cùng một đầu vào dữ liệu.
    *   Sử dụng toán tử so sánh (`==`) để tự động kiểm tra xem kết quả đầu ra của Mã SKU và Số lượng của cả 2 giải pháp có bằng nhau hay không và in kết quả kiểm thử (`True`/`False`) ra màn hình.