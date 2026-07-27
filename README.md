# 🤖 Elearning Content Factory — Multi-Agent Learning Material Generator

> **Hệ thống sản xuất học liệu tự động đa tác nhân (Multi-Agent Architecture) quy mô lớn — 100% Dynamic, Generic, Stack-Agnostic & Schema-Driven (Tuyệt đối Không Hardcode).**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![LangGraph / Antigravity](https://img.shields.io/badge/Orchestration-Antigravity-purple)](.)
[![Schema-Driven](https://img.shields.io/badge/Architecture-Pydantic%20Schema%20Driven-emerald)](.)
[![Zero Hardcode](https://img.shields.io/badge/Stack--Agnostic-100%25%20Generic-orange)](.)
[![SCORM 1.2](https://img.shields.io/badge/Export-SCORM%201.2-green)](.)

---

## 📋 Mục lục

1. [Giới thiệu tổng quan](#-giới-thiệu-tổng-quan)
2. [Kiến trúc hệ thống đa tầng (4-Tier Architecture)](#-kiến-trúc-hệ-thống-đa-tầng-4-tier-architecture)
3. [Các tính năng cốt lõi mới](#-các-tính-năng-cốt-lõi-mới)
4. [Hướng dẫn cài đặt & Khởi chạy](#-hướng-dẫn-cài-đặt--khởi-chạy)
5. [Cấu trúc thư mục dự án](#-cấu-trúc-thư-mục-dự-án)
6. [Quy trình kiểm định lập trình tự động (Master Validation Layer)](#-quy-trình-kiểm-định-lập-trình-tự-động-master-validation-layer)
7. [FAQ & Xử lý lỗi thường gặp](#-faq--xử-lý-lỗi-thường-gặp)

---

## 🌟 Giới thiệu tổng quan

**Elearning Content Factory** là hệ thống AI đa tác nhân tự động hóa việc chuyển đổi chương trình khung `syllabus.json` (hoặc PM Excel) thành bộ tài nguyên học liệu hoàn chỉnh cho **bất kỳ công nghệ nào** (Python, Java, React, SQL, Flutter, DevOps...):

| Loại Tài Nguyên | Định dạng | Công nghệ & Renderer |
|---|---|---|
| 📖 Bài đọc lý thuyết | HTML tương tác | JSON Payload ➔ `reading_renderer.py` + Sandbox Adapter |
| 🖼️ Slide bài giảng | HTML trình chiếu | JSON Payload ➔ `slide_renderer.py` + Tailwind/Reveal |
| ❓ Quiz trắc nghiệm | Excel (.xlsx) + JSON | `quiz_validator.py` + Dynamic Option Shuffler |
| 💻 Bài tập thực hành | Markdown + Code | Python `ast.parse()` + Checklist Guard |
| 🏗️ Đồ án / Project | Markdown + Rubric | Project Rubric 100-Point Sum Validator |
| 📦 SCORM Package | .zip (SCORM 1.2) | SCORM Publisher Engine |

---

## 📌 4 Loại Session Chuẩn Trong Hệ Thống (Standardized Session Types)

Hệ thống hỗ trợ và xử lý tự động **4 loại Session chuẩn**:

1. **`THEORY` — Session Lý Thuyết:** Chứa các bài học con (`Lesson 01`, `Lesson 02`...). Sinh đầy đủ **10 loại đầu ra chuẩn hóa**:
   * *Cấp Bài học (Per-Lesson):* (1) Bài đọc HTML tương tác, (2) Slide bài giảng HTML + Narration, (3) Bài thực hành theo bài (linh hoạt theo nội dung trọng tâm), (4) Quiz trắc nghiệm bài (đúng 5 câu/lesson).
   * *Cấp Phiên học (Per-Session):* (5) Quiz đầu giờ (đúng 45 câu Excel .xlsx), (6) Quiz cuối giờ (đúng 45 câu Excel .xlsx), (7) Bài tập về nhà Session (5 bài 5 cấp độ + 1 bài tổng hợp), (8) File gộp `reading_all.html`, (9) File gộp `session_slides.html`, (10) Kịch bản video Hyperframes.
2. **`PRACTICE` — Session Thực Hành:** Không chứa bài học con. Sinh tập trung các bộ Bài tập thực hành (Labs), Bài tập về nhà (Homework) và Kịch bản kiểm tra trạng thái.
3. **`MINI_PROJECT` — Session Mini Project:** Không chứa bài học con. Sinh 4 Entry Tests, Tài liệu đặc tả SRS tinh gọn và Đề bài Mini Project kèm Rubric 100 điểm.
4. **`FINAL_PROJECT` — Session Dự Án Cuối Khóa:** Không chứa bài học con. Sinh Đồ án Capstone cuối khóa hoàn chỉnh, Kiến trúc hệ thống tổng thể, Tài liệu đặc tả SRS đầy đủ và Rubric chấm 100 điểm.

---

```
                            ╔══════════════════════════════╗
                            ║      Dynamic Syllabus        ║
                            ║    (syllabus.json / PM Excel)║
                            ╚══════════════╤═══════════════╝
                                           │
                            ┌──────────────▼──────────────┐
                            │  Scope Calculator Engine    │  ← Computes Allowed (1..N) &
                            │  (core/scope_calculator.py) │     Forbidden Scope (N+1..End)
                            └──────────────┬──────────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        │   Declarative JSON Payload Schemas  │  ← Pure Content JSON
                        │   (Reading, Slide, Quiz, Project)   │  ← No Raw Mixed HTML/JS
                        └──────────────────┬──────────────────┘
                                           │
                        ┌──────────────────▼──────────────────┐
                        │  Master Programmatic Validator Layer│  ← HTML DOM & JS Linter
                        │  (core/validators/master_validator) │  ← AST Code Syntax Check
                        └──────────────────┬──────────────────┘  ← Rubric 100-pt Sum Check
                                           │
                        ┌──────────────────▼──────────────────┐
                        │ Generic Static Renderers & Adapter  │  ← reading_renderer.py
                        │ (core/renderers/ & sandbox_adapter) │  ← slide_renderer.py
                        └──────────────────┬──────────────────┘  ← Dynamic WASM/Worker Sandbox
                                           │
                        ┌──────────────────▼──────────────────┐
                        │ Session Compiler & SCORM Publisher  │  ← Merges reading_all.html
                        └─────────────────────────────────────┘
```

---

## ⚡ Các tính năng cốt lõi mới

### 1. Dynamic Scope Calculator & Progressive Scope Boundaries (`core/scope_calculator.py`)
* Loại bỏ 100% các từ khóa công nghệ hardcode.
* Tự động tính toán tập hợp từ khóa được phép $\bigcup_{1}^N$ và bị cấm $\bigcup_{N+1}^{\text{End}}$ cho từng bài học $N$.
* Tự động chặn các kiến thức vượt cấp sư phạm (ví dụ: bài học nhập môn không được xuất hiện mảng hoặc vòng lặp).

### 2. Declarative JSON Payload Engine (`core/schemas/`)
* Ép các Creator Agent chỉ xuất dữ liệu tri thức dạng JSON thuần theo Pydantic Schemas (`ReadingPayloadSchema`, `SlidePayloadSchema`).
* Triệt tiêu hoàn toàn khả năng LLM tự viết mã HTML/JS dở dang hoặc gây ra lỗi `Unexpected token`.

### 3. Full-Coverage Programmatic Validation Layer (`core/validators/`)
* **Reading Validator:** Kiểm tra HTML DOM structure balance & JS string escaping linter.
* **Slide Validator:** Kiểm tra số lượng slide (5-12 slides), kịch bản lời giảng, và sơ đồ Mermaid.
* **Quiz Validator:** Tự động kiểm tra độ khớp đáp án - giải thích và xáo trộn vị trí A/B/C/D ngẫu nhiên đều đặn.
* **Practice Validator:** Dùng Python `ast.parse()` kiểm tra cú pháp code Python thực tế.
* **Project Validator:** Kiểm tra thang điểm Rubric tổng điểm phải đúng bằng 100 điểm.
* **Master Validator Engine:** Điểm điều phối duy nhất `validate_resource()` tích hợp trực tiếp vào Reviewer Agent.

### 4. Dynamic Sandbox Runner Adapter (`core/sandbox_adapter.py`)
* Tự động chọn Code Sandbox runner phù hợp theo `tech_stack`:
  * `python` ➔ Pyodide WebAssembly Engine
  * `javascript` / `frontend` ➔ Native Web Worker Engine
  * `html` / `css` ➔ Live iFrame Preview
  * `devops` / `sql` / `sysadmin` ➔ Static Code Snippet + Copy Option

---

## 🚀 Hướng dẫn cài đặt & Khởi chạy

### 1. Yêu cầu môi trường
* Python 3.10 trở lên
* OpenPyXL (cho xuất Quiz Excel)
* BeautifulSoup4 (cho HTML DOM Linter)
* Pydantic v2 (cho JSON Schemas)

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường
Tạo file `.env` tại thư mục gốc:
```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. Khởi chạy sinh học liệu tự động

#### Cách 1: Khởi chạy qua CLI Workflow
```bash
python main.py --syllabus "path/to/syllabus.json" --output "output/MyCourse"
```

#### Cách 2: Chạy kiểm thử các Module Core
```bash
# Kiểm thử Scope Calculator & Master Validator
python -c "from core.validators.master_validator import validate_resource; print(validate_resource('READING', '<div>Nội dung...</div>'))"
```

---

## 📁 Cấu trúc thư mục dự án

```
Learning-Material/
├── agents/                   # Đội ngũ Multi-Agent (Creator, Reviewer, Compiler)
│   ├── creator_agents.py     # Agent tạo bài đọc & bài giảng
│   ├── reviewer_agents.py    # Agent kiểm định tích hợp Master Validator
│   └── slide_generator_agent.py
├── core/                     # Động cơ lõi (Core Engines & Infrastructure)
│   ├── scope_calculator.py   # Tính toán phạm vi kiến thức động
│   ├── sandbox_adapter.py    # Bộ chuyển đổi Code Sandbox động
│   ├── session_compilers.py  # Bộ gộp bài học thành reading_all.html & session_slides.html
│   ├── schemas/              # Pydantic Declarative JSON Schemas
│   │   ├── reading_schema.py
│   │   └── slide_schema.py
│   ├── renderers/            # Generic Static Renderers
│   │   ├── reading_renderer.py
│   │   └── slide_renderer.py
│   └── validators/           # Master Programmatic Validation Layer
│       ├── syntax_linter.py  # Linter kiểm tra cú pháp HTML/JS
│       ├── reading_validator.py
│       ├── slide_validator.py
│       ├── quiz_validator.py
│       ├── practice_validator.py
│       ├── project_validator.py
│       └── master_validator.py
├── config/                   # Dynamic Settings & Agent Prompts
├── output/                   # Thư mục chứa kết quả học liệu đã xuất
├── scratch/                  # Scripts kiểm thử tích hợp
└── main.py                   # Điểm khởi chạy hệ thống
```

---

## 🛡️ Quy trình kiểm định lập trình tự động (Master Validation Layer)

Tất cả học liệu được sinh ra đều phải trải qua **2 Tầng Kiểm Định Khắt Khe**:

1. **Tầng 1 - Programmatic Linter & AST Validator (Tự động 100%):**
   * Kiểm tra cú pháp HTML/JS string escaping linter.
   * Parse cú pháp code bằng AST (`ast.parse()`).
   * Kiểm tra khớp chỉ mục đáp án Quiz và xáo trộn A/B/C/D.
   * Kiểm tra tổng điểm Rubric 100 điểm.
   * Kiểm tra ranh giới từ khóa `forbidden_scope`.

2. **Tầng 2 - LLM Pedagogical & UX Reviewer:**
   * Sau khi vượt qua Tầng 1, Reviewer Agent sẽ đánh giá tính sư phạm, văn phong tiếng Việt có dấu chuẩn xác và độ hấp dẫn của bài học.

---

## ❓ FAQ & Xử lý lỗi thường gặp

* **Q: Làm sao để thay đổi khung chương trình học?**
  * *Trả lời:* Bạn chỉ cần cung cấp file `syllabus.json` mới. Hệ thống sẽ tự động tính toán Scope, cấm từ khóa vượt cấp và chọn Sandbox runner phù hợp cho môn học đó.
* **Q: Lỗi `Unexpected token` trong file HTML đã được giải quyết như thế nào?**
  * *Trả lời:* Đã triệt tiêu 100% nhờ tách biệt việc sinh nội dung (xuất JSON Payload thuần) và biên dịch HTML (thực hiện bởi `reading_renderer.py` & `syntax_linter.py`).

---

**Elearning Content Factory** — *Giải pháp tự động hóa học liệu chuẩn quốc tế cho mọi môn học công nghệ.*
