---
marp: true
theme: default
paginate: true
_class: lead
---

# Session 01 - Lesson 03: Hướng dẫn cài đặt công cụ

---

## 1. Mục tiêu bài học
* Cài đặt thành công Python và Git trên hệ thống.
* Hiểu cách thiết lập biến môi trường PATH tạm thời.
* Tạo và kích hoạt môi trường ảo `.venv` cho dự án.
* Chạy chương trình chẩn đoán môi trường và ứng dụng FastAPI tối giản.

---

## 2. Kiểm tra phiên bản công cụ
* **Kiểm tra phiên bản**:
  ```bash
  # Kiểm tra phiên bản Python cài đặt
  python --version
  
  # Kiểm tra phiên bản Git cài đặt
  git --version
  ```
* **Cấu hình danh tính Git toàn cục**:
  ```bash
  git config --global user.name "Nguyen Van A"
  git config --global user.email "anv@gmail.com"
  ```
* **Khởi tạo kho lưu trữ Git**:
  ```bash
  git init
  ```

---

## 3. Cấu hình PATH tạm thời (Temporary PATH)
* **Windows (PowerShell)**:
  ```powershell
  $env:Path += ";C:\Path\To\Python"
  ```
* **Linux/macOS (Bash/Zsh)**:
  ```bash
  export PATH="$PATH:/path/to/python"
  ```
* **Lưu ý**: Cấu hình PATH tạm thời chỉ có tác dụng trong phiên làm việc terminal hiện tại.

---

## 4. Thiết lập môi trường ảo (venv)
* **Khởi tạo venv**:
  ```bash
  python -m venv .venv
  ```
* **Kích hoạt venv**:
  * **Windows (PowerShell)**: `.\.venv\Scripts\Activate.ps1`
  * **Linux/macOS**: `source .venv/bin/activate`

---

## 5. Script chẩn đoán môi trường (kiem_tra_moi_truong)
```python
import sys

def run_diagnostics():
    print(f"Python Version: {sys.version}")
    is_venv = sys.prefix != sys.base_prefix
    print(f"Using virtual environment (venv): {is_venv}")
    try:
        import fastapi
        print(f"FastAPI installed successfully: version {fastapi.__version__}")
    except ImportError:
        print("FastAPI is NOT installed.")

if __name__ == "__main__":
    run_diagnostics()
```

---

## 6. Khởi tạo FastAPI tối giản (ung_dung_fastapi_toi_gian)
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "success", "message": "FastAPI da thiet lap thanh cong!"}
```
