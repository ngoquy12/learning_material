# core/prompts.py
"""
Unified Prompt Management Engine for Elearning Content Factory.
Provides robust Jinja2 template loading, caching, versioning, and context injection
to decouple massive prompt strings from agent business logic.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import jinja2

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_PROMPT_DIR = BASE_DIR / "templates" / "prompts"
TEMPLATES_PROMPT_DIR.mkdir(parents=True, exist_ok=True)

class PromptManager:
    """
    Centralized Prompt Manager that loads, caches, and renders Jinja2 prompt templates.
    """
    _instance: Optional["PromptManager"] = None

    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or TEMPLATES_PROMPT_DIR
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=False,  # Prompts are raw text / markdown / JSON specifications
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=jinja2.ChainableUndefined
        )
        self._cache: Dict[str, jinja2.Template] = {}

    @classmethod
    def get_instance(cls) -> "PromptManager":
        """Singleton accessor for PromptManager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def render(self, template_name: str, context: Optional[Dict[str, Any]] = None, fallback_text: str = "") -> str:
        """
        Renders a template by its filename (e.g. 'reading_system.j2') with the provided context.
        If the template file is not found, falls back to rendering fallback_text with Jinja2 if provided.
        """
        context = context or {}
        
        # Check cache
        if template_name not in self._cache:
            try:
                template = self._env.get_template(template_name)
                self._cache[template_name] = template
            except jinja2.TemplateNotFound:
                if fallback_text:
                    template = self._env.from_string(fallback_text)
                    self._cache[template_name] = template
                else:
                    raise FileNotFoundError(
                        f"Prompt template '{template_name}' not found in '{self.templates_dir}' and no fallback provided."
                    )
            except Exception as e:
                if fallback_text:
                    template = self._env.from_string(fallback_text)
                    self._cache[template_name] = template
                else:
                    raise e

        return self._cache[template_name].render(**context)

    def render_from_string(self, template_string: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Renders an arbitrary string as a Jinja2 template."""
        context = context or {}
        template = self._env.from_string(template_string)
        return template.render(**context)


def render_prompt(template_name: str, context: Optional[Dict[str, Any]] = None, fallback_text: str = "") -> str:
    """Convenience function to render a prompt template via the default PromptManager singleton."""
    return PromptManager.get_instance().render(template_name, context, fallback_text)
