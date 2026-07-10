import sys
from typing import Callable, Any, Dict, List

def component(func):
    """Component decorator for workflow nodes."""
    func.__is_component__ = True
    return func

def parallel(func):
    """Parallel decorator for branching nodes."""
    func.__is_parallel__ = True
    return func

class Workflow:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.entry_point = None

    def add_node(self, name: str, func: Callable):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges.append((from_node, to_node))

    def compile(self):
        return CompiledWorkflow(self)

class CompiledWorkflow:
    def __init__(self, workflow: Workflow):
        self.nodes = workflow.nodes
        self.edges = workflow.edges
        self.entry_point = workflow.entry_point

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
                # Execute the parallel branches
                branches = node_func(state)
                # Merge the parallel branch states back into the main state
                merged_state = state.copy()
                if "artifacts_status" not in merged_state:
                    merged_state["artifacts_status"] = {}
                if "review_logs" not in merged_state:
                    merged_state["review_logs"] = []
                
                for branch_name, branch_state in branches.items():
                    print(f"\n[Parallel Merger] Merging branch: {branch_name}")
                    
                    if "html_content" in branch_state and branch_state["html_content"]:
                        merged_state["html_content"] = branch_state["html_content"]
                    if "slide_markdown" in branch_state and branch_state["slide_markdown"]:
                        merged_state["slide_markdown"] = branch_state["slide_markdown"]
                    if "quiz_json" in branch_state and branch_state["quiz_json"]:
                        merged_state["quiz_json"] = branch_state["quiz_json"]
                    if "video_script_markdown" in branch_state and branch_state["video_script_markdown"]:
                        merged_state["video_script_markdown"] = branch_state["video_script_markdown"]
                    if "mindmap_markdown" in branch_state and branch_state["mindmap_markdown"]:
                        merged_state["mindmap_markdown"] = branch_state["mindmap_markdown"]
                        
                    if "artifacts_status" in branch_state:
                        merged_state["artifacts_status"].update(branch_state["artifacts_status"])
                        
                    if "review_logs" in branch_state:
                        for log in branch_state["review_logs"]:
                            if log not in merged_state["review_logs"]:
                                merged_state["review_logs"].append(log)
                                
                state = merged_state
            else:
                # Regular node
                state = node_func(state)

            # Find next node
            next_nodes = [to_n for from_n, to_n in self.edges if from_n == current_node]
            if next_nodes:
                current_node = next_nodes[0]
            else:
                current_node = None
                
        return state
