---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 01 - Lesson 02
## Cài đặt môi trường Python

Giảng viên: [Tên Giảng Viên]

---

## Vấn đề: Trở ngại khi bắt đầu

- **Lỗi đường dẫn hệ thống**: Người học thường gặp lỗi khi chạy lệnh Python trong terminal do thiếu cấu hình biến môi trường PATH.
- **Xung đột phiên bản (Dependency Conflict)**:
  - Việc cài đặt trực tiếp tất cả thư viện vào môi trường hệ thống (Global) dễ gây ra xung đột nghiêm trọng giữa các dự án khác nhau.
  - Khiến hệ thống mất ổn định và không thể chạy được mã nguồn.

---

## Phân tích: Trình dịch & Môi trường ảo

Để giải quyết vấn đề cô lập và thực thi mã nguồn, chúng ta cần phân biệt rõ:

- **Python Interpreter**:
  - Trình biên dịch dịch mã nguồn Python thành mã byte để thực thi trên máy.
  - Khi gõ lệnh `python`, hệ thống sẽ kích hoạt interpreter này. Trình soạn thảo (VS Code) cần được cấu hình chỉ tới đúng đường dẫn của tệp này.
- **Virtual Environment (Môi trường ảo)**:
  - Tạo ra các vùng thư mục cô lập độc lập dành riêng cho mỗi dự án.
  - Giúp quản lý riêng rẽ phiên bản thư viện mà không ảnh hưởng tới Python hệ thống.

---

## Các thành phần cấu hình cơ bản

- **Biến PATH (Environment Variable)**:
  - Biến hệ thống chứa danh sách các đường dẫn giúp hệ điều hành tìm thấy lệnh `python` và `pip` khi chạy từ Terminal.
- **IDE / VS Code**:
  - Trình soạn thảo mã nguồn cần cấu hình đường dẫn Python Interpreter phù hợp để nhận diện cú pháp và hỗ trợ gỡ lỗi.
- **venv & Anaconda**:
  - `venv` là công cụ tạo môi trường ảo tích hợp sẵn trong thư viện chuẩn của Python.
  - `Anaconda` là hệ sinh thái phân phối Python mở rộng cho khoa học dữ liệu.

---

## Quy trình 4 bước thiết lập chuẩn

1. **Cài đặt Python**: Cài đặt Python chính thức từ trang chủ và tích chọn cấu hình biến PATH tự động.
2. **Thiết lập IDE**: Cài đặt VS Code kèm extension Python và lựa chọn đường dẫn Interpreter thích hợp.
3. **Khởi tạo môi trường ảo**: Sử dụng module `venv` tích hợp sẵn trong thư viện tiêu chuẩn để tạo thư mục chứa môi trường ảo.
4. **Kích hoạt & Sử dụng**: Kích hoạt môi trường và thực hiện cài đặt các thư viện phụ thuộc riêng biệt.

---

## Các lệnh quản lý môi trường (CLI)

Thực hiện các lệnh sau để khởi tạo và kích hoạt môi trường ảo:

```bash
# Khoi tao moi truong ao co ten la 'myenv'
python -m venv myenv

# Kich hoat moi truong ao tren Windows (Command Prompt)
myenv\\Scripts\\activate

# Kich hoat va bypass loi phan quyen tren Windows (PowerShell)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\\myenv\\Scripts\\Activate.ps1

# Kich hoat moi truong ao tren macOS/Linux (Terminal)
source myenv/bin/activate
```

---

## Script kiểm tra thông tin cài đặt

Sử dụng script `verify_setup.py` để hiển thị các thông số môi trường hiện tại của hệ thống:

```python
import sys
import platform

# Hien thi cac thong so moi truong hien tai
print('He dieu hanh dang chay:', platform.system())
print('Phien ban Python dang su dung:', sys.version)
print('Duong dan thuc thi cua Python:', sys.executable)
```

---

## Script kiểm tra môi trường ảo

Sử dụng script `check_venv.py` để kiểm tra xem chương trình có đang chạy trong môi trường cô lập hay không:

```python
import sys

# Kiem tra xem chuong trinh co chay trong moi truong ao (Virtual Environment) hay khong
is_active_venv = sys.prefix != sys.base_prefix
print('Moi truong ao dang hoat dong:', is_active_venv)
print('Duong dan thu muc dang thuc thi (Active Prefix):', sys.prefix)
print('Duong dan thu muc goc (Base Prefix):', sys.base_prefix)
```

---

## Tổng kết: Ba sai lầm thường gặp

- **Quên cấu hình PATH**:
  - Không chọn "Add Python to PATH" khi cài đặt dẫn đến lỗi Terminal/CMD không nhận dạng được lệnh `python` hay `pip`.
- **Chưa kích hoạt môi trường ảo**:
  - Cài đặt thư viện khi chưa kích hoạt môi trường ảo khiến các gói phụ thuộc bị phân tán vào thư mục cài đặt gốc (Global).
- **Lỗi phân quyền Execution Policy**:
  - Hệ điều hành Windows PowerShell chặn thực thi script kích hoạt môi trường ảo (`.ps1`). Cần sử dụng lệnh Bypass tạm thời để xử lý.