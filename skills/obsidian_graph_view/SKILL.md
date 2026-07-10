---
name: obsidian_graph_view
description: Thiết lập cấu trúc liên kết Markdown (WikiLinks) tương thích Obsidian để trực quan hóa sơ đồ toàn bộ khóa học dạng Graph View.
---

# Kỹ năng Xuất Bản Sơ Đồ Cấu Trúc Obsidian (Obsidian Graph View Generator)

## 1. Mục tiêu và Triết lý thiết kế
Khi quản lý chương trình học tập đồ sộ, việc trực quan hóa sơ đồ mối quan hệ giữa các Session, Lesson, và các học phần thành phần (Bài đọc, Slide, Quiz, Kịch bản video, Sơ đồ tư duy) là cực kỳ quan trọng. 

Obsidian là một công cụ quản lý tri thức cục bộ mạnh mẽ sử dụng các tệp Markdown liên kết chéo qua cú pháp `[[Tên Note]]`. Bằng cách tạo ra một Vault Obsidian có cấu trúc liên kết chuẩn chỉ, người dùng có thể kích hoạt tính năng **Graph View** của Obsidian để xem toàn bộ bản đồ tri thức của môn học một cách trực quan, sinh động.

---

## 2. Quy tắc liên kết liên kết chéo (WikiLink Rules)
Mỗi tệp Markdown trong Vault Obsidian phải tuân thủ nghiêm ngặt quy tắc đặt tên và liên kết chéo sau:

### A. Trang Chủ Môn Học (`index.md`)
- Là điểm neo trung tâm (Central Hub) của toàn bộ đồ thị.
- Chứa các thông tin giới thiệu chung về môn học.
- Chứa liên kết trỏ tới tất cả các Session: `[[Session 01 - Tên Session]]`, `[[Session 02 - Tên Session]]`,...

### B. Note Session (`Session XX - Tên Session.md`)
- Liên kết quay lại trang chủ: `[[index|🏠 Trang chủ môn học]]`.
- Liên kết tới các Lesson trực thuộc: `[[Lesson XX.Y - Tên Lesson]]`.
- Liên kết tới các đề thi trắc nghiệm của Session: `[[Session XX - Entrance Quiz]]` và `[[Session XX - Exit Quiz]]`.

### C. Note Lesson (`Lesson XX.Y - Tên Lesson.md`)
- Liên kết quay lại Session cha: `[[Session XX - Tên Session|⬅️ Session XX]]`.
- Liên kết tới 4 tài nguyên chính của bài học:
  - Bài đọc: `[[Lesson XX.Y - Reading]]`
  - Bài giảng: `[[Lesson XX.Y - Slides]]`
  - Sơ đồ tư duy: `[[Lesson XX.Y - Mindmap]]`
  - Kịch bản Video: `[[Lesson XX.Y - Video Script]]`

### D. Note Tài nguyên thành phần (Component Notes)
- Phải có liên kết quay lại Note Lesson cha của nó: `[[Lesson XX.Y - Tên Lesson|↩️ Bài học chính]]`.

---

## 3. Cấu trúc thư mục của Vault
Thư mục Vault khi xuất ra ổ đĩa sẽ có dạng phẳng (flat) hoặc dạng cây phân cấp. Obsidian hỗ trợ liên kết phẳng rất tốt bất kể cấu trúc thư mục, nhưng để giữ sự ngăn nắp, cấu trúc thư mục sẽ được phân bổ như sau:
```text
obsidian_vault/
├── index.md (Trang chủ môn học)
├── Session 01 - Tên Session/
│   ├── Session 01 - Tên Session.md
│   ├── Session 01 - Entrance Quiz.md
│   ├── Session 01 - Exit Quiz.md
│   ├── Lesson 01.1 - Tên Lesson/
│   │   ├── Lesson 01.1 - Tên Lesson.md
│   │   ├── Lesson 01.1 - Reading.md
│   │   ├── Lesson 01.1 - Slides.md
│   │   ├── Lesson 01.1 - Mindmap.md
│   │   └── Lesson 01.1 - Video Script.md
```

---

## 4. Tiêu chuẩn giao diện và Metadata (Frontmatter)
Mỗi tệp Markdown được tạo ra phải chứa Metadata ở đầu tệp dưới dạng YAML frontmatter:
```markdown
---
type: [course | session | lesson | reading | slide | quiz | mindmap | video]
id: [Mã ID tương ứng]
title: [Tiêu đề đầy đủ]
tags:
  - learning-material
  - obsidian-graph
---
```

Cách thiết lập này giúp người dùng dễ dàng lọc (Filter) và tô màu (Group Coloring) các nút trong Graph View của Obsidian theo phân loại tài nguyên (ví dụ: tất cả Slide có màu tím, tất cả Quiz có màu đỏ, tất cả bài đọc có màu xanh lá).
