# backend/core/exchange_client.py
import os, requests

class BinanceClient:
    def __init__(self):
        self.mode = os.getenv("MODE", "DEMO")
        self.api_key = os.getenv("BINANCE_API_KEY", "")
        self.api_secret = os.getenv("BINANCE_API_SECRET", "")
        self.base = (
            "https://testnet.binance.vision" if self.mode == "DEMO" else "https://api.binance.com"
        )

    def get_prices(self):
        try:
            r = requests.get(f"{self.base}/api/v3/ticker/price")
            data = r.json()
            prices = {}
            for d in data:
                if d["symbol"] in ["ETHUSDC", "BTCUSDC"]:
                    prices[d["symbol"]] = float(d["price"])
            return prices
        except Exception:
            return None