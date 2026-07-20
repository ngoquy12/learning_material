# TIÊU CHUẨN NỘI DUNG SESSION — RIKKEI EDUCATION ELEARNING
> Phiên bản: 1.0 | Cập nhật: 2026-07-19 | Áp dụng cho: Toàn bộ Session trong hệ thống AI Elearning

---

## MỤC LỤC

1. [Tiêu chuẩn Quizz đầu giờ (Pre-Class Quiz)](#1-tiêu-chuẩn-quizz-đầu-giờ)
2. [Tiêu chuẩn Quizz trong lesson (In-Lesson Quiz)](#2-tiêu-chuẩn-quizz-trong-lesson)
3. [Tiêu chuẩn Quizz cuối giờ (Post-Class Quiz)](#3-tiêu-chuẩn-quizz-cuối-giờ)
4. [Tiêu chuẩn Bài đọc (Reading)](#4-tiêu-chuẩn-bài-đọc-reading)
5. [Tiêu chuẩn Video bài học (Lesson Video)](#5-tiêu-chuẩn-video-bài-học)
6. [Tiêu chuẩn Slide bài giảng (Slide)](#6-tiêu-chuẩn-slide-bài-giảng)
7. [Tiêu chuẩn Bài tập thực hành (Lab/Practice)](#7-tiêu-chuẩn-bài-tập-thực-hành-labpractice)
8. [Tiêu chuẩn Mindmap](#8-tiêu-chuẩn-mindmap)
9. [Tiêu chuẩn tổng quát một Session](#9-tiêu-chuẩn-tổng-quát-một-session)
10. [Tiêu chuẩn Session Mini Project (Dự án nhỏ)](#10-tiêu-chuẩn-session-mini-project-dự-án-nhỏ)

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

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông số</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quy định</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>15 câu</b> (random từ ngân hàng 45 câu)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thời gian làm bài</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">15 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số lần làm</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">1 lần (không làm lại)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thang điểm</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">15 điểm (1 điểm/câu)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Ngưỡng đạt</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">≥ 10/15</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Định dạng</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Trắc nghiệm 4 đáp án (A/B/C/D)</td>
    </tr>
  </tbody>
</table>

### 1.2 Phân bổ câu hỏi

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">STT</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Nội dung</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số câu</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Mức độ Bloom</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Mục tiêu đánh giá</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 1–4</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bài cũ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">4</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Vận dụng chuyên sâu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Hiện thực hóa cú pháp vào bài toán thực tế</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 5–7</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bài cũ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">3</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phân tích chuyên sâu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Đọc hiểu luồng code, phát hiện lỗi logic (Debug)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 8–10</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bài cũ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">3</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Sáng tạo</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tư duy kiến trúc, tối ưu hiệu năng hệ thống</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 11–12</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bài mới</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">2</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông hiểu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tiếp thu khái niệm, thuật ngữ, mục đích công nghệ mới</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 13–14</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bài mới</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">2</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Vận dụng sơ bộ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Nhận diện cú pháp chuẩn và cách triển khai cơ bản</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 15</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bài mới</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">1</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phân tích sơ bộ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">So sánh công nghệ mới với giải pháp đã biết</td>
    </tr>
  </tbody>
</table>

### 1.3 Ngân hàng câu hỏi (45 câu)

- **30 câu bài cũ** (phân bổ đều 3 mức độ: Vận dụng 12 câu / Phân tích 10 câu / Sáng tạo 8 câu)
- **15 câu bài mới** (Thông hiểu 6 / Vận dụng sơ bộ 6 / Phân tích sơ bộ 3)

### 1.4 Ma trận phân loại sinh viên

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Nhóm</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Kết quả</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phân loại</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Chiến thuật</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Gương mẫu</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">≥13/15 + Bài mới ≥4/5</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Xuất sắc: Nắm chắc bài cũ, chủ động nghiên cứu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Làm Leader nhóm / giao bài Sáng tạo khó hơn</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Nỗ lực</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">7–9/15 + Bài mới ≥3/5</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Chăm chỉ nhưng hổng nền tảng</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bổ trợ bài cũ ngay tại lớp</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Tư duy tốt</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">10–12/15 + Bài mới <3/5</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thực chiến tốt nhưng không xem bài mới</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Cảnh cáo kỷ luật, yêu cầu xem lại tài liệu</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Ổn định</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">10–12/15 + Bài mới ≥3/5</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Trung bình, đối phó</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Push để lên Gương mẫu</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Ẩn mình</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">7–9/15 + Bài mới <3</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông minh nhưng lười</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Theo dõi sát, tạo áp lực tích cực</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Nguy cơ</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><7/15</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Yếu cả hai</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Mentoring 1:1 / Trợ giảng hỗ trợ</td>
    </tr>
  </tbody>
</table>

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

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông số</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quy định</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>5 câu</b></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thời gian làm</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Không giới hạn thời gian</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số lần làm</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tối đa <b>3 lần</b></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Ngưỡng đạt</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>5/5 câu</b> (100%)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phản hồi sai</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Hiển thị ngay: "Sai rồi, xem lại phút XX:XX của video"</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Vị trí</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Cuối mỗi lesson (sau Video/Reading)</td>
    </tr>
  </tbody>
</table>

### 2.2 Mục tiêu đánh giá

- **Nhận diện**: Xác nhận sinh viên nắm từ khóa, cú pháp, khái niệm cốt lõi của bài mới
- **Thông hiểu**: Kiểm tra khả năng giải thích cơ chế hoạt động và luồng thực thi
- **Sàng lọc**: Phát hiện sớm các hiểu nhầm phổ biến để điều chỉnh học tập

### 2.3 Phân bổ câu hỏi

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">STT</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Mức độ Bloom</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Mục tiêu</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tỷ lệ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 1–2</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Nhận biết</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Từ khóa, cú pháp, định nghĩa</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">40%</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 3–4</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông hiểu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Cơ chế hoạt động, luồng thực thi</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">40%</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 5</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Vận dụng</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Áp dụng vào tình huống đơn giản</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">20%</td>
    </tr>
  </tbody>
</table>

### 2.4 Quy tắc viết câu hỏi trong lesson

- **Gắn trực tiếp** với nội dung video/reading của lesson đó
- Phải có **timestamp** phản hồi khi sai ("Xem lại phút XX:XX")
- Câu hỏi **không được vượt quá** phạm vi bài học hiện tại
- Các distractor phải là **hiểu nhầm điển hình** của người mới học

---

## 3. TIÊU CHUẨN QUIZZ CUỐI GIỜ

### 3.1 Thông số kỹ thuật

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông số</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quy định</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>15 câu</b></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thời gian làm</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">20 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số lần làm</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">1 lần</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Ngưỡng đạt</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">≥ 10/15</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phạm vi</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Toàn bộ Session (bài cũ + bài mới đã học trong ngày)</td>
    </tr>
  </tbody>
</table>

### 3.2 Phân bổ câu hỏi

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">STT</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Mức độ</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số câu</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Mục tiêu đánh giá</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 1–6</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Vận dụng</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">6</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Triển khai đúng cú pháp và chức năng cơ bản</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 7–11</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phân tích</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">5</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Đọc luồng code, bắt lỗi logic, hiểu cơ chế vận hành</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Câu 12–15</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Sáng tạo</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">4</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tư duy Best Practice, chọn giải pháp tối ưu</td>
    </tr>
  </tbody>
</table>

### 3.3 Ma trận phân loại sinh viên cuối giờ

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Nhóm</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Kết quả</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phân loại</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Chiến thuật</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Làm chủ</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">13–15 câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Xuất sắc: Hiểu bản chất, code sạch, xử lý bẫy logic</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Giao Project-based / Chỉ định làm Mentor</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Đạt</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">10–12 câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Khá: Nắm vững cú pháp, còn sai ở Phân tích/Tối ưu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Viết Comment giải thích, bài tập mức Giỏi</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Cơ bản</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">7–9 câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Trung bình: Dừng ở copy-paste / shadowing</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Làm lại từ đầu không nhìn mẫu, xem lại Record</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><b>Cần kèm</b></td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><7 câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Yếu: Chưa hiểu luồng code</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Kèm 1:1, rà soát hổng kiến thức nền</td>
    </tr>
  </tbody>
</table>

### 3.4 Mục tiêu đánh giá cuối giờ

- **Validation**: Sinh viên chuyển hóa lý thuyết → thực hành
- **Retention**: Nhớ được giải pháp xử lý bug và quy tắc tối ưu từ buổi học
- **Integration**: Kết hợp công nghệ mới với nền tảng cũ

---

## 4. TIÊU CHUẨN BÀI ĐỌC (READING)

### 4.1 Thông số kỹ thuật

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông số</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quy định</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Độ dài</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">800–1500 từ/bài đọc</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thời gian đọc ước tính</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">8–15 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Định dạng xuất</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">HTML (render trong hệ thống)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Cấu trúc bắt buộc</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">5 phần (xem bên dưới)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số code example</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">2–4 ví dụ thực tế</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Font code</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Fira Code, monospace</td>
    </tr>
  </tbody>
</table>

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

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông số</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quy định</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thời lượng</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">4–6 phút (240–360 giây)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Canvas</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">1920×1080px (Full HD)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Framework</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">HyperFrames (sub-composition architecture)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số scene</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">4–6 scenes</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Narration</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">400–800 từ</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Font chữ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Inter (text) + Fira Code (code)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Background</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">#0f1117 + dot grid pattern</td>
    </tr>
  </tbody>
</table>

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

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Element</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Giá trị</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Background</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#0f1117</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Text chính</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#e6edf3</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Text phụ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#c9d1d9</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Keyword</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#ff7b72</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">String</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#a5d6ff</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Variable</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#79c0ff</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Function</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#d2a8ff</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Good/Pass</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#3fb950</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Error/Bad</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>#f85149</code></td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Card bg</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;"><code>rgba(9,9,11,0.7)</code> + border <code>rgba(255,255,255,0.08)</code></td>
    </tr>
  </tbody>
</table>

### 5.6 Audio Architecture

- Audio files: `assets/tts/scene_XX.mp3`
- **BẮT BUỘC**: Tất cả `<audio>` đặt trong `index.html` (root), KHÔNG trong sub-composition
- Audio track-index bắt đầu từ 20+
- `data-start` trong index.html là timestamp tuyệt đối của root timeline

---

## 6. TIÊU CHUẨN SLIDE BÀI GIẢNG

### 6.1 Thông số kỹ thuật

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông số</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quy định</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số slide/lesson</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">8–15 slide</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tỷ lệ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">16:9 (1920×1080)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Slide đầu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Title slide bắt buộc</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Slide cuối</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Summary + Q&A slide</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Code trên slide</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tối đa 15 dòng/slide</td>
    </tr>
  </tbody>
</table>

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

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông số</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quy định</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số bài tập/lesson</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">2–4 bài</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phân loại độ khó</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">3 cấp: Cơ bản / Nâng cao / Xuất sắc</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thời gian làm ước tính</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Cơ bản: 15–20 phút / Nâng cao: 25–35 phút / Xuất sắc: 45–60 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Ngôn ngữ đề bài</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tiếng Việt (code comment: Tiếng Anh)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Auto-grading</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bắt buộc có test cases</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số test cases tối thiểu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">5 (bao gồm edge cases)</td>
    </tr>
  </tbody>
</table>

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

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thông số</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quy định</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Công cụ render</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Markmap (Markdown-based)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Node trung tâm</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tiêu đề Session/Lesson</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số nhánh cấp 1</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">4–7 nhánh</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số nhánh cấp 2</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">3–5 nhánh/nhánh cấp 1</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số nhánh cấp 3</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">2–3 (chỉ cho các nhánh quan trọng)</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tổng nodes</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">30–80 nodes</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Ngôn ngữ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Tiếng Việt (thuật ngữ kỹ thuật giữ nguyên tiếng Anh)</td>
    </tr>
  </tbody>
</table>

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

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thành phần</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Số lượng</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Thời lượng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Lessons</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">2–4</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">—</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Video/lesson</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">1</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">4–6 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Reading/lesson</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">1</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">8–15 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quizz in-lesson</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">5 câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Không giới hạn</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quizz đầu giờ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">15 câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">15 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quizz cuối giờ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">15 câu</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">20 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Bài tập Lab</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">2–4</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">15–60 phút</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Mindmap</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">1/session</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">—</td>
    </tr>
  </tbody>
</table>

### 9.3 Ma trận nội dung theo Bloom's Taxonomy

<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">
  <thead>
    <tr style="background-color: rgba(175, 184, 193, 0.2);">
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Phần nội dung</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">Nhận biết</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">Thông hiểu</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">Vận dụng</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">Phân tích</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">Đánh giá</th>
      <th style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">Sáng tạo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Video</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Reading</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quizz in-lesson</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quizz đầu giờ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Quizz cuối giờ</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Lab cơ bản</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Lab nâng cao</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
    </tr>
    <tr>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: left;">Lab xuất sắc</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">—</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
      <td style="padding: 8px; border: 1px solid #d0d7de; text-align: center;">✅</td>
    </tr>
  </tbody>
</table>

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

## 10. TIÊU CHUẨN SESSION MINI PROJECT (DỰ ÁN NHỎ)

### 10.1 Cấu trúc Session Dự án (No-Lesson Policy)
Khác với các Session học lý thuyết thông thường, Session Mini Project là dạng session thực chiến tổng hợp. 
* **Quy tắc không chứa bài học (No-Lesson Policy):** Session Mini Project tuyệt đối không chia thành các Lesson và không chứa bài đọc (Reading), Slide hay Video bài học nhỏ.
* **Tập hợp tài nguyên cấu thành:** Toàn bộ Session chỉ chứa 3 cấu phần dữ liệu chính:
  1. **project_entry_tests** (Đề kiểm tra đầu giờ song song)
  2. **project_srs** (Tài liệu đặc tả yêu cầu hệ thống SRS)
  3. **project_mini_project** (Đề bài dự án nhỏ & Tiêu chí chấm điểm Rubric)

### 10.2 Tiêu chuẩn Đề kiểm tra đầu giờ (Entry Tests)
* **Số lượng:** Bắt buộc sinh đúng **4 đề kiểm tra song song** ứng với các nghiệp vụ khác nhau (ví dụ: `cinema_booking`, `library_catalog`, `hotel_room_booking`, `courier_shipping`).
* **Độ khó:** Cơ bản (làm trong 30-40 phút).
* **Kiểm soát rò rỉ kiến thức (No Concept Leakage):** Chỉ kiểm tra những kiến thức học viên đã học ở các buổi trước. Tuyệt đối cấm kiểm tra cú pháp hay công nghệ mới của chính buổi học hiện tại hoặc các buổi sau.
* **Cấu trúc đề bài bắt buộc:**
  - Tiêu đề căn giữa: `## <center>[Tên đề bài tiếng Việt] ([Tên đề bài tiếng Anh])</center>`. Cấm đánh số thứ tự ở tiêu đề này.
  - Phải chứa đủ 4 tiêu đề H3 bôi đậm:
    - ### **1. Mục tiêu**
    - ### **2. Yêu cầu** (Yêu cầu thiết lập database giả lập trong RAM có sẵn ít nhất 2 bản ghi mẫu ban đầu. Đặc tả chính xác 3 API CRUD rút gọn có Method, Endpoint, Inputs, Logic xử lý và ví dụ Response JSON bọc trong Unified Envelope 6 trường).
    - ### **3. Tiêu chí đánh giá** (Thang điểm tổng 10 điểm chia nhỏ cho các tiêu chí kỹ thuật).
    - ### **4. Yêu cầu nộp bài** (Định dạng chuẩn 4 dòng hướng dẫn nộp link GitHub).

### 10.3 Tiêu chuẩn Tài liệu Đặc tả Yêu cầu Hệ thống (SRS)
Tài liệu SRS cung cấp thông tin kỹ thuật toàn diện cho Mini Project của học viên.
* **Nguyên tắc nghiệp vụ thực tế:** Thiết kế quy trình nghiệp vụ có chiều sâu doanh nghiệp (quản lý đơn hàng, thanh toán, phân quyền nhóm).
* **Cấm cung cấp code mẫu:** SRS tuyệt đối cấm chứa mã nguồn triển khai thực tế (như định nghĩa hàm Python, Class Java/TypeScript). Chỉ mô tả quy tắc, công thức hoặc mã giả (pseudocode).
* **Sơ đồ nghiệp vụ/Ảnh sự cố:**
  - Chứa đúng 1 prompt tạo ảnh (Prompt tạo ảnh bối cảnh nghiệp vụ kịch tính hoặc sự cố kỹ thuật).
  - Vị trí đặt: Nằm trong phần **1. Tổng quan hệ thống** hoặc **2. Đặc tả chức năng**.
  - Định dạng bắt buộc (viết bằng tiếng Anh): `*Prompt tạo ảnh: A realistic 16:9 cinematic photo of [mô tả chi tiết bối cảnh]. [Trạng thái con người/thiết bị căng thẳng hoặc lỗi hệ thống]. Cinematic lighting, detailed environment, professional photography, dramatic corporate lighting.*`
  - Phong cách bắt buộc là chụp ảnh điện ảnh chân thực (realistic cinematic photo), cấm dùng nét vẽ phẳng hay sơ đồ đơn điệu.
* **Chiều rộng bảng HTML:** Tất cả bảng (API, mã lỗi) bắt buộc phải co giãn 100% bằng cách sử dụng thẻ:
  `<table style="width: 100%; min-width: 100%; display: table; border-collapse: collapse;" width="100%">`
* **Cấu trúc tài liệu SRS bắt buộc:**
  - Tiêu đề căn giữa: `## <center>Tài liệu đặc tả Hệ thống API [Tên nghiệp vụ] ([Tên nghiệp vụ tiếng Anh])</center>`.
  - Phải chứa đủ 7 tiêu đề H3 bôi đậm:
    - ### **1. Tổng quan hệ thống** (Mục đích, đối tượng sử dụng, prompt tạo ảnh).
    - ### **2. Đặc tả chức năng (Functional Requirements)** (Đặc tả 4-5 API cốt lõi, bao gồm tìm kiếm nâng cao dùng Regex và thuật toán xử lý dữ liệu nội bộ).
    - ### **3. Đặc tả phi chức năng (Non-Functional Requirements)** (Bảo mật, lọc trường nhạy cảm bằng DTO, ẩn stack trace lỗi).
    - ### **4. Đặc tả dữ liệu (Data Model / Schemas)** (Các schema dữ liệu đầu vào và đầu ra JSON).
    - ### **5. Danh mục lỗi và Mã thông báo (Error Codes & Unified Envelope)** (Response Envelope chuẩn 6 trường: statusCode, message, data, error, timestamp, path; và bảng mã lỗi `ERR-TASK-xx`).
    - ### **6. Bảng tổng hợp tình huống lỗi (Edge Cases Mapping)** (Bảng HTML 100% map vị trí phát sinh, tình huống lỗi, mã lỗi, và hành động xử lý).
    - ### **7. Giao diện kiểm thử và Phản hồi hệ thống (API Specifications & Interface)** (Swagger UI/ReDoc, Try it out, response mẫu).

### 10.4 Tiêu chuẩn Đề bài Mini Project & Rubric chấm điểm
* **Nguyên tắc tinh gọn:** Đề bài Mini Project đóng vai trò như các thẻ nhiệm vụ tóm tắt (Task card), cấm liệt kê lại cấu trúc JSON hay bảng lỗi trùng lặp với SRS.
* **Liên kết tài nguyên:** Bắt buộc có chú thích dẫn link tương đối trực tiếp tới SRS:
  `*Ví dụ chú thích: "Học viên bắt buộc phải tự nghiên cứu và tuân thủ các quy định đặc tả chi tiết về cấu trúc dữ liệu, Pydantic validation, danh mục mã lỗi nghiệp vụ tại [Tài liệu đặc tả SRS](../Tài liệu đặc tả SRS/tai_lieu_dac_ta_yeu_cau_srs.md)."*
* **Cấu trúc đề bài bắt buộc:**
  - Tiêu đề căn giữa: `## <center>[Mini project] Hệ thống API [Tên nghiệp vụ] ([Tên nghiệp vụ tiếng Anh])</center>`.
  - Phải chứa đủ 3 tiêu đề H3 bôi đậm trong phần content:
    - ### **1. Mục tiêu dự án**
    - ### **2. Đề bài và Yêu cầu** (Liệt kê công việc lớn: Task 1, Task 2, Task 3...).
    - ### **3. Yêu cầu nộp bài** (Định dạng chuẩn 4 dòng hướng dẫn nộp link GitHub).
* **Tiêu chí chấm điểm (Rubric):** Nằm riêng trong cấu phần `<rubric>` của Mini Project, thiết kế tổng thang điểm 100 điểm + bonus theo đúng cấu trúc H3/H4 bắt buộc:
  - Đầu tiêu đề: `### **Tiêu chí chấm điểm (AI)**`
  - Tên dự án: `**[Tên Dự Án] — Tổng điểm: 100 điểm**`
  - 5 nhóm tiêu chí bắt buộc (H4 bôi đậm):
    - #### **1. Thiết lập cấu trúc và Khởi tạo — 20 điểm**
    - #### **2. Logic nghiệp vụ cốt lõi — 30 điểm**
    - #### **3. Kiểm chuẩn dữ liệu và Xử lý ngoại lệ — 30 điểm**
    - #### **4. Chức năng nâng cao hoặc Kiểm thử tự động — 10 điểm**
    - #### **5. Chất lượng mã nguồn và Quy chuẩn nộp bài — 10 điểm**
    - #### **Điểm cộng khuyến khích (Bonus) — 5 đến 10 điểm**

### 10.5 Tiêu chuẩn Ngôn từ & Nhãn phân loại
* **Không suồng sã:** Tuyệt đối cấm các từ ngữ suồng sã như "nhé", "nhé các bạn", "thân mến", "nha", "nhe".
* **Không nhắc tới công cụ AI:** Tuyệt đối cấm nhắc tới các từ khóa chỉ hệ thống tự động/AI ("AI", "Assistant", "ChatGPT", "Gemini", "LLM", "Copilot") trong toàn bộ đề bài và tài liệu SRS (ngoại trừ tiêu đề `Tiêu chí chấm điểm (AI)` của Rubric).
* **Cấm nhãn học lực:** Tuyệt đối không ghi các dòng chữ phân loại học lực (yếu/trung bình/khá/giỏi) hoặc mức độ khó vào tiêu đề hay nội dung của bài học/đặc tả để tránh gây áp lực tiêu cực cho học viên.

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

project_session:
  - no_lessons: true
  - entry_tests_count: 4
  - srs_has_7_bold_h3_headers: true
  - srs_has_realistic_cinematic_photo_prompt_in_english: true
  - srs_has_no_code_implementation_blocks: true
  - srs_tables_have_width_100_percent: true
  - mini_project_has_3_bold_h3_headers: true
  - mini_project_links_to_srs_relatively: true
  - rubric_starts_with_ai_criteria_header: true
  - rubric_has_5_required_groups_and_bonus: true
  - language_has_no_forbidden_ai_or_conversational_words: true
```

---

*Tài liệu này được xây dựng bởi AI Education Specialist, dựa trên tài liệu gốc của Rikkei Education.*
*Mọi thay đổi cần được PM và Academic Lead phê duyệt trước khi áp dụng.*
