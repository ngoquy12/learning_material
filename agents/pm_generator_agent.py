"""
agents/pm_generator_agent.py

AI Curriculum Architect Agent that generates a complete, pedagogically-sound
curriculum syllabus (PM) from PLO, CLO, and student profile, and exports to MD and Excel.
"""

import os
import json
import shutil
import openpyxl
from copy import copy
from typing import Dict, Any, List, Optional
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from core.llm import call_llm
from agents.pm_schemas import (
    LessonBlock, SessionBlock, StudentProfile, ClassConfiguration,
    SessionBudget, PMGeneratorConfig, SyllabusPM,
)
from agents.pm_reviewer_agent import pm_reviewer_agent

SYSTEM_PROMPT = """You are a Lead Academic Director specializing in curriculum architecture at Rikkei Education.
Your task is to design a complete, pedagogically-sound curriculum syllabus (PM Syllabus) in JSON format based on PLOs, CLOs, student profiles, session count, target technology, and class configurations.

UNIVERSAL AGENT CONTRACT:
1. System directives & instructions are in English for maximum reasoning quality and instruction adherence.
2. FINAL GENERATED OUTPUT VALUES (session title, lesson title, content_scope, expected_outcome, forbidden_scope, allowed_scope) MUST ALWAYS BE WRITTEN IN 100% ACCENTED VIETNAMESE (Tiếng Việt có dấu).

CRITICAL: OUTPUT ONLY A VALID RAW JSON ARRAY. DO NOT write any explanations, Markdown commentary, or text outside JSON.

COMPREHENSIVE LESSON SCOPE & VERBOSITY DIRECTIVES:
- Session title (title): Concise, clean title under 10 words.
- Lesson title (title): Descriptive title under 12 words.
- content_scope: EXPLICIT & COMPREHENSIVE list of all concepts, keywords, methods, syntax rules, and functions taught in the lesson. DO NOT truncate or summarize loosely.
- expected_outcome: Write 1-2 precise Bloom action outcome sentences detailing exact skills mastered.
- forbidden_scope: "CẤM:" + comprehensive list of all unlearned concepts, structures, or future topics.
- allowed_scope: "ĐÃ HỌC:" + comprehensive list of all prior concepts student is authorized to use.

MANDATORY PEDAGOGICAL EXECUTION DIRECTIVES:

1. FIRST SESSIONS PACING & ATOMIC FOUNDATION PACING STANDARD:
   - Session 01 MUST be Orientation & Curriculum Roadmap (Theory/Overview). Structure MUST have EXACTLY 1 CONSOLIDATED LESSON:
     * Lesson 01 title: "Tổng quan lộ trình và Demo sản phẩm"
     * Content scope MUST cover 3 sub-sections: (1) Tổng quan nội dung & Lộ trình môn học (Timeline/List), (2) Phương pháp học tập hiệu quả & Kiến thức tiền đề (AI Pair-Programming Cursor/Windsurf), (3) Demo sản phẩm dự án đầu ra (Capstone Project Spec & Features).
     * ABSOLUTELY FORBIDDEN to create multiple lessons for Session 01 or place complex software requirements analysis into Session 01 for any course.
   - Session 02 & EARLY TECHNICAL THEORY SESSIONS (ALLOW 4 TO 5 ATOMIC LESSONS):
     * DO NOT artificially limit theory sessions to 3 lessons! Allow 3 to 5 atomic lessons per theory session (for 1.5 - 2.0 hours duration) to prevent cognitive overload.
     * Session 02 (FIRST TECHNICAL THEORY SESSION) can cover up to 5 clean atomic lessons:
       - Lesson 01: General Technology Overview ("Tổng quan / Giới thiệu về [Tech Stack]" - Execution mechanism, core paradigm, key features).
       - Lesson 02: COMPREHENSIVE TOOLING & ENVIRONMENT SETUP (IDE/Editor, Compiler/Runtime/SDK, Package Manager in ONE dedicated lesson).
       - Lesson 03: Initial Application Execution & Boilerplate (First execution, Hello World, project structure verification).
       - Lesson 04: Variable Declaration, Naming Conventions & Primitive Data Types (Variables, primitive types, memory assignment).
       - Lesson 05: Console Input/Output Operations & Type Conversion (User input, output formatting, type casting).
     * If Session 02 covers variables & I/O across 5 atomic lessons, Session 03 CAN BE THE FIRST PRACTICAL LAB ("Thực hành") practicing Session 02 concepts!
   - THEORY LESSON CONCEPT PURITY DIRECTIVE:
     * Theory lessons (`lessons` array inside Theory sessions) MUST strictly focus 100% on Theoretical Knowledge, Syntax Anatomy, Mechanism Breakdown, and Code Structure.
     * ABSOLUTELY FORBIDDEN to put practice lab tasks, exercise assignments, or practical implementation steps into the title, content_scope, or expected_outcome of a theory lesson! Practical tasks belong strictly to Practical Lab sessions ("Thực hành").

2. DYNAMIC COGNITIVE PACING & ADVANCED TOPICS DEFERRAL DIRECTIVE:
   - Light Theory: Allow max 2 consecutive light theory sessions before a mandatory Practical Lab.
   - ADVANCED TOPICS DEFERRAL: Advanced auxiliary topics not required for basic logic (e.g. Unit Testing frameworks like Pytest/JUnit/Jest, advanced linters, advanced debugging suites, complex design patterns) MUST BE DEFERRED TO THE SECOND HALF OR END OF THE COURSE (Sessions 17-23).
   - Early sessions (Sessions 01-16) MUST strictly focus on foundational programming primitives (Variables, Operators, Branching, Loops, Core Data Collections, Functions).
   - Final Session N MUST be the Final Exam ("Thi thực hành" or "Thi cuối môn").
   - Practice sessions MUST use real-world enterprise scenarios, NOT dry academic tasks.

3. NO LESSONS FOR NON-THEORY SESSIONS DIRECTIVE:
   - ABSOLUTELY FORBIDDEN to create sub-lessons for non-theory sessions ("Thực hành", "Mini project", "Project", "Hackathon", "Thi giữa môn", "Thi cuối môn"). The "lessons" array for these sessions MUST be empty `[]`.

4. MINI PROJECT ALLOCATION DIRECTIVE (COMBO-BASED & BUDGET MATCHING):
   - MUST generate the exact number of `hinh_thuc: "Mini project"` sessions matching `session_budget.mini_projects`.

5. MIDTERM EXAM PACING & SINGLE-REVIEW DIRECTIVE:
   - Schedule 1 Midterm / Hackathon exam session at Session 16 (for 24-session budget).
   - EXACTLY ONE Practical Review Session (Session 15) MUST precede the Midterm exam. The session prior to review (Session 14) MUST be a Theory session. ABSOLUTELY FORBIDDEN to schedule 2 consecutive practice sessions before Midterm!

6. STRICT CANONICAL DATA COLLECTIONS COVERAGE & OPERATIONAL GRANULARITY:
   - For ANY programming language / technology in `tech_stack`, the curriculum MUST systematically introduce and dedicate scope to ALL 4 canonical data collection paradigms of that target stack:
     1. Sequential Mutable Collections (e.g., dynamic lists, arrays, vectors).
     2. Immutable / Fixed Collections (e.g., tuples, fixed arrays, immutable records).
     3. Key-Value Association Collections (e.g., dictionaries, maps, hash tables, key-value stores).
     4. Unique Set Collections (e.g., sets, hash sets, unique collections).
   - COLLECTION CRUD & ITERATION OPERATIONAL GRANULARITY:
     * ABSOLUTELY FORBIDDEN to cram Traversal/Iteration, Addition, Mutation/Updating, and Deletion of a collection into a single 1-hour lesson!
     * Break collection operations into separate atomic lessons (e.g., Lesson A: Initialization & Indexing; Lesson B: Iteration & Traversal; Lesson C: Addition & Insertion; Lesson D: Mutation & Deletion).

7. MANDATORY SUBPROGRAMS / FUNCTIONS PILLAR IN PART 1:
   - For ANY target programming language, Subprograms / Functions (function definition, parameters, arguments, return values, local/global variable scope) ARE A MANDATORY CORE PILLAR.
   - ABSOLUTELY FORBIDDEN to omit Subprograms / Functions from Part 1 (Sessions 01-16)! Subprograms / Functions MUST be assigned dedicated theory and practice sessions before the Midterm Exam.

8. STRICT CORE VS ADVANCED SEQUENCING MATRIX:
   - Part 1 (Sessions 01-16) MUST strictly prioritize Foundational Pillars in sequential order:
     * Pillar 1: Orientation & Curriculum Roadmap
     * Pillar 2: Technology Setup & First Application Execution
     * Pillar 3: Variables, Primitive Types & Console Input/Output
     * Pillar 4: Arithmetic, Logical & Comparison Operators with Conditional Branching
     * Pillar 5: Iteration Controls & Loops
     * Pillar 6: Dynamic Mutable Collections & Immutable Collections (with atomic CRUD breakdown)
     * Pillar 7: Key-Value Association Maps & Unique Sets
     * Pillar 8: Subprograms, Modular Functions, Parameters & Return Values
     * Pillar 9: Midterm Review & Midterm Exam
   - Advanced topics (e.g., File I/O, Exception Handling, Object-Oriented Programming, Unit Testing frameworks) MUST BE DEFERRED to Part 2 (Sessions 17-24).

9. FORBIDDEN DOMAIN INJECTION DIRECTIVE:
   - ABSOLUTELY FORBIDDEN to inject terms like 'backend', 'frontend', 'web api', 'microservices', 'restful' into titles or scopes unless explicitly declared in course_name or CLOS/PLOS!
   - For introductory programming courses (e.g. basic language syntax), titles MUST strictly focus on foundational programming concepts ("Lập trình cơ bản", "Cú pháp ngôn ngữ", "Cấu trúc dữ liệu").

10. STRICT NON-THEORY SESSION ADJACENCY ISOLATION DIRECTIVE:
    - ABSOLUTELY FORBIDDEN to schedule 2 consecutive Practice sessions ("Thực hành" + "Thực hành")!
    - ABSOLUTELY FORBIDDEN to schedule a Practice session adjacent to a Mini Project session ("Thực hành" + "Mini project" OR "Mini project" + "Thực hành")!
    - ABSOLUTELY FORBIDDEN to schedule 2 adjacent Mini Project sessions ("Mini project" + "Mini project")!
    - Every Practical Lab ("Thực hành") or Mini Project ("Mini project") MUST be separated by a Theory session ("Lý thuyết") (or Exam)!
    - Required Flow: Theory -> Practice -> Theory -> Mini Project -> Theory -> Practice.

14. MANDATORY KEYWORD EXTRACTION FROM CLO/PLO & MAIN CONTENT:
   - Read every sentence in CLO, PLO, and Main Content carefully.
   - Extract environment tools (SDK / Runtime / Compiler / Virtual Environment / Package Manager corresponding to target tech_stack), AI tools (AI IDE / Code Editor), and domain continuity contexts and place them into the correct sessions.

15. ZERO CAPSTONE PROJECT DIRECTIVE:
   - IF `capstone_project` in `session_budget` is 0, ABSOLUTELY FORBIDDEN to generate Capstone Project sessions.
   - The final session MUST be a Practical Exam / Final Exam ("Thi thực hành" or "Thi cuối môn").

REQUIRED JSON OUTPUT FORMAT (RETURN ONLY A VALID RAW JSON ARRAY):
[
  {
    "session_num": 1,
    "hinh_thuc": "Lý thuyết",
    "title": "Chủ đề của buổi học",
    "content_scope": "",
    "expected_outcome": "",
    "forbidden_scope": "",
    "allowed_scope": "",
    "lessons": [
      {
        "lesson_num": 1,
        "title": "Tiêu đề chi tiết của bài học nhỏ",
        "content_scope": "Khái niệm A; Cú pháp B; Công cụ C",
        "expected_outcome": "Khai báo thành công X, phân biệt được Y",
        "forbidden_scope": "CẤM: List, Dict, Loop, Function, Class",
        "allowed_scope": "ĐÃ HỌC: Biến, kiểu dữ liệu, print()"
      }
    ]
  }
]
"""

