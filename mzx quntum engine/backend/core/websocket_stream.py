# backend/core/websocket_stream.py
import asyncio, json, os, websockets

class BinanceWebSocket:
    def __init__(self, feed_ref):
        self.feed = feed_ref
        self.mode = os.getenv("MODE", "DEMO")
        self.endpoint = (
            "wss://testnet.binance.vision/ws" if self.mode == "DEMO" else "wss://stream.binance.com:9443/ws"
        )
        self.symbols = ["ethusdc", "btcusdc"]
        asyncio.create_task(self.run())

    async def run(self):
        while True:
            try:
                query = "/".join([f"{s}@ticker" for s in self.symbols])
                url = f"{self.endpoint}/{query}"

                async with websockets.connect(url, ping_interval=20, ping_timeout=20) as socket:
                    while True:
                        msg = await socket.recv()
                        data = json.loads(msg)

                        symbol = data.get("s", "").upper()
                        price = data.get("c", None)

                        if symbol and price:
                            try:
                                self.feed.update_from_ws(symbol, float(price))
                            except:
                                pass

            except Exception as e:
                await asyncio.sleep(3)