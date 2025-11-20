# backend/core/env_loader.py
import os
import json

def load_env_settings():
    """
    Loads API keys, mode (DEMO/LIVE), symbol, leverage
    from both ENV variables and config.json fallback.
    """
    config_path = "config.json"
    cfg = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                cfg = json.load(f)
        except:
            cfg = {}

    settings = {
        "mode": os.getenv("MODE", cfg.get("mode", "DEMO")),
        "api_key": os.getenv("BINANCE_API_KEY", cfg.get("api_key", "")),
        "api_secret": os.getenv("BINANCE_API_SECRET", cfg.get("api_secret", "")),
        "symbol": cfg.get("symbol", "ETHUSDC"),
        "lev": cfg.get("lev", 5),
        "email": cfg.get("email", "")
    }

    return settings


def save_env_settings(data: dict):
    """Persists settings to config.json"""
    try:
        with open("config.json", "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False
