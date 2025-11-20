backend/ai/fusion_filter.py

class FusionFilter:
    def __init__(self):
        self.last_score = 0
        self.last_state = "ok"

    # -----------------------------------------
    # CONFIDENCE + VOL + SPREAD + LIQUIDITY COMBINED INDEX
    # -----------------------------------------
    def compute(self, confidence, spread_state, vol, liquidity_map, hft_status, regime):
        score = 0
        total = 0

        # Confidence → fő súly
        score += confidence * 0.4
        total += 0.4

        # Spread → tight = jó, wide = rossz
        if spread_state == "tight": score += 0.2
        elif spread_state == "normal": score += 0.1
        else: score += 0.02
        total += 0.2

        # Volatility → túl magas vol esetén lassít
        if vol < 0.5:
            score += 0.2
        elif vol < 1.5:
            score += 0.1
        else:
            score += 0.02
        total += 0.2

        # Liquidity → nagy likviditás segíti a fill-t
        liq_score = min(1.0, (liquidity_map.get("bid",0) + liquidity_map.get("ask",0)) / 1000000)
        score += liq_score * 0.15
        total += 0.15

        # HFT spike → zajszűrés
        if hft_status in ["HFT SPIKE", "POSSIBLE SPIKE"]:
            score -= 0.25
        total += 0.05

        # Regime scaling
        if regime == "trend": score += 0.1
        elif regime == "compression": score -= 0.05
        total += 0.05

        final = max(0, min(score / total, 1))
        self.last_score = final
        return final

    # -----------------------------------------
    # SANITY CHECK – ha minden modul össze-vissza jelez, AI STOP
    # -----------------------------------------
    def sanity_check(self, bias, fusion_score, hft_status, vol):
        if fusion_score < 0.25 and hft_status == "HFT SPIKE":
            return False, "Fusion fail + HFT spike"
        if vol > 3:
            return False, "Volatility too high"
        if bias == "neutral" and fusion_score < 0.35:
            return False, "Uncertain neutral state"
        return True, "OK"
