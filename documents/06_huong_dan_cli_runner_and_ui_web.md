# TÀI LIỆU HƯỚNG DẪN 06: HƯỚNG DẪN SỬ DỤNG LỆNH CLI VÀ CÔNG CỤ VẬN HÀNH (ĐÃ KIỂM CHỨNG)

Tài liệu này cung cấp danh sách đầy đủ các câu lệnh CLI đã được **kiểm chứng thực tế (verified & tested)** trên môi trường hệ thống.

---

## 1. Kiểm Tra Trạng Thái và Cấu Hình Hệ Thống

### 1.1. Xem Trợ Giúp và Danh Sách Tùy Chọn CLI
```bash
python main.py --help
```
*Tác dụng: Hiển thị toàn bộ cờ tùy chọn (options) và mô tả cách sử dụng của hệ thống.*

### 1.2. Kiểm Tra Thống Kê Semantic Cache
```bash
python main.py --cache-stats
```
*Tác dụng: Thống kê số lượng response đã cache, số lần cache hit và ước tính token tiết kiệm được.*

### 1.3. Kiểm Tra Cấu Hình Centralized Settings và Secrets
```bash
python -c "from config.settings import get_settings; import json; print(json.dumps(get_settings().redacted_dict(), indent=2))"
```
*Tác dụng: Kiểm tra toàn bộ tham số môi trường và đảm bảo API Key được che giấu an toàn (`***REDACTED***`).*

---

## 2. Lệnh Sinh Học Liệu Chính (Content Generation Workflows)

### 2.1. Sinh Toàn Bộ Học Liệu Cho 1 Session Cụ Thể
```bash
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --approve-pm
```

### 2.2. Sinh Toàn Bộ Khóa Học (Tất cả các Session)
```bash
python main.py --pm "documents/PM_Python.xlsx" --session all --approve-pm
```

### 2.3. Sinh Chọn Lọc Từng Loại Học Liệu (Selective Generation)
Sử dụng cờ `--parts` với danh sách phân tách bằng dấu phẩy (`html`, `slide`, `quiz`, `practical_lab`):
```bash
# Chỉ sinh Bài đọc HTML và Slide bài giảng:
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --parts html,slide --approve-pm

# Chỉ sinh Bài tập và Bộ Quiz trắc nghiệm 45 câu:
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --parts quiz,practical_lab --approve-pm
```

### 2.4. Chạy Xử Lý Bất Đồng Bộ Song Song (Async Parallel Batch Mode)
Kích hoạt chạy song song các Lesson độc lập trong Session để tăng tốc độ sinh học liệu:
```bash
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --parallel --concurrency 4 --approve-pm
```

### 2.5. Khởi Tạo Nhanh Cây Cấu Trúc Thư Mục (Scaffolding Mode)
Khởi tạo cấu trúc thư mục rỗng chuẩn hóa từ file PM mà không cần gọi LLM sinh nội dung chi tiết:
```bash
python main.py --pm "documents/PM_Python.xlsx" --scaffold
```

---

## 3. Lệnh Đóng Gói Xuất Bản (Export LMS và Obsidian Vault)

### 3.1. Xuất Bản Gói SCORM 1.2 Cho Hệ Thống LMS (Moodle / Canvas)
```bash
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --scorm --approve-pm
```
*Kết quả: Tạo file nén `.zip` chuẩn SCORM 1.2 sẵn sàng import vào LMS.*

### 3.2. Xuất Bản Đồ Thị Tri Thức Obsidian Vault
```bash
python main.py --pm "documents/PM_Python.xlsx" --obsidian
```
*Kết quả: Đồng bộ toàn bộ liên kết 2 chiều và thẻ bài học vào thư mục `obsidian_vault/`.*

---

## 4. Lệnh Kiểm Thử và Chẩn Đoán Lõi (Testing & Core Verification)

### 4.1. Chạy Toàn Bộ Test Suite (159 Tests)
```bash
pytest
```

### 4.2. Chạy Kiểm Thử Riêng Cho Từng Module
```bash
# Kiểm thử Quản lý Cấu hình và Bảo mật:
pytest tests/test_centralized_settings.py -v

# Kiểm thử Động cơ Chặn rò rỉ kiến thức (Scope Calculator):
pytest tests/test_scope_calculator.py -v

# Kiểm thử Động cơ Sinh Slide PowerPoint:
pytest tests/test_slide_deck_generator.py -v
```

### 4.3. Kiểm Tra Trực Tiếp Các Module Core Qua Python CLI
```bash
# Kiểm tra danh sách framework bị cấm theo Tech Stack:
python -c "from core.scope_calculator import get_forbidden_frameworks_for_stack; print(get_forbidden_frameworks_for_stack('python/core'))"

# Kiểm tra phân loại Tier của Agent trong LLM Router:
python -c "from core.llm_router import AntigravityLLMRouter; print(AntigravityLLMRouter.classify_agent_tier('reading_creator'))"
```