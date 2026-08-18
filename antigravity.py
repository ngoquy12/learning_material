"""
antigravity.py — Backward compatibility shim for core.dag_engine.
Redirects all imports to core.dag_engine to eliminate Python standard library namespace collisions.
"""

from core.dag_engine import (
    override,
    append_unique,
    merge_dict,
    STATE_REDUCERS,
    get_reducer,
    register_reducer,
    component,
    parallel,
    Workflow,
    CompiledWorkflow,
)

__all__ = [
    "override",
    "append_unique",
    "merge_dict",
    "STATE_REDUCERS",
    "get_reducer",
    "register_reducer",
    "component",
    "parallel",
    "Workflow",
    "CompiledWorkflow",
]
