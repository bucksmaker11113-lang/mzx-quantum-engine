# backend/ai/smc_engine.py
import numpy as np

class SMCEngine:
    def __init__(self):
        self.last_bias = "neutral"
        self.last_trend = "range"

    def detect(self, prices: dict):
        eth = prices.get("ETHUSDC", 0)
        btc = prices.get("BTCUSDC", 0)
        avg = (eth + btc) / 2 if eth and btc else 0

        structure = {
            "bias": "long" if eth > avg else "short",
            "trend": "trend" if abs(eth - avg) > 5 else "range",
            "smc": {
                "bos": False,
                "choch": False,
                "fvg_up": False,
                "fvg_down": False,
                "sweep": False,
                "displacement": False,
            }
        }

        self.last_bias = structure["bias"]
        self.last_trend = structure["trend"]
        return structure

    def status(self):
        return {"bias": self.last_bias, "trend": self.last_trend, "status": "active"}