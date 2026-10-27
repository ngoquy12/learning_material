---
name: session_inclass_exercise_generator
description: Instructs AI agent to generate a 30-minute in-class synthesis session exercise for a theory session, combining all concepts taught across all lessons of the session into a single unified enterprise business scenario with explicit Input/Output parameters, strict "Closed How - Open What & Why" rule (no code spoilers), clean structure (Mục tiêu, Mô tả bối cảnh & I/O, Yêu cầu kỹ thuật, Checklist đánh giá), and 100% Accented Vietnamese output with zero AI clichés or text emojis.
---

# Session In-Class Synthesis Exercise Generator Skill — Rikkei Education Standards

This document defines the technical standards for the **`session_inclass_exercise_generator`** skill, responsible for generating a **30-minute in-class synthesis exercise** for a complete theory session.

---

## 0. PEDAGOGICAL OBJECTIVE & 6 CORE GUIDING PRINCIPLES

1. **Session-Wide Concept Synthesis (Vận dụng toàn bộ các nội dung của Session)**:
   - The exercise MUST synthesize and require students to apply all core technical concepts delivered across all lessons within that Session (e.g. combining `for` loops, `range()` function, `while` condition loops, and `break`/`continue` flow control).

2. **30-Minute In-Class Execution Scope (Thời lượng thực hiện 30 phút)**:
   - Designed for in-class completion within ~30 minutes under teacher guidance.
   - Basic/Intermediate application level. Functionality must be crisp, focused, and non-bloated.

3. **CLOSED HOW - OPEN WHAT & WHY (Có Input/Output rõ ràng - Cấm gợi ý Code)**:
   - Must specify explicit Input data format and Expected Output requirements.
   - ABSOLUTELY FORBIDDEN to provide code skeletons, algorithm execution steps, or code hints (e.g. forbid writing "Step 1: use for loop, Step 2: check condition with if/else"). Students must autonomously design the solution logic.

4. **Unified Enterprise Scenario Domain (Cùng Domain Doanh nghiệp của Session)**:
   - Must strictly maintain the exact same enterprise business scenario domain established for the Session (ShopeeFood, Student Management, E-commerce Checkout, Banking, Logistics WMS...).

5. **Standardized 4-Section Layout (Format Chuẩn 4 Phần)**:
   - **Section 1: Mục tiêu bài tập** (Objectives)
   - **Section 2: Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)** (Context, Input/Output definitions, and Input/Output Example Table)
   - **Section 3: Các bước thực hiện & Quy định kỹ thuật** (Environment, Technical Constraints - Closed How)
   - **Section 4: Checklist đánh giá kết quả (Nghiệm thu)** (Checkbox `[ ]` evaluation list)

6. **Strict Quality Rules & AI Marker Ban**:
   - ⛔ **Forbidden Cliché Words**: `"nhé"`, `"bẫy lập trình"`, `"thần thánh"`, `"bí kíp"`, `"tất tần tật"`, `"thân mến"`. Use formal technical terms: `"Lỗi thường gặp"`, `"Sai sót phổ biến"`, `"Ngoại lệ cần lưu ý"`.
   - ⛔ **Forbidden Text Emojis**: 100% forbidden to use text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶). Use standard clean Markdown typography only.
   - 100% Accented Vietnamese Output Contract.

---

## 1. OUTPUT FILE FORMAT STANDARD

The session in-class synthesis exercise MUST be formatted as a clean Markdown document. It is
generated as exercise #16 of the session's homework suite (see
`agents/creators/homework_creator.py::generate_inclass_synthesis_exercise`, invoked from
`generate_session_homework_suite`) and saved at
`Bài tập/16_tong_hop_demo_giang_vien_tren_lop/de_bai_bai_tap.md`, with its grading rubric at
`tieu_chi_cham_diem_ai.md` in the same folder:

