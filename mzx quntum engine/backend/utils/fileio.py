# backend/utils/fileio.py
import json
import os

class FileIO:
    def save_json(self, path: str, data: dict):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load_json(self, path: str, default=None):
        if not os.path.exists(path):
            return default
        with open(path, "r") as f:
            return json.load(f)

fileio = FileIO()


    logger.py
    mailer.py
    fileio.py
  main.py