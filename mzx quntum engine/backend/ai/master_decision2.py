def __init__(self):
        self.last_decision = "wait"
        self.last_reason = "init"

    # --------------------------------------------------
    # 1) FUSION MATRIX
    # --------------------------------------------------
    def fusion_matrix(self, bias, mc, regime, vol, conf):
        score_long = 0
        score_short = 0

        # Hybrid Bias → legerősebb komponens
        if bias == "long": score_long += 2.2
        if bias == "short": score_short += 2.2

        # Monte Carlo trend / reversal
        score_long += mc.get("trend", 0) * 1.4
        score_short += mc.get("reversal", 0) * 1.4

        # Regime alignment
        if regime == "trend": score_long += 1.0
        if regime == "expansion": score_long += 0.5
        if regime == "compression": score_short += 0.6

        # Volatility guard
        if vol > 5:
            score_short += 0.3
        elif vol < 1.0:
            score_long += 0.2

        # Confidence reinforcement
        score_long += conf * 0.8
        score_short += (1 - conf) * 0.8

        return score_long, score_short


    # --------------------------------------------------
    # 2) CONFLICT RESOLVER
    # --------------------------------------------------
    def resolve_conflict(self, sl, ss):
        diff = abs(sl - ss)
        if diff < 0.6:
            return "wait", "conflict: too close"
        return None, None


    # --------------------------------------------------
    # 3) ANTI-FAKEOUT LOGIC
    # --------------------------------------------------
    def anti_fakeout(self, regime, vol, spread_state):
        if regime == "compression" and vol < 1.2:
            return True
        if spread_state == "wide":
            return True
        return False


    # --------------------------------------------------
    # 4) SMART MOMENTUM FILTER
    # --------------------------------------------------
    def momentum_filter(self, mc):
        trend = mc.get("trend", 0)
        rev = mc.get("reversal", 0)
        if trend > 0.62: return "long"
        if rev > 0.62: return "short"
        return "neutral"


    # --------------------------------------------------
    # 5) FUSION ENGINE DECISION
    # --------------------------------------------------
    def evaluate(self, prices, liquidity, spread_value, bias, volatility, confidence, regime):
        # Monte Carlo fallback for internal logic (external MC already computed)
        mc_trend = 0.5
        mc_rev = 0.5
        if "MonteCarlo" in prices:
            mc_trend = prices["MonteCarlo"].get("trend", 0.5)
            mc_rev = prices["MonteCarlo"].get("reversal", 0.5)

        mc = {"trend": mc_trend, "reversal": mc_rev}

        # FUSION MATRIX
        sl, ss = self.fusion_matrix(bias, mc, regime, volatility, confidence)

        # Conflict
        d, r = self.resolve_conflict(sl, ss)
        if d:
            self.last_decision = d
            self.last_reason = r
            return {"decision": d, "reason": r, "bias": bias}

        # Anti-fakeout
        if self.anti_fakeout(regime, volatility, "tight" if spread_value < 0.5 else "wide"):
            self.last_decision = "wait"
            self.last_reason = "anti-fakeout"
            return {"decision": "wait", "reason": "anti-fakeout", "bias": bias}

        # Momentum filter
        mom = self.momentum_filter(mc)
        if mom == "long": sl += 0.4
        if mom == "short": ss += 0.4

        # Final decision
        if sl > ss:
            self.last_decision = "long"
            self.last_reason = "fusion-long"
        else:
            self.last_decision = "short"
            self.last_reason = "fusion-short"

        return {
            "decision": self.last_decision,
            "reason": self.last_reason,
            "bias": bias
        }

    def status(self):
        return {
            "decision": self.last_decision,
            "reason": self.last_reason
        }
