# core/llm.py
import sys
import os
import json
import time
import functools
import threading
from typing import Optional, Any

# Reconfigure stdout/stderr encoding for Windows console compatibility immediately
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Caching registry for Gemini Context Caching
_GEMINI_PROMPT_CACHES = {}

# Concurrency Limiter for parallel execution (default max 4 concurrent LLM requests)
MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT_LLM_CALLS", "4"))
_LLM_SEMAPHORE = threading.Semaphore(MAX_CONCURRENT)

# High-complexity agents requiring deeper reasoning (Pro models)
HIGH_COMPLEXITY_AGENTS = {
    "objective_architect", "objective_reviewer", "prerequisite_guard",
    "pm_reviewer", "sandbox_agent", "knowledge_memory_agent",
    "strategic_agent", "prerequisite_guard_agent"
}

def resolve_model_name(agent_name: str, is_gemini: bool = True) -> str:
    """
    Dynamically select the LLM model based on Antigravity LLM Router agent tier mapping.
    """
    from core.llm_router import resolve_model_tier_for_agent
    model_name, _ = resolve_model_tier_for_agent(agent_name)
    return model_name

def _get_cached_generative_model(
    model_name: str,
    system_prompt: str,
    generation_config: dict
) -> Optional[Any]:
    """
    Attempts to retrieve or create a Gemini CachedContent and returns a GenerativeModel preloaded with it.
    If caching is disabled, prompt is too short (< 32,768 tokens), or cache creation fails, returns None.
    """
    if os.getenv("GEMINI_PROMPT_CACHING", "True").lower() not in ("true", "1", "yes"):
        return None

    try:
        import google.generativeai as genai
        from google.generativeai import caching
        import datetime

        # Ensure canonical model name format for caching
        canonical_model = model_name
        if not canonical_model.startswith("models/"):
            canonical_model = f"models/{canonical_model}"

        # Context caching is supported on specific model versions (e.g., gemini-1.5-flash-001)
        if canonical_model in ("models/gemini-1.5-flash", "models/gemini-1.5-flash-latest"):
            canonical_model = "models/gemini-1.5-flash-001"
        elif canonical_model in ("models/gemini-1.5-pro", "models/gemini-1.5-pro-latest"):
            canonical_model = "models/gemini-1.5-pro-001"

        # Count tokens of system prompt to ensure minimum requirement
        try:
            temp_model = genai.GenerativeModel(model_name=canonical_model)
            token_count_resp = temp_model.count_tokens(system_prompt)
            total_tokens = getattr(token_count_resp, "total_tokens", getattr(token_count_resp, "total_token_count", len(system_prompt) // 4))
        except Exception:
            total_tokens = len(system_prompt) // 4

        min_tokens = int(os.getenv("GEMINI_CACHE_MIN_TOKENS", "32768"))
        if total_tokens < min_tokens:
            return None

        cache_key = (canonical_model, hash(system_prompt))
        now = time.time()

        # Check existing cached content
        if cache_key in _GEMINI_PROMPT_CACHES:
            cache_obj, expire_at = _GEMINI_PROMPT_CACHES[cache_key]
            if now < expire_at:
                print(f"  [Prompt Cache] Cache HIT for {canonical_model} ({total_tokens} tokens).")
                return genai.GenerativeModel.from_cached_content(cached_content=cache_obj)

        print(f"  [Prompt Cache] Cache MISS for {canonical_model} ({total_tokens} tokens). Creating new cached content...")
        
        # Create cached content with 30-minute TTL
        cache_obj = caching.CachedContent.create(
            model=canonical_model,
            display_name=f"prompt_cache_{abs(hash(system_prompt)) % 10000000}",
            contents=[system_prompt],
            ttl=datetime.timedelta(minutes=30)
        )
        
        # Save cache and expiration (25 minutes safety margin)
        _GEMINI_PROMPT_CACHES[cache_key] = (cache_obj, now + 25 * 60)
        
        return genai.GenerativeModel.from_cached_content(cached_content=cache_obj)

    except Exception as e:
        print(f"  [Prompt Cache Warning] Failed to initialize prompt caching: {e}. Falling back to standard model call.")
        return None


def with_retry(max_retries=3, initial_delay=2, backoff_factor=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if result:
                        return result
                    elif attempt < max_retries - 1:
                        print(f"  [LLM Retry] Empty response. Retrying in {delay} seconds (Attempt {attempt + 1}/{max_retries})...")
                        time.sleep(delay)
                        delay *= backoff_factor
                except Exception as e:
                    if attempt < max_retries - 1:
                        print(f"  [LLM Retry] Error: {e}. Retrying in {delay} seconds (Attempt {attempt + 1}/{max_retries})...")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        print(f"  [LLM Retry] Failed after {max_retries} attempts.")
            return func(*args, **kwargs) # Last attempt without catching
        return wrapper
    return decorator


@with_retry(max_retries=4, initial_delay=3, backoff_factor=2)
def call_llm(
    system_prompt: str,
    user_prompt: str,
    json_mode: bool = False,
    agent_name: str = "Unknown Agent",
    session_id: str = "",
    lesson_id: str = "",
    response_schema: Optional[Any] = None
) -> str:
    """
    Unified entry point for calling LLM (Gemini or OpenAI).
    Includes Dynamic Model Routing and Thread-Safe Concurrency Limiter.
    Records execution trace to local observability logs.
    Falls back to returning None if no API keys are present (allowing fallback to templates).
    """
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")

    if not (gemini_key or openai_key):
        raise RuntimeError(
            f"❌ [LỖI THIẾU API KEY] Agent '{agent_name}': Không tìm thấy GEMINI_API_KEY hoặc OPENAI_API_KEY trong .env. "
            f"Hệ thống tuyệt đối KHÔNG chạy fallback tĩnh. Vui lòng bổ sung API Key."
        )

    start_time = time.time()
    from core.observability import log_agent_call

    # Universal Agent Contract: Skill/Instructions in English, Output in 100% Accented Vietnamese
    universal_directive = (
        "UNIVERSAL AGENT CONTRACT & ROLE DIRECTIVE:\n"
        "1. Skill Directives & System Instructions: Drafted in precise, unambiguous English for maximum instruction adherence.\n"
        "2. 100% Accented Vietnamese Output Contract: All final generated output (reading materials, slides, exercises, video scripts, code comments, quizzes, UI text) MUST ALWAYS be written in 100% ACCENTED VIETNAMESE (Tiếng Việt có dấu chuẩn sản xuất).\n"
    )
    if system_prompt and "UNIVERSAL AGENT CONTRACT" not in system_prompt:
        system_prompt = f"{universal_directive}\n\n{system_prompt}"

    # Acquire semaphore to prevent 429 rate limits during parallel node execution
    with _LLM_SEMAPHORE:

        # Route OpenAI-compatible proxy endpoints (or sk- style keys) directly to OpenAI SDK for ultra-fast performance
        base_url = os.getenv("GEMINI_BASE_URL")
        if (gemini_key and gemini_key.startswith("sk-")) or (base_url and ("127.0.0.1" in base_url or "localhost" in base_url or ":804" in base_url)):
            try:
                from openai import OpenAI
                api_endpoint = base_url.rstrip("/") if base_url else "http://127.0.0.1:8045"
                if not api_endpoint.endswith("/v1"):
                    api_endpoint += "/v1"
                client = OpenAI(base_url=api_endpoint, api_key=gemini_key)
                model_name = resolve_model_name(agent_name, is_gemini=True)
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                kwargs = {"model": model_name, "messages": messages, "temperature": 0.7, "timeout": 90.0}
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}
                
                from core.llm_router import AntigravityLLMRouter
                tier = AntigravityLLMRouter.classify_agent_tier(agent_name)
                print(f"  [LLM Router - Antigravity Tier ({tier})] {agent_name} -> Model: {model_name} @ {api_endpoint}...")
                response = client.chat.completions.create(**kwargs)
                if response and response.choices and response.choices[0].message.content:
                    result_text = response.choices[0].message.content.strip()
                    log_agent_call(
                        agent_name=agent_name,
                        session_id=session_id,
                        lesson_id=lesson_id,
                        prompt_summary=f"System: {system_prompt}\nUser: {user_prompt}",
                        response_summary=result_text,
                        start_time=start_time,
                        token_cost={"total_tokens": getattr(response.usage, "total_tokens", 0) if hasattr(response, "usage") and response.usage else len(result_text) // 4}
                    )
                    return result_text
                else:
                    raise RuntimeError("Empty response from Antigravity Proxy")
            except Exception as proxy_err:
                print(f"  [LLM Router - Proxy Error] {proxy_err}")
                raise proxy_err  # Re-raise to trigger with_retry instead of falling through to native SDK with sk- key!

        # Prioritize Gemini Native SDK ONLY for official AI Studio keys (starting with AIzaSy)
        if gemini_key and gemini_key.startswith("AIzaSy"):
            try:
                import google.generativeai as genai
                if base_url and not base_url.startswith("http://127.0.0.1"):
                    genai.configure(
                        api_key=gemini_key,
                        transport="rest",
                        client_options={"api_endpoint": base_url}
                    )
                else:
                    genai.configure(api_key=gemini_key)
                
                # Dynamic Model Selection based on Agent Complexity
                model_name = resolve_model_name(agent_name, is_gemini=True)
                
                generation_config: dict = {"max_output_tokens": 65536}
                if json_mode:
                    generation_config["response_mime_type"] = "application/json"
                if response_schema:
                    generation_config["response_mime_type"] = "application/json"
                    generation_config["response_schema"] = response_schema
                    
                # Try calling with response_schema
                try:
                    cached_model = _get_cached_generative_model(model_name, system_prompt, generation_config)
                    print(f"  [LLM Router] {agent_name} -> Model: {model_name}...")
                    if cached_model:
                        response = cached_model.generate_content(
                            user_prompt,
                            generation_config=generation_config,
                            request_options={"timeout": 300.0}
                        )
                    else:
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=system_prompt,
                            generation_config=generation_config
                        )
                        response = model.generate_content(
                            user_prompt,
                            generation_config=generation_config,
                            request_options={"timeout": 300.0}
                        )
                    
                    if response and response.text:
                        result_text = response.text.strip()
                        if response_schema:
                            # Verify if it parses as valid JSON
                            cleaned_verify = result_text
                            if cleaned_verify.startswith("```json"):
                                cleaned_verify = cleaned_verify[7:]
                            if cleaned_verify.startswith("```"):
                                cleaned_verify = cleaned_verify[3:]
                            if cleaned_verify.endswith("```"):
                                cleaned_verify = cleaned_verify[:-3]
                            json.loads(cleaned_verify.strip())
                    else:
                        if response_schema:
                            raise ValueError("Gemini returned empty or invalid response under response_schema")
                except Exception as schema_err:
                    if response_schema:
                        print(f"  [LLM Schema Fallback] Gemini Structured Output failed or returned malformed JSON: {schema_err}. Retrying WITHOUT schema...")
                        generation_config_no = {"max_output_tokens": 65536}
                        if json_mode:
                            generation_config_no["response_mime_type"] = "application/json"
                        
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=system_prompt,
                            generation_config=generation_config_no
                        )
                        response = model.generate_content(
                            user_prompt,
                            generation_config=generation_config_no,
                            request_options={"timeout": 300.0}
                        )
                    else:
                        raise schema_err
                    
                if response and response.text:
                    result_text = response.text.strip()
                    
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
                print(f"  [LLM Warning] Gemini call failed: {e}.")
                if ("127.0.0.1" in str(e) or "8045" in str(e) or "10061" in str(e)) and gemini_key and gemini_key.startswith("AIzaSy"):
                    print("  [LLM Auto-Bypass Proxy] Thử lại kết nối trực tiếp tới Google AI API (bỏ qua local proxy 127.0.0.1:8045)...")
                    try:
                        genai.configure(api_key=gemini_key)
                        model_name = resolve_model_name(agent_name, is_gemini=True)
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=system_prompt,
                            generation_config=generation_config
                        )
                        response = model.generate_content(
                            user_prompt,
                            generation_config=generation_config,
                            request_options={"timeout": 300.0}
                        )
                        if response and response.text:
                            return response.text.strip()
                    except Exception as retry_err:
                        print(f"  [LLM Direct Fallback Error] {retry_err}")
                
        # Only route to OpenAI fallback if explicit OPENAI_API_KEY is provided
        if openai_key and openai_key.startswith("sk-") and os.getenv("OPENAI_API_KEY"):
            try:
                from openai import OpenAI
                client = OpenAI(
                    api_key=openai_key,
                    timeout=300.0,
                    default_headers={
                        "HTTP-Referer": "http://localhost:3000",
                        "X-Title": "Elearning Agent"
                    }
                )
                
                model_name = resolve_model_name(agent_name, is_gemini=False)
                
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                
                print(f"  [LLM Router] {agent_name} -> OpenAI Model: {model_name}...")
                if response_schema:
                    try:
                        response = client.beta.chat.completions.parse(
                            model=model_name,
                            messages=messages,
                            response_format=response_schema,
                            temperature=0.2,
                            timeout=300.0
                        )
                        if response and response.choices and response.choices[0].message.content:
                            result_text = response.choices[0].message.content.strip()
                            json.loads(result_text)
                        else:
                            raise ValueError("OpenAI returned empty or invalid response under response_schema")
                    except Exception as schema_err:
                        print(f"  [LLM Schema Fallback] OpenAI Structured Output failed: {schema_err}. Retrying WITHOUT schema...")
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=messages,
                            response_format={"type": "json_object"} if json_mode else None,
                            temperature=0.2,
                            timeout=300.0
                        )
                else:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=messages,
                        response_format={"type": "json_object"} if json_mode else None,
                        temperature=0.2,
                        timeout=300.0
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
            
        raise RuntimeError(
            f"❌ [LỖI GỌI LLM THẤT BẠI] Agent '{agent_name}': Không thể nhận phản hồi từ LLM (Gemini/OpenAI) "
            f"do lỗi kết nối mạng, vượt quá Quota limit hoặc hết Token. Pipeline lập tức dừng để bảo toàn dữ liệu."
        )


