import random
import re
import json
from typing import List, Dict, Any

def shuffle_options_and_explanations(q: Dict[str, Any]) -> None:
    """Randomly shuffles the 4 multiple-choice options and their corresponding explanations, updating isCorrect index (1 to 4)."""
    options = [
        (q.get("answer_1", ""), q.get("explanation_answer_1", ""), 1 == q.get("isCorrect", 1)),
        (q.get("answer_2", ""), q.get("explanation_answer_2", ""), 2 == q.get("isCorrect", 1)),
        (q.get("answer_3", ""), q.get("explanation_answer_3", ""), 3 == q.get("isCorrect", 1)),
        (q.get("answer_4", ""), q.get("explanation_answer_4", ""), 4 == q.get("isCorrect", 1))
    ]
    random.shuffle(options)
    for idx, (ans, exp, is_correct) in enumerate(options, 1):
        q[f"answer_{idx}"] = ans
        q[f"explanation_answer_{idx}"] = exp
        if is_correct:
            q["isCorrect"] = idx

FORBIDDEN_QUIZ_REFERRAL_PATTERNS = [
    r"\bở slide\b", r"\btrong slide\b", r"\bslide bài giảng\b", r"\bslide đề cập\b",
    r"\btrong bài giảng\b", r"\btheo bài giảng\b", r"\btheo video\b", r"\btrong video\b",
    r"\btừ lời giảng viên\b", r"\btheo lời giảng viên\b", r"\btheo phần \d+\b", r"\btrong bài đọc\b",
    r"\bkịch bản doanh nghiệp technova\b", r"\bdoanh nghiệp technova\b", r"\btechnova\b",
    r"\btừ một nguồn nào đó không rõ\b", r"\btrong kịch bản\b"
]

def check_quiz_referral_violations(text: str) -> List[str]:
    text_lower = text.lower()
    found = []
    for pattern in FORBIDDEN_QUIZ_REFERRAL_PATTERNS:
        if re.search(pattern, text_lower):
            clean_name = pattern.replace(r"\b", "").replace(r"\d+", "X")
            if clean_name not in found:
                found.append(clean_name)
    return found

