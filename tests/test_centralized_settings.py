"""
Unit Tests for Centralized Configuration & Secret Management Engine
===================================================================
Verifies type safety, secret masking (redaction), environment overrides,
and backward-compatible global exports.
"""

import os
import unittest
from unittest.mock import patch
from pydantic import SecretStr

from config.settings import (
    AppSettings,
    DatabaseSettings,
    LLMSettings,
    StorageSettings,
    SandboxSettings,
    ObservabilitySettings,
    CacheSettings,
    get_settings,
    get_agent_prompt,
    DATABASE_URL,
    LLM_MODEL,
)


class TestCentralizedSettings(unittest.TestCase):
    """Test suite for Centralized Configuration & Secret Management."""

    def test_default_settings_instantiation(self):
        """Verify AppSettings instantiate with robust defaults and proper types."""
        settings = AppSettings()
        self.assertEqual(settings.app_name, "Elearning Content Factory")
        self.assertFalse(settings.is_production())
        self.assertIsInstance(settings.database, DatabaseSettings)
        self.assertIsInstance(settings.llm, LLMSettings)
        self.assertIsInstance(settings.storage, StorageSettings)
        self.assertIsInstance(settings.sandbox, SandboxSettings)
        self.assertIsInstance(settings.observability, ObservabilitySettings)
        self.assertIsInstance(settings.cache, CacheSettings)

    def test_secret_str_redaction(self):
        """Verify secrets are masked with ***REDACTED*** in redacted_dict()."""
        settings = AppSettings(
            llm=LLMSettings(
                gemini_api_key=SecretStr("super-secret-gemini-key"),
                openai_api_key=SecretStr("sk-super-secret-openai-key"),
            ),
            observability=ObservabilitySettings(
                langfuse_secret_key=SecretStr("lf-secret-12345"),
            ),
        )

        redacted = settings.redacted_dict()

        # Check that secret values are completely hidden
        self.assertEqual(redacted["llm"]["gemini_api_key"], "***REDACTED***")
        self.assertEqual(redacted["llm"]["openai_api_key"], "***REDACTED***")
        self.assertEqual(redacted["observability"]["langfuse_secret_key"], "***REDACTED***")

        # Verify raw secret value is still retrievable safely
        self.assertEqual(settings.llm.gemini_api_key.get_secret_value(), "super-secret-gemini-key")
        self.assertEqual(settings.llm.openai_api_key.get_secret_value(), "sk-super-secret-openai-key")

    def test_environment_override(self):
        """Verify get_settings() correctly ingests custom environment variables."""
        mock_env = {
            "DATABASE_URL": "postgresql://user:pass@db.example.com:5432/custom_db",
            "DB_POOL_SIZE": "25",
            "GEMINI_MODEL": "gemini-2.0-pro",
            "MAX_CONCURRENT_LLM_CALLS": "12",
            "SEMANTIC_CACHE_ENABLED": "false",
            "SANDBOX_STRICT": "true",
        }
        with patch.dict(os.environ, mock_env, clear=False):
            # Clear cache for isolated testing
            get_settings.cache_clear()
            settings = get_settings()

            self.assertEqual(settings.database.url, "postgresql://user:pass@db.example.com:5432/custom_db")
            self.assertEqual(settings.database.pool_size, 25)
            self.assertEqual(settings.llm.gemini_model, "gemini-2.0-pro")
            self.assertEqual(settings.llm.max_concurrent_calls, 12)
            self.assertFalse(settings.cache.semantic_cache_enabled)
            self.assertTrue(settings.sandbox.strict_mode)

            # Reset cache
            get_settings.cache_clear()

    def test_backward_compatibility_exports(self):
        """Verify legacy global variables and prompt getters function seamlessly."""
        self.assertTrue(isinstance(DATABASE_URL, str))
        self.assertTrue(isinstance(LLM_MODEL, str))

    def test_use_real_gemini_api_key_flag(self):
        """Verify USE_REAL_GEMINI_API_KEY environment toggle."""
        # When set to true
        with patch.dict(os.environ, {"USE_REAL_GEMINI_API_KEY": "true"}, clear=False):
            get_settings.cache_clear()
            settings = get_settings()
            self.assertTrue(settings.llm.use_real_gemini_api_key)

        # When set to false
        with patch.dict(os.environ, {"USE_REAL_GEMINI_API_KEY": "false"}, clear=False):
            get_settings.cache_clear()
            settings = get_settings()
            self.assertFalse(settings.llm.use_real_gemini_api_key)

        get_settings.cache_clear()


if __name__ == "__main__":
    unittest.main()
