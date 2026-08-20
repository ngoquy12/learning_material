# 📊 BỘ TÀI LIỆU HƯỚNG DẪN 04: BƯỚC 3 - SINH SLIDE DECK, QUIZ EXCEL & BÀI TẬP VỀ NHÀ

## 1. 🎯 Mục Đích
Tự động hóa sản xuất các tài nguyên phụ trợ giảng dạy hoàn chỉnh: Slide bài giảng PowerPoint (`.pptx`) & HTML, Bộ Quiz trắc nghiệm 45 câu Excel, Bộ 17 bài tập về nhà phân cấp thang Bloom có rubric chấm điểm, và Sơ đồ tư duy Mindmap.

---

## 2. 💻 1. Slide Bài Giảng PowerPoint & HTML (`Slide bài giảng/`)
- Tự động tạo bộ Slide bài giảng chính thức định dạng **PowerPoint (`Slide_Bai_Giang_Session_XX.pptx`)** và **HTML tương tác (`slides.html`)**.
- Tuân thủ nghiêm ngặt nguyên tắc **3-30-300 Typography** (tối đa 3 ý/slide, 30 chữ/ý, font size >= 18px), Card Color Coding hiện đại, Bento Grid, và không chứa emoji hạt gạo.
- Tự động sinh file **`outline_bai_giang.md`** hỗ trợ giảng viên lên lớp với kịch bản chi tiết và timecode.
- Xuất file **`slide_deck_review_report.md`** đánh giá kiểm định chất lượng slide.

---

## 3. 📝 2. Bộ Quiz Đầu Giờ & Cuối Giờ (45 Câu Excel `.xlsx`)
- **Quiz Đầu Giờ (Entrance Quiz)**: 45 câu trắc nghiệm (30 câu ôn tập kiến thức Session cũ + 15 câu gợi mở chủ đề mới).
- **Quiz Cuối Giờ (Exit Quiz)**: 45 câu trắc nghiệm (100% câu hỏi mới) củng cố toàn bộ trọng tâm bài học vừa học.
- Tuân thủ **9 nguyên tắc sư phạm Quizz**: Không hỏi lý thuyết suông, 100% tình huống thực tế, 4 đáp án đồng đều độ dài, phân bổ ngẫu nhiên đáp án đúng.
- Xuất bản tệp Excel chuẩn định dạng LMS:
  - `Session XX._Quizz_Dau_Gio_*.xlsx`
  - `Session XX._Quizz_Cuoi_Gio_*.xlsx`

---

## 4. 🏋️ 3. Bộ Bài Tập Về Nhà 17 Thư Mục & Rubric Chấm Điểm (`Bài tập/`)
Bộ bài tập được tổ chức gọn gàng thành **17 thư mục con chuyên biệt** kèm theo file tiêu chí chấm điểm tổng hợp ở thư mục gốc:
- **`tieu_chi_danh_gia.md`**: Bảng Rubric 100 điểm phân bổ theo 5 tiêu chuẩn đánh giá.
- **17 Thư mục bài tập**:
  - `1_van_dung_co_ban_1_...` đến `6_van_dung_co_ban_6_...`: Bài tập sửa lỗi cú pháp & logic (Debugging).
  - `7_van_dung_nang_cao_1_...` đến `12_van_dung_nang_cao_6_...`: Bài tập xử lý nghiệp vụ Backend/Frontend thực tế.
  - `13_sang_tao_1_...` đến `15_sang_tao_3_...`: Mini project thiết kế module hoàn chỉnh (quyền tự chủ tối đa cho học viên).
  - `16_tong_hop_demo_giang_vien_tren_lop`: Bài tập tổng hợp live-coding trên lớp.
  - `17_tong_hop_he_thong_kien_thuc_mindmap`: Bài tập hệ thống hóa kiến thức.
- Mỗi thư mục con bao gồm 2 file Markdown chuẩn hóa: `de_bai_bai_tap.md` và `tieu_chi_cham_diem_ai.md`.

---

## 5. 🧠 4. Sơ Đồ Tư Duy Mindmap (`Mindmap/session_mindmap.md`)
- Xuất bản sơ đồ tư duy Markdown / Mermaid cô đọng cây kiến thức của toàn bộ Session, phục vụ việc ôn tập nhanh và liên kết vào Obsidian Knowledge Graph.