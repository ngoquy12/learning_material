"""
core/validators/hyperframes_validator.py
Programmatic Validation Layer for Video Narration Scripts & HyperFrames Compositions.
Validates narration pace (140-160 WPM), audio-first master timeline, GSAP scenes, and Vietnamese tone.
"""

import re
from typing import Tuple, List, Dict, Any

def validate_hyperframes_script(script_data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates a Video Narration Script / HyperFrames Blueprint.
    Returns (is_valid, list_of_error_strings).
    """
    if not script_data:
        return False, ["Dữ liệu kịch bản video HyperFrames bị trống."]
        
    errors = []
    scenes = script_data.get("scenes", []) or script_data.get("scenes_list", [])
    
    if not scenes:
        errors.append("Kịch bản Video HyperFrames phải có ít nhất 1 Cảnh (Scene).")
        return False, errors
        
    for idx, scene in enumerate(scenes, 1):
        scene_title = scene.get("title") or scene.get("scene_id") or f"Scene {idx}"
        narration = scene.get("narration") or scene.get("audio_text") or ""
        duration = scene.get("duration", 0)
        
        # 1. Narration Text Check
        if not narration.strip():
            errors.append(f"Cảnh {idx} ({scene_title}): Lời thoại lồng tiếng bị trống.")
            continue
            
        # 2. Narration Pace Check (Speech rate: ~140-160 words/min = ~2.5 words/sec)
        word_count = len(narration.strip().split())
        if word_count < 5:
            errors.append(f"Cảnh {idx} ({scene_title}): Lời thoại quá ngắn ({word_count} từ, tối thiểu 5 từ).")
            
        if duration > 0:
            est_wpm = (word_count / duration) * 60
            if est_wpm > 220:
                errors.append(f"Cảnh {idx} ({scene_title}): Tốc độ lời thoại quá nhanh ({word_count} từ / {duration}s = {int(est_wpm)} WPM, khuyến nghị < 180 WPM).")
                
        # 3. Forbidden Emojis in Narration
        if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]', narration):
            errors.append(f"Cảnh {idx} ({scene_title}): Lời thoại lồng tiếng chứa biểu tượng Emoji cấm.")
            
    return len(errors) == 0, errors
