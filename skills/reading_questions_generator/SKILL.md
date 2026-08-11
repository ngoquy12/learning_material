---
name: reading_questions_generator
description: Generate a 3 to 4 multi-case practical scenario question set anchored on reading.html code snippets to verify actual reading comprehension, exported as Markdown (reading_questions.md) inside the 'Câu hỏi bài đọc' folder. Target output language is 100% Accented Vietnamese.
---

# Multi-Case Practical Reading Check Generator Skill — Rikkei Education Standards

This document defines the technical standards for the **`reading_questions_generator`** skill, responsible for generating practical multi-case reading comprehension check questions anchored directly on code snippets and scenario data from `reading.html`.

---

## 0. PEDAGOGICAL OBJECTIVE & MULTI-CASE CODE TRACING MANDATE

1. **Primary Evaluation Objective**:
   - The Reading Comprehension Question Suite (`reading_questions.md`) is specifically designed to **verify that students have ACTUALLY READ, TRACED, and DEEPLY UNDERSTOOD the lesson article (`reading.html`)**.
   - Questions MUST NOT be long, text-heavy, or abstract theoretical essays. Questions MUST be **practical, concise, and structured around multi-case execution tracing**.

2. **Single Anchored Code Snippet / Scenario Card**:
   - Every reading question set MUST extract **1 concrete code snippet or CLI/configuration scenario** directly from Section 2 or Section 3 of `reading.html`.
   - The code snippet is presented at the top of the question set as the single source of truth.

3. **4-Case Evaluation Structure (Quy tắc 4 Trường hợp Thử nghiệm)**:
   - **Case 1 (Forward Tracing - Input X1 ➔ Output Y1)**: Provide specific input data $X_1$ ➔ Student identifies which condition branches execute and the exact output/variable state $Y_1$. (e.g. *"Nếu `order_amount = 250000`, chương trình chạy qua những nhánh nào và `discount_amount` bằng bao nhiêu?"*)
   - **Case 2 (Alternative Input Tracing - Input X2 ➔ Output Y2)**: Change input data to $X_2$ ➔ Student traces how execution flow and output change. (e.g. *"Nếu đổi `order_amount = 50000`, kết quả thu được là gì?"*)
   - **Case 3 (Reverse Deduction - Target Output Y3 ➔ Input X3)**: Provide target output $Y_3$ ➔ Student deduces the required input range or variable condition $X_3$. (e.g. *"Để nhận mức giảm giá 50,000đ, giá trị `order_amount` phải thỏa mãn điều kiện gì?"*)
   - **Case 4 (Edge Case & Gotcha Trap Tracing)**: Provide boundary/invalid input or code mutation (e.g., negative input, wrong condition ordering) ➔ Student pinpoints logic flaw, unreachable code, or error output.

4. **Domain-Agnostic Contract (Cấm Hardcode theo Môn)**:
   - **Executable Programming (Python, JS, Java, C++, SQL...)**: Trace variables, branching execution paths, boundary values, and console outputs.
   - **Tooling & Process (Git, Docker, VS Code, Agile...)**: Trace CLI command parameters, file config options, repository states, and terminal error outputs.

---

## 1. QUESTION MATRIX & SPECIFICATIONS

| # | Question Case Type | Pedagogical Objective | Expected Answer Format |
| :-: | :--- | :--- | :--- |
| **1** | **Forward Input Tracing** | Test step-by-step code execution flow for standard input data. | Step-by-step execution path + calculated output value. |
| **2** | **Alternative Input Tracing** | Test understanding of alternative branching logic. | Branch decision + new output value. |
| **3** | **Reverse Input Deduction** | Test reverse mathematical/logical deduction from target output. | Required input condition / value range. |
| **4** | **Gotcha & Edge Case Tracing** | Test detection of boundary errors, wrong condition order, or invalid inputs. | Root cause analysis + corrected code/input logic. |

---

## 2. OUTPUT FORMAT STANDARDS (`reading_questions.md`)

The reading comprehension questions MUST be formatted as a clean Markdown document saved at `Câu hỏi bài đọc/reading_questions.md`:

```markdown
# Bộ câu hỏi kiểm tra bài đọc (Reading Comprehension Questions)

## Tình huống & Mã nguồn kiểm tra
Dựa trên mã nguồn nghiệp vụ được trích dẫn từ bài đọc (`reading.html`):

```python
# [Đoạn mã nguồn / kịch bản thực tế trích từ bài đọc]
```

---

### Câu 1 (Xung hướng - Tính toán kết quả với dữ liệu X):
[Nội dung câu hỏi: Cho dữ liệu đầu vào cụ thể X, chỉ ra các dòng lệnh thực thi và kết quả trả về...]
> **Gợi ý trả lời & Định hướng đáp án:** 
> - [Các bước phân tích điều kiện đầu vào và luồng chạy...]
> - [Kết quả biến / Console Output thu được...]

---

### Câu 2 (Xung hướng - Thử nghiệm với mốc dữ liệu Y):
[Nội dung câu hỏi: Thay đổi dữ liệu đầu vào thành Y, chỉ ra nhánh điều kiện được kích hoạt và kết quả mới...]
> **Gợi ý trả lời & Định hướng đáp án:** 
> - [Phân tích sự thay đổi nhánh rẽ...]
> - [Kết quả biến / Console Output mới...]

---

### Câu 3 (Nghịch hướng - Suy luận dữ liệu đầu vào từ kết quả Z):
[Nội dung câu hỏi: Để nhận được kết quả mong muốn Z, dữ liệu đầu vào cần thỏa mãn điều kiện gì?]
> **Gợi ý trả lời & Định hướng đáp án:** 
> - [Công thức / điều kiện logic toán học của biến đầu vào...]

---

### Câu 4 (Phân tích bẫy lỗi & Trường hợp biên):
[Nội dung câu hỏi: Phân tích bẫy lỗi Gotcha hoặc trường hợp dữ liệu đầu vào âm / vượt khoảng / sai thứ tự...]
> **Gợi ý trả lời & Định hướng đáp án:** 
> - [Phân tích nguyên nhân lỗi / Unreachable code...]
> - [Giải pháp khắc phục đúng quy chuẩn PEP 8 / Best Practice...]
```

---

## 3. LESSON FOLDER STRUCTURE LOCATION

```text
📁 Lesson XX - [Tên Bài Học]/
├── 📂 Bài đọc/
│   └── 📄 reading.html
├── 📂 Câu hỏi bài đọc/
│   └── 📄 reading_questions.md
├── 📂 Câu hỏi Quizz/
│   └── 📄 quiz.json
└── 📂 Video/
    └── 📄 SCRIPT.md
```
