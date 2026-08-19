### Tiêu chuẩn Đánh giá & Thang điểm (100đ)

| Tiêu chí | Điểm tối đa | Mô tả chi tiết |
| :--- | :--- | :--- |
| **1. Cấu trúc Module & Phong cách mã nguồn** | **20đ** | - Thiết kế module `GrabFareApp` rõ ràng, tách biệt logic tính toán và logic thao tác DOM (10đ).<br>- Định dạng code chuẩn JavaScript (CamelCase, thụt lề, comment giải thích đầy đủ) (10đ). |
| **2. Logic Nghiệp vụ Tính toán Cước phí** | **30đ** | - Tính đúng Cước cơ bản (2km đầu 12k, km tiếp theo 4.5k/km) (10đ).<br>- Tính đúng Phụ phí thời tiết/cao điểm (hệ số 1.2x) (10đ).<br>- Áp dụng chính xác quy tắc của các mã giảm giá `GRABNEW`, `XEMAY10` (10đ). |
| **3. Thao tác DOM API & Cập nhật Giao diện** | **30đ** | - Truy xuất chính xác các phần tử DOM qua ID/Class theo yêu cầu (10đ).<br>- Cập nhật nội dung văn bản (`textContent`) và định dạng tiền tệ Việt Nam (`toLocaleString`) chuẩn xác (10đ).<br>- Thao tác thuộc tính linh hoạt (`setAttribute` cho ảnh đại diện, `classList` cho Badge trạng thái) (10đ). |
| **4. Xử lý Biên & Ngoại lệ (Edge Cases)** | **20đ** | - Hiển thị lỗi rõ ràng khi dữ liệu khoảng cách không hợp lệ ($D \le 0$) qua `#alert-box` và ẩn bảng tính tiền (10đ).<br>- Xử lý an toàn khi mã giảm giá không tồn tại hoặc giảm giá vượt quá tổng tiền (10đ). |
| **Tổng điểm** | **100đ** | **Đạt yêu cầu tối thiểu: 70/100 điểm.** |