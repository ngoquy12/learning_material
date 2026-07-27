"""
core/validators/project_validator.py
Programmatic Validation Layer for Mini-Projects and Major Projects.
Ensures grading rubric scale sums to exactly 100 points and validates project specifications.
"""

from typing import Tuple, List, Dict, Any

def validate_project_spec(project_data: Dict[str, Any], metadata: Dict[str, Any] = None) -> Tuple[bool, List[str]]:
    """
    Validates project specifications, rubric grading scale (must sum to 100 pts), and requirements.
    """
    if not project_data:
        return False, ["Dữ liệu đồ án/dự án bị trống."]
        
    errors = []
    
    title = project_data.get("title", "")
    requirements = project_data.get("requirements", [])
    rubric = project_data.get("rubric", [])
    
    if not title:
        errors.append("Tên dự án bị trống.")
        
    if not requirements:
        errors.append("Dự án phải có danh sách các yêu cầu chức năng (requirements).")
        
    # Rubric Score Sum Validation (Must equal 100 points)
    if rubric:
        total_score = 0
        for r_item in rubric:
            score = r_item.get("max_score", 0) or r_item.get("points", 0)
            total_score += score
            
        if total_score != 100 and total_score > 0:
            errors.append(f"Tổng điểm thang Rubric chấm đồ án phải đúng bằng 100 điểm (tổng hiện tại: {total_score} điểm).")
            
    return len(errors) == 0, errors
