import os
import re
import requests
import base64
from pathlib import Path
from core.state import AgentState
from agents.creators.common_utils import get_lesson_content, get_lesson_dir, log_agent_tokens

def generate_image_api(prompt_text: str, image_path) -> bool:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if api_key:
        try:
            base_url = os.getenv("GEMINI_BASE_URL")
            if base_url:
                url = f"{base_url.rstrip('/')}/v1/images/generations"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "prompt": prompt_text,
                    "n": 1,
                    "size": "1024x576"
                }
                response = requests.post(url, headers=headers, json=data, timeout=40)
                if response.status_code == 200:
                    resp_json = response.json()
                    img_data = resp_json.get("data", [])
                    if img_data and "b64_json" in img_data[0]:
                        img_b64 = img_data[0]["b64_json"]
                        with open(image_path, "wb") as f:
                            f.write(base64.b64decode(img_b64))
                        print(f"  [Image Generator] Saved diagram to: {image_path}")
                        return True
                    elif img_data and "url" in img_data[0]:
                        img_url = img_data[0]["url"]
                        img_resp = requests.get(img_url, timeout=20)
                        if img_resp.status_code == 200:
                            with open(image_path, "wb") as f:
                                f.write(img_resp.content)
                            print(f"  [Image Generator] Saved downloaded diagram to: {image_path}")
                            return True
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                "instances": [
                    {
                        "prompt": prompt_text
                    }
                ],
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "16:9",
                    "outputMimeType": "image/png"
                }
            }
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                resp_json = response.json()
                if "predictions" in resp_json and len(resp_json["predictions"]) > 0:
                    img_b64 = resp_json["predictions"][0]["bytesBase64Encoded"]
                    with open(image_path, "wb") as f:
                        f.write(base64.b64decode(img_b64))
                    print(f"  [Image Generator] Saved diagram to: {image_path}")
                    return True
                else:
                    print(f"  [Image Generator Warning] Response did not contain images: {resp_json}")
            else:
                print(f"  [Image Generator Warning] API status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"  [Image Generator Warning] Dynamic image generation error: {e}")
    return False

def draw_mindmap_fallback_diagram(prompt_text: str, image_path: Path, title: str):
    raise NotImplementedError("Fallback mindmap diagram generation is disabled. All images must be generated dynamically by AI.")

def process_mindmap_images(markmap_content: str, state: AgentState) -> str:
    brackets = re.findall(r"\[(?:Prompt|Tạo ảnh):\s*([^\]]+)\]", markmap_content)
    asterisks = re.findall(r"\*Prompt tạo ảnh:\s*([^*]+)\*", markmap_content, flags=re.IGNORECASE)
    
    all_prompts = []
    seen = set()
    for p in brackets + asterisks:
        p_clean = p.strip()
        if p_clean not in seen:
            seen.add(p_clean)
            all_prompts.append(p_clean)
            
    if not all_prompts:
        return markmap_content
        
    try:
        lesson_dir = get_lesson_dir(state)
        images_dir = lesson_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"  [Image Processing Warning] Could not resolve lesson directory: {e}")
        return markmap_content
        
    new_content = markmap_content
    for idx, prompt_text in enumerate(all_prompts, 1):
        image_name = f"mindmap_img_{idx}.png"
        image_path = images_dir / image_name
        
        print(f"  [Mindmap Image] Processing prompt {idx}: '{prompt_text[:50]}...'")
        
        force_rebuild = state.get("force_rebuild", False)
        if force_rebuild or not image_path.exists():
            success = generate_image_api(prompt_text, image_path)
            if not success:
                print(f"  [Mindmap Image Warning] AI image generation failed for prompt '{prompt_text[:50]}...'. Default fallback diagram is disabled.")
        
        search_bracket = r"\[(?:Prompt|Tạo ảnh):\s*" + re.escape(prompt_text) + r"\]"
        new_content = re.sub(search_bracket, f"![](../images/{image_name})", new_content)
        
        search_asterisk = r"\*Prompt tạo ảnh:\s*" + re.escape(prompt_text) + r"\*"
        new_content = re.sub(search_asterisk, f"![](../images/{image_name})", new_content, flags=re.IGNORECASE)
        
    return new_content

