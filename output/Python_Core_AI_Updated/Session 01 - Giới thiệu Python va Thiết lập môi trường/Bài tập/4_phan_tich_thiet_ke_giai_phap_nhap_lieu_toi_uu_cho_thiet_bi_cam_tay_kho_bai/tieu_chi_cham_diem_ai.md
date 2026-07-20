### **Tiêu chí chấm điểm (AI)**
**[Phân tích] Thiết kế giải pháp nhập liệu tối ưu cho thiết bị cầm tay kho bãi — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Nêu rõ được cơ chế hoạt động của việc gọi nhiều lời gọi `input()` tuần tự (Giải pháp 1) đối lập với việc đọc một luồng chuỗi ký tự duy nhất rồi phân tách trên RAM (Giải pháp 2).
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Điền đầy đủ thông tin phân tích vào 5 tiêu chí yêu cầu trong bảng. Lập luận rõ nét sự khác biệt về độ phức tạp khi số lượng thuộc tính của kiện hàng tăng lên (ví dụ: thêm phụ phí hàng cồng kềnh, mã bưu cục nhận).

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Giải thích thuyết phục tại sao lựa chọn giải pháp tối ưu phù hợp với tài nguyên phần cứng hạn chế của thiết bị cầm tay (như giảm IO block, tối thiểu hóa số lần gọi luồng nhập xuất tiêu chuẩn).
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Trình bày mã giả logic tường minh, đầy đủ các bước từ nhập dữ liệu, trích xuất chỉ mục hoặc cắt chuỗi, ép kiểu sang `float`/`int`, tính toán biểu thức đại số, và chuẩn bị chuỗi định dạng đầu ra.

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Viết mã lệnh Python chạy được mà không gặp lỗi cú pháp. Sử dụng chính xác phương thức xử lý chuỗi để phân tách và gán giá trị cho các biến thành phần từ chuỗi gộp.
*   **[15 điểm] Xử lý số liệu và biểu thức chính xác:** Thực hiện đúng trình tự ép kiểu dữ liệu (từ chuỗi sang số thực/số nguyên) trước khi làm toán. Áp dụng đúng công thức tính toán nghiệp vụ Logistics đã cho trong đề bài.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Response — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc hiển thị:** Sử dụng hiệu quả cơ chế căn lề của f-string để các nhãn hiển thị thẳng hàng (ví dụ: sử dụng `{bien:<15}` hoặc `{bien:>10}`). Định dạng số tiền có dấu phân cách hàng nghìn trực quan và làm tròn số tiền theo đúng nghiệp vụ.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến sử dụng chuẩn snake_case (ví dụ: `ma_van_don`, `trong_luong`, `tong_chi_phi`). Code có chú thích ngắn gọn giải thích các bước chuyển đổi dữ liệu.
*   **[5 điểm] Quy chuẩn nộp bài:** Đẩy mã nguồn lên GitHub đúng cấu trúc thư mục quy định (`[Tên Lớp]_[Môn Học]_Session01_Ex04`), lịch sử commit thể hiện rõ các bước hoàn thành bài tập.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Mô phỏng/Đánh giá hiệu năng:** Viết thêm một đoạn phân tích ngắn gọn trong báo cáo định lượng dung lượng bộ nhớ lý thuyết được giải phóng khi không phải duy trì các tiến trình đợi nhập liệu từ bàn phím lâu ngày, hoặc các giải pháp phòng tránh lỗi runtime khi chuỗi đầu vào bị thiếu/sai ký tự phân tách mà không cần dùng câu lệnh `if-else` (ví dụ: tận dụng các giá trị mặc định).