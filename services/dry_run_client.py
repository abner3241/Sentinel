# services/dry_run_client.py

import asyncio
import random
from typing import List, Dict, Optional
from uuid import uuid4


class DryRunClient:
    def __init__(self, *args, **kwargs):
        self._balance = 1000.0  # Saldo inicial simulado
        self.orders: List[Dict] = []

    async def get_klines(self, symbol: str, interval: str = "1m", limit: int = 500) -> List[List[float]]:
        """
        Gera candles simulados com valores OHLC aleatórios.
        """
        candles = []
        base = random.uniform(100, 200)
        for _ in range(limit):
            o = base + random.uniform(-1, 1)
            h = o + random.uniform(0, 2)
            l = o - random.uniform(0, 2)
            c = random.uniform(l, h)
            candles.append([0, o, h, l, c, 100])  # [timestamp, open, high, low, close, volume]
        return candles

    async def place_order(
        self,
        symbol: str,
        side: str,
        qty: float,
        price: Optional[float] = None,
        order_type: str = "market"
    ) -> Dict:
        """
        Simula uma ordem de mercado preenchida.
        """
        order = {
            "id": f"order_{uuid4().hex[:8]}",
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price or "market",
            "type": order_type,
            "status": "filled"
        }
        self.orders.append(order)
        return order

    async def get_balance(self) -> Dict[str, float]:
        """
        Retorna o saldo simulado da conta.
        """
        return {"balance": self._balance}

    def get_price(self, symbol: str) -> float:
        """
        Retorna um preço simulado atual para o ativo.
        """
        return round(random.uniform(20000, 30000), 2)

    def get_trading_symbols(self) -> List[str]:
        """
        Retorna os símbolos simulados disponíveis.
        """
        return ["BTCUSDT", "ETHUSDT"]

    def place_limit_order(self, symbol: str, side: str, qty: float, price: float) -> Dict:
        """
        Simula uma ordem limite.
        """
        order = {
            "id": f"limit_{uuid4().hex[:8]}",
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "type": "limit",
            "status": "open"
        }
        self.orders.append(order)
        return order

    def modify_order_stop(self, order_id: str, stop_price: float) -> Dict:
        """
        Simula a modificação do preço de stop de uma ordem existente.
        """
        return {"id": order_id, "new_stop": stop_price}
