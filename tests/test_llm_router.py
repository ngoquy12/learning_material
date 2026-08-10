# tests/test_llm_router.py
import unittest
import os
from core.llm_router import (
    AntigravityLLMRouter,
    resolve_model_tier_for_agent,
    TIER_1_FAST,
    TIER_2_REASONING,
    TIER_3_DEEP_CONTEXT
)

class TestAntigravityLLMRouter(unittest.TestCase):

    def test_tier_classification(self):
        """Verify agents are correctly classified into the appropriate model tier."""
        # Tier 1 (Fast & Light)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("quiz_validator"), TIER_1_FAST)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("syntax_linter"), TIER_1_FAST)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("tts_normalizer"), TIER_1_FAST)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("my_custom_validator"), TIER_1_FAST)

        # Tier 2 (High Reasoning)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("reading_creator"), TIER_2_REASONING)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("slide_creator"), TIER_2_REASONING)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("quiz_creator"), TIER_2_REASONING)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("unknown_agent"), TIER_2_REASONING)

        # Tier 3 (Deep Context & Code)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("enterprise_code_section_3"), TIER_3_DEEP_CONTEXT)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("hyperframes_writer_agent"), TIER_3_DEEP_CONTEXT)
        self.assertEqual(AntigravityLLMRouter.classify_agent_tier("session_video_script_agent"), TIER_3_DEEP_CONTEXT)

    def test_model_resolution(self):
        """Verify model resolution and context caching flag output."""
        model_t1, cache_t1 = AntigravityLLMRouter.resolve_model("quiz_validator")
        self.assertIn(model_t1, ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-3.6-flash-high"])
        self.assertFalse(cache_t1)

        model_t2, cache_t2 = AntigravityLLMRouter.resolve_model("reading_creator")
        self.assertEqual(model_t2, "gemini-3.6-flash-high")
        self.assertFalse(cache_t2)

        model_t3, cache_t3 = AntigravityLLMRouter.resolve_model("hyperframes_writer_agent")
        self.assertEqual(model_t3, "gemini-3.6-flash-high")
        self.assertTrue(cache_t3)

    def test_pro_reasoning_model_resolution(self):
        """Verify agents requiring Pro reasoning resolve to gemini-3.1-pro."""
        model_pro1, _ = AntigravityLLMRouter.resolve_model("objective_architect")
        self.assertEqual(model_pro1, "gemini-3.1-pro")

        model_pro2, _ = AntigravityLLMRouter.resolve_model("prerequisite_guard")
        self.assertEqual(model_pro2, "gemini-3.1-pro")

        model_pro3, _ = AntigravityLLMRouter.resolve_model("pm_reviewer")
        self.assertEqual(model_pro3, "gemini-3.1-pro")

    def test_env_override(self):
        """Verify FORCE_GEMINI_MODEL env var override takes precedence."""
        original_env = os.environ.get("GEMINI_MODEL")
        original_force = os.environ.get("FORCE_GEMINI_MODEL")
        try:
            os.environ["GEMINI_MODEL"] = "custom-gemini-test-model"
            os.environ["FORCE_GEMINI_MODEL"] = "true"
            model, _ = AntigravityLLMRouter.resolve_model("quiz_validator")
            self.assertEqual(model, "custom-gemini-test-model")
        finally:
            if original_env is not None:
                os.environ["GEMINI_MODEL"] = original_env
            else:
                os.environ.pop("GEMINI_MODEL", None)
            if original_force is not None:
                os.environ["FORCE_GEMINI_MODEL"] = original_force
            else:
                os.environ.pop("FORCE_GEMINI_MODEL", None)

    def test_fallback_candidates(self):
        """Verify fallback candidate listing works correctly."""
        fallbacks = AntigravityLLMRouter.get_fallback_candidates("quiz_validator", "gemini-1.5-flash")
        self.assertNotIn("gemini-1.5-flash", fallbacks)
        self.assertIn("gemini-3.6-flash-high", fallbacks)


if __name__ == "__main__":
    unittest.main()
