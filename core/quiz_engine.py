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

def generate_quiz_batch_via_llm(topic_name: str, tech_stack: str, count: int, difficulty: int, category: str, start_stt: int) -> List[Dict[str, Any]]:
    """Generates a batch of quiz questions via LLM using RAG content from local Vector DB."""
    import os
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        raise RuntimeError("LLM API Key is missing. Cannot generate quiz dynamically.")
        
    from core.llm import call_llm
    from core.skills import load_skill_content
    from core.vector_store import LightweightVectorStore
    
    rag_context = ""
    try:
        store = LightweightVectorStore()
        matches = store.query(topic_name, k=3)
        if matches:
            rag_context = "\nNgữ cảnh tham chiếu từ Vector DB:\n" + "\n".join([m["text"] for m in matches])
    except Exception as e:
        print(f"  [Quiz Engine] Info: Could not load vector context - {e}")
        
    skill_content = load_skill_content("quizz_session")
    
    questions = []
    remaining = count
    current_stt = start_stt
    max_sub_batch = 3
    
    while remaining > 0:
        sub_count = min(max_sub_batch, remaining)
        sub_qs = []
        
        system_prompt = f"""Bạn là Chuyên gia thiết kế câu hỏi kiểm tra học thuật (Assessment Specialist).
Nhiệm vụ của bạn là tạo ra đúng {sub_count} câu hỏi trắc nghiệm khách quan có chất lượng cực kỳ cao về chủ đề '{topic_name}' sử dụng công nghệ '{tech_stack}'.

Quy tắc sinh câu hỏi (Quizz Session Skill):
{skill_content}

RÀNG BUỘC CỦA ĐỢT SINH NÀY (BẮT BUỘC TUÂN THỦ):
- Số câu hỏi cần tạo: {sub_count} câu. KHÔNG ĐƯỢC THIẾU HOẶC THỪA.
- Số thứ tự bắt đầu (STT): {current_stt}.
- Độ khó (difficulty): {difficulty} (Thang điểm 1-10. 1-4: Nhớ/Hiểu, 5-7: Phân tích/Vận dụng, 8-10: Debug/Tối ưu/Kiến trúc).
- Phân loại (category): "{category}".
- QUY TẮC RÀNG BUỘC PHẠM VI KIẾN THỨC (DYNAMIC KNOWLEDGE SCOPE BOUNDARY):
  + Mọi câu hỏi CHỈ ĐƯỢC PHÉP hỏi về đúng chủ đề '{topic_name}' và công nghệ '{tech_stack}'.
  + TUYỆT ĐỐI CẤM đưa các khái niệm, cú pháp, hàm hay framework nâng cao thuộc các bài học tương lai hoặc chưa học vào câu hỏi hay bất kỳ phương án đáp án nào!
  + CẤM lạc đề, CẤM đưa từ ngữ mơ hồ ("theo slide", "trong video này"). Câu hỏi phải chính xác, khách quan như đề thi quốc tế.
{rag_context}

Yêu cầu định dạng đầu ra:
Bạn phải trả về duy nhất một mảng JSON (List) chứa đúng {sub_count} phần tử Object có cấu trúc như sau:
[
  {{
    "STT": {current_stt},
    "question_content": "Nội dung câu hỏi tình huống thực tế...",
    "answer_1": "Đáp án đúng A",
    "explanation_answer_1": "Giải thích vì sao A đúng...",
    "answer_2": "Đáp án nhiễu B",
    "explanation_answer_2": "Giải thích vì sao B sai...",
    "answer_3": "Đáp án nhiễu C",
    "explanation_answer_3": "Giải thích...",
    "answer_4": "Đáp án nhiễu D",
    "explanation_answer_4": "Giải thích...",
    "isCorrect": 1,
    "difficulty": {difficulty},
    "category": "{category}"
  }}
]
Mẹo cực kỳ quan trọng: Luôn xếp đáp án đúng vào 'answer_1' và 'isCorrect' là 1. Hệ thống của chúng tôi sẽ tự động xáo trộn ngẫu nhiên thứ tự 4 đáp án này ở bước hậu kỳ.
TUYỆT ĐỐI không trả về markdown block code (như ```json), chỉ trả về mảng JSON thuần túy.
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
            print(f"  [Session Quiz Agent Error] Failed to generate sub-batch of {sub_count} questions. Returning empty list.")
            return []
            
        questions.extend(sub_qs)
        remaining -= sub_count
        current_stt += sub_count
        
    return questions

def generate_entrance_quiz(session_id: str, current_topic: str, previous_topic: str, tech_stack: str = "python/fastapi") -> List[Dict[str, Any]]:
    """Generates a 45-question Entrance Quiz dynamically via LLM Agent."""
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
            str(batch["topic"]),
            tech_stack,
            int(batch["count"]),
            int(batch["diff"]),
            str(batch["cat"]),
            start_stt
        )
        if q_batch:
            questions.extend(q_batch)
            
    for q in questions:
        shuffle_options_and_explanations(q)
        
    # Fix STT sequencing just in case
    for idx, q in enumerate(questions, 1):
        q["STT"] = idx
        
    return questions

def generate_exit_quiz(session_id: str, current_topic: str, tech_stack: str = "python/fastapi") -> List[Dict[str, Any]]:
    """Generates a 45-question Exit Quiz dynamically via LLM Agent."""
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
            str(batch["topic"]),
            tech_stack,
            int(batch["count"]),
            int(batch["diff"]),
            str(batch["cat"]),
            start_stt
        )
        if q_batch:
            questions.extend(q_batch)
            
    for q in questions:
        shuffle_options_and_explanations(q)
        
    # Fix STT sequencing just in case
    for idx, q in enumerate(questions, 1):
        q["STT"] = idx
        
    return questions