# ─────────────────────────────────────────────────────
# Semantic Cache Activation
# ─────────────────────────────────────────────────────
try:
    from core.semantic_cache import with_semantic_cache
    call_llm = with_semantic_cache(call_llm)
    print("  [LLM] Semantic Cache activated. Duplicate LLM calls will be served from cache.")
except ImportError:
    pass


# ─────────────────────────────────────────────────────
# Gemini Vision — call_llm_with_images()
# For multi-modal prompts that include PNG screenshots alongside text.
# Used by reading_ui_reviewer.py to analyze HTML page UI quality.
# ─────────────────────────────────────────────────────
def call_llm_with_images(
    system_prompt: str,
    user_prompt: str,
    image_paths: list,
    agent_name: str = "Vision_Agent",
    session_id: str = "",
    lesson_id: str = ""
) -> str:
    """
    Send a multi-modal request to Gemini Vision with text + PNG images.
    image_paths: list of absolute file paths to PNG screenshots.
    Returns LLM text response.
    """
    import base64
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        return ""

    try:
        import google.generativeai as genai

        base_url = os.getenv("GEMINI_BASE_URL")
        if base_url:
            genai.configure(api_key=gemini_key, transport="rest",
                            client_options={"api_endpoint": base_url})
        else:
            genai.configure(api_key=gemini_key)

        # Use same model as call_llm — ensures compatibility with local proxy
        model_name = resolve_model_name(agent_name, is_gemini=True)

        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt,
            generation_config={"max_output_tokens": 16384}
        )

        # Build content parts: images first, then text
        parts = []
        for img_path in image_paths:
            if not os.path.exists(img_path):
                continue
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": base64.b64encode(img_bytes).decode("utf-8")
                }
            })

        parts.append({"text": user_prompt})

        print(f"  [Vision LLM] {agent_name} -> Model: {model_name} | Images: {len(image_paths)}...")
        response = model.generate_content(parts, request_options={"timeout": 120.0})

        if response and response.text:
            return response.text.strip()
        return ""

    except Exception as e:
        print(f"  [Vision LLM Error] {agent_name}: {e}")
        return ""
