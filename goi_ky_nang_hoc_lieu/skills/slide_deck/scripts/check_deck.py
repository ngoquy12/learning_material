"""Kiểm tra bộ slide .pptx ĐÃ DỰNG: văn bản, cỡ chữ, hình học và, trên Windows có PowerPoint, đo chữ tràn thật.

  python skills/slide_deck/scripts/check_deck.py deck.pptx [--json slides.json] [--render] [--out thư_mục_ảnh]

Có --render: mở bằng PowerPoint (COM), đo chiều cao chữ thật của từng khung, xuất ảnh từng slide và ghép
`sheet_N.png` (6 slide mỗi ảnh) để XEM BẰNG MẮT. Không có PowerPoint thì chỉ ước lượng và in cảnh báo
rõ ràng: khi đó phải tự xuất ảnh bằng công cụ khác và xem trước khi giao.

Mã thoát 1 nếu có LỖI. Cảnh báo không làm thất bại nhưng phải đọc.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from deck_lint import BANNED, BRACKET_TAG, EMOJI, lint_slides, load_slides  # noqa: E402

EMU_PER_PT = 12700
MIN_FONT_ERROR_PT = 10
MIN_FONT_WARN_PT = 12
BOUNDS_TOLERANCE_EMU = 20000
FOOTER_ZONE = 0.90          # chữ nằm dưới 90% chiều cao slide là chạm vùng chân trang của template
ALLOWED_CAPS = {"NỘI DUNG"}  # nhãn viết hoa có sẵn trong template gốc


def static_checks(pptx_path: Path) -> Dict[str, Any]:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    from pptx.util import Pt

    prs = Presentation(str(pptx_path))
    sw, sh = prs.slide_width, prs.slide_height
    errors: List[str] = []
    warnings: List[str] = []
    estimates: List[str] = []

    for idx, slide in enumerate(prs.slides, 1):
        notes_ok = slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip()
        if not notes_ok:
            errors.append(f"slide {idx}: thiếu ghi chú giảng (notes)")
        for shape in slide.shapes:
            is_pic = shape.shape_type == MSO_SHAPE_TYPE.PICTURE
            is_ph = shape.is_placeholder
            if shape.left is not None and not is_pic and not is_ph:
                right, bottom = shape.left + shape.width, shape.top + shape.height
                over = max(-shape.left, -shape.top, right - sw, bottom - sh)
                if over > BOUNDS_TOLERANCE_EMU:
                    warnings.append(f"slide {idx}: '{shape.name}' vượt mép slide {over / 914400:.2f} inch")
            if not shape.has_text_frame:
                continue
            text = shape.text_frame.text
            if not text.strip():
                continue
            if EMOJI.search(text):
                errors.append(f"slide {idx}: '{shape.name}' có emoji")
            low = text.lower()
            for word in BANNED:
                if word in low:
                    errors.append(f"slide {idx}: '{shape.name}' có từ bị cấm '{word}'")
            if BRACKET_TAG.search(text):
                errors.append(f"slide {idx}: '{shape.name}' có thẻ ngoặc vuông")
            letters = re.sub(r"[^A-Za-zÀ-ỹ]", "", text)
            if len(letters) >= 10 and letters == letters.upper() and text.strip() not in ALLOWED_CAPS:
                errors.append(f"slide {idx}: '{shape.name}' viết hoa toàn bộ: {text.strip()[:30]}")
            min_pt = None
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.font.size and run.text.strip():
                        pt = run.font.size / EMU_PER_PT
                        min_pt = pt if min_pt is None else min(min_pt, pt)
            if min_pt is not None:
                if min_pt < MIN_FONT_ERROR_PT:
                    errors.append(f"slide {idx}: '{shape.name}' cỡ chữ {min_pt:.0f}pt, dưới {MIN_FONT_ERROR_PT}pt")
                elif min_pt < MIN_FONT_WARN_PT:
                    warnings.append(f"slide {idx}: '{shape.name}' cỡ chữ {min_pt:.0f}pt, nên từ {MIN_FONT_WARN_PT}pt")
            # Ước lượng chiều cao chữ (chỉ dùng khi không đo được bằng PowerPoint)
            if shape.width and shape.height and not is_ph:
                width_pt = (shape.width - 182850) / EMU_PER_PT
                height_pt = (shape.height - 91400) / EMU_PER_PT
                need = 0.0
                for para in shape.text_frame.paragraphs:
                    runs = [r for r in para.runs if r.text]
                    if not runs:
                        continue
                    size = max((r.font.size / EMU_PER_PT for r in runs if r.font.size), default=14.0)
                    mono = any((r.font.name or "").lower().startswith(("consolas", "courier")) for r in runs)
                    cpl = max(1, int(width_pt / (size * (0.60 if mono else 0.52))))
                    chars = sum(len(r.text) for r in runs)
                    lines = max(1, math.ceil(chars / cpl))
                    spacing = para.line_spacing if isinstance(para.line_spacing, float) else 1.2
                    need += lines * size * spacing
                if need > height_pt * 1.10 and height_pt > 20:
                    estimates.append(f"slide {idx}: '{shape.name}' có thể tràn (cần ~{need:.0f}pt, khung {height_pt:.0f}pt)")
    return {"slides": len(prs.slides), "errors": errors, "warnings": warnings, "estimates": estimates,
            "width": sw, "height": sh}


PS_PROBE = r"""
param([string]$Pptx, [string]$OutDir, [string]$OutJson)
$ErrorActionPreference = "Stop"
$ppt = New-Object -ComObject PowerPoint.Application
try {
  $pres = $ppt.Presentations.Open($Pptx, $true, $false, $false)
  $sw = $pres.PageSetup.SlideWidth; $sh = $pres.PageSetup.SlideHeight
  $rows = @()
  foreach ($s in $pres.Slides) {
    foreach ($shape in $s.Shapes) {
      if ($shape.HasTable) {
        $rows += [pscustomobject]@{ slide=$s.SlideIndex; name=$shape.Name; kind="table"; rot=0; top=$shape.Top; height=$shape.Height; left=$shape.Left; width=$shape.Width; bh=0; bw=0; bl=0; bt=0; mt=0; mb=0 }
      } elseif ($shape.HasTextFrame -and $shape.TextFrame.HasText) {
        $tr = $shape.TextFrame.TextRange
        $rows += [pscustomobject]@{ slide=$s.SlideIndex; name=$shape.Name; kind="text"; rot=$shape.Rotation; top=$shape.Top; height=$shape.Height; left=$shape.Left; width=$shape.Width; bh=$tr.BoundHeight; bw=$tr.BoundWidth; bl=$tr.BoundLeft; bt=$tr.BoundTop; mt=$shape.TextFrame.MarginTop; mb=$shape.TextFrame.MarginBottom }
      }
    }
  }
  $pres.Export($OutDir, "PNG", 1280, 720)
  $pres.Close()
  $obj = [pscustomobject]@{ width=$sw; height=$sh; shapes=$rows }
  $json = $obj | ConvertTo-Json -Depth 4 -Compress
  [System.IO.File]::WriteAllText($OutJson, $json, (New-Object System.Text.UTF8Encoding($false)))
} finally { $ppt.Quit() }
"""


def render_with_powerpoint(pptx_path: Path, out_dir: Path) -> Dict[str, Any]:
    if sys.platform != "win32":
        return {"status": "SKIPPED", "reason": "không phải Windows"}
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("Slide*.PNG"):
        old.unlink()
    work = Path(tempfile.mkdtemp(prefix="deck_check_"))
    try:
        copy = work / "copy.pptx"
        shutil.copy(pptx_path, copy)
        ps1 = work / "probe.ps1"
        ps1.write_text(PS_PROBE, encoding="utf-8")
        out_json = work / "probe.json"
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1),
             "-Pptx", str(copy), "-OutDir", str(out_dir.resolve()), "-OutJson", str(out_json)],
            capture_output=True, text=True, timeout=300)
        if proc.returncode != 0 or not out_json.exists():
            return {"status": "FAILED", "reason": (proc.stderr or proc.stdout)[-400:]}
        data = json.loads(out_json.read_text(encoding="utf-8"))
        shapes = data["shapes"]
        if isinstance(shapes, dict):
            shapes = [shapes]
        return {"status": "OK", "width": data["width"], "height": data["height"], "shapes": shapes}
    except Exception as exc:  # noqa: BLE001
        return {"status": "FAILED", "reason": str(exc)}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def measured_checks(probe: Dict[str, Any]) -> Dict[str, List[str]]:
    """Lỗi = thứ nhìn thấy được: chữ chồng chữ, chữ chạm chân trang, chữ tràn khung nhiều.
    Chữ lệch vài point so với khung mà không chạm gì khác không phải lỗi."""
    errors, warnings = [], []
    sw, sh = probe["width"], probe["height"]
    by_slide: Dict[int, List[Dict[str, Any]]] = {}
    for s in probe["shapes"]:
        by_slide.setdefault(s["slide"], []).append(s)

    for slide, shapes in by_slide.items():
        rects = []
        for s in shapes:
            name = s["name"]
            if s["kind"] == "table":
                bottom = s["top"] + s["height"]
                if bottom > sh * FOOTER_ZONE:
                    errors.append(f"slide {slide}: bảng '{name}' kéo xuống {bottom / sh:.0%} chiều cao, chạm chân trang")
                rects.append((name, s["left"], s["top"], s["left"] + s["width"], bottom))
                continue
            if abs(s.get("rot", 0)) > 1:      # chữ xoay: PowerPoint không cho số đo đáng tin
                continue
            avail = s["height"] - s["mt"] - s["mb"]
            over = s["bh"] - avail
            if over > 8 and s["bh"] > avail * 1.15:
                warnings.append(f"slide {slide}: chữ '{name}' vượt khung {over:.0f}pt (cần {s['bh']:.0f}pt, khung {avail:.0f}pt)")
            if over > 30 and s["bh"] > avail * 1.5:
                errors.append(f"slide {slide}: chữ '{name}' tràn khung nhiều ({s['bh']:.0f}pt so với {avail:.0f}pt)")
            bottom = s["bt"] + s["bh"]
            if bottom > sh * FOOTER_ZONE and not name.startswith("Closing"):
                errors.append(f"slide {slide}: chữ '{name}' xuống {bottom / sh:.0%} chiều cao, chạm chân trang")
            if s["bl"] + s["bw"] > sw - 10:
                warnings.append(f"slide {slide}: chữ '{name}' sát hoặc vượt mép phải")
            rects.append((name, s["bl"], s["bt"], s["bl"] + s["bw"], bottom))
        # chữ chồng chữ
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                a, b = rects[i], rects[j]
                ix = min(a[3], b[3]) - max(a[1], b[1])
                iy = min(a[4], b[4]) - max(a[2], b[2])
                if ix > 4 and iy > 4:
                    errors.append(f"slide {slide}: '{a[0]}' chồng lên '{b[0]}' ({ix:.0f}x{iy:.0f}pt)")
    return {"errors": errors, "warnings": warnings}


def contact_sheets(out_dir: Path, per_sheet: int = 6) -> List[Path]:
    from PIL import Image
    files = sorted(out_dir.glob("Slide*.PNG"), key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))
    sheets: List[Path] = []
    for k in range(0, len(files), per_sheet):
        group = files[k:k + per_sheet]
        rows = (len(group) + 1) // 2
        sheet = Image.new("RGB", (1600, 450 * rows), "white")
        for j, f in enumerate(group):
            sheet.paste(Image.open(f).convert("RGB").resize((800, 450)), ((j % 2) * 800, (j // 2) * 450))
        path = out_dir / f"sheet_{k // per_sheet + 1}.png"
        sheet.save(path)
        sheets.append(path)
    return sheets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pptx")
    parser.add_argument("--json", default=None, help="slides.json để kiểm lại cấu trúc")
    parser.add_argument("--render", action="store_true", help="Đo chữ tràn thật và xuất ảnh bằng PowerPoint")
    parser.add_argument("--out", default=None, help="Thư mục ảnh (mặc định: <tên_tệp>_ảnh cạnh tệp pptx)")
    args = parser.parse_args()

    pptx = Path(args.pptx)
    errors: List[str] = []
    warnings: List[str] = []

    if args.json:
        e, w = lint_slides(load_slides(Path(args.json)))
        errors += [f"[json] {x}" for x in e]
        warnings += [f"[json] {x}" for x in w]

    res = static_checks(pptx)
    errors += res["errors"]
    warnings += res["warnings"]
    print(f"Đã đọc {res['slides']} slide.")

    sheets: List[Path] = []
    if args.render:
        out_dir = Path(args.out) if args.out else pptx.with_name(pptx.stem + "_anh")
        probe = render_with_powerpoint(pptx, out_dir)
        if probe["status"] == "OK":
            m = measured_checks(probe)
            errors += m["errors"]
            warnings += m["warnings"]
            sheets = contact_sheets(out_dir)
        else:
            warnings.append(f"KHÔNG đo và xuất ảnh được ({probe['status']}: {probe.get('reason', '')}). "
                            "Phải tự xuất ảnh bằng công cụ khác và xem từng slide trước khi giao.")
            warnings += [f"[ước lượng] {x}" for x in res["estimates"]]
    else:
        warnings.append("Chưa chạy --render: chưa đo chữ tràn thật và chưa có ảnh để xem.")
        warnings += [f"[ước lượng] {x}" for x in res["estimates"]]

    for w in warnings:
        print("CẢNH BÁO", w)
    for e in errors:
        print("LỖI", e)
    for s in sheets:
        print("ẢNH", s)
    print(f"{len(errors)} lỗi, {len(warnings)} cảnh báo")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
