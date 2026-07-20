# core/observability.py
import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, Optional

TRACE_LOG_PATH = "trace_logs.jsonl"

# 1. Try importing Langfuse SDK
_langfuse_client = None
try:
    from langfuse import Langfuse  # type: ignore
    from config.settings import LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST
    if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY:
        _langfuse_client = Langfuse(
            public_key=LANGFUSE_PUBLIC_KEY,
            secret_key=LANGFUSE_SECRET_KEY,
            host=LANGFUSE_HOST
        )
except ImportError:
    pass

# 2. Try importing OpenTelemetry SDK
_otel_enabled = False
_tracer = None
try:
    from opentelemetry import trace  # type: ignore
    from opentelemetry.sdk.trace import TracerProvider  # type: ignore
    from opentelemetry.sdk.trace.export import BatchSpanProcessor  # type: ignore
    from opentelemetry.sdk.resources import Resource  # type: ignore
    
    # Check if a custom endpoint or tracer provider is already active
    if not trace.get_tracer_provider().__class__.__name__ == "ProxyTracerProvider":
        _otel_enabled = True
        _tracer = trace.get_tracer("learning_material_factory")
    else:
        # Initialize standard provider with local resources
        resource = Resource(attributes={"service.name": "learning-material-factory"})
        provider = TracerProvider(resource=resource)
        
        # Configure OTLP Exporter if endpoint is specified
        from config.settings import OTEL_EXPORTER_OTLP_ENDPOINT
        if OTEL_EXPORTER_OTLP_ENDPOINT:
            try:
                # Try gRPC exporter first
                try:
                    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter  # type: ignore
                    exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)
                except ImportError:
                    # Fallback to HTTP protobuf exporter
                    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter  # type: ignore
                    exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)
                provider.add_span_processor(BatchSpanProcessor(exporter))
            except Exception as exp_err:
                print(f"  [Observability Warning] Failed to initialize OTLP Span Exporter: {exp_err}")
                pass
                
        trace.set_tracer_provider(provider)
        _otel_enabled = True
        _tracer = trace.get_tracer("learning_material_factory")
except ImportError:
    pass

def log_agent_call(
    agent_name: str,
    session_id: str,
    lesson_id: str,
    prompt_summary: str,
    response_summary: str,
    start_time: float,
    token_cost: Optional[Dict[str, int]] = None
):
    """
    Standardized observability dispatcher:
    1. Writes trace logs locally in JSONL following OpenTelemetry GenAI Semantic Conventions.
    2. Sends tracing spans to OpenTelemetry collectors (e.g. Phoenix, Honeycomb) if active.
    3. Logs generations to Langfuse if configured.
    """
    duration = time.time() - start_time
    tokens = token_cost or {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    
    # 1. Generate unique identifier for this span / trace segment
    trace_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())[:16]
    
    # Auto-detect AI model names from environment configurations
    model_name = os.getenv("GEMINI_MODEL") or os.getenv("LLM_MODEL") or "gemini-1.5-flash"
    ai_system = "Google Gemini" if "gemini" in model_name.lower() else "OpenAI"

    # 2. Local OpenTelemetry Semantic Log entry creation
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trace_id": trace_id,
        "span_id": span_id,
        "agent_name": agent_name,
        "session_id": session_id,
        "lesson_id": lesson_id,
        "duration_seconds": round(duration, 3),
        "prompt_summary": prompt_summary[:1500] if prompt_summary else "",
        "response_summary": response_summary[:1500] if response_summary else "",
        # OpenTelemetry standard GenAI attributes mapping
        "gen_ai.system": ai_system,
        "gen_ai.request.model": model_name,
        "gen_ai.response.model": model_name,
        "gen_ai.usage.input_tokens": tokens.get("prompt_tokens", 0),
        "gen_ai.usage.output_tokens": tokens.get("completion_tokens", 0),
        "gen_ai.usage.total_tokens": tokens.get("total_tokens", 0)
    }

    # Write to trace_logs.jsonl
    try:
        with open(TRACE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"  [Observability Warning] Failed to write trace log: {e}")

    # 3. OpenTelemetry Active Tracing
    if _otel_enabled and _tracer:
        try:
            with _tracer.start_as_current_span(agent_name) as span:
                span.set_attribute("gen_ai.system", ai_system)
                span.set_attribute("gen_ai.request.model", model_name)
                span.set_attribute("gen_ai.usage.input_tokens", tokens.get("prompt_tokens", 0))
                span.set_attribute("gen_ai.usage.output_tokens", tokens.get("completion_tokens", 0))
                span.set_attribute("session_id", session_id)
                span.set_attribute("lesson_id", lesson_id)
                span.set_attribute("duration_seconds", round(duration, 3))
        except Exception as otel_err:
            pass

    # 4. Langfuse Generation capturing
    if _langfuse_client:
        try:
            _langfuse_client.generation(
                name=agent_name,
                trace_id=session_id.replace(" ", "_"), # Map session ID as trace ID for grouping
                input=prompt_summary,
                output=response_summary,
                model=model_name,
                usage={
                    "input": tokens.get("prompt_tokens", 0),
                    "output": tokens.get("completion_tokens", 0),
                    "total": tokens.get("total_tokens", 0)
                },
                metadata={
                    "lesson_id": lesson_id,
                    "duration_seconds": round(duration, 3),
                    "trace_id_uuid": trace_id
                }
            )
        except Exception as lf_err:
            print(f"[Observability Langfuse Warning] Failed to dispatch generation trace: {lf_err}")

