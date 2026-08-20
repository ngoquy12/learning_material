"""
Centralized Configuration and Secret Management Engine
======================================================
Enterprise-grade, type-safe settings management using Pydantic Settings and SecretStr.
Supports environment loading (.env), secret masking/redaction, fail-fast validation,
and backward-compatible global variable aliases.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional
import yaml
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
PROMPTS_FILE = CONFIG_DIR / "prompts.yaml"


class DatabaseSettings(BaseModel):
    """Database connection and connection pool configuration."""
    url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/elearning_factory",
        description="Database connection URL string (PostgreSQL/SQLite/MySQL)",
    )
    pool_size: int = Field(default=5, ge=1, le=100, description="Database connection pool size")
    max_overflow: int = Field(default=10, ge=0, le=100, description="Maximum overflow connections")
    pool_timeout: float = Field(default=30.0, ge=1.0, description="Connection pool acquire timeout (seconds)")


class LLMSettings(BaseModel):
    """Large Language Model (LLM) and SLM provider configuration."""
    # API Keys (Protected via SecretStr)
    gemini_api_key: Optional[SecretStr] = Field(default=None, description="Google Gemini / Vertex API Key")
    openai_api_key: Optional[SecretStr] = Field(default=None, description="OpenAI API Key")

    # Model names & URLs
    gemini_model: str = Field(default="gemini-1.5-flash", description="Default Google Gemini model")
    openai_model: str = Field(default="gpt-4o-mini", description="Default OpenAI model")
    gemini_base_url: Optional[str] = Field(default=None, description="Custom Gemini API base endpoint")
    local_slm_url: Optional[str] = Field(default=None, description="Local SLM / Ollama / vLLM endpoint URL")

    # Rate Limiting & Concurrency Guardrails
    max_concurrent_calls: int = Field(default=4, ge=1, le=64, description="Max concurrent LLM worker calls")
    max_rpm: float = Field(default=60.0, ge=1.0, description="Max allowed LLM requests per minute")
    max_burst_capacity: float = Field(default=10.0, ge=1.0, description="Max token bucket burst capacity")

    # Context & Prompt Caching
    gemini_prompt_caching: bool = Field(default=True, description="Enable Gemini Prompt Caching")
    gemini_cache_min_tokens: int = Field(default=32768, ge=1024, description="Minimum tokens to trigger prompt cache")


class StorageSettings(BaseModel):
    """Storage provider settings (Local Filesystem or S3-Compatible Object Store)."""
    provider: str = Field(default="local", description="Storage backend ('local' or 's3')")
    s3_bucket_name: str = Field(default="elearning-artifacts", description="S3 bucket name")
    s3_endpoint_url: Optional[str] = Field(default=None, description="Custom S3 / MinIO endpoint URL")
    s3_region: str = Field(default="us-east-1", description="AWS S3 region")
    aws_access_key_id: Optional[SecretStr] = Field(default=None, description="AWS S3 Access Key ID")
    aws_secret_access_key: Optional[SecretStr] = Field(default=None, description="AWS S3 Secret Access Key")


class SandboxSettings(BaseModel):
    """Code execution sandbox settings (Docker / E2B / Local fallback)."""
    provider: str = Field(default="docker", description="Sandbox backend ('docker', 'e2b', 'local')")
    strict_mode: bool = Field(default=False, description="Strict sandbox isolation mode")
    timeout_seconds: int = Field(default=5, ge=1, le=120, description="Max script execution timeout in seconds")
    memory_limit: str = Field(default="256m", description="Max container memory allocation")
    cpus: str = Field(default="0.5", description="Max container CPU quota")
    e2b_api_key: Optional[SecretStr] = Field(default=None, description="E2B Code Interpreter API Key")


class ObservabilitySettings(BaseModel):
    """Telemetry, tracing, and observability configuration (Langfuse / OpenTelemetry)."""
    langfuse_public_key: Optional[str] = Field(default=None, description="Langfuse Public Key")
    langfuse_secret_key: Optional[SecretStr] = Field(default=None, description="Langfuse Secret Key")
    langfuse_host: str = Field(default="https://cloud.langfuse.com", description="Langfuse host URL")
    otel_exporter_endpoint: Optional[str] = Field(default=None, description="OpenTelemetry OTLP exporter endpoint")
    log_level: str = Field(default="INFO", description="Application logging level (DEBUG, INFO, WARNING, ERROR)")


class CacheSettings(BaseModel):
    """Semantic caching and deduplication configuration."""
    semantic_cache_enabled: bool = Field(default=True, description="Toggle semantic caching engine")
    similarity_threshold: float = Field(default=0.88, ge=0.0, le=1.0, description="Cosine similarity threshold for cache hits")
    max_age_days: int = Field(default=30, ge=1, le=365, description="Cache entry TTL in days")


class AppSettings(BaseSettings):
    """
    Centralized Application Configuration & Secret Management
    Loads variables from system environment and `.env` file automatically.
    """
    # Environment & Deployment
    app_name: str = Field(default="Elearning Content Factory", description="Application Title")
    app_version: str = Field(default="0.1.0", description="Semantic Application Version")
    env: str = Field(default="development", description="Deployment environment: development, staging, production")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Modular Domain Sub-settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    sandbox: SandboxSettings = Field(default_factory=SandboxSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    def is_production(self) -> bool:
        """Return True if running in production mode."""
        return self.env.lower() in ("production", "prod")

    def redacted_dict(self) -> Dict[str, Any]:
        """
        Return a safe dictionary representation of settings where sensitive
        secrets and API keys are masked with '***REDACTED***' for safe logging.
        """
        def _sanitize(obj: Any) -> Any:
            if isinstance(obj, SecretStr):
                return "***REDACTED***" if obj.get_secret_value() else None
            if isinstance(obj, BaseModel):
                return {k: _sanitize(v) for k, v in obj.__dict__.items()}
            if isinstance(obj, dict):
                return {k: _sanitize(v) for k, v in obj.items()}
            return obj

        return _sanitize(self)


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """
    Singleton factory for retrieving cached application settings.
    Automatically merges environment variables with defaults.
    """
    # Auto-populate nested keys from flat environment variables for backward compatibility
    db_url = os.getenv("DATABASE_URL")
    db_pool = os.getenv("DB_POOL_SIZE")
    db_overflow = os.getenv("DB_MAX_OVERFLOW")
    db_timeout = os.getenv("DB_POOL_TIMEOUT")

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL") or os.getenv("LLM_MODEL")
    gemini_base = os.getenv("GEMINI_BASE_URL")
    slm_url = os.getenv("LOCAL_SLM_URL")
    max_concurrent = os.getenv("MAX_CONCURRENT_LLM_CALLS")
    max_rpm = os.getenv("MAX_LLM_RPM")

    storage_provider = os.getenv("STORAGE_PROVIDER")
    s3_bucket = os.getenv("S3_BUCKET_NAME")
    s3_endpoint = os.getenv("S3_ENDPOINT_URL")

    sandbox_provider = os.getenv("SANDBOX_PROVIDER")
    sandbox_strict = os.getenv("SANDBOX_STRICT")
    sandbox_timeout = os.getenv("SANDBOX_TIMEOUT")
    e2b_key = os.getenv("E2B_API_KEY")

    langfuse_pk = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_sk = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_host = os.getenv("LANGFUSE_HOST")
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

    cache_enabled = os.getenv("SEMANTIC_CACHE_ENABLED")
    cache_threshold = os.getenv("CACHE_SIMILARITY_THRESHOLD")
    cache_age = os.getenv("CACHE_MAX_AGE_DAYS")

    # Build typed sub-configs
    database_cfg = DatabaseSettings(
        url=db_url or "postgresql://postgres:postgres@localhost:5432/elearning_factory",
        pool_size=int(db_pool) if db_pool else 5,
        max_overflow=int(db_overflow) if db_overflow else 10,
        pool_timeout=float(db_timeout) if db_timeout else 30.0,
    )

    llm_cfg = LLMSettings(
        gemini_api_key=SecretStr(gemini_key) if gemini_key else None,
        openai_api_key=SecretStr(openai_key) if openai_key else None,
        gemini_model=gemini_model or "gemini-1.5-flash",
        gemini_base_url=gemini_base,
        local_slm_url=slm_url,
        max_concurrent_calls=int(max_concurrent) if max_concurrent else 4,
        max_rpm=float(max_rpm) if max_rpm else 60.0,
    )

    storage_cfg = StorageSettings(
        provider=storage_provider or "local",
        s3_bucket_name=s3_bucket or "elearning-artifacts",
        s3_endpoint_url=s3_endpoint,
    )

    sandbox_cfg = SandboxSettings(
        provider=sandbox_provider or "docker",
        strict_mode=sandbox_strict.lower() in ("true", "1", "yes") if sandbox_strict else False,
        timeout_seconds=int(sandbox_timeout) if sandbox_timeout else 5,
        e2b_api_key=SecretStr(e2b_key) if e2b_key else None,
    )

    observability_cfg = ObservabilitySettings(
        langfuse_public_key=langfuse_pk,
        langfuse_secret_key=SecretStr(langfuse_sk) if langfuse_sk else None,
        langfuse_host=langfuse_host or "https://cloud.langfuse.com",
        otel_exporter_endpoint=otel_endpoint,
    )

    cache_cfg = CacheSettings(
        semantic_cache_enabled=cache_enabled.lower() in ("true", "1", "yes") if cache_enabled else True,
        similarity_threshold=float(cache_threshold) if cache_threshold else 0.88,
        max_age_days=int(cache_age) if cache_age else 30,
    )

    return AppSettings(
        database=database_cfg,
        llm=llm_cfg,
        storage=storage_cfg,
        sandbox=sandbox_cfg,
        observability=observability_cfg,
        cache=cache_cfg,
    )


# =========================================================================
# Backward-Compatibility Global Exports & Prompt Helpers
# =========================================================================

# Load System Prompts
PROMPTS: Dict[str, Any] = {}
if PROMPTS_FILE.exists():
    try:
        with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
            PROMPTS = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Warning: Failed to load prompts.yaml: {e}")


def get_agent_prompt(agent_name: str) -> dict:
    """Helper to get prompt persona and task for a given agent name."""
    return PROMPTS.get(agent_name, {"Persona": "", "Task": ""})


# Global accessors (aliases for backward compatibility across existing modules)
_default_settings = get_settings()

DATABASE_URL = _default_settings.database.url
DB_POOL_SIZE = _default_settings.database.pool_size
DB_MAX_OVERFLOW = _default_settings.database.max_overflow
DB_POOL_TIMEOUT = _default_settings.database.pool_timeout

LLM_API_KEY = _default_settings.llm.openai_api_key.get_secret_value() if _default_settings.llm.openai_api_key else ""
LLM_MODEL = _default_settings.llm.gemini_model

LANGFUSE_PUBLIC_KEY = _default_settings.observability.langfuse_public_key or ""
LANGFUSE_SECRET_KEY = _default_settings.observability.langfuse_secret_key.get_secret_value() if _default_settings.observability.langfuse_secret_key else ""
LANGFUSE_HOST = _default_settings.observability.langfuse_host
OTEL_EXPORTER_OTLP_ENDPOINT = _default_settings.observability.otel_exporter_endpoint or ""
