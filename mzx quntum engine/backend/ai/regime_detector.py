# backend/ai/regime_detector.py
import numpy as np

class RegimeDetector:
    def __init__(self, window=50):
        self.window = window
        self.history = []
        self.last_regime = "range"

    def update(self, price):
        if price is None:
            return self.last_regime
        self.history.append(price)
        if len(self.history) > self.window:
            self.history.pop(0)
        if len(self.history) < 10:
            return self.last_regime

        vol = np.std(self.history)
        slope = np.polyfit(range(len(self.history)), self.history, 1)[0]

        if abs(slope) > 0.5 and vol < 3:
            self.last_regime = "trend"
        elif vol < 1:
            self.last_regime = "compression"
        elif vol > 5:
            self.last_regime = "expansion"
        else:
            self.last_regime = "range"
        return self.last_regime