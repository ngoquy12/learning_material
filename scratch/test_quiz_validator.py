# scratch/test_quiz_validator.py
import sys
import json
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base_dir = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material")
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from core.validators.quiz_validator import validate_quiz_json, validate_reading_questions_md

def run_audit():
    print("==========================================================")
    print("Audit Inspection of Session 04 Assessment Resources")
    print("==========================================================")
    
    # 1. Lesson 01 Reading Questions
    l1_rq_path = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 01 - Toán tử số học và toán tử gán\Câu hỏi bài đọc\reading_questions.md"
    if l1_rq_path.exists():
        content = l1_rq_path.read_text(encoding="utf-8")
        is_val, errs = validate_reading_questions_md(content)
        print(f"\n--- [Audit] Lesson 01 reading_questions.md ---")
        if is_val:
            print("  ✅ PASS!")
        else:
            print(f"  ❌ FAIL ({len(errs)} errors):")
            for e in errs:
                print(f"     - {e}")

    # 2. Lesson 02 Reading Questions
    l2_rq_path = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 02 - Toán tử so sánh và toán tử logic\Câu hỏi bài đọc\reading_questions.md"
    if l2_rq_path.exists():
        content = l2_rq_path.read_text(encoding="utf-8")
        is_val, errs = validate_reading_questions_md(content)
        print(f"\n--- [Audit] Lesson 02 reading_questions.md ---")
        if is_val:
            print("  ✅ PASS!")
        else:
            print(f"  ❌ FAIL ({len(errs)} errors):")
            for e in errs:
                print(f"     - {e}")

    # 4. Lesson 03 Reading Questions & Quiz
    l3_rq_path = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 03 - Cấu trúc rẽ nhánh điều khiển với if, elif và else\Câu hỏi bài đọc\reading_questions.md"
    l3_q_path = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 03 - Cấu trúc rẽ nhánh điều khiển với if, elif và else\Câu hỏi Quizz\quiz.json"
    if l3_rq_path.exists():
        is_val, errs = validate_reading_questions_md(l3_rq_path.read_text(encoding="utf-8"))
        print(f"\n--- [Audit] Lesson 03 reading_questions.md ---")
        print("  ✅ PASS!" if is_val else f"  ❌ FAIL ({len(errs)} errors):\n" + "\n".join(f"     - {e}" for e in errs))
    if l3_q_path.exists():
        is_val, errs = validate_quiz_json(json.loads(l3_q_path.read_text(encoding="utf-8")))
        print(f"\n--- [Audit] Lesson 03 quiz.json ---")
        print("  ✅ PASS!" if is_val else f"  ❌ FAIL ({len(errs)} errors):\n" + "\n".join(f"     - {e}" for e in errs))

    # 5. Lesson 04 Reading Questions & Quiz
    l4_rq_path = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 04 - Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8\Câu hỏi bài đọc\reading_questions.md"
    l4_q_path = base_dir / r"output\pms\Lập_trình_Python\Session 04 - Toán tử số học, logic và Cấu trúc rẽ nhánh\Lesson 04 - Cấu trúc rẽ nhánh lồng nhau và Chuẩn hóa mã nguồn PEP 8\Câu hỏi Quizz\quiz.json"
    if l4_rq_path.exists():
        is_val, errs = validate_reading_questions_md(l4_rq_path.read_text(encoding="utf-8"))
        print(f"\n--- [Audit] Lesson 04 reading_questions.md ---")
        print("  ✅ PASS!" if is_val else f"  ❌ FAIL ({len(errs)} errors):\n" + "\n".join(f"     - {e}" for e in errs))
    if l4_q_path.exists():
        is_val, errs = validate_quiz_json(json.loads(l4_q_path.read_text(encoding="utf-8")))
        print(f"\n--- [Audit] Lesson 04 quiz.json ---")
        print("  ✅ PASS!" if is_val else f"  ❌ FAIL ({len(errs)} errors):\n" + "\n".join(f"     - {e}" for e in errs))

if __name__ == "__main__":
    run_audit()
