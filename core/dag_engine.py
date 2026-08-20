"""
core/dag_engine.py — Asynchronous DAG Workflow Engine with Declarative State Reducers.

Architecture:
    The engine executes a compiled directed graph of nodes. Each node is a pure function
    that receives an AgentState dict and returns an AgentState dict. Parallel nodes fork
    the state into independent branches and merge results back using DECLARATIVE REDUCERS
    defined in the state schema — the engine itself has ZERO knowledge of domain-specific
    field names.

State Reducer Pattern:
    Instead of hardcoding merge logic per field, each field in AgentState declares its own
    merge strategy via the STATE_REDUCERS registry:
        - override(old, new) → new           : Last-write-wins for content fields
        - append_unique(old, new) → merged    : Deduplication append for log fields
        - merge_dict(old, new) → merged       : Shallow dict merge for status maps
"""

import sys
from typing import Callable, Any, Dict, List, Optional, Union
from core.state import AgentState


# =============================================================================
# SECTION 1: BUILT-IN REDUCER FUNCTIONS
# =============================================================================

def override(old_value: Any, new_value: Any) -> Any:
    """
    Last-write-wins reducer.
    Returns new_value if it is truthy (non-empty string, non-empty dict, non-None),
    otherwise preserves old_value.
    """
    if new_value is None:
        return old_value
    if isinstance(new_value, str) and not new_value:
        return old_value
    if isinstance(new_value, dict) and not new_value:
        return old_value
    return new_value


def append_unique(old_value: Any, new_value: Any) -> Any:
    """
    Deduplication-append reducer for list fields.
    Appends items from new_value that don't already exist in old_value.
    """
    if not isinstance(old_value, list):
        old_value = []
    if not isinstance(new_value, list):
        return old_value
    merged = list(old_value)
    for item in new_value:
        if item not in merged:
            merged.append(item)
    return merged


def merge_dict(old_value: Any, new_value: Any) -> Any:
    """
    Shallow dictionary merge reducer.
    Updates old_value dict with all key-value pairs from new_value.
    """
    if not isinstance(old_value, dict):
        old_value = {}
    if not isinstance(new_value, dict):
        return old_value
    merged = dict(old_value)
    merged.update(new_value)
    return merged


# =============================================================================
# SECTION 2: STATE REDUCER REGISTRY
# =============================================================================

STATE_REDUCERS: Dict[str, Callable[[Any, Any], Any]] = {
    # --- Identity & Configuration ---
    "session_id":           override,
    "lesson_id":            override,
    "pm_input":             override,
    "time_reference":       merge_dict,
    "technology_stack":     override,
    "course_dir_name":      override,
    "requested_parts":      override,
    "force_rebuild":        override,
    "previous_lessons":     override,
    "pm_approved":          override,

    # --- Strategic Phase outputs ---
    "learning_outcomes":    override,
    "program_structure":    override,
    "core_ssot":            merge_dict,

    # --- 2-Tier Core Creator Phase outputs (Lesson Level) ---
    "html_content":                 override,
    "quiz_json":                    override,
    "practical_lab_markdown":       override,
    "practical_lab_html":           override,
    "lab_json":                     override,
    "reading_questions_markdown":   override,
    "reading_questions_json":       override,

    # --- Accumulating state ---
    "artifacts_status":     merge_dict,
    "review_logs":          append_unique,
}


def get_reducer(field_name: str) -> Callable[[Any, Any], Any]:
    """Looks up the reducer for a field. Falls back to 'override' for unregistered fields."""
    return STATE_REDUCERS.get(field_name, override)


def register_reducer(field_name: str, reducer_fn: Callable[[Any, Any], Any]) -> None:
    """Registers a custom reducer for a new state field at runtime."""
    STATE_REDUCERS[field_name] = reducer_fn


# =============================================================================
# SECTION 3: NODE DECORATORS
# =============================================================================

def component(func):
    """Component decorator for workflow nodes."""
    func.__is_component__ = True
    return func

def parallel(func):
    """Parallel decorator for branching nodes."""
    func.__is_parallel__ = True
    return func


# =============================================================================
# SECTION 4: WORKFLOW BUILDER & COMPILED RUNNER
# =============================================================================

class Workflow:
    """Declarative workflow builder."""
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.edges: List[tuple] = []
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges.append((from_node, to_node))

    def compile(self):
        return CompiledWorkflow(self)


class CompiledWorkflow:
    """Compiled, immutable workflow executor."""
    def __init__(self, workflow: Workflow):
        self.nodes = workflow.nodes
        self.edges = workflow.edges
        self.entry_point = workflow.entry_point

    def _merge_parallel_branches(
        self,
        base_state: Dict[str, Any],
        branch_results: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        merged = base_state.copy()

        for branch_name, branch_state in branch_results.items():
            print(f"\n[Parallel Merger] Merging branch: {branch_name}")

            for key, branch_value in branch_state.items():
                reducer = get_reducer(key)
                old_value = merged.get(key)
                merged[key] = reducer(old_value, branch_value)

        return merged

    def run(self, initial_state: Union[AgentState, Dict[str, Any]]) -> Dict[str, Any]:
        current_node = self.entry_point
        state = initial_state.copy()

        # Execute node-by-node down the path
        while current_node:
            node_func = self.nodes.get(current_node)
            if not node_func:
                print(f"Error: Node '{current_node}' not found in registered nodes.")
                break

            print(f"\n=========================================")
            print(f">>> Executing Node: [{current_node}] <<<")
            print(f"=========================================")

            is_parallel = getattr(node_func, "__is_parallel__", False)

            if is_parallel:
                branch_results = node_func(state)
                state = self._merge_parallel_branches(state, branch_results)
            else:
                state = node_func(state)

            next_nodes = [to_n for from_n, to_n in self.edges if from_n == current_node]
            if next_nodes:
                current_node = next_nodes[0]
            else:
                current_node = None

        return state
