# Kỹ năng thiết kế và tạo Câu hỏi trắc nghiệm (E-learning Quiz & Session Quiz Skill)

Bộ kỹ năng này hướng dẫn Agent cách thiết kế, chuẩn hóa và tạo ngân hàng câu hỏi trắc nghiệm (bao gồm Quiz từng bài học/Lesson và Quiz tổng hợp buổi học/Session) cho hệ thống E-learning, đáp ứng đầy đủ tiêu chuẩn sư phạm và định dạng dữ liệu xuất khẩu.

---

## 🎯 1. Các Nguyên Tắc Cốt Lõi Thiết Kế Câu Hỏi Trắc Nghiệm (Quizz Standards)

Khi tạo bất kỳ câu hỏi trắc nghiệm nào, Agent bắt buộc phải tuân thủ nghiêm ngặt 6 nguyên tắc sư phạm sau:

1. **Nguyên tắc đơn nhiệm (Single Concept):** Mỗi câu hỏi chỉ tập trung đánh giá duy nhất một kiến thức hoặc một kỹ năng. Đảm bảo phần code mẫu hoặc ngữ cảnh không chứa thêm các lỗi cú pháp hay logic ngoài lề để sinh viên tập trung tối đa vào vấn đề cần kiểm tra.
2. **Nguyên tắc ngữ cảnh hóa (Context-Driven):** Tránh các câu hỏi lý thuyết suông dạng định nghĩa ("Từ khóa break dùng để làm gì?"). Thay vào đó, hãy đặt sinh viên vào một tình huống nghiệp vụ/thực tế cụ thể (Scenario) để giải quyết vấn đề.
3. **Nguyên tắc phương án nhiễu "Thông minh" (Plausible Distractors):** Các phương án sai (nhiễu) phải có vẻ hợp lý và dựa trên lỗi sai phổ biến của sinh viên (ví dụ: lỗi lặp vô tận, lỗi lặp thừa/thiếu 1 lần). Tuyệt đối cấm đưa ra các đáp án ngớ ngẩn hoặc dạng "Cả 3 đáp án trên đều sai/đúng".
4. **Nguyên tắc đồng nhất (Homogeneity):** Cả 4 phương án trả lời (A, B, C, D) phải tương đồng nhau về mặt độ dài, cấu trúc ngữ pháp và phạm vi kiến thức. Tránh việc đáp án đúng thì dài và chi tiết, còn các phương án nhiễu thì ngắn cụt ngủn khiến học viên đoán mò được câu trả lời.
5. **Nguyên tắc sắc bén (No clues):** Loại bỏ mọi dấu hiệu mách nước. Không dùng các từ khóa trong câu hỏi trùng lặp trực tiếp với từ khóa trong đáp án đúng (Keyword matching).
6. **Nguyên tắc khách quan & có ý nghĩa (Objectivity & Contextual Integrity):** Đặt các câu hỏi có ý nghĩa chuyên môn rõ ràng. Nghiêm cấm sử dụng các từ ngữ tham chiếu bối cảnh bài học/bài giảng hay nguồn trích xuất mơ hồ như: "theo video", "trong video này", "lời giảng viên", "slide bài giảng", "slide đề cập", "từ một nguồn nào đó không rõ", v.v. Câu hỏi phải được phát biểu một cách khách quan, chính thống như một đề thi chuẩn.

---

## 📚 2. Cấu Trúc Đề Thi & Độ Khó (Difficulty) Cho Ngân Hàng Câu Hỏi

Hệ thống hỗ trợ 2 cấp độ đánh giá trắc nghiệm:

### 2.1. Quiz Bài học (Lesson Quiz) - 5 Câu hỏi
Mỗi bộ Quiz bài học lý thuyết gồm đúng 5 câu hỏi theo ma trận Bloom sau:
1. **Câu 1: Định nghĩa/Cú pháp (Nhớ)**: Kiểm tra cú pháp khai báo, tên thư viện, tham số cơ bản.
2. **Câu 2: Luồng xử lý/Cơ chế (Hiểu)**: Kiểm tra thứ tự thực thi của máy chủ, middleware, router hoặc database query.
3. **Câu 3: Đọc hiểu code (Vận dụng)**: Đưa ra một đoạn code ngắn và hỏi kết quả trả về hoặc lỗi cú pháp.
4. **Câu 4: So sánh/Phân biệt (Phân tích)**: So sánh giữa hai phương pháp (ví dụ: Path parameters vs Query parameters, Async vs Sync).
5. **Câu 5: Dự đoán kết quả với bẫy (Đánh giá)**: Đoạn code phức tạp chứa bẫy logic (trap) dễ nhầm lẫn để kiểm tra mức độ hiểu sâu sắc của học viên.

### 2.2. Quiz Buổi học (Session Quiz) - 45 Câu hỏi
Được chia làm 2 loại đề kiểm tra:

