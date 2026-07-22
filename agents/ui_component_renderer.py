"""
agents/ui_component_renderer.py

HyperFrames UI Component Renderer (Agent Interface)
===================================================
Tích hợp trực tiếp với `hyperframes.ui_manager` để cung cấp giao diện
render chuẩn hóa cho Writer Agent và các Agents khác.

Sử dụng `UIManager` tập trung duy nhất để đảm bảo 100% đồng bộ.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from hyperframes.ui_manager import UIManager, default_ui_manager


class UIComponentRenderer:
    """
    Agent-side Wrapper Interface for UIManager.
    Delegates component loading, slot substitution, and layout mapping
    to the centralized UIManager in `hyperframes/ui_manager.py`.
    """

    COMPONENT_MAP = {
        "code_editor":          "ide/vscode.html",
        "terminal_cli":         "ide/terminal.html",
        "comparison":           "cards/comparison.html",
        "pitfall_alert":        "cards/warning_card.html",
        "process_flow":         "cards/process_flow.html",
        "architecture_diagram": "cards/architecture.html",
        "summary_recap":        "cards/summary_recap.html",
        "interactive_quiz":     "cards/qa_quiz.html",
    }

    def __init__(self, components_root: Optional[Path] = None):
        if components_root is not None:
            self.manager = UIManager(components_dir=components_root)
        else:
            self.manager = default_ui_manager

    def render(self, scene: Dict[str, Any], lesson_title: str) -> str:
        """Render scene HTML using the centralized UIManager."""
        return self.manager.render_scene(scene, lesson_title)

    def list_components(self) -> Dict[str, Path]:
        """Return dict of canonical layout types and absolute file paths."""
        res = {}
        for layout in self.manager.list_layouts():
            meta = self.manager.get_layout_meta(layout)
            res[layout] = self.manager.components_dir / meta["rel_path"]
        return res
