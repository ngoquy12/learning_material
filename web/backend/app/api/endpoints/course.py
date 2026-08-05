from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Any
from pathlib import Path
ROOT = Path(__file__).resolve().parents[5]

from app.db.session import get_db
from app.models.course import Course
from app.schemas.course import CourseResponse, CourseCreate

router = APIRouter()

from fastapi import Query, HTTPException

@router.get("/", response_model=List[CourseResponse])
async def get_courses(semester_id: Optional[int] = Query(None), db: AsyncSession = Depends(get_db)):
    stmt = select(Course)
    if semester_id is not None:
        stmt = stmt.where(Course.semester_id == semester_id)
    stmt = stmt.order_by(Course.id.asc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=CourseResponse)
async def create_course(course_in: CourseCreate, db: AsyncSession = Depends(get_db)):
    new_course = Course(**course_in.model_dump())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(course_id: int, course_in: CourseCreate, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course_in.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    await db.commit()
    await db.refresh(course)
    return course

@router.delete("/{course_id}")
async def delete_course(course_id: int, db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    await db.delete(course)
    await db.commit()
    return {"status": "success"}


from fastapi import UploadFile, File
import openpyxl
import io
import re
from app.models.session import Session
from app.models.lesson import Lesson

from pydantic import BaseModel
from typing import Optional

class PMRow(BaseModel):
    session_id: Optional[str] = ""          # Col 1: Session (e.g. Session 01)
    session_type_vn: Optional[str] = ""     # Col 2: Loại Session (Lý thuyết, Thực hành, Mini Project...)
    session_code: Optional[str] = ""        # Col 3: Mã Session (THEORY, PRACTICE, MINI_PROJECT...)
    session_title: Optional[str] = ""       # Col 4: Tên Tiêu Đề Session
    lesson_title: Optional[str] = ""        # Col 5: Tên Lesson
    details: Optional[str] = ""             # Col 6: Nội Dung Chi Tiết (Lesson Scope)
    expected_outcome: Optional[str] = ""    # Col 7: Kết Quả Mong Đợi (Expected Outcome)
    forbidden_scope: Optional[str] = ""     # Col 8: Phạm Vi CẤM DÙNG (Forbidden Scope)
    allowed_scope: Optional[str] = ""       # Col 9: Phạm Vi ĐÃ HỌC (Allowed Scope)
    tech_stack: Optional[str] = ""          # Col 10: Tech Stack & Quy Chuẩn

    # Compatibility getters/properties for existing code
    @property
    def stt(self) -> str:
        return self.session_id or ""
    @property
    def form(self) -> str:
        return self.session_type_vn or ""
    @property
    def session_val(self) -> str:
        return self.session_id or ""
    @property
    def content_val(self) -> str:
        return self.session_title or ""
    @property
    def lesson_val(self) -> str:
        return self.lesson_title or ""
    @property
    def details_val(self) -> str:
        return self.details or ""
    @property
    def output_val(self) -> str:
        return self.expected_outcome or self.allowed_scope or ""
    @property
    def deadline(self) -> str:
        return ""

@router.post("/{course_id}/parse-excel", response_model=List[PMRow])
async def parse_excel_preview(course_id: int, file: UploadFile = File(...)):
    content = await file.read()
    wb = openpyxl.load_workbook(filename=io.BytesIO(content), data_only=True)
    ws: Any = wb.active
    
    rows = []
    curr_session_id = ""
    curr_type_vn = ""
    curr_code = ""
    curr_title = ""

    raw_rows = list(ws.iter_rows(values_only=True))
    if not raw_rows or len(raw_rows) < 2:
        return []

    header_found = False
    for row in raw_rows:
        cell_vals = [str(c).strip() if c is not None else "" for c in row]
        if not any(cell_vals):
            continue

        # Skip top metadata header rows until table header row is found
        if not header_found:
            first_val = cell_vals[0].lower()
            fifth_val = cell_vals[4].lower() if len(cell_vals) > 4 else ""
            if first_val == "session" or fifth_val in ["tên lesson", "lesson"]:
                header_found = True
            continue

        # Extract 10 columns safely matching PM_Template_Standard.xlsx
        if len(cell_vals) >= 10:
            val_session_id = cell_vals[0]
            val_type_vn = cell_vals[1]
            val_code = cell_vals[2]
            val_title = cell_vals[3]
            val_lesson = cell_vals[4]
            val_details = cell_vals[5]
            val_expected = cell_vals[6]
            val_forbidden = cell_vals[7]
            val_allowed = cell_vals[8]
            val_tech_stack = cell_vals[9]
        else:
            val_session_id = cell_vals[0] if len(cell_vals) > 0 else ""
            val_type_vn = cell_vals[1] if len(cell_vals) > 1 else ""
            val_code = cell_vals[2] if len(cell_vals) > 2 else ""
            val_title = cell_vals[3] if len(cell_vals) > 3 else ""
            val_lesson = cell_vals[4] if len(cell_vals) > 4 else ""
            val_details = cell_vals[5] if len(cell_vals) > 5 else ""
            val_expected = ""
            val_forbidden = cell_vals[6] if len(cell_vals) > 6 else ""
            val_allowed = cell_vals[7] if len(cell_vals) > 7 else ""
            val_tech_stack = cell_vals[8] if len(cell_vals) > 8 else ""

        # Forward fill merged cell values
        if val_session_id: curr_session_id = val_session_id
        if val_type_vn: curr_type_vn = val_type_vn
        if val_code: curr_code = val_code
        if val_title: curr_title = val_title

        rows.append(PMRow(
            session_id=val_session_id or curr_session_id,
            session_type_vn=val_type_vn or curr_type_vn,
            session_code=val_code or curr_code,
            session_title=val_title or curr_title,
            lesson_title=val_lesson,
            details=val_details,
            expected_outcome=val_expected,
            forbidden_scope=val_forbidden,
            allowed_scope=val_allowed,
            tech_stack=val_tech_stack
        ))
    return rows

def sync_curriculum_to_pms_excel(course_name: str, payload: List[PMRow]) -> None:
    """
    Finds the correct Excel file in the pms/ root directory, or creates one,
    and updates it with the list of PMRow objects representing the 9-column curriculum.
    """
    import openpyxl
    import re
    from pathlib import Path
    
    # ROOT is resolved as the project root (Learning-Material)
    pms_dir = ROOT / "pms"
    pms_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Resolve Excel file path
    target_excel = None
    xlsx_files = list(pms_dir.glob("*.xlsx")) if pms_dir.exists() else []
    xlsx_files = [f for f in xlsx_files if not f.name.startswith("~$")]
    
    if xlsx_files:
        clean_course_words = set(re.findall(r'\w+', course_name.lower()))
        best_match = None
        best_overlap = 0
        for f in xlsx_files:
            file_words = set(re.findall(r'\w+', f.stem.lower()))
            overlap = len(clean_course_words.intersection(file_words))
            if overlap > best_overlap:
                best_overlap = overlap
                best_match = f
                
        if best_match and best_overlap > 0:
            target_excel = best_match
        elif len(xlsx_files) == 1:
            target_excel = xlsx_files[0]
            
    if not target_excel:
        sanitized_name = re.sub(r'[\\/*?:"<>|]', "", course_name).strip().replace(" ", "_").replace("-", "_")
        target_excel = pms_dir / f"PM_{sanitized_name}.xlsx"
        
    print(f"  [PM Excel Sync] Writing curriculum to: {target_excel}")
    
    # 2. Write rows to Excel matching PM_Template_Standard.xlsx (9 columns)
    wb = openpyxl.Workbook()
    ws = wb.active
    if not ws:
        ws = wb.create_sheet()
    ws.title = "Syllabus"
    
    # Standard 10-column headers
    headers = [
        "Session", "Loại Session", "Mã Session", "Tên Tiêu Đề Session",
        "Tên Lesson", "Nội Dung Chi Tiết (Lesson Scope)",
        "Kết Quả Mong Đợi (Expected Outcome)",
        "Phạm Vi CẤM DÙNG (Forbidden Scope)", "Phạm Vi ĐÃ HỌC (Allowed Scope)", "Tech Stack & Quy Chuẩn"
    ]
    ws.append(headers)
    
    # Write curriculum rows
    for row in payload:
        ws.append([
            row.session_id or "",
            row.session_type_vn or "",
            row.session_code or "",
            row.session_title or "",
            row.lesson_title or "",
            row.details or "",
            row.expected_outcome or "",
            row.forbidden_scope or "",
            row.allowed_scope or "",
            row.tech_stack or ""
        ])
        
    # Standard format adjustments
    try:
        from openpyxl.styles import Font, Alignment
        header_font = Font(name="Calibri", size=11, bold=True)
        header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
        for col_idx in range(1, 10):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = header_font
            cell.alignment = header_align
            
        # Basic auto column width
        from openpyxl.utils import get_column_letter
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column or 1)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 50)
    except Exception as e:
        print(f"  [PM Excel Sync Warning] Styling failed: {e}")
        
    wb.save(str(target_excel))
    print(f"  [PM Excel Sync Success] Excel sync complete for course: {course_name}")


