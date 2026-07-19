---
name: lessons_learned
description: Kho tri thức đúc rút kinh nghiệm phòng chống lỗi kỹ thuật từ các Agent thế hệ trước.
---

# 🧠 Kho tri thức bài học kinh nghiệm (Lessons Learned)

Dưới đây là danh sách các quy tắc chặn lỗi được các Agent thế hệ trước đúc rút ra sau khi giải quyết các phản hồi lỗi từ Reviewer:

## 📌 Quy tắc kỹ thuật tích lũy
* **[PYTHON/FASTAPI]**: Khi xây dựng giao diện mô phỏng HTML/JS và câu hỏi trắc nghiệm, luôn đảm bảo ID của thẻ `<canvas>` là duy nhất để tránh lỗi `TypeError: getContext is not a function`, sử dụng class `active-line` thay vì inline style cho code tracker, và đối soát `correct_option_index` khớp chính xác với đáp án đúng trong dữ liệu JSON. | Trích từ bài [[Lesson 03 - Khởi tạo Ứng dụng FastAPI và Vận hành với Uvicorn]]
