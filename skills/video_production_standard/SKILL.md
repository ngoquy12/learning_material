---
name: video_production_standard
description: Quy trình chuẩn hóa sản xuất Video E-learning End-to-End (Voice-First Pipeline & UI Component Standards) từ kịch bản, âm thanh đến render MP4.
---

# QUY TRÌNH CHUẨN HÓA SẢN XUẤT VIDEO E-LEARNING END-TO-END (VIDEO PRODUCTION STANDARD SOP)

Tài liệu này định nghĩa **Quy trình vận hành chuẩn 8 bước (8-Stage SOP)** dành cho các AI Agent (Video Director Agent, HyperFrames Writer Agent, Reviewer Agent) và Kỹ sư sản xuất học liệu để tự động hóa tạo video chất lượng cao 1080p60.

---

## 📌 BỘ 8 QUY TẮC CỐT LÕI (8-STAGE STANDARD PIPELINE)

### 1. Stage 1: Đọc Tài Liệu SSOT & Chuẩn Hóa Từ Điển Âm Đọc (Pre-Script Gate)
- **SSOT chính thức**: Đọc bài đọc `reading.html` / `reading.md` làm Nguồn sự thật duy nhất.
- **Từ điển kỹ thuật (`Kokoro-Vietnamese/configs/tech_dictionary.json`)**:
  - Giữ nguyên các thuật ngữ tiếng Anh chuẩn (`Python`, `TypeError`, `ValueError`, `VS Code`, `Terminal`, `Console`, `Class`, `Object`, `snake_case`, `Heap`, `Stack`).
  - Không sử dụng các từ phiên âm tiếng Việt gượng gạo (`snếch-kê-xơ`, `Tai-pơ É-rơ`, `xót cốt`, `vê-ét cốt`).

### 2. Stage 2: Thiết Kế Kịch Bản & Tách Biệt Lời Thoại Với Giao Diện (Pedagogy & Voice-UI Gate)
- **Thời lượng chuẩn**: Mỗi video dài từ **3 - 6 phút (180s - 360s)**. Nếu vượt quá 7 phút (420s), bắt buộc tách thành các tập nhỏ (`Part 1`, `Part 2`).
- **Phân tách 100% Giữa Thoại (TTS) & Hình Ảnh (UI Display)**:
  - **Lời thoại (TTS Script)**: Đảm nhận phần giải thích chi tiết, câu chuyện sư phạm, phân tích bản chất "TẠI SAO".
  - **Giao diện (UI Display)**: **TUYỆT ĐỐI KHÔNG DÁN NGUYÊN CÂU KHỔ THOẠI LÊN MÀN HÌNH**. Màn hình UI CHỈ chứa:
    - Tiêu đề ngắn gọn (3 - 5 từ).
    - Các từ khóa kỹ thuật (Bullet points 3 - 6 từ).
    - Mã nguồn ví dụ thực tế (Production-Ready Code).
    - Vector Icons (`<svg>`) hoặc Sơ đồ khối (Diagrams).

### 3. Stage 3: Kiểm Định Kịch Bản & Duyệt Người Dùng (Human Script Review & Approval Gate)
- **Yêu cầu bắt buộc (BƯỚC DUYỆT KỊCH BẢN - STOP & ASK FOR APPROVAL)**:
  - Agent sinh tệp `blueprint.json` và `script_review.md` tổng hợp bảng kịch bản chi tiết từng Scene (bao gồm Lời thoại `narration` và Thẻ UI hiển thị `clean_content`).
  - Agent **TẠM DỪNG (STOP)** và trình bày bảng kịch bản cho User review.
  - **CHỈ TIẾN HÀNH SINH VOICE (STAGE 4)** khi User đã xem và xác nhận phê duyệt kịch bản (tránh lãng phí thời gian tạo lại âm thanh nhiều lần).

### 4. Stage 4: Tạo Âm Thanh Voice-First & Đo Thời Lượng Thực Tế (Voice-First Probe Gate)
- **Quy trình tạo giọng đọc trước (TTS-First)**:
  1. Chạy `gen_tts.py` / `VoiceDrivenVideoEngine` để sinh âm thanh giọng đọc Kokoro-Vietnamese (`assets/tts/Scene_01.wav` .. `Scene_XX.wav`).
  2. Sử dụng thư viện `soundfile` / `ffprobe` đo thời lượng chính xác tới từng milisecond của từng tệp `.wav`.
  3. Xuất tệp `assets/tts/durations.json`.
  4. Cập nhật thuộc tính `duration` thực tế vào blueprint DỰA TRÊN thời lượng thoại thật (loại bỏ hoàn toàn khoảng lặng dư thừa).

### 5. Stage 5: Tách Kênh Audio Độc Lập (Track Separation Gate)
- **Bảng phân kênh Audio trong `index.html`**:
  - Kênh Thoại Voiceover (TTS): `data-track-index="20"` ➔ `"35"` (Mỗi scene 1 kênh riêng).
  - Kênh Nhạc Nền (`bg-music`): Bắt buộc gán **`data-track-index="99"`** (Volume: `0.10` - `0.12`, `loop="true"`).
  - **Cấm đè kênh**: Không bao giờ đặt nhạc nền và giọng đọc trên cùng một `track-index`.

