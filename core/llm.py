# core/llm.py
import os
import json
import time
import functools
from typing import Optional, Any

# Load dotenv if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Caching registry for Gemini Context Caching
_GEMINI_PROMPT_CACHES = {}


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
        # Map base name versions to caching-enabled versions
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
    if gemini_key:
        try:
            import google.generativeai as genai
            base_url = os.getenv("GEMINI_BASE_URL")
            if base_url:
                genai.configure(
                    api_key=gemini_key,
                    transport="rest",
                    client_options={"api_endpoint": base_url}
                )
            else:
                genai.configure(api_key=gemini_key)
            
            # Select model
            model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            
            generation_config: dict = {"max_output_tokens": 8192}
            if json_mode:
                generation_config["response_mime_type"] = "application/json"
                
            # Try prompt caching first
            cached_model = _get_cached_generative_model(model_name, system_prompt, generation_config)
            
            print(f"  [LLM] Waiting for response from {model_name} (Local Proxy)...")
            if cached_model:
                response = cached_model.generate_content(
                    user_prompt,
                    generation_config=generation_config,
                    request_options={"timeout": 120.0}
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
                    request_options={"timeout": 120.0}
                )
                
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
            print(f"  [LLM Warning] Gemini call failed: {e}. Falling back to OpenAI or templates...")
            
    # Setup OpenAI key fallback if not set but gemini_key is an OpenAI key
    if not openai_key and gemini_key and gemini_key.startswith("sk-"):
        openai_key = gemini_key

    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=openai_key,
                timeout=120.0,
                default_headers={
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "Elearning Agent"
                }
            )
            
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
                timeout=120.0
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


# ─────────────────────────────────────────────────────
# Semantic Cache Activation
# Bọc call_llm với SemanticCache sau khi định nghĩa xong.
# Không thay đổi interface hay logic gốc.
# Tắt cache bằng cách đặt SEMANTIC_CACHE_ENABLED=false trong .env
# ─────────────────────────────────────────────────────
try:
    from core.semantic_cache import with_semantic_cache
    call_llm = with_semantic_cache(call_llm)
    print("  [LLM] Semantic Cache activated. Duplicate LLM calls will be served from cache.")
except ImportError:
    pass  # Nếu semantic_cache chưa được cài, bỏ qua
