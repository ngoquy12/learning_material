# agents/strategic_agents.py
import json
import hashlib
from typing import Dict, Any
from config.settings import get_agent_prompt
from core.llm import call_llm
from core.schemas.llm_schemas import ObjectiveOutcomeSchema

def objective_architect_agent(pm_input: str, tech_stack: str, previous_feedback: str = "") -> Dict[str, Any]:
    """
    Objective Architect Agent:
    Dynamically analyzes the PM input JSON string for a specific Session and generates backward-design
    learning outcomes tailored to the specified technology stack.
    """
    if not tech_stack or not tech_stack.strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] objective_architect_agent: Yêu cầu tham số tech_stack hợp lệ.")
    print(f"\n[Objective Architect Agent] Analyzing Session PM Input...")
    
    # Parse structured JSON if possible
    try:
        session_data = json.loads(pm_input)
        session_title = session_data.get("title", "Untitled Session")
        lessons = session_data.get("lessons", [])
    except Exception:
        session_title = "Programming Session"
        lessons = []
        
    print(f"  - Session Topic: '{session_title}' ({len(lessons)} lessons)")
    
    # Attempt LLM call
    agent_prompt = get_agent_prompt("Objective_Architect_Agent")
    system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
    user_prompt = f"""
    Analyze the following PM input data:
    {pm_input}
    
    The target technology stack for this course is: {tech_stack}
    
    {f"REVIEW REVISION FEEDBACK (Fix all reported errors): {previous_feedback}" if previous_feedback else ""}
    
    Generate backward-design learning outcomes tailored specifically for this stack.
    
    STRICT SCOPE & COGNITIVE LEVELS DIRECTIVES:
    1. Strictly focus on topics and concepts described in the PM input. FORBIDDEN to introduce unrequested advanced concepts or third-party libraries.
    2. Outcomes MUST strictly match current student cognitive levels (do not require advanced system design, performance tuning, or complex architectures in introductory sessions).
    3. FORBIDDEN to mix or reference concepts from other technology stacks.
    
    The response MUST be a valid JSON matching this schema:
    {{
        "session_title": "{session_title}",
        "student_profile_outcome": "Detailed outcome profile",
        "blooms_taxonomy": {{
            "remembering_understanding": ["outcome 1", "outcome 2"],
            "applying_analyzing": ["outcome 3", "outcome 4"],
            "evaluating_creating": ["outcome 5", "outcome 6"]
        }}
    }}
    Return only raw JSON. Do not wrap in markdown code blocks.
    """
    
    response_text = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Objective_Architect_Agent",
        session_id=session_title,
        response_schema=ObjectiveOutcomeSchema
    )
    if response_text:
        try:
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            result = json.loads(cleaned)
            print("  - Objective Architect Agent successfully invoked LLM dynamically via Structured Outputs.")
            return result
        except Exception as e:
            print(f"  [LLM Error] Failed to parse JSON response via Structured Outputs: {e}. Falling back to default rules.")
            
    # Default Rule-based Fallback
    blooms = {
        "remembering_understanding": [
            f"Recall core definitions of {session_title}.",
            "Explain core processing and logic lifecycles."
        ],
        "applying_analyzing": [],
        "evaluating_creating": []
    }
    
    for idx, les in enumerate(lessons, 1):
        title = les.get("title", "")
        out = les.get("expected_output", "")
        blooms["applying_analyzing"].append(f"Build: {title} to achieve output: '{out}'")
        if idx % 2 == 0:
            blooms["evaluating_creating"].append(f"Evaluate and debug errors during setup of {title}.")
            
    if not lessons:
        blooms["applying_analyzing"].append("Complete practical labs and write basic code modules.")
        blooms["evaluating_creating"].append("Evaluate program execution and troubleshoot logic errors.")
        
    return {
        "session_title": session_title,
        "student_profile_outcome": f"Students will confidently master the concepts and practical output of {session_title}.",
        "blooms_taxonomy": blooms
    }

