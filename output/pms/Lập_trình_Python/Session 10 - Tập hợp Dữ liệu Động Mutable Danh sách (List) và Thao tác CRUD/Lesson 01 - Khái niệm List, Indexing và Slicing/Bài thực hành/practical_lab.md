# Bài thực hành: Xử lý và Phân tích Nhật ký Đơn hàng E-commerce bằng List, Indexing và Slicing

## 1. Mục tiêu bài học
- Vận dụng kiến thức Python về kiểu dữ liệu List để khởi tạo và quản lý chuỗi dữ liệu nhật ký giao dịch thương mại điện tử.
- Thành thạo kỹ thuật truy cập Indexing với chỉ số dương và chỉ số âm để lấy thông tin đơn hàng cụ thể, đồng thời phân biệt chính xác kiểu dữ liệu trả về giữa Indexing và Slicing.
- Sử dụng thành thạo kỹ thuật cắt lát Slicing (start:stop:step) để đảo ngược danh sách và xử lý bài toán phân trang tĩnh (Pagination) cho Dashboard quản trị.
- Rèn luyện kỹ năng kiểm tra độ dài danh sách (len()) nhằm phòng tránh lỗi IndexError phổ biến trong môi trường sản xuất.

## 2. Yêu cầu bài toán
Bạn được giao nhiệm vụ phát triển module xử lý dữ liệu cho hệ thống Dashboard quản trị thương mại điện tử. Hệ thống nhận danh sách nhật ký đơn hàng dạng chuỗi và danh sách giá trị doanh thu tương ứng theo thứ tự thời gian phát sinh.

Yêu cầu nghiệp vụ:
1. Khởi tạo danh sách order_logs gồm 6 trạng thái giao dịch và order_amounts chứa 6 giá trị tương ứng (đơn vị: VNĐ).
2. Truy vấn đơn hàng đầu tiên (chỉ số dương) và đơn hàng mới nhất (chỉ số âm). Lấy doanh thu của đơn hàng đầu tiên bằng Indexing để cộng thêm phí dịch vụ 20,000 VNĐ.
3. Trích xuất danh sách Top 3 đơn hàng sớm nhất bằng Slicing (lưu ý quy tắc loại trừ cận trên 'stop').
4. Đảo ngược danh sách nhật ký giao dịch sử dụng bước nhảy step = -1 để hiển thị đơn hàng mới nhất lên đầu danh sách.
5. Lập trình tính năng phân trang tĩnh: Trích xuất dữ liệu hiển thị cho Trang 2 với quy mô 2 phần tử/trang.
6. Kiểm tra an toàn chỉ số trước truy cập để tránh lỗi hỏng chương trình (IndexError).

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường thực thi Python 3.x và tệp mã nguồn python đặt tên là `ecommerce_logs.py`.

### Các bước thực hiện:
1. Bước 1: Khởi tạo danh sách order_logs và order_amounts chứa dữ liệu 6 giao dịch mẫu.
2. Bước 2: Sử dụng Indexing chỉ số 0 để lấy đơn hàng đầu tiên và chỉ số -1 để lấy đơn hàng mới nhất. Tính tổng doanh thu đơn đầu tiên với phụ phí.
3. Bước 3: Thực hiện cắt lát Slicing [0:3] để trích xuất Top 3 đơn hàng đầu tiên và Slicing [::-1] để thu được danh sách đảo ngược thứ tự thời gian.
4. Bước 4: Tính toán vị trí start và stop theo công thức phân trang, thực hiện cắt lát [start:stop] để thu được dữ liệu hiển thị cho Trang 2.
5. Bước 5: Thêm đoạn mã kiểm tra độ dài danh sách bằng len() trước khi truy cập chỉ số vượt ngưỡng để minh họa việc phòng ngừa lỗi IndexError.

## 4. Mã nguồn tham khảo (Code Demo)

```text
# ========================================== 
# THỰC HÀNH: XỬ LÝ NHẬT KÝ ĐƠN HÀNG E-COMMERCE
# ========================================== 

# Bước 1: Khởi tạo danh sách nhật ký đơn hàng và giá trị doanh thu
order_logs = [
    "Đơn #101: Đã thanh toán",
    "Đơn #102: Đang vận chuyển",
    "Đơn #103: Đã hoàn tiền",
    "Đơn #104: Đã thanh toán",
    "Đơn #105: Đã giao hàng",
    "Đơn #106: Chờ xử lý"
]

order_amounts = [150000, 320000, 500000, 120000, 450000, 210000]

# Bước 2: Truy cập phần tử bằng Indexing (Dương & Âm)
first_order = order_logs[0]
latest_order = order_logs[-1]

# Truy cập doanh thu đơn đầu tiên bằng Indexing (kết quả trả về kiểu int)
first_amount = order_amounts[0]
service_fee = 20000
total_first_order = first_amount + service_fee

print("=== BÁO CÁO ĐƠN HÀNG ĐƠN LẺ ===")
print("Đơn hàng đầu tiên (Chỉ số 0):", first_order)
print("Đơn hàng mới nhất (Chỉ số -1):", latest_order)
print("Tổng giá trị đơn đầu tiên (+ Phụ phí):", total_first_order, "VNĐ\n")

# Bước 3: Trích xuất và đảo ngược dữ liệu bằng Slicing
# 3.1. Top 3 đơn hàng đầu tiên (lấy chỉ số 0, 1, 2 -> stop = 3)
top_3_orders = order_logs[0:3]

# 3.2. Đảo ngược danh sách nhật ký (mới nhất lên đầu)
reversed_logs = order_logs[::-1]

# 3.3. Phân trang tĩnh cho Trang 2 (kích thước mỗi trang: 2 phần tử)
items_per_page = 2
page_number = 2
start_index = (page_number - 1) * items_per_page  # 2
stop_index = start_index + items_per_page          # 4
page_2_logs = order_logs[start_index:stop_index]

print("=== BÁO CÁO DANH SÁCH & SLICING ===")
print("Top 3 đơn hàng khởi tạo sớm nhất:", top_3_orders)
print("Nhật ký xem từ mới nhất tới cũ nhất:", reversed_logs)
print("Dữ liệu hiển thị tại Trang 2:", page_2_logs)
print("")

# Bước 4: Kiểm tra và xử lý an toàn lỗi IndexError
target_index = 6
print("=== KIỂM TRA AN TOÀN CHỈ SỐ ===")
if target_index < len(order_logs):
    print(f"Đơn hàng tại chỉ số {target_index}:", order_logs[target_index])
else:
    print(f"Cảnh báo: Chỉ số {target_index} vượt quá giới hạn danh sách (Độ dài tối đa: {len(order_logs)})")
```

## 5. Checklist đánh giá kết quả
- [ ] Khởi tạo đúng cấu trúc danh sách order_logs và order_amounts theo yêu cầu bài toán.
- [ ] Sử dụng đúng chỉ số 0 và -1 để lấy chính xác dữ liệu phần tử đầu tiên và cuối cùng.
- [ ] Thực hiện phép tính toán số học trên phần tử lấy từ Indexing mà không gặp lỗi TypeError (phân biệt đúng giữa Indexing và Slicing).
- [ ] Sử dụng đúng cú pháp Slicing [0:3] lấy trọn vẹn 3 phần tử đầu tiên và [::-1] để đảo ngược danh sách.
- [ ] Tính toán chính sở bộ chỉ số start, stop và cắt lát đúng 2 phần tử của Trang 2.
- [ ] Chương trình chạy thành công, không phát sinh lỗi IndexError hay lỗi cú pháp Python.