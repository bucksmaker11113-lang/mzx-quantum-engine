# backend/integration/settings_binding.py
from backend.core.binance_switch import BinanceSwitch
from backend.core.env_loader import save_env_settings

switcher = BinanceSwitch()

async def bind_settings(data):
    """
    Updates API keys, mode, symbol, leverage, email
    and persists config.json
    """
    mode = data.get("mode", "DEMO")
    key = data.get("api_key", "")
    secret = data.get("api_secret", "")
    symbol = data.get("symbol", "ETHUSDC")
    lev = int(data.get("lev", 5))
    email = data.get("email", "")

    switcher.settings.update({
        "mode": mode,
        "api_key": key,
        "api_secret": secret,
        "symbol": symbol,
        "lev": lev,
        "email": email
    })

    switcher.apply()
    save_env_settings(switcher.settings)

    return {"saved": True, "mode": mode}