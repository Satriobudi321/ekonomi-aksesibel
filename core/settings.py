"""
core/settings.py

Manajemen pengaturan pengguna (font size, TTS rate, dll.)
disimpan dalam JSON.
"""

import json
import os


class Settings:
    DEFAULT_SETTINGS = {
        "font_size": 14,
        "tts_rate": 180,
        "tts_volume": 1.0,
        "current_user": "siswa",
        "high_contrast": False,
    }

    def __init__(self, filepath=None):
        if filepath is None:
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = os.path.join(base, "data", "progress", "settings.json")
        self.filepath = filepath
        self._data = dict(self.DEFAULT_SETTINGS)
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._data.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self.save()
