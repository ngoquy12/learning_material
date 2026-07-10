# core/observability.py
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

TRACE_LOG_PATH = "trace_logs.jsonl"

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
    Appends a detailed trace log of an Agent execution step to a local JSONL file.
    Calculates execution duration and saves structured metrics.
    """
    duration = time.time() - start_time
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "agent_name": agent_name,
        "session_id": session_id,
        "lesson_id": lesson_id,
        "duration_seconds": round(duration, 3),
        "prompt_summary": prompt_summary[:1000] if prompt_summary else "",
        "response_summary": response_summary[:1000] if response_summary else "",
        "token_cost": token_cost or {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }
    
    try:
        with open(TRACE_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"  [Observability Warning] Failed to write trace log: {e}")
