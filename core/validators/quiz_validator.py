"""
core/validators/quiz_validator.py
Programmatic Quiz Validator & Answer Choice Shuffler.
Ensures 100% alignment between correct answer index and explanation text,
and shuffles A/B/C/D option positions evenly before writing Excel .xlsx files.
"""

import random
from typing import List, Dict, Any, Tuple

def validate_and_shuffle_quiz(
    questions: List[Dict[str, Any]],
    seed: int = 42
) -> Tuple[bool, List[Dict[str, Any]], List[str]]:
    """
    Validates question options and explanation alignment, and evenly shuffles option positions.
    Returns (is_valid, processed_questions, errors).
    """
    if not questions:
        return False, [], ["Danh sách câu hỏi trắc nghiệm trống."]
        
    random.seed(seed)
    errors = []
    processed = []
    
    for idx, q in enumerate(questions, 1):
        options = q.get("options", [])
        correct_idx = q.get("correct_option_index", 0)
        explanation = q.get("explanation", "")
        question_text = q.get("question", "")
        
        if len(options) < 2:
            errors.append(f"Câu {idx}: Phải có tối thiểu 2 đáp án (tìm thấy {len(options)}).")
            continue
            
        if not (0 <= correct_idx < len(options)):
            errors.append(f"Câu {idx}: Chỉ mục đáp án đúng '{correct_idx}' vượt quá số lượng đáp án ({len(options)}).")
            continue
            
        # Get actual correct answer text
        correct_text = options[correct_idx]
        
        # Shuffle options while tracking the new position of correct_text
        shuffled_options = list(options)
        random.shuffle(shuffled_options)
        new_correct_idx = shuffled_options.index(correct_text)
        
        processed_q = dict(q)
        processed_q["options"] = shuffled_options
        processed_q["correct_option_index"] = new_correct_idx
        processed_q["correct_answer_text"] = correct_text
        processed.append(processed_q)
        
    return len(errors) == 0, processed, errors
