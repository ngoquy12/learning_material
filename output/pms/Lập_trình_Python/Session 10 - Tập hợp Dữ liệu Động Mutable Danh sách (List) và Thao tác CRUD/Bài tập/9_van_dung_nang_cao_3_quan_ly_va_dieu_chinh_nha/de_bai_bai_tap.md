# <center>[Vận dụng nâng cao 3] Quản lý và Điều chỉnh Nhật ký Cước phí Chuyến đi GrabRide</center>

### **1. Mục tiêu**
*   **Thao tác danh sách động nâng cao:** Vận dụng thành thạo kỹ thuật truy cập và cập nhật phần tử qua chỉ số (`list[index] = new_value`), xóa phần tử theo vị trí bằng lệnh `del`, và kiểm soát quy mô tập dữ liệu bằng `len()`.
*   **Tư duy phân tích & thiết kế luồng:** Đề xuất được cấu trúc dữ liệu lưu trữ cước phí ca làm việc, phân tích rõ ràng dữ liệu Input/Output và chuyển đổi quy tắc nghiệp vụ thực tế thành sơ đồ luồng (Mermaid Flowchart) chuẩn hóa.
*   **Xử lý sai sót biên & Kiểm soát an toàn chỉ số:** Xây dựng cơ chế kiểm tra tính hợp lệ của vị trí thao tác (chống lỗi `IndexError`) và ràng buộc giá trị cước phí/khoảng cách không hợp lệ trong môi trường Python 3.12 thuần.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống quản lý chuyến đi của ứng dụng đặt xe công nghệ **GrabRide**, sau mỗi ca làm việc, hệ thống tổng hợp một danh sách chứa cước phí tính toán ban đầu của từng chuyến đi mà tài xế đã thực hiện. Tuy nhiên, trong quá trình vận hành thực tế, dữ liệu này liên tục bị biến động do hai tình huống nghiệp vụ:
1.  **Điều chỉnh cước phí do phụ phí phát sinh:** Khách hàng di chuyển vào thời điểm trời mưa lớn hoặc giờ cao điểm, hoặc quãng đường thực tế bị sai lệch khiến cước phí của chuyến đi tại chỉ số `index` nhất định cần được tính toán lại và cập nhật trực tiếp vào danh sách.
2.  **Hủy chuyến đi gian lận / bị hủy ngang:** Chuyến đi bị hủy bởi khách hàng hoặc bị hệ thống đánh dấu gian lận cần bị loại bỏ hoàn toàn khỏi danh sách thu nhập ca làm việc bằng thao tác xóa tại vị trí `index`.

Hệ thống yêu cầu phát triển một mô-đun xử lý dữ liệu RAM trên tệp `main.py` để cập nhật, xóa và truy xuất chính xác số lượng chuyến đi hợp lệ còn lại cùng tổng doanh thu thực nhận của tài xế.

### **3. Quy tắc nghiệp vụ**
Hệ thống GrabRide áp dụng các quy tắc định giá và xử lý dữ liệu sau:

1.  **Quy tắc tính cước phí chuyến đi chuẩn (Trip Fare Rules):**
    *   **2 km đầu tiên ($\le 2.0$ km):** Cước phí cố định là **12.000 VNĐ**.
    *   **Từ km thứ 3 trở đi ($> 2.0$ km):** Mỗi km tiếp theo tính **4.500 VNĐ/km**.
        *   *Công thức cước chuẩn:* $Cước chuẩn = 12000 + (Quãng đường - 2.0) * 4500$
    *   **Phụ phí thời tiết / Giờ cao điểm:** Tổng cước phí được nhân hệ số **1.2x** (kết quả làm tròn về số nguyên float hoặc int).

