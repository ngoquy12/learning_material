# 🚀 KẾ HOẠCH TỐI ƯU HÓA & NÂNG CẤP TOÀN DIỆN HỆ THỐNG
## (Master System Optimization & Modernization Plan)

**Dự án:** Elearning Content Factory (Multi-Agent Learning Material Generator)  
**Tác giả:** Senior AI Architect & System Engineering Lead  
**Ngày lập:** 17/08/2026  
**Phiên bản:** v2.1 (Scope: Reading, Slides, Exercises, Labs, Quizzes, Visualizers, SCORM & Obsidian)  
**Tài liệu tham chiếu:** [docs/architecture.md](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/docs/architecture.md), [docs/SOLUTIONS_ARCHITECTURE_ANALYSIS.md](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/docs/SOLUTIONS_ARCHITECTURE_ANALYSIS.md), [.agents/AGENTS.md](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/.agents/AGENTS.md)

---

## 📋 MỤC LỤC

1. [Tóm Tắt Điều Hành (Executive Summary)](#1-tóm-tắt-điều-hành-executive-summary)
2. [Hiện Trạng & Ma Trận Phân Tích Nút Thắt (Bottleneck Matrix)](#2-hiện-trạng--ma-trận-phân-tích-nút-thắt-bottleneck-matrix)
3. [Kiến Trúc Đích Toàn Diện (Target Architecture Blueprint)](#3-kiến-trúc-đích-toàn-diện-target-architecture-blueprint)
4. [Các Trụ Cột Tối Ưu Hóa Chi Tiết (Deep-Dive Optimization Pillars)](#4-các-trụ-cột-tối-ưu-hóa-chi-tiết-deep-dive-optimization-pillars)
   - [Trụ cột 1: Chuẩn hóa Kiến trúc Module & Xử lý Nợ Kỹ thuật (Clean Architecture & Refactoring)](#trụ-cột-1-chuẩn-hóa-kiến-trúc-module--xử-lý-nợ-kỹ-thuật)
   - [Trụ cột 2: Tự động hóa Kiểm thử & CI/CD Mocking Strategy](#trụ-cột-2-tự-động-hóa-kiểm-thử--cicd-mocking-strategy)
   - [Trụ cột 3: Hiệu Năng, Concurrency & Quản Trị Chi Phí LLM/Cache](#trụ-cột-3-hiệu-năng-concurrency--quản-trị-chi-phí-llmcache)
   - [Trụ cột 4: Trừu tượng hóa Hạ tầng & Sẵn sàng Phân tán (Cloud-Ready & Distributed Scaling)](#trụ-cột-4-trừu-tượng-hóa-hạ-tầng--sẵn-sàng-phân-tán)
   - [Trụ cột 5: Automated Visual QA & Mở Rộng Chỉ Số PQM Engine](#trụ-cột-5-automated-visual-qa--mở-rộng-chỉ-số-pqm-engine)
5. [Lộ Trình Thực Hiện & Phân Kỳ (Actionable Milestones & Roadmap)](#5-lộ-trình-thực-hiện--phân-kỳ-actionable-milestones--roadmap)
6. [Ma Trận Đánh Giá Hiệu Quả & Chỉ Số Thành Công (KPIs & Metrics)](#6-ma-trận-đánh-giá-hiệu-quả--chỉ-số-thành-công-kpis--metrics)
7. [Kế Hoạch Quản Trị Rủi Ro (Risk Management & Fallback Strategies)](#7-kế-hoạch-quản-trị-rủi-ro-risk-management--fallback-strategies)

---

## 1. TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

Hệ thống **Elearning Content Factory** tập trung tối đa nguồn lực vào việc sản xuất bộ tài nguyên học liệu cốt lõi chất lượng cao nhất: **Bài đọc HTML tương tác (Pyodide Wasm Sandbox), Master Slide Bento Grid, Bộ 6 bài tập phân tầng Bloom, Lab thực hành theo dự án, Đề trắc nghiệm chuẩn sư phạm, Gói SCORM 1.2 cho LMS và Obsidian Vault Knowledge Graph**.

Nhằm tinh gọn hệ thống và tập trung vào thế mạnh cốt lõi, toàn bộ cấu phần HyperFrames video thử nghiệm đã được loại bỏ. Bản kế hoạch tối ưu hóa v2.1 tập trung giải quyết 3 bài toán trọng tâm:

1. **Nợ kỹ thuật về cấu trúc module và kiểm thử**: Chuẩn hóa import namespace, thiết lập mock layers để test suite chạy offline $100\%$ `< 15s`.
2. **Nâng cấp Pydantic v2 & Web API**: Đồng bộ hóa toàn bộ schemas `web/backend` sang `ConfigDict` và chuẩn hóa luồng xử lý API.
3. **Quản trị chi phí token & Sẵn sàng Cloud**: Tích hợp Token Bucket Rate Limiter, Gemini Context Caching cho giáo trình lớn, và xây dựng lớp `StorageProvider` (Local FS / S3 / MinIO).

---

## 2. HIỆN TRẠNG & MA TRẬN PHÂN TÍCH NÚT THẮT (BOTTLENECK MATRIX)

| Mã | Hạng mục | Vấn đề hiện tại | Mức độ ảnh hưởng | Mức độ ưu tiên | Giải pháp giải quyết |
|---|---|---|:---:|:---:|---|
| **B-01** | **Test Suite & CI/CD** | `test_pptx_generator.py` lỗi import; `test_evaluation_llm.py` treo vì gọi API live; thiếu mock layers. | 🔴 Critical | **P0 (Ngay lập tức)** | Chuẩn hóa import namespace, thiết lập `pytest-mock` & fixture recording. |
| **B-02** | **Code Organization** | Tồn tại song song file đơn lẻ ở `agents/` và thư mục con `agents/creators/`. | 🟡 High | **P0 (Ngay lập tức)** | Hoàn thiện refactor 100% sang `agents/creators/`, `agents/compilers/`, `agents/reviewers/`. |
| **B-03** | **Pydantic V2 Migration** | Cảnh báo `PydanticDeprecatedSince20` trong `web/backend/app/schemas/`. | 🟢 Medium | **P1 (Tuần 1)** | Nâng cấp sang `model_config = ConfigDict(...)`. |
| **B-04** | **Distributed Scaling** | SQLite WAL & Local Storage gây khó khăn khi scale nhiều workers cùng xử lý 1 khóa học lớn. | 🔴 Critical | **P1 (Tuần 2)** | Thiết kế `StorageProvider` (Local/S3) & Task Queue (Celery/Redis). |
| **B-05** | **Visual Layout Testing** | Mới chỉ lint bằng RegEx HTML, chưa chụp ảnh giao diện thực tế để bắt lỗi vỡ layout Bento Grid. | 🟡 High | **P2 (Tuần 3)** | Tích hợp Playwright Visual Headless Screenshot & Layout Linter. |

---

## 3. KIẾN TRÚC ĐÍCH TOÀN DIỆN (TARGET ARCHITECTURE BLUEPRINT)

```
                                  ┌────────────────────────────────┐
                                  │       CLI / Web API Server     │
                                  │   (FastAPI + Pydantic v2 + WS) │
                                  └───────────────┬────────────────┘
                                                  │ Dispatches Jobs
                                                  ▼
                                  ┌────────────────────────────────┐
                                  │   Asynchronous Worker Pool     │
                                  │     (Antigravity DAG Engine)   │
                                  ├────────────────────────────────┤
                                  │ • Dynamic Model Tier Router    │
                                  │ • Semantic Offline Cache (WAL) │
                                  │ • Gemini Context Caching       │
                                  │ • Scope Boundary Governance    │
                                  │ • Pyodide / Sandbox Validation │
                                  └───────────────┬────────────────┘
                                                  │
                                                  ▼
                                  ┌────────────────────────────────┐
                                  │  Multi-Target Publisher Node   │
                                  ├────────────────────────────────┤
                                  │ • HTML Master Compiler         │
                                  │ • Marp Slide Engine            │
                                  │ • SCORM 1.2 Packager           │
                                  │ • Obsidian Vault Graph Linker  │
                                  │ • Excel 13-Column Quiz Exporter│
                                  └───────────────┬────────────────┘
                                                  │
                                                  ▼
                      ┌──────────────────────────────────────┐
                      │      Unified Storage Abstraction     │
                      │  • State: PostgreSQL / SQLite WAL    │
                      │  • Artifacts: S3 / MinIO / Local FS  │
                      │  • Traces: OpenTelemetry + Langfuse  │
                      └──────────────────────────────────────┘
```

---

## 4. CÁC TRỤ CỘT TỐI ƯU HÓA CHI TIẾT (DEEP-DIVE OPTIMIZATION PILLARS)

### TRỤ CỘT 1: CHUẨN HÓA KIẾN TRÚC MODULE & XỬ LÝ NỢ KỸ THUẬT

#### 1.1. Tái cấu trúc Thư mục `agents/`
- **Mục tiêu**: Xóa bỏ hoàn toàn tình trạng duplicate file và import vòng giữa thư mục gốc và thư mục con.
- **Cấu trúc chuẩn hóa**:
  ```
  agents/
  ├── creators/
  │   ├── blueprint_creator.py
  │   ├── reading_creator.py
  │   ├── slide_creator.py
  │   ├── quiz_creator.py
  │   ├── practical_lab_creator.py
  │   ├── reading_questions_creator.py
  │   ├── visualizer_creator.py
  │   └── mindmap_creator.py
  ├── reviewers/
  │   ├── pm_reviewer.py
  │   ├── prerequisite_guard.py
  │   ├── reading_ui_reviewer.py
  │   ├── quiz_reviewer.py
  │   └── sandbox_testing_reviewer.py
  ├── compilers/
  │   ├── session_reading_compiler.py
  │   ├── session_slide_compiler.py
  │   └── session_mindmap_compiler.py
  └── shared/
      ├── base_agent.py
      └── agent_prompts.py
  ```

#### 1.2. Nâng cấp Pydantic v2 trong Web Backend
- Thay thế toàn bộ cấu trúc cũ `class Config: orm_mode = True` trong [web/backend/app/schemas/](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/web/backend/app/schemas) bằng:
  ```python
  from pydantic import BaseModel, ConfigDict

  class LessonResponse(LessonBase):
      id: int
      model_config = ConfigDict(from_attributes=True)
  ```

---

### TRỤ CỘT 2: TỰ ĐỘNG HÓA KIỂM THỬ & CI/CD MOCKING STRATEGY

#### 2.1. Phân tầng Kiểm thử (3-Tier Test Strategy)
1. **Tier 1: Unit Tests (100% Offline, Fast < 5s)**
   - Test logic state reducers trong [antigravity.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/antigravity.py).
   - Test tính toán phạm vi trong [core/scope_calculator.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/core/scope_calculator.py).
   - Test các hàm linting/validation cú pháp HTML/Mermaid trong [core/validators/](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/core/validators).
2. **Tier 2: Mocked Pipeline Integration Tests (Offline < 15s)**
   - Sử dụng `unittest.mock.patch` hoặc `pytest_mock` giả lập phản hồi của `call_llm_api`.
   - Kiểm thử toàn vẹn luồng DAG `compile_learning_content_workflow` từ Giai đoạn 0 đến Giai đoạn 5 mà không tốn token/thời gian chờ mạng.
3. **Tier 3: E2E Quality Benchmark (Chạy định kỳ / Trigger thủ công)**
   - Đánh giá chất lượng thực tế bằng `LLM-as-a-judge` và Sandbox Execution trên môi trường Staging.

#### 2.2. Khắc phục lỗi Test hiện tại
- Sửa file [tests/test_pptx_generator.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/tests/test_pptx_generator.py): Cập nhật đường dẫn import chuẩn xác từ `agents.slide_generator_agent` hoặc `agents.creators.slide_creator`.
- Thêm cờ `--skip-live-llm` hoặc biến môi trường `RUN_LIVE_LLM_TESTS=false` cho [tests/test_evaluation_llm.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/tests/test_evaluation_llm.py) và [tests/test_e2e_pipeline.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/tests/test_e2e_pipeline.py).

---

### TRỤ CỘT 3: HIỆU NĂNG, CONCURRENCY & QUẢN TRỊ CHI PHÍ LLM/CACHE

#### 3.1. Centralized Token Bucket Rate Limiter
- Trong [core/llm.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/core/llm.py), bổ sung cơ chế **Token Bucket Algorithm** kết hợp với `_LLM_SEMAPHORE` hiện tại:
  - Tự động điều chỉnh tần suất gửi request theo RPM (Requests Per Minute) và TPM (Tokens Per Minute) của từng Model Tier.
  - Tự động Backoff theo Exponential Jitter khi gặp mã lỗi `429 (Resource Exhausted)`.

#### 3.2. Nâng cấp Semantic Cache & Context Caching
- **Context Caching Warm-up**: Tự động nhận diện các giáo trình lớn (> 32k tokens) và khởi tạo cache trước (Warm-up) tại Node `lock_ssot` để các Creators phía sau (Reading, Slides, Lab) dùng chung cùng một cache handle, giảm 90% latency và chi phí input token.
- **Cache Eviction Policy**: Bổ sung cơ chế tự động dọn dẹp các cache record quá hạn (TTL 30 ngày) và nén dữ liệu response bằng `zlib`.

---

### TRỤ CỘT 4: TRỪU TƯỢNG HÓA HẠ TẦNG & SẴN SÀNG PHÂN TÁN

#### 4.1. Storage Provider Abstraction Layer
- Thiết lập interface thống nhất trong `core/storage/`:
  ```python
  from abc import ABC, abstractmethod

  class BaseStorageProvider(ABC):
      @abstractmethod
      def save_artifact(self, path: str, content: bytes) -> str: pass
      @abstractmethod
      def load_artifact(self, path: str) -> bytes: pass
      @abstractmethod
      def exists(self, path: str) -> bool: pass

  class LocalStorageProvider(BaseStorageProvider): ...
  class S3StorageProvider(BaseStorageProvider): ...      # MinIO / AWS S3
  ```

#### 4.2. Asynchronous Job Processing cho Multi-Session Batching
- Tận dụng `asyncio` worker pool hoặc Celery Queue để sinh song song nhiều Session trong một Curriculum mà không block luồng Web API.

---

### TRỤ CỘT 5: AUTOMATED VISUAL QA & MỞ RỘNG CHỈ SỐ PQM ENGINE

#### 5.1. Visual Regression Linter (Playwright / Puppeteer)
- Tích hợp module [core/validators/visual_linter.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/core/validators/visual_linter.py):
  1. Khởi chạy browser không đầu (Headless Browser) render file `reading.html` và `slides.html`.
  2. Bắt lỗi tràn màn hình (Overflow X/Y), thẻ bị che khuất (Overlap).
  3. Kiểm tra độ tương phản màu sắc đạt chuẩn WCAG AA (tối thiểu 4.5:1).
  4. Chụp screenshot lưu vào thư mục `reports/visual_diff/` phục vụ kiểm duyệt trực quan.

#### 5.2. Nâng cấp Pedagogical Quality Scoring (PQM)
- Mở rộng [core/quality_evaluator.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/core/quality_evaluator.py) từ 4 lên 6 tiêu chí định lượng:
  1. **Bloom Cognitive Alignment** (Độ phủ 4 bậc nhận thức).
  2. **Code Health & Safety Ratio** (% Code vượt qua Sandbox an toàn).
  3. **Anti-AI Cliche Ban Index** (Phát hiện từ sáo rỗng, bẫy từ cấm).
  4. **Strict Scope Compliance** (Tỷ lệ tuân thủ ranh giới kiến thức Bài 1..N).
  5. **Visual Layout Balance** (Độ cân xứng Bento Grid & biểu đồ Mermaid).
  6. **Real-World Business Scenario Relevance** (Độ sát thực tế doanh nghiệp).

---

## 5. LỘ TRÌNH THỰC HIỆN & PHÂN KỲ (ACTIONABLE MILESTONES & ROADMAP)

```
Tuần:        [Tuần 1]              [Tuần 2]              [Tuần 3]
             ────────              ────────              ────────
Sprint 1:    [Fix Imports & CI]
             [Pydantic v2 Fix]
Sprint 2:                          [Refactor Agents]
                                   [Rate Limiter & Cache]
Sprint 3:                                                [Storage Layer]
                                                         [Visual Linter & PQM]
```

### 📅 GIAI ĐOẠN 1: ỔN ĐỊNH HÓA & DỌN DẸP CODEBASE (Sprint 1 - Tuần 1)
- [ ] **M1.1**: Sửa toàn bộ lỗi import trong `tests/` và thiết lập mock fixtures cho LLM calls.
- [ ] **M1.2**: Đưa toàn bộ test suite pass $100\%$ với thời gian chạy `< 15s`.
- [ ] **M1.3**: Nâng cấp toàn bộ Schemas trong `web/backend` sang Pydantic v2 `ConfigDict`.

### 📅 GIAI ĐOẠN 2: CHUẨN HÓA MODULE & QUẢN TRỊ RATE LIMIT (Sprint 2 - Tuần 2)
- [ ] **M2.1**: Hoàn tất hợp nhất các file agent rời rạc vào `agents/creators/` và `agents/compilers/`.
- [ ] **M2.2**: Bổ sung Token Bucket Rate Limiter và Exponential Backoff trong `core/llm.py`.
- [ ] **M2.3**: Tối ưu SQLite WAL connection pool và bổ sung auto-eviction cho Semantic Cache.

### 📅 GIAI ĐOẠN 3: SCALE HẠ TẦNG & VISUAL QA (Sprint 3 - Tuần 3)
- [ ] **M3.1**: Xây dựng lớp `BaseStorageProvider` và adapter `LocalStorageProvider` / `S3StorageProvider`.
- [ ] **M3.2**: Hoàn thiện Headless Browser Visual Linter tự động chụp ảnh bắt lỗi vỡ giao diện.
- [ ] **M3.3**: Mở rộng PQM Quality Evaluator lên 6 tiêu chí định lượng và lưu trữ lịch sử báo cáo.

---

## 6. MA TRẬN ĐÁNH GIÁ HIỆU QUẢ & CHỈ SỐ THÀNH CÔNG (KPIS & METRICS)

| Chỉ số Đánh giá (KPI) | Giá trị Hiện tại | Mục tiêu Sau Tối ưu | Phương pháp Đo lường |
|---|:---:|:---:|---|
| **Thời gian chạy Test Suite CI/CD** | Bị lỗi / Treo (> 60s) | **< 15 giây (Pass 100%)** | `pytest tests/` với Mock Layer |
| **Tỷ lệ lỗi Rate Limit (429 HTTP)** | ~8 - 12% khi chạy batch | **< 0.5%** | Token Bucket Limiter & Jitter Retry |
| **Thời gian sinh 1 Session đầy đủ** | 3 - 5 phút | **< 1.5 phút** | Gemini Context Cache + Async Parallel |
| **Tỷ lệ Cache Hit của Semantic Cache** | ~40% | **> 75% khi re-build** | Semantic SQLite Cache Engine |
| **Điểm Đánh giá Chất lượng PQM** | 82/100 | **> 95/100** | PQM Engine (6 tiêu chí) |

---

## 7. KẾ HOẠCH QUẢN TRỊ RỦI RO (RISK MANAGEMENT & FALLBACK STRATEGIES)

1. **Rủi ro R-01 (API Quota Spike & 429 Errors)**:
   - *Biện pháp kiểm soát*: Kích hoạt Fallback giữa các model Gemini trong cùng Tier (`gemini-3.6-flash-high` ➔ `gemini-2.0-flash` ➔ `gemini-1.5-flash`).
2. **Rủi ro R-02 (Visual Lint False Positives)**:
   - *Biện pháp kiểm soát*: Điều chỉnh pixel difference threshold (tolerance đạt 98%).
3. **Rủi ro R-03 (Bảo toàn dữ liệu cũ khi refactor module)**:
   - *Biện pháp kiểm soát*: Tạo alias backwards-compatibility trong `agents/__init__.py` để đảm bảo code bên ngoài vẫn import được trong suốt quá trình chuyển giao.
