# backend/risk/position_sizing.py
class PositionSizing:
    def __init__(self, base_risk=0.01):
        self.base_risk = base_risk

    def size(self, balance: float, vol: float):
        if vol <= 0:
            return balance * self.base_risk
        return max(1, balance * self.base_risk / vol)