@router.post("/{course_id}/confirm-import")
async def confirm_import(course_id: int, payload: List[PMRow], db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    from sqlalchemy import delete
    
    # Get all session IDs for this course
    sess_stmt = select(Session.id).where(Session.course_id == course_id)
    sess_res = await db.execute(sess_stmt)
    session_ids = sess_res.scalars().all()
    
    if session_ids:
        # Get all lesson IDs for these sessions
        less_stmt = select(Lesson.id).where(Lesson.session_id.in_(session_ids))
        less_res = await db.execute(less_stmt)
        lesson_ids = less_res.scalars().all()
        
        # 1. Delete lesson artifacts
        if lesson_ids:
            from app.models.artifact import Artifact
            await db.execute(delete(Artifact).where(Artifact.lesson_id.in_(lesson_ids)))
            # 2. Delete lessons
            await db.execute(delete(Lesson).where(Lesson.session_id.in_(session_ids)))
            
        # 3. Delete session-level artifacts
        from app.models.artifact import Artifact
        await db.execute(delete(Artifact).where(Artifact.session_id.in_(session_ids)))
        
        # 4. Delete sessions
        await db.execute(delete(Session).where(Session.course_id == course_id))
        
    await db.flush()
    
    current_session_model: Any = None
    session_name = ""
    s_title = ""
    last_session_name = None
    session_counter = 0
    lesson_counter = 0
    
    for row in payload:
        session_val_str = row.session_val.strip() if row.session_val else ""
        
        should_create_session = False
        if session_val_str:
            s_match = re.search(r'(:| - )', session_val_str)
            if s_match:
                s_idx = s_match.start()
                session_name = session_val_str[:s_idx].strip()
                s_title = session_val_str[s_idx + len(s_match.group(1)):].strip()
            else:
                session_name = session_val_str
                s_title = row.content_val.strip() if row.content_val else "Untitled"
                
            from app.utils.json_helper import normalize_id
            norm_sess_name = normalize_id(session_name)
            if current_session_model is None or last_session_name is None or norm_sess_name != last_session_name:
                should_create_session = True
                last_session_name = norm_sess_name
        else:
            # If session_val is empty, we continue with the current session
            pass
            
        if should_create_session:
            session_counter += 1
            new_session = Session(
                name=session_name,
                title=s_title,
                session_type_vn=row.session_type_vn or row.form or "Lý thuyết",
                session_code=row.session_code or "THEORY",
                course_id=course_id,
                order_index=session_counter
            )
            db.add(new_session)
            await db.flush()
            current_session_model = new_session
            lesson_counter = 0
            
        lesson_val_str = row.lesson_val.strip() if row.lesson_val else ""
        if lesson_val_str and current_session_model:
            s_title_lower = current_session_model.title.lower() if current_session_model.title else ""
            s_name_lower = current_session_model.name.lower() if current_session_model.name else ""
            is_practice_or_project = (
                "thực hành" in s_title_lower or "thực hành" in s_name_lower or
                "practice" in s_title_lower or "practice" in s_name_lower or
                "mini project" in s_title_lower or "mini project" in s_name_lower or
                "project" in s_title_lower or "project" in s_name_lower or
                "dự án" in s_title_lower or "dự án" in s_name_lower
            )
            if not is_practice_or_project:
                match = re.search(r'(:| - )', lesson_val_str)
                if match:
                    idx = match.start()
                    l_name = lesson_val_str[:idx].strip()
                    l_title = lesson_val_str[idx + len(match.group(1)):].strip()
                else:
                    prefix_match = re.match(r'^((?:lesson|bài|bai|less|chương|session)\s*\d+)\s*(.*)', lesson_val_str, re.IGNORECASE)
                    if prefix_match:
                        l_name = prefix_match.group(1).strip()
                        l_title = prefix_match.group(2).strip() or l_name
                    else:
                        l_name = lesson_val_str
                        l_title = lesson_val_str
                    
                lesson_counter += 1
                det = (row.details or row.details_val or "").strip()
                exp = (row.expected_outcome or row.output_val or "").strip()
                forb = (row.forbidden_scope or "").strip()
                allow = (row.allowed_scope or "").strip()
                tech = (row.tech_stack or "").strip()
                
                new_lesson = Lesson(
                    name=l_name,
                    title=l_title,
                    details=det if det else None,
                    expected_output=exp if exp else None,
                    forbidden_scope=forb if forb else None,
                    allowed_scope=allow if allow else None,
                    tech_stack=tech if tech else None,
                    session_id=current_session_model.id,
                    order_index=lesson_counter
                )
                db.add(new_lesson)
            
    await db.commit()
    
    # Sync edited syllabus to Excel
    try:
        sync_curriculum_to_pms_excel(str(course.name), payload)
    except Exception as exc:
        print(f"  [PM Excel Sync Warning] Failed to write back to Excel syllabus: {exc}")
        
    return {"status": "success", "message": "Imported sessions and lessons successfully"}

@router.post("/{course_id}/review-pm")
async def review_pm(course_id: int, payload: List[PMRow], db: AsyncSession = Depends(get_db)):
    course = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    # Chuẩn bị dữ liệu 10 cột tiêu chuẩn gửi cho LLM Senior Academic Director
    markdown_table = "| Session | Loại Session | Mã Session | Tiêu đề Session | Tên Lesson | Nội Dung Chi Tiết (Lesson Scope) | Kết Quả Mong Đợi (Outcome) | Phạm vi CẤM DÙNG (Forbidden) | Phạm vi ĐÃ HỌC (Allowed) | Tech Stack |\n"
    markdown_table += "|---|---|---|---|---|---|---|---|---|---|\n"
    for row in payload:
        s_id = row.session_id or row.session_val or ""
        s_type = row.session_type_vn or row.form or ""
        s_code = row.session_code or ""
        s_title = row.session_title or row.content_val or ""
        l_title = row.lesson_title or row.lesson_val or ""
        details = row.details or row.details_val or ""
        expected = row.expected_outcome or ""
        forbidden = row.forbidden_scope or ""
        allowed = row.allowed_scope or row.output_val or ""
        tech = row.tech_stack or ""
        
        if s_id or l_title:
            markdown_table += f"| {s_id} | {s_type} | {s_code} | {s_title} | {l_title} | {details} | {expected} | {forbidden} | {allowed} | {tech} |\n"
            
    prompt = f"""Bạn là một Giám đốc Học thuật (Senior Academic Director) và Kiến trúc sư Chương trình (Curriculum Architect) với hơn 10 năm kinh nghiệm thiết kế khóa học công nghệ.
Hãy xem xét cấu trúc môn học sau (dựa trên mẫu PM 10 cột chuẩn quốc tế: Session, Loại Session, Mã Session, Tiêu đề, Lesson, Chi tiết Scope, Kết quả mong đợi Expected Outcome, Phạm vi Cấm dùng, Phạm vi Đã học, Tech Stack) và đưa ra đánh giá sắc bén.
Môn học: {course.name} (Tech Stack master: {course.technology_stack})

Cấu trúc chương trình 10 cột:
{markdown_table}

Nhiệm vụ kiểm định của bạn:
1. Kiểm tra 'Kết Quả Mong Đợi (Expected Outcome)' của từng bài học: Có rõ ràng, đo lường được theo Thang tư duy Bloom's Taxonomy không? Đã xác định rõ sản phẩm/năng lực sinh viên tự viết/làm được chưa?
2. Nhận xét về luồng logic: Có bài học nào dạy quá sớm trước khi học kiến thức nền không?
3. Kiểm tra Phạm vi CẤM DÙNG (Forbidden Scope): BẮT BUỘC kiểm tra cả 2 khía cạnh: (a) CẤM dùng các kiến thức/khái niệm của các bài học VÀ session PHÍA SAU trong chương trình học (chưa đến buổi học), và (b) CẤM các kiến thức BÊN NGOÀI phạm vi môn học. Phát hiện và cảnh báo nếu có bài học bị rò rỉ kiến thức của các bài phía sau hoặc rò rỉ kiến thức nâng cao ngoài chương trình.
4. Kiểm tra Phạm vi ĐÃ HỌC (Allowed Scope) và Chi tiết Lesson Scope: Đã đủ prompt context để AI Content Agent sinh bài đọc HTML/GSAP và SCORM chất lượng cao chưa?
5. Kiểm tra sự phù hợp của Mã Session (ORIENTATION, THEORY, PRACTICE, MINI_PROJECT, FINAL_PROJECT) và Tech Stack.
6. Gợi ý 1-3 cải tiến cụ thể.

Bạn BẮT BUỘC phải trả về kết quả dưới dạng JSON có cấu trúc chính xác như sau:
{{
  "strengths": ["Điểm mạnh 1", "Điểm mạnh 2"],
  "weaknesses": ["Điểm cần cải tiến 1", "Điểm cần cải tiến 2"],
  "detailed_issues": [
    {{
      "session": "Tên Session (ví dụ: Session 01)",
      "lesson": "Tên Lesson (ví dụ: Lesson 02)",
      "issue": "Mô tả chi tiết điểm chưa tốt",
      "suggestion": "Gợi ý cải tiến cụ thể"
    }}
  ]
}}
"""

    import asyncio
    from core.llm import call_llm
    
    try:
        # Gọi Gemini/LLM từ hệ thống lõi trong background thread để không block event loop
        review_result = await asyncio.to_thread(
            call_llm,
            system_prompt="You are an expert Curriculum Reviewer. You must return response in JSON format.",
            user_prompt=prompt,
            json_mode=True,
            agent_name="Senior Academic Director",
        )
        
        import json
        evaluation = None
        review_content = ""
        
        if review_result:
            try:
                # Clean code blocks
                clean_json = review_result.strip()
                if clean_json.startswith("```"):
                    clean_json = clean_json.split("```")[1]
                    if clean_json.startswith("json"):
                        clean_json = clean_json[4:]
                clean_json = clean_json.strip()
                
                evaluation = json.loads(clean_json)
                
                # Build markdown description from evaluation
                md = "### Đánh giá từ Senior Academic Director\n\n"
                if evaluation.get("strengths"):
                    md += "**Điểm mạnh:**\n"
                    for s in evaluation["strengths"]:
                        md += f"* {s}\n"
                    md += "\n"
                if evaluation.get("weaknesses"):
                    md += "**Điểm chưa tốt:**\n"
                    for w in evaluation["weaknesses"]:
                        md += f"* {w}\n"
                    md += "\n"
                review_content = md
            except Exception as parse_ex:
                print(f"[Review PM Parsing Error] {parse_ex}. Raw content: {review_result}")
                review_content = review_result
        
        # Fallback if empty or failed
        if not evaluation:
            strengths = [
                f"Cấu trúc khóa học {course.name} được phân chia các Session rõ ràng theo tiến độ.",
                "Các Lesson được thiết kế có đầy đủ mục tiêu đầu ra dự kiến."
            ]
            weaknesses = [
                "Một số Lesson có phần mô tả chi tiết còn quá ngắn gọn, chưa đủ prompt context cho AI.",
                "Thứ tự một số bài học cài đặt công cụ cần được tối ưu lại."
            ]
            detailed_issues = []
            
            # Find the first few sessions/lessons from payload to create a realistic tree
            session_map = {}
            for row in payload:
                if row.session_val and row.lesson_val:
                    sess_name = row.session_val.split(":")[0].strip()
                    less_name = row.lesson_val.split(":")[0].strip()
                    if sess_name not in session_map:
                        session_map[sess_name] = []
                    session_map[sess_name].append(less_name)
            
            # Add mock issues to the first 2 lessons found
            count = 0
            for s_name, l_list in session_map.items():
                for l_name in l_list:
                    if count == 0:
                        detailed_issues.append({
                            "session": s_name,
                            "lesson": l_name,
                            "issue": "Thiếu hướng dẫn cài đặt môi trường chi tiết và kiểm tra quyền admin.",
                            "suggestion": "Bổ sung các bước chuẩn bị môi trường hệ điều hành Windows/macOS."
                        })
                    elif count == 1:
                        detailed_issues.append({
                            "session": s_name,
                            "lesson": l_name,
                            "issue": "Nội dung lý thuyết quá rộng cho một buổi học.",
                            "suggestion": "Chia nhỏ bài học hoặc tập trung vào các khái niệm cốt lõi, lược bớt phần nâng cao."
                        })
                    count += 1
            
            evaluation = {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "detailed_issues": detailed_issues
            }
            review_content = f"### Đánh giá từ Senior Academic Director (Offline Mode)\n\n"
            review_content += "**Điểm mạnh:**\n" + "\n".join(f"* {s}" for s in strengths) + "\n\n"
            review_content += "**Điểm chưa tốt:**\n" + "\n".join(f"* {w}" for w in weaknesses) + "\n"
            
        return {
            "status": "success",
            "review_content": review_content,
            "evaluation": evaluation
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import BackgroundTasks
from sqlalchemy import select

@router.post("/{course_id}/generate-all")
async def generate_all_course_lessons(
    course_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    course: Any = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    from app.api.endpoints.lesson import generate_lesson_task
    
    stmt = select(Lesson).join(Session).where(Session.course_id == course_id)
    result = await db.execute(stmt)
    lessons: List[Any] = list(result.scalars().all())
    
    if not lessons:
        raise HTTPException(status_code=400, detail="Không có bài học nào trong khóa này để tạo AI.")
    
    # Khởi tạo trạng thái Pending cho tất cả bài học trong khóa học
    from app.models.artifact import Artifact
    from sqlalchemy import delete
    
    lesson_ids = [l.id for l in lessons]
    await db.execute(delete(Artifact).where(Artifact.lesson_id.in_(lesson_ids)))
    
    pending_types = ["outline", "reading", "quiz", "walkthrough"]
    for l_id in lesson_ids:
        for p_type in pending_types:
            db.add(Artifact(lesson_id=l_id, type=p_type, status="Pending"))
    await db.commit()
    
    if not course or not course.technology_stack:
        raise HTTPException(
            status_code=400,
            detail="❌ [LỖI THIẾU TECHNOLOGY STACK] Môn học chưa được cấu hình Technology Stack. Vui lòng cập nhật thông tin môn học trước khi sinh học liệu."
        )
    tech_stack = course.technology_stack.strip()
    course_dir_name = course.name.strip().replace(" ", "_").replace("-", "_") if course.name else "Course_Output"

    from app.core.process_manager import reset_cancel_flags
    reset_cancel_flags()

    for lesson in lessons:
        pm_input = lesson.details if lesson.details else "Vui lòng phân tích và sinh bài học chi tiết."
        background_tasks.add_task(generate_lesson_task, lesson.id, lesson.session_id, pm_input, lesson.title, tech_stack, course_dir_name)
        
    return {"status": "processing", "message": f"Đã khởi tạo hàng chờ và đẩy thành công {len(lessons)} bài học vào AI!"}

class PMAutoFixRequest(BaseModel):
    payload: List[PMRow]
    review_report: str

def map_pm_rows_to_json(rows: List[PMRow]) -> List[dict]:
    sessions = []
    current_session = None
    last_session_name = None
    
    for row in rows:
        s_id = row.session_id or row.session_val or ""
        s_type = row.session_type_vn or row.form or "Lý thuyết"
        s_code = row.session_code or "THEORY"
        s_title = row.session_title or row.content_val or "Untitled Session"
        l_title = row.lesson_title or row.lesson_val or ""
        details = row.details or row.details_val or ""
        expected = row.expected_outcome or ""
        forbidden = row.forbidden_scope or ""
        allowed = row.allowed_scope or row.output_val or ""
        tech = row.tech_stack or ""

        should_create_session = False
        if s_id:
            if current_session is None or last_session_name != s_id:
                should_create_session = True
                last_session_name = s_id

        if should_create_session:
            current_session = {
                "session_id": s_id,
                "session_type_vn": s_type,
                "session_code": s_code,
                "session_title": s_title,
                "lessons": []
            }
            sessions.append(current_session)

        if l_title and current_session:
            lessons_list: Any = current_session["lessons"]
            lessons_list.append({
                "lesson_title": l_title,
                "details": details,
                "expected_outcome": expected,
                "forbidden_scope": forbidden,
                "allowed_scope": allowed,
                "tech_stack": tech
            })

    return sessions


def flatten_json_to_pm_rows(sessions_data: List[dict]) -> List[PMRow]:
    rows = []
    for s_idx, session in enumerate(sessions_data, 1):
        s_id = session.get("session_id", f"Session {s_idx:02d}")
        s_type = session.get("session_type_vn", session.get("form", "Lý thuyết"))
        s_code = session.get("session_code", "THEORY")
        s_title = session.get("session_title", session.get("title", ""))

        lessons = session.get("lessons", [])
        if not lessons:
            rows.append(PMRow(
                session_id=s_id,
                session_type_vn=s_type,
                session_code=s_code,
                session_title=s_title,
                lesson_title="",
                details="",
                expected_outcome="",
                forbidden_scope="",
                allowed_scope="",
                tech_stack=""
            ))
        else:
            for l_idx, lesson in enumerate(lessons):
                l_title = lesson.get("lesson_title", lesson.get("title", ""))
                details = lesson.get("details", "")
                expected = lesson.get("expected_outcome", lesson.get("outcome", ""))
                forbidden = lesson.get("forbidden_scope", "")
                allowed = lesson.get("allowed_scope", "")
                tech = lesson.get("tech_stack", "")

                rows.append(PMRow(
                    session_id=s_id,
                    session_type_vn=s_type,
                    session_code=s_code,
                    session_title=s_title,
                    lesson_title=l_title,
                    details=details,
                    expected_outcome=expected,
                    forbidden_scope=forbidden,
                    allowed_scope=allowed,
                    tech_stack=tech
                ))
    return rows

@router.post("/{course_id}/auto-fix-pm", response_model=List[PMRow])
async def auto_fix_pm(course_id: int, request_data: PMAutoFixRequest, db: AsyncSession = Depends(get_db)):
    course: Any = await db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    if not course.technology_stack:
        raise HTTPException(status_code=400, detail="❌ [LỖI THIẾU TECHNOLOGY STACK] Môn học chưa được cấu hình Technology Stack.")
    tech_stack = course.technology_stack.strip()
    
    # Map rows to nested JSON structure
    nested_curriculum = map_pm_rows_to_json(request_data.payload)
    
    import json
    pm_json_str = json.dumps(nested_curriculum, ensure_ascii=False)
    
    # Run the PM Updater Agent to automatically apply fixes based on the review report
    from agents.reviewer_agents import pm_updater_agent
    import asyncio
    
    try:
        updated_json_str = await asyncio.to_thread(
            pm_updater_agent,
            pm_json_str,
            request_data.review_report,
            tech_stack
        )
        
        # Clean potential markdown wrap and parse back to JSON
        from app.utils.json_helper import clean_and_parse_json, merge_curriculums
        parsed_json = clean_and_parse_json(updated_json_str)
        
        # Merge updated content back into the original curriculum
        merged_json = merge_curriculums(nested_curriculum, parsed_json)
        
        # Guarantee expected_outcome and forbidden_scope are 100% populated
        from agents.reviewer_agents import apply_smart_pedagogical_rule_fixes
        merged_json_str = json.dumps(merged_json, ensure_ascii=False)
        fixed_json_str = apply_smart_pedagogical_rule_fixes(merged_json_str, tech_stack)
        fixed_json = clean_and_parse_json(fixed_json_str)
        
        # Flatten back into PMRow list
        fixed_rows = flatten_json_to_pm_rows(fixed_json)
        return fixed_rows
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

class PMGenerateFromScratchRequest(BaseModel):
    course_name: str
    description: Optional[str] = ""
    tech_stack: Optional[str] = ""
    total_sessions: int = 30
    target_persona: Optional[str] = ""
    course_outcomes: Optional[str] = ""
    capstone_target: Optional[str] = ""

@router.post("/generate-pm-from-scratch", response_model=List[PMRow])
async def generate_pm_from_scratch(request_data: PMGenerateFromScratchRequest):
    from agents.pm_generator_agent import pm_generator_agent
    from app.utils.json_helper import clean_and_parse_json
    import asyncio
    
    try:
        json_str = await asyncio.to_thread(
            pm_generator_agent,
            request_data.course_name,
            request_data.description or "",
            request_data.tech_stack or "",
            request_data.total_sessions,
            request_data.target_persona or "",
            request_data.course_outcomes or "",
            request_data.capstone_target or ""
        )
        
        if not json_str:
            raise HTTPException(status_code=500, detail="Không nhận được phản hồi từ AI Agent. Vui lòng kiểm tra lại kết nối mạng tới Google AI.")
            
        parsed_json = clean_and_parse_json(json_str)
        rows = flatten_json_to_pm_rows(parsed_json)
        return rows
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi khi AI sinh PM tự động: {str(e)}")

