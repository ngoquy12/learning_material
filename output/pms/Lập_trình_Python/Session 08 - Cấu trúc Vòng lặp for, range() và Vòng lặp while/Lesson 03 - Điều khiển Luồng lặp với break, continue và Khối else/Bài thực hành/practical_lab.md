# Bài thực hành: Xây dựng hệ thống quét an ninh và phân loại kiện hàng tự động (WMS)

## 1. Mục tiêu bài học
- Thành thạo việc sử dụng từ khóa `break` để ngắt vòng lặp lập tức khi phát hiện điều kiện dừng khẩn cấp.
- Vận dụng linh hoạt từ khóa `continue` để bỏ qua lượt lặp hiện tại và chuyển nhanh sang chu kỳ kế tiếp.

## 2. Yêu cầu bài toán
Hệ thống Quản lý Kho hàng (WMS) cần lập trình mô-đun kiểm soát băng tải quét mã an ninh kiện hàng tự động.
Vì hệ thống chưa hỗ trợ mảng dữ liệu phức tạp, danh sách kiện hàng được biểu diễn dưới dạng một chuỗi ký tự (String) liên tiếp, trong đó:
- Ký tự `N` (`NORMAL`): Kiện hàng thường, cần quét mã, đóng gói và chuyển sang bộ phận vận chuyển.
- Ký tự `P` (`PROMO_ONLY`): Kiện hàng khuyến mãi tặng kèm, được miễn phí kiểm tra thuế, chỉ cần quét thông tin và bỏ qua bước đóng gói thông thường để đi thẳng tới khu đóng gói chung (sử dụng `continue`).
- Ký tự `E` (`CRITICAL_ERROR`): Phát hiện kiện hàng chứa lỗi an ninh nghiêm trọng. Hệ thống phải lập tức dừng băng tải và phát tín hiệu báo động khẩn cấp (sử dụng `break`).

Nếu toàn bộ chuỗi kiện hàng được xử lý an toàn không gặp lỗi an ninh nghiêm trọng nào, hệ thống sẽ sử dụng cờ hiệu trạng thái (boolean flag) để ghi nhận và in báo cáo tổng kết an toàn toàn bộ lô hàng sau khi kết thúc vòng lặp.

## 3. Các bước thực hiện
- **Tài nguyên đầu vào**: Môi trường phát triển python và tệp mã nguồn main.py.

### Các bước thực hiện:
1. **Bước 1**: Khởi tạo chuỗi kiện hàng chạy trên băng chuyền (ví dụ: `package_sequence = "NPNPN"`). Khởi tạo biến đếm `package_count = 0` và cờ trạng thái `all_safe = True`.
2. **Bước 2**: Sử dụng vòng lặp `for` duyệt qua từng ký tự trong chuỗi kiện hàng. Tại mỗi vòng lặp, tăng biến đếm `package_count` lên 1 đơn vị.
3. **Bước 3**: Viết điều kiện kiểm tra nếu gặp ký tự lỗi `E`, in cảnh báo dừng băng chuyền, đổi `all_safe = False` và gọi lệnh `break` thoát khỏi vòng lặp.
4. **Bước 4**: Viết điều kiện kiểm tra nếu gặp ký tự khuyến mãi `P`, in thông báo bỏ qua đóng gói và gọi lệnh `continue` để tiếp tục quét kiện hàng tiếp theo.
5. **Bước 5**: Viết khối lệnh xử lý mặc định cho loại hàng `N` (nằm ngoài các điều kiện `if` trên).
6. **Bước 6**: Sau vòng lặp, viết điều kiện kiểm tra cờ hiệu `all_safe`, nếu là `True` thì in ra thông báo hoàn tất quét lô hàng an toàn.
7. **Bước 7**: Chạy thử nghiệm với 2 kịch bản:
   - Kịch bản 1: Lô hàng an toàn (không chứa ký tự `E`).
   - Kịch bản 2: Lô hàng chứa lỗi (ví dụ chuỗi là `NPEPN`), kiểm tra xem băng chuyền có dừng lập tức tại kiện số 3 và thông báo an toàn có bị bỏ qua hay không.

## 4. Mã nguồn tham khảo (Code Demo)

```python

# Tệp mã nguồn: main.py

# Bài thực hành: Điều khiển Luồng lặp với break và continue

print("=== HỆ THỐNG QUÉT AN NINH VÀ PHÂN LOẠI HÀNG HOÁ WMS ===")

# Kịch bản 1: Lô hàng an toàn (Không có ký tự 'E')
package_sequence = "NPNPN"
package_count = 0
all_safe = True

print("Bắt đầu xử lý lô hàng...")
for package in package_sequence:
    package_count += 1
    print(f"\nQuét kiện hàng #{package_count}: Mã phân loại = {package}")

# 1. Kiểm tra lỗi an ninh nghiêm trọng
    if package == 'E':
        print("--> CẢNH BÁO: Phát hiện sự cố an ninh nghiêm trọng! Dừng băng tải khẩn cấp!")
        all_safe = False
        break

# 2. Kiểm tra hàng khuyến mãi miễn đóng gói riêng
    if package == 'P':
        print("--> Hệ thống: Kiện hàng tặng kèm, chuyển thẳng tới khu đóng gói chung.")
        continue

# 3. Quy trình đóng gói mặc định cho hàng thường
    print("--> Hệ thống: Đóng gói thành công, dán nhãn vận chuyển.")

if all_safe:
    print("\n🎉 THÔNG BÁO: Đã hoàn tất quét an toàn lô hàng! Không phát hiện sự cố.")

print("-" * 50)

# Kịch bản 2: Lô hàng có sự cố (Có ký tự 'E' ở vị trí thứ 3)
package_sequence_with_error = "NPEPN"
package_count = 0
all_safe_with_error = True

print("Bắt đầu xử lý lô hàng có sự cố...")
for package in package_sequence_with_error:
    package_count += 1
    print(f"\nQuét kiện hàng #{package_count}: Mã phân loại = {package}")
    
    if package == 'E':
        print("--> CẢNH BÁO: Phát hiện sự cố an ninh nghiêm trọng! Dừng băng tải khẩn cấp!")
        all_safe_with_error = False
        break
        
    if package == 'P':
        print("--> Hệ thống: Kiện hàng tặng kèm, chuyển thẳng tới khu đóng gói chung.")
        continue
        
    print("--> Hệ thống: Đóng gói thành công, dán nhãn vận chuyển.")

if all_safe_with_error:
    print("\n🎉 THÔNG BÁO: Đã hoàn tất quét an toàn lô hàng! Không phát hiện sự cố.")

print("\n=== QUY TRÌNH KẾT THÚC ===")
```

# 5. Checklist đánh giá kết quả
- [ ] Sử dụng đúng từ khóa `break` để ngắt luồng xử lý và dừng băng tải khi gặp ký tự lỗi `E`.
- [ ] Sử dụng đúng từ khóa `continue` để bỏ qua bước đóng gói đối với ký tự khuyến mãi `P` mà không dừng vòng lặp.
- [ ] Thiết lập đúng cờ hiệu trạng thái (boolean flag) để kiểm soát và chỉ in báo cáo tổng kết khi không phát hiện sự cố.
- [ ] Kiểm chứng mã nguồn hoạt động chính xác với cả 2 kịch bản chuỗi dữ liệu.