```markdown
# Bài tập tổng hợp trên lớp: [Tên bài toán nghiệp vụ doanh nghiệp]

## 1. Mục tiêu bài tập
- Vận dụng tổng hợp toàn bộ kiến thức trong Session [Tên Session] để xây dựng giải pháp phần mềm.
- Triển khai chức năng nghiệp vụ [Mô tả tính năng chính] với dữ liệu đầu vào và đầu ra xác định.
- Rèn luyện kỹ năng tổ chức mã nguồn sạch (Clean Code), xử lý ngoại lệ và bắt lỗi dữ liệu đầu vào.

## 2. Mô tả bối cảnh & Yêu cầu bài toán (Input / Output)
- **Bối cảnh doanh nghiệp**: [Mô tả chi tiết 2-3 câu bối cảnh bài toán thực tế của doanh nghiệp...]
- **Dữ liệu đầu vào (Input)**: [Quy định rõ định dạng, kiểu dữ liệu và thông số đầu vào...]
- **Kết quả đầu ra (Output)**: [Quy định rõ kết quả in ra màn hình / console output hoặc cấu trúc dữ liệu trả về...]

### Bảng ví dụ minh họa Input/Output:
| Trường hợp (Case) | Dữ liệu đầu vào (Input) | Kết quả kỳ vọng (Expected Output) | Ghi chú nghiệp vụ |
| :--- | :--- | :--- | :--- |
| **Trường hợp 1 (Chuẩn)** | `[Input mẫu 1]` | `[Output mẫu 1]` | Xử lý luồng thành công. |
| **Trường hợp 2 (Ngoại lệ)** | `[Input mẫu 2]` | `[Output mẫu 2]` | Bắt lỗi và thông báo hợp lệ. |

## 3. Các bước thực hiện & Quy định kỹ thuật
- **Tài nguyên & Môi trường**: Thực thi trên môi trường `{tech_stack}`.
- **Yêu cầu kỹ thuật**:
  - Kết hợp sử dụng các cấu trúc điều khiển và cú pháp cốt lõi đã học trong Session.
  - Xử lý an toàn các trường hợp dữ liệu không hợp lệ hoặc biên.
  - Tuân thủ quy chuẩn đặt tên biến/hàm (`snake_case` / `camelCase`) và tổ chức mã nguồn rõ ràng.
  *(LƯU Ý: Học viên tự chủ động thiết kế giải thuật và cấu trúc chương trình. Không cung cấp mã nguồn gợi ý).*

## 4. Checklist đánh giá kết quả (Nghiệm thu)
- [ ] Xây dựng hoàn chỉnh chương trình đáp ứng đúng bối cảnh nghiệp vụ doanh nghiệp.
- [ ] Trả về kết quả Output chính xác theo đúng bảng ví dụ minh họa cho các trường hợp dữ liệu đầu vào.
- [ ] Bắt lỗi ngoại lệ và xử lý dữ liệu biên an toàn không gây crash chương trình.
- [ ] Mã nguồn đạt chuẩn Clean Code, đặt tên biến/hàm đúng quy chuẩn và có chú thích rõ ràng.
```

---

## 💻 2. CODE & SCENARIO ADAPTATION BY TECH STACK

| Tech Stack Category | In-Memory Storage & Flow Control | Input/Output Presentation | Technical Constraints |
| :--- | :--- | :--- | :--- |
| **Python Core** (`python/core`) | `for`, `while`, `range()`, `break`/`continue`, `list`/`dict` | Console I/O, `input()`, `print()` | `snake_case`, PEP 8, native exceptions (`ValueError`). **NO FastAPI / NO HTTP status.** |
| **C / C++** (`c/cpp`) | `for`, `while`, `do-while`, `struct`, array | Standard I/O `scanf`/`printf`, `cin`/`cout` | Memory safety, pointer bounds, ANSI C / C++11. |
| **Java Core** (`java/core`) | `for`, `while`, `ArrayList`, `Scanner` | System console I/O | Clean OOP, camelCase/PascalCase, Java Code Conventions. |
| **JavaScript** (`javascript/web`) | `for`, `while`, array methods, DOM/CLI | Console log / Prompt I/O | ES6 standards, camelCase, `const`/`let`. |
