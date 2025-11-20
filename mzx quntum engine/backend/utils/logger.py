# backend/utils/logger.py
import datetime

class Logger:
    def log(self, message: str):
        ts = datetime.datetime.utcnow().isoformat()
        print(f"[LOG] {ts} :: {message}")

logger = Logger()