def generate_quiz_batch_via_llm(
    topic_name: str,
    tech_stack: str,
    count: int,
    difficulty: int,
    category: str,
    start_stt: int,
    forbidden_scope: str = "",
    allowed_scope: str = ""
) -> List[Dict[str, Any]]:
    """Generates a batch of quiz questions via LLM using RAG content from local Vector DB and dynamic PM scope constraints."""
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise RuntimeError("LLM API Key is missing. Cannot generate quiz dynamically.")
        
    from core.llm import call_llm
    from core.skills import load_skill_content
    from core.vector_store import get_vector_store
    
    rag_context = ""
    try:
        store = get_vector_store()
        matches = store.query(topic_name, k=3)
        if matches:
            rag_context = "\nNgữ cảnh tham chiếu từ Vector DB:\n" + "\n".join([m["text"] for m in matches])
    except Exception as e:
        print(f"  [Quiz Engine] Info: Could not load vector context - {e}")
        
    skill_content = load_skill_content("quizz_session")
    
    # Extract scope directives dynamically from PM without any hardcoded language keywords
    scope_prompt_rules = []
    if allowed_scope:
        scope_prompt_rules.append(f"PHẠM VI KIẾN THỨC ĐÃ HỌC TỪ PM MÔN HỌC (ALLOWED SCOPE): {allowed_scope}.")
        scope_prompt_rules.append("Nội dung câu hỏi và mã mẫu chỉ được phép sử dụng các kiến thức nằm trong phạm vi đã học này.")
    if forbidden_scope:
        scope_prompt_rules.append(f"PHẠM VI CẤM DÙNG TỪ PM HỌC PHẦN (FORBIDDEN SCOPE): {forbidden_scope}.")
        scope_prompt_rules.append("TUYỆT ĐỐI CẤM đưa bất kỳ khái niệm, cú pháp, đối tượng, phương thức hay thư viện nào thuộc PHẠM VI CẤM DÙNG trên vào câu hỏi, đáp án hay phần giải thích.")

    scope_prompt_formatted = "\n".join(scope_prompt_rules)

    questions = []
    remaining = count
    current_stt = start_stt
    max_sub_batch = 3
    
    while remaining > 0:
        sub_count = min(max_sub_batch, remaining)
        sub_qs = []
        
        system_prompt = f"""You are a strict E-Learning Assessment Specialist at Rikkei Education.
Your task is to generate EXACTLY {sub_count} high-quality multiple-choice questions for topic '{topic_name}' using tech stack '{tech_stack}'.

=== 9 MANDATORY QUESTION CONTENT REQUIREMENTS (CRITICAL) ===
1. Professional Significance: 100% of question content MUST have clear technical value, directly targeting core concepts or practical developer scenarios taught in the lesson.
2. Anti-Generic (Non-Googleable): ABSOLUTELY FORBIDDEN to ask generic outside trivia that students can easily Google without studying the course.
3. Concrete Scenario-Based: Questions MUST revolve around concrete technical examples or practical real-world developer situations present in the lesson.
4. STRICT PROHIBITION OF CONTEXT/SOURCE REFERRAL PHRASES (CRITICAL):
   - ABSOLUTELY FORBIDDEN to use intermediate context or source referral phrases in questions, answer choices, or explanations: "in the slide", "on slide", "lecture slide", "slide mentions", "in the lecture", "according to the lecture", "according to the video", "in the video", "from the instructor", "instructor said", "According to Section ...", "in enterprise scenario ...", "in the scenario", "from an unknown source", etc.
   - All questions, options, and explanations MUST be stated 100% objectively, independently, and professionally as standard domain knowledge.
5. Sophisticated Distractors: Incorrect options MUST be designed based on common student misconceptions or subtle syntax traps. FORBIDDEN options: "All of the above are correct" or "All of the above are incorrect".
6. Option Homogeneity (Equal Length): All 4 choices (A, B, C, D) MUST have comparable text length, grammatical structure, and detail level.
7. Metadata Specs: Starting STT: {current_stt}. Difficulty: {difficulty} (scale 1-10). Category: "{category}".
8. Code Formatting: Wrap all code snippets/identifiers in Markdown code fences (```).
9. Detailed Objective Explanations: Provide detailed technical explanations for why the correct answer is right and why distractors are wrong (stated objectively without source referral phrases).
10. TARGET OUTPUT LANGUAGE: 100% Accented Vietnamese (Tiếng Việt có dấu chuẩn sản xuất) for question content, options, and explanations.

DYNAMIC KNOWLEDGE BOUNDARY RULES:
{scope_prompt_formatted}

Output Format Requirement:
Return ONLY a raw JSON array containing exactly {sub_count} objects matching this schema:
[
  {{
    "STT": {current_stt},
    "question_content": "Nội dung câu hỏi tình huống thực tế...",
    "answer_1": "Đáp án đúng A",
    "explanation_answer_1": "Giải thích chi tiết vì sao A đúng...",
    "answer_2": "Đáp án nhiễu B",
    "explanation_answer_2": "Phân tích vì sao B sai...",
    "answer_3": "Đáp án nhiễu C",
    "explanation_answer_3": "Phân tích vì sao C sai...",
    "answer_4": "Đáp án nhiễu D",
    "explanation_answer_4": "Phân tích vì sao D sai...",
    "isCorrect": 1,
    "difficulty": {difficulty},
    "category": "{category}"
  }}
]
Always place the correct answer in 'answer_1' and set 'isCorrect' to 1. The engine will shuffle options randomly at post-processing.
Do NOT wrap output in markdown code fences. Return raw JSON string only.
"""
        
        user_prompt = f"Hãy tạo đúng {sub_count} câu hỏi trắc nghiệm định dạng JSON chuẩn xác."
        
        success = False
        for attempt in range(3):
            try:
                response = call_llm(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    agent_name=f"Session_Quiz_Agent_Att{attempt+1}",
                    session_id=category,
                    lesson_id=topic_name
                )
                
                if not response:
                    continue
                    
                clean_json = response.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json.split("```json", 1)[1]
                if clean_json.endswith("```"):
                    clean_json = clean_json.rsplit("```", 1)[0]
                clean_json = clean_json.strip()
                
                qs = json.loads(clean_json)
                if isinstance(qs, list) and len(qs) == sub_count:
                    # 100% Dynamic Scope Audit & Referral Violations Check
                    from core.scope_calculator import validate_text_against_scope
                    
                    forbidden_set = set(item.strip() for item in re.split(r'[,;\n/•\-]', forbidden_scope) if item.strip()) if forbidden_scope else set()
                    
                    is_valid = True
                    for q in qs:
                        q_str = json.dumps(q, ensure_ascii=False)
                        violations = validate_text_against_scope(q_str, forbidden_set)
                        if violations:
                            print(f"  [Quiz Dynamic Scope Audit] REJECTED sub-batch attempt {attempt+1}: Vi phạm khái niệm cấm từ PM ({', '.join(violations)}).")
                            is_valid = False
                            break
                            
                        ref_violations = check_quiz_referral_violations(q_str)
                        if ref_violations:
                            print(f"  [Quiz Referral Audit] REJECTED sub-batch attempt {attempt+1}: Chứa từ ngữ tham chiếu bối cảnh cấm ({', '.join(ref_violations)}).")
                            is_valid = False
                            break

                    if not is_valid:
                        continue

                    for idx, q in enumerate(qs):
                        q["STT"] = current_stt + idx
                        q["difficulty"] = difficulty
                        q["category"] = category
                        if "isCorrect" not in q:
                            q["isCorrect"] = 1
                    sub_qs = qs
                    success = True
                    break
                else:
                    print(f"  [Session Quiz Agent] Attempt {attempt+1} got wrong number of questions: {len(qs) if isinstance(qs, list) else 'not a list'} instead of {sub_count}")
            except Exception as e:
                print(f"  [Session Quiz Agent] Attempt {attempt+1} failed to generate {sub_count} questions: {e}.")
                
        if not success:
            print(f"  [Session Quiz Agent Warning] Sub-batch of {sub_count} questions could not pass strict scope validation after 3 attempts. Accepting best attempt.")
            if 'qs' in locals() and isinstance(qs, list) and len(qs) == sub_count:
                for idx, q in enumerate(qs):
                    q["STT"] = current_stt + idx
                    q["difficulty"] = difficulty
                    q["category"] = category
                    if "isCorrect" not in q:
                        q["isCorrect"] = 1
                sub_qs = qs
            else:
                return []
            
        questions.extend(sub_qs)
        remaining -= sub_count
        current_stt += sub_count
        
    return questions

