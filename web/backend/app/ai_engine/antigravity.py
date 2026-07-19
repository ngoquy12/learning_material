"""
antigravity.py — Asynchronous DAG Workflow Engine with Declarative State Reducers.

Architecture:
    The engine executes a compiled directed graph of nodes. Each node is a pure function
    that receives an AgentState dict and returns an AgentState dict. Parallel nodes fork
    the state into independent branches and merge results back using DECLARATIVE REDUCERS
    defined in the state schema — the engine itself has ZERO knowledge of domain-specific
    field names like 'html_content' or 'quiz_json'.

State Reducer Pattern:
    Instead of hardcoding merge logic per field, each field in AgentState declares its own
    merge strategy via the STATE_REDUCERS registry:
        - override(old, new) → new           : Last-write-wins for content fields
        - append_unique(old, new) → merged    : Deduplication append for log fields
        - merge_dict(old, new) → merged       : Shallow dict merge for status maps

    Adding a new artifact type (e.g. 'lab_json', 'exercise_pdf') requires ONLY adding
    the field to AgentState and registering its reducer — the engine code stays untouched.

Changelog:
    v2.0 — State Reducer pattern replaces hardcoded parallel merger (2026-07-13)
    v1.0 — Original implementation with manual field-by-field merge
"""

import sys
from typing import Callable, Any, Dict, List, Optional


# =============================================================================
# SECTION 1: BUILT-IN REDUCER FUNCTIONS
# =============================================================================
# Each reducer is a pure function: (old_value, new_value) → merged_value.
# They are composable, testable, and can be extended by downstream code.
# =============================================================================

def override(old_value: Any, new_value: Any) -> Any:
    """
    Last-write-wins reducer.
    Returns new_value if it is truthy (non-empty string, non-empty dict, non-None),
    otherwise preserves old_value. This prevents a branch that didn't touch a field
    from accidentally blanking it with an empty string.

    Use for: html_content, slide_markdown, video_script_markdown, mindmap_markdown,
             quiz_json, learning_outcomes, program_structure, core_ssot, etc.
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
    Handles edge cases where either side is None or not a list.

    Use for: review_logs, error_logs, or any accumulating event stream.
    """
    if not isinstance(old_value, list):
        old_value = []
    if not isinstance(new_value, list):
        return old_value
    merged = list(old_value)  # shallow copy
    for item in new_value:
        if item not in merged:
            merged.append(item)
    return merged


def merge_dict(old_value: Any, new_value: Any) -> Any:
    """
    Shallow dictionary merge reducer.
    Updates old_value dict with all key-value pairs from new_value.
    Non-dict inputs are handled gracefully.

    Use for: artifacts_status, time_reference, or any flat config map.
    """
    if not isinstance(old_value, dict):
        old_value = {}
    if not isinstance(new_value, dict):
        return old_value
    merged = dict(old_value)  # shallow copy
    merged.update(new_value)
    return merged


# =============================================================================
# SECTION 2: STATE REDUCER REGISTRY
# =============================================================================
# The registry maps each AgentState field name to its reducer function.
# This is the SINGLE PLACE where merge semantics are declared.
#
# Convention:
#   - Content fields (str)  → override
#   - Log fields (list)     → append_unique
#   - Status fields (dict)  → merge_dict
#   - Identity fields (str) → override (but branches shouldn't change them)
#
# DEFAULT BEHAVIOR: Fields not in this registry use 'override' as fallback.
# =============================================================================

STATE_REDUCERS: Dict[str, Callable[[Any, Any], Any]] = {
    # --- Identity & Configuration (read-only across branches) ---
    "session_id":           override,
    "lesson_id":            override,
    "pm_input":             override,
    "time_reference":       merge_dict,
    "technology_stack":     override,
    "course_dir_name":      override,
    "requested_parts":      override,
    "force_rebuild":        override,
    "previous_lessons":     override,

    # --- Strategic Phase outputs ---
    "learning_outcomes":    override,
    "program_structure":    override,
    "core_ssot":            merge_dict,

    # --- Creator Phase outputs (parallel branches produce these) ---
    "html_content":             override,
    "slide_markdown":           override,
    "quiz_json":                override,
    "video_script_markdown":    override,
    "mindmap_markdown":         override,

    # --- Accumulating state (must be merged, not overwritten) ---
    "artifacts_status":     merge_dict,
    "review_logs":          append_unique,
}


def get_reducer(field_name: str) -> Callable[[Any, Any], Any]:
    """Looks up the reducer for a field. Falls back to 'override' for unregistered fields."""
    return STATE_REDUCERS.get(field_name, override)


def register_reducer(field_name: str, reducer_fn: Callable[[Any, Any], Any]) -> None:
    """
    Registers a custom reducer for a new state field at runtime.
    This is the extension point for downstream code that adds new artifact types
    without touching the engine source code.

    Example:
        from antigravity import register_reducer, append_unique
        register_reducer("lab_results", append_unique)
    """
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
    """
    Declarative workflow builder.
    Nodes are registered with names, edges define execution order,
    and the entry point sets where traversal begins.
    """
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
    """
    Compiled, immutable workflow executor.

    Key design decision for parallel merge:
        The engine iterates over ALL keys present in ANY branch state and applies
        the registered reducer for each key. This means:
        1. The engine never needs to know field names in advance
        2. New fields added by a branch are automatically picked up
        3. Merge semantics are always consistent with the registry
    """
    def __init__(self, workflow: Workflow):
        self.nodes = workflow.nodes
        self.edges = workflow.edges
        self.entry_point = workflow.entry_point

    def _merge_parallel_branches(
        self,
        base_state: Dict[str, Any],
        branch_results: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Merges multiple parallel branch states back into a single unified state
        using the declarative reducer registry.

        Algorithm:
            1. Start with a copy of the base state (pre-fork snapshot)
            2. For each branch, for each key in that branch's state:
               a. Look up the reducer for that key
               b. Apply: merged[key] = reducer(merged[key], branch[key])
            3. Return the fully merged state

        This is O(B × K) where B = number of branches and K = average keys per branch.
        For the current system (5 branches, ~20 keys), this is negligible.
        """
        merged = base_state.copy()

        for branch_name, branch_state in branch_results.items():
            print(f"\n[Parallel Merger] Merging branch: {branch_name}")

            for key, branch_value in branch_state.items():
                reducer = get_reducer(key)
                old_value = merged.get(key)
                merged[key] = reducer(old_value, branch_value)

        return merged

    def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
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

            # Check if this node is parallel
            is_parallel = getattr(node_func, "__is_parallel__", False)

            if is_parallel:
                # Execute the parallel branches and merge via reducers
                branch_results = node_func(state)
                state = self._merge_parallel_branches(state, branch_results)
            else:
                # Regular sequential node
                state = node_func(state)

            # Find next node
            next_nodes = [to_n for from_n, to_n in self.edges if from_n == current_node]
            if next_nodes:
                current_node = next_nodes[0]
            else:
                current_node = None

        return state
