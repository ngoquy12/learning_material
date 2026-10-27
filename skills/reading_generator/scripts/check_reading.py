"""Kiểm tra một bài đọc reading.html: chạy bộ kiểm tra có sẵn của dự án và thêm các kiểm tra mà nó chưa có.

  python skills/reading_generator/scripts/check_reading.py reading.html --tech-stack javascript
         [--course-name "NodeJS"] [--title "Tên bài"] [--orientation] [--no-budget]

Bộ kiểm tra của dự án (core/validators/reading_validator.py): id section-1..section-5, Mục 3 có mã và ít nhất
3 ví dụ, emoji, từ cấm, khối "Yêu cầu bài toán", giới hạn số từ 15 phút, tương thích Pyodide với môn Python.
Kiểm tra thêm ở đây: href="#", nút thiếu type, ảnh thiếu chú thích, lớp dark:, tiêu đề/nút viết hoa toàn bộ,
thẻ ngoặc vuông kiểu [NOTE].

Script KHÔNG chạy mã trong bài và không đánh giá chất lượng sư phạm: phải tự chạy mọi ví dụ và mở trang trên
trình duyệt. Mã thoát 1 nếu có LỖI.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List

HERE = Path(__file__).resolve().parent


def find_repo_root() -> Path:
    for parent in [HERE, *HERE.parents]:
        if (parent / "core" / "validators" / "reading_validator.py").exists():
            return parent
    raise SystemExit("Không tìm thấy core/validators/reading_validator.py: chạy script bên trong kho dự án.")


def extra_checks(html: str) -> tuple[List[str], List[str]]:
    from bs4 import BeautifulSoup

    errors: List[str] = []
    warnings: List[str] = []
    soup = BeautifulSoup(html, "html.parser")

    if re.search(r'href=["\']#["\']', html):
        errors.append('có thẻ <a href="#">')

    for btn in soup.find_all("button"):
        if not btn.get("type"):
            label = btn.get_text(strip=True)[:30] or btn.get("id", "")
            errors.append(f"nút thiếu type=\"button\": {label}")
            break

    for img in soup.find_all("img"):
        parent = img.find_parent("figure")
        has_caption = bool(parent and parent.find("figcaption"))
        if not has_caption:
            nxt = img.find_next_sibling()
            has_caption = bool(nxt and nxt.name in ("p", "i", "em", "figcaption"))
        if not has_caption:
            warnings.append(f"ảnh thiếu chú thích ngay bên dưới: {str(img.get('src', ''))[:50]}")

    dark = set()
    for tag in soup.find_all(class_=True):
        for cls in tag.get("class", []):
            if cls.startswith("dark:"):
                dark.add(cls)
    if dark:
        warnings.append(f"còn {len(dark)} lớp dark: (bài chỉ dùng nền sáng), ví dụ {sorted(dark)[0]}")

    for tag in soup.find_all(["h1", "h2", "h3", "button"]):
        text = tag.get_text(" ", strip=True)
        letters = re.sub(r"[^A-Za-zÀ-ỹ]", "", text)
        if len(letters) >= 10 and letters == letters.upper():
            errors.append(f"{tag.name} viết hoa toàn bộ: {text[:40]}")
            break

    body_text = soup.get_text(" ")
    if re.search(r"\[(NOTE|TIP|WARNING|CẢNH BÁO|LƯU Ý)\]", body_text):
        errors.append("có thẻ ngoặc vuông kiểu [NOTE]")

    # Chỉ xét văn bản ngoài khối mã: JSX như style={{ color: "red" }} là mã hợp lệ.
    prose = BeautifulSoup(html, "html.parser")
    for tag in prose.find_all(["pre", "code", "script", "style"]):
        tag.decompose()
    prose_text = prose.get_text(" ")
    if re.search(r"\{\{\s*[A-Za-z_][\w.]*\s*(\|[^}]*)?\}\}|\{clean_title\}|\[object Object\]", prose_text):
        errors.append("còn chỗ giữ chỗ hoặc giá trị chưa kết xuất ({{ tên }}, {clean_title}, [object Object])")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html")
    parser.add_argument("--tech-stack", required=True, help="Công nghệ của môn (javascript, python, sql, git...)")
    parser.add_argument("--course-name", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--orientation", action="store_true", help="Bài định hướng Session 01")
    parser.add_argument("--no-budget", action="store_true", help="Bỏ kiểm giới hạn số từ")
    args = parser.parse_args()

    root = find_repo_root()
    sys.path.insert(0, str(root))
    from core.validators.reading_validator import count_visible_words, validate_reading_material

    html = Path(args.html).read_text(encoding="utf-8")
    metadata = {
        "tech_stack": args.tech_stack,
        "course_name": args.course_name,
        "lesson_title": args.title or Path(args.html).parent.parent.name,
        "is_orientation": args.orientation,
        "enforce_word_budget": not args.no_budget,
    }
    ok, validator_errors = validate_reading_material(html, metadata)
    errors = list(validator_errors)
    warnings: List[str] = []

    words = count_visible_words(html)
    print(f"Số từ hiển thị: {words} (mục tiêu 1.500-2.000 cho 15 phút)")
    if not args.orientation and not 1500 <= words <= 2000:
        warnings.append(f"số từ {words} ngoài khoảng 1.500-2.000")

    e, w = extra_checks(html)
    errors += e
    warnings += w

    for msg in warnings:
        print("CẢNH BÁO", msg)
    for msg in errors:
        print("LỖI", msg)
        if "Section 2.4" in msg:
            print("     (biến thể mô phỏng ở cuối Mục 3 của môn ReactJS và NodeJS báo lỗi này: xem SKILL.md mục 3)")
    print(f"{len(errors)} lỗi, {len(warnings)} cảnh báo")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
