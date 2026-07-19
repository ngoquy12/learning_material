---
markmap:
  colorFreezeLevel: 3
---
# Session 02 - Giới thiệu & Cài đặt FastAPI cơ bản

## Lesson 01: Tổng quan kiến trúc web và FastAPI

### Mục tiêu bài học
- Nắm vững nguyên lý hoạt động của mô hình Client-Server và giao thức HTTP.
- Làm chủ cách thiết lập môi trường ảo và khởi tạo dự án FastAPI độc lập.
- Xây dựng, cấu hình và vận hành thành công Endpoint đầu tiên bằng Uvicorn.

### Mô hình Client-Server
#### Khái niệm cốt lõi
- Mô hình mạng phân chia vai trò rõ rệt giữa bên gửi yêu cầu (Client) và bên tiếp nhận, xử lý và phản hồi (Server).
#### Cú pháp & Cách khai báo
- Không áp dụng cú pháp code trực tiếp cho mô hình kiến trúc hệ thống.
#### Lưu ý thực chiến
- Server phải luôn hoạt động ở trạng thái lắng nghe và sẵn sàng xử lý yêu cầu gửi đến từ Client.
- ![](../images/mindmap_img_1.png)

### Giao thức HTTP
#### Khái niệm cốt lõi
- Giao thức truyền tải siêu văn bản dạng Request-Response, hoạt động trên tầng ứng dụng và không lưu trạng thái (Stateless).
#### Cú pháp & Cách khai báo
- Cấu trúc bản tin HTTP gồm: Start Line, HTTP Headers, và Message Body.
#### Lưu ý thực chiến
- Sử dụng đúng phương thức HTTP (GET, POST, PUT, DELETE) và mã trạng thái (2xx, 4xx, 5xx) để đảm bảo chuẩn RESTful API.
- ![](../images/mindmap_img_2.png)

### Môi trường ảo (Virtual Environment)
#### Khái niệm cốt lõi
- Không gian hoạt động biệt lập cho từng dự án Python nhằm cô lập các thư viện, tránh xung đột phiên bản hệ thống.
#### Cú pháp & Cách khai báo
- Khởi tạo và kích hoạt môi trường ảo:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
#### Lưu ý thực chiến
- Quên kích hoạt môi trường ảo (venv) dẫn đến lỗi chạy sai phiên bản Python hoặc không tìm thấy thư viện khi deploy.

### FastAPI
#### Khái niệm cốt lõi
- Một Web Framework hiện đại, hiệu năng cao phục vụ xây dựng Web API bằng Python dựa trên chuẩn OpenAPI và Pydantic.
#### Cú pháp & Cách khai báo
- Khởi tạo ứng dụng FastAPI:
  ```python
  from fastapi import FastAPI
  app = FastAPI()
  ```
#### Lưu ý thực chiến
- Tránh khởi tạo nhiều thực thể app trong cùng một tệp nguồn khi chưa có cấu hình định tuyến cha-con rõ ràng.

### Uvicorn (ASGI)
#### Khái niệm cốt lõi
- Máy chủ Web ASGI hiệu năng cao, chịu trách nhiệm nhận yêu cầu bất đồng bộ và chuyển tiếp cho ứng dụng FastAPI xử lý.
#### Cú pháp & Cách khai báo
- Cài đặt và khởi chạy máy chủ phát triển:
  ```bash
  pip install uvicorn
  uvicorn main:app --reload
  ```
#### Lưu ý thực chiến
- Chỉ định sai tên tệp chứa thực thể app (ví dụ main:app) sẽ khiến trình chạy Uvicorn báo lỗi không tìm thấy ứng dụng.

### Endpoint
#### Khái niệm cốt lõi
- Điểm cuối kết nối được xác định bởi sự kết hợp giữa một đường dẫn cụ thể (URI) và một phương thức HTTP.
#### Cú pháp & Cách khai báo
- Khai báo một Router Endpoint cơ bản:
  ```python
  @app.get("/")
  def read_root():
      return {"message": "Hello World"}
  ```
#### Lưu ý thực chiến
- Định nghĩa trùng lặp đường dẫn và phương thức HTTP sẽ dẫn đến việc ghi đè logic của các Endpoint định nghĩa trước đó.
```
```

## Lesson 02: Thiết lập môi trường và Virtual Environment

### Mục tiêu bài học
- Hiểu bản chất và thiết lập thành công môi trường ảo venv để cô lập dự án.
- Sử dụng thành thạo công cụ pip để quản lý các gói thư viện Python.
- Nắm vững cách quản lý phần phụ thuộc của dự án qua tệp requirements.txt.

