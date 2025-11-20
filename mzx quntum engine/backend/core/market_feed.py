# backend/core/market_feed.py
from .exchange_client import BinanceClient
from .websocket_stream import BinanceWebSocket

class MarketFeed:
    def __init__(self):
        self.client = BinanceClient()
        self.ws = BinanceWebSocket(self)
        self.last_prices = {"ETHUSDC": None, "BTCUSDC": None}
        self.last_liquidity = {"ETHUSDC": {"bid": 0, "ask": 0}, "BTCUSDC": {"bid": 0, "ask": 0}}
        self.last_spread = {"ETHUSDC": 0, "BTCUSDC": 0}

    def get_prices(self):
        data = self.client.get_prices()
        if data:
            for sym, p in data.items():
                self.last_prices[sym] = p
        return self.last_prices

    def update_from_ws(self, symbol, price):
        if symbol in self.last_prices:
            self.last_prices[symbol] = price

    def update_liquidity(self, symbol, bid, ask):
        if symbol in self.last_liquidity:
            self.last_liquidity[symbol] = {"bid": bid, "ask": ask}
            self.last_spread[symbol] = abs(ask - bid)

    def get_spread(self, symbol):
        return self.last_spread.get(symbol, 0)

    def get_liquidity(self, symbol):
        return self.last_liquidity.get(symbol, {"bid": 0, "ask": 0})

#