import json
import os
from pathlib import Path
from typing import List, Dict, Optional

CONFIG_DIR = Path.home() / ".jiuzhao"
CONFIG_FILE = CONFIG_DIR / "config.json"
MODELS_FILE = Path("models.json")

DEFAULT_CONFIG = {
    "current_model": "rwkv-7-prover-1.5b",
    "models": []
}

def load_default_models() -> List[Dict]:
    if MODELS_FILE.exists():
        with open(MODELS_FILE, "r") as f:
            return json.load(f)
    return []

def load_config() -> Dict:
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            if not config.get("models"):
                config["models"] = load_default_models()
            return config
    except Exception:
        return DEFAULT_CONFIG

def save_config(config: Dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_model_config(model_name: str) -> Optional[Dict]:
    config = load_config()
    for m in config.get("models", []):
        if m["name"] == model_name:
            return m
    return None
