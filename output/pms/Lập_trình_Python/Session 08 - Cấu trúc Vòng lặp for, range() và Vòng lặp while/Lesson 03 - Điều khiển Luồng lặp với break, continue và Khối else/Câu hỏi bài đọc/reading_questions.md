# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ quét an ninh kiện hàng WMS bằng chuỗi ký tự được trích dẫn từ bài thực hành:

```python

# Chuỗi đại diện cho chuỗi kiện hàng chạy qua đầu quét an ninh:

# 'N': Kiện hàng thường (NORMAL)

# 'P': Hàng khuyến mãi tặng kèm (PROMO_ONLY)

# 'E': Lỗi an ninh nghiêm trọng (CRITICAL_ERROR)
package_sequence = "NPNEN"
package_count = 0

for package in package_sequence:
    package_count += 1
    print(f"Quét kiện hàng #{package_count}: {package}")

# Kiểm tra lỗi an ninh nghiêm trọng (Ký tự 'E')
    if package == 'E':
        print("--> CẢNH BÁO: Dừng băng tải khẩn cấp!")
        break

# Kiểm tra hàng khuyến mãi miễn kiểm thuế (Ký tự 'P')
    if package == 'P':
        print("--> Hệ thống: Miễn kiểm thuế, chuyển thẳng khu đóng gói.")
        continue

# Quy trình đóng gói mặc định (Ký tự 'N')
    print("--> Hệ thống: Đóng gói thành công.")

print("\n🎉 THÔNG BÁO: Kết thúc ca làm việc quét kiện hàng!")
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X): Khi thực thi đoạn mã trên với chuỗi `package_sequence = "NPNEN"`, hệ thống sẽ in ra màn hình những dòng thông báo cụ thể nào và dừng lại ở kiện hàng số mấy?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Vòng lặp duyệt qua từng ký tự của chuỗi `"NPNEN"`:
>   - Vòng 1 (`package = 'N'`): `package_count` tăng lên 1. In thông báo quét kiện #1, in `"Đóng gói thành công."`.
>   - Vòng 2 (`package = 'P'`): `package_count` tăng lên 2. In thông báo quét kiện #2, in `"Miễn kiểm thuế..."`, gọi lệnh `continue` để bỏ qua lệnh đóng gói phía dưới và chuyển sang lượt lặp tiếp theo.
>   - Vòng 3 (`package = 'N'`): `package_count` tăng lên 3. In thông báo quét kiện #3, in `"Đóng gói thành công."`.
>   - Vòng 4 (`package = 'E'`): `package_count` tăng lên 4. In thông báo quét kiện #4, kích hoạt điều kiện dừng, in `"CẢNH BÁO: Dừng băng tải khẩn cấp!"`, gọi lệnh `break` ngắt vòng lặp lập tức.
> - Vòng lặp dừng lại hoàn toàn ở kiện hàng thứ `4` (không xử lý ký tự `'N'` cuối cùng) và không chạy dòng thông báo cuối cùng do lệnh break ngắt ngang.

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y): Nếu thay đổi chuỗi đầu vào thành `package_sequence = "NPNPN"` (không chứa ký tự `E`), kết quả hiển thị trên màn hình console sẽ thay đổi ra sao và dòng thông báo cuối cùng có được thực thi hay không?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Hệ thống sẽ duyệt qua lần lượt cả 5 ký tự trong chuỗi `"NPNPN"`.
> - Do không có ký tự `'E'`, điều kiện lỗi không bao giờ được thỏa mãn, vòng lặp không bị ngắt quãng bởi câu lệnh `break` nào.
> - Khi hoàn thành tất cả 5 lượt lặp, chương trình chạy tiếp câu lệnh phía dưới vòng lặp để in ra dòng chữ: `"\n🎉 THÔNG BÁO: Kết thúc ca làm việc quét kiện hàng!"`.

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z): Giả sử kết quả chạy chương trình in ra thông báo an ninh dừng khẩn cấp ở kiện hàng số 3, điều này cho ta biết gì về cấu tạo ký tự của chuỗi `package_sequence` đầu vào?
> **Gợi ý trả lời & Định hướng đáp án:**
> - Lệnh dừng khẩn cấp bằng `break` diễn ra ở lượt lặp thứ 3 (`package_count = 3`) có nghĩa là:
>   - Hai ký tự đầu tiên của chuỗi `package_sequence` không chứa ký tự `'E'` (chúng là `'N'` hoặc `'P'`).
>   - Ký tự thứ ba của chuỗi `package_sequence` chính xác là ký tự lỗi `'E'`.

---

### Câu 4 (Phân tích lỗi thường gặp & Trường hợp biên): Một lập trình viên viết nhầm câu lệnh `continue` thành `break` tại vị trí kiểm tra ký tự khuyến mãi `P`. Hãy phân tích lỗi nghiệp vụ nghiêm trọng xảy ra đối với băng chuyền kho hàng từ sai sót này.
> **Gợi ý trả lời & Định hướng đáp án:**
> - Ký tự `'P'` đại diện cho hàng khuyến mãi bình thường, chỉ cần bỏ qua khâu đóng gói riêng (dùng `continue`).
> - Nếu nhầm thành `break`: khi gặp ký tự `'P'` đầu tiên (ví dụ ở lượt quét số 2), vòng lặp sẽ bị dừng hoàn toàn ngay lập tức.
> - Băng chuyền dừng đột ngột ngoài ý muốn và toàn bộ các kiện hàng phía sau không được xử lý, gây tắc nghẽn hoạt động của toàn bộ kho hàng.