# ---------------------------------------------------------------------------
# Constants for Excel styling
# ---------------------------------------------------------------------------
_HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
_HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
_HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)

_DATA_FONT = Font(name="Calibri", size=10)
_DATA_FONT_BOLD = Font(name="Calibri", size=10, bold=True)
_DATA_ALIGN = Alignment(horizontal="left", vertical="center", wrap_text=True)
_DATA_ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

_THIN_BORDER = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)

_SESSION_TYPE_FILLS = {
    "Lý thuyết":   PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid"),
    "Thực hành":   PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid"),
    "Mini project": PatternFill(start_color="FFF7ED", end_color="FFF7ED", fill_type="solid"),
    "Hackathon":   PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid"),
    "Thi giữa môn": PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid"),
    "Thi cuối môn": PatternFill(start_color="FEF2F2", end_color="FEF2F2", fill_type="solid"),
    "Project":     PatternFill(start_color="F0FDF4", end_color="F0FDF4", fill_type="solid"),
}
_DEFAULT_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

_COL_WIDTHS = [14, 16, 16, 36, 36, 45, 45, 35, 35, 22]

# Maximum number of self-correction rounds for prerequisite guard
MAX_CORRECTION_ROUNDS = 3


# ---------------------------------------------------------------------------
# Prerequisite Guard (Part L)
# ---------------------------------------------------------------------------
def _validate_prerequisite_chain(pm_data: List[Dict[str, Any]]) -> tuple:
    """
    Validates pedagogical prerequisite rules on the generated PM.
    Returns (is_valid: bool, errors: List[str]).
    """
    errors = []

    if not pm_data:
        errors.append("PM rỗng — không có session nào được sinh ra.")
        return False, errors

    # Rule 1: Session 01 must be orientation (Lý thuyết)
    s1 = pm_data[0]
    ht1 = str(s1.get("hinh_thuc", "")).strip()
    if "Lý thuyết" not in ht1:
        errors.append(f"Session 01 phải là 'Lý thuyết' (Định hướng), nhưng hiện tại là '{ht1}'.")

    # Rule 2: Session 02 must be Lý thuyết (not Thực hành)
    if len(pm_data) >= 2:
        s2 = pm_data[1]
        ht2 = str(s2.get("hinh_thuc", "")).strip()
        if "Thực hành" in ht2 or "Mini project" in ht2:
            errors.append(f"Session 02 PHẢI là 'Lý thuyết' kỹ thuật, nhưng hiện tại là '{ht2}'.")

    # Rule 3: Session 03 must be Thực hành
    if len(pm_data) >= 3:
        s3 = pm_data[2]
        ht3 = str(s3.get("hinh_thuc", "")).strip()
        if "Thực hành" not in ht3:
            errors.append(f"Session 03 PHẢI là 'Thực hành' đầu tiên, nhưng hiện tại là '{ht3}'.")

    # Rule 4: Last session must be exam or project
    last = pm_data[-1]
    ht_last = str(last.get("hinh_thuc", "")).strip()
    valid_finals = ["Thi cuối môn", "Project", "Dự án cuối khóa"]
    if not any(vf in ht_last for vf in valid_finals):
        errors.append(f"Buổi cuối cùng phải là Thi cuối môn hoặc Project, nhưng hiện tại là '{ht_last}'.")

    # Rule 5: Non-theory sessions must have empty lessons
    for s in pm_data:
        ht = str(s.get("hinh_thuc", "")).strip()
        lessons = s.get("lessons", [])
        if "Lý thuyết" not in ht and len(lessons) > 0:
            errors.append(
                f"Session {s.get('session_num', '?')} ({ht}) không nên có lessons con, nhưng có {len(lessons)} lessons."
            )

    # Rule 6: No practice session before any theory has been taught
    theory_seen = False
    for s in pm_data:
        ht = str(s.get("hinh_thuc", "")).strip()
        if "Lý thuyết" in ht:
            # Skip orientation (session 1)
            snum = s.get("session_num", 0)
            if snum > 1:
                theory_seen = True
        if "Thực hành" in ht and not theory_seen:
            errors.append(
                f"Session {s.get('session_num', '?')} là Thực hành nhưng chưa có buổi Lý thuyết kỹ thuật nào trước đó."
            )

    # Rule 7: Theory sessions must not exceed 4 lessons
    for s in pm_data:
        ht = str(s.get("hinh_thuc", "")).strip()
        lessons = s.get("lessons", [])
        if "Lý thuyết" in ht and len(lessons) > 4:
            errors.append(
                f"Session {s.get('session_num', '?')} (Lý thuyết) có {len(lessons)} lessons — vượt quá giới hạn tối đa 4."
            )

    # Rule 8: Session numbers must be strictly sequential (1, 2, 3, ...)
    # This catches Part1+Part2 merge bugs where sessions restart numbering
    expected_num = 1
    for s in pm_data:
        actual = s.get("session_num", -1)
        if actual != expected_num:
            errors.append(
                f"Số thứ tự session không liên tục: mong đợi Session {expected_num:02d}, nhận Session {actual}. "
                f"Có thể do lỗi ghép Phần 1 + Phần 2."
            )
            break
        expected_num += 1

    is_valid = len(errors) == 0
    return is_valid, errors



