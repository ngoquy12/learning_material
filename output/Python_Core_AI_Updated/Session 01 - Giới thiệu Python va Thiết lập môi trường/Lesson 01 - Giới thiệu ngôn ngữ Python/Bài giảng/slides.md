---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 01 - Lesson 01: Giới thiệu ngôn ngữ Python
**Giới thiệu nền tảng, cơ chế vận hành và triết lý lập trình**

---

## Đặt Vấn Đề

* **Bối cảnh lịch sử:** Python được sáng lập bởi Guido van Rossum năm 1991 nhằm hướng tới mục tiêu thiết kế tối giản, rõ ràng.
* **Thực trạng tiếp cận:** Lập trình viên thường bắt đầu viết mã ngay mà bỏ qua nguồn gốc lịch sử hoặc đặc tính vận hành nền tảng.
* **Hậu quả:** 
  * Thiết kế hệ thống sai lệch.
  * Dễ gặp lỗi Runtime khi phân tích kiểu hoặc tối ưu hóa hiệu năng ứng dụng do thiếu hiểu biết về hệ thống.

---

## Ngôn Ngữ Thông Dịch (Interpreted Language)

* **Cơ chế:** Mã nguồn được trình thông dịch (Python Interpreter) đọc và thực thi tuần tự từ trên xuống dưới tại thời điểm runtime.
* **Ưu điểm:** Tăng tốc độ phát triển, dễ dàng kiểm nghiệm và phát hiện lỗi tại từng dòng lệnh.
* **Demo thực thi tuần tự:**

```python
# Minh họa thực thi tuần tự từng dòng của trình thông dịch
print("Dong 1: Chuong trinh bat dau chay.")
print("Dong 2: Trinh thong dich dang doc va phan tich den day...")
# Trình thông dịch sẽ thực thi tuần tự từ trên xuống dưới và báo lỗi ngay tại dòng xảy ra lỗi runtime nếu có
```

---

## Sơ Đồ Vận Hành Trình Thông Dịch

Mô hình vận hành tối giản hóa của môi trường thực thi Python:

<div style="text-align: center; margin-top: 30px;">
  <svg viewBox="0 0 400 100" width="90%">
    <rect x="10" y="30" width="80" height="40" fill="#38BDF8" rx="5"/>
    <text x="50" y="55" fill="black" text-anchor="middle" font-size="12" font-weight="bold">Code .py</text>
    <path d="M 90 50 L 140 50" stroke="black" stroke-width="2" fill="none"/>
    <rect x="150" y="30" width="100" height="40" fill="#D97757" rx="5"/>
    <text x="200" y="55" fill="black" text-anchor="middle" font-size="12" font-weight="bold">Interpreter</text>
    <path d="M 250 50 L 300 50" stroke="black" stroke-width="2" fill="none"/>
    <rect x="310" y="30" width="80" height="40" fill="#F59E0B" rx="5"/>
    <text x="350" y="55" fill="black" text-anchor="middle" font-size="12" font-weight="bold">Output</text>
  </svg>
</div>

---

## Kiểu Dữ Liệu Động (Dynamic Typing)

* **Khái niệm:** Kiểu dữ liệu của biến được xác định tự động lúc runtime dựa trên giá trị gán, thay vì phải khai báo tĩnh trước.
* **Đặc tính:** Một biến có thể linh hoạt thay đổi kiểu dữ liệu trong suốt vòng đời hoạt động của nó.
* **Demo kiểu dữ liệu động:**

```python
# Ví dụ minh họa kiểu dữ liệu động trong Python
# Biến x ban đầu lưu trữ một số nguyên (int)
x = 10
print("Gia tri:", x, "| Kieu du lieu:", type(x))

# Biến x sau đó được gán một chuỗi văn bản (str)
x = "Xin chao Python"
print("Gia tri moi:", x, "| Kieu du lieu moi:", type(x))
```

---

## Triết Lý Thiết Kế (Zen of Python)

* **Mục tiêu:** Định hướng cách viết mã nguồn Python tối giản, dễ đọc và rõ ràng.
* **Một số châm ngôn tiêu biểu:**
  * "Đẹp đẽ tốt hơn xấu xí" (*Beautiful is better than ugly*).
  * "Đơn giản tốt hơn phức tạp" (*Simple is better than complex*).
* **Cách truy xuất:** Gọi trực tiếp qua câu lệnh trong môi trường tương tác:

```python
import this
```

---

## Ứng Dụng Đa Lĩnh Vực & Tự Động Hóa

* **Ứng dụng đa lĩnh vực:** Phổ biến từ Phát triển Web (phần backend) đến Khoa học dữ liệu, AI và các kịch bản Tự động hóa.
* **Tự động hóa (Automation/Scripting):** Viết các script ngắn để tự động hóa các tác vụ lặp đi lặp lại như chuẩn hóa dữ liệu, xử lý tệp tin.
* **Demo tự động hóa căn bản:**

```python
# Ví dụ tự động hóa: Chuẩn hóa tự động một danh sách file bị thừa khoảng trắng
danh_sach_file = [" bao_cao.txt ", "hinh_anh.PNG ", " tailieu.pdf"]
danh_sach_chuan_hoa = []

for file in danh_sach_file:
    # Tự động loại bỏ khoảng trắng thừa ở hai đầu và đưa về chữ thường
    file_sach = file.strip().lower()
    danh_sach_chuan_hoa.append(file_sach)

print("Danh sach ban dau:", danh_sach_file)
print("Danh sach da tu dong chuan hoa:", danh_sach_chuan_hoa)
```

---

## Tổng Kết & Lưu Ý Quan Trọng

* **Tóm tắt:** Python là ngôn ngữ thông dịch, có kiểu dữ liệu động, đề cao triết lý tối giản của Guido van Rossum.
* **3 sai lầm thường gặp cần tránh:**
  * **Nhầm lẫn kiểu dữ liệu** khi thực hiện tính toán lúc runtime.
  * **Lỗi thụt lề (`IndentationError`)** do không nhất quán trong việc sử dụng khoảng trắng/tab.
  * **Tự ý gán đè kiểu dữ liệu khác loại** làm ảnh hưởng đến các logic xử lý ở những module phía sau.