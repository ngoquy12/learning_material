# **Tiêu chí chấm điểm (AI)**
**[Phân tích 2] Cập nhật và Xóa cước phí chuyến xe GrabRide — Tổng điểm: 100 điểm**

#### **1. Báo cáo Đề xuất đa giải pháp & So sánh Trade-off — 30 điểm**
*   **[15 điểm] Mô tả ít nhất 2 giải pháp kỹ thuật:** Học viên tự đề xuất và phân tích cấu trúc 2 phương án xử lý khác nhau (ví dụ: Thao tác cập nhật gán chỉ số và xóa trực tiếp bằng `del` VS. Khởi tạo danh sách mới để sao chép phần tử loại trừ phần tử bị hủy) mà không vi phạm phạm vi kiến thức cấm.
*   **[15 điểm] Bảng so sánh Trade-off trực quan:** Xây dựng bảng so sánh chuẩn format HTML với đầy đủ 5 tiêu chí:
    <table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
      <thead>
        <tr>
          <th style="border: 1px solid #dddddd; padding: 8px;">Tiêu chí</th>
          <th style="border: 1px solid #dddddd; padding: 8px;">Phương án A</th>
          <th style="border: 1px solid #dddddd; padding: 8px;">Phương án B</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="border: 1px solid #dddddd; padding: 8px;">Time Complexity</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Đánh giá chi tiết O(...)</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Đánh giá chi tiết O(...)</td>
        </tr>
        <tr>
          <td style="border: 1px solid #dddddd; padding: 8px;">Space Complexity</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Đánh giá bộ nhớ O(...)</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Đánh giá bộ nhớ O(...)</td>
        </tr>
        <tr>
          <td style="border: 1px solid #dddddd; padding: 8px;">Maintainability</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Mức độ dễ bảo trì</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Mức độ dễ bảo trì</td>
        </tr>
        <tr>
          <td style="border: 1px solid #dddddd; padding: 8px;">Readability</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Độ trong sáng mã nguồn</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Độ trong sáng mã nguồn</td>
        </tr>
        <tr>
          <td style="border: 1px solid #dddddd; padding: 8px;">Suitability</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Độ phù hợp với bài học</td>
          <td style="border: 1px solid #dddddd; padding: 8px;">Độ phù hợp với bài học</td>
        </tr>
      </tbody>
    </table>

#### **2. Giải trình Lựa chọn và Mã giả thiết kế — 20 điểm**
*   **[10 điểm] Lý giải logic khoa học cho lựa chọn:** Giải thích lập luận rõ ràng tại sao chọn phương án tối ưu dựa trên bài toán thao tác danh sách nhỏ trong bộ nhớ ca trực GrabRide.
*   **[10 điểm] Viết mã giả/Lưu đồ luồng tối ưu:** Sử dụng chuẩn syntax Mermaid Flowchart với các hình dạng chuẩn:
    *   Terminal: `([Bắt đầu quy trình])`, `([Kết thúc quy trình])`
    *   Input/Output: `[/In kết quả ra màn hình/]`
    *   Process: `["Cập nhật trip_fares[2] = 60000"]`, `["Xóa del trip_fares[1]"]`
    *   Decision: `Kiểm tra index 1 và index 2 hợp lệ?`

#### **3. Triển khai mã nguồn logic nghiệp vụ — 30 điểm**
*   **[15 điểm] Hiện thực hóa phương án tối ưu bằng code:** Đưa ra mã nguồn Python 3.12 thực thi chính xác việc cập nhật phần tử index 2 và xóa phần tử index 1. Tuyệt đối không dùng `append`, `pop`, `remove`, `def`, `class`, `dict`, `set`, `tuple`.
*   **[15 điểm] Chặn các lỗi logic biên nghiệp vụ:** Có câu lệnh kiểm tra độ dài danh sách bằng `len()` trước khi thao tác chỉ số (Index Out of Bounds validation), tránh tình trạng chương trình bị crash khi danh sách không đủ phần tử.

#### **4. Kiểm chuẩn dữ liệu và Định dạng Đầu ra — 10 điểm**
*   **[10 điểm] Trả về chuẩn cấu trúc dữ liệu:** In đầy đủ 3 thông tin theo chuẩn:
    1. Danh sách chuyến xe ban đầu.
    2. Danh sách chuyến xe sau khi cập nhật và xóa.
    3. Tổng số chuyến xe còn lại trong ca trực.

#### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
*   **[5 điểm] Đặt tên biến và Clean Code:** Tên biến tiếng Anh rõ ràng (ví dụ `trip_fares: list[int]`, `remaining_trips: int`), tuân thủ PEP 8, comment chú thích logic bằng tiếng Việt có dấu.
*   **[5 điểm] Nộp bài GitHub:** Đường dẫn repository hợp lệ theo cấu trúc `[Tên Lớp]_[Môn Học]_Session10_Ex11`.

#### **Điểm cộng khuyến khích (Bonus) — 10 điểm**
*   **[10 điểm] Viết Benchmark Script:** Viết đoạn mã kịch bản đo đạc thời gian thực thi (dùng thư viện `time`) so sánh hiệu năng của 2 phương án trên một danh sách mô phỏng lớn mà không dùng kiến thức cấm.
