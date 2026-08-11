### **Tiêu chí chấm điểm (AI)**
**Tính Phí Vận Chuyển và Xử Lý Logic Đơn Hàng Logistics — Tổng điểm: 100 điểm**

#### **1. Thiết lập & Khởi tạo (10 điểm)**
- **10 điểm**: Khởi tạo file `logistics_calculator.py` đúng cấu trúc script Python 3.12. Thực hiện nhập dữ liệu từ console (`input()`) và ép kiểu đúng 100% cho 6 biến đầu vào (`trong_luong`, `khoang_cach`, `loai_dich_vu`, `vung_giao_hang`, `hang_de_vo`, `gia_tri_hang`).
- **5 điểm**: Khởi tạo file và nhận input nhưng ép sai kiểu dữ liệu (ví dụ: quên ép kiểu `float` cho khoảng cách/trọng lượng).
- **0 điểm**: Không khởi tạo đúng file hoặc bị lỗi cú pháp không chạy được script.

#### **2. Logic nghiệp vụ (30 điểm)**
- **30 điểm**: Thực hiện chính xác toàn bộ logic tính toán chi tiết:
  + Phí cơ bản theo 3 nấc trọng lượng chính xác.
  + Phụ phí khoảng cách theo 3 nấc cự ly chính xác.
  + Hệ số dịch vụ (`STANDARD`: 1.0, `EXPRESS`: 1.4, `FAST_NEXT_DAY`: 1.8) và cước chính chính xác.
  + Phụ phí vùng địa lý (Vùng 1, 2, 3) và phụ phí hàng dễ vỡ (chọn `max(20000, 0.05 * phi_co_ban)`).
  + Phí bảo hiểm 1% khi giá trị hàng `> 3,000,000 VNĐ`.
  + Tổng chi phí vận chuyển được tính đúng bằng tổng tất cả các thành phần.
- **20 điểm**: Tính đúng các khoản phí cơ bản và khoảng cách nhưng tính sai hệ số dịch vụ hoặc thiếu logic phụ phí hàng dễ vỡ.
- **10 điểm**: Tính sai từ 3 công thức trở lên trong quy tắc nghiệp vụ.
- **0 điểm**: Tính sai toàn bộ tổng phí hoặc không có logic tính toán.

#### **3. Kiểm chuẩn dữ liệu & Xử lý ngoại lệ (30 điểm)**
- **30 điểm**: Xử lý triệt để kiểm chuẩn đầu vào và ràng buộc tuyến đường:
  + Bắt đúng tất cả điều kiện dữ liệu không hợp lệ (`trong_luong <= 0`, `khoang_cach <= 0`, `gia_tri_hang < 0`, mã vùng sai, gói dịch vụ sai tên) và dừng chương trình đúng lúc.
  + Bắt đúng điều kiện loại trừ dịch vụ: `vung_giao_hang == 3` và `loai_dich_vu == "FAST_NEXT_DAY"`.
- **20 điểm**: Kiểm tra được dữ liệu âm/bằng 0 nhưng bỏ sót việc kiểm tra tính hợp lệ của mã vùng hoặc tên loại dịch vụ.
- **10 điểm**: Bỏ sót logic kiểm tra loại trừ dịch vụ vùng 3 với `FAST_NEXT_DAY`.
- **0 điểm**: Không có kiểm chuẩn dữ liệu đầu vào.

#### **4. Tối ưu hoá hiệu suất (20 điểm)**
- **20 điểm**: Sử dụng cấu trúc rẽ nhánh `if-elif-else` tối ưu, ứng dụng hiệu quả cơ chế Short-circuit evaluation với các toán tử `and`/`or` để tránh thực hiện các phép so sánh thừa. Không lặp lại các điều kiện đã kiểm tra trước đó.
- **10 điểm**: Sử dụng quá nhiều câu lệnh `if` độc lập làm chương trình phải duyệt qua tất cả điều kiện dù đã khớp từ trước, hoặc lặp logic kiểm tra nhiều lần.
- **0 điểm**: Cấu trúc rẽ nhánh hỗn loạn, lồng ghép sai logic làm sai lệch thứ tự kiểm tra.

#### **5. Chất lượng mã nguồn (10 điểm)**
- **10 điểm**: Tuân thủ chuẩn PEP 8: đặt tên biến `snake_case` rõ nghĩa (ví dụ: `trong_luong`, `phi_co_ban`), thụt lề chuẩn 4 khoảng trắng, mã nguồn clean, có comment giải thích các khối điều kiện chính.
- **5 điểm**: Đặt tên biến viết tắt gây khó hiểu (ví dụ: `tl`, `kc`, `vgh`) hoặc thụt lề không đồng nhất.
- **0 điểm**: Vi phạm nặng chuẩn PEP 8, mã nguồn không có ghi chú.

#### **Điểm cộng (5-10 điểm)**
- **+5 điểm**: Định dạng chuỗi đầu ra đẹp mắt, sử dụng f-string với định dạng phân cách phần ngàn hoặc căn chỉnh cột bảng hóa đơn chuyên nghiệp.
- **+5 điểm**: Xử lý linh hoạt chuỗi đầu vào không phân biệt hoa thường cho `loai_dich_vu` và `hang_de_vo` (ví dụ: nhận cả `"express"`, `"y"`, `"N"` bằng cách dùng `.upper()`).