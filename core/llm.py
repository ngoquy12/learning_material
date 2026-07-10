# core/llm.py
import os
import json
import time
from typing import Optional

# Load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def call_llm(
    system_prompt: str,
    user_prompt: str,
    json_mode: bool = False,
    agent_name: str = "Unknown Agent",
    session_id: str = "",
    lesson_id: str = ""
) -> str:
    """
    Unified entry point for calling LLM (Gemini or OpenAI).
    Records execution trace to local observability logs.
    Falls back to returning None if no API keys are present (allowing fallback to templates).
    """
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    
    start_time = time.time()
    from core.observability import log_agent_call
    
    # Prioritize Gemini for Elearning Tools prompt guidelines
    # Prioritize Gemini for Elearning Tools prompt guidelines
    if gemini_key:
        base_url = os.getenv("GEMINI_BASE_URL")
        if base_url:
            # If GEMINI_BASE_URL is set, use OpenAI client to connect, because local proxy uses OpenAI protocol
            try:
                from openai import OpenAI
                api_base = base_url
                if not api_base.endswith("/v1") and not api_base.endswith("/v1/"):
                    api_base = api_base.rstrip("/") + "/v1"
                
                model_name = os.getenv("GEMINI_MODEL", "gemini-3-flash")
                client = OpenAI(api_key=gemini_key, base_url=api_base, timeout=8.0)
                
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": user_prompt})
                
                response_format = {"type": "json_object"} if json_mode else None
                
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    response_format=response_format,
                    temperature=0.2,
                    timeout=8.0
                )
                if response and response.choices:
                    result_text = response.choices[0].message.content.strip()
                    tokens = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                    try:
                        if response.usage:
                            tokens = {
                                "prompt_tokens": response.usage.prompt_tokens,
                                "completion_tokens": response.usage.completion_tokens,
                                "total_tokens": response.usage.total_tokens
                            }
                    except Exception:
                        pass
                    
                    log_agent_call(
                        agent_name=agent_name,
                        session_id=session_id,
                        lesson_id=lesson_id,
                        prompt_summary=f"System: {system_prompt}\nUser: {user_prompt}",
                        response_summary=result_text,
                        start_time=start_time,
                        token_cost=tokens
                    )
                    return result_text
            except Exception as e:
                print(f"  [LLM Warning] Gemini OpenAI proxy call failed: {e}. Trying standard SDK or fallback...")
        
        # Standard Google GenerativeAI SDK
        if not base_url:
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                
                # Select model
                model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
                
                generation_config = {}
                if json_mode:
                    generation_config["response_mime_type"] = "application/json"
                    
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_prompt,
                    generation_config=generation_config
                )
                
                response = model.generate_content(user_prompt, request_options={"timeout": 8.0})
                if response and response.text:
                    result_text = response.text.strip()
                    
                    # Try to extract tokens metadata
                    tokens = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                    try:
                        if hasattr(response, "usage_metadata") and response.usage_metadata:
                            tokens = {
                                "prompt_tokens": response.usage_metadata.prompt_token_count,
                                "completion_tokens": response.usage_metadata.candidates_token_count,
                                "total_tokens": response.usage_metadata.total_token_count
                            }
                    except Exception:
                        pass
                    
                    log_agent_call(
                        agent_name=agent_name,
                        session_id=session_id,
                        lesson_id=lesson_id,
                        prompt_summary=f"System: {system_prompt}\nUser: {user_prompt}",
                        response_summary=result_text,
                        start_time=start_time,
                        token_cost=tokens
                    )
                    return result_text
            except Exception as e:
                print(f"  [LLM Warning] Gemini standard SDK call failed: {e}. Trying OpenAI or fallback...")
            
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key, timeout=8.0)
            
            model_name = os.getenv("LLM_MODEL", "gpt-4o-mini")
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response_format = {"type": "json_object"} if json_mode else None
            
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                response_format=response_format,
                temperature=0.2,
                timeout=8.0
            )
            if response and response.choices:
                result_text = response.choices[0].message.content.strip()
                
                tokens = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                try:
                    if response.usage:
                        tokens = {
                            "prompt_tokens": response.usage.prompt_tokens,
                            "completion_tokens": response.usage.completion_tokens,
                            "total_tokens": response.usage.total_tokens
                        }
                except Exception:
                    pass
                
                log_agent_call(
                    agent_name=agent_name,
                    session_id=session_id,
                    lesson_id=lesson_id,
                    prompt_summary=f"System: {system_prompt}\nUser: {user_prompt}",
                    response_summary=result_text,
                    start_time=start_time,
                    token_cost=tokens
                )
                return result_text
        except Exception as e:
            print(f"  [LLM Warning] OpenAI call failed: {e}. Falling back to templates...")
            
    # Record trace log for fallback path
    try:
        log_agent_call(
            agent_name=agent_name,
            session_id=session_id,
            lesson_id=lesson_id,
            prompt_summary=f"System: {system_prompt}\nUser: {user_prompt}",
            response_summary="FALLBACK: No API keys configured or calls failed, using offline static templates.",
            start_time=start_time,
            token_cost={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        )
    except Exception:
        pass
        
    return ""
