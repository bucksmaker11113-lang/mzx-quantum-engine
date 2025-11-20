# backend/ai/master_decision.py
import numpy as np

class MasterDecision:
    def __init__(self):
        self.last_decision = "wait"
        self.last_reason = "boot"

    def evaluate(self, prices, liquidity, spread_value, bias, volatility, confidence, regime):
        eth = prices.get("ETHUSDC")
        btc = prices.get("BTCUSDC")

        if eth is None:
            return {"decision": "wait", "reason": "No price"}

        reasons = []
        score_long = 0
        score_short = 0

        # ----------- BIAS -----------
        if bias == "long":
            score_long += 1.0; reasons.append("HybridBias LONG")
        elif bias == "short":
            score_short += 1.0; reasons.append("HybridBias SHORT")
        else:
            reasons.append("HybridBias NEUTRAL")

        # ----------- REGIME -----------
        if regime == "trend":
            score_long += 0.5; reasons.append("Trend regime")
        elif regime == "compression":
            score_short += 0.3; reasons.append("Compression regime")
        elif regime == "expansion":
            score_long += 0.2; reasons.append("Expansion regime")

        # ----------- SPREAD -----------
        if spread_value < 0.5:
            score_long += 0.2
            reasons.append("Tight spread – good for long")
        elif spread_value > 2.0:
            score_short += 0.2
            reasons.append("Wide spread – short bias")

        # ----------- VOLATILITY -----------
        if volatility < 0.015:
            score_long += 0.3; reasons.append("Low vol – stable long entry")
        elif volatility > 0.04:
            score_short += 0.4; reasons.append("High vol – avoid longs")

        # ----------- CONFIDENCE -----------
        if confidence > 0.65:
            score_long += 0.25; reasons.append("High confidence")
        elif confidence < 0.35:
            score_short += 0.2; reasons.append("Low confidence → short bias")

        # ----------- FINAL DECISION -----------
        if score_long - score_short > 0.6:
            self.last_decision = "long"
        elif score_short - score_long > 0.6:
            self.last_decision = "short"
        else:
            self.last_decision = "wait"

        self.last_reason = ", ".join(reasons)

        return {
            "decision": self.last_decision,
            "reason": self.last_reason,
            "scores": {"long": score_long, "short": score_short},
        }