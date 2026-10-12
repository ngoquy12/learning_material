"""
core/reading_budget.py - Nguồn sự thật duy nhất cho thời lượng bài đọc của sinh viên.

15 phút là GIỚI HẠN CỨNG, quy đổi thành 1.500-2.000 từ (kể cả mã nguồn và khối mô
phỏng tương tác). Mọi prompt, validator, phân tích học tập và tài liệu phải lấy số từ
đây thay vì tự ghi số riêng, để các nơi không lệch nhau.
"""

READING_TARGET_MINUTES: int = 15
READING_WORD_BUDGET: tuple = (1500, 2000)

READING_WORD_MIN: int = READING_WORD_BUDGET[0]
READING_WORD_MAX: int = READING_WORD_BUDGET[1]
