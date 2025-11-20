# backend/state/config_loader.py
import json

class ConfigLoader:
    def load(self, path="config.json"):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except:
            return {}
