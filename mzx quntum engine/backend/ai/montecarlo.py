# backend/ai/montecarlo.py
import numpy as np
import random

class MonteCarloEngine:
    def __init__(self, simulations=500):
        self.simulations = simulations
        self.last_prob = {"trend": 0.5, "reversal": 0.5, "vol": 0.01}

    def probability(self, prices):
        eth = prices.get("ETHUSDC")
        btc = prices.get("BTCUSDC")
        if not eth or not btc:
            return self.last_prob
        base = (eth + btc) / 2

        trend_count, reversal_count = 0, 0
        vol_acc = []

        for _ in range(self.simulations):
            move = random.uniform(-5, 5)
            simulated = base + move
            if simulated > base:
                trend_count += 1
            else:
                reversal_count += 1
            vol_acc.append(abs(move))

        result = {
            "trend": trend_count / self.simulations,
            "reversal": reversal_count / self.simulations,
            "vol": float(np.mean(vol_acc))
        }
        self.last_prob = result
        return result

    def status(self):
        return self.last_prob