def generate_entrance_quiz(
    session_id: str,
    current_topic: str,
    previous_topic: str,
    tech_stack: str,
    forbidden_scope: str = "",
    allowed_scope: str = ""
) -> List[Dict[str, Any]]:
    """Generates a 45-question Entrance Quiz dynamically via LLM Agent under PM dynamic scope constraints."""
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] generate_entrance_quiz: Yêu cầu tham số tech_stack hợp lệ.")
    print(f"  [Quiz Engine] Generating 45-question Entrance Quiz via Agent for stack: {tech_stack}...")
    questions = []
    
    batches = [
        {"topic": previous_topic, "count": 12, "diff": 4, "cat": "BÀI CŨ"},
        {"topic": previous_topic, "count": 9, "diff": 6, "cat": "BÀI CŨ"},
        {"topic": previous_topic, "count": 9, "diff": 8, "cat": "BÀI CŨ"},
        {"topic": current_topic, "count": 6, "diff": 5, "cat": "BÀI MỚI"},
        {"topic": current_topic, "count": 6, "diff": 7, "cat": "BÀI MỚI"},
        {"topic": current_topic, "count": 3, "diff": 9, "cat": "BÀI MỚI"}
    ]
    
    for batch in batches:
        start_stt = len(questions) + 1
        print(f"    -> Agent generating {batch['count']} questions (Diff {batch['diff']}) for '{batch['topic']}'...")
        q_batch = generate_quiz_batch_via_llm(
            topic_name=str(batch["topic"]),
            tech_stack=tech_stack,
            count=int(batch["count"]),
            difficulty=int(batch["diff"]),
            category=str(batch["cat"]),
            start_stt=start_stt,
            forbidden_scope=forbidden_scope,
            allowed_scope=allowed_scope
        )
        if q_batch:
            questions.extend(q_batch)
            
    for q in questions:
        shuffle_options_and_explanations(q)
        
    for idx, q in enumerate(questions, 1):
        q["STT"] = idx
        
    return questions

