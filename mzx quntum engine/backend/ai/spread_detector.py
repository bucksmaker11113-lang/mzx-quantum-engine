# backend/ai/spread_detector.py
class SpreadDetector:
    def __init__(self, threshold=0.8):
        self.threshold = threshold
        self.last_spread = 0
        self.status_text = "normal"

    def update(self, spread_value):
        self.last_spread = spread_value
        if spread_value < self.threshold:
            self.status_text = "tight"
        elif spread_value < self.threshold * 2:
            self.status_text = "normal"
        else:
            self.status_text = "wide"
        return self.status_text

    def status(self):
        return {"spread": self.last_spread, "condition": self.status_text}