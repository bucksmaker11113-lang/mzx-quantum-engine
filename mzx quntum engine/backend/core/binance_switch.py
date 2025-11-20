# backend/core/binance_switch.py
import os
from backend.core.exchange_client import BinanceClient
from backend.core.env_loader import load_env_settings

class BinanceSwitch:
    def __init__(self):
        self.settings = load_env_settings()
        self.client = None
        self.apply()

    def apply(self):
        """Applies current DEMO/LIVE mode + keys to BinanceClient safely"""
        os.environ["MODE"] = self.settings["mode"]
        os.environ["BINANCE_API_KEY"] = self.settings["api_key"]
        os.environ["BINANCE_API_SECRET"] = self.settings["api_secret"]

        self.client = BinanceClient()  # re-init with new env

    def set_mode(self, mode):
        self.settings["mode"] = mode
        self.apply()

    def update_keys(self, key, secret):
        self.settings["api_key"] = key
        self.settings["api_secret"] = secret
        self.apply()

    def save(self):
        return save_env_settings(self.settings)