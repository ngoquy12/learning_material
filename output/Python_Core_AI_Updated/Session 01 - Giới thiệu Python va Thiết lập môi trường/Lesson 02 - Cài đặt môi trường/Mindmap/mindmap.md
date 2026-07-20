```markmap
# Session 01: Cài đặt môi trường

## Mục tiêu bài học
- Cấu hình thành công trình thông dịch Python và cài đặt trình soạn thảo mã nguồn VS Code.
- Tự thiết lập và vận hành độc lập môi trường ảo để phục vụ quá trình học tập và làm việc.
- Giải quyết thành thạo các lỗi vận hành cài đặt phổ biến liên quan đến biến hệ thống và quyền chạy script.

## Python Interpreter
### Khái niệm cốt lõi
Trình thông dịch Python chịu trách nhiệm dịch mã nguồn Python thành mã trung gian bytecode sau đó máy ảo Python thực thi các chỉ thị này trên hệ điều hành.
![](../images/mindmap_img_1.png)
### Cú pháp & Cách khai báo
- Xem thông số môi trường thi hành hiện tại qua mã nguồn:
  ```python
  import sys
  import platform
  print("He dieu hanh:", platform.system())
  print("Phien ban Python OS:", sys.version)
  print("Duong dan thuc thi:", sys.executable)
  ```
### Lưu ý thực chiến
Tránh sử dụng phiên bản Python quá mới bị thiếu sự hỗ trợ từ các thư viện chưa nâng cấp, khuyến nghị sử dụng các bản phân phối LTS ổn định.

## Integrated Development Environment (IDE) / VS Code
### Khái niệm cốt lõi
Visual Studio Code là trình soạn thảo mã nguồn gọn nhẹ cung cấp các công cụ mạnh mẽ như tô sáng cú pháp, tự động hoàn thiện mã nguồn và gỡ lỗi trực quan.
### Cú pháp & Cách khai báo
- Phím tắt mở bảng điều khiển Command Palette:
  - Windows/Linux: `Ctrl + Shift + P`
  - macOS: `Cmd + Shift + P`
- Lệnh cấu hình trình thông dịch cho VS Code trong Command Palette:
  - `Python: Select Interpreter`
### Lưu ý thực chiến
Luôn cấu hình tệp workspace trong VS Code trỏ và liên kết trực tiếp vào thư mục chứa môi trường ảo của dự án hiện hành để chạy debugger chuẩn xác.

## Virtual Environment
### Khái niệm cốt lõi
Môi trường ảo là cấu trúc thư mục phụ lập cách ly tuyệt đối mọi thư viện bên thứ ba cài thêm để tránh xung đột phiên bản phần mềm giữa các dự án khác nhau.
![](../images/mindmap_img_2.png)
### Cú pháp & Cách khai báo
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
### Lưu ý thực chiến
Khi kiểm thử mã nguồn trên các môi trường phân tán phải xuất tệp phụ thuộc để tái tạo môi trường bằng chỉ thị `pip freeze > requirements.txt`.

## venv & Anaconda
### Khái niệm cốt lõi
venv là công cụ tích hợp sẵn gọn nhẹ cho việc đóng gói ứng dụng web, trong khi Anaconda là một hệ phân phối phần mềm nặng cung cấp môi trường khép kín conda tích hợp sẵn thư viện phân tích tính toán.
### Cú pháp & Cách khai báo
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
### Lưu ý thực chiến
Tránh cài đặt cài chéo các thư viện bằng pip cài đè đắp lên môi trường do conda quản lý vì có thể làm gãy cấu cấu trúc thư viện gốc của hệ sinh thái Anaconda.

## Biến PATH (Environment Variable)
### Khái niệm cốt lõi
PATH là biến môi trường của hệ thống chứa danh sách địa chỉ chỉ mục đến các thư mục chứa lệnh điều khiển của phần mềm, giúp hệ thống nhận diện tệp thực thi toàn cục.
![](../images/mindmap_img_3.png)
### Cú pháp & Cách khai báo
- Xem danh sách đường dẫn biến PATH đang hoạt động của hệ điều hành:
  - Windows (PowerShell):
    ```powershell
    $env:Path -split ";"
    ```
  - macOS / Linux:
    ```bash
    echo $PATH | tr ":" "\n"
    ```
### Lưu ý thực chiến
Không kiểm tra việc nạp lệnh vào biến PATH trong tiến trình cài đặt Python sẽ trực tiếp kích hoạt lỗi thông báo dòng lệnh `python is not recognized`.

## Lỗi phân quyền kích hoạt shell (Execution Policy)
### Khái niệm cốt lõi
Execution Policy là cơ chế bảo mật nội tại của Windows PowerShell ngăn chặn các mã tập lệnh trái phép khởi tạo, bao gồm cả tập lệnh kích hoạt môi trường ảo.
### Cú pháp & Cách khai báo
- Thiết lập quyền thực thi tập lệnh môi trường ảo trong Windows PowerShell:
  - Kiểm tra trạng thái hiện hành:
    ```powershell
    Get-ExecutionPolicy
    ```
  - Cho phép chạy script nội bộ đã ký từ nhà phát triển:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
### Lưu ý thực chiến
Chỉ mở ở phạm vi người dùng tối giản nhất là CurrentUser để bảo mật hệ thống toàn diện, tránh sử dụng chính sách không an toàn `Unrestricted` trên toàn máy tính.
```
```
```