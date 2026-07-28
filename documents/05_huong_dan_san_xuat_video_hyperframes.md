# 🎬 BỘ TÀI LIỆU HƯỚNG DẪN 05: BƯỚC 4 - QUY TRÌNH SẢN XUẤT VIDEO HYPERFRAMES (8-STAGE SOP)

## 1. 🎯 Mục Đích
Sản xuất video bài giảng tự động chuẩn Full HD 1080p60 theo quy trình **Voice-First** và **UI Component Architecture**.

---

## 📌 BỘ 8 QUY TẮC CỐT LÕI (8-STAGE STANDARD PIPELINE)

### Stage 1: Đọc SSOT & Từ Điển Tiếng Anh
- Đọc bài đọc `reading.html` làm Nguồn sự thật duy nhất.
- Chuẩn hóa `Kokoro-Vietnamese/configs/tech_dictionary.json` giữ từ tiếng Anh chuẩn (`Python`, `TypeError`, `VS Code`, `Terminal`, `Console`, `Class`, `Object`, `snake_case`).

### Stage 2: Thiết Kế Kịch Bản & Tách Biệt Voice - UI
- **Thời lượng**: 3 - 6 phút (180s - 360s) / video.
- **Tách biệt 100%**:
  - **Giọng đọc (TTS)**: Giảng giải chi tiết, phân tích bản chất "TẠI SAO".
  - **Màn hình UI**: **TUYỆT ĐỐI KHÔNG DÁN CÂU VĂN THOẠI LÊN MÀN HÌNH**. Chỉ dùng từ khóa ngắn (3-6 từ), Code Snippets thực tế và Sơ đồ khối.

### Stage 3: Kiểm Định Kịch Bản (Reviewer Audit)
- Số phân cảnh: 6 - 12 scenes.
- Cấm chữ toàn in hoa (**Strict No ALL CAPS**), chỉ dùng Sentence case.

### Stage 4: Tạo Voice TTS & Đo Thời Lượng Thực Tế
- Tổng hợp giọng đọc Kokoro-Vietnamese (`hung_thinh`).
- Đo exact `.wav` durations và nạp vào `assets/tts/durations.json`.

### Stage 5: Tách Kênh Audio Độc Lập
- Kênh thoại Voice: `track-index="20"` ➔ `"35"`.
- Kênh nhạc nền (`bg-music`): Bắt buộc gán **`track-index="99"`** (Volume 0.10 - 0.12).

### Stage 6: Dựng Cấu Trúc Dự Án HyperFrames (GSAP)
- Dựng master `index.html` & sub-compositions `Scene_XX.html` từ bộ `hyperframes/components/`.

### Stage 7 & 8: Kiểm Tra Cục Bộ & Render MP4 1080p60
- Chạy `npm run check`, `npm run dev`, và thực thi `npm run render`.
- Tệp video xuất bản tại `renders/session_XX_lesson_YY_TIMESTAMP.mp4`.