def mindmap_agent(state: AgentState) -> AgentState:
    """
    Mindmap Agent:
    Generates a structured Markmap diagram based on skills/mindmap_generator/SKILL.md.
    Uses the LLM with retry/critique logs if keys are available, otherwise falls back to a template.
    """
    session_id = state.get("session_id", "Session 01")
    from core.state import require_tech_stack
    tech_stack = require_tech_stack(state, "mindmap_agent")
    
    core_ssot = state.get("core_ssot", {})
    lesson_title = core_ssot.get("session_title", "Course Session")
    lesson_details = core_ssot.get("lesson_details", "")
    expected_output = core_ssot.get("expected_output", "")
    
    mindmap_logs = [log for log in state.get("review_logs", []) if log["source"] == "Mindmap_Reviewer"]
    attempt_num = len(mindmap_logs) + 1
    feedback = mindmap_logs[-1]["feedback"] if mindmap_logs else ""
    
    print(f"\n[Mindmap_Agent] Generating Markmap diagram for {session_id} {lesson_id} (Attempt #{attempt_num}) using mindmap_generator skill...")
    
    content = get_lesson_content(
        session_id=session_id,
        lesson_id=lesson_id,
        lesson_title=lesson_title,
        lesson_details=lesson_details,
        expected_output=expected_output,
        attempt_num=attempt_num,
        core_ssot=core_ssot,
        feedback=feedback,
        state=state
    )
    
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    if not (gemini_key or openai_key):
        ex_snippet = content.get("example", "")
        indented_example = "\n".join(f"      {line}" for line in ex_snippet.splitlines()) if ex_snippet else "      # Không có mã nguồn minh họa."
        mindmap_prompt = f"[Prompt: Generate a visual flow/sequence diagram showing the architecture, control flow, and execution lifecycle of '{tech_stack}']"
        
        markmap_content = f"""```markmap
# {session_id}: {lesson_title}
## Mục tiêu bài học
- Hiểu rõ khái niệm cốt lõi và kiến trúc của {lesson_title}.
- Áp dụng các quy tắc triển khai thực tiễn để giải quyết bài toán: {expected_output if expected_output else 'tích hợp thành công'}.
- Vận hành và kiểm tra đầu ra hoạt động ổn định.
## {lesson_title}
### Khái niệm cốt lõi
- Giải pháp kỹ thuật giúp tối ưu hóa hiệu năng, giảm thiểu blocking I/O và tự động hóa validation cho {tech_stack}.
### Cú pháp & Cách khai báo
- Ví dụ triển khai:
{indented_example}
### Lưu ý thực chiến
- Tránh bỏ sót các tham số bắt buộc.
- Cấu hình môi trường ảo venv chính xác và không đặt trùng tên file hệ thống.
{mindmap_prompt}
```"""
    else:
        from core.llm import call_llm
        from core.skills import load_skill_content
        
        mindmap_skill = load_skill_content("mindmap_generator")
        image_skill = load_skill_content("image_prompt_standard")
        
        master_content_summary = ""
        if content:
            sections_text = "\n".join([f"### {sec['title']}\n{sec['content']}" for sec in content.get("reading_sections", [])])
            master_content_summary = f"""
--- NỘI DUNG CHI TIẾT BÀI HỌC (Sử dụng làm cơ sở dữ liệu học thuật) ---
{sections_text}

--- MÃ NGUỒN VÍ DỤ ---
```python
{content.get('example', '')}
```

--- TỔNG KẾT & SAI LẦM THƯỜNG GẶP ---
{content.get('summary', '')}
"""

        system_prompt = f"""You are a Lead Academic Director & Senior Curriculum Mindmap Specialist at Rikkei Education.
Your task is to synthesize a complete, highly-condensed, and visually structured MARKMAP MINDMAP summarizing the technical learning content of the lesson below.

MANDATORY MINDMAP DIRECTIVES:
1. Strictly follow the rules, branching hierarchy, and constraints specified in the Mindmap Generator Skill:
{mindmap_skill}

2. Visual Design & Image Prompts Standard:
For complex architecture/flow concepts, embed image prompt nodes adhering strictly to the blueprint formula below:
{image_skill}
"""
        
        concepts_list = "\n".join([f"- {k}" for k in core_ssot.get("concepts", {}).keys()])
        feedback_context = f"\nMindmap Reviewer Revision Feedback (if any, you MUST fix these errors): {feedback}\n" if feedback else ""
        
        user_prompt = f"""Generate a Markmap system mindmap for lesson:
Session: {session_id}
Lesson: {lesson_id} (Title: {lesson_title})
Curriculum Details from PM: {lesson_details}
Expected Output: {expected_output}
Target Technology Stack: {tech_stack}

MANDATORY OUTPUT CONTRACT:
- Return ONLY a single Markdown code block: ` ```markmap ... ` ```.
- Target Output Language: All mindmap nodes, objectives, problems, and notes MUST be written in 100% Accented Vietnamese.
- The mindmap must be extremely concise, rich in technical depth but visually clean, with no long paragraphs.
- Level 1 Heading (#) MUST contain ONLY the clean content/topic title, stripping any prefixes like "{lesson_id} - " or "{lesson_id}: ". For example, if lesson is "Lesson 02 - Vòng lặp for", the H1 MUST be "# Vòng lặp for".
- Level 2 Headings (##) MUST follow this strict sequence:
  1. First branch MUST be "## Mục tiêu bài học" (outlining 3-4 generalized goals in Accented Vietnamese).
  2. Second branch MUST be "## Đặt tình huống" (outlining real-world business context/problem statement).
  3. Subsequent branches MUST represent the actual child lessons or core technical topics of this lesson.
- Level 3 Headings (###) MUST be dynamic and ultra-short (e.g. use "### Cú pháp" instead of "### Cú pháp lập trình", and "### Lưu ý" instead of "### Các lưu ý thực chiến").
- For difficult concepts or workflow control, embed a standard English image generation prompt matching: *Prompt tạo ảnh: A clean 2D flat vector technical illustration of [logic]. Main title in concise Accented Vietnamese. Strictly NO text emojis. 16:9 aspect ratio...*
- ABSOLUTELY FORBIDDEN to use any text emojis (❌, ✅, ⚠️, 🔴, 🟢, ▶) anywhere in the mindmap content.

{feedback_context}
"""
        markmap_content = call_llm(
            system_prompt,
            user_prompt,
            json_mode=False,
            agent_name=f"Mindmap_Agent_Att{attempt_num}",
            session_id=session_id,
            lesson_id=lesson_id
        )
        if markmap_content:
            markmap_content = markmap_content.strip()
            if markmap_content.startswith("```markdown"):
                markmap_content = markmap_content[11:].strip()
            
            if not markmap_content.startswith("```markmap"):
                if "```markmap" in markmap_content:
                    idx = markmap_content.find("```markmap")
                    markmap_content = markmap_content[idx:].strip()
                else:
                    markmap_content = "```markmap\n" + markmap_content
            
            lines = markmap_content.splitlines()
            level = 0
            for line in lines:
                stripped_line = line.strip()
                if stripped_line.startswith("```"):
                    if level == 0 and stripped_line.startswith("```markmap"):
                        level = 1
                    elif level == 1:
                        level = 2
                    elif level == 2:
                        level = 1
                    elif level == 1 and stripped_line == "```":
                        level = 0
            if level == 2:
                lines.append("```")
                level = 1
            if level == 1:
                lines.append("```")
                level = 0
            markmap_content = "\n".join(lines)
        else:
            markmap_content = f"```markmap\n# {session_id}: {lesson_title}\n## Mục tiêu bài học\n- Lỗi khi sinh sơ đồ tư duy.\n```"

    processed_content = process_mindmap_images(markmap_content, state)
    state["mindmap_markdown"] = processed_content
    log_agent_tokens("Mindmap_Agent", state, processed_content)
    return state
