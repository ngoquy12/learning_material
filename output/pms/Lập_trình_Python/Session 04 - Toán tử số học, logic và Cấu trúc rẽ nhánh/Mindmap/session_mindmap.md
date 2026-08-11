```markmap
# Toán tử và Cấu trúc rẽ nhánh

## Mục tiêu bài học
- Sử dụng thành thạo các toán tử số học và toán tử logic trong Python
- Làm chủ cấu trúc rẽ nhánh if-elif-else để điều khiển luồng chương trình
- Tối ưu rẽ nhánh lồng nhau bằng kỹ thuật phẳng hóa điều kiện
- Áp dụng chuẩn quy tắc mã nguồn PEP 8 tránh lỗi Arrow Anti-Pattern

## Đặt tình huống
- Xây dựng hệ thống tự động xét duyệt hồ sơ vay tín dụng ngân hàng
- Bài toán: Kiểm tra điều kiện về tuổi (18-65), thu nhập (>=15tr) và điểm tín dụng (>=650)
- Thách thức: Viết mã nguồn lồng nhau quá sâu làm code rối rắm và khó bảo trì

## Toán tử số học và logic
### Toán tử số học
- Tính toán dữ liệu số: +, -, *, /, // (chia nguyên), % (chia dư), ** (lũy thừa)
```python
total_score = (math_mark * 2 + english_mark) % 10
```
### Toán tử logic
- Kết hợp nhiều điều kiện: and (đồng thời đúng), or (một trong hai đúng), not (đảo ngược)
```python
is_eligible = (age >= 18) and (income >= 15 or credit_score >= 650)
```
### Thứ tự ưu tiên
- Ưu tiên thực hiện: Ngoặc () -> Số học -> So sánh (==, !=, >) -> Logic (not -> and -> or)

## Cấu trúc rẽ nhánh if-elif-else
### Cú pháp cơ bản
- Đánh giá điều kiện Boolean để quyết định khối lệnh được thực thi
```python
if score >= 90:
    grade = "Xuat sac"
elif score >= 75:
    grade = "Gioi"
else:
    grade = "Kha"
```
### Cơ chế thực thi
- Luồng chạy từ trên xuống, dừng lại ngay khi gặp điều kiện đầu tiên thỏa mãn

## Rẽ nhánh lồng nhau và Chuẩn PEP 8
### Arrow Anti-Pattern
- Lồng quá nhiều khối if lồng nhau làm mã nguồn thụt lề dạng mũi tên sâu
### Phẳng hóa điều kiện
- Gom nhóm điều kiện logic bằng and/or giúp giảm độ phức tạp mã nguồn
```python
if age < 18 or age > 65:
    print("Tu choi: Do tuoi khong phu hop")
elif income >= 15 and credit_score >= 650:
    print("Phe duyet: Du dieu kien vay")
```
### Minh họa trực quan
![](../images/mindmap_img_1.png)
### Quy chuẩn PEP 8
- Thụt lề chính xác 4 khoảng trắng (Spaces) cho mỗi cấp độ lồng nhau
- Thêm khoảng trắng quanh toán tử: age >= 18 thay vì age>=18
```