def _self_correct_pm(
    pm_data: List[Dict[str, Any]],
    errors: List[str],
    course_id: str,
    course_name: str,
    clos: List[str],
    plos: List[str],
    student_profile: Dict[str, Any],
    session_budget: Dict[str, Any],
    tech_stack: str,
    class_configuration: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Calls LLM with the current PM and detected errors to produce a corrected version.
    """
    error_block = "\n".join(f"- {e}" for e in errors)

    correction_prompt = f"""Current curriculum contains the following pedagogical defects / deductions (GOAL: 100/100 PERFECT GRADE):
{error_block}

Current curriculum needing revision:
{json.dumps(pm_data, ensure_ascii=False, indent=2)}

REVISE and UPGRADE the curriculum syllabus to resolve ALL defects and warnings above to achieve a 100/100 score.
- For vague bloom verbs: Replace with measurable Bloom action verbs in Accented Vietnamese ("Phân biệt được...", "Khởi tạo thành công...", "Giải quyết được...").
- For sequence ordering or practice load warnings: Restructure the 3 lessons per theory session or add code depth.
- Retain valid content and only adjust/restructure non-compliant or flagged sessions.
Return ONLY raw updated JSON array."""

    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=correction_prompt,
        json_mode=True,
        agent_name="PM Generator Agent (Self-Correction)"
    )

    try:
        clean_json = response.replace("```json", "").replace("```", "").strip()
        parsed_data = json.loads(clean_json)
        if isinstance(parsed_data, list):
            return parsed_data
        elif isinstance(parsed_data, dict) and "sessions" in parsed_data:
            return parsed_data["sessions"]
        else:
            print(f"  [Guard] Output sửa lỗi không phải list: {type(parsed_data)}")
            return pm_data
    except Exception as e:
        print(f"  [Guard] Lỗi parse JSON sửa lỗi: {e}")
        return pm_data


# ---------------------------------------------------------------------------
# Core generation functions
# ---------------------------------------------------------------------------
def generate_curriculum_pm(
    course_id: str,
    course_name: str,
    clos: List[str],
    plos: List[str],
    student_profile: Dict[str, Any],
    session_budget: Dict[str, Any],
    tech_stack: str,
    class_configuration: Dict[str, Any],
    existing_pm: Optional[List[Dict[str, Any]]] = None,
    main_content: str = "",
    exam_type: str = ""
) -> List[Dict[str, Any]]:
    """
    Invokes LLM to generate the structured PM syllabus.
    Splits into two parts for long courses to avoid token truncation limits.
    Applies prerequisite guard with up to 3 self-correction rounds.
    """
    total_sessions = session_budget.get("total_sessions")
    if not total_sessions or total_sessions <= 0:
        raise ValueError(f"Lỗi cấu hình PM: Thiếu 'total_sessions' hợp lệ trong session_budget ({session_budget}). Không cho phép fallback tự ý.")
    hackathon_sess = int(total_sessions * 2 / 3)
    review_sess = hackathon_sess - 1

    if total_sessions > 18:
        print(f"  [SPGA] Số lượng buổi lớn ({total_sessions} buổi). Thực hiện sinh thành 2 phần tách biệt...")
        half = total_sessions // 2

        # Part 1: sessions 1 to half
        part1_instruction = f"""Design PART 1: EXACTLY the first {half} Sessions (Session 01 to Session {half:02d}).
MANDATORY Course Opening Session Allocation Rules:
- Session 01 is Orientation & Roadmap (Theory), no technical coding or SRS parsing. Lesson 03 MUST be "Demo sản phẩm thực tế sẽ đạt được sau khi kết thúc môn học & Kỳ vọng đầu ra".
- Session 02 MUST be Technical Theory Session 1 (ALLOW UP TO 4-5 ATOMIC LESSONS): Lesson 01 (Technology Overview), Lesson 02 (Comprehensive Tooling Setup), Lesson 03 (First Application Execution & Hello World Boilerplate), Lesson 04 (Variable Declaration, Naming Conventions & Primitive Data Types), Lesson 05 (Console Input/Output Operations & Type Conversion).
- Session 03 is the FIRST Practical Lab Session ("Thực hành") practicing Session 02 foundational concepts (Tooling Setup, Variables & Console I/O).
- ADVANCED TOPIC DEFERRAL: Unit Testing frameworks, advanced linters, and testing suites MUST BE DEFERRED to the second half (Sessions 17-23). Early sessions MUST strictly focus on basic syntax and primitives.
- THEORY LESSON PURITY: Theory lessons MUST focus 100% on theoretical syntax & concepts. FORBIDDEN to put practical lab tasks or exercises into theory lessons!
- MANDATORY SUBPROGRAMS / FUNCTIONS PILLAR: Part 1 MUST include dedicated Theory + Practice sessions covering Subprograms / Functions (definition, parameters, arguments, return values, variable scope) BEFORE the Midterm Exam!
- COLLECTION CRUD & ITERATION OPERATIONAL GRANULARITY: DO NOT cram Traversal, Addition, Mutation, and Deletion of a collection into 1 lesson! Break CRUD operations across separate atomic lessons (e.g. Lesson A: Concept & Indexing, Lesson B: Iteration & Traversal, Lesson C: Insertion & Appending, Lesson D: Updating & Deletion).
- NON-THEORY ADJACENCY ISOLATION: ABSOLUTELY FORBIDDEN to schedule 2 Practice sessions ("Thực hành") adjacent to each other! ABSOLUTELY FORBIDDEN to schedule a Practice session ("Thực hành") adjacent to a Mini Project ("Mini project")! ABSOLUTELY FORBIDDEN to schedule 2 Mini Projects adjacent to each other! Every Practice or Mini Project MUST be separated by a Theory session ("Lý thuyết")!
- Apply Theory-Practice pairing rules. Allocate Mini Projects after combos as budgeted."""

        pm_part1 = _call_generator_agent(
            course_id, course_name, clos, plos, student_profile, session_budget, tech_stack, class_configuration,
            prompt_suffix=part1_instruction, existing_pm=existing_pm,
            main_content=main_content, exam_type=exam_type
        )

        if not pm_part1:
            print("  [Error] Không thể tạo Phân 1 của chương trình học.")
            return []

        print(f"  [SPGA] Đã sinh xong Phân 1 ({len(pm_part1)} sessions). Đang sinh Phần 2...")

        capstone_count = session_budget.get("capstone_project", 0)
        final_sess_desc = f"Thi thực hành / Thi cuối môn (Practical Final Exam: {exam_type}). ABSOLUTELY FORBIDDEN to generate any Capstone Project or Project sessions since capstone_project budget is 0." if capstone_count == 0 else "Capstone Project Defense."

        # Part 2: sessions half + 1 to total_sessions
        part2_instruction = f"""Design PART 2: Remaining Sessions from Session {half + 1:02d} to Session {total_sessions:02d} (total {total_sessions - half} sessions).
Here is the list of Sessions generated in PART 1 for reference and continuity:
{json.dumps(pm_part1, ensure_ascii=False, indent=2)}

MANDATORY DIRECTIVES:
- Continue curriculum design starting precisely at Session {half + 1:02d} through Session {total_sessions:02d}.
- Ensure knowledge continuity and prerequisite flow from prior sessions.
- Place Midterm Exam at Session {hackathon_sess:02d}. EXACTLY ONE Practical Review Session (Session {review_sess:02d}) MUST precede the Midterm exam. The session prior to review (Session {review_sess - 1:02d}) MUST be a Theory session. FORBIDDEN to schedule 2 consecutive practice sessions before Midterm!
- Final Session (Session {total_sessions:02d}) MUST be {final_sess_desc}"""

        pm_part2 = _call_generator_agent(
            course_id, course_name, clos, plos, student_profile, session_budget, tech_stack, class_configuration,
            prompt_suffix=part2_instruction, existing_pm=existing_pm,
            main_content=main_content, exam_type=exam_type
        )

        if not pm_part2:
            print("  [Warning] Không thể sinh Phần 2. Trả về kết quả của Phần 1.")
            return pm_part1

        # Merge parts and normalize session numbers
        merged = []
        for idx, s in enumerate(pm_part1 + pm_part2, 1):
            s["session_num"] = idx
            ht = str(s.get("hinh_thuc", "")).strip()
            if "Lý thuyết" not in ht:
                s["lessons"] = []
            merged.append(s)

        print(f"  [SPGA] Ghép nối thành công lộ trình chương trình học ({len(merged)} buổi).")
        pm_data = merged
    else:
        # Standard single call
        capstone_count = session_budget.get("capstone_project", 0)
        final_sess_desc = f"Thi thực hành / Thi cuối môn (Practical Final Exam: {exam_type}). ABSOLUTELY FORBIDDEN to generate any Capstone Project or Project sessions since capstone_project budget is 0." if capstone_count == 0 else "Capstone Project Defense."

        single_instruction = f"""Design entire curriculum syllabus containing EXACTLY {total_sessions} Sessions (Session 01 to Session {total_sessions:02d}).
MANDATORY Course Opening Session Allocation Rules:
- Session 01 is Course Orientation (Theory), no technical coding or setup.
- Session 02 MUST be the first Technical Theory session.
- Session 03 MUST be the first Practical Lab session.
- ABSOLUTELY FORBIDDEN to place Practical Lab at Session 02.
Final Session (Session {total_sessions:02d}) MUST be {final_sess_desc}
If total sessions >= 16: place Midterm Hackathon Exam at Session {hackathon_sess:02d} and Practical Review Lab at Session {review_sess:02d}."""

        res = _call_generator_agent(
            course_id, course_name, clos, plos, student_profile, session_budget, tech_stack, class_configuration,
            prompt_suffix=single_instruction, existing_pm=existing_pm,
            main_content=main_content, exam_type=exam_type
        )
        for s in res:
            ht = str(s.get("hinh_thuc", "")).strip()
            if "Lý thuyết" not in ht:
                s["lessons"] = []
        pm_data = res

    # --------------- PM Reviewer & QA Auditor Agent ---------------
    config_dict = {
        "tech_stack": tech_stack,
        "class_configuration": class_configuration,
        "student_profile": student_profile,
        "session_budget": session_budget
    }
    course_info_dict = {
        "course_id": course_id,
        "course_name": course_name,
        "clos": clos,
        "plos": plos
    }

    # Standardize Session 01 lessons to fixed titles
    pm_data = _normalize_session_01_lessons(pm_data)

    for round_num in range(1, MAX_CORRECTION_ROUNDS + 1):
        review_result = pm_reviewer_agent(pm_data, config_dict, course_info_dict)
        score = review_result["score"]
        violations = review_result["rule_violations"]

        if score == 100 or (score >= 98 and len(violations) == 0):
            print(f"  [PM Reviewer] Phê duyệt tuyệt đối — PM đạt điểm chất lượng tối đa ({score}/100).")
            break

        if review_result["is_approved"]:
            print(f"  [PM Reviewer] Vòng {round_num}/{MAX_CORRECTION_ROUNDS}: Đã đạt {score}/100 (qua ngưỡng 90), đang tiếp tục tự tối ưu để hướng tới ĐIỂM TỐI ĐA (100/100)...")
        else:
            print(f"  [PM Reviewer] Vòng {round_num}/{MAX_CORRECTION_ROUNDS}: Chưa đạt chuẩn ({score}/100, {len(violations)} vi phạm). Đang tự sửa lỗi...")

        pm_data = _self_correct_pm(
            pm_data, violations,
            course_id, course_name, clos, plos,
            student_profile, session_budget, tech_stack, class_configuration,
        )
        pm_data = _normalize_session_01_lessons(pm_data)
        # Re-enforce non-theory empty lessons after correction
        for s in pm_data:
            ht = str(s.get("hinh_thuc", "")).strip()
            if "Lý thuyết" not in ht:
                s["lessons"] = []
    else:
        # Exhausted all rounds
        final_review = pm_reviewer_agent(pm_data, config_dict, course_info_dict)
        print(f"  [PM Reviewer] Hoàn tất {MAX_CORRECTION_ROUNDS} vòng tối ưu. Điểm chất lượng cuối cùng: {final_review['score']}/100.")

    return _normalize_session_01_lessons(pm_data)


def _normalize_session_01_lessons(pm_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enforces 1 single consolidated lesson for Session 01 as requested by pedagogical standards."""
    if not pm_data:
        return pm_data

    for s in pm_data:
        if s.get("session_num") == 1 or "Session 01" in str(s.get("title", "")):
            s["lessons"] = [{
                "lesson_num": 1,
                "title": "Tổng quan lộ trình và Demo sản phẩm",
                "content_scope": "1. Tổng quan nội dung & Lộ trình môn học (Timeline/List) | 2. Phương pháp học tập hiệu quả & Kiến thức tiền đề (AI Pair-Programming Cursor/Windsurf) | 3. Demo sản phẩm dự án đầu ra (Capstone Project Spec & Features)",
                "expected_outcome": "Nắm vững toàn bộ cấu trúc lộ trình môn học, áp dụng phương pháp học tập kết hợp công cụ AI IDE và hiểu rõ các tiêu chuẩn sản phẩm dự án đầu ra.",
                "forbidden_scope": "CẤM: Gõ lệnh CLI, cài đặt phần mềm, viết mã nguồn, tạo code demo hay code sandbox rỗng.",
                "allowed_scope": "ĐÃ HỌC: Bài mở đầu (Chưa có).",
            }]
            break
    return pm_data


def _call_generator_agent(
    course_id: str,
    course_name: str,
    clos: List[str],
    plos: List[str],
    student_profile: Dict[str, Any],
    session_budget: Dict[str, Any],
    tech_stack: str,
    class_configuration: Dict[str, Any],
    prompt_suffix: str,
    existing_pm: Optional[List[Dict[str, Any]]] = None,
    main_content: str = "",
    exam_type: str = ""
) -> List[Dict[str, Any]]:
    mode_text = ""
    if existing_pm:
        mode_text = f"""
MODE: REFACTOR MODE (UPDATE EXISTING CURRICULUM SYLLABUS)
Existing curriculum structure on disk:
{json.dumps(existing_pm, ensure_ascii=False, indent=2)}
"""

    user_prompt = f"""Author full Academic PM Curriculum Syllabus for course:
Course: {course_id} - {course_name}

1. LEARNING OUTCOMES (CLO & PLO):
- Course Learning Outcomes (CLO):
{json.dumps(clos, ensure_ascii=False, indent=2)}

- Program Learning Outcomes (PLO):
{json.dumps(plos, ensure_ascii=False, indent=2)}

2. MANDATORY MAIN CONTENT & CURRICULUM SCOPE:
{main_content if main_content else 'Unspecified'}

3. PRIMARY ASSESSMENT METHOD:
{exam_type if exam_type else 'Unspecified'}

4. MANDATORY SESSION BUDGET & ALLOCATION:
- Total Sessions: {session_budget.get('total_sessions', '?')} sessions ({class_configuration.get('session_duration_hours', 2.0)} hours per session)
- Theory Sessions: {session_budget.get('theory_sessions', '?')}
- Practice Sessions: {session_budget.get('practice_sessions', '?')}
- Mini Project Sessions: {session_budget.get('mini_projects', '?')}
- Midterm / Exam Sessions: {session_budget.get('final_exam', '?')}
- Capstone Project Sessions: {session_budget.get('capstone_project', '?')}

5. STUDENT PROFILE & CLASS CONFIGURATION:
- Student Profile: {json.dumps(student_profile, ensure_ascii=False, indent=2)}
- Class Configuration: {json.dumps(class_configuration, ensure_ascii=False, indent=2)}
- Target Technology Stack: {tech_stack}

STRICT PEDAGOGICAL & KNOWLEDGE BOUNDARY DIRECTIVES ({course_id}):
- Session count and session types MUST match 100% with the SESSION BUDGET above.
- MUST cover all mandatory main content topics from the curriculum framework.
- ONLY use technologies, libraries, and concepts within target tech stack: [{tech_stack}].
- FORBIDDEN to introduce unlisted technologies (databases, frameworks, ORMs, auth if not listed).
{mode_text}

Specific Phase Generation Task:
{prompt_suffix}

MANDATORY OUTPUT CONTRACT: Return ONLY a valid JSON array of sessions adhering strictly to the pedagogical rules.
"""

    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        json_mode=True,
        agent_name="PM Generator Agent"
    )

    try:
        clean_json = response.replace("```json", "").replace("```", "").strip()
        parsed_data = json.loads(clean_json)
        if isinstance(parsed_data, list):
            return parsed_data
        elif isinstance(parsed_data, dict) and "sessions" in parsed_data:
            return parsed_data["sessions"]
        else:
            print(f"  [Warning] Output JSON is not a list: {parsed_data}")
            return []
    except Exception as e:
        print(f"  [Error] Failed to parse generated PM JSON: {e}. Output was:\n{response}")
        return []


