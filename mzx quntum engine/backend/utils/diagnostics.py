 backend/utils/diagnostics.py
import time
import psutil
import os

class Diagnostics:
    def __init__(self):
        self.last_snapshot = {}

    def snapshot(self):
        proc = psutil.Process(os.getpid())
        cpu = psutil.cpu_percent(interval=0.1)
        mem = proc.memory_info().rss / (1024*1024)
        th = proc.num_threads()
        ts = time.time()

        snap = {
            "timestamp": ts,
            "cpu": cpu,
            "mem_mb": round(mem,2),
            "threads": th
        }
        self.last_snapshot = snap
        return snap

diagnostics = Diagnostics()