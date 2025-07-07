# services/dry_run_client.py

import asyncio
import random


class DryRunClient:
    def __init__(self, *args, **kwargs):
        self._balance = 1000.0  # Saldo inicial simulado
        self.orders = []

    async def get_klines(self, symbol: str, interval: str = "1m", limit: int = 500):
        """
        Gera candles simulados com valores aleatórios.
        """
        candles = []
        base = random.uniform(100, 200)
        for _ in range(limit):
            o = base + random.uniform(-1, 1)
            h = o + random.uniform(0, 2)
            l = o - random.uniform(0, 2)
            c = random.uniform(l, h)
            candles.append([0, o, h, l, c, 100])
        return candles

    async def place_order(self, symbol: str, side: str, qty: float, price: float = None, order_type: str = "Market"):
        """
        Simula uma ordem colocada e armazena localmente.
        """
        order = {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price or "market",
            "status": "filled"
        }
        self.orders.append(order)
        return order

    async def get_balance(self):
        """
        Retorna o saldo simulado.
        """
        return {"balance": self._balance}