def scheduler_agent(learning_outcomes: Dict[str, Any], time_reference: Dict[str, Any], tech_stack: str) -> Dict[str, Any]:
    """
    Scheduler Agent:
    Takes learning outcomes and structures the lessons, checking cognitive load limitations.
    """
    if not tech_stack or not tech_stack.strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] scheduler_agent: Yêu cầu tham số tech_stack hợp lệ.")
    print("\n[Scheduler_Agent] Balancing cognitive load schedules...")
    session_title = learning_outcomes.get("session_title", "Scheduled Topic")
    
    agent_prompt = get_agent_prompt("Scheduler_Agent")
    system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
    user_prompt = f"""
    Given the following learning outcomes:
    {json.dumps(learning_outcomes, ensure_ascii=False)}
    
    And the time reference constraints:
    {json.dumps(time_reference, ensure_ascii=False)}
    
    The target technology stack for this course is: {tech_stack}
    Response MUST be a valid JSON matching this schema:
    {{
        "session_title": "...",
        "lessons": [
            {{
                "lesson_num": 1,
                "topic": "Topic description from outcomes",
                "cognitive_load_minutes": {{
                    "html_reading": 15,
                    "video_lecture": 10,
                    "quiz_practice": 25
                }}
            }}
        ]
    }}
    Return only raw JSON. Do not wrap in markdown code blocks.
    """
    
    response_text = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Scheduler_Agent",
        session_id=session_title
    )
    if response_text:
        try:
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            result = json.loads(cleaned)
            print("  - Scheduler Agent successfully invoked LLM dynamically.")
            return result
        except Exception as e:
            print(f"  [LLM Error] Failed to parse Scheduler JSON: {e}. Falling back to default rules.")
            
    # Default Fallback
    program_structure = {
        "session_title": session_title,
        "lessons": []
    }
    
    blooms_app = learning_outcomes.get("blooms_taxonomy", {}).get("applying_analyzing", [])
    for idx, bloom_task in enumerate(blooms_app, 1):
        program_structure["lessons"].append({
            "lesson_num": idx,
            "topic": bloom_task,
            "cognitive_load_minutes": {
                "html_reading": 15,
                "video_lecture": 10,
                "quiz_practice": 25
            }
        })
        
    if not program_structure["lessons"]:
        program_structure["lessons"].append({
            "lesson_num": 1,
            "topic": "Session Practice and Lab execution",
            "cognitive_load_minutes": {
                "html_reading": 10,
                "video_lecture": 5,
                "quiz_practice": 45
            }
        })
        
    print(f"  - Scheduled {len(program_structure['lessons'])} timeline lessons successfully.")
    return program_structure

