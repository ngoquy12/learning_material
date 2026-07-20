# agents/strategic_agents.py
import json
import hashlib
from typing import Dict, Any
from config.settings import get_agent_prompt
from core.llm import call_llm

def objective_architect_agent(pm_input: str, tech_stack: str = "python/core", previous_feedback: str = "") -> Dict[str, Any]:
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
    
    {f"CẢNH BÁO TỪ LẦN REVIEW TRƯỚC (Hãy sửa lỗi theo phản hồi này): {previous_feedback}" if previous_feedback else ""}
    
    Generate backward-design learning outcomes tailored specifically for this stack.
    
    🛑 CHỈ THỊ VỀ PHẠM VI & PHÂN BẬC NHẬN THỨC (STRICT SCOPE & COGNITIVE LEVELS):
    1. Chỉ tập trung tuyệt đối vào đúng các chủ đề, kiến thức được mô tả trong PM input. Tuyệt đối không đưa vào các khái niệm nâng cao, thư viện bên ngoài phức tạp hoặc các tính năng không được yêu cầu.
    2. Các chuẩn đầu ra phải phù hợp với trình độ hiện tại của học viên (không đòi hỏi các kỹ năng thiết kế hệ thống, tối ưu hiệu năng cao hay kiến trúc nâng cao ở các bài nhập môn).
    3. Không trộn lẫn hay tham chiếu đến các công nghệ thuộc stack khác.
    
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
    
    🛑 QUY TẮC PHẠM VI & PHÂN BẬC SƯ PHẠM NGHIÊM NGẶT (STRICT SCOPE & PEDAGOGICAL BOUNDARIES):
    1. Chỉ cung cấp khái niệm (concepts) và mã nguồn mẫu (code_samples) thuộc phạm vi của buổi học hiện tại. Tuyệt đối không đưa trước kiến thức của các buổi học sau hay các thư viện, framework ngoài lề.
    2. Cú pháp và cấu trúc mã nguồn mẫu phải cực kỳ đơn giản, dễ tiếp cận và tương xứng với trình độ hiện tại của học viên (ví dụ: không viết async/await, lambda phức tạp, hay kết nối database khi học lập trình căn bản).
    3. Mã nguồn ví dụ phải tập trung giải quyết đúng 1 vấn đề cốt lõi của bài học, tránh thêm code thừa hoặc các chức năng nâng cao không có trong yêu cầu.
    
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
        
        if lang == "python":
            if framework == "fastapi":
                code_samples = {
                    "app_init": (
                        "from fastapi import FastAPI\n\n"
                        "app = FastAPI()\n\n"
                        "@app.get('/')\n"
                        "def read_root():\n"
                        "    return {'message': 'Hello World'}"
                    )
                }
            else:
                code_samples = {
                    "hello_world": (
                        "def main():\n"
                        "    print('Hello from Python Core!')\n\n"
                        "if __name__ == '__main__':\n"
                        "    main()"
                    )
                }
        elif lang in ("typescript", "javascript"):
            if framework == "nestjs":
                code_samples = {
                    "app_controller": (
                        "import { Controller, Get } from '@nestjs/common';\n\n"
                        "@Controller()\n"
                        "export class AppController {\n"
                        "  @Get()\n"
                        "  getHello(): string {\n"
                        "    return 'Hello World!';\n"
                        "  }\n"
                        "}"
                    )
                }
            elif framework == "react":
                code_samples = {
                    "app_component": (
                        "import React from 'react';\n\n"
                        "export default function App() {\n"
                        "  return (\n"
                        "    <div>\n"
                        "      <h1>Hello World</h1>\n"
                        "      <p>Welcome to React</p>\n"
                        "    </div>\n"
                        "  );\n"
                        "}"
                    )
                }
            elif framework == "express":
                code_samples = {
                    "app_init": (
                        "const express = require('express');\n"
                        "const app = express();\n"
                        "const port = 3000;\n\n"
                        "app.get('/', (req, res) => {\n"
                        "  res.send('Hello World!');\n"
                        "});\n\n"
                        "app.listen(port, () => {\n"
                        "  console.log(`App listening at http://localhost:${port}`);\n"
                        "});"
                    )
                }
            else:
                code_samples = {
                    "hello_world": (
                        "console.log('Hello from JS/TS Core!');"
                    )
                }
        elif lang == "java":
            if framework == "springboot":
                code_samples = {
                    "controller": (
                        "package com.example.demo;\n"
                        "import org.springframework.web.bind.annotation.GetMapping;\n"
                        "import org.springframework.web.bind.annotation.RestController;\n\n"
                        "@RestController\n"
                        "public class HelloController {\n"
                        "    @GetMapping(\"/\")\n"
                        "    public String index() {\n"
                        "        return \"Hello from Spring Boot!\";\n"
                        "    }\n"
                        "}"
                    )
                }
            else:
                code_samples = {
                    "hello_world": (
                        "public class Main {\n"
                        "    public static void main(String[] args) {\n"
                        "        System.out.println(\"Hello from Java Core!\");\n"
                        "    }\n"
                        "}"
                    )
                }
        elif lang == "dart" or framework == "flutter":
            code_samples = {
                "hello_world": (
                    "import 'package:flutter/material.dart';\n\n"
                    "void main() => runApp(const MyApp());\n\n"
                    "class MyApp extends StatelessWidget {\n"
                    "  const MyApp({super.key});\n"
                    "  @override\n"
                    "  Widget build(BuildContext context) {\n"
                    "    return const MaterialApp(\n"
                    "      home: Scaffold(body: Center(child: Text('Hello Flutter'))),\n"
                    "    );\n"
                    "  }\n"
                    "}"
                )
            }
        else:
            code_samples = {
                "hello_world": (
                    f"// Hello world sample for {tech_stack}\n"
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
