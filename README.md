# 🤖 Elearning Content Factory — Multi-Agent Learning Material Generator

> **Hệ thống sản xuất học liệu tự động, đa tác nhân (Multi-Agent), được thiết kế bởi nguyên tắc Thiết kế Ngược (Backward Design) và chuẩn hóa theo Thang đo Bloom.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![LangGraph / Antigravity](https://img.shields.io/badge/Orchestration-Antigravity-purple)](.)
[![SCORM 1.2](https://img.shields.io/badge/Export-SCORM%201.2-green)](.)
[![SQLite](https://img.shields.io/badge/Memory-SQLite-orange)](.)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Mục lục

1. [Giới thiệu tổng quan](#-giới-thiệu-tổng-quan)
2. [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
3. [Yêu cầu cài đặt](#-yêu-cầu-cài-đặt)
4. [Cài đặt nhanh](#-cài-đặt-nhanh)
5. [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
6. [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
7. [Các Agent trong hệ thống](#-các-agent-trong-hệ-thống)
8. [Luồng pipeline đầy đủ](#-luồng-pipeline-đầy-đủ)
9. [Tính năng nâng cao](#-tính-năng-nâng-cao)
10. [Cấu hình môi trường](#-cấu-hình-môi-trường)
11. [FAQ & Xử lý lỗi](#-faq--xử-lý-lỗi)

---

## 🌟 Giới thiệu tổng quan

**Elearning Content Factory** là một pipeline AI tự động biến một file **PM Excel (Chương trình khung)** thành một bộ học liệu hoàn chỉnh gồm:

| Đầu ra | Định dạng | Công nghệ |
|---|---|---|
| 📖 Bài đọc lý thuyết | HTML tương tác | AI + Plannotator/Code Tracker |
| 🖼️ Slide bài giảng | HTML (Marp) | AI + Marp CLI |
| ❓ Quiz trắc nghiệm | JSON + Excel | AI + Sandbox Testing |
| 🎬 Kịch bản video | Markdown | AI + HyperFrames |
| 🧠 Sơ đồ tư duy | Markdown (Markmap) | AI |
| 📊 Obsidian Vault | WikiLinks + YAML | Knowledge Linker |
| 📦 SCORM Package | .zip (SCORM 1.2) | SCORM Exporter |

**Điểm mạnh vượt trội:**
- ✅ **Self-Correction:** Mỗi artifact có vòng lặp Reviewer tự động sửa lỗi (tối đa 3 lần)
- ✅ **Knowledge Memory:** SQLite-backed memory agent học từ lỗi cũ, không bao giờ lặp lại
- ✅ **Prerequisite Guard:** DAG-validator kiểm tra tính tuần tự tri thức trước khi biên dịch
- ✅ **Semantic Cache:** Tiết kiệm ~40% token cost nhờ caching thông minh
- ✅ **SCORM Export:** Xuất trực tiếp vào Moodle/Canvas/LMS chuẩn quốc tế

---

## 🏗️ Kiến trúc hệ thống

```
                        ╔══════════════════════════════╗
                        ║    PM Excel (Chương trình)   ║
                        ╚══════════════╤═══════════════╝
                                       │
                        ┌─────────────▼─────────────┐
                        │  [0] PM Reviewer Agent     │  ← Format & content audit
                        └─────────────┬─────────────┘
                                       │
                        ┌─────────────▼─────────────┐
                        │ [0.5] Prerequisite Guard   │  ← DAG sequence check (NEW)
                        │       Agent (PGA)          │  ← BLOCKER → stop pipeline
                        └─────────────┬─────────────┘
                                       │
                   ┌──────────────────▼──────────────────┐
                   │     Giai đoạn 1: Hoạch định         │
                   │  Objective Architect → Scheduler →   │
                   │  Knowledge Base → SQLite SSOT Lock   │
                   └──────────────────┬──────────────────┘
                                       │  inject KMA memories ↑
                   ┌──────────────────▼──────────────────┐
                   │  [3.5] Generate Master Content       │  ← KnowledgeMemoryAgent
                   │  + Semantic Cache Layer              │  ← 88% similarity cache
                   └─┬──────┬──────┬──────┬──────┬───────┘
                     │      │      │      │      │
                  HTML  Slide  Quiz Video  MM   (parallel)
                     │      │      │      │      │
                 Reviewer Reviewer Sandbox Rev   Rev
                     │      │      │      │      │
                   ┌─▼──────▼──────▼──────▼──────▼───┐
                   │    Session Compiler + Publisher   │
                   └────────────────┬─────────────────┘
                                    │
            ┌──────────┬────────────┼──────────────┬──────────┐
            │          │            │              │          │
        HTML files  Slide.html  Quiz.json    Quiz Excel  Mindmap.md
                                    │
                    ┌───────────────▼──────────────────┐
                    │  [6] KnowledgeMemoryAgent         │  ← SQLite lessons learned
                    │  + LessonsLearnedAgent (legacy)   │
                    └───────────────────────────────────┘

                    ─── Optional Export Flows ───
                    --obsidian  → ObsidianKnowledgeLinker (prereq graph)
                    --scorm     → SCORM 1.2 Package (.zip)
```

---

## 💻 Yêu cầu cài đặt

| Thành phần | Phiên bản tối thiểu | Ghi chú |
|---|---|---|
| Python | 3.10+ | Bắt buộc |
| Node.js | 18+ | Để chạy Marp CLI |
| Docker | 24+ | Tùy chọn — Sandbox an toàn |
| Gemini API Key | — | Hoặc OpenAI API Key |

**Python packages:**
```bash
pip install -r requirements.txt
```

---

## ⚡ Cài đặt nhanh

### 1. Clone & cài thư viện
```bash
git clone <repo-url>
cd Learning-Material
pip install -r requirements.txt
```

### 2. Cấu hình API Key
```bash
# Tạo file .env từ mẫu
cp .env.example .env
```

Chỉnh sửa `.env`:
```env
# ── LLM Provider (chọn một) ──
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash        # hoặc gemini-1.5-pro

# ── Hoặc dùng OpenAI / OpenRouter ──
# OPENAI_API_KEY=your_openai_key_here
# LLM_MODEL=gpt-4o-mini

# ── Sandbox Security ──
SANDBOX_PROVIDER=docker              # docker | e2b | local_subprocess
E2B_API_KEY=                         # Để trống nếu dùng Docker

# ── Semantic Cache ──
SEMANTIC_CACHE_ENABLED=true
CACHE_SIMILARITY_THRESHOLD=0.88      # 0.0 - 1.0
CACHE_MAX_AGE_DAYS=30

# ── Gemini Prompt Caching ──
GEMINI_PROMPT_CACHING=True
```

### 3. Chuẩn bị file PM Excel
Đặt file Excel chương trình khung vào thư mục `pms/`:
```
pms/
  PM_Web_Application_With_FastAPI.xlsx
  PM_Python_Core.xlsx
  PM_NestJS_Backend.xlsx
```

---

## 📖 Hướng dẫn sử dụng

### Lệnh cơ bản

#### ① Chạy kiểm duyệt PM (không biên dịch)
```bash
python main.py --pm "pms/PM_Web_Application_With_FastAPI.xlsx"
```
Pipeline sẽ phân tích PM, xuất báo cáo `output/.../pm_review_report.md` và hỏi bạn có muốn AI tự sửa không.

#### ② Biên dịch toàn bộ khóa học
```bash
python main.py --pm "pms/PM_Web_Application_With_FastAPI.xlsx" --approve-pm
```

#### ③ Biên dịch một Session cụ thể
```bash
python main.py --pm "pms/PM_Web_Application_With_FastAPI.xlsx" --approve-pm --session "Session 03"
```

#### ④ Chỉ tạo một số loại học liệu
```bash
# Chỉ tạo HTML và Quiz (bỏ slide, video, mindmap)
python main.py --pm "pms/..." --approve-pm --parts "html,quiz"
```

#### ⑤ Rebuild bắt buộc (bỏ qua checkpoint)
```bash
python main.py --pm "pms/..." --approve-pm --force
```

---

### Lệnh xuất bản nâng cao

#### 📁 Tạo Obsidian Knowledge Vault
Sinh toàn bộ vault với dependency graph, prerequisite frontmatter và bidirectional wikilinks:
```bash
python main.py --pm "pms/PM_Web_Application_With_FastAPI.xlsx" --obsidian
```
Vault được tạo tại: `obsidian_vault/<course_name>/`

Mở vault trong Obsidian → **Graph View (Ctrl+G)** để xem bản đồ lộ trình học tập.

#### 📦 Xuất SCORM 1.2 Package
Sau khi đã biên dịch xong, xuất ra file `.zip` nạp vào Moodle/Canvas:
```bash
python main.py --pm "pms/PM_Web_Application_With_FastAPI.xlsx" --scorm
```
File được tạo tại: `output/SCORM_<course>_<timestamp>.zip`

**Cách nạp vào Moodle:**
1. Moodle → Khóa học → Thêm hoạt động → SCORM Package
2. Tải lên file `.zip` vừa tạo
3. Học viên có thể học và hệ thống tự động ghi nhận tiến độ

#### 📊 Xem thống kê Semantic Cache
```bash
python main.py --cache-stats
```
Output mẫu:
```
====== 📊 Semantic Cache Statistics ======
  Tổng response đã cache : 247
  Tổng lần cache HIT     : 89
  Ước tính tokens tiết kiệm: ~71,200
  Phân tích theo Agent:
    HTML_Writer: 45 cached, 23 hits
    Slide_Agent: 38 cached, 18 hits
    Quiz_Agent: 31 cached, 12 hits
==========================================
```

---

### Lệnh SCORM độc lập
Có thể chạy SCORM exporter trực tiếp mà không cần main.py:
```bash
python -m core.scorm_exporter \
  --output "output/PM_Web_Application_With_FastAPI" \
  --course-name "Lập trình Web với FastAPI" \
  --dest "dist/course_scorm.zip"
```

---

## 📂 Cấu trúc thư mục

```
Learning-Material/
│
├── main.py                          # Entry point chính
├── graph_view.html                  # Sơ đồ tương tác luồng pipeline
├── README.md                        # Tài liệu này
├── requirements.txt
├── .env                             # API Keys (không commit lên git)
│
├── pms/                             # File PM Excel đầu vào
│   └── PM_*.xlsx
│
├── agents/                          # Tất cả AI Agents
│   ├── __init__.py
│   ├── strategic_agents.py          # Objective Architect, Scheduler, KB Agent
│   ├── creator_agents.py            # HTML, Slide, Quiz, Video, Mindmap creators
│   ├── reviewer_agents.py           # UX, Academic, Sandbox, PM reviewers
│   ├── knowledge_memory_agent.py    # 🆕 SQLite-backed lessons learned store
│   ├── prerequisite_guard_agent.py  # 🆕 DAG sequence validator
│   ├── lessons_learned_agent.py     # Legacy Markdown lessons logger
│   ├── homework_agents.py
│   ├── practice_agents.py
│   └── project_agents.py
│
├── core/                            # Core infrastructure modules
│   ├── graph.py                     # Antigravity workflow graph definition
│   ├── llm.py                       # Unified LLM caller (Gemini/OpenAI)
│   ├── semantic_cache.py            # 🆕 SQLite LLM response cache
│   ├── scorm_exporter.py            # 🆕 SCORM 1.2 package generator
│   ├── obsidian_knowledge_linker.py # 🆕 Prerequisite-aware vault generator
│   ├── obsidian_exporter.py         # Legacy Obsidian exporter
│   ├── sandbox.py                   # Docker/E2B code execution
│   ├── vector_store.py              # Lightweight embedding store
│   ├── observability.py             # Agent call tracing & logs
│   ├── persistence.py               # Checkpoint save/load
│   ├── quiz_engine.py               # Quiz generation engine
│   ├── session_compilers.py         # File writer & Marp CLI caller
│   └── state.py                     # AgentState TypedDict definition
│
├── skills/                          # Skill prompts cho Agents
│   ├── reading_generator/SKILL.md
│   ├── quiz_generator/SKILL.md
│   ├── lab_generator/SKILL.md
│   ├── mindmap_generator/SKILL.md
│   ├── video_script_generator/SKILL.md
│   └── lessons_learned/SKILL.md
│
├── output/                          # Học liệu đã biên dịch (tự động tạo)
│   └── <course_dir_name>/
│       ├── pm_review_report.md
│       ├── prerequisite_report.md   # 🆕 Báo cáo kiểm tra tiên quyết
│       └── <Session_XX>/
│           └── <Lesson_XX>/
│               ├── reading.html
│               ├── slides.html
│               ├── quiz.json
│               ├── video_script.md
│               └── mindmap.md
│
├── obsidian_vault/                  # Obsidian Knowledge Vault (tự động tạo)
│   └── <course_name>/
│       ├── index.md
│       ├── Prerequisite Map.md      # 🆕 Bản đồ lộ trình học tập
│       ├── Concept Map.md           # 🆕 Bản đồ khái niệm
│       └── <Session_XX>/
│
├── knowledge_store.db               # 🆕 SQLite knowledge memory store
├── semantic_cache.db                # 🆕 SQLite LLM response cache
│
└── web/                             # Web UI (FastAPI backend)
    └── backend/
        └── app/ai_engine/           # Mirror agents cho web API
```

---

## 🤖 Các Agent trong hệ thống

### Nhóm Chiến lược (Strategic Agents)
| Agent | File | Nhiệm vụ |
|---|---|---|
| **PM Reviewer** | `reviewer_agents.py` | Audit format & content PM Excel |
| **Prerequisite Guard** 🆕 | `prerequisite_guard_agent.py` | DAG validator — kiểm tra tính tuần tự tri thức |
| **Objective Architect** | `strategic_agents.py` | Trích xuất chuẩn đầu ra (Bloom's Taxonomy) |
| **Scheduler** | `strategic_agents.py` | Phân bổ thời lượng học hợp lý |
| **Knowledge Base** | `strategic_agents.py` | Tổng hợp tri thức nền tảng vào SSOT |

### Nhóm Sáng tạo (Creator Agents)
| Agent | Đầu ra | Reviewer tương ứng |
|---|---|---|
| **HTML Writer** | Bài đọc HTML tương tác | UX Reviewer |
| **Slide Agent** | Markdown Marp slides | Academic Reviewer |
| **Quiz Agent** | JSON quiz + lab | Sandbox Testing Agent |
| **Video Script** | Markdown kịch bản | Video Script Reviewer |
| **Mindmap Agent** | Markdown mindmap | Mindmap Reviewer |

### Nhóm Kiểm duyệt (Reviewer Agents)
| Agent | Tiêu chí đánh giá | Phản hồi khi REJECT |
|---|---|---|
| **UX Reviewer** | Pedagogy + UX design | Feedback → HTML Writer retry |
| **Academic Reviewer** | Học thuật + Thuật ngữ | Feedback → Slide Agent retry |
| **Sandbox Agent** | Code execution logic | Error trace → Quiz Agent retry |
| **Mindmap Reviewer** | Cấu trúc + Coverage | Feedback → Mindmap retry |

### Nhóm Trí nhớ (Memory Agents)
| Agent | Storage | Nhiệm vụ |
|---|---|---|
| **Knowledge Memory Agent** 🆕 | SQLite (`knowledge_store.db`) | Lưu lessons learned có cấu trúc, 10 category |
| **Lessons Learned Agent** | Markdown (`SKILL.md`) | Legacy logger — tương thích ngược |

---

## 🔄 Luồng pipeline đầy đủ

```
Bước 0   │ PM Excel → [PM Reviewer] → pm_review_report.md
         │   └── AI tự sửa Excel (y/n) hoặc --approve-pm để bỏ qua
         │
Bước 0.5 │ [Prerequisite Guard Agent] ← 🆕
         │   ├── Phân tích toàn bộ curriculum
         │   ├── Xây dựng Dependency Graph (DAG)
         │   ├── BLOCKER violations → DỪNG pipeline
         │   └── prerequisite_report.md + state["prerequisite_data"]
         │
Bước 1   │ [Objective Architect] → Chuẩn đầu ra (Bloom's L1-L6)
         │   └── [Objective Reviewer] → Vòng lặp duyệt (max 3 lần)
         │
Bước 2   │ [Scheduler] → Phân bổ thời lượng Session/Lesson
         │
Bước 3   │ [Knowledge Base] → Tổng hợp tri thức nền
         │
Bước 3.5 │ [Generate Master Content] ← 🆕 inject KMA memories
         │   ├── KnowledgeMemoryAgent.recall() → kinh nghiệm phân loại
         │   ├── Semantic Cache check (88% threshold)
         │   └── call_llm() → master_content JSON
         │
Bước 4   │ ─── Parallel Production ───
         │   ├── [HTML Writer] → [UX Reviewer] → Approved/Retry(x3)
         │   ├── [Slide Agent] → [Academic Rev] → Approved/Retry(x3)
         │   ├── [Quiz Agent]  → [Sandbox Test] → Approved/Retry(x3)
         │   ├── [Video Script] → [Video Rev]   → Approved/Retry(x3)
         │   └── [Mindmap Agent] → [MM Rev]     → Approved/Retry(x3)
         │
Bước 5   │ [Session Compiler] → Ghi file vật lý
         │   ├── reading.html
         │   ├── slides.md → npx marp-cli → slides.html
         │   ├── quiz.json
         │   ├── video_script.md
         │   └── mindmap.md
         │
Bước 6   │ [Knowledge Memory Agent] ← 🆕 (SQLite)
         │   ├── Phân tích review_logs
         │   ├── Phân loại lỗi (10 categories)
         │   ├── Lưu Bad/Good examples
         │   └── [Lessons Learned Agent] (legacy Markdown)
         │
         │ ─── Optional Exports ───
         │   ├── --obsidian → [ObsidianKnowledgeLinker] → vault với prereq links
         │   └── --scorm   → [SCORM Exporter] → .zip cho Moodle/Canvas
```

---

## ✨ Tính năng nâng cao

### 🧠 Knowledge Memory Agent (SQLite)
Agent học từ lỗi, lưu vào SQLite với 10 category có cấu trúc:

```python
from agents.knowledge_memory_agent import recall_memories

# Query memories theo tech_stack và scope
memories = recall_memories(tech_stack="python/fastapi", scope="quiz", limit=10)
```

**10 Error Categories:**
`scope_violation` | `syntax_error` | `format_violation` | `prerequisite_leak` | `pedagogical_error` | `image_prompt_error` | `structure_error` | `terminology_error` | `ai_mention_violation` | `other`

---

### 🛡️ Prerequisite Guard Agent
Kiểm tra tính tuần tự tri thức trước khi biên dịch:

```python
from agents.prerequisite_guard_agent import run_prerequisite_check_for_pm

is_valid, result = run_prerequisite_check_for_pm(
    sessions=sessions,
    tech_stack="python/fastapi",
    output_report_path="output/.../prerequisite_report.md"
)

if not is_valid:
    # Pipeline dừng tự động
    print(f"BLOCKER: {result['stats']['blocker_count']} violations")
```

---

### 💾 Semantic Cache
Tránh gọi LLM 2 lần cho cùng 1 nội dung:

```python
# Tự động hoạt động khi import core.llm
# Tắt: SEMANTIC_CACHE_ENABLED=false trong .env

# Xem stats:
python main.py --cache-stats
```

**Hai cơ chế matching:**
1. **Exact Hash:** SHA-256 hash của prompt → O(1)
2. **Fuzzy TF-IDF:** Jaccard + Coverage similarity → ngưỡng 88%

---

### 📦 SCORM Exporter
Tương thích SCORM 1.2 — nạp được vào hầu hết LMS:
- ✅ Moodle 3.x / 4.x
- ✅ Canvas LMS
- ✅ Blackboard
- ✅ TalentLMS
- ✅ SCORM Cloud

---

### 🔍 Obsidian Knowledge Vault
Vault với prerequisite dependencies:
- **Frontmatter `requires:`** cho mỗi Session
- **Bản đồ lộ trình học** (`Prerequisite Map.md`)
- **Bidirectional WikiLinks** (A → B và B → A)
- **Graph View** trong Obsidian = bản đồ tri thức trực quan

---

## ⚙️ Cấu hình môi trường

| Biến môi trường | Mặc định | Mô tả |
|---|---|---|
| `GEMINI_API_KEY` | — | Google Gemini API Key |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Model Gemini sử dụng |
| `OPENAI_API_KEY` | — | OpenAI/OpenRouter API Key |
| `LLM_MODEL` | `gpt-4o-mini` | Model OpenAI sử dụng |
| `SANDBOX_PROVIDER` | `docker` | `docker` \| `e2b` \| `local_subprocess` |
| `SANDBOX_TIMEOUT` | `5` | Giới hạn thời gian chạy code (giây) |
| `SANDBOX_MEMORY` | `256m` | RAM tối đa cho Docker sandbox |
| `SANDBOX_CPUS` | `0.5` | CPU tối đa cho Docker sandbox |
| `E2B_API_KEY` | — | E2B Cloud Sandbox API Key |
| `SEMANTIC_CACHE_ENABLED` | `true` | Bật/tắt Semantic Cache |
| `CACHE_SIMILARITY_THRESHOLD` | `0.88` | Ngưỡng fuzzy match (0.0-1.0) |
| `CACHE_MAX_AGE_DAYS` | `30` | Số ngày cache hết hạn |
| `GEMINI_PROMPT_CACHING` | `True` | Bật Gemini Context Caching |
| `GEMINI_CACHE_MIN_TOKENS` | `32768` | Số token tối thiểu để cache prompt |

---

## ❓ FAQ & Xử lý lỗi

### Q: PM bị reject ở bước 0, làm sao tiếp tục?
```bash
# Xem báo cáo đề xuất chỉnh sửa
cat output/<course>/pm_review_report.md

# Sau khi đã xem và đồng ý:
python main.py --pm "pms/..." --approve-pm
```

### Q: Pipeline dừng với thông báo BLOCKER?
Prerequisite Guard phát hiện vi phạm tuần tự:
```bash
# Xem chi tiết vi phạm
cat output/<course>/prerequisite_report.md
# Sửa thứ tự bài học trong Excel, sau đó chạy lại
```

### Q: Làm thế nào để reset cache?
```bash
# Xóa file SQLite cache
del semantic_cache.db
# Hoặc: đặt SEMANTIC_CACHE_ENABLED=false trong .env
```

### Q: Muốn rebuild 1 bài học đã approve?
```bash
python main.py --pm "pms/..." --approve-pm --session "Session 03" --force
```

### Q: Docker không hoạt động?
Đảm bảo Docker Desktop đang chạy, hoặc dùng E2B:
```env
SANDBOX_PROVIDER=e2b
E2B_API_KEY=your_e2b_key
```

### Q: Làm sao kiểm tra toàn bộ pipeline chạy đúng không?
```bash
# Xem trace log tất cả agent calls
cat output/<course>/agent_trace.log
```

---

## 📄 License

MIT License © 2024 Rikkei Education

---

*Built with ❤️ by the Rikkei Education AI Team*
