
import asyncio
from datetime import datetime
from services.exchange_factory import ExchangeFactory

class DataCollector:
    def __init__(self):
        self.client = ExchangeFactory.get_client()

    async def get_historical(self, symbol: str, interval: str = "1m", start: datetime = None, end: datetime = None):
        return await self.client.get_klines(symbol=symbol, interval=interval, limit=500)

    async def get_order_book(self, symbol: str, limit: int = 100):
        return await self.client._client.orderbook(symbol=symbol, limit=limit)
