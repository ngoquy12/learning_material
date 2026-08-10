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