def generate_exit_quiz(
    session_id: str,
    current_topic: str,
    tech_stack: str,
    forbidden_scope: str = "",
    allowed_scope: str = ""
) -> List[Dict[str, Any]]:
    """Generates a 45-question Exit Quiz dynamically via LLM Agent under PM dynamic scope constraints."""
    if not tech_stack or not str(tech_stack).strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] generate_exit_quiz: Yêu cầu tham số tech_stack hợp lệ.")
    print(f"  [Quiz Engine] Generating 45-question Exit Quiz via Agent for stack: {tech_stack}...")
    questions = []
    
    batches = [
        {"topic": current_topic, "count": 18, "diff": 6, "cat": "BÀI MỚI"},
        {"topic": current_topic, "count": 15, "diff": 10, "cat": "BÀI MỚI"},
        {"topic": current_topic, "count": 12, "diff": 11, "cat": "BÀI MỚI"}
    ]
    
    for batch in batches:
        start_stt = len(questions) + 1
        print(f"    -> Agent generating {batch['count']} questions (Diff {batch['diff']}) for '{batch['topic']}'...")
        q_batch = generate_quiz_batch_via_llm(
            topic_name=str(batch["topic"]),
            tech_stack=tech_stack,
            count=int(batch["count"]),
            difficulty=int(batch["diff"]),
            category=str(batch["cat"]),
            start_stt=start_stt,
            forbidden_scope=forbidden_scope,
            allowed_scope=allowed_scope
        )
        if q_batch:
            questions.extend(q_batch)
            
    for q in questions:
        shuffle_options_and_explanations(q)
        
    for idx, q in enumerate(questions, 1):
        q["STT"] = idx
        
    return questions