def knowledge_base_agent(program_structure: Dict[str, Any], tech_stack: str) -> Dict[str, Any]:
    """
    Knowledge Base Agent:
    Builds the SSOT knowledge maps, providing definitions, code examples,
    and configurations based on the scheduled topics.
    """
    if not tech_stack or not tech_stack.strip():
        raise ValueError("❌ [LỖI THIẾU TECHNOLOGY STACK] knowledge_base_agent: Yêu cầu tham số tech_stack hợp lệ.")
    print("\n[Knowledge_Base_Agent] Compiling exact SSOT definitions and code snippets...")
    session_title = program_structure.get("session_title", "")
    
    agent_prompt = get_agent_prompt("Knowledge_Base_Agent")
    system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
    user_prompt = f"""
    Build a Single Source of Truth (SSOT) knowledge base for the following program structure:
    {json.dumps(program_structure, ensure_ascii=False)}
    
    The target technology stack is: {tech_stack}
    
    STRICT SCOPE & PEDAGOGICAL BOUNDARIES DIRECTIVES:
    1. Provide concepts and code samples strictly within the scope of the current session. FORBIDDEN to introduce future lesson concepts, unlearned frameworks, or alien libraries.
    2. Syntax and code structures MUST be simple, beginner-friendly, and match current student level (e.g. avoid complex async/await, lambdas, or database connections in introductory lessons).
    3. Code samples MUST focus on solving exactly 1 core problem of the lesson without bloated or unrequested features.
    
    Provide definitions for all key concepts and write solid, realistic code samples strictly in the target tech_stack ('{tech_stack}'). Do NOT use other languages or unrequested frameworks.
    The response MUST be a valid JSON matching this schema:
    {{
        "session_title": "{session_title}",
        "concepts": {{
            "concept_name_1": "precise definition",
            "concept_name_2": "precise definition"
        }},
        "code_samples": {{
            "code_sample_name_1": "actual clean code snippet",
            "code_sample_name_2": "actual clean code snippet"
        }}
    }}
    WARNING: All backslashes (\\) in strings (such as Windows paths like venv\\Scripts) MUST be properly escaped as double backslashes (\\\\) to ensure the output is strictly valid JSON!
    Return only raw JSON. Do not wrap in markdown code blocks.
    """
    
    response_text = call_llm(
        system_prompt,
        user_prompt,
        json_mode=True,
        agent_name="Knowledge_Base_Agent",
        session_id=session_title
    )
    
    concepts = None
    code_samples = None
    
    if response_text:
        try:
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            result = json.loads(cleaned)
            concepts = result.get("concepts")
            code_samples = result.get("code_samples")
            print("  - Knowledge Base Agent successfully invoked LLM dynamically.")
        except Exception as e:
            print(f"  [LLM Error] Failed to parse KB JSON: {e}. Falling back to default rules.")
            
    # Dynamic category-aware fallback if LLM fails or is not configured
    if not concepts or not code_samples:
        print(f"  [KB Fallback] Using dynamic category-aware fallback for stack: {tech_stack}")
        parts = tech_stack.lower().split('/')
        lang = parts[0] if len(parts) > 0 else "generic"
        framework = parts[1] if len(parts) > 1 else "core"
        
        concepts = {
            f"core_{lang}_concept": f"Introduction to fundamental concepts of {lang.capitalize()} within {session_title}.",
            "architecture_overview": f"Basic architectural overview and request-response lifecycle for {framework.capitalize()} applications.",
            "best_practices": "Code organization, formatting, and standard conventions for development."
        }
        
        # Removed hardcoded tech stack switch statement to enforce language-agnostic logic
        code_samples = {
            "hello_world": (
                f"// Core hello world structural sample for {tech_stack}\n"
                "// Dynamic fallback generated offline"
            )
        }
        
    # Generate stable Hash
    hash_input = json.dumps(program_structure) + json.dumps(concepts)
    hash_key = "sha256_" + hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:16]
    
    core_ssot = {
        "session_title": session_title,
        "course_metadata": {
            "hash_key": hash_key,
            "status": "LOCKED"
        },
        "concepts": concepts,
        "code_samples": code_samples
    }
    
    # Seed Lightweight Vector Store with SSOT elements
    try:
        from core.vector_store import get_vector_store
        store = get_vector_store()
        docs = []
        for name, val in concepts.items():
            docs.append({
                "text": f"Khái niệm: {name} - Định nghĩa: {val}",
                "metadata": {"type": "concept", "session": session_title}
            })
        for name, val in code_samples.items():
            docs.append({
                "text": f"Mã nguồn mẫu cho {name}:\n{val}",
                "metadata": {"type": "code", "session": session_title}
            })
        store.add_documents(docs)
        print(f"  [VectorStore] Successfully seeded {len(docs)} document chunks into local Vector DB.")
    except Exception as e:
        print(f"  [VectorStore Warning] Seeding failed: {e}")
        
    print(f"  - Compiled SSOT for '{session_title}' with hash {hash_key}")
    return core_ssot
