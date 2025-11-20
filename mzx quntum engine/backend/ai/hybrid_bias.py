# backend/ai/hybrid_bias.py
class HybridBias:
    def __init__(self):
        self.last_bias = "neutral"
        self.weights = {"smc": 0.35, "mc": 0.35, "regime": 0.15, "spread": 0.10, "confidence": 0.05}

    def compute(self, smc, mc, regime, spread, confidence):
        long_s, short_s = 0, 0

        if smc.get("bias") == "long": long_s += self.weights["smc"]
        if smc.get("bias") == "short": short_s += self.weights["smc"]

        if mc.get("trend", 0) > 0.55: long_s += self.weights["mc"]
        if mc.get("reversal", 0) > 0.55: short_s += self.weights["mc"]

        if regime == "trend": long_s += self.weights["regime"]
        if regime == "compression": short_s += self.weights["regime"]

        if spread < 0.5: long_s += self.weights["spread"]
        else: short_s += self.weights["spread"]

        long_s += confidence * self.weights["confidence"]
        short_s += (1 - confidence) * self.weights["confidence"]

        if long_s - short_s > 0.1:
            self.last_bias = "long"
        elif short_s - long_s > 0.1:
            self.last_bias = "short"
        else:
            self.last_bias = "neutral"

        return self.last_bias

    def status(self):
        return {"bias": self.last_bias}
