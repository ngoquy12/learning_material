### **Tiêu chí chấm điểm (AI)**
**[Khắc phục lỗi tính trọng lượng quy đổi thể tích hàng hóa] — Tổng điểm: 100 điểm**

#### **1. Phân tích & Phát hiện lỗi logic (Báo cáo Test Case) — 30 điểm**
*   **[15 điểm] Xác định chính xác vị trí dòng lỗi:**
    *   Chỉ ra lỗi ép kiểu trực tiếp `float(input())` gây crash khi nhập chuỗi không phải số (5 điểm).
    *   Chỉ ra lỗi sử dụng toán tử chia nguyên `//` ở phép tính toán trọng lượng quy đổi (5 điểm).
    *   Chỉ ra lỗi thiếu kiểm tra các giá trị âm hoặc bằng 0 cho kích thước và trọng lượng (5 điểm).
*   **[15 điểm] Xây dựng bảng Test Case chứng minh:** Thiết kế đủ 3 kịch bản kiểm thử (Input sai làm crash hệ thống, Input số âm gây sai nghiệp vụ, Input số thực lẻ chứng minh phép chia nguyên làm tròn sai kết quả). Đầy đủ các trường: Input, Output lỗi thực tế, Output mong muốn.

#### **2. Hiện thực sửa lỗi mã nguồn nghiệp vụ — 40 điểm**
*   **[20 điểm] Mã nguồn chạy đúng logic nghiệp vụ:** 
    *   Tính đúng trọng lượng quy đổi bằng phép chia `/` (10 điểm).
    *   So sánh chính xác và xác định được trọng lượng tính cước lớn nhất bằng hàm phù hợp hoặc logic điều kiện (10 điểm).
*   **[20 điểm] Định dạng hiển thị chuyên nghiệp:** Sử dụng f-string định dạng hiển thị kết quả làm tròn đến 2 chữ số thập phân (`{value:.2f}`) cho tất cả các chiều kích thước và trọng lượng đầu ra (20 điểm).

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ đầu vào — 20 điểm**
*   **[10 điểm] Validate định dạng đầu vào cơ bản:** Có cơ chế kiểm tra dữ liệu chuỗi nhập vào trước khi ép kiểu để tránh lỗi `ValueError` hoặc bắt lỗi nhập chuỗi (10 điểm).
*   **[10 điểm] Bắt lỗi giá trị nghiệp vụ:** Kiểm tra và chặn các trường hợp độ dài, chiều rộng, chiều cao hoặc trọng lượng thực tế $\le 0$. Đưa ra giải pháp dừng chương trình an toàn hoặc yêu cầu nhập lại thay vì tiếp tục thực hiện tính toán (10 điểm).

#### **4. Lý thuyết mở rộng và tối ưu — 10 điểm**
*   **[10 điểm] Câu hỏi tự luận bổ sung:** Trình bày được vì sao việc sử dụng phép chia nguyên (`//`) lại gây thiệt hại tài chính cho doanh nghiệp vận chuyển logistics (Gợi ý: sự mất mát của phần thập phân khi nhân với đơn phi vận chuyển lớn sẽ gây thất thoát nhiều tiền của đơn hàng số lượng lớn).

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Định dạng mã nguồn sạch:** Tổ chức mã nguồn khoa học, đặt tên biến rõ ràng, tuân thủ quy chuẩn viết code PEP 8 (thụt lề, khoảng cách toán tử).
*   **[5 điểm] Tuân thủ nộp bài GitHub:** Đẩy mã nguồn lên GitHub Repo đúng cấu trúc thư mục quy định: `[Tên Lớp]_PythonCore_Session01_Ex02`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Xử lý vòng lặp nhập lại:** Áp dụng thành công vòng lặp (dù chưa học chính thức) để yêu cầu người dùng nhập lại dữ liệu khi nhập sai định dạng hoặc nhập số âm, thay vì tắt hẳn chương trình.