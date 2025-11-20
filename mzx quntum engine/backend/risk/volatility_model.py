# backend/risk/volatility_model.py
import numpy as np

class VolatilityModel:
    def __init__(self, window=20):
        self.window = window
        self.history = []
        self.last_vol = 0

    def update(self, price: float):
        if price is None:
            return self.last_vol
        self.history.append(price)
        if len(self.history) > self.window:
            self.history.pop(0)
        if len(self.history) < 5:
            return self.last_vol
        self.last_vol = float(np.std(self.history))
        return self.last_vol