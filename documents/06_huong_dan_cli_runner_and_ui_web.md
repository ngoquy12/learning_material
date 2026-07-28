# 🛠️ BỘ TÀI LIỆU HƯỚNG DẪN 06: BƯỚC 5 - HƯỚNG DẪN SỬ DỤNG LỆNH CLI & WEB DASHBOARD

## 1. 🎯 Chạy Tự Động Toàn Bộ Học Liệu Qua CLI

```bash
# Chạy sinh tài nguyên non-video cho Session 07, 08, 09 tuần tự:
python -X utf8 -c "import sys; from cli.runner import main_entry; sys.argv=['runner.py', '--pm', 'pms/PM_Python.xlsx', '--session', 'Session 07', '--parts', 'html,slide,quiz,mindmap', '--approve-pm']; main_entry()"
```

---

## 2. 🎬 Chạy Tạo Dự Án & Render Video Cho Bài Học

```bash
# Bước 1: Khởi chạy Pipeline tạo dự án Video & Voiceover
python -X utf8 scratch/prepare_and_render_session08_lesson01.py

# Bước 2: Di chuyển vào thư mục dự án và Render tệp MP4
cd "output/PM_Python/Session 08 - Hàm (Function) va Phạm vi biến/Lesson 01 - Giới thiệu hàm và cách định nghĩa/Video/session_08_lesson_01"
npm run render
```

---

## 3. 🌐 Khởi Chạy Giao Diện Web Dashboard UI (Gradio / FastAPI)

```bash
# Cửa sổ 1: Khởi chạy Gradio App UI
python app_gradio.py

# Cửa sổ 2: Khởi chạy Web Backend FastAPI
cd web/backend
uvicorn app.main:app --reload --port 8000
```
- Mở trình duyệt truy cập: `http://localhost:7860` để thao tác trực quan trên giao diện Web!