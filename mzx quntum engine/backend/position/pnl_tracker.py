# backend/position/pnl_tracker.py
class PnLTracker:
    def __init__(self):
        self.unrealized = 0

    def update_unrealized(self, entry, current, direction):
        if entry is None or current is None:
            return 0
        diff = current - entry
        self.unrealized = diff if direction == "LONG" else -diff
        return self.unrealized

    def get_unrealized(self):
        return self.unrealized