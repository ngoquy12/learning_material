## <center>[Phân tích 1] Thiết kế Module Phụ thu Check-in sớm và Phê duyệt Đặt phòng Khách sạn</center>

### **1. Mục tiêu**
*   **Tư duy phân tích nghiệp vụ:** Hiểu và áp dụng các phép toán số học và toán tử so sánh trong Python để tính toán phụ thu dịch vụ và phê duyệt đơn đặt phòng tự động cho hệ thống đặt phòng khách sạn (HOTEL_BOOKING).
*   **Phân tích đa giải pháp:** Tự đề xuất và đánh giá các phương án kỹ thuật xử lý logic nghiệp vụ mà không cần sử dụng câu lệnh rẽ nhánh (`if/else`) hay toán tử logic (`and/or/not`).
*   **Thiết kế & Đánh giá:** Xây dựng báo cáo so sánh đánh giá Trade-off giữa các phương án, thiết kế lưu đồ thuật toán (Flowchart) đạt chuẩn và triển khai mã nguồn Python 3.12 chuẩn hóa.

### **2. Bối cảnh & Vấn đề**
Trong hệ thống đặt phòng homestay và khách sạn trực tuyến (tương tự Agoda hoặc Traveloka), bộ phận vận hành đang triển khai tính năng **"Phê duyệt tức thì (Instant Confirmation)"** và **"Phụ thu Check-in sớm"**. 

Khi khách hàng thực hiện đặt phòng, hệ thống cần căn cứ vào giờ nhận phòng thực tế (`checkin_hour`) và số tiền cọc khách đã trả (`deposit_amount`) để tính toán:
1. Phụ thu nếu khách check-in trước 12:00 trưa.
2. Tổng tiền thanh toán dự kiến của đơn đặt phòng.
3. Số tiền còn lại khách phải thanh toán trực tiếp tại lễ tân khi nhận phòng.
4. Trạng thái đơn phòng có đủ điều kiện phê duyệt tự động ngay lập tức hay không.

Do hệ thống đang ở giai đoạn xây dựng lõi tính toán tốc độ cao (High-performance Core Engine), kiến trúc sư hệ thống yêu cầu xử lý toàn bộ logic trên chỉ bằng **toán tử số học** và **toán tử so sánh**, tuyệt đối chưa sử dụng cấu trúc rẽ nhánh phức tạp hay các thư viện ngoài.### **3. Quy tắc nghiệp vụ**
Cho trước các thông tin đầu vào của một giao dịch đặt phòng:
*   `base_price_per_night` (`float`): Giá niêm yết của 1 đêm lưu trú (VNĐ).
*   `nights` (`int`): Số đêm lưu trú.
*   `checkin_hour` (`int`): Giờ nhận phòng thực tế (từ `0` đến `23`).
*   `deposit_amount` (`float`): Số tiền cọc khách hàng đã thanh toán trước (VNĐ).

Các quy tắc tính toán nghiệp vụ áp dụng:
*   **Quy tắc 1 (Tiền phòng gốc):** `base_total` = `nights` * `base_price_per_night`.
*   **Quy tắc 2 (Phụ thu check-in sớm):** Nếu giờ nhận phòng trước 12h trưa (`checkin_hour < 12`), khách hàng bị tính phụ thu 30% (`0.30`) giá của 1 đêm lưu trú. Nếu giờ nhận phòng từ 12h trưa trở đi (`checkin_hour >= 12`), tiền phụ thu bằng `0`.
*   **Quy tắc 3 (Tổng chi phí lưu trú):** `grand_total` = `base_total` + tiền phụ thu check-in sớm.
*   **Quy tắc 4 (Tiền còn lại thanh toán tại lễ tân):** `remaining_balance` = `grand_total` - `deposit_amount`.
*   **Quy tắc 5 (Phê duyệt tự động - Instant Confirmation):** Đơn đặt phòng đạt trạng thái phê duyệt tự động (`is_instant_confirmed = True`) nếu và chỉ nếu số tiền cọc (`deposit_amount`) lớn hơn hoặc bằng 50% (`0.50`) tổng chi phí lưu trú (`grand_total`). Ngược lại, trả về `False`.

