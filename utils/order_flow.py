from typing import Optional
from exchange_factory import get_exchange

def order_book_imbalance(symbol: str,
                         api_key: str,
                         api_secret: str,
                         depth: int = 10) -> float:
    """Calcula o desequilíbrio de volume no book (bid vs ask)."""
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
    """Retorna 'buy' se imbalance > threshold, 'sell' se < -threshold, senão None."""
    imb = order_book_imbalance(symbol, api_key, api_secret, depth)
    if imb > threshold:
        return 'buy'
    if imb < -threshold:
        return 'sell'
    return None


def compute_candle_delta(symbol: str, limit: int = 200) -> float:
    """Calcula delta de volume comprador vs. vendedor nos últimos `limit` trades."""
    from exchange_factory import get_exchange
    import os
    client = get_exchange('bybit', os.getenv('BYBIT_API_KEY'), os.getenv('BYBIT_API_SECRET'))
    trades = client.get_trading_records(symbol=symbol, limit=limit)
    # trades may have 'result' key or be list directly
    records = trades.get('result', trades if isinstance(trades, list) else [])
    delta = 0.0
    for t in records:
        size = float(t.get('size', t.get('qty', 0)))
        side = t.get('side', '')
        if side.lower() == 'buy':
            delta += size
        elif side.lower() == 'sell':
            delta -= size
    return delta
