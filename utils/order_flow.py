# utils/order_flow.py

import os
from typing import Optional
from exchange_factory import get_exchange


def order_book_imbalance(symbol: str,
                         api_key: str,
                         api_secret: str,
                         depth: int = 10) -> float:
    """
    Calcula o desequilíbrio entre volume de compra e venda no order book.
    Retorna valor entre -1 e 1 (positivo = pressão compradora).
    """
    client = get_exchange('bybit', api_key, api_secret)
    ob = client.get_order_book(symbol=symbol, limit=depth)
    bids = ob.get('bids', [])
    asks = ob.get('asks', [])
    bid_vol = sum(float(b[1]) for b in bids)
    ask_vol = sum(float(a[1]) for a in asks)
    total = bid_vol + ask_vol
    if total == 0:
        return 0.0
    return (bid_vol - ask_vol) / total


def get_order_flow_signal(symbol: str,
                          api_key: str,
                          api_secret: str,
                          depth: int = 10,
                          threshold: float = 0.1) -> Optional[str]:
    """
    Converte imbalance em sinal discreto:
    - 'buy' se imbalance > threshold
    - 'sell' se imbalance < -threshold
    - None se neutro
    """
    imb = order_book_imbalance(symbol, api_key, api_secret, depth)
    if imb > threshold:
        return 'buy'
    elif imb < -threshold:
        return 'sell'
    return None


def compute_candle_delta(symbol: str, limit: int = 200) -> float:
    """
    Calcula o delta de fluxo de ordens recentes:
    - Positivo: dominância de compras
    - Negativo: dominância de vendas
    """
    client = get_exchange('bybit', os.getenv('BYBIT_API_KEY'), os.getenv('BYBIT_API_SECRET'))
    trades = client.get_trading_records(symbol=symbol, limit=limit)

    records = trades.get('result') if isinstance(trades, dict) else trades
    if not isinstance(records, list):
        return 0.0

    delta = 0.0
    for t in records:
        size = float(t.get('size', t.get('qty', 0)))
        side = str(t.get('side', '')).lower()
        if side == 'buy':
            delta += size
        elif side == 'sell':
            delta -= size
    return delta
