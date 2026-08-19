# **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Phân tích và Thiết kế Module Tính Tiền Hóa Đơn POS Highlands Coffee — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:**
    *   Mô tả chi tiết 2 phương án kỹ thuật độc lập xử lý bài toán tính tiền tệ (Ví dụ: Phương án 1 dùng phép tính số thực `float` kết hợp ép kiểu làm tròn `int(round(...))`; Phương án 2 dùng phép tính quy đổi hoàn toàn về số nguyên `int` thông qua công thức tỉ lệ đại số để tránh sai số float).
    *   Nêu rõ sự khác biệt về bản chất kiểu dữ liệu và toán tử sử dụng giữa 2 phương án.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:**
    *   Lập bảng so sánh đầy đủ 5 tiêu chí: Speed, Memory, Maintainability, Readability, Suitability.
    *   Phân tích ưu/nhược điểm hợp lý, chuẩn xác về mặt khoa học máy tính.

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:**
    *   Đưa ra lý do thuyết phục tại sao chọn phương án tối ưu (tập trung vào tính chính xác tuyệt đối của tài chính và độ sáng rõ của mã nguồn).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu (Flowchart):**
    *   Vẽ sơ đồ Mermaid chuẩn hóa 5 dạng hình (Terminator `([ ])`, Input/Output `[/ /]`, Process `[" "]`, Decision `{" "}`, Flowline `-->`).
    *   Luồng xử lý tuần tự logic từ lúc thu thập input CLI đến khi in ra hóa đơn cuối cùng.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:**
    *   Nhập đầy đủ thông tin từ bàn phím bằng `input()`.
    *   Thực hiện chuyển đổi kiểu dữ liệu `int()` / `float()` phù hợp cho từng biến đầu vào.
    *   Tính toán chính xác các chỉ số: Phụ thu topping, Subtotal, Giảm giá Vàng (10%), VAT (8%), và Final Total.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:**
    *   Xử lý đúng trường hợp số lượng topping bằng 0.
    *   Đảm bảo không bị hiện tượng làm tròn sai lệch (ví dụ xuất ra số đuôi thập phân dài `.000000001` trên hóa đơn).

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:**
    *   In hóa đơn chuyên nghiệp với tiêu đề, phân dòng và các mục tiền rõ ràng.
    *   Kết quả hiển thị tiền tệ được làm tròn về số nguyên chuẩn xác.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:**
    *   Tên biến bằng tiếng Anh đúng chuẩn danh từ/tính từ (`drink_name`, `base_price`, `topping_count`, `discount_amount`, `final_total`).
    *   Mã nguồn có chú thích bằng tiếng Việt có dấu rõ ràng, dễ hiểu.
*   **[5 điểm] Nộp bài GitHub:**
    *   Đường dẫn GitHub hợp lệ, thư mục đặt đúng quy chuẩn `[Tên Lớp]_[Môn Học]_SessionSESSION_01_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:**
    *   Viết đoạn mã đo lường thời gian thực thi (dùng thư viện `time`) so sánh hiệu năng chạy 1.000.000 phép tính giữa 2 phương án đã đề xuất.
