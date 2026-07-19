"""
tests/test_mindmap_compiler.py
==============================
Unit tests for the optimized session mindmap compiler and lesson mindmap agent.
Chạy: cd web/backend && pytest tests/test_mindmap_compiler.py -v
"""
import pytest
import sys
from pathlib import Path

# Add project and app/ai_engine to path
backend_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "app" / "ai_engine"))

from app.ai_engine.core.session_compilers import compile_session_mindmap_markdown

def test_compile_session_mindmap_markdown_hierarchical_shifting():
    """
    Checks that compile_session_mindmap_markdown shifts header levels of lesson mindmaps correctly
    and keeps the structure intact (objectives, theory, syntax, notes).
    """
    session_title = "FastAPI Advanced Concepts"
    mindmap_data = [
        {
            "title": "Lesson 01: Dependency Injection",
            "content": """```markmap
# Lesson 01: Dependency Injection
## Mục tiêu bài học
- Hiểu DI trong FastAPI
## Dependency Injection
### Khái niệm lý thuyết
- DI giúp tái sử dụng code.
### Cấu trúc cú pháp
- Ví dụ:
    ```python
    def get_db():
        pass
    ```
### Lưu ý
- Tránh lạm dụng dependencies.
```"""
        },
        {
            "title": "Lesson 02: Background Tasks",
            "content": """
# Lesson 02: Background Tasks
## Mục tiêu bài học
- Hiểu BackgroundTasks
## Background Tasks
### Khái niệm lý thuyết
- Chạy tác vụ nền.
### Cấu trúc cú pháp
- Ví dụ:
    ```python
    def task():
        pass
    ```
### Lưu ý
- Không dùng cho CPU-bound tasks.
"""
        }
    ]
    
    compiled = compile_session_mindmap_markdown(session_title, mindmap_data)
    
    assert "# FastAPI Advanced Concepts" in compiled
    # Shifting # -> ##
    assert "## Lesson 01: Dependency Injection" in compiled
    assert "## Lesson 02: Background Tasks" in compiled
    
    # Shifting ## -> ###
    assert "### Mục tiêu bài học" in compiled
    assert "### Dependency Injection" in compiled
    assert "### Background Tasks" in compiled
    
    # Shifting ### -> ####
    assert "#### Khái niệm lý thuyết" in compiled
    assert "#### Cấu trúc cú pháp" in compiled
    assert "#### Lưu ý" in compiled
    
    # Assert standard YAML config is present and freeze level is set to 3
    assert "colorFreezeLevel: 3" in compiled
    
    # Ensure code blocks inside syntactic sections are preserved
    assert "def get_db():" in compiled
    assert "def task():" in compiled
