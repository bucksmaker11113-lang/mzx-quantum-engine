# backend/ai/confidence_model.py
import numpy as np

class ConfidenceModel:
    def __init__(self):
        self.last_conf = 0.5

    def compute(self, smc, mc, regime, spread_state):
        score = 0
        weight = 0

        if smc.get("bias") in ["long", "short"]:
            score += 0.3
        weight += 0.3

        mc_vol = mc.get("vol", 0.02)
        mc_stability = max(0, 1 - mc_vol)
        score += mc_stability * 0.3
        weight += 0.3

        if regime in ["trend", "compression"]:
            score += 0.2
        weight += 0.2

        if spread_state == "tight":
            score += 0.2
        elif spread_state == "wide":
            score += 0.05
        weight += 0.2

        self.last_conf = float(np.clip(score / weight, 0.0, 1.0))
        return self.last_conf

    def status(self):
        return {"confidence": self.last_conf}