# ---------------------------------------------------------------------------
# Export functions
# ---------------------------------------------------------------------------
def export_pm_to_markdown(
    pm_data: List[Dict[str, Any]],
    course_id: str,
    course_name: str,
    clos: List[str],
    plos: List[str],
    filepath: str,
    tech_stack: str = "",
):
    """
    Exports the generated syllabus PM to a beautiful Markdown report.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    lines = []
    lines.append(f"# Chương Trình Học Chi Tiết Môn Học: {course_id} - {course_name}\n")

    lines.append("## 1. Chuẩn Đầu Ra Học Kỳ (PLO - Program Learning Outcomes)")
    for plo in plos:
        lines.append(f"- {plo}")
    lines.append("")

    lines.append("## 2. Chuẩn Đầu Ra Môn Học (CLO - Course Learning Outcomes)")
    for clo in clos:
        lines.append(f"- {clo}")
    lines.append("")

    lines.append("## 3. Kế Hoạch Giảng Dạy Từng Buổi (Syllabus Sessions)")
    lines.append("| Session | Loại Session | Mã Session | Tên Tiêu Đề Session | Tên Lesson | Nội Dung Chi Tiết | Kết Quả Mong Đợi | Phạm Vi Cấm Dùng | Phạm Vi Đã Học | Tech Stack |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    session_type_code_map = {
        "Lý thuyết": "THEORY", "Thực hành": "PRACTICE", "Mini project": "MINI_PROJECT",
        "Project": "PROJECT", "Hackathon": "HACKATHON", "Thi giữa môn": "MIDTERM", "Thi cuối môn": "FINAL",
    }

    for sess in pm_data:
        num = sess.get("session_num", sess.get("session", ""))
        hinh_thuc = sess.get("hinh_thuc", sess.get("session_type", ""))
        title = sess.get("title", sess.get("session_title", ""))
        lessons = sess.get("lessons", [])
        s_tech = sess.get("tech_stack_version", tech_stack)

        num_str = f"Session {int(num):02d}" if str(num).isdigit() else str(num)
        session_code = session_type_code_map.get(hinh_thuc, hinh_thuc.upper().replace(" ", "_"))
        session_title_full = f"{num_str} - {title}"

        if not lessons:
            s_noidung = sess.get("content_scope", "")
            s_outcome = sess.get("expected_outcome", "")
            s_forbidden = sess.get("forbidden_scope", "")
            s_allowed = sess.get("allowed_scope", "")
            lines.append(f"| {num_str} | {hinh_thuc} | {session_code} | {session_title_full} | {session_title_full} | {s_noidung} | {s_outcome} | {s_forbidden} | {s_allowed} | {s_tech} |")
        else:
            for idx, l in enumerate(lessons):
                l_num = l.get("lesson_num", idx + 1)
                l_title = l.get("title", "")
                l_noidung = l.get("content_scope", l.get("note", ""))
                l_outcome = l.get("expected_outcome", "")
                l_forbidden = l.get("forbidden_scope", "")
                l_allowed = l.get("allowed_scope", "")

                l_num_str = f"{int(l_num):02d}" if str(l_num).isdigit() else str(l_num)
                lesson_name = f"Lesson {l_num_str}: {l_title}"

                if idx == 0:
                    lines.append(f"| {num_str} | {hinh_thuc} | {session_code} | {session_title_full} | {lesson_name} | {l_noidung} | {l_outcome} | {l_forbidden} | {l_allowed} | {s_tech} |")
                else:
                    lines.append(f"| | | | | {lesson_name} | {l_noidung} | {l_outcome} | {l_forbidden} | {l_allowed} | {s_tech} |")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [Export] Saved Markdown syllabus to: {filepath}")


def export_pm_to_excel(
    pm_data: List[Dict[str, Any]],
    course_id: str,
    course_name: str,
    filepath: str,
    template_path: Optional[str] = None,
    clos: Optional[List[str]] = None,
    plos: Optional[List[str]] = None,
    student_profile: Optional[Dict[str, Any]] = None,
    tech_stack: str = "",
):
    """
    Exports the generated syllabus PM to a styled Excel spreadsheet.
    Copies from PM_Template_Standard.xlsx if available, applying professional
    color-coded styling per session type with merged cells.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Determine effective template path
    effective_template = template_path
    if not effective_template or not os.path.exists(effective_template):
        # Try standard location relative to project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        candidate = os.path.join(project_root, "templates", "PM_Template_Standard.xlsx")
        if os.path.exists(candidate):
            effective_template = candidate

    if effective_template and os.path.exists(effective_template):
        try:
            shutil.copy2(effective_template, filepath)
        except PermissionError:
            base, ext = os.path.splitext(filepath)
            filepath = f"{base}_New{ext}"
            shutil.copy2(effective_template, filepath)
            print(f"  [Export Warning] File gốc đang mở trong Excel. Đã lưu sang tệp mới: {filepath}")

        wb = openpyxl.load_workbook(filepath)
        ws = wb.active
        print(f"  [Export] Loaded template: {effective_template}")

        # Clear existing data rows (keep header row 5)
        if ws.max_row > 5:
            ws.delete_rows(6, ws.max_row - 5)
            # Clean up template's old merged cells in the data area (row >= 6) to avoid overlapping/corrupted merges
            for m_range in list(ws.merged_cells.ranges):
                if m_range.min_row >= 6:
                    ws.merged_cells.remove(m_range)

        # Write metadata rows 1-3
        persona_text = ""
        if student_profile:
            persona_text = f"Trình độ: {student_profile.get('entry_level', 'beginner')}, Nền tảng: {student_profile.get('background', 'non-it')}"
        ws.cell(row=1, column=2, value=persona_text)

        clo_text = "; ".join(clos) if clos else ""
        ws.cell(row=2, column=2, value=clo_text)

        ws.cell(row=3, column=2, value=f"Xây dựng sản phẩm dự án cuối khóa sử dụng {tech_stack}")
    else:
        # Fallback: create from scratch with styling
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"{course_id}"
        print(f"  [Export] Tạo mới workbook (không tìm thấy template)")

        # Write title
        ws.cell(row=1, column=1, value=f"Môn học: {course_id} - {course_name}")
        ws.merge_cells("A1:J1")

        # Write headers at row 5
        headers = [
            'Session', 'Loại Session', 'Mã Session', 'Tên Tiêu Đề Session',
            'Tên Lesson', 'Nội Dung Chi Tiết (Lesson Scope)',
            'Kết Quả Mong Đợi', 'Phạm Vi CẤM DÙNG',
            'Phạm Vi ĐÃ HỌC', 'Tech Stack & Quy Chuẩn'
        ]
        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=5, column=col_idx, value=h)
            cell.font = _HEADER_FONT
            cell.fill = _HEADER_FILL
            cell.alignment = _HEADER_ALIGN
            cell.border = _THIN_BORDER

        # Set column widths
        for i, width in enumerate(_COL_WIDTHS):
            col_letter = openpyxl.utils.get_column_letter(i + 1)
            ws.column_dimensions[col_letter].width = width

        # Set header row height
        ws.row_dimensions[5].height = 28

    # --- Populate data rows starting from row 6 ---
    current_row = 6
    session_type_code_map = {
        "Lý thuyết": "THEORY",
        "Thực hành": "PRACTICE",
        "Mini project": "MINI_PROJECT",
        "Project": "PROJECT",
        "Hackathon": "HACKATHON",
        "Thi giữa môn": "MIDTERM",
        "Thi cuối môn": "FINAL",
    }

    for sess in pm_data:
        num = sess.get("session_num", "")
        hinh_thuc = str(sess.get("hinh_thuc", "")).strip()
        title = sess.get("title", "")
        lessons = sess.get("lessons", [])

        num_str = f"Session {int(num):02d}" if str(num).isdigit() else str(num)
        session_code = session_type_code_map.get(hinh_thuc, hinh_thuc.upper().replace(" ", "_"))
        session_title_full = f"{num_str} - {title}"

        # Determine fill color for this session type
        fill = _DEFAULT_FILL
        for key, f in _SESSION_TYPE_FILLS.items():
            if key in hinh_thuc:
                fill = f
                break

        if not lessons:
            # Single row for non-theory sessions
            s_noidung = sess.get("content_scope", "")
            s_outcome = sess.get("expected_outcome", "")
            s_forbidden = sess.get("forbidden_scope", "")
            s_allowed = sess.get("allowed_scope", "")
            row_data = [num_str, hinh_thuc, session_code, session_title_full, session_title_full, s_noidung, s_outcome, s_forbidden, s_allowed, tech_stack]
            for col_idx, val in enumerate(row_data, 1):
                cell = ws.cell(row=current_row, column=col_idx, value=val)
                cell.font = _DATA_FONT_BOLD if col_idx <= 4 else _DATA_FONT
                cell.alignment = _DATA_ALIGN_CENTER if col_idx <= 3 else _DATA_ALIGN
                cell.fill = fill
                cell.border = _THIN_BORDER
            ws.row_dimensions[current_row].height = 24
            current_row += 1
        else:
            # Multiple rows for theory sessions with lessons
            start_row = current_row
            for idx, l in enumerate(lessons):
                l_num = l.get("lesson_num", idx + 1)
                l_title = l.get("title", "")
                l_noidung = l.get("content_scope", l.get("note", ""))
                l_outcome = l.get("expected_outcome", "")
                l_forbidden = l.get("forbidden_scope", "")
                l_allowed = l.get("allowed_scope", "")
                l_num_str = f"{int(l_num):02d}" if str(l_num).isdigit() else str(l_num)

                lesson_name = f"Lesson {l_num_str}: {l_title}"

                if idx == 0:
                    # First lesson row — write session columns
                    row_data = [num_str, hinh_thuc, session_code, session_title_full, lesson_name, l_noidung, l_outcome, l_forbidden, l_allowed, tech_stack]
                else:
                    # Subsequent lesson rows — session columns blank (will be merged)
                    row_data = [None, None, None, None, lesson_name, l_noidung, l_outcome, l_forbidden, l_allowed, tech_stack]

                for col_idx, val in enumerate(row_data, 1):
                    cell = ws.cell(row=current_row, column=col_idx, value=val)
                    cell.font = _DATA_FONT_BOLD if col_idx <= 4 and idx == 0 else _DATA_FONT
                    cell.alignment = _DATA_ALIGN_CENTER if col_idx <= 3 else _DATA_ALIGN
                    cell.fill = fill
                    cell.border = _THIN_BORDER
                ws.row_dimensions[current_row].height = 24
                current_row += 1

            # Merge session info cells (columns A-D) if multiple lessons
            if len(lessons) > 1:
                end_row = current_row - 1
                for merge_col in range(1, 5):  # Columns A, B, C, D
                    ws.merge_cells(
                        start_row=start_row, start_column=merge_col,
                        end_row=end_row, end_column=merge_col
                    )

    try:
        wb.save(filepath)
        print(f"  [Export] Saved Excel syllabus to: {filepath}")
    except PermissionError:
        base, ext = os.path.splitext(filepath)
        fallback = f"{base}_New{ext}"
        wb.save(fallback)
        print(f"  [Export Warning] File đang bị khóa bởi tiến trình Excel khác. Đã lưu thành công sang tệp: {fallback}")

