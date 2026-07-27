"""
core/sandbox_adapter.py
Dynamic Sandbox Runner Adapter for Elearning Agent.
Selects and renders the appropriate Code Sandbox runner tags dynamically
from metadata without hardcoding technology logic inside renderers.
"""

from typing import Dict, Any, Optional

# Dynamic Sandbox Registry mapping runner types to CDN scripts and configurations
SANDBOX_REGISTRY: Dict[str, Dict[str, Any]] = {
    "PYODIDE_WASM": {
        "script_cdn": "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js",
        "description": "Pyodide WebAssembly Runtime Engine"
    },
    "JS_WEB_WORKER": {
        "script_cdn": None,
        "description": "Native Web Worker JavaScript Engine"
    },
    "IFRAME_PREVIEW": {
        "script_cdn": None,
        "description": "Live HTML/CSS iFrame Live Preview"
    },
    "STATIC_CODE_BLOCK": {
        "script_cdn": None,
        "description": "Static Formatted Code Snippet"
    }
}

def get_sandbox_config(tech_stack: str, custom_registry: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Returns sandbox configuration for the specified technology stack dynamically.
    """
    registry = custom_registry or SANDBOX_REGISTRY
    tech_lower = (tech_stack or "").lower().strip()
    
    if "python" in tech_lower:
        return registry.get("PYODIDE_WASM", {})
    elif any(kw in tech_lower for kw in ["javascript", "js", "typescript", "ts", "frontend", "web"]):
        return registry.get("JS_WEB_WORKER", {})
    elif any(kw in tech_lower for kw in ["html", "css"]):
        return registry.get("IFRAME_PREVIEW", {})
    
    return registry.get("STATIC_CODE_BLOCK", {})

def render_sandbox_script_tag(tech_stack: str) -> str:
    """
    Renders script tag or comment for the sandbox runner dynamically without hardcoding script strings in renderers.
    """
    config = get_sandbox_config(tech_stack)
    cdn = config.get("script_cdn")
    desc = config.get("description", "Code Sandbox")
    
    if cdn:
        return f'<script src="{cdn}"></script>'
    return f'<!-- Sandbox Runner: {desc} -->'
