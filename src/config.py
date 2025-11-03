import os
import json
from pathlib import Path
from dotenv import load_dotenv


class ConfigManager:
    CONFIG_PATH = Path.home() / ".memoscli" / "config.json"

    def __init__(self):
        load_dotenv()
        self.config = self._load_config()
    
    def _load_config(self):
        if self.CONFIG_PATH.exists():
            with open(self.CONFIG_PATH,"r") as f:
                return json.load(f)

        return {}
    
    def get(self, key, default=None):
        return os.getenv(key.upper()) or self.config.get(key,default)

    def set(self, key, value):
        self.config[key] = value
        self._save_config()

    def _save_config(self):
        self.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(self.CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def save(self):
        """Salva as configurações no arquivo json"""
        self._save_config()
    
    def all(self):
        return {**self.config, **{k.lower(): v for k, v in os.environ.items() if k.startswith("MEMOS_")}}
        
