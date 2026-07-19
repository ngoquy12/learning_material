# TIÊU CHUẨN NỘI DUNG SESSION — RIKKEI EDUCATION ELEARNING
> Phiên bản: 1.0 | Cập nhật: 2026-07-19 | Áp dụng cho: Toàn bộ Session trong hệ thống AI Elearning

---

## MỤC LỤC

1. [Tiêu chuẩn Quizz đầu giờ (Pre-Class Quiz)](#1-tiêu-chuẩn-quizz-đầu-giờ)
2. [Tiêu chuẩn Quizz trong lesson (In-Lesson Quiz)](#2-tiêu-chuẩn-quizz-trong-lesson)
3. [Tiêu chuẩn Quizz cuối giờ (Post-Class Quiz)](#3-tiêu-chuẩn-quizz-cuối-giờ)
4. [Tiêu chuẩn Bài đọc (Reading)](#4-tiêu-chuẩn-bài-đọc)
5. [Tiêu chuẩn Video bài học (Lesson Video)](#5-tiêu-chuẩn-video-bài-học)
6. [Tiêu chuẩn Slide bài giảng (Slide)](#6-tiêu-chuẩn-slide-bài-giảng)
7. [Tiêu chuẩn Bài tập thực hành (Lab/Practice)](#7-tiêu-chuẩn-bài-tập-thực-hành)
8. [Tiêu chuẩn Mindmap](#8-tiêu-chuẩn-mindmap)
9. [Tiêu chuẩn tổng quát một Session](#9-tiêu-chuẩn-tổng-quát-một-session)

---

## NGUYÊN TẮC CỐT LÕI CHUNG

### A. Nguyên tắc đơn nhiệm (Single Concept)
Mỗi đơn vị nội dung (câu hỏi, đoạn đọc, slide, scene video) **chỉ được truyền tải DUY NHẤT một kiến thức hoặc kỹ năng**. Không gộp nhiều khái niệm vào một đơn vị.

### B. Nguyên tắc ngữ cảnh hóa (Contextualization)
Tất cả nội dung phải gắn với **bài toán thực tế có ngữ cảnh rõ ràng** — không hỏi/dạy kiến thức trừu tượng tách biệt. Ví dụ phải gần với công việc thực tế của lập trình viên.

### C. Nguyên tắc phân tầng (Bloom's Taxonomy)
Mọi nội dung được thiết kế theo **thang đo Bloom** từ thấp đến cao:
- **Nhận biết** → **Thông hiểu** → **Vận dụng** → **Phân tích** → **Đánh giá** → **Sáng tạo**

### D. Nguyên tắc nhất quán công nghệ
Tất cả nội dung trong một Session **phải bám 100% vào technology_stack** được khai báo. Tuyệt đối không lẫn lộn công nghệ.

---

## 1. TIÊU CHUẨN QUIZZ ĐẦU GIỜ

### 1.1 Thông số kỹ thuật

| Thông số | Quy định |
|----------|----------|
| Số câu | **15 câu** (random từ ngân hàng 45 câu) |
| Thời gian làm bài | 15 phút |
| Số lần làm | 1 lần (không làm lại) |
| Thang điểm | 15 điểm (1 điểm/câu) |
| Ngưỡng đạt | ≥ 10/15 |
| Định dạng | Trắc nghiệm 4 đáp án (A/B/C/D) |

### 1.2 Phân bổ câu hỏi

| STT | Nội dung | Số câu | Mức độ Bloom | Mục tiêu đánh giá |
|-----|----------|--------|--------------|-------------------|
| Câu 1–4 | Bài cũ | 4 | Vận dụng chuyên sâu | Hiện thực hóa cú pháp vào bài toán thực tế |
| Câu 5–7 | Bài cũ | 3 | Phân tích chuyên sâu | Đọc hiểu luồng code, phát hiện lỗi logic (Debug) |
| Câu 8–10 | Bài cũ | 3 | Sáng tạo | Tư duy kiến trúc, tối ưu hiệu năng hệ thống |
| Câu 11–12 | Bài mới | 2 | Thông hiểu | Tiếp thu khái niệm, thuật ngữ, mục đích công nghệ mới |
| Câu 13–14 | Bài mới | 2 | Vận dụng sơ bộ | Nhận diện cú pháp chuẩn và cách triển khai cơ bản |
| Câu 15 | Bài mới | 1 | Phân tích sơ bộ | So sánh công nghệ mới với giải pháp đã biết |

### 1.3 Ngân hàng câu hỏi (45 câu)

- **30 câu bài cũ** (phân bổ đều 3 mức độ: Vận dụng 12 câu / Phân tích 10 câu / Sáng tạo 8 câu)
- **15 câu bài mới** (Thông hiểu 6 / Vận dụng sơ bộ 6 / Phân tích sơ bộ 3)

### 1.4 Ma trận phân loại sinh viên

| Nhóm | Kết quả | Phân loại | Chiến thuật |
|------|---------|-----------|-------------|
| **Gương mẫu** | ≥13/15 + Bài mới ≥4/5 | Xuất sắc: Nắm chắc bài cũ, chủ động nghiên cứu | Làm Leader nhóm / giao bài Sáng tạo khó hơn |
| **Nỗ lực** | 7–9/15 + Bài mới ≥3/5 | Chăm chỉ nhưng hổng nền tảng | Bổ trợ bài cũ ngay tại lớp |
| **Tư duy tốt** | 10–12/15 + Bài mới <3/5 | Thực chiến tốt nhưng không xem bài mới | Cảnh cáo kỷ luật, yêu cầu xem lại tài liệu |
| **Ổn định** | 10–12/15 + Bài mới ≥3/5 | Trung bình, đối phó | Push để lên Gương mẫu |
| **Ẩn mình** | 7–9/15 + Bài mới <3 | Thông minh nhưng lười | Theo dõi sát, tạo áp lực tích cực |
| **Nguy cơ** | <7/15 | Yếu cả hai | Mentoring 1:1 / Trợ giảng hỗ trợ |

### 1.5 Quy tắc viết câu hỏi

**BẮT BUỘC:**
- [ ] Câu dẫn rõ ràng, đủ ngữ cảnh (ví dụ code thực tế, không trừu tượng)
- [ ] 4 phương án: 1 đúng + 3 sai (distractor có chủ đích, gần đúng)
- [ ] Distractor phải là lỗi phổ biến thực tế của sinh viên
- [ ] Độ dài 4 đáp án tương đương nhau (±20% ký tự)
- [ ] Không có cụm "Tất cả các đáp án trên" hoặc "Không có đáp án nào"
- [ ] Không có manh mối ngữ pháp (câu dẫn + đáp án phải hợp ngữ pháp với mọi phương án)
- [ ] Code snippet trong câu hỏi phải chạy được (ngoại trừ câu Debug có lỗi chủ đích)

**CẤM:**
- Hỏi 2 kiến thức cùng lúc trong 1 câu
- Dùng từ "không bao giờ", "luôn luôn" (tạo bias)
- Code snippet dài >20 dòng
- Câu hỏi có đáp án đúng quá rõ ràng

---

## 2. TIÊU CHUẨN QUIZZ TRONG LESSON

### 2.1 Thông số kỹ thuật

| Thông số | Quy định |
|----------|----------|
| Số câu | **5 câu** |
| Thời gian làm | Không giới hạn thời gian |
| Số lần làm | Tối đa **3 lần** |
| Ngưỡng đạt | **5/5 câu** (100%) |
| Phản hồi sai | Hiển thị ngay: "Sai rồi, xem lại phút XX:XX của video" |
| Vị trí | Cuối mỗi lesson (sau Video/Reading) |

### 2.2 Mục tiêu đánh giá

- **Nhận diện**: Xác nhận sinh viên nắm từ khóa, cú pháp, khái niệm cốt lõi của bài mới
- **Thông hiểu**: Kiểm tra khả năng giải thích cơ chế hoạt động và luồng thực thi
- **Sàng lọc**: Phát hiện sớm các hiểu nhầm phổ biến để điều chỉnh học tập

### 2.3 Phân bổ câu hỏi

| STT | Mức độ Bloom | Mục tiêu | Tỷ lệ |
|-----|-------------|----------|--------|
| Câu 1–2 | Nhận biết | Từ khóa, cú pháp, định nghĩa | 40% |
| Câu 3–4 | Thông hiểu | Cơ chế hoạt động, luồng thực thi | 40% |
| Câu 5 | Vận dụng | Áp dụng vào tình huống đơn giản | 20% |

### 2.4 Quy tắc viết câu hỏi trong lesson

- **Gắn trực tiếp** với nội dung video/reading của lesson đó
- Phải có **timestamp** phản hồi khi sai ("Xem lại phút XX:XX")
- Câu hỏi **không được vượt quá** phạm vi bài học hiện tại
- Các distractor phải là **hiểu nhầm điển hình** của người mới học

---

## 3. TIÊU CHUẨN QUIZZ CUỐI GIỜ

### 3.1 Thông số kỹ thuật

| Thông số | Quy định |
|----------|----------|
| Số câu | **15 câu** |
| Thời gian làm | 20 phút |
| Số lần làm | 1 lần |
| Ngưỡng đạt | ≥ 10/15 |
| Phạm vi | Toàn bộ Session (bài cũ + bài mới đã học trong ngày) |

### 3.2 Phân bổ câu hỏi

| STT | Mức độ | Số câu | Mục tiêu đánh giá |
|-----|--------|--------|-------------------|
| Câu 1–6 | Vận dụng | 6 | Triển khai đúng cú pháp và chức năng cơ bản |
| Câu 7–11 | Phân tích | 5 | Đọc luồng code, bắt lỗi logic, hiểu cơ chế vận hành |
| Câu 12–15 | Sáng tạo | 4 | Tư duy Best Practice, chọn giải pháp tối ưu |

### 3.3 Ma trận phân loại sinh viên cuối giờ

| Nhóm | Kết quả | Phân loại | Chiến thuật |
|------|---------|-----------|-------------|
| **Làm chủ** | 13–15 câu | Xuất sắc: Hiểu bản chất, code sạch, xử lý bẫy logic | Giao Project-based / Chỉ định làm Mentor |
| **Đạt** | 10–12 câu | Khá: Nắm vững cú pháp, còn sai ở Phân tích/Tối ưu | Viết Comment giải thích, bài tập mức Giỏi |
| **Cơ bản** | 7–9 câu | Trung bình: Dừng ở copy-paste / shadowing | Làm lại từ đầu không nhìn mẫu, xem lại Record |
| **Cần kèm** | <7 câu | Yếu: Chưa hiểu luồng code | Kèm 1:1, rà soát hổng kiến thức nền |

### 3.4 Mục tiêu đánh giá cuối giờ

- **Validation**: Sinh viên chuyển hóa lý thuyết → thực hành
- **Retention**: Nhớ được giải pháp xử lý bug và quy tắc tối ưu từ buổi học
- **Integration**: Kết hợp công nghệ mới với nền tảng cũ

---

## 4. TIÊU CHUẨN BÀI ĐỌC (READING)

### 4.1 Thông số kỹ thuật

| Thông số | Quy định |
|----------|----------|
| Độ dài | 800–1500 từ/bài đọc |
| Thời gian đọc ước tính | 8–15 phút |
| Định dạng xuất | HTML (render trong hệ thống) |
| Cấu trúc bắt buộc | 5 phần (xem bên dưới) |
| Số code example | 2–4 ví dụ thực tế |
| Font code | Fira Code, monospace |

### 4.2 Cấu trúc bắt buộc (5 phần)

```
1. BÀI TOÁN ĐẶT RA (Problem Statement)      → Hook, tình huống thực tế
2. GIẢI THÍCH KHÁI NIỆM (Concept)           → Định nghĩa, cơ chế
3. VÍ DỤ THỰC TẾ (Code Example)             → Code demo có syntax highlight
4. PHÂN TÍCH SÂU (Deep Dive)                → Pitfalls, best practices, so sánh
5. TÓM TẮT (Summary)                        → Key takeaways dạng bullet
```

### 4.3 Quy tắc viết bài đọc

**Bắt buộc:**
- [ ] Phần 1 phải có tình huống thực tế (không được bắt đầu bằng định nghĩa)
- [ ] Mỗi khái niệm phải có ít nhất 1 ví dụ code chạy được
- [ ] Code phải có syntax highlighting đúng ngôn ngữ
- [ ] Phần tóm tắt phải có ≥3 bullet points
- [ ] Đọc xong phải trả lời được 5 câu Quizz in-lesson

**Cấm:**
- Bắt đầu bài đọc bằng định nghĩa khô khan
- Code snippet lỗi (trừ ví dụ minh họa lỗi có chú thích)
- Sử dụng ví dụ không liên quan thực tế (ví dụ: `foo`, `bar`, `x`, `y` vô nghĩa)
- Độ dài >2000 từ (gây quá tải nhận thức)

### 4.4 Checklist chất lượng bài đọc

- [ ] Hook có gây tò mò trong 2 câu đầu tiên
- [ ] Có ít nhất 1 bảng so sánh (với/không với kỹ thuật mới)
- [ ] Có cảnh báo lỗi thường gặp (Pitfall section)
- [ ] Ngôn ngữ giản dị, không hàn lâm quá mức
- [ ] Tất cả link/reference hoạt động

---

## 5. TIÊU CHUẨN VIDEO BÀI HỌC

### 5.1 Thông số kỹ thuật

| Thông số | Quy định |
|----------|----------|
| Thời lượng | 4–6 phút (240–360 giây) |
| Canvas | 1920×1080px (Full HD) |
| Framework | HyperFrames (sub-composition architecture) |
| Số scene | 4–6 scenes |
| Narration | 400–800 từ |
| Font chữ | Inter (text) + Fira Code (code) |
| Background | #0f1117 + dot grid pattern |

### 5.2 Cấu trúc bắt buộc

```
Scene 1: Giới thiệu & Bài toán đặt ra     (30–45s)
Scene 2: Khái niệm cốt lõi               (40–60s)
Scene 3: Code Demo                        (50–70s)
Scene 4: Phân tích / Pitfalls            (40–60s)
Scene 5: [Optional] Ứng dụng thực tế    (30–50s)
Scene N: Tổng kết & CTA                  (20–30s)
```

### 5.3 Quy tắc GSAP Timeline (bắt buộc mọi scene)

```
t=0.0s: tl.set(".clip", { autoAlpha: 1 }, 0)  ← BẮT BUỘC ĐẦU TIÊN
t=0.2s: Intro title fade in (scale 0.8→1)
t=3.2s: Intro title lên góc / fade out
t≥4.0s: Nội dung chính xuất hiện             ← KHÔNG BAO GIỜ trước 4.0s
t=DUR:  tl.set({}, {}, DUR)                   ← BẮT BUỘC CUỐI TIMELINE
```

### 5.4 Quy tắc Narration

- Mở đầu: "Chào mừng các em đã quay trở lại với hệ thống Elearning của Rikkei Education..."
- Kết thúc: "Cảm ơn các em đã theo dõi, hẹn gặp lại trong bài học tiếp theo!"
- Câu chuyển cảnh mượt mà giữa các scene
- Tốc độ đọc: ~120–150 từ/phút

### 5.5 Design System

| Element | Giá trị |
|---------|---------|
| Background | `#0f1117` |
| Text chính | `#e6edf3` |
| Text phụ | `#c9d1d9` |
| Keyword | `#ff7b72` |
| String | `#a5d6ff` |
| Variable | `#79c0ff` |
| Function | `#d2a8ff` |
| Good/Pass | `#3fb950` |
| Error/Bad | `#f85149` |
| Card bg | `rgba(9,9,11,0.7)` + border `rgba(255,255,255,0.08)` |

### 5.6 Audio Architecture

- Audio files: `assets/tts/scene_XX.mp3`
- **BẮT BUỘC**: Tất cả `<audio>` đặt trong `index.html` (root), KHÔNG trong sub-composition
- Audio track-index bắt đầu từ 20+
- `data-start` trong index.html là timestamp tuyệt đối của root timeline

---

## 6. TIÊU CHUẨN SLIDE BÀI GIẢNG

### 6.1 Thông số kỹ thuật

| Thông số | Quy định |
|----------|----------|
| Số slide/lesson | 8–15 slide |
| Tỷ lệ | 16:9 (1920×1080) |
| Slide đầu | Title slide bắt buộc |
| Slide cuối | Summary + Q&A slide |
| Code trên slide | Tối đa 15 dòng/slide |

### 6.2 Cấu trúc slide chuẩn

```
Slide 1:  Title + Session info
Slide 2:  Mục tiêu bài học (Learning Objectives)
Slide 3:  Bài toán đặt ra (Problem Hook)
Slide 4–N: Nội dung chính (1 khái niệm/slide)
Slide N-1: Demo/Code walkthrough
Slide N:  Tóm tắt + Key Takeaways
```

### 6.3 Quy tắc thiết kế slide

**Bắt buộc:**
- [ ] Mỗi slide chỉ 1 ý chính (One Idea per Slide)
- [ ] Không quá 6 bullet points/slide
- [ ] Mỗi bullet tối đa 1 dòng (không viết đoạn văn trên slide)
- [ ] Code phải có syntax highlighting
- [ ] Hình ảnh/diagram ưu tiên hơn text

**Cấm:**
- Slide chỉ có text, không có visual
- Font size < 24px
- Màu chữ contrast thấp (WCAG AA minimum)
---
# TIÊU CHUẨN SESSION — PHẦN 2: BÀI TẬP, MINDMAP & SESSION TỔNG QUÁT

---

## 7. TIÊU CHUẨN BÀI TẬP THỰC HÀNH (LAB/PRACTICE)

### 7.1 Thông số kỹ thuật

| Thông số | Quy định |
|----------|----------|
| Số bài tập/lesson | 2–4 bài |
| Phân loại độ khó | 3 cấp: Cơ bản / Nâng cao / Xuất sắc |
| Thời gian làm ước tính | Cơ bản: 15–20 phút / Nâng cao: 25–35 phút / Xuất sắc: 45–60 phút |
| Ngôn ngữ đề bài | Tiếng Việt (code comment: Tiếng Anh) |
| Auto-grading | Bắt buộc có test cases |
| Số test cases tối thiểu | 5 (bao gồm edge cases) |

### 7.2 Cấu trúc bài tập chuẩn

```
1. TIÊU ĐỀ BÀI TẬP
   → Tên bài toán + Độ khó (Cơ bản / Nâng cao / Xuất sắc)

2. MÔ TẢ BÀI TOÁN (Context)
   → Tình huống thực tế, không trừu tượng
   → Vai trò của sinh viên (VD: "Bạn là dev tại công ty X, cần...")

3. YÊU CẦU ĐẦU VÀO / ĐẦU RA
   → Input: Kiểu dữ liệu, ràng buộc
   → Output: Kết quả mong đợi chính xác

4. VÍ DỤ MINH HỌA (Examples)
   → Ít nhất 2 ví dụ: Input → Expected Output
   → Giải thích tại sao output đó đúng

5. RÀNG BUỘC KỸ THUẬT (Constraints)
   → Cấm/Bắt buộc dùng API gì
   → Giới hạn thời gian/bộ nhớ (nếu có)
   → Yêu cầu phong cách code (clean code, type hints...)

6. GỢI Ý (Hints) — Tùy chọn
   → Chỉ hiển thị khi sinh viên yêu cầu
   → 1–3 gợi ý theo thứ tự từ nhẹ đến mạnh

7. TEST CASES
   → Test cases công khai (2–3 cases)
   → Test cases ẩn (3–5 cases, bao gồm edge cases)
```

### 7.3 Phân cấp độ khó chi tiết

#### Cấp 1: Cơ bản (Basic)
- **Mục tiêu**: Áp dụng đúng cú pháp và chức năng cơ bản
- **Đặc điểm**: 1 function, input/output rõ ràng, logic đơn giản
- **Bloom**: Vận dụng (Apply)
- **Ví dụ**: Viết hàm tính tổng mảng, đảo ngược chuỗi, kiểm tra số chẵn lẻ

#### Cấp 2: Nâng cao (Advanced)
- **Mục tiêu**: Kết hợp nhiều kiến thức, xử lý edge case
- **Đặc điểm**: 2–3 function, cần xử lý exception, logic phức tạp hơn
- **Bloom**: Phân tích (Analyze)
- **Ví dụ**: Xây dựng class, xử lý file, kết hợp data structures

#### Cấp 3: Xuất sắc (Excellence)
- **Mục tiêu**: Tư duy thuật toán, tối ưu, thiết kế hệ thống nhỏ
- **Đặc điểm**: Multiple modules, performance consideration, design patterns
- **Bloom**: Sáng tạo (Create)
- **Ví dụ**: Thiết kế mini-app, tối ưu Big-O, implement design pattern

### 7.4 Quy tắc viết Test Cases

**Bắt buộc có:**
- [ ] Happy path (input hợp lệ thông thường)
- [ ] Boundary values (giá trị biên: min, max, 0, -1)
- [ ] Edge cases (mảng rỗng, chuỗi rỗng, None/null)
- [ ] Negative cases (input không hợp lệ → Exception handling)

**Cấm:**
- Test case chỉ test 1 loại input
- Test case expected output sai
- Không có edge case nào

### 7.5 Quy tắc chấm điểm tự động

```
Test cases công khai đúng:    30% điểm
Test cases ẩn đúng:           50% điểm
Code quality (nếu có):        20% điểm
  ├── Đặt tên biến có nghĩa   5%
  ├── Có comment giải thích   5%
  └── Không code lặp (DRY)    10%
```

### 7.6 Checklist chất lượng bài tập

- [ ] Bài toán có ngữ cảnh thực tế (không phải "tính toán số học thuần túy")
- [ ] Yêu cầu input/output đủ rõ ràng để sinh viên không cần đoán
- [ ] Có ví dụ minh họa với giải thích
- [ ] Test cases bao phủ edge cases
- [ ] Gợi ý không tiết lộ quá nhiều
- [ ] Độ khó phù hợp với level của Session

---

## 8. TIÊU CHUẨN MINDMAP

### 8.1 Thông số kỹ thuật

| Thông số | Quy định |
|----------|----------|
| Công cụ render | Markmap (Markdown-based) |
| Node trung tâm | Tiêu đề Session/Lesson |
| Số nhánh cấp 1 | 4–7 nhánh |
| Số nhánh cấp 2 | 3–5 nhánh/nhánh cấp 1 |
| Số nhánh cấp 3 | 2–3 (chỉ cho các nhánh quan trọng) |
| Tổng nodes | 30–80 nodes |
| Ngôn ngữ | Tiếng Việt (thuật ngữ kỹ thuật giữ nguyên tiếng Anh) |

### 8.2 Cấu trúc Mindmap chuẩn

```markdown
# [Tên Session/Lesson]
## 1. Tổng quan (Overview)
### Định nghĩa
### Mục đích / Use case
### Lịch sử / Bối cảnh
## 2. Cú pháp & Cấu trúc (Syntax)
### Khai báo cơ bản
### Các biến thể
### Ví dụ
## 3. Cơ chế hoạt động (How it works)
### Luồng xử lý
### Memory model (nếu có)
## 4. Ưu/Nhược điểm (Pros & Cons)
### Ưu điểm
### Nhược điểm / Hạn chế
## 5. Lỗi thường gặp (Common Mistakes)
## 6. Best Practices
## 7. Liên hệ với kiến thức khác (Related Concepts)
```

### 8.3 Quy tắc viết Mindmap

**Bắt buộc:**
- [ ] Node trung tâm là tên chính xác của khái niệm/lesson
- [ ] Mỗi node dưới 6 từ (không viết câu dài)
- [ ] Thuật ngữ kỹ thuật (API, function names) giữ nguyên tiếng Anh
- [ ] Nhánh "Lỗi thường gặp" phải có trong mọi mindmap kỹ thuật
- [ ] Nhánh "Best Practices" phải có
- [ ] Liên kết với kiến thức đã học (phần tiên quyết)

**Cấm:**
- Node quá dài (>7 từ) gây rối diagram
- Mindmap không có nhánh về lỗi/pitfalls
- Dùng cấu trúc phẳng (1 cấp), phải có hierarchy

### 8.4 Ví dụ Mindmap chuẩn (Python List)

```markdown
# Python List
## Định nghĩa
### Ordered Collection
### Mutable (có thể thay đổi)
### Cho phép duplicate
## Khai báo
### Literal: [1, 2, 3]
### list() constructor
### List comprehension
## Thao tác cơ bản
### Truy cập: list[index]
### Slicing: list[start:end]
### Thêm: append(), insert()
### Xóa: remove(), pop(), del
### Độ dài: len()
## Phương thức nâng cao
### sort(), sorted()
### reverse()
### copy(), deepcopy()
## Lỗi thường gặp
### IndexError: vượt index
### Shallow copy vs Deep copy
### Mutability side effects
## Best Practices
### List comprehension > loop
### Dùng tuple nếu bất biến
### Tránh append trong vòng lặp lớn
## Liên hệ
### Tuple (immutable)
### Dict (key-value)
### Set (unique elements)
```

---

## 9. TIÊU CHUẨN TỔNG QUÁT MỘT SESSION

### 9.1 Cấu trúc Session chuẩn

```
SESSION (1.5–3 tiếng học)
├── Pre-Class (Trước buổi học)
│   ├── Video bài học (4–6 phút) × N lessons
│   ├── Bài đọc (Reading) × N lessons
│   └── Quizz trong lesson (5 câu) × N lessons
│
├── In-Class (Trong buổi học)
│   ├── Quizz đầu giờ (15 câu, 15 phút)
│   ├── [Giảng viên giảng dựa trên Slide]
│   ├── Lab thực hành (Cơ bản → Nâng cao)
│   └── Quizz cuối giờ (15 câu, 20 phút)
│
└── Post-Class (Sau buổi học)
    ├── Bài tập về nhà (theo phân loại năng lực)
    └── Mindmap ôn tập
```

### 9.2 Thông số Session chuẩn

| Thành phần | Số lượng | Thời lượng |
|------------|----------|-----------|
| Lessons | 2–4 | — |
| Video/lesson | 1 | 4–6 phút |
| Reading/lesson | 1 | 8–15 phút |
| Quizz in-lesson | 5 câu | Không giới hạn |
| Quizz đầu giờ | 15 câu | 15 phút |
| Quizz cuối giờ | 15 câu | 20 phút |
| Bài tập Lab | 2–4 | 15–60 phút |
| Mindmap | 1/session | — |

### 9.3 Ma trận nội dung theo Bloom's Taxonomy

| Phần nội dung | Nhận biết | Thông hiểu | Vận dụng | Phân tích | Đánh giá | Sáng tạo |
|--------------|:---------:|:----------:|:--------:|:---------:|:--------:|:--------:|
| Video | ✅ | ✅ | — | — | — | — |
| Reading | ✅ | ✅ | ✅ | ✅ | — | — |
| Quizz in-lesson | ✅ | ✅ | ✅ | — | — | — |
| Quizz đầu giờ | — | ✅ | ✅ | ✅ | — | ✅ |
| Quizz cuối giờ | — | — | ✅ | ✅ | ✅ | ✅ |
| Lab cơ bản | — | — | ✅ | — | — | — |
| Lab nâng cao | — | — | ✅ | ✅ | — | — |
| Lab xuất sắc | — | — | — | ✅ | ✅ | ✅ |

### 9.4 Luồng học tập (Learning Flow)

```
[Sinh viên tự học] Xem Video → Đọc Reading → Làm Quizz in-lesson (đạt 5/5)
        ↓
[Buổi học] Quizz đầu giờ → GV phân loại → GV giảng trọng tâm → Lab → Quizz cuối giờ
        ↓
[Sau buổi học] Bài tập về nhà (theo nhóm năng lực) → Ôn tập Mindmap
```

### 9.5 Tiêu chí tối thiểu để publish Session

Một Session chỉ được đưa vào hệ thống khi đáp ứng ĐỦ tất cả tiêu chí sau:

**Content:**
- [ ] Đủ số lesson theo PM Input
- [ ] Mỗi lesson có: Video + Reading + 5 câu Quizz in-lesson
- [ ] Ngân hàng 45 câu Quizz đầu giờ (30 bài cũ + 15 bài mới)
- [ ] 15 câu Quizz cuối giờ
- [ ] Tối thiểu 2 bài tập Lab (1 Cơ bản + 1 Nâng cao)
- [ ] 1 Mindmap session

**Kỹ thuật:**
- [ ] Video render thành công (1920×1080, không black screen)
- [ ] Reading HTML không lỗi render
- [ ] Tất cả code example chạy được
- [ ] Quizz có đúng đáp án (đã QA)
- [ ] Test cases bài tập chạy đúng

**Sư phạm:**
- [ ] Nội dung nhất quán công nghệ (technology_stack)
- [ ] Phân bổ Bloom's Taxonomy đúng theo từng loại nội dung
- [ ] Không có kiến thức vượt cấp (phải học bài trước mới hiểu được)
- [ ] Mỗi lesson độc lập trong phạm vi Session

---

## PHỤ LỤC: CHECKLIST REVIEWER TỔNG HỢP

### Checklist cho AI Creator Agent

```yaml
video:
  - scenes: 4–6
  - narration_words: 400–800
  - has_intro: true  # "Chào mừng..."
  - has_outro: true  # "Cảm ơn các em..."
  - gsap_clip_set: true  # tl.set(".clip", {autoAlpha:1}, 0) đầu tiên
  - audio_in_root: true  # audio chỉ trong index.html
  - timeline_continuous: true

reading:
  - word_count: 800–1500
  - sections: [problem, concept, example, deepdive, summary]
  - code_examples: 2–4
  - code_runnable: true

quiz_inlesson:
  - total_questions: 5
  - bloom_distribution: [recognize:2, understand:2, apply:1]
  - has_timestamp_feedback: true
  - all_questions_have_4_options: true
  - no_double_concept: true

quiz_prequizz:
  - total_questions: 15  # từ bank 45
  - old_content: 10
  - new_content: 5
  - bloom_distribution_old: [apply:4, analyze:3, create:3]
  - bloom_distribution_new: [understand:2, apply:2, analyze:1]

quiz_postquizz:
  - total_questions: 15
  - bloom_distribution: [apply:6, analyze:5, create:4]

lab:
  - has_basic: true
  - has_advanced: true
  - test_cases_min: 5
  - has_edge_cases: true
  - has_examples: true

mindmap:
  - nodes_range: 30–80
  - has_pitfalls_branch: true
  - has_best_practices_branch: true
  - node_max_words: 6
```

---

*Tài liệu này được xây dựng bởi AI Education Specialist, dựa trên tài liệu gốc của Rikkei Education.*
*Mọi thay đổi cần được PM và Academic Lead phê duyệt trước khi áp dụng.*
