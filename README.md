# 🤖 Elearning Content Factory — Multi-Agent Learning Material Generator

> **Hệ thống sản xuất học liệu tự động đa tác nhân (Multi-Agent Architecture) quy mô lớn — 100% Dynamic, Generic, Stack-Agnostic & Schema-Driven (Tuyệt đối Không Hardcode).**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18+-green?logo=nodedotjs)](https://nodejs.org)
[![LangGraph / Antigravity](https://img.shields.io/badge/Orchestration-Antigravity-purple)](.)
[![Schema-Driven](https://img.shields.io/badge/Architecture-Pydantic%20Schema%20Driven-emerald)](.)
[![SCORM 1.2](https://img.shields.io/badge/Export-SCORM%201.2-green)](.)

---

## 📋 Mục Lục

1. [Giới thiệu tổng quan](#-giới-thiệu-tổng-quan)
2. [Các loại học liệu hệ thống sinh tự động](#-các-loại-học-liệu-hệ-thống-sinh-tự-động)
3. [Yêu cầu tiền đề (Prerequisites)](#-yêu-cầu-tiền-đề-prerequisites)
4. [Hướng dẫn cài đặt chi tiết (Installation Guide)](#-hướng-dẫn-cài-đặt-chi-tiết-installation-guide)
5. [Cấu hình biến môi trường (.env)](#-cấu-hình-biến-môi-trường-env)
6. [Hướng dẫn sử dụng & Khởi chạy hệ thống (Usage Guide)](#-hướng-dẫn-sử-dụng--khởi-chạy-hệ-thống-usage-guide)
   - [6.1. Sinh bộ học liệu đầy đủ qua CLI Workflow](#61-sinh-bộ-học-liệu-đầy-đủ-qua-cli-workflow)
   - [6.2. Kiểm thử các Module Core & Validator](#62-kiểm-thử-các-module-core--validator)
7. [Cấu trúc thư mục dự án](#-cấu-trúc-thư-mục-dự-án)
8. [Quy chuẩn thiết kế học liệu chuẩn hệ thống (AGENTS.md)](#-quy-chuẩn-thiết-kế-học-liệu-chuẩn-hệ-thống-agentsmd)
9. [FAQ & Xử lý lỗi thường gặp](#-faq--xử-lý-lỗi-thường-gặp)

---

## 🌟 Giới Thiệu Tổng Quan

**Elearning Content Factory** là hệ thống AI đa tác nhân chuyên nghiệp tự động hóa việc chuyển đổi chương trình khung `syllabus.json` (hoặc PM Excel) thành bộ tài nguyên học liệu hoàn chỉnh cho **bất kỳ công nghệ nào** (Python, Java, React, SQL, Flutter, DevOps...):

- **100% Tiếng Việt có dấu chuẩn sản xuất** & thuật ngữ tiếng Anh `snake_case` / `camelCase`.
- **Phân định phạm vi kiến thức động (Dynamic Scope Boundaries)**: Tự động chặn từ khóa vượt cấp.
- **Hệ thống Kiểm thử & Đánh giá Sư phạm Đa tầng**: Pyodide Code Sandbox, Bloom's Taxonomy Alignment, và PQM Engine.

---

## 📚 Các Loại Học Liệu Hệ Thống Sinh Tự Động

| Loại Học Liệu               | Định dạng Đầu ra                    | Đặc tả & Tiêu chuẩn Sư phạm                                                                                                                      |
| --------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 📖 **Bài đọc lý thuyết**    | `reading.html` & `reading_all.html` | Cấu trúc list ngắt ý ngắn gọn, 100% tiếng Việt có dấu, ảnh bối cảnh 16:9, Dark Terminal Console, Self-Test left-alignment, Live Pyodide Sandbox. |
| 🖼️ **Slide bài giảng**      | `slides.html`                       | Master HTML Slides (15-20 slides/session), Bento Grid modern, 3-30-300 typography, Card Color Coding, Dual Theme (Light/Dark), NO Emoji.         |
| 📝 **Bài tập thực hành**    | Markdown + Code files               | 6 bài tập theo bối cảnh doanh nghiệp (4 cấp độ Bloom: Vận dụng ➔ Phân tích ➔ Sáng tạo). Code 100% tiếng Anh.                                     |
| 🧪 **Mini Project / Lab**   | Markdown + Checklist                | Bố cục 3 phần: Mục tiêu ➔ Các bước thực hiện ➔ Checklist đánh giá định lượng `[ ]`.                                                              |
| ❓ **Quizz Trắc nghiệm**    | Excel (.xlsx) + JSON                | 5 câu/lesson (Bloom), Entrance Quiz 45 câu (30 cũ + 15 mới), Exit Quiz 45 câu (100% mới). 7 nguyên tắc sư phạm Quizz.                            |
| 🗺️ **Visualizer & Mindmap** | HTML / JS Interactive               | Interactive DOM canvas (`#visualizer-canvas`), high-contrast code tracker highlighting, console log panel.                                       |
| 📦 **SCORM & Obsidian**     | ZIP SCORM 1.2 & Obsidian Vault      | Đóng gói chuẩn e-learning LMS (SCORM 1.2) và đồ thị liên kết tri thức 2 chiều (Obsidian Markmap).                                                |

---

## 🛠️ Yêu Cầu Tiền Đề (Prerequisites)

Trước khi cài đặt, hãy đảm bảo máy tính của bạn đã cài đặt các công cụ sau:

1. **Python**: Phiên bản `3.10` trở lên ([Tải Python](https://www.python.org/downloads/)).
2. **Node.js & npm**: Phiên bản `18.0.0` trở lên ([Tải Node.js](https://nodejs.org/)) cho công cụ Marp Slide CLI.
3. **Git**: Công cụ quản lý mã nguồn.

---

## 📥 Hướng Dẫn Cài Đặt Chi Tiết (Installation Guide)

### Bước 1: Clone repository về máy

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
- **Trên macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Bước 3: Cài đặt các thư viện Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 4: Cài đặt các gói Node.js (cho Marp Slide CLI)

```bash
npm install
```

---

## ⚙️ Cấu Hình Biến Môi Trường (.env)

Tạo file `.env` tại thư mục gốc của dự án `Learning-Material/.env`:

```env
# API Keys cho hệ thống Multi-Agent
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Cấu hình Output Directory
DEFAULT_OUTPUT_DIR=output/PM_Python
```

---

## 🚀 Hướng Dẫn Sử Dụng & Khởi Chạy Hệ Thống (Usage Guide)

### 6.1. Sinh bộ học liệu đầy đủ qua CLI Workflow

Để khởi chạy toàn bộ hệ thống tự động sinh tài nguyên cho một khóa học từ `syllabus.json`:

```bash
python main.py --syllabus "path/to/syllabus.json" --output "output/PM_Python"
```

Hoặc sử dụng các cờ tùy chọn nâng cao:

```bash
# Chỉ sinh Bài đọc & Slide bài giảng
python main.py --syllabus "path/to/syllabus.json" --types reading,slide

# Sinh Bài tập & Quizz trắc nghiệm xuất file Excel
python main.py --syllabus "path/to/syllabus.json" --types exercise,quiz
```

---

### 6.2. Kiểm thử các Module Core & Validator

Bạn có thể kiểm thử trực tiếp từng thành phần lõi của hệ thống:

```bash
# 1. Kiểm thử Master Programmatic Validator
python -c "from core.validators.master_validator import validate_resource; print(validate_resource('READING', '<div>Nội dung học liệu...</div>'))"

# 2. Kiểm thử Scope Calculator Engine
python -c "from core.scope_calculator import ScopeCalculator; calc = ScopeCalculator(); print(calc.get_allowed_scope(1))"

# 3. Kiểm thử Antigravity LLM Router
python -c "from core.llm_router import AntigravityLLMRouter; print(AntigravityLLMRouter.resolve_model('reading_creator'))"
```

---

## 📁 Cấu Trúc Thư Mục Dự Án

```
Learning-Material/
├── .agents/                  # Quy chuẩn hệ thống & Quy định thiết kế (AGENTS.md)
│   └── AGENTS.md             # Single Source of Truth cho Quy chuẩn Sư phạm & UI
├── agents/                   # Đội ngũ Multi-Agent (Creator, Reviewer, Compiler)
│   ├── creators/             # Các Agent sinh nội dung (Reading, Quiz, Lab, Slide, Mindmap)
│   ├── reviewer_agents.py    # Agent kiểm định tích hợp Master Validator
│   └── homework_agents.py    # Agent sinh bài tập phân tầng Bloom
├── core/                     # Động cơ lõi (Core Infrastructure)
│   ├── graph.py              # Đồ thị quy trình Asynchronous DAG
│   ├── scope_calculator.py   # Tính toán phạm vi kiến thức động
│   ├── sandbox_adapter.py    # Bộ chuyển đổi Code Sandbox động (Pyodide/Worker)
│   ├── session_compilers.py  # Bộ gộp bài học thành reading_all.html & slides
│   ├── schemas/              # Pydantic Declarative JSON Schemas
│   ├── renderers/            # Generic Static Renderers
│   └── validators/           # Master Programmatic Validation Layer
├── skills/                   # Bộ Kỹ năng Chuyên biệt (Skill Repository)
│   ├── reading_generator/    # Kỹ năng sinh Bài đọc học liệu
│   ├── exercise_generator/   # Kỹ năng sinh Bài tập 6 cấp độ
│   ├── lab_generator/        # Kỹ năng sinh Bài thực hành Lab
│   ├── quiz_generator/       # Kỹ năng sinh Quizz & Ma trận đề
│   └── slide_generator/      # Kỹ năng sinh Slide HTML Master
├── output/                   # Kết quả học liệu đã xuất theo môn học & Session
├── requirements.txt          # Danh sách thư viện Python
├── package.json              # Danh sách gói Node.js
└── main.py                   # Điểm khởi chạy chính của CLI
```

---

## 🛡️ Quy Chuẩn Thiết Kế Học Liệu Chuẩn Hệ Thống (AGENTS.md)

Tất cả các Agent và Module trong hệ thống bắt buộc phải tuân thủ nghiêm ngặt **Quy chuẩn Thiết kế Học liệu** được quy định tại [.agents/AGENTS.md](file:///.agents/AGENTS.md):

1. **Bài Đọc (`reading.html`)**: Scannable Bullets (`- Ý chính` / `  - Chi tiết`), 100% tiếng Việt có dấu, ảnh bối cảnh 16:9, Code Cards (Good vs Bad), Dark Terminal Console, Self-Test left-alignment.
2. **Bài Tập (6 Exercises)**: Đặt trong bối cảnh thực tế doanh nghiệp (LMS, Điểm danh, Khảo thí...), 4 cấp độ Bloom (Vận dụng ➔ Phân tích ➔ Sáng tạo). Code 100% tiếng Anh `snake_case`.
3. **Bài Thực Hành Lab**: 3 phần chuẩn hóa (Mục tiêu ➔ Các bước ➔ Checklist đánh giá `[ ]`).
4. **Quizz Trắc Nghiệm**: 7 nguyên tắc sư phạm Quizz, ma trận đề 5 câu/lesson, 45 câu Entrance Quiz (30 cũ + 15 mới), 45 câu Exit Quiz (100% mới).

---

## ❓ FAQ & Xử Lý Lỗi Thường Gặp

- **Q: Gặp lỗi encoding tiếng Việt trên Windows PowerShell?**
  - _Trả lời:_ Dự án đã tích hợp `sys.stdout.reconfigure(encoding="utf-8")`. Nếu gặp lỗi hiển thị, hãy chạy lệnh `$env:PYTHONIOENCODING="utf-8"` trong PowerShell trước khi thực thi.

- **Q: Làm sao để xuất gói SCORM 1.2 cho LMS?**
  - _Trả lời:_ Sử dụng module `core/scorm_exporter.py` hoặc flag `--export-scorm` trong CLI runner.