### môi trường ảo (venv)
#### Khái niệm cốt lõi
- Không gian hoạt động độc lập chứa bản sao Python và thư viện riêng, ngăn chặn xung đột phiên bản giữa các dự án.
- ![](../images/mindmap_img_1.png)
#### Cú pháp & Cách khai báo
- Khởi tạo và kích hoạt:
  ```bash
  # Khởi tạo thư mục môi trường ảo
  python -m venv venv

  # Kích hoạt trên macOS/Linux
  source venv/bin/activate

  # Kích hoạt trên Windows (PowerShell)
  venv\Scripts\Activate.ps1
  ```
#### Lưu ý thực chiến
- Không tạo thư mục venv lồng nhau bên trong một thư mục venv khác.
- Tuyệt đối không đẩy thư mục venv lên kho lưu trữ Git để tránh tốn dung lượng.

### pip (Package Installer for Python)
#### Khái niệm cốt lõi
- Hệ thống quản lý mã nguồn mở giúp tải và cài đặt các thư viện Python từ kho lưu trữ trung tâm PyPI.
#### Cú pháp & Cách khai báo
- Cài đặt thư viện:
  ```bash
  # Cài đặt thư viện cần thiết cho Stack công nghệ
  pip install fastapi sqlalchemy pymysql

  # Gỡ bỏ thư viện không cần thiết
  pip uninstall pymysql
  ```
#### Lưu ý thực chiến
- Luôn kiểm tra xem môi trường ảo đã được kích hoạt trước khi dùng lệnh cài đặt.
- Sử dụng pip list để kiểm tra nhanh các gói thư viện hiện diện trong môi trường ảo hiện tại.

### requirements.txt
#### Khái niệm cốt lõi
- Tệp văn bản lưu trữ danh sách và phiên bản chính xác của các thư viện bên thứ ba giúp đồng bộ môi trường phát triển giữa các lập trình viên.
#### Cú pháp & Cách khai báo
- Xuất và cài đặt môi trường:
  ```bash
  # Xuất danh sách thư viện đang cài đặt trong venv
  pip freeze > requirements.txt

  # Cài đặt môi trường từ tệp cấu hình có sẵn
  pip install -r requirements.txt
  ```
#### Lưu ý thực chiến
- Cần chạy lại lệnh kết xuất pip freeze mỗi khi cài đặt thêm thư viện mới cho dự án.
- Bắt buộc phải đưa tệp requirements.txt vào hệ thống kiểm soát phiên bản Git.
```
```

## Lesson 03: Khởi tạo ứng dụng FastAPI
### Mục tiêu bài học
- Hiểu tổng quan về FastAPI và vai trò của ASGI Server Uvicorn.
- Khởi tạo môi trường ảo và xây dựng ứng dụng FastAPI đầu tiên.
- Vận hành ứng dụng web bằng Uvicorn với chế độ tự động tải lại.
### Tổng quan về FastAPI và ASGI Server Uvicorn
#### Khái niệm lý thuyết
- FastAPI là web framework hiệu năng cao cho Python 3.8+, thiết kế dựa trên tiêu chuẩn Python type hints.
- Uvicorn là máy chủ web chuẩn ASGI đóng vai trò cầu nối tiếp nhận HTTP request và chuyển giao cho ứng dụng FastAPI.
#### Lưu ý
- Khác với chuẩn WSGI truyền thống, ASGI hỗ trợ xử lý bất đồng bộ, WebSockets và cơ chế async/await.
### Khởi tạo Môi trường và Ứng dụng FastAPI Đầu tiên
#### Khái niệm lý thuyết
- Môi trường ảo (venv) giúp cô lập các thư viện phụ thuộc và tránh xung đột phiên bản hệ thống.
- Đối tượng FastAPI quản lý cấu hình và định tuyến, kết hợp với Path Operation Decorator để liên kết URL với hàm xử lý.
#### Cấu trúc cú pháp
- Khởi tạo môi trường và viết ứng dụng:
    ```python
    # Tạo và kích hoạt venv
    python -m venv venv
    source venv/bin/activate

    # Cài đặt thư viện
    pip install fastapi uvicorn

    # Mã nguồn main.py
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"message": "Chào mừng bạn đến với FastAPI!"}
    ```
#### Lưu ý
- Quên kích hoạt môi trường ảo venv sẽ dẫn đến lỗi ModuleNotFoundError: No module named 'fastapi'.
### Vận hành và Tự động Tải lại với Uvicorn
#### Khái niệm lý thuyết
- Uvicorn vận hành ứng dụng FastAPI thông qua câu lệnh CLI với cú pháp uvicorn <tên_file>:<tên_instance>.
- Cờ --reload cho phép Uvicorn tự động khởi động lại server khi phát hiện thay đổi trong mã nguồn.
#### Cấu trúc cú pháp
- Lệnh khởi chạy server:
    ```bash
    uvicorn main:app --reload
    ```
#### Lưu ý
- Nhập sai tên file hoặc tên instance (ví dụ file app.py nhưng gõ main:app) sẽ gây lỗi không tìm thấy ứng dụng.
- Không sử dụng cờ --reload trong môi trường Production vì tiêu tốn tài nguyên hệ thống.
