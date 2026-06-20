import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class ConfigModel(BaseModel):
    """April configuration model with validation."""
    
    # Voice & Listening
    wake_words: List[str] = Field(default=["april", "hey april"])
    quick_command_code_word: str = Field(default="snap")
    quick_command_duration_seconds: int = Field(default=30, ge=5, le=120)
    
    # Fuzzy Matching
    confidence_threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    fuzzy_threshold: int = Field(default=80, ge=0, le=100)
    
    # UI/UX
    hud_display_seconds: int = Field(default=2, ge=1, le=10)
    
    # Safety
    danger_default: str = Field(default="prompt", regex="^(prompt|always_allow|always_block)$")
    
    # Do Not Disturb
    typing_dnd_threshold: int = Field(default=20, ge=0, le=100)
    typing_dnd_resume_delay: int = Field(default=5, ge=0, le=30)
    
    # Scheduled Tasks
    daily_standup_time: str = Field(default="09:00", regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    backup_time: str = Field(default="02:00", regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    
    # Vault
    vault_path: str = Field(default="~/.april/vault")
    github_repo_url: str = Field(default="")
    
    # Privacy
    local_only_mode: bool = Field(default=False)
    whisper_mode: bool = Field(default=False)
    
    # LLM
    llm_model: str = Field(default="llama3")
    llm_backend: str = Field(default="ollama", regex="^(ollama|transformers|openai)$")
    llm_api_url: str = Field(default="http://localhost:11434")
    
    # Debug
    debug_mode: bool = Field(default=False)
    log_level: str = Field(default="INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    # Review more configuration fields to add in the future 
    
    @validator("vault_path")
    def expand_vault_path(cls, v: str) -> str:
        """Expand tilde to home directory."""
        return str(Path(v).expanduser())


class ConfigManager:
    """Manages configuration loading and saving."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize config manager."""
        self.config_path = config_path or Path.home() / ".april" / "config.json"
        self.config: Optional[ConfigModel] = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file or create defaults."""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                self.config = ConfigModel(**data)
            else:
                # Create default config
                self.config = ConfigModel()
                self._save_config()
        except Exception as e:
            print(f"[ConfigManager] Error loading config: {e}")
            self.config = ConfigModel()
    
    def _save_config(self) -> None:
        """Save current configuration to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, "w") as f:
                json.dump(self.config.dict(), f, indent=2)
        except Exception as e:
            print(f"[ConfigManager] Error saving config: {e}")
    
    def get(self) -> ConfigModel:
        """Get the current configuration."""
        return self.config
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values."""
        updated = self.config.dict()
        updated.update(updates)
        self.config = ConfigModel(**updated)
        self._save_config()
    
    def get_vault_path(self) -> Path:
        """Get the expanded vault path."""
        return Path(self.config.vault_path).expanduser()