### 6. Stage 6: Sinh Mã HTML Composition Dựa Trên Voice Thật (Voice-Driven Composition Gate)
- **BẮT BUỘC THỨ TỰ THỰC THI**: Mã HTML Sub-compositions (`Scene_XX.html`) và Master Timeline (`index.html`) **CHỈ ĐƯỢC SINH RA SAU KHI ĐÃ CÓ DỮ LIỆU ĐỘ DÀI VOICEOVER THỰC TẾ** từ Stage 4. Đảm bảo GSAP Keyframes và thời lượng phân cảnh trùng khớp $100\%$ giọng đọc AI.
- **Tách biệt Sub-composition Intro & Outro (CHỐNG ĐÈ UI HTML)**:
  - Bắt buộc tạo 2 tệp Sub-composition độc lập: `src/compositions/Intro.html` (9.24s) và `src/compositions/Outro.html` (12.15s).
  - Khai báo dưới dạng Composition Clips trong `index.html`:
    - Intro Clip: `data-composition-src="src/compositions/Intro.html"`, `data-start="0"`, `data-duration="9.24"`.
    - Outro Clip: `data-composition-src="src/compositions/Outro.html"`, `data-start="{OUTRO_START}"`, `data-duration="12.15"`.
- **Quy chuẩn Giao diện Video Nền Sáng Chuẩn (Light Theme & Clean Typography Standard)**:
  - **Nền màn hình canvas (1920x1080)**: Gradient trắng xám kem nhạt `background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%)`.
  - **Phông chữ mặc định**: **Be Vietnam Pro** (`font-family: 'Be Vietnam Pro', sans-serif;`) hiển thị chuẩn nét dấu Tiếng Việt.
  - **Logo Thương hiệu**: Thẻ `<img>` logo Rikkei `https://rikkei.edu.vn/wp-content/uploads/2025/09/Logo.png` nằm cố định ở góc **TRÊN-PHẢI** (`top: 50px; right: 80px; height: 52px; z-index: 100`).
  - **Màu chủ đạo thương hiệu (`#ba252a` Rikkei Red)**:
    - **Tiêu đề phân cảnh (Main Title)**: Nằm ở góc **TRÊN-TRÁI** (`top: 50px; left: 80px; font-size: 44px; font-weight: 800; color: #ba252a`), nằm trên **CÙNG MỘT HÀNG NGANG** song song với Logo.
    - **Thẻ Số Thứ Tự (Number Badge)**: Màu đỏ `#ba252a` (`background: #ba252a; color: #ffffff`).
    - **Viền Thẻ & Icon**: Đường viền lề trái `#ba252a` (`border-left: 6px solid #ba252a`), icon sublist `ph-check-circle` màu `#ba252a`.
    - **Khung Code Header**: Viền trên màu đỏ `#ba252a` (`border-top: 5px solid #ba252a`), từ khóa ngôn ngữ màu `#ba252a`.
  - **Bắt buộc Căn Trái 100% (`text-align: left !important`)**: Toàn bộ văn bản tiêu đề, mô tả, danh sách sublist và mã nguồn ví dụ.
  - **Trình bày Code chuẩn Monospace Fira Code**: Dùng thẻ `<pre class="code-body">` nằm sát lề trái, bảo toàn chính xác thụt lề $4\text{ khoảng trắng}$ chuẩn ngôn ngữ.

### 7. Stage 7: Kiểm Tra & Chạy Thử Cục Bộ (Sanity Check Gate)
- Kiểm tra liên kết tệp: `npm run check`
- Xem trước tương tác trên trình duyệt: `npm run dev`

### 8. Stage 8: Render Video MP4 1080p60 (Puppeteer Render Gate)
- Thực thi render: `npm run render`
- Tệp video đầu ra được lưu tại `renders/session_XX_lesson_YY_TIMESTAMP.mp4`.

---

## 🛠️ HƯỚNG DẪN DÙNG CHO NGƯỜI DÙNG & AGENT

### Cách 1: Chạy Tự Động Qua CLI
```bash
# Tạo kịch bản & dự án Video cho Lesson 01 Session 06 (Voice-First Pipeline)
python -X utf8 scratch/recreate_video_lesson01_session06.py

# Render ra tệp MP4 chất lượng cao 1080p60
cd "output/PM_Python/Session 06 - Cấu trúc dữ liệu List va Tuple/Lesson 01 - Khái niệm List và cách khởi tạo/Video/session_06_lesson_01"
npm run render
```

### Cách 2: Xem Trước Video Tương Tác Trực Tiếp Trên Web Dev Server
```bash
cd "output/PM_Python/Session 06 - Cấu trúc dữ liệu List va Tuple/Lesson 01 - Khái niệm List và cách khởi tạo/Video/session_06_lesson_01"
npm run dev
# Mở trình duyệt truy cập: http://localhost:5173
```