[REQUIREMENT] Giới hạn phạm vi kỹ thuật:
*   CHỈ ĐƯỢC SỬ DỤNG các toán tử số học (`+`, `-`, `*`, `/`, `//`, `%`, `**`) và toán tử so sánh (`==`, `!=`, `>`, `<`, `>=`, `<=`).
*   TUYỆT ĐỐI CẤM SỬ DỤNG: Cấu trúc rẽ nhánh (`if`, `elif`, `else`), toán tử logic (`and`, `or`, `not`), vòng lặp (`for`, `while`), danh sách (`list`), từ điển (`dict`), hàm tự định nghĩa hay các module bên ngoài.

### **4. Yêu cầu bài toán**

Học viên đóng vai trò Chuyên viên Phân tích & Triển khai Phần mềm (Software Engineer) thực hiện 3 phần nhiệm vụ sau:

#### **Phần 1: Báo cáo Đề xuất đa giải pháp & So sánh Trade-off**
*   Tự nghiên cứu và đề xuất ít nhất **02 phương án kỹ thuật khác nhau** để tính toán tiền phụ thu và xác định trạng thái `is_instant_confirmed` mà KHÔNG sử dụng câu lệnh `if/else` hay toán tử logic `and/or/not`. *(Gợi ý tư duy: Tận dụng tính chất biểu thức so sánh trả về giá trị Boolean `True`/`False` và khả năng tham gia vào phép tính số học của Boolean trong Python)*.
*   Lập **Bảng so sánh Trade-off** chi tiết giữa 2 phương án trên HTML table theo 5 tiêu chí bắt buộc:
    1. Hiệu năng thực thi (Execution Speed).
    2. Mức tiêu hao bộ nhớ (Memory Consumption).
    3. Khả năng bảo trì & Mở rộng (Maintainability & Extensibility).
    4. Độ dễ đọc của mã nguồn (Readability).
    5. Tính phù hợp với quy chuẩn dự án HOTEL_BOOKING.

#### **Phần 2: Lý giải lựa chọn & Thiết kế Lưu đồ luồng (Flowchart)**
*   Đưa ra lập luận kỹ thuật để chọn ra 01 phương án tối ưu nhất.
*   Vẽ lưu đồ thuật toán (Mermaid Flowchart) mô tả toàn bộ quá trình xử lý logic nghiệp vụ cho phương án đã chọn. Lưu đồ phải tuân thủ nghiêm ngặt 5 chuẩn hình dạng:
    - **Terminator** `([Bắt đầu / Kết thúc])`: Hình bo tròn (Stadium).
    - **Input/Output** `[/Nhập/Xuất dữ liệu/]`: Hình bình hành.
    - **Process** `["Tính toán / Thao tác"]`: Hình chữ nhật (TUYỆT ĐỐI KHÔNG dùng hình bình hành cho bước tính toán).
    - **Decision** `Kiểm tra điều kiện?`: Hình thoi với các nhánh `-->|Đúng|` và `-->|Sai|`.
    - **Flowline**: Mũi tên chỉ hướng luồng thực thi `-->`.

#### **Phần 3: Triển khai Mã nguồn Python (Python Implementation)**
*   Viết chương trình Python 3.12 hoàn chỉnh thực thi logic đã thiết kế.
*   Khai báo biến rõ ràng, có chú thích type hints chuẩn xác (`int`, `float`, `bool`).
*   In kết quả đầu ra trực quan ra màn hình Console với đầy đủ các thông tin: Tiền phòng gốc, Phụ thu check-in sớm, Tổng chi phí, Tiền còn lại phải trả tại lễ tân, và Trạng thái phê duyệt tự động.

### **5. Yêu cầu nộp bài**
Học viên cần nộp:
*   Phần phân tích/báo cáo và mã nguồn triển khai.
*   Đẩy mã nguồn lên GitHub theo định dạng thư mục: `[Tên Lớp]_[Môn Học]_Session04_Ex10`.
    Ví dụ: `HNKS25CNTT1_Core_Session04_Ex10`