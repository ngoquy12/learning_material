import os
import yaml
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
PROMPTS_FILE = CONFIG_DIR / "prompts.yaml"

# Load Prompts
PROMPTS = {}
if PROMPTS_FILE.exists():
    try:
        with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
            PROMPTS = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Warning: Failed to load prompts.yaml: {e}")

def get_agent_prompt(agent_name: str) -> dict:
    """Helper to get prompt persona and task for a given agent name."""
    return PROMPTS.get(agent_name, {"Persona": "", "Task": ""})

# Database Configuration (mock default, can be overridden by environment variables)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/elearning_factory")

# LLM Configurations
LLM_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
