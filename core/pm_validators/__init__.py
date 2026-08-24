"""
core/pm_validators package — Modular Validators and Quality Gates for PM Syllabus and Learning Resources.
"""

from core.pm_validators.constants import (
    HYPE_WORDS,
    DIFFICULTY_BADGES,
    VAGUE_OUTCOME_VERBS,
    BLOOM_ACTION_VERBS,
    extract_out_of_scope_technologies,
    is_programming_language_course,
    get_hinh_thuc,
    get_session_num
)

from core.pm_validators.structure_validator import validate_syllabus_structure
from core.pm_validators.academic_tone_validator import validate_academic_tone
from core.pm_validators.granularity_validator import validate_pm_granularity
from core.pm_validators.scope_continuity_validator import validate_scope_continuity
from core.pm_validators.clo_bloom_validator import validate_clo_bloom_alignment
from core.pm_validators.clo_coverage_validator import validate_clo_coverage
from core.pm_validators.syllabus_linter import lint_pm_syllabus
from core.pm_validators.quality_gates import (
    audit_reading_html_quality_gate,
    audit_exercise_quality_gate
)

__all__ = [
    "HYPE_WORDS",
    "DIFFICULTY_BADGES",
    "VAGUE_OUTCOME_VERBS",
    "BLOOM_ACTION_VERBS",
    "extract_out_of_scope_technologies",
    "is_programming_language_course",
    "get_hinh_thuc",
    "get_session_num",
    "validate_syllabus_structure",
    "validate_academic_tone",
    "validate_pm_granularity",
    "validate_scope_continuity",
    "validate_clo_coverage",
    "validate_clo_bloom_alignment",
    "lint_pm_syllabus",
    "audit_reading_html_quality_gate",
    "audit_exercise_quality_gate"
]
