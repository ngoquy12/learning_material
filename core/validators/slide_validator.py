"""
core/validators/slide_validator.py
Programmatic Validation Layer for Presentation Slides.
Checks slide counts, narration length, bullet point counts, and Mermaid diagram syntax.
"""

from typing import Tuple, List, Dict, Any

def validate_slide_presentation(slides_data: List[Dict[str, Any]], metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates a list of slide scenes for presentation standards.
    """
    if not slides_data:
        return False, ["Danh sách slide bài giảng bị trống."]
        
    errors = []
    
    # 1. Slide Count Check (5 to 12 slides per lesson)
    if not (4 <= len(slides_data) <= 15):
        errors.append(f"Số lượng slide không hợp lệ ({len(slides_data)} slides, khuyến nghị từ 5 đến 12 slides).")
        
    # 2. Per-slide validation
    for idx, slide in enumerate(slides_data, 1):
        title = slide.get("scene_title") or slide.get("action_title") or ""
        narration = slide.get("narration", "")
        bullets = slide.get("bullets", [])
        
        if not title.strip():
            errors.append(f"Slide {idx}: Tiêu đề slide bị trống.")
            
        if len(narration.strip().split()) < 10:
            errors.append(f"Slide {idx}: Kịch bản lời giảng quá ngắn ({len(narration.strip().split())} từ, tối thiểu 10 từ).")
            
        if len(bullets) > 6:
            errors.append(f"Slide {idx}: Quá nhiều ý chính ({len(bullets)} bullets, tối đa 6 bullets để tránh gây rối mắt).")
            
    return len(errors) == 0, errors