def extract_15_question_entrance_exam(entrance_bank_45: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rút chính xác 15 câu hỏi bài thi Đầu giờ (Entrance Exam) cho sinh viên từ Ngân hàng 45 câu
    tuân thủ đúng tỉ lệ ma trận pedagogical ratio từ RE_Tiêu chuẩn quizz.pdf:
    - 10 câu Bài cũ: 4 Vận dụng (STT 1-12), 3 Phân tích/Debug (STT 13-21), 3 Tối ưu/Bảo mật (STT 22-30).
    - 5 câu Bài mới: 2 Thông hiểu (STT 31-36), 2 Vận dụng (STT 37-42), 1 Phân tích (STT 43-45).
    """
    if not entrance_bank_45 or len(entrance_bank_45) < 45:
        # Fallback if bank has fewer than 45 questions
        return entrance_bank_45[:15]

    old_app = entrance_bank_45[0:12]      # 12 questions
    old_dbg = entrance_bank_45[12:21]     # 9 questions
    old_opt = entrance_bank_45[21:30]     # 9 questions

    new_und = entrance_bank_45[30:36]     # 6 questions
    new_app = entrance_bank_45[36:42]     # 6 questions
    new_ana = entrance_bank_45[42:45]     # 3 questions

    selected = []
    selected.extend(random.sample(old_app, min(4, len(old_app))))
    selected.extend(random.sample(old_dbg, min(3, len(old_dbg))))
    selected.extend(random.sample(old_opt, min(3, len(old_opt))))

    selected.extend(random.sample(new_und, min(2, len(new_und))))
    selected.extend(random.sample(new_app, min(2, len(new_app))))
    selected.extend(random.sample(new_ana, min(1, len(new_ana))))

    # Re-number STT 1 to 15
    exam_15 = []
    for idx, q in enumerate(selected, 1):
        item = dict(q)
        item["STT"] = idx
        exam_15.append(item)

    return exam_15


def extract_15_question_exit_exam(exit_bank_45: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rút chính xác 15 câu hỏi bài thi Cuối giờ (Exit Exam) cho sinh viên từ Ngân hàng 45 câu bài mới
    tuân thủ đúng tỉ lệ ma trận pedagogical ratio từ RE_Tiêu chuẩn quizz.pdf:
    - 6 câu Vận dụng (STT 1-18)
    - 5 câu Phân tích / Debug (STT 19-33)
    - 4 câu Sáng tạo / Best Practice (STT 34-45)
    """
    if not exit_bank_45 or len(exit_bank_45) < 45:
        return exit_bank_45[:15]

    app_qs = exit_bank_45[0:18]    # 18 questions
    dbg_qs = exit_bank_45[18:33]   # 15 questions
    opt_qs = exit_bank_45[33:45]   # 12 questions

    selected = []
    selected.extend(random.sample(app_qs, min(6, len(app_qs))))
    selected.extend(random.sample(dbg_qs, min(5, len(dbg_qs))))
    selected.extend(random.sample(opt_qs, min(4, len(opt_qs))))

    # Re-number STT 1 to 15
    exam_15 = []
    for idx, q in enumerate(selected, 1):
        item = dict(q)
        item["STT"] = idx
        exam_15.append(item)

    return exam_15


class StudentClassifier:
    """
    Module tự động Phân loại Năng lực Sinh viên và Xuất đề xuất chiến thuật giảng dạy (Actionable Pedagogy)
    tuân thủ 100% Ma trận 5 nhóm (Đầu giờ) và 4 nhóm (Cuối giờ) từ RE_Tiêu chuẩn quizz.pdf.
    """

    @staticmethod
    def classify_entrance_student(student_name: str, total_score: int, new_lesson_score: int) -> Dict[str, Any]:
        """
        Phân loại 1 sinh viên bài thi Đầu giờ (15 câu = 10 bài cũ + 5 bài mới).
        """
        if total_score >= 13 and new_lesson_score == 5:
            group = "Gương mẫu"
            level = "Xuất sắc"
            strategy = "Cho làm Leader nhóm hoặc giao các bài tập Sáng tạo khó hơn."
        elif total_score >= 10 and new_lesson_score >= 3:
            group = "Ổn định"
            level = "Trung bình - Khá"
            strategy = "Cần động lực (Push) để bước lên nhóm Gương mẫu."
        elif total_score >= 10 and new_lesson_score < 3:
            group = "Tư duy tốt"
            level = "Thực chiến tốt nhưng lười tự học"
            strategy = "Cảnh cáo về kỷ luật tự học và yêu cầu xem lại tài liệu bài mới ngay tại lớp."
        elif 7 <= total_score <= 9 and new_lesson_score >= 3:
            group = "Nỗ lực"
            level = "Chăm chỉ nhưng hổng kiến thức nền"
            strategy = "Tập trung bổ trợ lại bài cũ ngay tại lớp để không bị hổng kiến thức hệ thống."
        elif 7 <= total_score <= 9 and new_lesson_score < 3:
            group = "Ẩn mình"
            level = "Có tư duy nhưng thiếu kỷ luật"
            strategy = "Yêu cầu xem lại tài liệu bài mới ngay tại lớp."
        else:
            group = "Nguy cơ"
            level = "Mất gốc bài cũ và không chuẩn bị bài mới"
            strategy = "Cần kèm cặp riêng 1:1 bởi Trợ giảng hoặc Giảng viên ngay sau buổi học."

        return {
            "student_name": student_name,
            "total_score": f"{total_score}/15",
            "new_lesson_score": f"{new_lesson_score}/5",
            "group": group,
            "level": level,
            "recommended_strategy": strategy
        }

    @staticmethod
    def classify_exit_student(student_name: str, score: int) -> Dict[str, Any]:
        """
        Phân loại 1 sinh viên bài thi Cuối giờ (15 câu bài mới).
        """
        if score >= 13:
            group = "Làm chủ"
            level = "Xuất sắc (Hiểu bản chất, code sạch, xử lý bẫy logic)"
            strategy = "Giao bài tập về nhà mức xuất sắc (Project-based), chỉ định làm Mentor hỗ trợ nhóm yếu ở buổi sau, miễn bài tập lặp lại cơ bản."
        elif 10 <= score <= 12:
            group = "Đạt"
            level = "Khá (Nắm vững cú pháp, chưa tối ưu câu Phân tích)"
            strategy = "Yêu cầu viết Comment/Documentation giải thích luồng code bài tập, giao bài tập về nhà rèn luyện độ tỉ mỉ."
        elif 7 <= score <= 9:
            group = "Cơ bản"
            level = "Trung bình (Chỉ dừng ở mức copy-paste hoặc shadowing theo thầy)"
            strategy = "Yêu cầu làm lại bài tập từ đầu (không nhìn code mẫu), bắt buộc xem lại Record buổi học tại các đoạn giảng logic."
        else:
            group = "Cần kèm"
            level = "Yếu (Chưa hiểu luồng chạy của code, gặp khó khăn vận dụng)"
            strategy = "Kèm cặp 1:1 bởi Trợ giảng hoặc Giảng viên ngay sau buổi học, rà soát lại kiến thức nền."

        return {
            "student_name": student_name,
            "score": f"{score}/15",
            "group": group,
            "level": level,
            "recommended_strategy": strategy
        }

