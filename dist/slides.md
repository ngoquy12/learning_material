---
marp: true
theme: gaia
_class: lead
paginate: true
---

# Session 02 - Lesson 06:
## Bản chất của OpenAPI trong FastAPI
**(Bổ sung từ AI)**

---

## Vấn đề & Hiểu lầm phổ biến

* **Sự tiện lợi:** Giao diện Swagger UI tự động sinh ra tại `/docs` làm việc kiểm thử API cực kỳ nhanh chóng.
* **Hiểu lầm:** Nhiều nhà phát triển nghĩ rằng Swagger UI đọc mã nguồn Python theo thời gian thực hoặc FastAPI trực tiếp dựng HTML giao diện này.
* **Hậu quả:** Khi cần tùy biến bảo mật API, cấu hình metadata hoặc tích hợp hệ thống frontend bên ngoài, bạn sẽ gặp bế tắc nếu không hiểu cơ chế thực sự phía sau.

---

## Phân tích bản chất vận hành

* FastAPI vận hành dựa trên **OpenAPI Specification (OAS)**.
* Khi khởi chạy, FastAPI phân tích mã nguồn (routers, Pydantic models, metadata) để tạo ra tập tin JSON duy nhất: `/openapi.json`.
* Swagger UI thực chất là một ứng dụng client HTML/JS độc lập. 
* Khi tải trang `/docs`, Swagger UI gửi HTTP request để kéo `/openapi.json` về, phân tích cú pháp (parse) rồi vẽ giao diện đồ họa.

---

## Sơ đồ Quy trình Hoạt động

<div align="center">
<svg viewBox="0 0 600 100" width="100%" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="20" width="120" height="50" rx="6" fill="#1e293b" stroke="#6366f1" stroke-width="2"/>
  <text x="70" y="50" fill="#f8fafc" font-size="11" text-anchor="middle" font-family="monospace">FastAPI Code</text>
  <path d="M 130 45 L 210 45" stroke="#8b5cf6" stroke-width="2" fill="none"/>
  <polygon points="215,45 205,40 205,50" fill="#8b5cf6"/>
  <rect x="220" y="20" width="140" height="50" rx="6" fill="#312e81" stroke="#8b5cf6" stroke-width="2"/>
  <text x="290" y="50" fill="#f8fafc" font-size="11" text-anchor="middle" font-family="monospace">openapi.json</text>
  <path d="M 360 45 L 440 45" stroke="#10b981" stroke-width="2" fill="none"/>
  <polygon points="445,45 435,40 435,50" fill="#10b981"/>
  <rect x="450" y="20" width="130" height="50" rx="6" fill="#064e3b" stroke="#10b981" stroke-width="2"/>
  <text x="515" y="50" fill="#f8fafc" font-size="11" text-anchor="middle" font-family="monospace">Swagger UI (docs)</text>
</svg>
</div>

---

## Khái niệm cốt lõi (Phần 1)

* **OpenAPI Specification (OAS):** Tiêu chuẩn đặc tả mở dùng để mô tả API RESTful dưới dạng JSON/YAML, giúp cả người và máy hiểu cấu trúc API.
* **Cơ chế tự động hóa Schema:** Khả năng tự động ánh xạ cấu trúc dữ liệu của các hàm Python truyền thống và lớp BaseModel của Pydantic thành các OpenAPI Schema tương thích.
* **openapi.json:** Tập tin JSON do FastAPI tự động tạo, lưu đặc tả chi tiết về endpoints, HTTP methods, parameters và schema.

---

## Khái niệm cốt lõi (Phần 2)

* **Metadata cấu hình:** Các thông tin mô tả ứng dụng như title, description, version, và openapi_url được truyền vào khi khởi tạo FastAPI.
* **Request/Response Schema:** Cấu trúc dữ liệu đầu vào (Request Body) và đầu ra (Response Body) từ các lớp Pydantic, giúp đồng bộ hóa trực tiếp với Swagger UI.

---

## Demo 1: Tự động chuyển đổi Pydantic sang Schema

FastAPI tự động chuyển đổi cấu trúc lớp Pydantic thành đặc tả OpenAPI Schema:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Khai báo cấu trúc dữ liệu bằng Pydantic
class SanPham(BaseModel):
    ten: str
    gia: float

# FastAPI tự động chuyển đổi lớp SanPham thành OpenAPI Schema
@app.post("/san-pham/")
def tao_san_pham(item: SanPham):
    return item
```

---

## Demo 2: Cấu hình Metadata cho API

Tùy biến các thông tin hiển thị trên Swagger UI thông qua tham số khởi tạo:

```python
from fastapi import FastAPI

# Tùy biến metadata hiển thị trên Swagger UI
app = FastAPI(
    title="API Cửa Hàng Tiện Lợi",
    description="Đây là hệ thống API quản lý kho và bán hàng tự động.",
    version="2.1.0",
    openapi_url="/he-thong/openapi.json"
)

@app.get("/check-in")
def health_check():
    return {"status": "hoat_dong"}
```

---

## Demo 3: Đồng bộ hóa cấu trúc Request/Response

Sử dụng `response_model` giúp đồng bộ giao diện Swagger UI phản ánh đúng cấu trúc dữ liệu trả ra:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Schema cho Request Body gửi lên
class KhachHangDangKy(BaseModel):
    username: str
    mat_khau: str

# Schema cho Response Body trả về (ẩn đi mật khẩu)
class KhachHangResponse(BaseModel):
    username: str
    trang_thai: bool = True

# Định nghĩa response_model để đồng bộ hóa giao diện Swagger UI
@app.post("/dang-ky/", response_model=KhachHangResponse)
def dang_ky(user: KhachHangDangKy):
    return {"username": user.username, "trang_thai": True}
```

---

## 3 Lỗi thường gặp cần tránh

1. **Cấu hình sai `openapi_url`:** Vô hiệu hóa hoặc cấu hình sai đường dẫn file json khiến Swagger UI không thể load dữ liệu API.
2. **Thiếu hoặc sai kiểu dữ liệu Pydantic:** Làm cho OpenAPI schema sinh ra không mô tả đúng dữ liệu mong đợi thực tế.
3. **Quên cấu hình `response_model`:** Làm mất thông tin mô tả chi tiết của dữ liệu phản hồi (Response Body) trong tài liệu API trực quan.