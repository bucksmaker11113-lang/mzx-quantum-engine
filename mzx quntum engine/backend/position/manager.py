# backend/position/manager.py
class PositionManager:
    def __init__(self):
        self.state = {
            "status": "FLAT",
            "direction": None,
            "entry": None,
            "sl": None,
            "tp": None,
            "pnl_unrealized": 0,
        }

    def open_long(self, entry):
        self.state.update({
            "status": "OPEN",
            "direction": "LONG",
            "entry": entry,
        })

    def open_short(self, entry):
        self.state.update({
            "status": "OPEN",
            "direction": "SHORT",
            "entry": entry,
        })

    def close(self, price):
        self.state.update({
            "status": "FLAT",
            "direction": None,
            "entry": None,
            "sl": None,
            "tp": None,
            "pnl_unrealized": 0,
        })

    def get_state(self):
        return self.state

    def status(self):
        return self.state