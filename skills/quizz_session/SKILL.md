---
name: quizz_session
description: Generate comprehensive session-level entrance and exit quizzes based on current and previous lesson topics, formatted as 13-column flat structures.
---

# Kỹ năng thiết kế câu hỏi trắc nghiệm buổi học (Quizz Session Generator Skill)

## 1. Mục tiêu
Thiết kế và cấu trúc hai bộ đề kiểm tra trắc nghiệm buổi học dạng phẳng (flat structure) phục vụ cho hệ thống thi trắc nghiệm (Entrance Quiz - 45 câu và Exit Quiz - 45 câu). Đảm bảo phân bổ độ khó theo Bloom's taxonomy và tỉ lệ phân tách câu hỏi bài mới/bài cũ.

## 2. Tiêu chuẩn Nội dung (Phân bổ 45 câu)

### 2.1. Đề thi đầu giờ (Entrance Quiz)
Kiểm tra kiến thức bài cũ (tỷ lệ 2/3) kết hợp khởi động bài mới (tỷ lệ 1/3) để kiểm soát tự học ở nhà.
* **Nhóm 30 câu Bài cũ:**
  - `STT 1-12 (12 câu)`: Vận dụng chuyên sâu (Application) | difficulty: `4`.
  - `STT 13-21 (9 câu)`: Phân tích lỗi sai/Debug (Analysis) | difficulty: `6`.
  - `STT 22-30 (9 câu)`: Tối ưu hóa & Bảo mật (Optimization & Security) | difficulty: `8`.
* **Nhóm 15 câu Bài mới:**
  - `STT 31-36 (6 câu)`: Thông hiểu cơ chế (Understand) | difficulty: `5`.
  - `STT 37-42 (6 câu)`: Vận dụng sơ bộ (Basic Apply) | difficulty: `7`.
  - `STT 43-45 (3 câu)`: Phân tích cơ bản (Basic Analyze) | difficulty: `9`.

### 2.2. Đề thi cuối giờ (Exit Quiz)
Đo lường mức độ tiếp thu và ứng dụng thực hành ngay tại lớp đối với bài mới.
* **Nhóm 45 câu Bài mới hoàn toàn:**
  - `STT 1-18 (18 câu)`: Vận dụng nghiệp vụ (Application) | difficulty: `6`.
  - `STT 19-33 (15 câu)`: Phân tích lỗi nghiệp vụ & Sửa code (Debug) | difficulty: `10`.
  - `STT 34-45 (12 câu)`: Sáng tạo giải pháp/Tối ưu hóa (Create) | difficulty: `11`.

## 3. Quy chuẩn đáp án nhiễu & Văn phong
* **Đồng nhất đáp án**: Cả 4 đáp án (A, B, C, D) phải có độ dài tương đồng nhau.
* **Đáp án nhiễu thông minh (Plausible Distractors)**: Các phương án sai phải phản ánh lỗi sai thực tế của lập trình viên (ví dụ: sai import path, quên await, sai syntax decorator).
* **Văn phong**: Khách quan, trung lập. Tuyệt đối cấm dùng các cụm từ tham chiếu mơ hồ ("theo video", "trong bài học này").
* **Đầu ra**: Trả về danh sách JSON chứa các câu hỏi theo đúng định dạng 13 cột của Excel template.
