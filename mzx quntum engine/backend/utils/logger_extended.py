# backend/utils/logger_extended.py
import datetime

class LoggerExtended:
    def log(self, msg: str):
        ts = datetime.datetime.utcnow().isoformat()
        print(f"[LOGX] {ts} :: {msg}")

logger_ext = LoggerExtended()


# backend/pipeline/diagnostic_layer.py
from backend.utils.diagnostics import diagnostics
from backend.utils.tracer import tracer
from backend.utils.logger_extended import logger_ext

class DiagnosticLayer:
    def __init__(self):
        self.enabled = True

    def before_tick(self):
        tracer.mark("tick_start")

    def after_tick(self):
        tracer.mark("tick_end")
        snap = diagnostics.snapshot()
        logger_ext.log(f"CPU={snap['cpu']}% MEM={snap['mem_mb']}MB THREADS={snap['threads']}")

    def export(self):
        return {
            "system": diagnostics.last_snapshot,
            "trace": tracer.export()
        }

diagnostic_layer = DiagnosticLayer()