2.  **Quy tắc Cập nhật & Xóa phần tử trên List:**
    *   **Cập nhật (Update):** Thay thế trực tiếp giá trị tại vị trí `index` bằng giá trị cước phí mới: `danh_sach_cuoc_phi[index] = cuoc_phi_moi`.
    *   **Xóa (Delete):** Loại bỏ phần tử khỏi danh sách tại vị trí `index` bằng câu lệnh `del danh_sach_cuoc_phi[index]`.
    *   **Đo độ dài:** Kiểm tra số lượng chuyến đi còn lại sau khi xóa bằng `len(danh_sach_cuoc_phi)`.

3.  **Ràng buộc kiểm soát an toàn (Edge Cases):**
    *   Vị trí `index` cần thao tác phải thỏa mãn điều kiện hợp lệ: $0 \le index < len(danh\_sach)$.
    *   Nếu `index` ngoài phạm vi (nhỏ hơn 0 hoặc lớn hơn/bằng độ dài danh sách), hệ thống không thực hiện thao tác và xuất cảnh báo lỗi.
    *   Khoảng cách km nhập vào phải $\ge 0.0$.

### **4. Yêu cầu bài toán**

#### **Phần 1 - Báo cáo Phân tích & Thiết kế Giải pháp (Bắt buộc trong báo cáo)**
1.  **Phân tích Đầu vào / Đầu ra (Input / Output):**
    *   Liệt kê rõ ràng danh sách đầu vào, chỉ số cần thao tác, cước phí/khoảng cách điều chỉnh và kiểu dữ liệu tương ứng trong Python.
2.  **Đề xuất Giải pháp Logic & Sơ đồ luồng (Mermaid Flowchart):**
    *   Trình bày các bước logic xử lý từ khởi tạo, kiểm tra điều kiện index, cập nhật phần tử, xóa phần tử và tính tổng thu nhập.
    *   Vẽ sơ đồ Mermaid Flowchart minh họa quy trình. Sơ đồ BẮT BUỘC tuân thủ 5 hình dạng chuẩn:
        *   `([Bắt đầu / Kết thúc])` (Hình Oval / Stadium).
        *   `[/Nhập / Xuất dữ liệu/]` (Hình bình hành - KHÔNG dùng cho bước tính toán).
        *   `["Thực hiện tính toán / Thao tác danh sách"]` (Hình chữ nhật).
        *   `Kiểm tra chỉ số index hợp lệ?` (Hình thoi).
        *   `-->` (Mũi tên luồng thực thi).

#### **Phần 2 - Triển khai Mã nguồn Python (tệp `main.py`)**
Viết chương trình Python 3.12 đáp ứng các kịch bản sau:
*   Khởi tạo danh sách cước phí ban đầu của ca làm việc (ví dụ: `[12000.0, 21000.0, 12000.0, 48000.0, 14250.0]`).
*   In danh sách ban đầu và số lượng chuyến đi bằng `len()`.
*   **Thực thi Thao tác Cập nhật:** Tiến hành tính lại và cập nhật cước phí cho chuyến đi tại `index = 1` do phát sinh phụ phí mưa lớn (nhân hệ số 1.2).
*   **Thực thi Thao tác Xóa:** Tiến hành xóa chuyến đi bị hủy tại `index = 2` bằng câu lệnh `del`.
*   **Thực thi Kiểm tra Biên:** Thử nghiệm thao tác xóa hoặc cập nhật tại chỉ số không hợp lệ (ví dụ: `index = 10`) và hiển thị thông báo lỗi phù hợp.
*   **Tổng hợp:** In danh sách cước phí hoàn chỉnh sau xử lý, số lượng chuyến đi còn lại và dùng vòng lặp `for` tính tổng doanh thu thu nhập của tài xế.

*[LƯU Ý NGHIÊM CẤM]: Không sử dụng các phương thức `append()`, `pop()`, `insert()`, `remove()`, không dùng Dictionary, Set, Tuple, không định nghĩa hàm `def` hay lớp `class`.*

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_SessionSession 10_Ex9`.
    Ví dụ: `HNKS25CNTT1_Core_Session_Session 10_Ex9`
