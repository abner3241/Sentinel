# services/binance_client.py

import asyncio
import requests


class BinanceClient:
    def __init__(self, *args, **kwargs):
        # Cliente simples baseado na API pública da Binance
        self.base_url = "https://api.binance.com"

    async def get_klines(self, symbol: str, interval: str = "1m", limit: int = 500):
        """
        Retorna candles (klines) da Binance usando a API pública.
        """
        url = f"{self.base_url}/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        return await asyncio.to_thread(lambda: requests.get(url, params=params).json())

    async def place_order(self, *args, **kwargs):
        """
        Placeholder: BinanceClient não implementa ordens nesta versão.
        """
        raise NotImplementedError("place_order não implementado para BinanceClient")

    async def get_balance(self):
        """
        Placeholder: saldo não disponível via API pública da Binance.
        """
        return {"balance": "N/A (BinanceClient não autenticado)"}
