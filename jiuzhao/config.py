import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Any

CONFIG_DIR = Path.home() / ".jiuzhao"
CONFIG_FILE = CONFIG_DIR / "config.json"
MODELS_FILE = Path("models.json")

DEFAULT_CONFIG = {
    "current_model": "rwkv-7-prover-1.5b",
    "generation": {
        "temperature": 0.2,
        "max_tokens": 4096,
        "max_turns": 15,
        "timeout": 60
    },
    "models": []
}

def load_default_models() -> List[Dict]:
    """Load models from the local models.json file if it exists."""
    if MODELS_FILE.exists():
        try:
            with open(MODELS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def load_config() -> Dict:
    """Load user configuration, merging with defaults."""
    config = DEFAULT_CONFIG.copy()
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                user_config = json.load(f)
                # Deep merge for generation settings
                if "generation" in user_config:
                    config["generation"].update(user_config["generation"])
                if "current_model" in user_config:
                    config["current_model"] = user_config["current_model"]
                if "models" in user_config:
                    config["models"] = user_config["models"]
        except Exception:
            pass # Fallback to default on error
    
    # Ensure models list is populated
    if not config["models"]:
        config["models"] = load_default_models()
        
    return config

def save_config(config: Dict):
    """Save configuration to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_model_config(model_name: str) -> Optional[Dict]:
    """Retrieve specific model configuration by name."""
    config = load_config()
    for m in config.get("models", []):
        if m["name"] == model_name:
            return m
    return None

def get_generation_config() -> Dict[str, Any]:
    """Get generation parameters."""
    return load_config().get("generation", DEFAULT_CONFIG["generation"])
