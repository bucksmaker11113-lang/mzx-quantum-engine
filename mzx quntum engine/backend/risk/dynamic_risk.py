# backend/risk/dynamic_risk.py
import numpy as np

class DynamicRisk:
    def __init__(self, base_risk=0.01):
        self.base_risk = base_risk
        self.last_risk = base_risk

    def compute(self, volatility):
        if volatility < 1:
            self.last_risk = self.base_risk * 0.5
        elif volatility < 3:
            self.last_risk = self.base_risk
        else:
            self.last_risk = self.base_risk * 1.5
        return self.last_risk

    def status(self):
        return {"risk": self.last_risk}