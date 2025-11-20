
# backend/position/stop_engine.py
class StopEngine:
    def __init__(self, base_sl=0.003):  # 0.3%
        self.base_sl = base_sl

    def compute_sl(self, entry, direction):
        if direction == "LONG":
            return round(entry * (1 - self.base_sl), 5)
        else:
            return round(entry * (1 + self.base_sl), 5)