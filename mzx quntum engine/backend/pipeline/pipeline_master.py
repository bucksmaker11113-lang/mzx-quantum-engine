# ===============================
# backend/pipeline/pipeline_master.py — FULL PRO VERSION (FULL FILE)
# ===============================

# backend/pipeline/pipeline_master.py
import asyncio
import time
from backend.core.market_feed import MarketFeed
from backend.core.exchange_client import BinanceClient
from backend.ai.smc_engine import SMCEngine
from backend.ai.montecarlo import MonteCarloEngine
from backend.ai.hybrid_bias import HybridBias
from backend.ai.regime_detector import RegimeDetector
from backend.ai.spread_detector import SpreadDetector
from backend.ai.confidence_model import ConfidenceModel
from backend.ai.hft_detector import HFTDetector
from backend.ai.master_decision import MasterDecision
from backend.ai.fusion_filter import FusionFilter
from backend.position.manager import PositionManager
from backend.position.pnl_tracker import PnLTracker
from backend.position.stop_engine import StopEngine
from backend.risk.position_sizing import PositionSizing
from backend.risk.volatility_model import VolatilityModel
from backend.state.global_state import GlobalState
from backend.utils.logger import logger

class PipelineMaster:
    """
    FULL PRO VERSION — INSTITUTIONAL AI ENGINE

    - REST + WebSocket price sync
    - SMC / Monte Carlo / Hybrid Bias / Regime / Spread / Confidence / HFT
    - Fusion Decision Engine v4
    - FusionFilter institutional risk layer
    - Auto position engine + SL/TP model
    - Volatility‑adaptive stop logic
    - Event logging, diagnostics
    """

    def __init__(self):
        # Market
        self.market = MarketFeed()
        self.client = BinanceClient()

        # AI Modules
        self.smc = SMCEngine()
        self.mc = MonteCarloEngine()
        self.hybrid = HybridBias()
        self.regime = RegimeDetector()
        self.spread = SpreadDetector()
        self.confidence = ConfidenceModel()
        self.hft = HFTDetector()
        self.master = MasterDecision()
        self.fusion = FusionFilter()

        # Position subsystem
        self.pos = PositionManager()
        self.pnl = PnLTracker()
        self.stop = StopEngine()
        self.sizer = PositionSizing()
        self.vol = VolatilityModel()

        # State
        self.state = GlobalState()
        self.last_tick = 0

        logger.log("[INIT] PipelineMaster ready.")

    # ----------------------------
    # PRICE FETCH (REST fallback)
    # ----------------------------
    def load_prices(self):
        try:
            prices = self.market.get_prices() or {}
            if not prices.get("ETHUSDC"):
                logger.log("[WARN] Missing ETH price")
            return prices
        except Exception as e:
            logger.log(f"[ERR] Price fetch failed: {e}")
            return {"ETHUSDC": None, "BTCUSDC": None}

    # ----------------------------
    # SINGLE TICK OF THE ENGINE
    # ----------------------------
    def step(self):
        prices = self.load_prices()
        eth = prices.get("ETHUSDC")
        btc = prices.get("BTCUSDC")

        # If no price → halt
        if eth is None:
            return {
                "decision": "wait",
                "reason": "no_price",
                "position": self.pos.get_state(),
                "events": self.state.last_event_log,
            }

        # ---------------------------
        # AI Modules
        # ---------------------------
        smc_res = self.smc.detect(prices)
        mc_res = self.mc.probability(prices)
        regime_res = self.regime.update(eth)
        spread_v = self.market.get_spread("ETHUSDC") or 0
        spread_res = self.spread.update(spread_v)
        conf_res = self.confidence.compute(smc_res, mc_res, regime_res, spread_res)
        hft_res = self.hft.update(eth)
        vol_value = self.vol.update(eth)

        # Fusion filter layer
        fusion_score = self.fusion.compute(
            confidence=conf_res,
            spread_state=spread_res,
            vol=vol_value,
            liquidity_map=self.market.get_liquidity("ETHUSDC"),
            hft_status=hft_res,
            regime=regime_res,
        )

        allow, reason_sanity = self.fusion.sanity_check(
            bias=smc_res.get("bias"),
            fusion_score=fusion_score,
            hft_status=hft_res,
            vol=vol_value,
        )

        if not allow:
            decision = "wait"
            reason = f"sanity_block: {reason_sanity}"
        else:
            # MASTER DECISION v4
            res = self.master.evaluate(
                prices=prices,
                liquidity=self.market.get_liquidity("ETHUSDC"),
                spread_value=spread_v,
                bias=smc_res.get("bias"),
                volatility=mc_res.get("vol", 0.01),
                confidence=conf_res,
                regime=regime_res,
            )
            decision = res.get("decision", "wait")
            reason = res.get("reason", "none") + f" | fusion={fusion_score:.2f}"

        # ---------------------------
        # POSITION ENGINE
        # ---------------------------
        current = self.pos.get_state()

        if current["status"] == "FLAT":
            if decision in ["long", "short"]:
                size = self.sizer.size(300, max(vol_value, 0.001))
                sl = self.stop.compute_sl(entry=eth, direction=decision.upper())

                if decision == "long": self.pos.open_long(eth)
                else: self.pos.open_short(eth)

                logger.log(f"[OPEN] {decision.upper()} @ {eth} | SL={sl} | size={size}")

        else:
            # manage existing
            entry = current.get("entry")
            direction = current.get("direction")
            self.pnl.update_unrealized(entry, eth, direction)

            # opposite → exit
            if decision != direction.lower():
                logger.log(f"[CLOSE] {direction} @ {eth} | AI reverse")
                self.pos.close(eth)

        # ---------------------------
        # STATE UPDATE
        # ---------------------------
        self.state.market_data = prices
        self.state.bias = smc_res.get("bias")
        self.state.trend = smc_res.get("trend")
        self.state.vol = vol_value
        self.state.add_event(f"AI: {decision} ({reason})")

        # ---------------------------
        # RETURN PAYLOAD
        # ---------------------------
        return {
            "prices": prices,
            "decision": decision,
            "reason": reason,
            "bias": smc_res.get("bias"),
            "trend": smc_res.get("trend"),
            "volatility": vol_value,
            "spread": spread_res,
            "regime": regime_res,
            "confidence": conf_res,
            "fusion_score": fusion_score,
            "hft": hft_res,
            "position": self.pos.get_state(),
            "events": self.state.last_event_log,
        }

    # ----------------------------
    # ASYNC PUBLIC WRAPPER
    # ----------------------------
    async def tick(self):
        return await asyncio.to_thread(self.step)