#### A. Quiz Đầu Giờ (Entrance Quiz)
*Nhằm mục đích kiểm tra kiến thức bài cũ (tập trung kỹ năng & tư duy thực chiến) kết hợp khởi động bài mới (kiểm soát kỷ luật tự học).*
* **Phân bổ ngân hàng 45 câu**: **30 câu Bài cũ** và **15 câu Bài mới** (tỷ lệ 2:1).
* **Nhóm 30 câu Bài cũ:**
  1. *Câu 1 - 12 (12 câu): Vận dụng chuyên sâu (Application)*: category: `"BÀI CŨ"`, difficulty: `4`.
  2. *Câu 13 - 21 (9 câu): Phân tích chuyên sâu (Debug)*: category: `"BÀI CŨ"`, difficulty: `6`.
  3. *Câu 22 - 30 (9 câu): Sáng tạo (Optimization & Security)*: category: `"BÀI CŨ"`, difficulty: `8`.
* **Nhóm 15 câu Bài mới:**
  4. *Câu 31 - 36 (6 câu): Thông hiểu (Understand)*: category: `"BÀI MỚI"`, difficulty: `5`.
  5. *Câu 37 - 42 (6 câu): Vận dụng sơ bộ (Basic Apply)*: category: `"BÀI MỚI"`, difficulty: `7`.
  6. *Câu 43 - 45 (3 câu): Phân tích sơ bộ (Basic Analyze)*: category: `"BÀI MỚI"`, difficulty: `9`.

#### B. Quiz Cuối Giờ (Exit Quiz)
*Nhằm mục đích đo lường khả năng chuyển hóa kiến thức từ lý thuyết sang thực hành và độ bền vững kiến thức ngay tại lớp.*
* **Phân bổ ngân hàng 45 câu**: Toàn bộ thuộc **Bài mới** (Category: `BÀI MỚI`).
  1. *Câu 1 - 18 (18 câu): Vận dụng chuyên sâu (Application)*: difficulty: `6`.
  2. *Câu 19 - 33 (15 câu): Phân tích chuyên sâu (Debug)*: difficulty: `10`.
  3. *Câu 34 - 45 (12 câu): Sáng tạo (Create)*: difficulty: `11`.

---

## 📊 3. Định Dạng Template Excel Xuất Khẩu

### 3.1. Quy ước đặt tên file Excel (Export Naming Convention)
Khi xuất file Excel ngân hàng câu hỏi Quizz đầu giờ và Quizz cuối giờ, tên file bắt buộc phải bám sát tiêu đề của slide bài mới theo định dạng chuẩn:
* **Quizz đầu giờ:** `SessionXX._Quizz_Dau_Gio_<Ten_slide_bai_moi>.xlsx`
* **Quizz cuối giờ:** `SessionXX._Quizz_Cuoi_Gio_<Ten_slide_bai_moi>.xlsx`
*(Trong đó `SessionXX.` lấy từ chỉ số buổi học trên slide, ví dụ `Session02.`, các khoảng trắng và ký tự đặc biệt trong tên slide được chuyển thành dấu gạch dưới `_`).*

### 3.2. Cấu trúc bảng phẳng dữ liệu câu hỏi (13 cột)

| STT | Tên cột trong Excel    | Kiểu dữ liệu | Mô tả                                                                   |
| :-- | :--------------------- | :----------- | :---------------------------------------------------------------------- |
| 1   | `STT`                  | Number       | Số thứ tự từ 1 đến 45.                                                  |
| 2   | `question_content`     | Text         | Nội dung câu hỏi ngắn gọn, thực tế.                                     |
| 3   | `answer_1`             | Text         | Phương án trả lời 1 (loại bỏ ký tự tiền tố A., B. nếu có).              |
| 4   | `explanation_answer_1` | Text         | Giải thích ngắn gọn lý do vì sao phương án 1 đúng hoặc sai.             |
| 5   | `answer_2`             | Text         | Phương án trả lời 2.                                                    |
| 6   | `explanation_answer_2` | Text         | Giải thích ngắn gọn lý do vì sao phương án 2 đúng hoặc sai.             |
| 7   | `answer_3`             | Text         | Phương án trả lời 3.                                                    |
| 8   | `explanation_answer_3` | Text         | Giải thích ngắn gọn lý do vì sao phương án 3 đúng hoặc sai.             |
| 9   | `answer_4`             | Text         | Phương án trả lời 4.                                                    |
| 10  | `explanation_answer_4` | Text         | Giải thích ngắn gọn lý do vì sao phương án 4 đúng hoặc sai.             |
| 11  | `isCorrect`            | Number       | Chỉ mục đáp án đúng (`1` cho A, `2` cho B, `3` cho C, `4` cho D).       |
| 12  | `difficulty`           | Number       | Độ khó của câu hỏi theo thang từ `1` đến `11`.                         |
| 13  | `category`             | Text         | Phân loại nguồn câu hỏi: `"BÀI CŨ"` hoặc `"BÀI MỚI"`.                   |
