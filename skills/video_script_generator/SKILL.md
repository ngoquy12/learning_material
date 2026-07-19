---
name: video_script_generator
description: Sinh kịch bản video HyperFrames (Production Blueprint JSON) cho bài học E-learning theo chuẩn dev-tutorial-video. Bao gồm scene structure, audio architecture, GSAP timeline và design system.
---

# Video Script Generator — HyperFrames Production Standard

Skill này hướng dẫn **Video Director Agent** tạo ra `Production Blueprint JSON` — kịch bản sản xuất chuẩn HyperFrames cho mỗi bài học.

---

## 1. Pipeline Tổng Quan (3 Agents Khép Kín)

```
video_script_agent          ← Sinh Production Blueprint JSON
       ↓
video_script_reviewer_agent ← Validate theo 8 tiêu chí HyperFrames
       ↓ (APPROVED)
hyperframes_writer_agent    ← Ghi file HTML/JSON ra đĩa
```

---

## 2. Output Format — Production Blueprint JSON

Agent **PHẢI** trả về JSON với cấu trúc sau:

```json
{
  "lesson_slug": "session_01_lesson_02_list_python",
  "lesson_title": "Tổng quan về List trong Python",
  "total_duration": 187.84,
  "scenes": [
    {
      "scene_id": "Scene_01",
      "scene_title": "Tại sao phải dùng List?",
      "start_at_root": 0,
      "duration": 38.84,
      "track_index": 1,
      "narration": "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education...",
      "visual_description": "Màn hình chia đôi. Bên trái: code biến rời gạch bỏ. Bên phải: List code xanh.",
      "html_structure": "split-container, panel-left (code cũ), panel-right (code mới)",
      "animation_timeline": [
        "0.0s: tl.set('.clip', {autoAlpha:1}, 0)",
        "0.2s: intro-title fade in",
        "3.2s: intro-title lên góc trên-trái",
        "4.5s: split-container slide in",
        "6.0s: code-left hiện từng dòng",
        "12.0s: strikethrough effect",
        "18.0s: code-right bounce in"
      ]
    }
  ],
  "tts_scripts": {
    "Scene_01": "Chào mừng các em đã quay trở lại...",
    "Scene_02": "..."
  }
}
```

**Ràng buộc bắt buộc:**
- `start_at_root[N] = sum(duration[0..N-1])`
- `total_duration = sum(all scene durations)`
- `track_index` của scenes: 1, 2, 3, ... (tăng dần)
- Audio tracks: 20, 21, 22, ... (được gán trong `index.html`)

---

## 3. Quy tắc Narration (Lời Thoại)

| Tiêu chí | Yêu cầu |
|----------|---------|
| Tổng từ | 400–800 từ |
| Từ/scene | 80–180 từ |
| Mở đầu | "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education..." |
| Kết thúc | "Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!" |
| Chuyển cảnh | Có câu nối mượt mà: "Bây giờ chúng ta cùng...", "Tiếp theo là..." |

---

## 4. Quy tắc Animation Timeline

Mỗi scene **PHẢI** có animation_timeline tuân thủ đúng thứ tự:

```
0.0s  → "tl.set('.clip', {autoAlpha:1}, 0)"  ← BẮT BUỘC ĐẦU TIÊN
0.2s  → intro-title fade in (scale 0.8→1)
3.2s  → intro-title lên góc / fade out
≥4.0s → nội dung chính (KHÔNG BAO GIỜ trước 4.0s)
...
{DUR}s → tl.set({}, {}, {DUR})              ← BẮT BUỘC CUỐI TIMELINE
```

---

## 5. Chia Scene theo Loại Bài Học

**Theory Lesson (5-6 scenes):**
1. **Giới thiệu & Vấn đề** — Hook, bài toán thực tế
2. **Khái niệm cốt lõi** — Definition, so sánh
3. **Code Demo** — Code block reveal, syntax highlight
4. **Áp dụng thực tế** — Use case, example
5. **Lỗi thường gặp** — Pitfalls, warnings
6. **Tổng kết** — Key takeaways, CTA

**Practical Lesson (4-5 scenes):**
1. **Lab Setup** — Mục tiêu, môi trường
2. **Bước 1-2** — Hướng dẫn từng bước
3. **Bước 3-4** — Coding walkthrough
4. **Test & Debug** — Chạy thử, xử lý lỗi
5. **Kết quả & Review** — Verify output

---

## 6. Design System (BẮT BUỘC tuân theo)

```
Background: #0f1117 + dot grid + radial cyan/purple glow
Font text: Inter | Font code: Fira Code
Text colors: #e6edf3 (primary), #c9d1d9 (secondary), #8b949e (muted)
Syntax: keyword #ff7b72 | string #a5d6ff | variable #79c0ff
Cards: rgba(9,9,11,0.7) + border rgba(255,255,255,0.08) + border-radius 20px
Canvas: 1920×1080px, overflow hidden
```

---

## 7. Reviewer Checklist (8 Tiêu Chí)

Reviewer agent sẽ REJECT nếu vi phạm bất kỳ tiêu chí nào:

1. ✅ JSON có đủ fields: `lesson_slug`, `lesson_title`, `total_duration`, `scenes`, `tts_scripts`
2. ✅ Đủ 4–6 scenes
3. ✅ Mỗi scene có đủ: `scene_id`, `scene_title`, `start_at_root`, `duration`, `track_index`, `narration`, `animation_timeline`
4. ✅ Timeline liên tục: `start_at_root[N] = sum(duration[0..N-1])`
5. ✅ Narration 400–800 từ
6. ✅ Có câu mở đầu + kết thúc sư phạm
7. ✅ `tts_scripts` có đủ entry cho mọi `scene_id`
8. ✅ `track_index` tăng dần: 1, 2, 3, ...
