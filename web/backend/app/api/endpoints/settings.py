import json
import os
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

# Path to persistent settings file
SETTINGS_FILE = Path(__file__).resolve().parent.parent.parent / "core" / "settings_store.json"

DEFAULT_SETTINGS = {
    "llmProvider": "gemini",
    "modelName": "gemini-1.5-pro",
    "temperature": 0.2,
    "maxTokens": 4096,
    "systemPromptType": "standard_pedagogical",
    "enableSemanticCache": True,
    "obsidianPath": "C:\\Users\\Admin\\Obsidian\\Vaults\\Elearning",
    "scormStandard": "SCORM_2004",
    "defaultAuthor": "Elearning Content Factory",
    "pollingInterval": 3000,
    "enableLogs": True
}

class SystemSettingsSchema(BaseModel):
    llmProvider: str = Field(default="gemini")
    modelName: str = Field(default="gemini-1.5-pro")
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    maxTokens: int = Field(default=4096)
    systemPromptType: str = Field(default="standard_pedagogical")
    enableSemanticCache: bool = Field(default=True)
    obsidianPath: str = Field(default="C:\\Users\\Admin\\Obsidian\\Vaults\\Elearning")
    scormStandard: str = Field(default="SCORM_2004")
    defaultAuthor: str = Field(default="Elearning Content Factory")
    pollingInterval: int = Field(default=3000)
    enableLogs: bool = Field(default=True)

def _load_settings() -> dict:
    if not SETTINGS_FILE.exists():
        _save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged = DEFAULT_SETTINGS.copy()
            merged.update(data)
            return merged
    except Exception:
        return DEFAULT_SETTINGS.copy()

def _save_settings(data: dict):
    os.makedirs(SETTINGS_FILE.parent, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@router.get("/", response_model=SystemSettingsSchema, summary="Lấy cấu hình hệ thống hiện tại")
async def get_settings():
    return _load_settings()

@router.put("/", response_model=SystemSettingsSchema, summary="Cập nhật cấu hình hệ thống")
async def update_settings(payload: SystemSettingsSchema):
    data = payload.model_dump()
    _save_settings(data)
    return data

@router.post("/reset", response_model=SystemSettingsSchema, summary="Khôi phục cấu hình về mặc định")
async def reset_settings():
    _save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS.copy()
