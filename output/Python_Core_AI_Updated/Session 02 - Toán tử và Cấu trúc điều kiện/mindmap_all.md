```markmap
---
markmap:
  colorFreezeLevel: 3
---
# Session 02 - Toán tử và Cấu trúc điều kiện

## Mục tiêu bài học
- Hiểu và áp dụng thành thạo các toán tử số học cơ bản và nâng cao trong Python.
- Thực hiện đúng thứ tự ưu tiên của các phép toán để tránh sai sót logic.
- Nhận biết và xử lý các lỗi thường gặp như chia cho 0 hoặc lỗi kiểu dữ liệu từ input.
- Hiểu rõ chức năng của 6 toán tử so sánh cơ bản trong ngôn ngữ Python.
- Phân biệt chính xác bản chất của phép gán và phép so sánh bằng.
- Tạo lập các biểu thức logic thực tế và kiểm soát lỗi không tương thích kiểu dữ liệu.
- Hiểu rõ cách hoạt động của các toán tử logic and, or, not trong Python.
- Nắm vững thứ tự ưu tiên của toán tử và cơ chế đánh giá ngắn mạch.
- Biết cách tạo bảng chân trị tự động để kiểm tra logic code thực tế.
- Sử dụng cấu trúc rẽ nhánh điều kiện logic cơ bản với if, elif và else.
- Viết biểu thức so sánh và kết hợp chúng bằng toán tử logic để kiểm soát chương trình.
- Phát hiện và khắc phục các lỗi cú pháp về thụt lề và lỗi dòng điều khiển không thể thực thi.
- Hiểu và tối ưu hóa cấu trúc rẽ nhánh phức tạp trong Python
- Áp dụng toán tử ba ngôi và mệnh đề bảo vệ để làm sạch mã nguồn
- Hiểu và áp dụng cơ chế so khớp mẫu (Pattern Matching) để thay thế cấu trúc if-elif-else phức tạp.
- Sử dụng thành thạo cấu trúc match-case với Sequence, Mapping, Guard Clause và Capture Pattern.
- Kiểm soát và xử lý an toàn các nhánh rẽ nhánh đa trường hợp trong Python 3.10+.

## 



### Toán tử số học cơ bản

#### Khái niệm cốt lõi

- Các phép tính cơ bản bao gồm cộng (+), trừ (-), nhân (*) và lũy thừa (**), được sử dụng để thực hiện tính toán trên các kiểu dữ liệu số.

#### Cú pháp & Cách khai báo

- Ví dụ:
  
  ```python
  a = 17
  b = 5
  tong = a + b
  hieu = a - b
  tich = a * b
  luy_thua = b ** 2
  ```

#### Lưu ý thực chiến

- Toán tử lũy thừa (**) có độ ưu tiên cao hơn các toán tử nhân và chia thông thường.

### Phép chia thông thường (/)

#### Khái niệm cốt lõi

- Phép chia thông thường (/) thực hiện chia hai số và luôn trả về kết quả dưới dạng số thực (float), ngay cả khi hai số chia hết cho nhau.

#### Cú pháp & Cách khai báo

- Ví dụ:
  
  ```python
  thuong_thuc = 17 / 5
  ```

#### Lưu ý thực chiến

- Kết quả nhận được luôn có kiểu dữ liệu là float. Gây ra lỗi ZeroDivisionError nếu chia cho số 0.

### Phép chia lấy nguyên (//)

#### Khái niệm cốt lõi

- Phép chia lấy nguyên (//) chia phần trị số và làm tròn xuống số nguyên lớn nhất nhỏ hơn hoặc bằng kết quả thực tế.

#### Cú pháp & Cách khai báo

- Ví dụ:
  
  ```python
  thuong_nguyen = 17 // 5
  ```

#### Lưu ý thực chiến

- Nếu một trong hai toán hạng là kiểu số thực (float), kết quả trả về sẽ là một số thực làm tròn (ví dụ: 17.0 // 5 cho ra 3.0). Tránh chia cho 0 để ngăn ZeroDivisionError.

### Phép chia lấy dư (%)

#### Khái niệm cốt lõi

- Phép chia lấy dư (%) thực hiện phép chia và trả về phần dư còn lại của phép chia đó.

#### Cú pháp & Cách khai báo

- Ví dụ:
  
  ```python
  so_du = 17 % 5
  ```

#### Lưu ý thực chiến

- Thường dùng để kiểm tra tính chẵn lẻ của một số (chia dư cho 2) hoặc tính chia hết. Gây lỗi chia cho 0 nếu số chia là 0.

### Thứ tự ưu tiên toán tử

#### Khái niệm cốt lõi

- Độ ưu tiên sắp xếp từ cao xuống thấp: Ngoặc đơn () -> Lũy thừa (**) -> Nhân, chia, chia nguyên, chia dư (*, /, //, %) -> Cộng, trừ (+, -).
- ![](../images/mindmap_img_1.png)

#### Cú pháp & Cách khai báo

- Ví dụ:
  
  ```python
  ket_qua = (17 + 5) * 2 ** 3
  ```

#### Lưu ý thực chiến

- Luôn sử dụng dấu ngoặc đơn () để chỉ định rõ ràng thứ tự tính toán mong muốn, giúp tránh lỗi logic và làm mã nguồn dễ đọc hơn.

### Hàm input và chuyển đổi dữ liệu

#### Khái niệm cốt lõi

- Hàm input() nhận dữ liệu từ bàn phím dưới dạng chuỗi (str). Cần ép kiểu dữ liệu sang int hoặc float trước khi thực hiện các phép toán số học.

#### Cú pháp & Cách khai báo

- Ví dụ:
  
  ```python
  a = int(input())
  b = float(input())
  ```

#### Lưu ý thực chiến

- Quên ép kiểu sẽ gây ra lỗi TypeError vì không thể thực hiện phép toán số học giữa chuỗi và số.

## 



### Phân biệt gán và so sánh bằng

#### Khái niệm cốt lõi

- Toán tử gán (=) để lưu trữ giá trị vào vùng nhớ của biến. Toán tử so sánh bằng (==) để kiểm tra tính tương đương và trả về kết quả True hoặc False.
- ![](../images/mindmap_img_1.png)

#### Cú pháp & Cách khai báo

- ```python
  # Gán giá trị 20 cho biến age
  age = 20
  # So sánh giá trị của age với 18
  is_equal = age == 18
  ```

#### Lưu ý thực chiến

- Nhầm lẫn sử dụng '=' thay cho '==' trong cấu trúc điều kiện là lỗi cú pháp phổ biến dẫn đến SyntaxError.

### Sáu toán tử so sánh cơ bản

#### Khái niệm cốt lõi

- Các toán tử so sánh bao gồm: lớn hơn (>), bé hơn (<), lớn hơn hoặc bằng (>=), bé hơn hoặc bằng (<=), bằng (==), khác (!=). Bản chất là đánh giá quan hệ giữa hai toán hạng.

#### Cú pháp & Cách khai báo

- ```python
  x = 15
  y = 10
  print(x > y)   # True
  print(x <= y)  # False
  print(x != y)  # True
  ```

#### Lưu ý thực chiến

- Không viết sai thứ tự của các toán tử ghép, ví dụ viết nhầm thành '=>' hoặc '=<' sẽ gây lỗi cú pháp.

### Kiểu dữ liệu Boolean và biểu thức

#### Khái niệm cốt lõi

- Kết quả trả về của bất kỳ biểu thức so sánh nào đều thuộc kiểu dữ liệu boolean (chỉ gồm hai giá trị: True hoặc False).

#### Cú pháp & Cách khai báo

- ```python
  score = 8.5
  has_passed = score >= 5.0
  print(has_passed)       # True
  print(type(has_passed)) # <class 'bool'>
  ```

#### Lưu ý thực chiến

- Biến kiểu Boolean nên được đặt tên có tiền tố chỉ trạng thái như 'is_', 'has_', 'can_' để mã nguồn tự tường minh.

### So sánh chuỗi và số

#### Khái niệm cốt lõi

- Việc so sánh chuỗi với số qua toán tử so sánh thứ tự (>, <, >=, <=) sẽ sinh lỗi. Phép so sánh quan hệ chuỗi được thực hiện theo thứ tự mã Unicode (lexicographical order).
- ![](../images/mindmap_img_2.png)

#### Cú pháp & Cách khai báo

- ```python
  compare_str = 'apple' < 'banana' # True
  # So sánh bằng khác kiểu dữ liệu
  is_equal = '20' == 20            # False
  ```

#### Lưu ý thực chiến

- So sánh lớn bé khác kiểu dữ liệu sinh ra lỗi TypeError. Phải ép kiểu dữ liệu về cùng một dạng trước khi so sánh.

### Biểu thức logic thực tế

#### Khái niệm cốt lõi

- Biểu thức so sánh lưu kết quả boolean của các điều kiện trong thực tế để phục vụ cho các logic rẽ nhánh chương trình.

#### Cú pháp & Cách khai báo

- ```python
  age = 20
  # Đánh giá tính hợp lệ của tuổi tham gia
  is_eligible = age >= 18
  print('Eligible:', is_eligible)
  ```

#### Lưu ý thực chiến

- Nên phân tách các biểu thức logic phức tạp thành các biến bool trung gian thay vì viết chuỗi so sánh quá dài trên một dòng code.

## 



### Toán tử logic cơ bản

#### Khái niệm cốt lõi

- Toán tử logic kết hợp nhiều điều kiện so sánh để đưa ra quyết định rẽ nhánh chương trình.

#### Cú pháp & Cách khai báo

- Ví dụ cơ bản:
  
  ```python
  a = True
  b = False
  print(a and b)  # Kết quả: False
  print(a or b)   # Kết quả: True
  print(not a)    # Kết quả: False
  ```

#### Lưu ý thực chiến

- Tránh nhầm lẫn giữa toán tử logic (and, or) với toán tử bitwise (&, |) khi xử lý các giá trị Boolean.

### Thứ tự ưu tiên logic

#### Khái niệm cốt lõi

- Thứ tự ưu tiên thực thi từ cao xuống thấp khi không có dấu ngoặc là: not, tiếp đến is/in/so sánh, and, và cuối cùng là or.

#### Cú pháp & Cách khai báo

- Phân biệt thứ tự mặc định và sử dụng dấu ngoặc đơn:
  
  ```python
  # Mặc định: and chạy trước or
  res1 = True or False and False  # Tương đương: True or (False and False) -> True
  
  # Thay đổi thứ tự bằng dấu ngoặc
  res2 = (True or False) and False  # Kết quả: False
  ```

#### Lưu ý thực chiến

- Luôn sử dụng cặp ngoặc đơn để tường minh hóa các biểu thức phức tạp, tránh lỗi logic do quên thứ tự ưu tiên.

### Kiểm tra đầu vào

#### Khái niệm cốt lõi

- Sử dụng các toán tử logic để kiểm tra đồng thời nhiều ràng buộc dữ liệu đầu vào trước khi xử lý tiếp.

#### Cú pháp & Cách khai báo

- Xác thực dữ liệu hợp lệ:
  
  ```python
  tuoi = 20
  chieu_cao = 165
  # Kiểm tra nhiều điều kiện đồng thời
  is_valid = (tuoi >= 18) and (chieu_cao >= 150)
  ```

#### Lưu ý thực chiến

- Cảnh giác với giá trị rỗng (chuỗi rỗng "", số 0, None) vì Python coi chúng là Falsy trong các biểu thức điều kiện.

### Đánh giá ngắn mạch

#### Khái niệm cốt lõi

- Khi kết quả của biểu thức đã được xác định chắc chắn ở vế trước, Python sẽ dừng và không đánh giá vế sau.

#### Cú pháp & Cách khai báo

- Ngăn ngừa lỗi runtime chia cho 0 hoặc lỗi giá trị None:
  
  ```python
  mau_so = 0
  # Vế trái False giúp bỏ qua vế phải, tránh lỗi ZeroDivisionError
  hop_le = (mau_so != 0) and (10 / mau_so > 1)
  ```

#### Lưu ý thực chiến

- Đặt điều kiện kiểm tra an toàn (như khác None hoặc khác 0) ở vế bên trái của toán tử logic để tránh lỗi hệ thống.
- ![](../images/mindmap_img_1.png)

### Bảng chân trị tự động

#### Khái niệm cốt lõi

- Sử dụng vòng lặp lồng nhau duyệt qua các cặp giá trị True/False để kết xuất ra toàn bộ kết quả của biểu thức logic.

#### Cú pháp & Cách khai báo

- Tạo bảng chân trị tự động cho biểu thức logic:
  
  ```python
  print("A     | B     | A and (not B)")
  print("-" * 30)
  for A in [True, False]:
      for B in [True, False]:
          ket_qua = A and (not B)
          print(f"{str(A):<5} | {str(B):<5} | {str(ket_qua)}")
  ```

#### Lưu ý thực chiến

- Tự động hóa bảng chân trị giúp kiểm thử và phát hiện sai sót logic trong các điều kiện nghiệp vụ phức tạp.

## 



### Khối lệnh điều kiện if-else

#### Khái niệm cốt lõi

- Cho phép chương trình lựa chọn thực thi hoặc bỏ qua một khối lệnh dựa trên tính đúng/sai (True/False) của một điều kiện.

#### Cú pháp & Cách khai báo

- Ví dụ cú pháp:
  
  ```python
  x = 10
  if x > 5:
      print("Lớn hơn 5")
  else:
      print("Nhỏ hơn hoặc bằng 5")
  ```

#### Lưu ý thực chiến

- Cần có dấu hai chấm ở cuối điều kiện và bắt buộc các dòng lệnh phía dưới phải thụt lề đồng nhất để tránh lỗi SyntaxError hoặc IndentationError.

### Biểu thức điều kiện

#### Khái niệm cốt lõi

- Biểu thức trả về giá trị Boolean (True hoặc False) qua việc so sánh các giá trị hoặc biến số.

#### Cú pháp & Cách khai báo

- Ví dụ cú pháp:
  
  ```python
  a = 15
  b = 20
  ket_qua = a < b
  ```

#### Lưu ý thực chiến

- Tránh nhầm lẫn giữa toán tử gán '=' và toán tử so sánh bằng '=='.

### Cấu trúc rẽ nhánh nhiều trường hợp if-elif-else

#### Khái niệm cốt lõi

- Chuỗi các nhánh điều kiện chạy liên tiếp, chương trình sẽ đi vào khối lệnh đầu tiên thoả mãn True và bỏ qua các nhánh còn lại.

#### Cú pháp & Cách khai báo

- Ví dụ cú pháp:
  
  ```python
  bmi = 22.5
  if bmi < 18.5:
      print("Thiếu cân")
  elif bmi < 25.0:
      print("Bình thường")
  else:
      print("Béo phì")
  ```

#### Lưu ý thực chiến

- Nhánh else là tuỳ chọn và chỉ chạy khi toàn bộ các điều kiện if và elif phía trước đều sai (False).
- ![](../images/mindmap_img_1.png)

### Toán tử logic

#### Khái niệm cốt lõi

- Các từ khoá and, or, not dùng để liên kết nhiều biểu thức so sánh đơn lẻ thành một điều kiện phức tạp.

#### Cú pháp & Cách khai báo

- Ví dụ sử dụng:
  
  ```python
  tuoi = 20
  co_bang_lai = True
  if tuoi >= 18 and co_bang_lai:
      print("Được phép lái xe")
  ```

#### Lưu ý thực chiến

- Toán tử and yêu cầu tất cả các vế đúng, toán tử or chỉ cần một vế đúng, toán tử not phủ định giá trị Boolean gốc.

### Dòng điều khiển (Control Flow)

#### Khái niệm cốt lõi

- Trình tự thực thi các câu lệnh của chương trình, bị rẽ sang các hướng khác nhau khi gặp cấu trúc điều kiện.

#### Cú pháp & Cách khai báo

- Ví dụ dòng chạy:
  
  ```python
  print("Bắt đầu")
  if False:
      print("Bỏ qua dòng này")
  print("Kết thúc")
  ```

#### Lưu ý thực chiến

- Dòng điều khiển sẽ đi từ trên xuống dưới, việc kiểm soát thứ tự nhánh quyết định hiệu năng và logic của chương trình.
- ![](../images/mindmap_img_2.png)

### Lỗi logic điều kiện không thể thực thi (Unreachable Code)

#### Khái niệm cốt lõi

- Hiện tượng một khối lệnh không bao giờ được thực hiện do logic điều kiện bao trùm của nhánh trước đó đã chặn hết các dữ liệu đầu vào có thể xảy ra.

#### Cú pháp & Cách khai báo

- Ví dụ lỗi:
  
  ```python
  x = 15
  if x > 10:
      print("Lớn hơn 10")
  elif x > 20: 
      print("Không thể chạm tới")
  ```

#### Lưu ý thực chiến

- Luôn kiểm tra xem miền giá trị của các điều kiện đằng sau có bị trùng khít hay nằm hoàn toàn trong miền của các điều kiện đằng trước hay không.

### Tối ưu hóa thứ tự nhánh điều kiện

#### Khái niệm cốt lõi

- Sắp xếp các điều kiện theo mức độ ưu tiên hoặc phạm vi từ hẹp đến rộng để tránh bỏ sót trường hợp và tối ưu số lần so khớp biểu thức.

#### Cú pháp & Cách khai báo

- Sắp xếp hợp lý:
  
  ```python
  score = 85
  if score >= 90:
      print("Xuất sắc")
  elif score >= 80:
      print("Khá")
  ```

#### Lưu ý thực chiến

- Đặt điều kiện có điều kiện biên chặt chẽ hơn hoặc có tần suất xảy ra cao hơn lên trước nhằm giảm thiểu công sức tính toán của máy tính.

## 

### Nested if-else (Cấu trúc điều kiện lồng nhau)

#### Khái niệm cốt lõi

- Việc đặt câu lệnh điều kiện if-else này bên trong một câu lệnh if-else khác để kiểm tra các điều kiện phụ thuộc lẫn nhau.
- ![](../images/mindmap_img_1.png)

#### Cú pháp & Cách khai báo

- Cú pháp lồng nhau:
  
  ```python
  if condition_1:
      if condition_2:
          result = "Both true"
      else:
          result = "Only first true"
  ```

#### Lưu ý thực chiến

- Tránh lỗi Deep Nesting (Pyramid of Doom) khi lồng quá 3 tầng if-else, gây khó đọc và bảo trì mã nguồn.

### Ternary Operator (Toán tử ba ngôi trong Python)

#### Khái niệm cốt lõi

- Cú pháp viết tắt if-else trên một dòng để gán giá trị hoặc trả về kết quả nhanh chóng dựa theo điều kiện logic.

#### Cú pháp & Cách khai báo

- Cú pháp toán tử ba ngôi:
  
  ```python
  result = "Approved" if amount > 1000 else "Pending"
  ```

#### Lưu ý thực chiến

- Không lồng biểu thức ba ngôi trong biểu thức ba ngôi khác vì sẽ gây khó hiểu và giảm khả năng đọc code.

### Guard Clauses (Mệnh đề bảo vệ)

#### Khái niệm cốt lõi

- Kỹ thuật kiểm tra điều kiện biên hoặc lỗi ở đầu hàm và thoát sớm bằng return, loại bỏ cấu trúc if-else lồng nhau phức tạp.
- ![](../images/mindmap_img_2.png)

#### Cú pháp & Cách khai báo

- Cú pháp sử dụng Guard Clauses:
  
  ```python
  def check_payment(amount, is_verified):
      if amount <= 0:
          return "Invalid amount"
      if not is_verified:
          return "Unverified account"
      return "Require approval" if amount > 1000 else "Approved"
  ```

#### Lưu ý thực chiến

- Bắt buộc phải có lệnh return hoặc raise tương ứng trong các nhánh bảo vệ để chấm dứt hàm ngay lập tức, tránh để logic chạy tiếp xuống dưới.

## 



### Structural Pattern Matching

#### Khái niệm cốt lõi

- Cơ chế so khớp cấu trúc dữ liệu theo mẫu (shape/structure) và giá trị của dữ liệu.

#### Cú pháp & Cách khai báo

- Cú pháp cơ bản:
  
  ```python
  match status_code:
      case 200:
          print("OK")
      case 404:
          print("Not Found")
  ```

#### Lưu ý thực chiến

- Chỉ hỗ trợ từ Python 3.10 trở lên. Không hoạt động trên các phiên bản cũ hơn.
- ![](../images/mindmap_img_1.png)

### Wildcard Pattern (case _)

#### Khái niệm cốt lõi

- Mẫu đại diện khớp với bất kỳ giá trị nào, đóng vai trò như nhánh mặc định (default/else) khi không có trường hợp nào khác khớp.

#### Cú pháp & Cách khai báo

- Sử dụng ký tự gạch dưới:
  
  ```python
  match value:
      case 1:
          print("One")
      case _:
          print("Default case")
  ```

#### Lưu ý thực chiến

- Bắt buộc phải đặt ở vị trí cuối cùng trong danh sách các match case để tránh gây lỗi SyntaxError.

### Sequence Pattern

#### Khái niệm cốt lõi

- So khớp dữ liệu dạng chuỗi tuần tự như danh sách (list) hoặc bộ dữ liệu (tuple) dựa trên số lượng và cấu trúc phần tử.

#### Cú pháp & Cách khai báo

- Ví dụ so khớp list/tuple:
  
  ```python
  match point:
      case (0, 0):
          print("Origin")
      case (x, y):
          print(f"Point {x}, {y}")
      case (x, y, *rest):
          print(f"3D+ Point, remaining: {rest}")
  ```

#### Lưu ý thực chiến

- Sử dụng dấu sao (*) để gom phần còn lại của sequence vào một biến, tránh lỗi lệch số lượng phần tử.

### Mapping Pattern

#### Khái niệm cốt lõi

- So khớp dữ liệu kiểu ánh xạ hoặc từ điển (dictionary) dựa trên sự hiện diện của các khóa (keys) và giá trị tương ứng.

#### Cú pháp & Cách khai báo

- Ví dụ so khớp dictionary:
  
  ```python
  match user_data:
      case {"role": "admin", "id": user_id}:
          print(f"Admin ID: {user_id}")
      case {"role": _}:
          print("Standard user")
  ```

#### Lưu ý thực chiến

- Chỉ kiểm tra sự trùng khớp của các cặp key-value được khai bảo, các key dư thừa khác trong object thực tế sẽ được bỏ qua.

### Guard Clause (if trong match-case)

#### Khái niệm cốt lõi

- Điều kiện bổ sung (guard) đi kèm sau biểu thức so khớp mẫu giúp bộ lọc hoạt động chặt chẽ hơn.

#### Cú pháp & Cách khai báo

- Thêm từ khóa if phía sau case pattern:
  
  ```python
  match number:
      case val if val > 0:
          print("Positive")
      case val if val < 0:
          print("Negative")
  ```

#### Lưu ý thực chiến

- Biến trong pattern sẽ được gán giá trị trước khi biểu thức điều kiện của mệnh đề if được đánh giá.

### Capture Pattern (Từ khóa as)

#### Khái niệm cốt lõi

- Trích xuất và ràng buộc một phần hoặc toàn bộ mẫu đã khớp vào một biến để tái sử dụng trong khối mã thực thi.

#### Cú pháp & Cách khai báo

- Sử dụng từ khóa as để gán biến:
  
  ```python
  match response:
      case {"status": 200, "data": x} as result:
          print(f"Full response: {result}, data: {x}")
  ```

#### Lưu ý thực chiến

- Rất hữu dụng khi cần vừa xác thực cấu trúc logic của mẫu vừa lưu lại toàn bộ dữ liệu gốc để xử lý.
```