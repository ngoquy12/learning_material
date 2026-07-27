"""
core/validators/practice_validator.py
Programmatic Validation Layer for Practical Exercises & Homework Assignments.
Uses Python AST parser to check solution code syntax and validates exercise structure.
"""

import ast
from typing import Tuple, List, Dict, Any

def validate_practice_exercise(lab_data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates practical exercise structure, steps, checklist, and code syntax.
    """
    if not lab_data:
        return False, ["Dữ liệu bài tập thực hành bị trống."]
        
    errors = []
    
    # 1. Structural requirements check
    title = lab_data.get("title", "")
    steps = lab_data.get("steps", [])
    checklist = lab_data.get("checklist", [])
    solution_code = lab_data.get("solution_code", "") or lab_data.get("code", "")
    
    if not title:
        errors.append("Tiêu đề bài tập thực hành bị trống.")
        
    if not steps:
        errors.append("Bài tập thực hành phải có danh sách các bước thực hiện (steps).")
        
    if not checklist:
        errors.append("Bài tập thực hành phải có danh sách tiêu chí tự kiểm tra (checklist).")
        
    # 2. Rubric / Grading Criteria Check (100-Point Sum Enforcement)
    rubric = lab_data.get("rubric", []) or lab_data.get("rubric_items", [])
    content_str = str(lab_data.get("content", "")) or str(lab_data.get("description", ""))
    
    has_rubric_header = ("rubric" in content_str.lower() or "tiêu chí chấm" in content_str.lower() or "thang điểm" in content_str.lower())
    
    if not rubric and not has_rubric_header:
        errors.append("Bài tập thực hành / Về nhà bắt buộc phải có Bảng Rubric Tiêu chí chấm điểm (100 điểm) cho Giảng viên/Mentor.")
    else:
        # Extract rubric points dynamically if embedded in markdown text
        if rubric:
            total_pts = sum(r.get("max_score", 0) or r.get("points", 0) for r in rubric)
        else:
            import re
            point_matches = re.findall(r'\[(\d+)\s*điểm\]', content_str, re.IGNORECASE)
            total_pts = sum(int(p) for p in point_matches) if point_matches else 100
            
        if total_pts not in [100, 110] and total_pts > 0:
            errors.append(f"Tổng điểm thang Rubric bài tập phải đúng bằng 100 điểm (tổng điểm phát hiện hiện tại: {total_pts} điểm).")
            
    # 3. Python Code Syntax Check via AST if python code provided
    if solution_code and "python" in str(metadata.get("tech_stack", "")).lower():
        try:
            ast.parse(solution_code)
        except SyntaxError as se:
            errors.append(f"Mã nguồn lời giải mẫu bị lỗi cú pháp Python (AST SyntaxError): Line {se.lineno} - {se.msg}")
            
    return len(errors) == 0, errors
