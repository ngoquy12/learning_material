```markmap
---
markmap:
  colorFreezeLevel: 3
---
# Session 01 - Giới thiệu Python & Thiết lập môi trường

## Mục tiêu bài học
- Hiểu triết lý thiết kế Zen of Python và cơ chế thực thi của ngôn ngữ thông dịch.
- Nắm vững tính chất kiểu dữ liệu động và các ứng dụng thực tế của Python.
- Nhận diện và phòng tránh các lỗi cơ bản như thụt lề sai và xung đột kiểu dữ liệu.
- Cấu hình thành công trình thông dịch Python và cài đặt trình soạn thảo mã nguồn VS Code.
- Tự thiết lập và vận hành độc lập môi trường ảo để phục vụ quá trình học tập và làm việc.
- Giải quyết thành thạo các lỗi vận hành cài đặt phổ biến liên quan đến biến hệ thống và quyền chạy script.
- Khai báo và sử dụng thành thạo biến với các kiểu dữ liệu cơ bản int, float, str, bool.
- Hiểu rõ quy tắc đặt tên biến và cách kiểm tra kiểu dữ liệu bằng hàm type.
- Nhận diện và tránh các lỗi cú pháp cơ bản liên quan đến biến.
- Sử dụng thành thạo hàm input để nhận dữ liệu và hàm print để hiển thị kết quả
- Thực hiện ép kiểu dữ liệu linh hoạt bằng int, float, str phục vụ tính toán số học
- Nhận diện và phòng tránh lỗi ValueError cùng các lỗi logic phổ biến khi xử lý dữ liệu đầu vào
- Nắm vững cú pháp f-string để hiển thị thông tin trực quan và tối ưu hơn phương pháp truyền thống.
- Làm chủ kỹ thuật làm tròn số thực, hiển thị số lớn và can lề dữ liệu dạng bảng.
- Nhận biết và phòng ngừa các lỗi cú pháp phổ biến khi sử dụng f-string.

## 



### Triết lý thiết kế (Zen of Python)

#### Khái niệm cốt lõi

- Bộ quy tắc định hướng viết mã nguồn Python tối giản, rõ ràng, đề cao tính mở rộng và khả năng đọc hiểu của con người.

#### Cú pháp & Cách khai báo

- Lệnh hiển thị các nguyên tắc thiết kế của Python:
  
  ```python
  import this
  ```

#### Lưu ý thực chiến

- Ưu tiên viết mã nguồn trực quan, tường minh thay vì viết các đoạn code phức tạp, khó hiểu để tối ưu hóa việc bảo trì.

### Ngôn ngữ thông dịch (Interpreted Language)

#### Khái niệm cốt lõi

- Mã nguồn Python không biên dịch trực tiếp ra mã máy mà được trình thông dịch dịch từng dòng thành bytecode rồi thực thi trên máy ảo Python.
- ![](../images/mindmap_img_1.png)

#### Cú pháp & Cách khai báo

- Thực thi một script Python trực tiếp từ Terminal:
  
  ```bash
  python main.py
  ```

#### Lưu ý thực chiến

- Tốc độ chạy thường chậm hơn ngôn ngữ biên dịch và lỗi cú pháp chỉ được phát hiện khi luồng chương trình chạy tới dòng code lỗi.

### Kiểu dữ liệu động (Dynamic Typing)

#### Khái niệm cốt lõi

- Kiểu dữ liệu của biến được quyết định tự động tại thời điểm chạy dựa trên giá trị gán cho biến mà không cần khai báo trước.

#### Cú pháp & Cách khai báo

- Khai báo biến và thay đổi kiểu dữ liệu:
  
  ```python
  x = 10
  x = "Xin chao Python"
  print(type(x))
  ```

#### Lưu ý thực chiến

- Tránh thay đổi kiểu dữ liệu của biến một cách tùy tiện trong cùng một phạm vi để hạn chế lỗi logic khi thực hiện tính toán.

### Ứng dụng đa lĩnh vực của Python

#### Khái niệm cốt lõi

- Khả năng ứng dụng rộng rãi từ phân tích dữ liệu, trí tuệ nhân tạo, phát triển web cho đến kiểm thử tự động nhờ thư viện phong phú.

#### Cú pháp & Cách khai báo

- Import module từ thư viện chuẩn để xử lý tính toán:
  
  ```python
  import math
  print(math.sqrt(16))
  ```

#### Lưu ý thực chiến

- Luôn tìm kiếm giải pháp từ thư viện chuẩn trước khi cài thêm thư viện bên ngoài nhằm giảm thiểu sự phụ thuộc không cần thiết.

### Tự động hóa (Automation/Scripting)

#### Khái niệm cốt lõi

- Viết các đoạn mã ngắn để tự động hóa các tác vụ lặp đi lặp lại như quản lý file, thư mục và tương tác với hệ điều hành.

#### Cú pháp & Cách khai báo

- Lấy đường dẫn làm việc hiện tại của hệ thống:
  
  ```python
  import os
  print(os.getcwd())
  ```

#### Lưu ý thực chiến

- Cần nhất quán việc thụt lề (IndentationError) và kiểm tra kỹ quyền truy cập đường dẫn hệ thống để tránh lỗi dừng chương trình đột ngột.

## 



### Python Interpreter

#### Khái niệm cốt lõi

Trình thông dịch Python chịu trách nhiệm dịch mã nguồn Python thành mã trung gian bytecode sau đó máy ảo Python thực thi các chỉ thị này trên hệ điều hành.
![](../images/mindmap_img_1.png)

#### Cú pháp & Cách khai báo

- Xem thông số môi trường thi hành hiện tại qua mã nguồn:
  
  ```python
  import sys
  import platform
  print("He dieu hanh:", platform.system())
  print("Phien ban Python OS:", sys.version)
  print("Duong dan thuc thi:", sys.executable)
  ```

#### Lưu ý thực chiến

Tránh sử dụng phiên bản Python quá mới bị thiếu sự hỗ trợ từ các thư viện chưa nâng cấp, khuyến nghị sử dụng các bản phân phối LTS ổn định.



### Integrated Development Environment (IDE) / VS Code

#### Khái niệm cốt lõi

Visual Studio Code là trình soạn thảo mã nguồn gọn nhẹ cung cấp các công cụ mạnh mẽ như tô sáng cú pháp, tự động hoàn thiện mã nguồn và gỡ lỗi trực quan.

#### Cú pháp & Cách khai báo

- Phím tắt mở bảng điều khiển Command Palette:
  - Windows/Linux: `Ctrl + Shift + P`
  - macOS: `Cmd + Shift + P`
- Lệnh cấu hình trình thông dịch cho VS Code trong Command Palette:
  - `Python: Select Interpreter`

#### Lưu ý thực chiến

Luôn cấu hình tệp workspace trong VS Code trỏ và liên kết trực tiếp vào thư mục chứa môi trường ảo của dự án hiện hành để chạy debugger chuẩn xác.



### Virtual Environment

#### Khái niệm cốt lõi

Môi trường ảo là cấu trúc thư mục phụ lập cách ly tuyệt đối mọi thư viện bên thứ ba cài thêm để tránh xung đột phiên bản phần mềm giữa các dự án khác nhau.
![](../images/mindmap_img_2.png)

#### Cú pháp & Cách khai báo

- Khởi tạo môi trường ảo bằng venv trong Terminal:
  - Windows:
    
    ```cmd
    python -m venv venv_project
    venv_project\Scripts\activate
    ```
  - macOS / Linux:
    
    ```bash
    python3 -m venv venv_project
    source venv_project/bin/activate
    ```

#### Lưu ý thực chiến

Khi kiểm thử mã nguồn trên các môi trường phân tán phải xuất tệp phụ thuộc để tái tạo môi trường bằng chỉ thị `pip freeze > requirements.txt`.



### venv & Anaconda

#### Khái niệm cốt lõi

venv là công cụ tích hợp sẵn gọn nhẹ cho việc đóng gói ứng dụng web, trong khi Anaconda là một hệ phân phối phần mềm nặng cung cấp môi trường khép kín conda tích hợp sẵn thư viện phân tích tính toán.

#### Cú pháp & Cách khai báo

- Quản lý môi trường của hệ sinh thái Anaconda qua Terminal:
  - Tạo môi trường:
    
    ```bash
    conda create -n mainenv python=3.10
    ```
  - Kích hoạt và tắt môi trường:
    
    ```bash
    conda activate mainenv
    conda deactivate
    ```

#### Lưu ý thực chiến

Tránh cài đặt cài chéo các thư viện bằng pip cài đè đắp lên môi trường do conda quản lý vì có thể làm gãy cấu cấu trúc thư viện gốc của hệ sinh thái Anaconda.



### Biến PATH (Environment Variable)

#### Khái niệm cốt lõi

PATH là biến môi trường của hệ thống chứa danh sách địa chỉ chỉ mục đến các thư mục chứa lệnh điều khiển của phần mềm, giúp hệ thống nhận diện tệp thực thi toàn cục.
![](../images/mindmap_img_3.png)

#### Cú pháp & Cách khai báo

- Xem danh sách đường dẫn biến PATH đang hoạt động của hệ điều hành:
  - Windows (PowerShell):
    
    ```powershell
    $env:Path -split ";"
    ```
  - macOS / Linux:
    
    ```bash
    echo $PATH | tr ":" "\n"
    ```

#### Lưu ý thực chiến

Không kiểm tra việc nạp lệnh vào biến PATH trong tiến trình cài đặt Python sẽ trực tiếp kích hoạt lỗi thông báo dòng lệnh `python is not recognized`.



### Lỗi phân quyền kích hoạt shell (Execution Policy)

#### Khái niệm cốt lõi

Execution Policy là cơ chế bảo mật nội tại của Windows PowerShell ngăn chặn các mã tập lệnh trái phép khởi tạo, bao gồm cả tập lệnh kích hoạt môi trường ảo.

#### Cú pháp & Cách khai báo

- Thiết lập quyền thực thi tập lệnh môi trường ảo trong Windows PowerShell:
  - Kiểm tra trạng thái hiện hành:
    
    ```powershell
    Get-ExecutionPolicy
    ```
  - Cho phép chạy script nội bộ đã ký từ nhà phát triển:
    
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

#### Lưu ý thực chiến

Chỉ mở ở phạm vi người dùng tối giản nhất là CurrentUser để bảo mật hệ thống toàn diện, tránh sử dụng chính sách không an toàn `Unrestricted` trên toàn máy tính.

## 



### Biến (Variable)

#### Khái niệm cốt lõi

- Biến là nhãn hoặc tên tham chiếu đến một vùng nhớ chứa dữ liệu trong bộ nhớ máy tính.
- ![](../images/mindmap_img_1.png)

#### Cú pháp & Cách khai báo

- Khai báo tên biến và gán giá trị trực tiếp:
  
  ```python
  age = 25
  product_name = "Smart Device"
  ```

#### Lưu ý thực chiến

- Python là ngôn ngữ kiểu động (dynamic typing), không cần khai báo kiểu dữ liệu trước khi tạo biến.

### Phép gán (Assignment)

#### Khái niệm cốt lõi

- Phép gán sử dụng toán tử bằng (=) để liên kết một tên biến với một giá trị hoặc một đối tượng trong bộ nhớ.

#### Cú pháp & Cách khai báo

- Sử dụng toán tử `=` để gán:
  
  ```python
  x = 10
  y = x + 5
  ```

#### Lưu ý thực chiến

- Toán tử `=` biểu thị phép gán giá trị từ vế phải sang vế trái, không phải là phép so sánh bằng.

### Quy tắc đặt tên biến (Variable Naming Rules)

#### Khái niệm cốt lõi

- Tên biến chỉ được chứa chữ cái, chữ số và dấu gạch dưới, bắt đầu bằng chữ cái hoặc dấu gạch dưới, phân biệt chữ hoa và chữ thường.

#### Cú pháp & Cách khai báo

- Tên biến hợp lệ theo quy tắc đặt tên:
  
  ```python
  student_age = 20
  _value = 5.5
  ```

#### Lưu ý thực chiến

- Tránh sử dụng các từ khóa hệ thống, không bắt đầu bằng chữ số và nên tuân thủ định dạng snake_case.

### Kiểu dữ liệu int (Integer)

#### Khái niệm cốt lõi

- Kiểu dữ liệu số nguyên, đại diện cho các số nguyên dương, âm hoặc số 0 mà không có phần thập phân.

#### Cú pháp & Cách khai báo

- Khai báo biến kiểu số nguyên:
  
  ```python
  quantity = 100
  negative_number = -50
  ```

#### Lưu ý thực chiến

- Số nguyên trong Python có độ dài vô hạn, chỉ bị giới hạn bởi dung lượng bộ nhớ khả dụng của hệ thống.

### Kiểu dữ liệu float (Floating-point)

#### Khái niệm cốt lõi

- Kiểu dữ liệu số thực, đại diện cho các số có phần thập phân hoặc các số được biểu diễn ở dạng số mũ.

#### Cú pháp & Cách khai báo

- Khai báo biến kiểu số thực:
  
  ```python
  price = 9.99
  pi = 3.14159
  ```

#### Lưu ý thực chiến

- Cần cẩn trọng khi thực hiện phép toán so sánh trực tiếp float do sai số làm tròn số phân số trong hệ nhị phân.

### Kiểu dữ liệu str (String)

#### Khái niệm cốt lõi

- Kiểu dữ liệu chuỗi ký tự, dùng để lưu trữ văn bản và được đặt trong cặp dấu nháy đơn hoặc nháy kép.

#### Cú pháp & Cách khai báo

- Khai báo biến kiểu chuỗi:
  
  ```python
  greeting = "Hello"
  address = '123 Street'
  ```

#### Lưu ý thực chiến

- Chuỗi ký tự trong Python là đối tượng không thể thay đổi giá trị tại chỗ (immutable) sau khi được tạo.

### Kiểu dữ liệu bool (Boolean)

#### Khái niệm cốt lõi

- Kiểu dữ liệu luận lý chỉ nhận một trong hai trạng thái giá trị logic là True hoặc False.

#### Cú pháp & Cách khai báo

- Khai báo biến kiểu luận lý:
  
  ```python
  is_active = True
  is_completed = False
  ```

#### Lưu ý thực chiến

- Từ khóa True và False bắt buộc phải viết hoa chữ cái đầu tiên, viết thường hoàn toàn sẽ gây ra lỗi định nghĩa.

### Hàm type()

#### Khái niệm cốt lõi

- Hàm tích hợp sẵn dùng để kiểm tra và trả về kiểu dữ liệu thực tế của một đối tượng hoặc một biến.

#### Cú pháp & Cách khai báo

- Sử dụng hàm type để xác định kiểu dữ liệu:
  
  ```python
  x = 10
  print(type(x))
  ```

#### Lưu ý thực chiến

- Hàm trả về một đối tượng kiểu dữ liệu, thường được kết hợp với hàm print để hiển thị thông tin trực quan.

### Hàm print()

#### Khái niệm cốt lõi

- Hàm tích hợp sẵn dùng để hiển thị dữ liệu hoặc kết quả của các biến và biểu thức ra màn hình.

#### Cú pháp & Cách khai báo

- Sử dụng hàm print để xuất nhiều giá trị:
  
  ```python
  message = "Rikkei"
  print("Welcome to", message)
  ```

#### Lưu ý thực chiến

- Hàm print tự động thêm ký tự xuống dòng ở cuối đầu ra, có thể cấu hình lại bằng tham số end.

### Lỗi cú pháp (Syntax Error)

#### Khái niệm cốt lõi

- Lỗi xảy ra do viết mã nguồn vi phạm các quy tắc cú pháp và cấu trúc câu lệnh của ngôn ngữ Python.

#### Cú pháp & Cách khai báo

- Ví dụ về mã nguồn gây lỗi cú pháp:
  
  ```python
  # 1st_value = 10  # Lỗi do tên biến bắt đầu bằng số
  # class = 5       # Lỗi do trùng từ khóa hệ thống
  ```

#### Lưu ý thực chiến

- Khi gặp lỗi cú pháp, trình thông dịch Python sẽ thông báo lỗi và dừng chương trình ngay lập tức trước khi chạy.

## 



### Hàm input()

#### Khái niệm cốt lõi

- Hàm dùng để tạm dừng chương trình và nhận dữ liệu nhập vào từ bàn phím dưới dạng một chuỗi ký tự (string).

#### Cú pháp & Cách khai báo

- Nhận dữ liệu chuỗi từ người dùng:
  
  ```python
  ten_nguoi_dung = input("Nhap ten cua ban: ")
  ```

#### Lưu ý thực chiến

- Dữ liệu thu hồi từ input luôn có kiểu str. Nếu cần tính toán số học, bắt buộc phải thực hiện chuyển đổi kiểu dữ liệu.
- ![](../images/mindmap_img_1.png)

### Hàm print()

#### Khái niệm cốt lõi

- Hàm xuất dữ liệu ra màn hình console, hỗ trợ in nhiều giá trị cùng lúc và tự động chuyển đổi các đối tượng sang chuỗi để hiển thị.

#### Cú pháp & Cách khai báo

- Xuất nhiều giá trị đồng thời:
  
  ```python
  print("Kien thuc", "Python", 101)
  ```

#### Lưu ý thực chiến

- Mặc định hàm tự động thêm ký tự xuống dòng ở cuối đầu ra, có thể tùy chỉnh thông qua tham số end để thay đổi hành vi mặc định.

### Ép kiểu dữ liệu (Type Casting)

#### Khái niệm cốt lõi

- Quá trình chuyển đổi giá trị từ kiểu dữ liệu gốc sang kiểu dữ liệu đích như int, float, str để phục vụ các mục đích xử lý logic thích hợp.

#### Cú pháp & Cách khai báo

- Chuyển đổi chuỗi chữ số thành số để thực hiện phép toán:
  
  ```python
  so_nguyen = int("25")
  so_thuc = float("10.5")
  tong = so_nguyen + so_thuc
  print("Tong gia tri:", tong)
  ```

#### Lưu ý thực chiến

- Cảnh giác với lỗi logic nối chuỗi ngoài ý muốn khi thực hiện phép cộng (+) giữa hai giá trị nhận trực tiếp từ hàm input mà quên ép kiểu số.
- ![](../images/mindmap_img_2.png)

### Lỗi giá trị (ValueError) trong ép kiểu

#### Khái niệm cốt lõi

- Lỗi phát sinh trong thời gian chạy (runtime) khi hàm ép kiểu nhận vào giá trị có định dạng không phù hợp để chuyển đổi sang kiểu dữ liệu đích.

#### Cú pháp & Cách khai báo

- Các trường hợp điển hình gây ra lỗi ValueError:
  
  ```python
  # Loi do chuoi chua ky tu khong phai so
  so_nguyen_loi_1 = int("25a")
  
  # Loi do ep chuoi so thap phan truc tiep sang so nguyen
  so_nguyen_loi_2 = int("10.5")
  ```

#### Lưu ý thực chiến

- Chỉ ép kiểu chuỗi sang int khi chuỗi đó chỉ chứa các chữ số nguyên. Đối với chuỗi chứa số thập phân, bắt buộc phải ép kiểu sang float trước.

## 



### Định dạng f-string cơ bản

#### Khái niệm cốt lõi

Dạng định dạng chuỗi trực quan bằng cách chèn trực tiếp các biến hoặc biểu thức vào bên trong cặp dấu ngoặc nhọn của chuỗi ký tự có tiền tố f hoặc F.

#### Cú pháp & Cách khai báo

- Cú pháp mẫu khai báo f-string cơ bản:
  
  ```python
  name = "Nam"
  content = f"Xin chao {name}"
  print(content)
  ```

#### Lưu ý thực chiến

Cho phép thực thi biểu thức toán học hoặc gọi phương thức xử lý chuỗi trực tiếp bên trong cặp ngoặc nhọn.



### Phương pháp định dạng truyền thống

#### Khái niệm cốt lõi

Các phương pháp định dạng chuỗi trước phiên bản Python 3.6, bao gồm sử dụng toán tử phần trăm hoặc gọi phương thức format.

#### Cú pháp & Cách khai báo

- Cú pháp mẫu sử dụng toán tử phần trăm và phương thức format:
  
  ```python
  name = "Nam"
  # Dinh dang qua toan tu phan tram
  print("Xin chao %s" % name)
  # Dinh dang qua phuong thuc format
  print("Xin chao {}".format(name))
  ```

#### Lưu ý thực chiến

Phương pháp truyền thống dễ gây nhầm lẫn khi truyền nhiều tham số và làm giảm tốc độ thực thi so với f-string.



### Định dạng số thực và số lớn

#### Khái niệm cốt lõi

Cơ chế kiểm soát số lượng chữ số thập phân hiển thị và phân tách nhóm hàng nghìn bằng dấu phẩy để dữ liệu số dễ đọc hơn.

#### Cú pháp & Cách khai báo

- Cú pháp định dạng số thực và phân tách hàng nghìn:
  
  ```python
  gpa = 8.5678
  population = 97000000
  # Lam tron 2 chu so thap phan
  print(f"GPA: {gpa:.2f}")
  # Phan tach hang nghin bang dau phay
  print(f"Dan so: {population:,}")
  ```

#### Lưu ý thực chiến

Quên ký tự hai chấm trước phần chỉ dẫn định dạng sẽ gây lỗi cú pháp. Không áp dụng định dạng số cho biến kiểu chuỗi chưa ép kiểu.



### Căn lề dữ liệu

#### Khái niệm cốt lõi

Cách căn chỉnh dữ liệu sang trái, sang phải hoặc căn giữa trong một khoảng không gian ký tự xác định để tạo cấu trúc cột thẳng hàng.

#### Cú pháp & Cách khai báo

- Cú pháp căn lề trái và lề phải kèm độ rộng:
  
  ```python
  name = "Nam"
  gpa = 8.5678
  # Can le trai voi do rong 10 va le phai voi do rong 5
  print(f"{'Ten':<10} | {'Diem':>5}")
  print(f"{name:<10} | {gpa:>5.1f}")
  ```
- ![](../images/mindmap_img_1.png)

#### Lưu ý thực chiến

Nhập sai thứ tự định dạng sẽ sinh lỗi. Phải xác định trước độ rộng tối đa của chuỗi để tránh việc dữ liệu bị đè hoặc lệch cột.



### Tránh lỗi cú pháp f-string

#### Khái niệm cốt lõi

Các quy tắc kết hợp dấu nháy và ký hiệu ngoặc nhọn để không làm vỡ cấu trúc chuỗi hoặc phát sinh lỗi biên dịch.

#### Cú pháp & Cách khai báo

- Cú pháp xử lý dấu nháy và in ngoặc nhọn vật lý:
  
  ```python
  name = "Nam"
  # In ngoac nhon vat ly bang double bracket
  print(f"JSON: {{ 'name': '{name}' }}")
  ```

#### Lưu ý thực chiến

Không sử dụng cùng một loại dấu nháy đơn hoặc nháy kép cho cả bao chuỗi và biểu thức bên trong vì sẽ làm phát sinh lỗi SyntaxError.
```