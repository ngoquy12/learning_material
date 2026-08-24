"""
scripts/run_pedagogical_eval.py — Chạy bộ chấm chất lượng sư phạm và ghi xu hướng (G3).

Dùng chính các bản golden trong tests/golden/expected/ làm đối tượng chấm. Lựa chọn
này có chủ đích:

  - Chúng đã được commit và TẤT ĐỊNH, nên điểm số chỉ đổi khi mã nguồn đổi, không
    phải vì LLM hôm nay trả lời khác hôm qua. Chấm trên nội dung sinh mới mỗi lần
    thì không phân biệt được "code tệ đi" với "LLM hôm nay kém may".
  - Chúng đi qua đúng đường render thật, nên phản ánh đúng học liệu người học nhận.
  - Chúng phủ đủ bốn nhóm công nghệ, nên tụt điểm ở riêng một nhóm sẽ hiện ra.

Chạy:
    python scripts/run_pedagogical_eval.py              # chấm và ghi xu hướng
    python scripts/run_pedagogical_eval.py --check      # đỏ (exit 1) nếu tụt điểm
    python scripts/run_pedagogical_eval.py --no-record  # chỉ chấm, không ghi
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

GOLDEN_DIR = BASE_DIR / "tests" / "golden"


def _load_subjects():
    """Các bài đọc golden kèm metadata, bỏ qua bài thực hành (bộ chấm dành cho bài đọc)."""
    subjects = []
    fixtures_dir = GOLDEN_DIR / "fixtures"
    expected_dir = GOLDEN_DIR / "expected"

    for fixture_path in sorted(fixtures_dir.glob("*.json")):
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        if fixture.get("renderer") != "reading":
            continue

        html_path = expected_dir / f"{fixture_path.stem}.html"
        if not html_path.exists():
            print(f"  [Bỏ qua] Chưa có bản golden cho {fixture_path.stem}")
            continue

        metadata = fixture.get("metadata", {})
        subjects.append(
            {
                "name": fixture_path.stem,
                "html": html_path.read_text(encoding="utf-8"),
                "tech_stack": metadata.get("tech_stack", ""),
                "lesson_title": metadata.get("lesson_title", fixture_path.stem),
            }
        )
    return subjects


def main() -> int:
    parser = argparse.ArgumentParser(description="Chấm chất lượng sư phạm và theo dõi xu hướng")
    parser.add_argument("--check", action="store_true",
                        help="Trả mã lỗi khi phát hiện tụt điểm so với lần chấm trước")
    parser.add_argument("--no-record", action="store_true",
                        help="Chỉ chấm và in kết quả, không ghi vào kho xu hướng")
    parser.add_argument("--min-score", type=float, default=0.0,
                        help="Ngưỡng điểm tối thiểu; dưới ngưỡng thì trả mã lỗi")
    args = parser.parse_args()

    from core.evals.benchmark import evaluate_lesson_pedagogy
    from core.evals.trend_store import (
        detect_regressions,
        format_trend_report,
        record_scorecard,
    )

    subjects = _load_subjects()
    if not subjects:
        print("Không tìm thấy bản golden nào để chấm. Sinh trước bằng:")
        print("    UPDATE_GOLDEN=1 python -m pytest tests/test_golden_design.py")
        return 1

    print(f"Đang chấm {len(subjects)} bài đọc golden...\n")

    names = []
    below_threshold = []
    for subject in subjects:
        scorecard = evaluate_lesson_pedagogy(
            html_content=subject["html"],
            lesson_id=subject["name"],
            lesson_title=subject["lesson_title"],
            tech_stack=subject["tech_stack"],
        )
        verdict = "ĐẠT" if scorecard.passed else "CHƯA ĐẠT"
        print(f"  {subject['name'][:38]:<38} {scorecard.overall_score:5.1f}  {verdict}")

        if args.min_score and scorecard.overall_score < args.min_score:
            below_threshold.append((subject["name"], scorecard.overall_score))

        if not args.no_record:
            record_scorecard(scorecard, subject=subject["name"])
        names.append(subject["name"])

    if not args.no_record:
        print(format_trend_report(names))

    exit_code = 0

    if below_threshold:
        print("Dưới ngưỡng điểm tối thiểu:")
        for name, score in below_threshold:
            print(f"  - {name}: {score:.1f} < {args.min_score}")
        exit_code = 1

    if args.check and not args.no_record:
        regressions = detect_regressions(names)
        if regressions:
            print("PHÁT HIỆN TỤT ĐIỂM CHẤT LƯỢNG:")
            for r in regressions:
                print(f"  - {r.message()}")
            exit_code = 1
        else:
            print("Không có tụt điểm so với lần chấm trước.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
