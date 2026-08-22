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

    # --- Scope & Domain Contracts (bất biến trong 1 lesson, nhánh nào cũng như nhau) ---
    "allowed_scope":        override,
    "forbidden_scope":      override,
    "session_domain":       override,
    "chosen_domain":        override,
    "lesson_type":          override,

    # --- Strategic Phase outputs ---
    "learning_outcomes":    override,
    "program_structure":    override,
    "core_ssot":            merge_dict,
    "full_curriculum":      override,
    "prerequisite_data":    override,
    "prerequisite_checked": override,

    # --- Shared upstream context (sinh trước khi rẽ nhánh song song) ---
    "master_content":           override,
    "lesson_blueprint":         override,
    "lesson_content":           override,
    "reading_material":         override,
    "lessons_learned_prompt":   override,
    "images_dir":               override,

    # --- 2-Tier Core Creator Phase outputs (Lesson Level) ---
    "html_content":                 override,
    "quiz_json":                    override,
    "practical_lab_markdown":       override,
    "practical_lab_html":           override,
    "lab_json":                     override,
    "reading_questions_markdown":   override,
    "reading_questions_json":       override,
    "video_script_markdown":        override,
    "self_test_markdown":           override,
    "slide_markdown":               override,

    # --- Tier 1: Session-level Artifacts ---
    "classroom_lecture_html":   override,
    "session_quizzes_json":     override,
    "homework_markdown":        override,
    "mindmap_markdown":         override,

    # --- Accumulating state ---
    "artifacts_status":     merge_dict,
    "review_logs":          append_unique,
    "scope_audits":         merge_dict,
}


def get_reducer(field_name: str) -> Callable[[Any, Any], Any]:
    """Looks up the reducer for a field. Falls back to 'override' for unregistered fields."""
    return STATE_REDUCERS.get(field_name, override)


def merge_branch_states(
    base_state: Dict[str, Any],
    branch_results: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Merges parallel branch states back into the base state using STATE_REDUCERS.

    ĐÂY LÀ ĐƯỜNG MERGE DUY NHẤT của hệ thống. Trước đây core/graph.py có một hàm
    _merge_sub_state riêng copy tay từng tên field, tồn tại song song với reducer
    registry ở đây. Hệ quả là mỗi khi thêm một field state mới phải nhớ sửa 2 chỗ —
    và thực tế đã quên: practical_lab_html có trong registry nhưng thiếu ở bản copy tay,
    khiến artifact do LLM sinh bị vứt bỏ lúc merge.

    Bất kỳ nơi nào cần gộp kết quả các nhánh song song đều phải gọi hàm này.
    """
    merged = base_state.copy()

    for branch_name, branch_state in branch_results.items():
        if not isinstance(branch_state, dict):
            print(f"  [Parallel Merger] Bỏ qua nhánh '{branch_name}': không phải dict hợp lệ.")
            continue

        print(f"  [Parallel Merger] Gộp nhánh: {branch_name}")
        for key, branch_value in branch_state.items():
            reducer = get_reducer(key)
            merged[key] = reducer(merged.get(key), branch_value)

    return merged


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

# Sentinel truyền cho `path_map` của add_conditional_edge() để đánh dấu kết thúc
# pipeline theo một nhánh cụ thể, thay vì phải trỏ tới một node "no-op" giả.
END = "__END__"


class Workflow:
    """
    Declarative workflow builder.

    Hỗ trợ 2 loại cạnh:
      - Cạnh thẳng (add_edge): luôn đi tới đúng 1 node kế tiếp, không điều kiện.
      - Cạnh có điều kiện (add_conditional_edge): node kế tiếp được QUYẾT ĐỊNH LÚC
        CHẠY dựa trên state hiện tại — đây là phần "DAG" thật của engine. Trước khi
        có cơ chế này, CompiledWorkflow.run() chỉ đi tuyến tính theo edges[0], nên
        mọi "rẽ nhánh" trong graph.py đều phải giả bằng early-return bên trong từng
        node thay vì bằng cấu trúc đồ thị — cách này hoạt động nhưng khiến luồng rẽ
        nhánh không thể nhìn thấy được từ chính cấu trúc workflow.
    """
    def __init__(self):
        self.nodes: Dict[str, Callable] = {}
        self.edges: List[tuple] = []
        self.conditional_edges: Dict[str, tuple] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges.append((from_node, to_node))

    def add_conditional_edge(
        self,
        from_node: str,
        condition: Callable[[Dict[str, Any]], str],
        path_map: Dict[str, str],
    ) -> None:
        """
        Đăng ký rẽ nhánh thật: sau khi `from_node` chạy xong, `condition(state)` trả về
        một khoá, và `path_map[khoá]` là node kế tiếp thực sự sẽ chạy (hoặc `END`).

        Một node chỉ nên có MỘT cạnh có điều kiện. Nếu `from_node` cũng có cạnh thẳng
        (add_edge), cạnh có điều kiện được ưu tiên — cạnh thẳng khi đó chỉ còn ý nghĩa
        tài liệu (không được engine dùng tới).
        """
        self.conditional_edges[from_node] = (condition, path_map)

    def compile(self):
        return CompiledWorkflow(self)


class CompiledWorkflow:
    """Compiled, immutable workflow executor."""
    def __init__(self, workflow: Workflow):
        self.nodes = workflow.nodes
        self.edges = workflow.edges
        self.conditional_edges = workflow.conditional_edges
        self.entry_point = workflow.entry_point

    def _resolve_next_node(self, current_node: str, state: Dict[str, Any]) -> Optional[str]:
        """
        Tìm node kế tiếp cho `current_node`.

        Cạnh có điều kiện được ưu tiên tuyệt đối trước cạnh thẳng. Nếu `condition(state)`
        trả về một khoá không có trong `path_map`, raise ngay kèm danh sách khoá hợp lệ —
        cùng triết lý fail-loud của require_tech_stack(): một nhánh rẽ đi sai chỗ mà
        không ai biết còn nguy hiểm hơn nhiều so với dừng pipeline lại để sửa.
        """
        if current_node in self.conditional_edges:
            condition, path_map = self.conditional_edges[current_node]
            branch_key = condition(state)
            if branch_key not in path_map:
                raise ValueError(
                    f"❌ [LỖI ĐIỀU KIỆN RẼ NHÁNH] Node '{current_node}': condition() trả về "
                    f"'{branch_key}', nhưng path_map chỉ có các khoá {list(path_map.keys())}."
                )
            next_node = path_map[branch_key]
            return None if next_node == END else next_node

        next_nodes = [to_n for from_n, to_n in self.edges if from_n == current_node]
        return next_nodes[0] if next_nodes else None

    def _merge_parallel_branches(
        self,
        base_state: Dict[str, Any],
        branch_results: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Delegates to the single shared merge implementation."""
        return merge_branch_states(base_state, branch_results)

    def run(self, initial_state: Union[AgentState, Dict[str, Any]]) -> Dict[str, Any]:
        # Kiểm định kiểu dữ liệu ngay tại cổng vào pipeline: AgentState là TypedDict,
        # không có gì ngăn một caller truyền nhầm kiểu (vd core_ssot là chuỗi thay vì
        # dict). Bắt ở đây, sai lệch lộ ra ngay tại nơi bắt đầu chạy — không phải
        # crash mù mờ sâu trong một renderer không liên quan hàng chục bước sau.
        from core.schemas.agent_state_schema import validate_state
        validate_state(initial_state, caller="CompiledWorkflow.run")

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

            current_node = self._resolve_next_node(current_node, state)

        return state
