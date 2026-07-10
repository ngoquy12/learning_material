# agents/strategic_agents.py
import json
import hashlib
from typing import Dict, Any
from config.settings import get_agent_prompt
from core.llm import call_llm

def objective_architect_agent(pm_input: str, tech_stack: str = "python/core") -> Dict[str, Any]:
    """
    Objective Architect Agent:
    Dynamically analyzes the PM input JSON string for a specific Session and generates backward-design
    learning outcomes tailored to the specific FastAPI / Web Services topic.
    """
    print(f"\n[Objective Architect Agent] Analyzing Session PM Input...")
    
    # Parse structured JSON if possible
    try:
        session_data = json.loads(pm_input)
        session_title = session_data.get("title", "Untitled Session")
        lessons = session_data.get("lessons", [])
    except Exception:
        session_title = "FastAPI Development"
        lessons = []
        
    print(f"  - Session Topic: '{session_title}' ({len(lessons)} lessons)")
    
    # Attempt LLM call
    agent_prompt = get_agent_prompt("Objective_Architect_Agent")
    system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
    user_prompt = f"""
    Analyze the following PM input data:
    {pm_input}
    
    The target technology stack for this course is: {tech_stack}
    Generate backward-design learning outcomes tailored specifically for this stack.
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
        session_id=session_title
    )
    if response_text:
        try:
            # Strip markdown formatting just in case
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            result = json.loads(cleaned)
            print("  - Objective Architect Agent successfully invoked LLM dynamically.")
            return result
        except Exception as e:
            print(f"  [LLM Error] Failed to parse JSON response: {e}. Falling back to default rules.")
            
    # Default Rule-based Fallback
    blooms = {
        "remembering_understanding": [
            f"Recall core definitions of {session_title}.",
            "Explain client-server request-response lifecycles."
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
        blooms["applying_analyzing"].append("Complete practical labs and write basic REST API routes.")
        blooms["evaluating_creating"].append("Evaluate endpoint responsiveness and troubleshoot response code errors.")
        
    return {
        "session_title": session_title,
        "student_profile_outcome": f"Students will confidently master the concepts and practical output of {session_title}.",
        "blooms_taxonomy": blooms
    }

def scheduler_agent(learning_outcomes: Dict[str, Any], time_reference: Dict[str, Any], tech_stack: str = "python/core") -> Dict[str, Any]:
    """
    Scheduler Agent:
    Takes learning outcomes and structures the lessons, checking cognitive load limitations.
    """
    print("\n[Scheduler_Agent] Balancing cognitive load schedules...")
    session_title = learning_outcomes.get("session_title", "FastAPI Topic")
    
    agent_prompt = get_agent_prompt("Scheduler_Agent")
    system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
    user_prompt = f"""
    Given the following learning outcomes:
    {json.dumps(learning_outcomes, ensure_ascii=False)}
    
    And the time reference constraints:
    {json.dumps(time_reference, ensure_ascii=False)}
    
    The target technology stack for this course is: {tech_stack}
    Structure the session lessons. Calculate and assign realistic cognitive load minutes (html_reading: max 25, video_lecture: max 15, quiz_practice: max 45).
    Response MUST be a valid JSON matching this schema:
    {{
        "session_title": "{session_title}",
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

def knowledge_base_agent(program_structure: Dict[str, Any], tech_stack: str = "python/core") -> Dict[str, Any]:
    """
    Knowledge Base Agent:
    Builds the SSOT knowledge maps, providing definitions, code examples,
    and configurations based on the scheduled FastAPI topics.
    """
    print("\n[Knowledge_Base_Agent] Compiling exact SSOT definitions and code snippets...")
    session_title = program_structure.get("session_title", "")
    
    agent_prompt = get_agent_prompt("Knowledge_Base_Agent")
    system_prompt = f"{agent_prompt.get('Persona', '')}\n{agent_prompt.get('Task', '')}"
    user_prompt = f"""
    Build a Single Source of Truth (SSOT) knowledge base for the following program structure:
    {json.dumps(program_structure, ensure_ascii=False)}
    
    The target technology stack is: {tech_stack}
    Provide definitions for all key concepts and write solid, realistic code samples strictly in this stack (for example, if stack is 'python/core', all code samples must be in Python and explain Python-specific core concepts. Do NOT use JavaScript or other languages).
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
            
    # Default Fallback values if LLM fails or is not configured
    if not concepts or not code_samples:
        concepts = {
            "client_server": "Client (Browser/Postman) sends HTTP requests to Web API server, which queries Database and returns RESTful JSON responses.",
            "virtual_env": "A self-contained directory containing a Python installation for a particular version of Python, plus additional packages.",
            "uvicorn": "An ASGI web server implementation for Python, used to serve FastAPI applications.",
            "routing": "Mapping HTTP methods (GET, POST, etc.) and URLs to specific Python execution handler functions.",
            "swagger": "An open-source software framework backed by a large ecosystem of tools that helps developers design, build, document, and consume RESTful Web APIs."
        }
        
        code_samples = {
            "virtual_env_setup": (
                "# B1: Tạo môi trường ảo\n"
                "python -m venv venv\n\n"
                "# B2: Kích hoạt môi trường\n"
                "venv\\Scripts\\activate  # Trên Windows\n"
                "source venv/bin/activate  # Trên Linux/macOS\n\n"
                "# B3: Cài đặt thư viện\n"
                "pip install fastapi uvicorn"
            ),
            "fastapi_app": (
                "from fastapi import FastAPI\n\n"
                "app = FastAPI(title='IT215 FastAPI App')\n\n"
                "@app.get('/hello')\n"
                "def read_root():\n"
                "    return {'message': 'Hello World'}"
            ),
            "diagram_ascii": (
                "  +------------+             +-------------+             +------------+\n"
                "  |   Client   |   REQUEST   | FastAPI API |   QUERY     |  Database  |\n"
                "  | (Postman)  | ----------> |   Server    | ----------> |  (MySQL)   |\n"
                "  |            | <---------- |             | <---------- |            |\n"
                "  +------------+  RESPONSE   +-------------+  RESULT     +------------+"
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
        from core.vector_store import LightweightVectorStore
        store = LightweightVectorStore()
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
