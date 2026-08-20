# Elearning Content Factory — Multi-Agent Harness & Bộ Sinh Học Liệu Tự Động

> **Hệ thống sản xuất học liệu tự động đa tác nhân (Multi-Agent Harness Architecture) cấp Doanh nghiệp — 100% Dynamic, Generic, Stack-Agnostic, Type-Safe & Schema-Driven.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.12+-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![CI Pipeline](https://img.shields.io/badge/CI%20Pipeline-Passing-2088FF?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![Docker Ready](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![SCORM 1.2](https://img.shields.io/badge/Export-SCORM%201.2-2E7D32)](core/scorm_exporter.py)
[![Obsidian Graph](https://img.shields.io/badge/Knowledge%20Graph-Obsidian%20Markmap-8A2BE2?logo=obsidian&logoColor=white)](obsidian_vault/)

---

## Mục Lục

1. [Giới thiệu tổng quan](#1-giới-thiệu-tổng-quan)
2. [Kiến trúc hệ thống (Agent Harness Architecture)](#2-kiến-trúc-hệ-thống-agent-harness-architecture)
3. [Các loại học liệu hệ thống sinh tự động](#3-các-loại-học-liệu-hệ-thống-sinh-tự-động)
4. [Yêu cầu hệ thống (Prerequisites)](#4-yêu-cầu-hệ-thống-prerequisites)
5. [Hướng dẫn cài đặt chi tiết (Installation Guide)](#5-hướng-dẫn-cài-đặt-chi-tiết-installation-guide)
6. [Quản lý cấu hình & Bảo mật bí mật (Centralized Settings & Secrets)](#6-quản-lý-cấu-hình--bảo-mật-bí-mật-centralized-settings--secrets)
   - [6.1. Chế độ 1: Local Proxy (Antigravity Proxy @ 8045)](#61-chế-độ-1-local-proxy-antigravity-proxy--8045)
   - [6.2. Chế độ 2: API Key thật Google Gemini (Google AI Studio)](#62-chế-độ-2-api-key-thật-google-gemini-google-ai-studio)
7. [Hướng dẫn sử dụng & Khởi chạy hệ thống (Usage Guide)](#7-hướng-dẫn-sử-dụng--khởi-chạy-hệ-thống-usage-guide)
   - [7.1. Chạy CLI Workflow sinh học liệu](#71-chạy-cli-workflow-sinh-học-liệu)
   - [7.2. Chạy kiểm thử tự động (Test Suite)](#72-chạy-kiểm-thử-tự-động-test-suite)
8. [Tự động hóa CI/CD (GitHub Actions)](#8-tự-động-hóa-cicd-github-actions)
9. [Cấu trúc thư mục dự án (Project Layout)](#9-cấu-trúc-thư-mục-dự-án-project-layout)
10. [Quy chuẩn sư phạm & Tiêu chuẩn thiết kế (AGENTS.md)](#10-quy-chuẩn-sư-phạm--tiêu-chuẩn-thiết-kế-agentsmd)
11. [FAQ & Xử lý sự cố thường gặp](#11-faq--xử-lý-sự-cố-thường-gặp)

---

## 1. Giới Thiệu Tổng Quan

**Elearning Content Factory** là hệ thống AI đa tác nhân chuyên nghiệp, tự động hóa toàn bộ quy trình chuyển đổi chương trình đào tạo (`syllabus.json` hoặc file PM Excel) thành bộ tài nguyên học liệu hoàn chỉnh, chuẩn sư phạm và chuẩn kỹ thuật doanh nghiệp cho **mọi công nghệ** (Python, Java, TypeScript/React, Golang, SQL, Docker/DevOps...):

- **100% Tiếng Việt có dấu chuẩn xuất bản**: Toàn bộ nội dung bài đọc, slide, câu hỏi, kịch bản và chú thích mã nguồn được biên soạn bằng tiếng Việt chuẩn ngữ pháp sư phạm.
- **Phân định phạm vi kiến thức động (Dynamic Scope Boundaries)**: Tự động phát hiện và chặn các từ khóa, cú pháp vượt cấp để đảm bảo bài học không dùng kiến thức của các bài học tương lai.
- **Vòng lặp Phản hồi & Tự sửa lỗi (Reflexion Loop)**: Tự động đánh giá chất lượng học liệu (thang đo Bloom, PQM Engine) và kích hoạt cơ chế tự hiệu chỉnh khi phát hiện lỗi.
- **Môi trường thực thi Sandbox an toàn**: Tích hợp Pyodide WASM Engine và Docker Sandbox để chạy và kiểm chứng 100% mã nguồn mẫu trước khi xuất bản bài học.
- **Tương thích LMS Doanh nghiệp & Đồ thị Tri thức**: Hỗ trợ xuất gói SCORM 1.2 cho các nền tảng LMS (Moodle, Canvas, Blackboard) và xuất mạng lưới liên kết tri thức 2 chiều Obsidian Markmap.

---

## 2. Kiến Trúc Hệ Thống (Agent Harness Architecture)

Dự án được thiết kế theo mô hình **Multi-Agent Production & Evaluation Harness**:

```mermaid
flowchart TD
    subgraph InputLayer ["1. Input Layer"]
        PM["Chương trình khung (PM Excel / Syllabus JSON)"]
    end

    subgraph HarnessOrchestrator ["2. Orchestration & State Harness"]
        DAG["DAG Engine / State Machine (core/dag_engine.py)"]
        Scope["Scope Calculator (core/scope_calculator.py)"]
        Cache["Semantic Cache (core/semantic_cache.py)"]
    end

    subgraph AgentSwarm ["3. Multi-Agent Swarm"]
        Creator["Content Creators (Reading, Slides, Labs, Quizzes, HW)"]
        Reviewer["Reviewer Agents (Master Programmatic Validator)"]
        Compiler["Session Compilers (Session Aggregation)"]
    end

    subgraph GuardrailsAndEvals ["4. Guardrails & Evaluation Harness"]
        Sandbox["Code Execution Sandbox (Pyodide / Docker)"]
        Reflexion["Self-Correction Loop (core/reflexion.py)"]
    end

    subgraph OutputLayer ["5. Export Layer"]
        ReadingOut["reading.html & reading_all.html"]
        SlideOut["Slide Bài Giảng (.pptx & slides.html)"]
        HWOut["17 Thư Mục Bài Tập & Rubric"]
        SCORMOut["Gói SCORM 1.2 LMS"]
        ObsidianOut["Obsidian Knowledge Vault"]
    end

    PM --> DAG
    DAG --> Scope
    Scope --> Creator
    Creator --> Sandbox
    Sandbox --> Reviewer
    Reviewer -->|Phát hiện lỗi| Reflexion
    Reflexion -->|Tự sửa lại| Creator
    Reviewer -->|Đạt chuẩn| Compiler
    Compiler --> ReadingOut
    Compiler --> SlideOut
    Compiler --> HWOut
    Compiler --> SCORMOut
    Compiler --> ObsidianOut
```

---

## 3. Các Loại Học Liệu Hệ Thống Sinh Tự Động

| Loại Học Liệu | Định dạng Đầu ra | Đặc tả & Tiêu chuẩn Kỹ thuật |
| :--- | :--- | :--- |
| **Bài đọc lý thuyết** | `reading.html` & `reading_all.html` | Cấu trúc danh sách ngắt ý ngắn gọn, 100% tiếng Việt có dấu, ảnh bối cảnh 16:9, Dark Terminal Console, Self-Test tương tác, Sandbox Pyodide chạy trực tiếp trên trình duyệt. |
| **Slide bài giảng** | `Slide_Bai_Giang.pptx` & `slides.html` | Master Slide (15-20 slides/session), Bento Grid hiện đại, quy tắc 3-30-300 typography, phân màu thẻ kỹ thuật, dàn ý sư phạm chi tiết cho giảng viên. |
| **Bài tập thực hành** | 17 thư mục Markdown + Code files + Rubric | 17 bài tập phân tầng theo thang nhận thức Bloom (Vận dụng cơ bản -> Vận dụng nâng cao -> Sáng tạo -> Tổng hợp). Kèm bảng tiêu chí chấm điểm chi tiết 100 điểm (`tieu_chi_danh_gia.md`). |
| **Mini Project / Lab** | `practical_lab.md` + JSON + Checklist | Bố cục 3 phần chuẩn hóa: Mục tiêu -> Các bước thực hiện -> Bảng checklist tự kiểm tra định lượng `[ ]`. |
| **Quizz Trắc nghiệm** | Excel (`.xlsx`) + JSON | 5 câu/lesson, Entrance Quiz 45 câu (30 câu cũ + 15 câu mới), Exit Quiz 45 câu (100% câu mới). Tuân thủ 9 nguyên tắc sư phạm Quizz. |
| **SCORM 1.2 & Obsidian** | ZIP SCORM 1.2 & Obsidian Vault | Đóng gói tương thích chuẩn e-learning LMS quốc tế và đồ thị mạng lưới tri thức 2 chiều (Obsidian Markmap). |

---

## 4. Yêu Cầu Hệ Thống (Prerequisites)

- **Python**: Phiên bản `3.10`, `3.11`, hoặc `3.12` ([Tải Python](https://www.python.org/downloads/)).
- **Node.js**: Phiên bản `18.0.0+` ([Tải Node.js](https://nodejs.org/)).
- **Git**: Quản lý phiên bản mã nguồn.
- **Docker** *(Tùy chọn)*: Khi sử dụng chế độ Sandbox cô lập hoặc đóng gói container.

---

## 5. Hướng Dẫn Cài Đặt Chi Tiết (Installation Guide)

### Bước 1: Sao chép mã nguồn về máy
```bash
git clone https://github.com/ngoquy12/learning_material.git
cd Learning-Material
```

### Bước 2: Khởi tạo và kích hoạt môi trường ảo Python
- **Trên Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **Trên Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Bước 3: Cài đặt các thư viện phụ thuộc
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 6. Quản Lý Cấu Hình & Bảo Mật Bí Mật (Centralized Settings & Secrets)

Hệ thống sử dụng **Pydantic `BaseSettings`** tại [config/settings.py](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/config/settings.py) để tự động kiểm tra kiểu dữ liệu, che giấu các khóa bí mật (`SecretStr`), và ngăn chặn hoàn toàn việc rò rỉ API key khi ghi log hệ thống.

Khởi tạo file cấu hình `.env` từ file mẫu [`.env.example`](file:///d:/Rikkei%20Education/Elearning_Agent/Learning-Material/.env.example):
```bash
cp .env.example .env
```

### 6.1. Chế độ 1: Local Proxy (Antigravity Proxy @ 8045)
Sử dụng proxy cục bộ (mặc định):
```env
USE_REAL_GEMINI_API_KEY=false
GEMINI_API_KEY=sk-your-proxy-key-here
GEMINI_BASE_URL=http://127.0.0.1:8045
GEMINI_MODEL=gemini-3.6-flash-high
```

### 6.2. Chế độ 2: API Key thật Google Gemini (Google AI Studio)
Khi chuyển sang sử dụng API Key thật của Google, chỉ cần bật cờ `USE_REAL_GEMINI_API_KEY=true` (hệ thống sẽ **tự động bỏ qua proxy `127.0.0.1:8045`** và kết nối trực tiếp đến máy chủ Google):
```env
USE_REAL_GEMINI_API_KEY=true
GEMINI_API_KEY=AIzaSyYourRealGoogleApiKeyHere...
GEMINI_MODEL=gemini-1.5-flash
```

---

## 7. Hướng Dẫn Sử Dụng & Khởi Chạy Hệ Thống (Usage Guide)

### 7.1. Chạy CLI Workflow sinh học liệu

Khởi chạy hệ thống tự động sinh toàn bộ tài nguyên cho một khóa học từ file PM Excel:

```bash
# Sinh toàn bộ học liệu cho Session 01:
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --approve-pm

# Sinh toàn bộ khóa học (tất cả các buổi học):
python main.py --pm "documents/PM_Python.xlsx" --session all --approve-pm

# Chỉ sinh một số thành phần cụ thể (ví dụ Bài đọc và Slide):
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --parts html,slide --approve-pm

# Chạy xử lý bất đồng bộ song song nhiều luồng (Parallel Batch Mode):
python main.py --pm "documents/PM_Python.xlsx" --session "Session 01" --parallel --concurrency 4 --approve-pm

# Khởi tạo nhanh toàn bộ cây cấu trúc thư mục rỗng (Scaffolding Mode):
python main.py --pm "documents/PM_Python.xlsx" --scaffold
```

### 7.2. Chạy kiểm thử tự động (Test Suite)

Thực thi toàn bộ **159 bài kiểm thử** tự động đã được kiểm chứng:

```bash
# Chạy toàn bộ test suite:
pytest

# Chạy test chi tiết kèm báo cáo thu gọn:
pytest -v --tb=short

# Kiểm thử riêng module Quản lý Cấu hình & Bảo mật:
pytest tests/test_centralized_settings.py
```

---

## 8. Tự Động Hóa CI/CD (GitHub Actions)

Dự án tích hợp sẵn 2 pipeline tự động hóa chuẩn doanh nghiệp tại thư mục `.github/workflows/`:

1. **CI Pipeline ([.github/workflows/ci.yml](file:///.github/workflows/ci.yml))**:
   - **Kiểm tra cú pháp (Linting)**: Tự động kiểm tra chất lượng mã nguồn bằng `ruff` và `flake8`.
   - **Kiểm thử ma trận đa phiên bản**: Tự động chạy toàn bộ 159 tests trên 3 phiên bản Python `3.10`, `3.11`, và `3.12` song song với môi trường `Node.js 18`.
   - **Kiểm định Docker Build**: Kiểm tra tính khả thi của quá trình đóng gói container từ `Dockerfile`.
2. **CD Pipeline ([.github/workflows/cd.yml](file:///.github/workflows/cd.yml))**:
   - Tự động đóng gói gói cài đặt Python Wheel Package (`.whl`) khi gắn tag phiên bản (`v*.*.*`).
   - Kiểm tra điểm khởi chạy CLI và lưu trữ các gói phát hành Release Artifacts.

---

## 9. Cấu Trúc Thư Mục Dự Án (Project Layout)

```
Learning-Material/
├── .agents/                      # Quy chuẩn Sư phạm & Tiêu chuẩn Thiết kế (AGENTS.md)
├── .github/                      # Quy trình CI/CD Workflows (GitHub Actions)
│   └── workflows/
│       ├── ci.yml                # Automated Lint, Matrix Tests & Docker Build
│       └── cd.yml                # Automated Package Build & Release
├── agents/                       # Hệ thống Multi-Agent Chuyên biệt
│   ├── creators/                 # Creators (Reading, Slides, Labs, Quizzes, Mindmap)
│   ├── reviewer_agents.py        # Reviewers & Programmatic Validators
│   └── homework_agents.py        # Homework Generators (17 thư mục theo thang Bloom)
├── config/                       # Quản lý Cấu hình Tập trung
│   ├── settings.py               # Pydantic BaseSettings & Secret Management Engine
│   └── prompts.yaml              # Persona & System Prompts
├── core/                         # Động cơ Hạ tầng Lõi (Core Infrastructure)
│   ├── dag_engine.py             # Asynchronous DAG Engine & State Machine
│   ├── graph.py                  # Multi-Agent Workflow Orchestrator
│   ├── llm.py                    # LLM Interface (Gemini Native & OpenAI Proxy)
│   ├── llm_router.py             # Antigravity Dynamic Model Router
│   ├── sandbox.py                # Pyodide / Docker Code Execution Sandbox
│   ├── scope_calculator.py       # Tính toán & Chặn rò rỉ phạm vi kiến thức
│   ├── semantic_cache.py         # Semantic Embedding Cache Engine
│   ├── scorm_exporter.py         # Bộ đóng gói xuất bản SCORM 1.2
│   ├── schemas/                  # Pydantic Declarative Data Schemas
│   ├── renderers/                # Bộ Render HTML, PPTX, CSS, SVG
│   └── validators/               # Master Programmatic Validators & PQM Engine
├── documents/                    # Tài liệu hướng dẫn nghiệp vụ & vận hành
├── obsidian_vault/               # Vault đồ thị liên kết tri thức 2 chiều
├── templates/                    # Jinja2 Templates (Prompts, HTML, CSS, PPTX)
├── tests/                        # Bộ kiểm thử Unit, Integration & Eval Tests (159 tests)
├── .env.example                  # File mẫu cấu hình biến môi trường an toàn
├── .gitignore                    # Bộ lọc bảo mật & chặn rác/output
├── Dockerfile                    # Containerization Manifest
├── pyproject.toml                # Cấu hình dự án & gói phụ thuộc
├── requirements.txt              # Danh sách thư viện Python
└── main.py                       # Điểm khởi chạy CLI chính của hệ thống
```

---

## 10. Quy Chuẩn Sư Phạm & Tiêu Chuẩn Thiết Kế (AGENTS.md)

Mọi nội dung học liệu do Agent sinh ra đều phải tuân thủ nghiêm ngặt **10 Nguyên Tắc Cốt Lõi** quy định tại [.agents/AGENTS.md](file:///.agents/AGENTS.md):

1. **Cấu trúc 5 phần bắt buộc**: Bài toán thực tế -> Cú pháp & Cơ chế -> Ví dụ thực tiễn lũy tiến -> Lỗi thường gặp & Giải pháp -> Tóm tắt & Form tự kiểm tra.
2. **Triết lý 10-Minute Micro-Learning**: Ngắn gọn, súc tích, ngắt ý bằng bullet list, không sử dụng văn bản khối dài.
3. **Tiếp cận từ vấn đề thực tế (Problem-First)**: Luôn xuất phát từ bối cảnh thực tế và bài toán doanh nghiệp trước khi giới thiệu cú pháp lý thuyết.
4. **Chuẩn đồ họa 2D Flat Vector**: Đồ thị Mermaid chuẩn hóa 5 hình khối theo quy chuẩn kỹ thuật, ảnh bối cảnh 16:9 sắc nét, không dùng emoji hoặc hình ảnh 3D cường điệu.
5. **Nghiêm cấm từ ngữ sáo rỗng (AI Cliché)**: Loại bỏ hoàn toàn các từ ngữ sáo rỗng và thay thế bằng thuật ngữ kỹ thuật tiêu chuẩn.
6. **Bảo mật phạm vi kiến thức**: Không sử dụng cú pháp hay câu lệnh của các bài học tương lai trong bài học hiện tại.

---

## 11. FAQ & Xử Lý Sự Cố Thường Gặp

- **Hỏi: Làm sao để chuyển đổi giữa Local Proxy và Google Gemini API Key thật?**
  - *Trả lời:* Trong file `.env`, chuyển `USE_REAL_GEMINI_API_KEY=true` và dán API Key `AIzaSy...` của bạn vào `GEMINI_API_KEY`. Hệ thống sẽ tự động bỏ qua proxy.
- **Hỏi: Thư mục `output/` có bị đẩy lên GitHub không?**
  - *Trả lời:* Không. File `.gitignore` đã chặn toàn bộ thư mục `output/` để giữ repository luôn sạch sẽ và bảo mật dữ liệu học liệu nội bộ.
- **Hỏi: Gặp lỗi hiển thị tiếng Việt trên Windows PowerShell?**
  - *Trả lời:* Hệ thống đã tự động cấu hình UTF-8. Nếu terminal hiển thị sai ký tự, hãy chạy lệnh `$env:PYTHONIOENCODING="utf-8"` trên PowerShell trước khi thực thi lệnh.
