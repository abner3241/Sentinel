# services/bybit_client.py

import os
import time
import hmac
import httpx
import asyncio
import hashlib
from pybit.unified_trading import HTTP as BybitHTTP


class BybitClient:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.getenv("BYBIT_API_KEY")
        self.api_secret = api_secret or os.getenv("BYBIT_API_SECRET")
        self.testnet = os.getenv("BYBIT_TESTNET", "false").lower() == "true"

        self.base_url = "https://api-testnet.bybit.com" if self.testnet else "https://api.bybit.com"
        self._client = BybitHTTP(api_key=self.api_key, api_secret=self.api_secret)

    async def get_balance(self):
        """Consulta saldo com autenticação manual (API v5)."""
        recv_window = 5000
        timestamp = int(time.time() * 1000)
        params = f"api_key={self.api_key}&recv_window={recv_window}&timestamp={timestamp}"
        signature = hmac.new(self.api_secret.encode(), params.encode(), hashlib.sha256).hexdigest()
        url = f"{self.base_url}/v5/account/wallet-balance?{params}&sign={signature}"
        headers = {"X-BAPI-SIGN-TYPE": "2"}

        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers)
            return resp.json()

    async def get_klines(self, symbol: str, interval: str = "1m", limit: int = 200):
        return await asyncio.to_thread(
            self._client.query_kline,
            symbol=symbol,
            interval=interval,
            limit=limit
        )

    async def get_price(self, symbol: str) -> float:
        tick = await asyncio.to_thread(self._client.latest_information_for_symbol, symbol=symbol)
        return float(tick['result'][0]['last_price'])

    async def place_order(self, symbol: str, side: str, qty: float, price: float = None, order_type: str = "Market"):
        params = {
            "symbol": symbol,
            "side": side.capitalize(),
            "order_type": order_type.capitalize(),
            "qty": qty,
            "time_in_force": "GoodTillCancel"
        }
        if price:
            params["price"] = price
        return await asyncio.to_thread(self._client.place_order, **params)

    async def place_limit_order(self, symbol: str, side: str, qty: float, price: float):
        return await self.place_order(symbol, side, qty, price=price, order_type="Limit")

    async def modify_order_stop(self, order_id: str, stop_price: float):
        return await asyncio.to_thread(self._client.modify_order, order_id=order_id, stop_loss=stop_price)

    async def get_trading_symbols(self):
        info = await asyncio.to_thread(self._client.get_instruments_info, category="linear")
        return [s['symbol'] for s in info['result']['list']]
