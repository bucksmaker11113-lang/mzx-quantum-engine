# backend/utils/tracer.py
import time

class Tracer:
    def __init__(self):
        self.records = []
        self.max_records = 200

    def mark(self, label: str):
        entry = {
            "time": time.time(),
            "label": label
        }
        self.records.append(entry)
        if len(self.records) > self.max_records:
            self.records.pop(0)

    def export(self):
        return self.records

tracer = Tracer()