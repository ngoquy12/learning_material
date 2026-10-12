"""
scripts/check_exercise_scope.py - Kiểm tra bài tập/lab của một môn trước khi giao.

Hai kiểm tra (xem core/validators/code_scope_linter.py):
  1. Mã starter/đáp án mẫu có dùng cấu trúc ngôn ngữ mà môn CHƯA dạy hay không.
  2. Hàm trùng tên giữa các bài (mã nền dùng lại) có bị lệch chữ ký hay không.

Ví dụ:
  python scripts/check_exercise_scope.py "output/pms/js_advanced_ai_driven" --forbid class,this,module,closure
  python scripts/check_exercise_scope.py <thư mục môn> --forbid class,closure --language javascript --no-drift

Mã thoát 1 nếu có vi phạm (dùng được trong CI hoặc làm bước cuối của quy trình sinh học liệu).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.validators.code_scope_linter import (  # noqa: E402
    find_scope_violations,
    find_signature_drift,
    mask_lines,
    mask_lines_matching,
    provided_code_lines,
)

EXT = {"javascript": ".js", "python": ".py"}
# Tệp hạ tầng chấm điểm / thư viện bên thứ ba: không phải mã của sinh viên.
SKIP_NAMES = {"harness.js", "mock-api.js", "axios.min.js", "tests.js", "demo.js"}


def collect_exercise_files(root: Path, language: str) -> List[Path]:
    ext = EXT.get(language, ".js")
    files = []
    for path in sorted(root.rglob(f"script{ext}")):
        if path.name in SKIP_NAMES:
            continue
        files.append(path)
    return files


def starter_for(path: Path, files: List[Path]) -> Path | None:
    """Với đáp án mẫu `.../dap_an_mau/bai_N/script.js`, tìm starter của bài N cùng buổi."""
    parts = path.parts
    if "dap_an_mau" not in parts:
        return None
    folder = parts[parts.index("dap_an_mau") + 1]
    if not folder.startswith("bai_"):
        return None
    n = folder[len("bai_"):]
    bai_tap = path
    while bai_tap.name != "Bai tap" and bai_tap.parent != bai_tap:
        bai_tap = bai_tap.parent
    for f in files:
        if "starter" in f.parts and f.parent.parent.name.startswith(f"{n}_") and bai_tap in f.parents:
            return f
    return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", help="Thư mục môn học (chứa các bài tập có script.js / script.py).")
    parser.add_argument("--forbid", default="", help="Cấu trúc chưa dạy, cách nhau dấu phẩy: class,this,module,closure (JS); class,global,lambda,comprehension,decorator,closure (Python).")
    parser.add_argument("--language", default="javascript", choices=sorted(EXT))
    parser.add_argument("--no-drift", action="store_true", help="Bỏ kiểm tra lệch chữ ký hàm dùng chung.")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"Không tìm thấy thư mục: {root}")
        return 2

    forbidden = [f.strip() for f in args.forbid.split(",") if f.strip()]
    files = collect_exercise_files(root, args.language)
    if not files:
        print("Không tìm thấy tệp script nào để kiểm tra.")
        return 2

    problems = 0
    contents: Dict[str, str] = {}
    for path in files:
        code = path.read_text(encoding="utf-8", errors="replace")
        contents[str(path.relative_to(root))] = code
        if forbidden:
            # Mã nền sinh viên không viết nên không tính: dùng dấu "Mã nền ... HẾT MÃ NỀN" của
            # chính tệp, hoặc (với đáp án mẫu) các dòng trùng với khối mã nền của starter tương ứng.
            scan_code = mask_lines(code, provided_code_lines(code))
            ref = starter_for(path, files)
            if ref is not None:
                scan_code = mask_lines_matching(scan_code, ref.read_text(encoding="utf-8", errors="replace"))
            for finding in find_scope_violations(scan_code, args.language, forbidden):
                problems += 1
                print(f"[PHẠM VI] {path.relative_to(root)}: {finding}")

    if not args.no_drift:
        # So sánh trong cùng nhóm "đáp án mẫu" (bài này dùng lại mã nền của bài kia); starter có
        # TODO nên chữ ký có thể khác thân hàm nhưng không được khác tham số.
        # Chỉ so trong cùng một buổi: mã nền của buổi khác được viết lại có chủ đích.
        by_session: Dict[str, Dict[str, str]] = {}
        for rel, code in contents.items():
            by_session.setdefault(Path(rel).parts[0], {})[rel] = code
        for session, group in by_session.items():
            for drift in find_signature_drift(group, args.language):
                problems += 1
                print(f"[LỆCH CHỮ KÝ] ({session}) {drift}")

    print(f"\nĐã quét {len(files)} tệp, {problems} vấn đề.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
