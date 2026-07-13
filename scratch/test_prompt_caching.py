# scratch/test_prompt_caching.py
import sys
import os
import time

# Put learning material workspace on search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Create a mock for google.generativeai to test caching logic offline
class MockCachedContent:
    def __init__(self, model, display_name, contents, ttl):
        self.model = model
        self.display_name = display_name
        self.contents = contents
        self.ttl = ttl
        self.name = f"projects/mock/cachedContents/{display_name}"

    @classmethod
    def create(cls, model, display_name, contents, ttl):
        return cls(model, display_name, contents, ttl)

class MockCachingModule:
    CachedContent = MockCachedContent

class MockGenerativeModel:
    def __init__(self, model_name=None, system_instruction=None, generation_config=None, cached_content=None):
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.generation_config = generation_config
        self.cached_content = cached_content

    @staticmethod
    def from_cached_content(cached_content):
        return MockGenerativeModel(cached_content=cached_content)

    def count_tokens(self, text):
        class TokenResponse:
            total_token_count = len(text) // 4
        return TokenResponse()

# Patch the sys.modules before importing
sys.modules["google.generativeai.caching"] = MockCachingModule
sys.modules["google.generativeai"] = sys.modules.get("google.generativeai") or type("MockGenAI", (object,), {
    "GenerativeModel": MockGenerativeModel,
    "caching": MockCachingModule
})

# Now import the caching helper
from core.llm import _get_cached_generative_model, _GEMINI_PROMPT_CACHES

def run_tests():
    print("====================================================")
    print("Testing core/llm.py Gemini Context Caching Workflow")
    print("====================================================")

    # Clean the registry before test
    _GEMINI_PROMPT_CACHES.clear()

    # System prompt simulating a large template (approx 140,000 characters ~ 35,000 tokens)
    large_system_prompt = "INSTRUCTION: " + ("A" * 140000)
    # System prompt simulating a small template (approx 1,000 characters ~ 250 tokens)
    small_system_prompt = "INSTRUCTION: " + ("A" * 1000)

    # Test 1: Caching disabled via environment variable
    print("\n--- Test 1: Caching Disabled via Env Var ---")
    os.environ["GEMINI_PROMPT_CACHING"] = "False"
    res = _get_cached_generative_model("gemini-1.5-flash", large_system_prompt, {})
    print(f"Result: {res}")
    assert res is None, "Should return None when caching is disabled"

    # Test 2: Prompt too small for caching (Below 32,768 tokens)
    print("\n--- Test 2: Prompt Too Small (Below Limit) ---")
    os.environ["GEMINI_PROMPT_CACHING"] = "True"
    os.environ["GEMINI_CACHE_MIN_TOKENS"] = "32768"
    res = _get_cached_generative_model("gemini-1.5-flash", small_system_prompt, {})
    print(f"Result: {res}")
    assert res is None, "Should return None when prompt does not meet token minimum"

    # Test 3: Cache MISS on first large prompt
    print("\n--- Test 3: Cache MISS on First Request ---")
    os.environ["GEMINI_CACHE_MIN_TOKENS"] = "1000" # set low for testing
    res_miss = _get_cached_generative_model("gemini-1.5-flash", large_system_prompt, {})
    print(f"Model instanced: {res_miss}")
    print(f"Cached Content object: {res_miss.cached_content}")
    assert res_miss is not None, "Should successfully create cached model"
    assert res_miss.cached_content.model == "models/gemini-1.5-flash-001", "Should rewrite base model name to canonical cached name"

    # Test 4: Cache HIT on second large prompt
    print("\n--- Test 4: Cache HIT on Subsequent Request ---")
    res_hit = _get_cached_generative_model("gemini-1.5-flash", large_system_prompt, {})
    print(f"Model instanced: {res_hit}")
    print(f"Cached Content object: {res_hit.cached_content}")
    assert res_hit is not None
    assert res_hit.cached_content == res_miss.cached_content, "Cache HIT must return the same cached object"

    # Test 5: Cache expiration validation
    print("\n--- Test 5: Cache Expiration Check ---")
    # Manually expire the cache key
    cache_key = ("models/gemini-1.5-flash-001", hash(large_system_prompt))
    assert cache_key in _GEMINI_PROMPT_CACHES
    cache_obj, old_expire = _GEMINI_PROMPT_CACHES[cache_key]
    _GEMINI_PROMPT_CACHES[cache_key] = (cache_obj, time.time() - 10) # 10s in the past

    # Calling again should trigger a MISS and create a new cached content
    res_expired_miss = _get_cached_generative_model("gemini-1.5-flash", large_system_prompt, {})
    new_expire = _GEMINI_PROMPT_CACHES[cache_key][1]
    print(f"Expired Miss result: {res_expired_miss}")
    assert new_expire > old_expire, "Expired cache key must be refreshed with a new cache object"

    print("\n====================================================")
    print("ALL PROMPT CACHING WORKFLOW TESTS PASSED - SUCCESS")
    print("====================================================")

if __name__ == "__main__":
    run_tests()
