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
            "id": f"order_{len(self.orders)}",
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

    def get_price(self, symbol: str):
        """
        Retorna um preço simulado para o ativo.
        """
        return random.uniform(20000, 30000)

    def get_trading_symbols(self):
        """
        Retorna uma lista de símbolos simulados.
        """
        return ["BTCUSDT", "ETHUSDT"]

    def place_limit_order(self, symbol, side, qty, price):
        """
        Simula ordem limite.
        """
        order = {
            "id": f"limit_{len(self.orders)}",
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "price": price,
            "type": "limit",
            "status": "open"
        }
        self.orders.append(order)
        return order

    def modify_order_stop(self, order_id, stop_price):
        """
        Simula modificação de stop.
        """
        return {"id": order_id, "new_stop": stop_price}
