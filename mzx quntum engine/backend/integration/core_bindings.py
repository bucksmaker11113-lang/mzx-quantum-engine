# backend/integration/core_bindings.py
from backend.core.market_feed import MarketFeed
from backend.core.exchange_client import BinanceClient
from backend.core.websocket_stream import BinanceWebSocket
from backend.ai.smc_engine import SMCEngine
from backend.ai.montecarlo import MonteCarloEngine
from backend.ai.hybrid_bias import HybridBias
from backend.ai.regime_detector import RegimeDetector
from backend.ai.spread_detector import SpreadDetector
from backend.ai.confidence_model import ConfidenceModel
from backend.ai.hft_detector import HFTDetector
from backend.ai.master_decision import MasterDecision
from backend.risk.dynamic_risk import DynamicRisk
from backend.position.manager import PositionManager
from backend.position.pnl_tracker import PnLTracker
from backend.state.global_state import GlobalState

market = MarketFeed()
client = BinanceClient()
ws = BinanceWebSocket(market)
smc = SMCEngine()
mc = MonteCarloEngine()
hybrid = HybridBias()
regime = RegimeDetector()
spread = SpreadDetector()
confidence = ConfidenceModel()
hft = HFTDetector()
risk = DynamicRisk()
pos = PositionManager()
pnl_tracker = PnLTracker()
state = GlobalState()
master = MasterDecision()

async def pipeline_dashboard():
    """Improved 4/10 master pipeline with full AI integration, fallback handling,
    SL/TP management, volatility + risk + hybrid bias integration.
    """
    # --- SAFE PRICE LOAD (REST fallback) ---
    prices = market.get_prices() or {"ETHUSDC": None, "BTCUSDC": None}
    eth = prices.get("ETHUSDC")

    # If still no price → return minimal dashboard
    if eth is None:
        return {
            "prices": prices,
            "decision": "wait",
            "reason": "No price data yet",
            "bias": "neutral",
            "trend": "range",
            "volatility": 0,
            "confidence": 0.5,
            "spread": "unknown",
            "regime": "unknown",
            "hft": {"hft_status": "NO DATA", "intensity": 0},
            "position": pos.get_state(),
            "events": state.last_event_log,
        }

    # --- REGIME ---
    regime_res = regime.update(eth)

    # --- VOLATILITY ---
    vol_value = mc.last_prob.get("vol", 0.02)

    # --- SPREAD ---
    spread_value = market.get_spread("ETHUSDC") or 0
    spread_state = spread.update(spread_value)

    # --- MONTE CARLO ---
    mc_res = mc.probability(prices)

    # --- SMC STRUCTURE ---
    smc_res = smc.detect(prices)

    # --- CONFIDENCE ---
    conf_res = confidence.compute(
        smc_res,
        mc_res,
        regime_res,
        spread_state
    )

    # --- HFT ---
    hft_res = hft.update(eth)

    # --- HYBRID BIAS (REAL MASTER INPUT) ---
    hybrid_bias = hybrid.compute(
        smc_res,
        mc_res,
        regime_res,
        spread_value,
        conf_res
    )

    # --- MASTER DECISION ENGINE ---
    master_out = master.evaluate(
        prices=prices,
        liquidity=market.get_liquidity("ETHUSDC"),
        spread_value=spread_value,
        bias=hybrid_bias,
        volatility=mc_res.get("vol", 0.01),
        confidence=conf_res,
        regime=regime_res
    )

    decision = master_out.get("decision", "wait")
    reason = master_out.get("reason", "none")

    # --- POSITION MANAGER ---
    current = pos.get_state()
    entry_price = eth

    # OPEN POSITION
    if current["status"] == "FLAT":
        if decision == "long":
            pos.open_long(entry_price)
        elif decision == "short":
            pos.open_short(entry_price)

    # MANAGE EXISTING POSITION
    else:
        direction = current["direction"]

        # Opposite → close
        if (direction == "LONG" and decision == "short") or \
           (direction == "SHORT" and decision == "long"):
            pos.close(entry_price)
        else:
            pnl_tracker.update_unrealized(
                current["entry"],
                entry_price,
                direction
            )

    # --- UPDATE GLOBAL STATE ---
    state.market_data = prices
    state.bias = hybrid_bias
    state.trend = smc_res.get("trend", "range")
    state.vol = mc_res.get("vol")
    state.add_event(f"AI: {decision} ({reason})")

    # --- FINAL DASHBOARD OUTPUT ---
    return {
        "prices": prices,
        "decision": decision,
        "reason": reason,
        "bias": hybrid_bias,
        "trend": smc_res.get("trend"),
        "volatility": mc_res.get("vol"),
        "confidence": conf_res,
        "spread": spread_state,
        "regime": regime_res,
        "hft": hft_res,
        "position": pos.get_state(),
        "events": state.last_event_log,
    }
async def pipeline_modules():
    return {
        "smc": smc.status(),
        "mc": mc.status(),
        "hybrid": hybrid.status(),
        "regime": regime.last_regime,
        "spread": spread.status(),
        "confidence": confidence.status(),
        "hft": hft.status(),
        "risk": risk.status(),
        "pos": pos.status(),
    }

async def pipeline_position(): return pos.get_state()
async def pipeline_save_settings(data): state.settings = data; return {"saved": True}
async def pipeline_chat(message): return {"reply": f"AI válasz: {message}"}