# backend/ai/hft_detector.py
import numpy as np

class HFTDetector:
    def __init__(self, window=20, threshold=2.5):
        self.window = window
        self.threshold = threshold
        self.history = []
        self.last_status = "NO SPIKE"
        self.last_intensity = 0.0

    def update(self, price):
        if price is None:
            return self.last_status
        self.history.append(price)
        if len(self.history) > self.window:
            self.history.pop(0)
        if len(self.history) < 5:
            return self.last_status
        diffs = np.diff(self.history)
        noise = np.std(diffs)
        intensity = noise / max(1e-9, np.mean(np.abs(diffs)))
        self.last_intensity = float(intensity)
        if intensity > self.threshold * 1.5:
            self.last_status = "HFT SPIKE"
        elif intensity > self.threshold:
            self.last_status = "POSSIBLE SPIKE"
        else:
            self.last_status = "NO SPIKE"
        return self.last_status