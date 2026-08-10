# Bài thực hành: Xây dựng hệ thống xét duyệt tín dụng tự động và tái cấu trúc mã nguồn theo chuẩn PEP 8

## 1. Mục tiêu
- Vận dụng cấu trúc rẽ nhánh lồng nhau (nested if-else) và các toán tử logic (and, or, not) trong Python để giải quyết bài toán xét duyệt tín dụng đa điều kiện.
- Tối ưu hóa và làm phẳng các điều kiện rẽ nhánh phức tạp nhằm nâng cao tính dễ đọc, dễ bảo trì của chương trình.
- Áp dụng chuẩn định dạng mã nguồn PEP 8 vào bài làm bao gồm thụt lề 4 khoảng trắng, đặt tên biến theo chuẩn snake_case và quy chuẩn khoảng trắng quanh toán tử.

## 2. Mô tả & Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển Python 3.x (như VS Code hoặc PyCharm) cùng tệp mã nguồn mẫu `credit_approval.py` chứa danh sách dữ liệu kiểm thử.

### Các bước thực hiện:
1. Bước 1: Khởi tạo không gian làm việc với tệp `credit_approval.py` và khai báo các biến đại diện cho hồ sơ vay gồm: age (tuổi), monthly_income (thu nhập hàng tháng), credit_score (điểm tín dụng) và has_bad_debt (trạng thái nợ xấu).
2. Bước 2: Xây dựng thuật toán xét duyệt ban đầu bằng cấu trúc rẽ nhánh lồng nhau nhiều cấp để phân loại các mức tín dụng (Phê duyệt, Cần xem xét thêm, Từ chối) dựa trên các tiêu chí nghiệp vụ.
3. Bước 3: Tiến hành tái cấu trúc (refactor) mã nguồn: gộp các điều kiện lồng nhau thành điều kiện phẳng bằng toán tử logic (and, or) và áp dụng kỹ thuật guard clauses để giảm độ sâu của các khối lệnh.
4. Bước 4: Thực hiện chuẩn hóa mã nguồn theo quy chuẩn PEP 8 (sử dụng 4 khoảng trắng cho mỗi cấp thụt lề, khoảng trắng hợp lý quanh toán tử so sánh, giới hạn độ dài dòng) và chạy kiểm thử với các tập dữ liệu biên để xác nhận kết quả.

## 3. Checklist đánh giá
- [ ] Chương trình thực thi thành công và trả về kết quả xét duyệt chính xác tương ứng với từng tập dữ liệu đầu vào.
- [ ] Cấu trúc rẽ nhánh được đơn giản hóa hiệu quả, làm phẳng các khối lệnh lồng nhau phức tạp bằng toán tử logic.
- [ ] Mã nguồn tuân thủ đầy đủ quy chuẩn PEP 8 về đặt tên biến snake_case, thụt lề 4 khoảng trắng và định dạng khoảng trắng quanh toán tử.