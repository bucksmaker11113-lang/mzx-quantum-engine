# backend/state/global_state.py
class GlobalState:
    def __init__(self):
        self.market_data = {}
        self.bias = "neutral"
        self.trend = "range"
        self.vol = 0.0
        self.settings = {}
        self.last_event_log = []

    def add_event(self, msg):
        self.last_event_log.append(msg)
        if len(self.last_event_log) > 50:
            self.last_event_log.pop(0)