# scripts/build_slm_fine_tune_dataset.py
"""
Dataset Generator Utility for Fine-Tuning Small Language Models (Qwen2.5-Coder / Llama-3.1-Coder).
Extracts Enterprise domain rules, pedagogical code guidelines, and enterprise scenarios
into standard JSONL LoRA training pairs formatted as {"instruction", "input", "output"}.
"""

import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.domain_adapters import DOMAIN_RULES, ENTERPRISE_SCENARIOS

OUTPUT_DATASET_PATH = Path("storage") / "slm_finetune_dataset.jsonl"

def generate_fine_tune_pairs() -> list[dict[str, str]]:
    """
    Constructs a dataset of high-quality Enterprise prompt-code pairs.
    """
    pairs = []

    # 1. Domain Adapter Rules Training Pairs
    for domain_name, rules_text in DOMAIN_RULES.items():
        instruction = f"Provide enterprise production coding standards and best practices for domain: {domain_name}."
        pairs.append({
            "instruction": instruction,
            "input": f"Target Tech Stack: {domain_name}",
            "output": rules_text.strip()
        })

    # 2. Enterprise Scenario Architecture Training Pairs
    for scenario_name, scenario_text in ENTERPRISE_SCENARIOS.items():
        instruction = f"Design enterprise architecture and code blueprint for real-world scenario: {scenario_name}."
        pairs.append({
            "instruction": instruction,
            "input": f"Business Scenario: {scenario_name}",
            "output": scenario_text.strip()
        })

    # 3. Add Sample Enterprise Code Implementation Pairs
    sample_enterprise_implementations = [
        {
            "instruction": "Implement an idempotent payment webhook receiver in Python with cryptographic signature verification.",
            "input": "Payment Gateway: Stripe / PayPal Webhook",
            "output": """import hmac
import hashlib
import time

def verify_webhook_signature(payload: bytes, signature_header: str, secret: str) -> bool:
    \"\"\"Verifies cryptographic HMAC-SHA256 signature for incoming payment webhook.\"\"\"
    if not signature_header or not secret:
        return False
    
    expected_sig = hmac.new(secret.encode('utf-8'), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_sig, signature_header)
"""
        },
        {
            "instruction": "Implement a Redis Sliding Window Rate Limiter for Microservices API Gateway.",
            "input": "Algorithm: Sliding Window Counter, Max Requests: 100 per minute",
            "output": """import time
import redis

class RedisSlidingWindowRateLimiter:
    \"\"\"Sliding Window Rate Limiter using Redis Sorted Sets.\"\"\"
    def __init__(self, redis_client: redis.Redis, limit: int = 100, window_seconds: int = 60):
        self.redis = redis_client
        self.limit = limit
        self.window = window_seconds

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        clear_before = now - self.window
        key = f"rate_limit:{user_id}"
        
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, clear_before)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, self.window)
        results = pipe.execute()
        
        request_count = results[2]
        return request_count <= self.limit
"""
        }
    ]

    pairs.extend(sample_enterprise_implementations)
    return pairs


def build_dataset_file(output_path: Path = OUTPUT_DATASET_PATH) -> Path:
    """
    Exports the generated dataset pairs into a JSONL file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pairs = generate_fine_tune_pairs()

    with open(output_path, "w", encoding="utf-8") as f:
        for item in pairs:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"[SUCCESS] Successfully generated SLM fine-tuning dataset with {len(pairs)} JSONL pairs at: {output_path}")
    return output_path


if __name__ == "__main__":
    build_dataset_file()
