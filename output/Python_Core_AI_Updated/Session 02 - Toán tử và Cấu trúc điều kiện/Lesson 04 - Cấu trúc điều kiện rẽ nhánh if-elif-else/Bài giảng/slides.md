---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 02 - Lesson 04
## Cấu trúc điều kiện rẽ nhánh if-elif-else

---

### Đặt vấn đề

* Khi phát triển phần mềm, chương trình cần đưa ra quyết định thông minh dựa trên dữ liệu thực tế.
* Thay vì chỉ thực thi các dòng lệnh tuần tự từ trên xuống dưới, chương trình cần có khả năng rẽ nhánh.
* Việc phân loại dữ liệu đầu vào (như điểm số, chỉ số sức khỏe, độ tuổi...) đòi hỏi một cơ chế điều hướng dòng điều khiển linh hoạt.

---

### Dòng điều khiển (Control Flow) và if-else

* **Dòng điều khiển**: Trình tự các câu lệnh được thực thi trong một chương trình.
* **Cấu trúc điều khiển**: Cho phép chương trình đưa ra quyết định thực thi các đoạn mã khác nhau dựa trên kết quả biểu thức điều kiện.
* **Biểu thức điều kiện**: Một biểu thức logic trả về giá trị kiểu Boolean (`True` hoặc `False`), được xây dựng từ các biến, giá trị, toán tử so sánh (như `==`, `!=`, `>`, `<`) và toán tử logic.

---

### Demo: Kiểm tra chẵn/lẻ cơ bản

```python
# Bài học 1: Kiểm tra một số nguyên là chẵn hay lẻ
so_nguyen = 14
if so_nguyen % 2 == 0:
    print('Day la so chan')
else:
    print('Day la so le')
```

---

### Cấu trúc rẽ nhánh nhiều trường hợp `if-elif-else`

* **Cơ chế đánh giá**: Trình thông dịch sẽ đánh giá biểu thức điều kiện tuần tự từ trên xuống dưới.
* **Nguyên tắc ngắt**: Ngay khi một nhánh điều kiện đúng (`True`), khối lệnh tương ứng sẽ chạy và toàn bộ cấu trúc điều kiện phía sau sẽ bị bỏ qua.
* **Nhánh else cuối cùng**: Đóng vai trò là phương án bổ trợ cuối cùng khi tất cả các điều kiện phía trên đều trả về `False`.

---

### Toán tử logic kết hợp

Để xây dựng các điều kiện phức tạp hơn, ta kết hợp các toán tử logic:
* **`and` (Đồng thời)**: Chỉ trả về `True` nếu tất cả điều kiện đều đúng.
* **`or` (Hoặc)**: Trả về `True` nếu có ít nhất một điều kiện đúng.
* **`not` (Phủ định)**: Đảo ngược trạng thái logic của biểu thức.

---

### Demo: Phân loại giá vé với Toán tử Logic

```python
# Bài học 2: Phân loại giá vé dựa trên tuổi và trạng thái thẻ ưu tiên
tuoi = 20
co_the_thanh_vien = True

if tuoi < 12:
    print('Gia ve tre em: Mien phi')
elif tuoi >= 18 and co_the_thanh_vien:
    print('Gia ve thanh vien nguoi lon: Giảm 20%')
elif tuoi >= 18 and not co_the_thanh_vien:
    print('Gia ve nguoi lon tieu chuan: Gia goc')
else:
    print('Gia ve hoc sinh: Giam 10%')
```

---

### Lỗi logic điều kiện không thể thực thi (Unreachable Code)

* **Hiện tượng**: Xảy ra khi một điều kiện ở nhánh dưới bị bao trùm hoàn toàn bởi một điều kiện bao quát hơn ở nhánh trên.
* **Hậu quả**: Đoạn mã ở nhánh dưới không bao giờ có thể chạy được (Unreachable Code).
* **Giải pháp**: Sắp xếp thứ tự kiểm tra từ điều kiện nghiêm ngặt/cụ thể nhất hoặc có phạm vi thu hẹp nhất lên trên cùng.

---

### Demo: Phát hiện và sửa lỗi Unreachable Code

```python
# LOI LOGIC: Diem 9.5 se roi vao diem >= 5.0 va in sai phan loai
diem = 9.5
if diem >= 5.0:
    print('Chua toi uu: Khen thuong Trung binh (Loi vi >= 5.0 chan truoc >= 8.0)')
elif diem >= 8.0:
    print('Chua toi uu: Khen thuong Gioi')

# KHAC PHUC: Sap xep thu tu kiem tra tu dieu kien nghiem ngat nhat thap dan
if diem >= 8.0:
    print('Toi uu: Dat loai Gioi')
elif diem >= 5.0:
    print('Toi uu: Dat loai Trung binh')
else:
    print('Toi uu: Dat loai Yeu')
```

---

### Tối ưu hóa thứ tự nhánh điều kiện

* **Kỹ thuật**: Sắp xếp các nhánh điều kiện sao cho các trường hợp mang tính cụ thể cao được kiểm tra trước.
* **Ưu điểm**: Giúp mã nguồn tối giản phép toán (ví dụ: tận dụng chuỗi tăng/giảm dần để không cần dùng toán tử logic ghép `and` thừa thãi).
* **Ứng dụng**: Phân loại các thông số động như chỉ số BMI, phân cấp ngân sách, tính thuế thu nhập doanh nghiệp.

---

### Demo: Ứng dụng phân loại chỉ số BMI tối ưu

```python
# Bài học 4: Ung dung phan loai BMI toi uu thu tu cac nhanh dieu kien
chieu_cao_m = 1.70
can_nang_kg = 65.0

bmi = can_nang_kg / (chieu_cao_m ** 2)
print('Chi so BMI tinh duoc:', round(bmi, 2))

# Sap xep dieu kien tang dan giup code ngan gon va toi uu phep so sanh
if bmi < 18.5:
    print('Ket qua: Thieu can. Khuyen nghi: Can bo sung dinh duong.')
elif bmi < 25.0:
    print('Ket qua: Binh thuong. Khuyen nghi: Duy tri che do an hien tai.')
elif bmi < 30.0:
    print('Ket qua: Thua can. Khuyen nghi: Tang cuong tap the duc.')
else:
    print('Ket qua: Beo phi. Khuyen nghi: Han che chat beo va duong.')
```

---

### Tổng kết và Lỗi thường gặp

* Cấu trúc rẽ nhánh điều khiển dòng chạy của ứng dụng dựa trên kết quả Boolean.
* **3 lỗi cơ bản cần ghi nhớ để phòng tránh**:
  * **Cố ý hoặc quên dấu hai chấm** `:` ở cuối dòng chứa điều kiện (`SyntaxError`).
  * **Thụt lề không đồng nhất** (Indentation) trong các khối lệnh (`IndentationError`).
  * **Sắp xếp sai thứ tự điều kiện** dẫn đến các dòng mã nguồn không thể chạm tới (`Unreachable Code`).