"""Atomic user settings; independent of the firmware algorithm catalogue."""
import json
from pathlib import Path

class SettingsStore:
    def __init__(self, path=None):
        self.path = Path(path or Path(__file__).resolve().parents[1]/'config/session.json')
        self.values = {}
        if self.path.exists():
            try:
                self.values = json.loads(self.path.read_text(encoding='utf-8'))
                if not isinstance(self.values,dict):self.values={}
            except (OSError, ValueError):
                self.values = {}

    def get(self, key, default=None):
        return self.values.get(key, default)

    def set(self, key, value):
        self.values[key] = value
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_suffix('.tmp')
        temp.write_text(json.dumps(self.values, ensure_ascii=False, indent=2), encoding='utf-8')
        temp.replace(self.path)
