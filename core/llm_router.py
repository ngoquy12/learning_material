# core/llm_router.py
"""
Dynamic Model Tier Router for Antigravity API Proxy Infrastructure.
Automatically maps agent tasks into 3 execution tiers:
- Tier 1 (Fast & Light): Fast validation, linting, keyword extraction, summaries.
- Tier 2 (High Reasoning): Pedagogical creation (reading, slides, quizzes, scope calculation).
- Tier 3 (Deep Context & Code): Enterprise code generation (with Context Caching).

STRICT CONTRACT: Transparent infrastructure optimization only. ZERO mutation to Agent business logic.
"""

import os
from typing import Tuple, List, Dict, Any

# Tier Definitions
TIER_1_FAST = "tier_1_fast"
TIER_2_REASONING = "tier_2_reasoning"
TIER_3_DEEP_CONTEXT = "tier_3_deep_context"

# Model Candidate Priority Lists per Tier (Antigravity Proxy Native)
TIER_MODEL_MAPPING = {
    TIER_1_FAST: ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-3.6-flash-high"],
    TIER_2_REASONING: ["gemini-3.6-flash-high", "gemini-3.1-pro", "gemini-1.5-pro"],
    TIER_3_DEEP_CONTEXT: ["gemini-3.6-flash-high", "gemini-3.1-pro", "gemini-1.5-pro"]
}

# Agents requiring Pro-grade deep reasoning (gemini-3.1-pro)
HIGH_REASONING_PRO_AGENTS = {
    "objective_architect", "objective_reviewer", "prerequisite_guard",
    "pm_reviewer", "knowledge_memory_agent", "strategic_agent", "prerequisite_guard_agent"
}

# Task/Agent Mapping Registry
AGENT_TIER_REGISTRY: Dict[str, str] = {
    # Tier 1: Validation, Linters, Summaries, TTS Normalization
    "quiz_validator": TIER_1_FAST,
    "reading_validator": TIER_1_FAST,
    "slide_validator": TIER_1_FAST,
    "practice_validator": TIER_1_FAST,
    "project_validator": TIER_1_FAST,
    "syntax_linter": TIER_1_FAST,
    "tts_normalizer": TIER_1_FAST,
    "session_compiler_validator": TIER_1_FAST,
    "html_ux_reviewer": TIER_1_FAST,
    "mindmap_reviewer": TIER_1_FAST,
    
    # Tier 3: High Context & Complex Code (gemini-3.6-flash-high / gemini-3.1-pro)
    "enterprise_code_section_3": TIER_3_DEEP_CONTEXT,
    
    # Tier 2: Standard & Pro Pedagogical Creators (gemini-3.6-flash-high / gemini-3.1-pro)
    "reading_creator": TIER_2_REASONING,
    "html_writer_agent": TIER_2_REASONING,
    "classroom_lecture_generator": TIER_2_REASONING,
    "classroom_lecture_creator": TIER_2_REASONING,
    "classroom_lecture_agent": TIER_2_REASONING,
    "slide_creator": TIER_2_REASONING,
    "slide_agent": TIER_2_REASONING,
    "quiz_creator": TIER_2_REASONING,
    "quiz_agent": TIER_2_REASONING,
    "practical_lab_creator": TIER_2_REASONING,
    "visualizer_creator": TIER_2_REASONING,
    "mindmap_creator": TIER_2_REASONING,
    "prerequisite_guard": TIER_2_REASONING,
    "prerequisite_guard_agent": TIER_2_REASONING,
    "scope_calculator": TIER_2_REASONING,
    "objective_architect": TIER_2_REASONING,
    "objective_reviewer": TIER_2_REASONING,
    "pm_generator": TIER_2_REASONING,
    "pm_reviewer": TIER_2_REASONING,
    "knowledge_memory_agent": TIER_2_REASONING,
    "sandbox_agent": TIER_2_REASONING,
}

class AntigravityLLMRouter:
    """
    Centralized Router that resolves the optimal Gemini Model Tier & Context Cache flag
    for any LLM invocation based on the invoking agent's name or task type.
    """
    
    @staticmethod
    def classify_agent_tier(agent_name: str, task_type: str = "") -> str:
        """
        Determines the execution tier for a given agent or task type.
        Defaults to TIER_2_REASONING if unspecified.
        """
        normalized_name = (agent_name or "").lower().strip()
        normalized_task = (task_type or "").lower().strip()
        
        # Check task type override first
        if normalized_task in AGENT_TIER_REGISTRY:
            return AGENT_TIER_REGISTRY[normalized_task]
            
        # Check agent name registry
        for key, tier in AGENT_TIER_REGISTRY.items():
            if key in normalized_name:
                return tier
                
        # Fast-track keywords for Tier 1
        if any(kw in normalized_name for kw in ["validator", "linter", "normalizer", "summary"]):
            return TIER_1_FAST
            
        # Deep context keywords for Tier 3
        if any(kw in normalized_name for kw in ["section_3_code", "enterprise_code"]):
            return TIER_3_DEEP_CONTEXT
            
        return TIER_2_REASONING

    @staticmethod
    def resolve_model(agent_name: str, task_type: str = "") -> Tuple[str, bool]:
        """
        Returns (model_name, enable_cache_flag) based on the classified tier.
        Allows environment variable GEMINI_MODEL override if explicitly provided.
        """
        tier = AntigravityLLMRouter.classify_agent_tier(agent_name, task_type)
        
        # Check if environment variable explicitly forces a global model override
        force_override = os.getenv("FORCE_GEMINI_MODEL", "false").lower() in ("true", "1", "yes")
        env_override = os.getenv("GEMINI_MODEL")
        
        if force_override and env_override:
            model_name = env_override
        else:
            normalized_name = (agent_name or "").lower().strip()
            if any(pro_agent in normalized_name for pro_agent in HIGH_REASONING_PRO_AGENTS):
                model_name = "gemini-3.1-pro"
            else:
                candidates = TIER_MODEL_MAPPING.get(tier, TIER_MODEL_MAPPING[TIER_2_REASONING])
                model_name = candidates[0]
            
        enable_cache = (tier == TIER_3_DEEP_CONTEXT)
        return model_name, enable_cache

    @staticmethod
    def get_fallback_candidates(agent_name: str, current_model: str) -> List[str]:
        """
        Returns alternative candidate model names within the same tier if current_model fails.
        """
        tier = AntigravityLLMRouter.classify_agent_tier(agent_name)
        candidates = TIER_MODEL_MAPPING.get(tier, TIER_MODEL_MAPPING[TIER_2_REASONING])
        return [m for m in candidates if m != current_model]


def resolve_model_tier_for_agent(agent_name: str, task_type: str = "") -> Tuple[str, bool]:
    """
    Public utility function to resolve model tier and cache settings for an agent.
    """
    return AntigravityLLMRouter.resolve_model(agent_name, task_type)
