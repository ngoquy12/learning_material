"""Dựng slide.pptx từ dữ liệu JSON bằng bộ dựng của dự án (core/renderers/pptx/deck_engine.py).

  python skills/slide_deck/scripts/build_deck.py slides.json "<đầu ra>/slide.pptx" [--template mau.pptx]

Bước 1: kiểm dữ liệu bằng deck_lint (dừng nếu có lỗi). Bước 2: dựng. Không sửa XML tay, không dùng python-pptx
để tạo slide: toàn bộ màu, font, bố cục lấy từ template qua bộ dựng.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from deck_lint import lint_slides, load_slides  # noqa: E402


def find_repo_root() -> Path:
    for parent in [HERE, *HERE.parents]:
        if (parent / "core" / "renderers" / "pptx" / "deck_engine.py").exists():
            return parent
    raise SystemExit("Không tìm thấy core/renderers/pptx/deck_engine.py: chạy script bên trong kho dự án.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slides_json")
    parser.add_argument("output_pptx")
    parser.add_argument("--template", default=None, help="Mặc định: templates/pptx/SLIDE TEMPLATE.pptx")
    parser.add_argument("--no-lint", action="store_true", help="Bỏ qua kiểm dữ liệu (không khuyến nghị)")
    args = parser.parse_args()

    slides = load_slides(Path(args.slides_json))
    if not args.no_lint:
        errors, warnings = lint_slides(slides)
        for w in warnings:
            print("CẢNH BÁO", w)
        for e in errors:
            print("LỖI", e)
        if errors:
            print(f"Dừng: {len(errors)} lỗi dữ liệu. Sửa slides.json rồi chạy lại.")
            return 1

    root = find_repo_root()
    sys.path.insert(0, str(root))
    from core.renderers.pptx.deck_engine import build_deck  # noqa: E402

    out = build_deck(slides, args.output_pptx, args.template)
    print(f"Đã dựng {len(slides)} slide: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
