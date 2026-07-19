import os

def load_skill_content(skill_name: str) -> str:
    """
    Loads raw markdown content of a skill from the skills directory,
    stripping the YAML frontmatter if present.
    """
    # Try finding inside the local skills folder
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_path = os.path.join(base_path, "skills", skill_name, "SKILL.md")
    
    if not os.path.exists(skill_path):
        return ""
        
    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return content.strip()
    except Exception as e:
        print(f"[Skills Warning] Failed to load skill {skill_name}: {e}")
        return ""
