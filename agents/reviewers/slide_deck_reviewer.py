"""
agents/reviewers/slide_deck_reviewer.py
SlideDeckReviewerAgent: Audits and validates generated PowerPoint (.pptx) Slide Decks
and Markdown outline according to Create_Slide's 3-skill instructional quality standard.
"""

from __future__ import annotations
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from core.renderers.pptx.slide_validator import validate_pptx_file, export_slide_images

class SlideDeckReviewerAgent:
    """
    Reviewer agent for validating Session Slide Decks (.pptx) and Outline.
    """

    def review_slide_deck(
        self,
        slide_deck_dir: Union[str, Path],
        session_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Audits the Slide bài giảng directory for files integrity, design tokens, and PPTX validity.
        """
        dir_path = Path(slide_deck_dir)
        if not dir_path.exists() or not dir_path.is_dir():
            return {
                "status": "REJECTED",
                "score": 0,
                "feedback": f"Thư mục Slide bài giảng không tồn tại: {slide_deck_dir}",
                "errors": [f"Thư mục không tồn tại: {slide_deck_dir}"],
                "warnings": []
            }

        errors = []
        warnings = []

        # 1. Check outline_bai_giang.md
        outline_file = dir_path / "outline_bai_giang.md"
        if not outline_file.exists():
            errors.append("Thiếu file đề cương bài giảng: outline_bai_giang.md")
        elif outline_file.stat().st_size < 300:
            errors.append("File outline_bai_giang.md quá ngắn hoặc rỗng")

        # 2. Check Slide_Bai_Giang_*.pptx
        pptx_files = list(dir_path.glob("*.pptx"))
        if not pptx_files:
            errors.append("Không tìm thấy file trình chiếu PowerPoint (.pptx) trong thư mục Slide bài giảng")
            target_pptx = None
        else:
            target_pptx = pptx_files[0]
            if target_pptx.stat().st_size < 10000:
                errors.append(f"File PPTX {target_pptx.name} có dung lượng bất thường (<10KB)")

        # 3. Run Quantitative OOXML Validator if PPTX exists
        val_res = {"passed": True, "errors": [], "warnings": [], "total_slides": 0}
        if target_pptx and target_pptx.exists():
            val_res = validate_pptx_file(target_pptx)
            if not val_res.get("passed", True):
                errors.extend(val_res.get("errors", []))
            warnings.extend(val_res.get("warnings", []))

        # 4. Export each slide to PNG for visual QA (overflow/overlap/wrong-illustration
        #    checks that the regex validator above cannot catch — see Skill 3 Giai đoạn 3).
        image_paths: List[str] = []
        if target_pptx and target_pptx.exists():
            images_dir = dir_path / "slide_images"
            export_res = export_slide_images(target_pptx, images_dir)
            image_paths = export_res.get("images", [])
            if export_res.get("status") == "SUCCESS":
                warnings.append(
                    f"Đã xuất {len(image_paths)} ảnh slide vào {images_dir} — cần soi mắt (hoặc LLM vision) "
                    f"để bắt lỗi overflow/chồng lấn/sai minh họa mà validator không đo được."
                )
            elif export_res.get("status") == "SKIPPED":
                warnings.append(f"Bỏ qua bước xuất ảnh QA: {export_res.get('reason')}")
            else:
                warnings.append(f"Xuất ảnh slide QA thất bại: {export_res.get('reason')}")

        is_passed = len(errors) == 0
        score = 100 if is_passed else max(0, 100 - len(errors) * 20)

        return {
            "status": "PASSED" if is_passed else "REJECTED",
            "score": score,
            "total_slides": val_res.get("total_slides", 0),
            "errors": errors,
            "warnings": warnings,
            "slide_images": image_paths,
            "feedback": "Slide bài giảng PowerPoint đạt chuẩn chất lượng 100% Rikkei Education." if is_passed else f"Cần điều chỉnh các lỗi: {', '.join(errors)}"
        }

slide_deck_reviewer = SlideDeckReviewerAgent()

def review_session_slide_deck(
    slide_deck_dir: Union[str, Path],
    session_title: Optional[str] = None
) -> Dict[str, Any]:
    """Functional entrypoint for reviewing session slide deck."""
    return slide_deck_reviewer.review_slide_deck(
        slide_deck_dir=slide_deck_dir,
        session_title=session_title
    )
